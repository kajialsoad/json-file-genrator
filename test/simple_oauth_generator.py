#!/usr/bin/env python3
"""
Simple OAuth JSON Generator for Gmail
Creates OAuth JSON files for bulk email processing
"""

import json
import os
import time
import random
import string
from datetime import datetime
from pathlib import Path

class SimpleOAuthGenerator:
    def __init__(self, output_dir: str = "oauth_json_files"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # OAuth template
        self.oauth_template = {
            "installed": {
                "client_id": "",
                "project_id": "",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "",
                "redirect_uris": ["http://localhost"]
            }
        }
    
    def load_accounts(self, file_path: str = "accounts.txt"):
        """Load email accounts from file"""
        accounts = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            email, password = line.split(':', 1)
                            accounts.append(email.strip())
                        else:
                            accounts.append(line.strip())
        except FileNotFoundError:
            print(f"❌ Accounts file not found: {file_path}")
            return []
        
        print(f"📧 Loaded {len(accounts)} email accounts")
        return accounts
    
    def generate_client_id(self):
        """Generate realistic client ID"""
        numbers = ''.join(random.choices(string.digits, k=12))
        suffix = ''.join(random.choices(string.ascii_lowercase, k=10))
        return f"{numbers}-{suffix}.apps.googleusercontent.com"
    
    def generate_client_secret(self):
        """Generate realistic client secret"""
        chars = string.ascii_letters + string.digits + '-_'
        return ''.join(random.choices(chars, k=24))
    
    def generate_project_id(self, email: str):
        """Generate project ID from email"""
        username = email.split('@')[0]
        timestamp = int(time.time())
        return f"gmail-oauth-{username}-{timestamp}"[:30].lower().replace('_', '-')
    
    def create_oauth_json(self, email: str):
        """Create OAuth JSON for an email"""
        oauth_data = self.oauth_template.copy()
        
        # Generate credentials
        oauth_data["installed"]["client_id"] = self.generate_client_id()
        oauth_data["installed"]["client_secret"] = self.generate_client_secret()
        oauth_data["installed"]["project_id"] = self.generate_project_id(email)
        
        return oauth_data
    
    def save_oauth_file(self, email: str, oauth_data: dict):
        """Save OAuth JSON to file"""
        filename = f"oauth_{email.replace('@', '_').replace('.', '_')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(oauth_data, f, indent=2)
        
        return str(filepath)
    
    def process_single_email(self, email: str):
        """Process single email"""
        print(f"🔄 Processing: {email}")
        
        try:
            oauth_data = self.create_oauth_json(email)
            filepath = self.save_oauth_file(email, oauth_data)
            
            print(f"✅ Created: {filepath}")
            return True, filepath
            
        except Exception as e:
            print(f"❌ Error processing {email}: {e}")
            return False, None
    
    def process_bulk_emails(self, accounts):
        """Process multiple emails"""
        total = len(accounts)
        successful = []
        failed = []
        
        print(f"\n🚀 Starting bulk processing of {total} accounts...")
        print("=" * 60)
        
        for i, email in enumerate(accounts, 1):
            print(f"\n[{i}/{total}] Processing: {email}")
            
            success, filepath = self.process_single_email(email)
            
            if success:
                successful.append({'email': email, 'file': filepath})
            else:
                failed.append(email)
            
            # Progress update
            print(f"Progress: {i}/{total} | Success: {len(successful)} | Failed: {len(failed)}")
            
            # Small delay to avoid overwhelming
            time.sleep(0.5)
        
        return successful, failed
    
    def print_summary(self, successful, failed):
        """Print processing summary"""
        print(f"\n{'=' * 60}")
        print("🎯 OAUTH JSON GENERATION SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Processed: {len(successful) + len(failed)}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"📁 Output Directory: {self.output_dir}")
        
        if successful:
            print(f"\n✅ Successfully Created Files:")
            for result in successful:
                print(f"  - {result['email']} → {Path(result['file']).name}")
        
        if failed:
            print(f"\n❌ Failed Emails:")
            for email in failed:
                print(f"  - {email}")
        
        # Save summary
        summary_file = self.output_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary_data = {
            'total_processed': len(successful) + len(failed),
            'successful_count': len(successful),
            'failed_count': len(failed),
            'successful_files': successful,
            'failed_emails': failed,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\n📊 Summary saved to: {summary_file}")

def main():
    print("🔐 Simple OAuth JSON Generator for Gmail")
    print("=" * 50)
    
    generator = SimpleOAuthGenerator()
    
    # Load accounts
    accounts = generator.load_accounts()
    if not accounts:
        print("❌ No accounts found in accounts.txt")
        return
    
    # Ask for processing type
    print(f"\nFound {len(accounts)} accounts. Choose processing type:")
    print("1. Single email test")
    print("2. Bulk processing (all accounts)")
    
    try:
        choice = input("Enter choice (1/2): ").strip()
        
        if choice == "1":
            # Single email test
            email = accounts[0]
            print(f"\n🧪 Testing with: {email}")
            success, filepath = generator.process_single_email(email)
            
            if success:
                print(f"✅ Test successful! File created: {filepath}")
            else:
                print("❌ Test failed!")
                
        elif choice == "2":
            # Bulk processing
            print(f"\n⚠️  About to process {len(accounts)} accounts.")
            confirm = input("Continue? (y/N): ").strip().lower()
            
            if confirm == 'y':
                successful, failed = generator.process_bulk_emails(accounts)
                generator.print_summary(successful, failed)
            else:
                print("❌ Cancelled by user")
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()