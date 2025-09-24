#!/usr/bin/env python3
"""
Fully Automated Google Cloud OAuth JSON Generator
Supports bulk processing of 100+ emails with retry mechanisms
"""

import os
import sys
import json
import time
import logging
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class BulkOAuthAutomation:
    def __init__(self, output_dir: str = "oauth_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        log_file = self.output_dir / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Results tracking
        self.results = {
            'successful': [],
            'failed': [],
            'total_processed': 0,
            'start_time': datetime.now().isoformat()
        }
        
    def load_accounts(self, file_path: str = "accounts.txt") -> List[Dict[str, str]]:
        """Load email accounts from file"""
        accounts = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            email, password = line.split(':', 1)
                            accounts.append({
                                'email': email.strip(),
                                'password': password.strip(),
                                'line_number': line_num
                            })
                        else:
                            accounts.append({
                                'email': line.strip(),
                                'password': '',
                                'line_number': line_num
                            })
        except FileNotFoundError:
            self.logger.error(f"Accounts file not found: {file_path}")
            return []
        
        self.logger.info(f"Loaded {len(accounts)} accounts from {file_path}")
        return accounts
    
    def check_gcloud_cli(self) -> bool:
        """Check if Google Cloud CLI is installed"""
        try:
            result = subprocess.run(['gcloud', 'version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.logger.info("Google Cloud CLI is installed")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.logger.error("Google Cloud CLI not found. Please install it first.")
        return False
    
    def install_gcloud_cli(self) -> bool:
        """Install Google Cloud CLI automatically"""
        self.logger.info("Installing Google Cloud CLI...")
        try:
            # Download and install Google Cloud CLI
            if os.name == 'nt':  # Windows
                install_cmd = [
                    'powershell', '-Command',
                    '(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:TEMP\\GoogleCloudSDKInstaller.exe"); Start-Process -Wait -FilePath "$env:TEMP\\GoogleCloudSDKInstaller.exe" -ArgumentList "/S"'
                ]
            else:  # Linux/Mac
                install_cmd = [
                    'curl', 'https://sdk.cloud.google.com', '|', 'bash'
                ]
            
            result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Failed to install Google Cloud CLI: {e}")
            return False
    
    def generate_project_name(self, email: str) -> str:
        """Generate unique project name"""
        username = email.split('@')[0]
        timestamp = int(time.time())
        return f"oauth-{username}-{timestamp}"[:30].lower().replace('_', '-')
    
    def authenticate_gcloud(self, email: str) -> bool:
        """Authenticate with Google Cloud using email"""
        try:
            self.logger.info(f"Authenticating with {email}...")
            
            # Login command
            auth_cmd = ['gcloud', 'auth', 'login', '--account', email, '--quiet']
            
            result = subprocess.run(auth_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully authenticated with {email}")
                return True
            else:
                self.logger.error(f"Authentication failed for {email}: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Authentication error for {email}: {e}")
            return False
    
    def create_project(self, project_name: str) -> bool:
        """Create Google Cloud project"""
        try:
            self.logger.info(f"Creating project: {project_name}")
            
            create_cmd = ['gcloud', 'projects', 'create', project_name, '--quiet']
            result = subprocess.run(create_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Set as active project
                set_cmd = ['gcloud', 'config', 'set', 'project', project_name]
                subprocess.run(set_cmd, capture_output=True, text=True, timeout=10)
                
                self.logger.info(f"Project {project_name} created successfully")
                return True
            else:
                self.logger.error(f"Project creation failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Project creation error: {e}")
            return False
    
    def enable_gmail_api(self, project_name: str) -> bool:
        """Enable Gmail API for the project"""
        try:
            self.logger.info(f"Enabling Gmail API for {project_name}")
            
            enable_cmd = ['gcloud', 'services', 'enable', 'gmail.googleapis.com', 
                         '--project', project_name, '--quiet']
            
            result = subprocess.run(enable_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.logger.info("Gmail API enabled successfully")
                return True
            else:
                self.logger.error(f"Failed to enable Gmail API: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Gmail API enable error: {e}")
            return False
    
    def create_oauth_credentials(self, project_name: str, email: str) -> Optional[str]:
        """Create OAuth 2.0 credentials and return JSON content"""
        try:
            self.logger.info(f"Creating OAuth credentials for {project_name}")
            
            # Create OAuth consent screen (simplified)
            consent_cmd = [
                'gcloud', 'alpha', 'iap', 'oauth-brands', 'create',
                '--application_title=Gmail OAuth App',
                '--support_email=' + email,
                '--project=' + project_name,
                '--quiet'
            ]
            
            subprocess.run(consent_cmd, capture_output=True, text=True, timeout=30)
            
            # Create OAuth client
            client_cmd = [
                'gcloud', 'alpha', 'iap', 'oauth-clients', 'create',
                '--display_name=Gmail OAuth Client',
                '--project=' + project_name,
                '--quiet'
            ]
            
            result = subprocess.run(client_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Extract client ID and secret from output
                output_lines = result.stdout.strip().split('\n')
                client_id = None
                client_secret = None
                
                for line in output_lines:
                    if 'Client ID:' in line:
                        client_id = line.split(':', 1)[1].strip()
                    elif 'Client Secret:' in line:
                        client_secret = line.split(':', 1)[1].strip()
                
                if client_id and client_secret:
                    # Generate OAuth JSON
                    oauth_json = {
                        "installed": {
                            "client_id": client_id,
                            "project_id": project_name,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "client_secret": client_secret,
                            "redirect_uris": ["http://localhost"]
                        }
                    }
                    
                    return json.dumps(oauth_json, indent=2)
                
            self.logger.error("Failed to extract OAuth credentials")
            return None
            
        except Exception as e:
            self.logger.error(f"OAuth creation error: {e}")
            return None
    
    def save_oauth_json(self, email: str, json_content: str) -> str:
        """Save OAuth JSON to file"""
        filename = f"oauth_{email.replace('@', '_').replace('.', '_')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_content)
        
        self.logger.info(f"OAuth JSON saved: {filepath}")
        return str(filepath)
    
    def process_single_email(self, account: Dict[str, str], retry_count: int = 3) -> bool:
        """Process a single email account with retry mechanism"""
        email = account['email']
        
        for attempt in range(retry_count):
            try:
                self.logger.info(f"Processing {email} (Attempt {attempt + 1}/{retry_count})")
                
                # Step 1: Authenticate
                if not self.authenticate_gcloud(email):
                    if attempt < retry_count - 1:
                        time.sleep(5)
                        continue
                    return False
                
                # Step 2: Create project
                project_name = self.generate_project_name(email)
                if not self.create_project(project_name):
                    if attempt < retry_count - 1:
                        time.sleep(5)
                        continue
                    return False
                
                # Step 3: Enable Gmail API
                if not self.enable_gmail_api(project_name):
                    if attempt < retry_count - 1:
                        time.sleep(5)
                        continue
                    return False
                
                # Step 4: Create OAuth credentials
                oauth_json = self.create_oauth_credentials(project_name, email)
                if not oauth_json:
                    if attempt < retry_count - 1:
                        time.sleep(5)
                        continue
                    return False
                
                # Step 5: Save JSON file
                json_path = self.save_oauth_json(email, oauth_json)
                
                # Record success
                self.results['successful'].append({
                    'email': email,
                    'project_name': project_name,
                    'json_path': json_path,
                    'processed_at': datetime.now().isoformat()
                })
                
                self.logger.info(f"✅ Successfully processed {email}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error processing {email} (Attempt {attempt + 1}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(10)
                    continue
        
        # Record failure
        self.results['failed'].append({
            'email': email,
            'error': f"Failed after {retry_count} attempts",
            'failed_at': datetime.now().isoformat()
        })
        
        return False
    
    def process_bulk_emails(self, accounts: List[Dict[str, str]], max_concurrent: int = 1) -> Dict:
        """Process multiple emails with rate limiting"""
        total_accounts = len(accounts)
        self.logger.info(f"Starting bulk processing of {total_accounts} accounts")
        
        for i, account in enumerate(accounts, 1):
            self.logger.info(f"\n{'='*50}")
            self.logger.info(f"Processing account {i}/{total_accounts}")
            self.logger.info(f"{'='*50}")
            
            success = self.process_single_email(account)
            self.results['total_processed'] += 1
            
            # Progress update
            success_count = len(self.results['successful'])
            failed_count = len(self.results['failed'])
            
            self.logger.info(f"Progress: {i}/{total_accounts} | Success: {success_count} | Failed: {failed_count}")
            
            # Rate limiting - wait between requests
            if i < total_accounts:
                self.logger.info("Waiting 30 seconds before next account...")
                time.sleep(30)
        
        # Final results
        self.results['end_time'] = datetime.now().isoformat()
        self.save_results()
        
        return self.results
    
    def save_results(self):
        """Save processing results to JSON file"""
        results_file = self.output_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {results_file}")
    
    def print_summary(self):
        """Print processing summary"""
        print(f"\n{'='*60}")
        print("🎯 BULK OAUTH AUTOMATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Processed: {self.results['total_processed']}")
        print(f"✅ Successful: {len(self.results['successful'])}")
        print(f"❌ Failed: {len(self.results['failed'])}")
        print(f"📁 Output Directory: {self.output_dir}")
        
        if self.results['successful']:
            print(f"\n✅ Successful Accounts:")
            for result in self.results['successful']:
                print(f"  - {result['email']} → {result['json_path']}")
        
        if self.results['failed']:
            print(f"\n❌ Failed Accounts:")
            for result in self.results['failed']:
                print(f"  - {result['email']}: {result['error']}")

def main():
    parser = argparse.ArgumentParser(description='Bulk Google OAuth JSON Generator')
    parser.add_argument('--accounts', default='accounts.txt', help='Accounts file path')
    parser.add_argument('--output', default='oauth_results', help='Output directory')
    parser.add_argument('--single', help='Process single email')
    parser.add_argument('--max-concurrent', type=int, default=1, help='Max concurrent processes')
    
    args = parser.parse_args()
    
    # Initialize automation
    automation = BulkOAuthAutomation(args.output)
    
    # Check Google Cloud CLI
    if not automation.check_gcloud_cli():
        print("❌ Google Cloud CLI not found!")
        print("Please install it from: https://cloud.google.com/sdk/docs/install")
        return
    
    if args.single:
        # Process single email
        account = {'email': args.single, 'password': ''}
        success = automation.process_single_email(account)
        if success:
            print(f"✅ Successfully processed {args.single}")
        else:
            print(f"❌ Failed to process {args.single}")
    else:
        # Process bulk emails
        accounts = automation.load_accounts(args.accounts)
        if not accounts:
            print("❌ No accounts found!")
            return
        
        print(f"🚀 Starting bulk processing of {len(accounts)} accounts...")
        results = automation.process_bulk_emails(accounts, args.max_concurrent)
        automation.print_summary()

if __name__ == "__main__":
    main()