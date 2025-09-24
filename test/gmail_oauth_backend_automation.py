#!/usr/bin/env python3
"""
Gmail OAuth Backend Automation
Automated backend system for Gmail OAuth JSON generation
Works with existing Gmail_OAuth_Generator.exe
"""

import os
import sys
import json
import time
import logging
import subprocess
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chrome as uc

class GmailOAuthBackendAutomation:
    def __init__(self, output_dir: str = "oauth_json_files"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        log_file = self.output_dir / f"backend_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
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
        
        # Browser setup
        self.driver = None
        self.wait = None
        
    def setup_browser(self, headless: bool = False) -> bool:
        """Setup undetected Chrome browser"""
        try:
            self.logger.info("Setting up browser...")
            
            options = uc.ChromeOptions()
            
            if headless:
                options.add_argument('--headless')
            
            # Anti-detection options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Download preferences
            download_dir = str(self.output_dir.absolute())
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 30)
            
            self.logger.info("Browser setup completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Browser setup failed: {e}")
            return False
    
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
    
    def google_login(self, email: str, password: str) -> bool:
        """Login to Google account"""
        try:
            self.logger.info(f"Logging in with {email}...")
            
            # Navigate to Google Cloud Console
            self.driver.get("https://console.cloud.google.com/")
            time.sleep(3)
            
            # Check if already logged in
            try:
                # Look for sign in button
                sign_in_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign in')]"))
                )
                sign_in_btn.click()
                time.sleep(2)
            except TimeoutException:
                # Already logged in, check if correct account
                try:
                    account_element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{email}')]")
                    self.logger.info(f"Already logged in with {email}")
                    return True
                except NoSuchElementException:
                    # Wrong account, need to switch
                    self.logger.info("Wrong account detected, switching...")
                    pass
            
            # Enter email
            try:
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "identifierId"))
                )
                email_input.clear()
                email_input.send_keys(email)
                
                next_btn = self.driver.find_element(By.ID, "identifierNext")
                next_btn.click()
                time.sleep(3)
            except TimeoutException:
                self.logger.error("Email input field not found")
                return False
            
            # Enter password
            try:
                password_input = self.wait.until(
                    EC.element_to_be_clickable((By.NAME, "password"))
                )
                password_input.clear()
                password_input.send_keys(password)
                
                password_next = self.driver.find_element(By.ID, "passwordNext")
                password_next.click()
                time.sleep(5)
            except TimeoutException:
                self.logger.error("Password input field not found")
                return False
            
            # Check for 2FA or other verification
            try:
                # Wait for successful login (check for Google Cloud Console elements)
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Google Cloud')]")),
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'console')]")),
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Create')]"))
                    )
                )
                self.logger.info(f"Successfully logged in with {email}")
                return True
                
            except TimeoutException:
                self.logger.error("Login verification failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Login error for {email}: {e}")
            return False
    
    def create_project(self, project_name: str) -> bool:
        """Create new Google Cloud project"""
        try:
            self.logger.info(f"Creating project: {project_name}")
            
            # Navigate to project creation
            self.driver.get("https://console.cloud.google.com/projectcreate")
            time.sleep(3)
            
            # Enter project name
            try:
                project_name_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "p6n-kp-name-input"))
                )
                project_name_input.clear()
                project_name_input.send_keys(project_name)
                time.sleep(1)
            except TimeoutException:
                # Try alternative selector
                try:
                    project_name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='My Project']")
                    project_name_input.clear()
                    project_name_input.send_keys(project_name)
                except NoSuchElementException:
                    self.logger.error("Project name input not found")
                    return False
            
            # Click Create button
            try:
                create_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]"))
                )
                create_btn.click()
                time.sleep(5)
            except TimeoutException:
                self.logger.error("Create button not found")
                return False
            
            # Wait for project creation to complete
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Project created')]")),
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'created')]")),
                        EC.url_contains("console.cloud.google.com")
                    )
                )
                self.logger.info(f"Project {project_name} created successfully")
                return True
                
            except TimeoutException:
                self.logger.error("Project creation timeout")
                return False
                
        except Exception as e:
            self.logger.error(f"Project creation error: {e}")
            return False
    
    def enable_gmail_api(self) -> bool:
        """Enable Gmail API for the project"""
        try:
            self.logger.info("Enabling Gmail API...")
            
            # Navigate to API Library
            self.driver.get("https://console.cloud.google.com/apis/library")
            time.sleep(3)
            
            # Search for Gmail API
            try:
                search_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for APIs & Services']"))
                )
                search_input.clear()
                search_input.send_keys("Gmail API")
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
            except TimeoutException:
                self.logger.error("API search input not found")
                return False
            
            # Click on Gmail API
            try:
                gmail_api_link = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'gmail')]"))
                )
                gmail_api_link.click()
                time.sleep(3)
            except TimeoutException:
                self.logger.error("Gmail API link not found")
                return False
            
            # Enable the API
            try:
                enable_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Enable') or contains(text(), 'ENABLE')]"))
                )
                enable_btn.click()
                time.sleep(5)
                
                # Wait for API to be enabled
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'API enabled')]")),
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Manage')]")),
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'enabled')]"))
                    )
                )
                
                self.logger.info("Gmail API enabled successfully")
                return True
                
            except TimeoutException:
                self.logger.error("Enable button not found or API enable timeout")
                return False
                
        except Exception as e:
            self.logger.error(f"Gmail API enable error: {e}")
            return False
    
    def setup_oauth_consent_screen(self, email: str) -> bool:
        """Setup OAuth consent screen"""
        try:
            self.logger.info("Setting up OAuth consent screen...")
            
            # Navigate to OAuth consent screen
            self.driver.get("https://console.cloud.google.com/apis/credentials/consent")
            time.sleep(3)
            
            # Check if consent screen already exists
            try:
                edit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Edit')]")
                self.logger.info("OAuth consent screen already exists")
                return True
            except NoSuchElementException:
                pass
            
            # Select External user type
            try:
                external_radio = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='EXTERNAL']"))
                )
                external_radio.click()
                time.sleep(1)
                
                create_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
                create_btn.click()
                time.sleep(3)
            except TimeoutException:
                self.logger.error("External user type selection failed")
                return False
            
            # Fill app information
            try:
                # App name
                app_name_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='App name']"))
                )
                app_name_input.clear()
                app_name_input.send_keys("Gmail OAuth App")
                
                # User support email
                support_email_input = self.driver.find_element(By.XPATH, "//input[@aria-label='User support email']")
                support_email_input.clear()
                support_email_input.send_keys(email)
                
                # Developer contact email
                dev_email_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Developer contact information']")
                dev_email_input.clear()
                dev_email_input.send_keys(email)
                
                # Save and continue
                save_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save and Continue')]")
                save_btn.click()
                time.sleep(3)
                
                self.logger.info("OAuth consent screen setup completed")
                return True
                
            except (TimeoutException, NoSuchElementException) as e:
                self.logger.error(f"OAuth consent screen setup failed: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"OAuth consent screen error: {e}")
            return False
    
    def create_oauth_credentials(self, email: str) -> Optional[str]:
        """Create OAuth 2.0 credentials and return download path"""
        try:
            self.logger.info("Creating OAuth credentials...")
            
            # Navigate to credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(3)
            
            # Click Create Credentials
            try:
                create_credentials_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Credentials') or contains(text(), 'CREATE CREDENTIALS')]"))
                )
                create_credentials_btn.click()
                time.sleep(2)
            except TimeoutException:
                self.logger.error("Create Credentials button not found")
                return None
            
            # Select OAuth client ID
            try:
                oauth_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'OAuth client ID')]"))
                )
                oauth_option.click()
                time.sleep(3)
            except TimeoutException:
                self.logger.error("OAuth client ID option not found")
                return None
            
            # Select application type (Desktop application)
            try:
                app_type_dropdown = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']"))
                )
                app_type_dropdown.click()
                time.sleep(1)
                
                desktop_option = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Desktop application')]")
                desktop_option.click()
                time.sleep(1)
            except (TimeoutException, NoSuchElementException):
                self.logger.error("Application type selection failed")
                return None
            
            # Enter name
            try:
                name_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Name']")
                name_input.clear()
                name_input.send_keys(f"Gmail OAuth Client - {email}")
                time.sleep(1)
            except NoSuchElementException:
                self.logger.error("Name input field not found")
                return None
            
            # Create credentials
            try:
                create_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
                create_btn.click()
                time.sleep(5)
            except NoSuchElementException:
                self.logger.error("Create button not found")
                return None
            
            # Download JSON file
            try:
                download_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download JSON') or contains(text(), 'DOWNLOAD JSON')]"))
                )
                download_btn.click()
                time.sleep(3)
                
                self.logger.info("OAuth credentials created and downloaded")
                return "downloaded"
                
            except TimeoutException:
                self.logger.error("Download JSON button not found")
                return None
                
        except Exception as e:
            self.logger.error(f"OAuth credentials creation error: {e}")
            return None
    
    def rename_and_organize_json(self, email: str) -> Optional[str]:
        """Find downloaded JSON file and rename it properly"""
        try:
            # Wait for download to complete
            time.sleep(5)
            
            # Find the most recent JSON file in download directory
            json_files = list(self.output_dir.glob("*.json"))
            if not json_files:
                # Check default download directory
                downloads_dir = Path.home() / "Downloads"
                json_files = list(downloads_dir.glob("client_secret_*.json"))
            
            if json_files:
                # Get the most recent file
                latest_file = max(json_files, key=os.path.getctime)
                
                # Create new filename based on email
                email_safe = email.replace('@', '_').replace('.', '_')
                new_filename = f"gmail_oauth_{email_safe}.json"
                new_path = self.output_dir / new_filename
                
                # Move and rename file
                latest_file.rename(new_path)
                
                self.logger.info(f"JSON file renamed and saved: {new_path}")
                return str(new_path)
            
            self.logger.error("No JSON file found to rename")
            return None
            
        except Exception as e:
            self.logger.error(f"JSON file organization error: {e}")
            return None
    
    def generate_project_name(self, email: str) -> str:
        """Generate unique project name"""
        username = email.split('@')[0]
        timestamp = int(time.time())
        return f"gmail-oauth-{username}-{timestamp}"[:30].lower().replace('_', '-')
    
    def process_single_email(self, account: Dict[str, str]) -> bool:
        """Process a single email account through complete OAuth setup"""
        email = account['email']
        password = account['password']
        
        try:
            self.logger.info(f"Starting OAuth setup for {email}")
            
            # Step 1: Login to Google
            if not self.google_login(email, password):
                return False
            
            # Step 2: Create project
            project_name = self.generate_project_name(email)
            if not self.create_project(project_name):
                return False
            
            # Step 3: Enable Gmail API
            if not self.enable_gmail_api():
                return False
            
            # Step 4: Setup OAuth consent screen
            if not self.setup_oauth_consent_screen(email):
                return False
            
            # Step 5: Create OAuth credentials
            if not self.create_oauth_credentials(email):
                return False
            
            # Step 6: Rename and organize JSON file
            json_path = self.rename_and_organize_json(email)
            if not json_path:
                return False
            
            # Record success
            self.results['successful'].append({
                'email': email,
                'project_name': project_name,
                'json_path': json_path,
                'processed_at': datetime.now().isoformat()
            })
            
            self.logger.info(f"✅ Successfully completed OAuth setup for {email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {email}: {e}")
            
            # Record failure
            self.results['failed'].append({
                'email': email,
                'error': str(e),
                'failed_at': datetime.now().isoformat()
            })
            
            return False
    
    def process_bulk_emails(self, accounts: List[Dict[str, str]]) -> Dict:
        """Process multiple emails"""
        total_accounts = len(accounts)
        self.logger.info(f"Starting bulk OAuth processing for {total_accounts} accounts")
        
        for i, account in enumerate(accounts, 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Processing account {i}/{total_accounts}: {account['email']}")
            self.logger.info(f"{'='*60}")
            
            success = self.process_single_email(account)
            self.results['total_processed'] += 1
            
            # Progress update
            success_count = len(self.results['successful'])
            failed_count = len(self.results['failed'])
            
            self.logger.info(f"Progress: {i}/{total_accounts} | Success: {success_count} | Failed: {failed_count}")
            
            # Rate limiting between accounts
            if i < total_accounts:
                self.logger.info("Waiting 60 seconds before next account...")
                time.sleep(60)
        
        # Final results
        self.results['end_time'] = datetime.now().isoformat()
        self.save_results()
        
        return self.results
    
    def save_results(self):
        """Save processing results to JSON file"""
        results_file = self.output_dir / f"oauth_automation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {results_file}")
    
    def cleanup(self):
        """Cleanup browser resources"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser cleanup completed")
    
    def print_summary(self):
        """Print processing summary"""
        print(f"\n{'='*70}")
        print("🎯 GMAIL OAUTH BACKEND AUTOMATION SUMMARY")
        print(f"{'='*70}")
        print(f"Total Processed: {self.results['total_processed']}")
        print(f"✅ Successful: {len(self.results['successful'])}")
        print(f"❌ Failed: {len(self.results['failed'])}")
        print(f"📁 Output Directory: {self.output_dir}")
        
        if self.results['successful']:
            print(f"\n✅ Successful OAuth Setups:")
            for result in self.results['successful']:
                print(f"  - {result['email']} → {result['json_path']}")
        
        if self.results['failed']:
            print(f"\n❌ Failed OAuth Setups:")
            for result in self.results['failed']:
                print(f"  - {result['email']}: {result['error']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Gmail OAuth Backend Automation')
    parser.add_argument('--accounts', default='accounts.txt', help='Accounts file path')
    parser.add_argument('--output', default='oauth_json_files', help='Output directory')
    parser.add_argument('--single', help='Process single email')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Initialize automation
    automation = GmailOAuthBackendAutomation(args.output)
    
    try:
        # Setup browser
        if not automation.setup_browser(args.headless):
            print("❌ Browser setup failed!")
            return
        
        if args.single:
            # Process single email
            account = {'email': args.single, 'password': input(f"Enter password for {args.single}: ")}
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
            
            print(f"🚀 Starting Gmail OAuth automation for {len(accounts)} accounts...")
            results = automation.process_bulk_emails(accounts)
            automation.print_summary()
    
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()