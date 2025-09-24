#!/usr/bin/env python3
"""
Complete Gmail OAuth Automation - Final Version
Fully automated Gmail OAuth setup with comprehensive error handling
"""

import time
import random
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class CompleteGmailOAuthAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self.project_name = f"Gmail-OAuth-{random.randint(1000, 9999)}"
        self.results = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "steps_completed": [],
            "errors": [],
            "success": False,
            "json_file_path": None
        }
    
    def setup_driver(self):
        """Setup Chrome driver with basic configuration"""
        try:
            print("🚀 Setting up Chrome driver...")
            
            options = Options()
            
            # Basic configuration
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Random window size
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            options.add_argument(f'--window-size={width},{height}')
            
            # Create driver
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 30)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup complete!")
            self.results["steps_completed"].append("Driver setup")
            return True
            
        except Exception as e:
            error_msg = f"Driver setup failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def human_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_type(self, element, text, delay_range=(0.05, 0.15)):
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def move_mouse_randomly(self):
        """Move mouse to random position"""
        try:
            action = ActionChains(self.driver)
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            action.move_by_offset(x, y).perform()
            self.human_delay(0.5, 1)
        except:
            pass
    
    def login_to_google(self):
        """Login to Google Cloud Console"""
        try:
            print("🔐 Starting login to Google Cloud Console...")
            
            # Navigate to Google Cloud Console
            self.driver.get("https://console.cloud.google.com/")
            self.human_delay(3, 5)
            
            # Check if already logged in
            if "console.cloud.google.com" in self.driver.current_url and "Sign in" not in self.driver.page_source:
                print("✅ Already logged in!")
                self.results["steps_completed"].append("Login (already logged in)")
                return True
            
            # Find and click sign in button
            sign_in_selectors = [
                "//a[contains(text(), 'Sign in')]",
                "//button[contains(text(), 'Sign in')]",
                "//a[@data-action='sign in']",
                "//a[contains(@href, 'accounts.google.com')]"
            ]
            
            for selector in sign_in_selectors:
                try:
                    sign_in_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_mouse_randomly()
                    sign_in_btn.click()
                    print("✅ Clicked sign in button")
                    break
                except:
                    continue
            
            self.human_delay(2, 4)
            
            # Enter email
            email_selectors = [
                "input[type='email']",
                "input[id='identifierId']",
                "input[name='identifier']",
                "input[autocomplete='username']"
            ]
            
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    email_field.clear()
                    self.human_type(email_field, self.email)
                    print(f"✅ Entered email: {self.email}")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Click Next button
            next_selectors = [
                "//button[@id='identifierNext']",
                "//button[contains(text(), 'Next')]",
                "//input[@value='Next']",
                "//button[@type='submit']"
            ]
            
            for selector in next_selectors:
                try:
                    next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    next_btn.click()
                    print("✅ Clicked Next button")
                    break
                except:
                    continue
            
            self.human_delay(2, 4)
            
            # Enter password
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "input[id='password']",
                "input[autocomplete='current-password']"
            ]
            
            for selector in password_selectors:
                try:
                    password_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    password_field.clear()
                    self.human_type(password_field, self.password)
                    print("✅ Entered password")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Click Next/Sign in button
            signin_selectors = [
                "//button[@id='passwordNext']",
                "//button[contains(text(), 'Next')]",
                "//button[contains(text(), 'Sign in')]",
                "//input[@value='Sign in']"
            ]
            
            for selector in signin_selectors:
                try:
                    signin_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    signin_btn.click()
                    print("✅ Clicked Sign in button")
                    break
                except:
                    continue
            
            self.human_delay(5, 8)
            
            # Verify login success
            if "console.cloud.google.com" in self.driver.current_url:
                print("✅ Login successful!")
                self.results["steps_completed"].append("Login")
                return True
            else:
                raise Exception("Login verification failed")
                
        except Exception as e:
            error_msg = f"Login failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def create_project(self):
        """Create a new Google Cloud project"""
        try:
            print("📁 Creating new Google Cloud project...")
            
            # Navigate to project creation
            self.driver.get("https://console.cloud.google.com/projectcreate")
            self.human_delay(3, 5)
            
            # Enter project name
            project_name_selectors = [
                "input[name='projectId']",
                "input[id='projectId']",
                "input[placeholder*='project']",
                "input[aria-label*='Project name']"
            ]
            
            for selector in project_name_selectors:
                try:
                    name_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    name_field.clear()
                    self.human_type(name_field, self.project_name)
                    print(f"✅ Entered project name: {self.project_name}")
                    break
                except:
                    continue
            
            self.human_delay(2, 3)
            
            # Click Create button
            create_selectors = [
                "//button[contains(text(), 'Create')]",
                "//button[@type='submit']",
                "//input[@value='Create']",
                "//button[contains(@class, 'create')]"
            ]
            
            for selector in create_selectors:
                try:
                    create_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_mouse_randomly()
                    create_btn.click()
                    print("✅ Clicked Create button")
                    break
                except:
                    continue
            
            # Wait for project creation
            print("⏳ Waiting for project creation...")
            self.human_delay(10, 15)
            
            # Verify project creation
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    if "console.cloud.google.com" in self.driver.current_url and "projectcreate" not in self.driver.current_url:
                        print("✅ Project created successfully!")
                        self.results["steps_completed"].append("Project creation")
                        return True
                except:
                    pass
                
                self.human_delay(2, 3)
                print(f"⏳ Waiting for project creation... ({attempt + 1}/{max_attempts})")
            
            raise Exception("Project creation timeout")
            
        except Exception as e:
            error_msg = f"Project creation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def enable_gmail_api(self):
        """Enable Gmail API"""
        try:
            print("📧 Enabling Gmail API...")
            
            # Navigate to API Library
            self.driver.get("https://console.cloud.google.com/apis/library/gmail.googleapis.com")
            self.human_delay(3, 5)
            
            # Click Enable button
            enable_selectors = [
                "//button[contains(text(), 'Enable')]",
                "//button[contains(text(), 'ENABLE')]",
                "//a[contains(text(), 'Enable')]",
                "//button[@aria-label='Enable']"
            ]
            
            for selector in enable_selectors:
                try:
                    enable_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_mouse_randomly()
                    enable_btn.click()
                    print("✅ Clicked Enable Gmail API")
                    break
                except:
                    continue
            
            self.human_delay(5, 8)
            
            print("✅ Gmail API enabled!")
            self.results["steps_completed"].append("Gmail API enabled")
            return True
            
        except Exception as e:
            error_msg = f"Gmail API enablement failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def setup_oauth_consent(self):
        """Setup OAuth consent screen"""
        try:
            print("🔐 Setting up OAuth consent screen...")
            
            # Navigate to OAuth consent screen
            self.driver.get("https://console.cloud.google.com/apis/credentials/consent")
            self.human_delay(3, 5)
            
            # Select External user type
            external_selectors = [
                "//input[@value='EXTERNAL']",
                "//mat-radio-button[contains(text(), 'External')]",
                "//label[contains(text(), 'External')]"
            ]
            
            for selector in external_selectors:
                try:
                    external_radio = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    external_radio.click()
                    print("✅ Selected External user type")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Click Create button
            create_selectors = [
                "//button[contains(text(), 'Create')]",
                "//button[contains(text(), 'CREATE')]",
                "//input[@value='Create']"
            ]
            
            for selector in create_selectors:
                try:
                    create_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    create_btn.click()
                    print("✅ Clicked Create for OAuth consent")
                    break
                except:
                    continue
            
            self.human_delay(3, 5)
            
            # Fill required fields
            app_name_selectors = [
                "input[name='displayName']",
                "input[id='displayName']",
                "input[placeholder*='App name']"
            ]
            
            for selector in app_name_selectors:
                try:
                    app_name_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    app_name_field.clear()
                    self.human_type(app_name_field, f"Gmail OAuth App {random.randint(100, 999)}")
                    print("✅ Entered app name")
                    break
                except:
                    continue
            
            # Enter user support email
            email_selectors = [
                "input[name='supportEmail']",
                "input[id='supportEmail']",
                "input[type='email']"
            ]
            
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    if email_field.get_attribute('value') == '':
                        email_field.clear()
                        self.human_type(email_field, self.email)
                        print("✅ Entered support email")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Save and continue
            save_selectors = [
                "//button[contains(text(), 'Save and Continue')]",
                "//button[contains(text(), 'SAVE AND CONTINUE')]",
                "//button[contains(text(), 'Continue')]"
            ]
            
            for selector in save_selectors:
                try:
                    save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    save_btn.click()
                    print("✅ Saved OAuth consent screen")
                    break
                except:
                    continue
            
            self.human_delay(3, 5)
            
            print("✅ OAuth consent screen setup complete!")
            self.results["steps_completed"].append("OAuth consent screen")
            return True
            
        except Exception as e:
            error_msg = f"OAuth consent setup failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def create_oauth_credentials(self):
        """Create OAuth 2.0 credentials"""
        try:
            print("🔑 Creating OAuth 2.0 credentials...")
            
            # Navigate to credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            self.human_delay(3, 5)
            
            # Click Create Credentials
            create_cred_selectors = [
                "//button[contains(text(), 'Create Credentials')]",
                "//button[contains(text(), 'CREATE CREDENTIALS')]",
                "//a[contains(text(), 'Create Credentials')]"
            ]
            
            for selector in create_cred_selectors:
                try:
                    create_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    create_btn.click()
                    print("✅ Clicked Create Credentials")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Select OAuth client ID
            oauth_selectors = [
                "//a[contains(text(), 'OAuth client ID')]",
                "//button[contains(text(), 'OAuth client ID')]",
                "//li[contains(text(), 'OAuth client ID')]"
            ]
            
            for selector in oauth_selectors:
                try:
                    oauth_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    oauth_option.click()
                    print("✅ Selected OAuth client ID")
                    break
                except:
                    continue
            
            self.human_delay(2, 3)
            
            # Select Desktop application
            desktop_selectors = [
                "//option[contains(text(), 'Desktop application')]",
                "//mat-option[contains(text(), 'Desktop application')]",
                "//li[contains(text(), 'Desktop application')]"
            ]
            
            for selector in desktop_selectors:
                try:
                    desktop_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    desktop_option.click()
                    print("✅ Selected Desktop application")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Enter name for OAuth client
            name_selectors = [
                "input[name='displayName']",
                "input[id='displayName']",
                "input[placeholder*='Name']"
            ]
            
            oauth_name = f"Gmail OAuth Client {random.randint(100, 999)}"
            for selector in name_selectors:
                try:
                    name_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    name_field.clear()
                    self.human_type(name_field, oauth_name)
                    print(f"✅ Entered OAuth client name: {oauth_name}")
                    break
                except:
                    continue
            
            self.human_delay(1, 2)
            
            # Click Create
            create_final_selectors = [
                "//button[contains(text(), 'Create')]",
                "//button[contains(text(), 'CREATE')]",
                "//input[@value='Create']"
            ]
            
            for selector in create_final_selectors:
                try:
                    create_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    create_btn.click()
                    print("✅ Created OAuth credentials")
                    break
                except:
                    continue
            
            self.human_delay(3, 5)
            
            print("✅ OAuth credentials created!")
            self.results["steps_completed"].append("OAuth credentials created")
            return True
            
        except Exception as e:
            error_msg = f"OAuth credentials creation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def download_json_file(self):
        """Download the JSON credentials file"""
        try:
            print("📥 Downloading JSON credentials file...")
            
            # Look for download button
            download_selectors = [
                "//button[contains(text(), 'Download JSON')]",
                "//button[contains(text(), 'DOWNLOAD JSON')]",
                "//a[contains(text(), 'Download JSON')]",
                "//button[@aria-label='Download JSON']",
                "//button[contains(@class, 'download')]"
            ]
            
            for selector in download_selectors:
                try:
                    download_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    download_btn.click()
                    print("✅ Clicked Download JSON")
                    break
                except:
                    continue
            
            self.human_delay(3, 5)
            
            # Check downloads folder for the JSON file
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            json_files = [f for f in os.listdir(downloads_path) if f.endswith('.json') and 'client_secret' in f.lower()]
            
            if json_files:
                # Get the most recent JSON file
                json_files.sort(key=lambda x: os.path.getctime(os.path.join(downloads_path, x)), reverse=True)
                latest_json = json_files[0]
                
                # Move and rename the file
                source_path = os.path.join(downloads_path, latest_json)
                target_filename = f"gmail_oauth_credentials_{self.email.replace('@', '_').replace('.', '_')}.json"
                target_path = os.path.join(os.getcwd(), target_filename)
                
                import shutil
                shutil.move(source_path, target_path)
                
                self.results["json_file_path"] = target_path
                print(f"✅ JSON file downloaded and saved as: {target_filename}")
                self.results["steps_completed"].append("JSON file downloaded")
                return True
            else:
                raise Exception("JSON file not found in downloads")
                
        except Exception as e:
            error_msg = f"JSON download failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def run_complete_automation(self):
        """Run the complete Gmail OAuth automation"""
        try:
            print("🚀 Starting Complete Gmail OAuth Automation...")
            print(f"📧 Email: {self.email}")
            print("=" * 60)
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Login to Google
            if not self.login_to_google():
                return False
            
            # Create project
            if not self.create_project():
                return False
            
            # Enable Gmail API
            if not self.enable_gmail_api():
                return False
            
            # Setup OAuth consent screen
            if not self.setup_oauth_consent():
                return False
            
            # Create OAuth credentials
            if not self.create_oauth_credentials():
                return False
            
            # Download JSON file
            if not self.download_json_file():
                return False
            
            self.results["success"] = True
            print("🎉 Complete Gmail OAuth automation successful!")
            print(f"📁 JSON file saved: {self.results['json_file_path']}")
            
            return True
            
        except Exception as e:
            error_msg = f"Complete automation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
        
        finally:
            # Save results
            timestamp = int(time.time())
            results_filename = f"complete_oauth_results_{self.email.replace('@', '_').replace('.', '_')}_{timestamp}.json"
            
            with open(results_filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            print(f"📊 Results saved to: {results_filename}")
            
            # Keep browser open for 30 seconds for verification
            print("🔍 Keeping browser open for 30 seconds for verification...")
            time.sleep(30)
            
            if self.driver:
                self.driver.quit()

def main():
    """Main function"""
    email = "nilamb010@gmail.com"
    password = "Nilam@2024"
    
    automation = CompleteGmailOAuthAutomation(email, password)
    success = automation.run_complete_automation()
    
    if success:
        print("✅ Gmail OAuth automation completed successfully!")
    else:
        print("❌ Gmail OAuth automation failed!")

if __name__ == "__main__":
    main()