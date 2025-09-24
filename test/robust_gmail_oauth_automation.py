#!/usr/bin/env python3
"""
Robust Gmail OAuth Automation Script
Handles browser window closures and provides better error recovery
"""

import os
import sys
import time
import json
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    NoSuchWindowException,
    InvalidSessionIdException
)

class RobustGmailOAuthAutomation:
    def __init__(self, email, password=None):
        self.email = email
        self.password = password
        self.driver = None
        self.results = {
            "email": email,
            "timestamp": int(time.time()),
            "status": "started",
            "steps_completed": [],
            "errors": [],
            "oauth_json_path": None
        }
        
    def setup_driver(self):
        """Setup Chrome driver with robust options"""
        try:
            print("🚀 Setting up robust Chrome driver...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Create driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            
            # Execute stealth script
            stealth_script = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            """
            self.driver.execute_script(stealth_script)
            
            print("✅ Chrome driver setup complete!")
            self.results["steps_completed"].append("driver_setup")
            return True
            
        except Exception as e:
            error_msg = f"Failed to setup Chrome driver: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def check_driver_health(self):
        """Check if driver is still healthy"""
        try:
            # Try to get current URL
            current_url = self.driver.current_url
            return True
        except (NoSuchWindowException, InvalidSessionIdException, WebDriverException):
            return False
    
    def recover_driver(self):
        """Attempt to recover from driver issues"""
        print("🔄 Attempting to recover driver...")
        try:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            # Wait a bit before recreating
            time.sleep(3)
            
            # Recreate driver
            return self.setup_driver()
        except Exception as e:
            print(f"❌ Driver recovery failed: {str(e)}")
            return False
    
    def safe_navigate(self, url, max_retries=3):
        """Safely navigate to URL with retries"""
        for attempt in range(max_retries):
            try:
                if not self.check_driver_health():
                    if not self.recover_driver():
                        return False
                
                print(f"🌐 Navigating to: {url}")
                self.driver.get(url)
                time.sleep(3)
                return True
                
            except Exception as e:
                print(f"❌ Navigation attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return False
        return False
    
    def safe_find_element(self, by, value, timeout=10, max_retries=2):
        """Safely find element with retries"""
        for attempt in range(max_retries):
            try:
                if not self.check_driver_health():
                    if not self.recover_driver():
                        return None
                
                wait = WebDriverWait(self.driver, timeout)
                element = wait.until(EC.presence_of_element_located((by, value)))
                return element
                
            except TimeoutException:
                print(f"⏰ Element not found (attempt {attempt + 1}): {value}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
            except Exception as e:
                print(f"❌ Error finding element (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
        return None
    
    def safe_click(self, element, max_retries=2):
        """Safely click element with retries"""
        for attempt in range(max_retries):
            try:
                if not self.check_driver_health():
                    if not self.recover_driver():
                        return False
                
                # Scroll to element
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                
                # Try to click
                element.click()
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"❌ Click attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return False
        return False
    
    def login_to_google(self):
        """Login to Google with robust error handling"""
        try:
            print("🔐 Starting robust login to Google Cloud Console...")
            
            # Navigate to Google Cloud Console
            if not self.safe_navigate("https://console.cloud.google.com/"):
                return False
            
            # Check if already logged in
            time.sleep(5)
            if "console.cloud.google.com" in self.driver.current_url and "signin" not in self.driver.current_url:
                print("✅ Already logged in!")
                self.results["steps_completed"].append("login_check")
                return True
            
            # Look for email input
            email_input = self.safe_find_element(By.ID, "identifierId", timeout=15)
            if not email_input:
                # Try alternative selectors
                email_input = self.safe_find_element(By.CSS_SELECTOR, "input[type='email']", timeout=10)
            
            if email_input:
                print(f"📧 Entering email: {self.email}")
                email_input.clear()
                email_input.send_keys(self.email)
                time.sleep(2)
                
                # Click Next
                next_button = self.safe_find_element(By.ID, "identifierNext")
                if not next_button:
                    next_button = self.safe_find_element(By.CSS_SELECTOR, "[data-primary='true']")
                
                if next_button and self.safe_click(next_button):
                    print("✅ Email entered successfully")
                    self.results["steps_completed"].append("email_entered")
                    time.sleep(5)
                    
                    # Handle password if provided
                    if self.password:
                        return self.enter_password()
                    else:
                        print("⏳ Please complete login manually...")
                        return self.wait_for_manual_login()
                else:
                    print("❌ Could not click Next button")
                    return False
            else:
                print("❌ Could not find email input field")
                return False
                
        except Exception as e:
            error_msg = f"Login failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def enter_password(self):
        """Enter password with robust handling"""
        try:
            print("🔑 Entering password...")
            
            # Wait for password field
            password_input = self.safe_find_element(By.NAME, "password", timeout=15)
            if not password_input:
                password_input = self.safe_find_element(By.CSS_SELECTOR, "input[type='password']", timeout=10)
            
            if password_input:
                password_input.clear()
                password_input.send_keys(self.password)
                time.sleep(2)
                
                # Click Next
                next_button = self.safe_find_element(By.ID, "passwordNext")
                if not next_button:
                    next_button = self.safe_find_element(By.CSS_SELECTOR, "[data-primary='true']")
                
                if next_button and self.safe_click(next_button):
                    print("✅ Password entered successfully")
                    self.results["steps_completed"].append("password_entered")
                    time.sleep(10)
                    return True
                else:
                    print("❌ Could not click password Next button")
                    return False
            else:
                print("❌ Could not find password input field")
                return False
                
        except Exception as e:
            error_msg = f"Password entry failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def wait_for_manual_login(self, timeout=300):
        """Wait for manual login completion"""
        print("⏳ Waiting for manual login completion...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if not self.check_driver_health():
                    print("❌ Browser window was closed")
                    return False
                
                current_url = self.driver.current_url
                if "console.cloud.google.com" in current_url and "signin" not in current_url:
                    print("✅ Login completed successfully!")
                    self.results["steps_completed"].append("manual_login_completed")
                    return True
                
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error during manual login wait: {str(e)}")
                return False
        
        print("⏰ Manual login timeout")
        return False
    
    def create_project(self):
        """Create new Google Cloud project"""
        try:
            print("📁 Creating new project...")
            
            # Navigate to project creation
            if not self.safe_navigate("https://console.cloud.google.com/projectcreate"):
                return False
            
            time.sleep(5)
            
            # Generate project name
            project_name = f"gmail-oauth-{int(time.time())}"
            
            # Find project name input
            name_input = self.safe_find_element(By.ID, "p6n-kpn-project-name-input")
            if not name_input:
                name_input = self.safe_find_element(By.CSS_SELECTOR, "input[aria-label*='Project name']")
            
            if name_input:
                name_input.clear()
                name_input.send_keys(project_name)
                time.sleep(2)
                
                # Click Create button
                create_button = self.safe_find_element(By.CSS_SELECTOR, "button[aria-label='Create']")
                if not create_button:
                    create_button = self.safe_find_element(By.XPATH, "//button[contains(text(), 'Create')]")
                
                if create_button and self.safe_click(create_button):
                    print(f"✅ Project creation initiated: {project_name}")
                    self.results["steps_completed"].append("project_created")
                    self.results["project_name"] = project_name
                    
                    # Wait for project creation to complete
                    time.sleep(15)
                    return True
                else:
                    print("❌ Could not click Create button")
                    return False
            else:
                print("❌ Could not find project name input")
                return False
                
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
            if not self.safe_navigate("https://console.cloud.google.com/apis/library/gmail.googleapis.com"):
                return False
            
            time.sleep(5)
            
            # Click Enable button
            enable_button = self.safe_find_element(By.XPATH, "//button[contains(text(), 'Enable') or contains(text(), 'ENABLE')]")
            if enable_button and self.safe_click(enable_button):
                print("✅ Gmail API enabled successfully")
                self.results["steps_completed"].append("gmail_api_enabled")
                time.sleep(10)
                return True
            else:
                print("❌ Could not find or click Enable button")
                return False
                
        except Exception as e:
            error_msg = f"Gmail API enablement failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def configure_oauth_consent(self):
        """Configure OAuth consent screen"""
        try:
            print("🔐 Configuring OAuth consent screen...")
            
            # Navigate to OAuth consent screen
            if not self.safe_navigate("https://console.cloud.google.com/apis/credentials/consent"):
                return False
            
            time.sleep(5)
            
            # Select External user type
            external_radio = self.safe_find_element(By.CSS_SELECTOR, "input[value='EXTERNAL']")
            if external_radio and self.safe_click(external_radio):
                time.sleep(2)
                
                # Click Create button
                create_button = self.safe_find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
                if create_button and self.safe_click(create_button):
                    print("✅ OAuth consent screen configured")
                    self.results["steps_completed"].append("oauth_consent_configured")
                    time.sleep(5)
                    return True
            
            print("❌ Could not configure OAuth consent screen")
            return False
            
        except Exception as e:
            error_msg = f"OAuth consent configuration failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def create_oauth_credentials(self):
        """Create OAuth credentials"""
        try:
            print("🔑 Creating OAuth credentials...")
            
            # Navigate to credentials page
            if not self.safe_navigate("https://console.cloud.google.com/apis/credentials"):
                return False
            
            time.sleep(5)
            
            # Click Create Credentials
            create_button = self.safe_find_element(By.XPATH, "//button[contains(text(), 'Create Credentials')]")
            if create_button and self.safe_click(create_button):
                time.sleep(2)
                
                # Select OAuth client ID
                oauth_option = self.safe_find_element(By.XPATH, "//span[contains(text(), 'OAuth client ID')]")
                if oauth_option and self.safe_click(oauth_option):
                    time.sleep(3)
                    
                    # Select Desktop application
                    desktop_option = self.safe_find_element(By.CSS_SELECTOR, "option[value='DESKTOP']")
                    if desktop_option and self.safe_click(desktop_option):
                        time.sleep(2)
                        
                        # Enter name
                        name_input = self.safe_find_element(By.CSS_SELECTOR, "input[aria-label*='Name']")
                        if name_input:
                            name_input.clear()
                            name_input.send_keys("Gmail OAuth Client")
                            time.sleep(2)
                            
                            # Click Create
                            final_create_button = self.safe_find_element(By.XPATH, "//button[contains(text(), 'Create')]")
                            if final_create_button and self.safe_click(final_create_button):
                                print("✅ OAuth credentials created")
                                self.results["steps_completed"].append("oauth_credentials_created")
                                time.sleep(5)
                                return True
            
            print("❌ Could not create OAuth credentials")
            return False
            
        except Exception as e:
            error_msg = f"OAuth credentials creation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def download_json(self):
        """Download OAuth JSON file"""
        try:
            print("📥 Downloading OAuth JSON file...")
            
            # Look for download button
            download_button = self.safe_find_element(By.XPATH, "//button[contains(@aria-label, 'Download')]")
            if not download_button:
                download_button = self.safe_find_element(By.CSS_SELECTOR, "[data-value='download']")
            
            if download_button and self.safe_click(download_button):
                print("✅ JSON download initiated")
                self.results["steps_completed"].append("json_downloaded")
                time.sleep(5)
                
                # Look for downloaded file
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                json_files = [f for f in os.listdir(downloads_path) if f.endswith('.json') and 'client_secret' in f]
                
                if json_files:
                    latest_json = max([os.path.join(downloads_path, f) for f in json_files], key=os.path.getctime)
                    self.results["oauth_json_path"] = latest_json
                    print(f"✅ JSON file found: {latest_json}")
                    return True
                else:
                    print("⚠️ JSON file not found in Downloads folder")
                    return False
            else:
                print("❌ Could not find download button")
                return False
                
        except Exception as e:
            error_msg = f"JSON download failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def save_results(self):
        """Save automation results"""
        try:
            self.results["status"] = "completed" if len(self.results["errors"]) == 0 else "completed_with_errors"
            self.results["completion_time"] = int(time.time())
            
            filename = f"robust_oauth_results_{self.email.replace('@', '_').replace('.', '_')}_{self.results['timestamp']}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            print(f"📊 Results saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Failed to save results: {str(e)}")
            return None
    
    def run_complete_automation(self):
        """Run the complete OAuth automation process"""
        try:
            print("🚀 Starting Robust Gmail OAuth Automation...")
            print(f"📧 Email: {self.email}")
            print("=" * 60)
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Login
            if not self.login_to_google():
                return False
            
            # Create project
            if not self.create_project():
                return False
            
            # Enable Gmail API
            if not self.enable_gmail_api():
                return False
            
            # Configure OAuth consent
            if not self.configure_oauth_consent():
                return False
            
            # Create OAuth credentials
            if not self.create_oauth_credentials():
                return False
            
            # Download JSON
            if not self.download_json():
                return False
            
            print("🎉 Complete automation successful!")
            return True
            
        except Exception as e:
            error_msg = f"Complete automation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
        
        finally:
            # Save results
            self.save_results()
            
            # Keep browser open for verification
            if self.driver:
                print("🔍 Keeping browser open for 60 seconds for verification...")
                time.sleep(60)
                try:
                    self.driver.quit()
                except:
                    pass

def main():
    """Main function"""
    email = "nilamb010@gmail.com"
    
    # Create automation instance
    automation = RobustGmailOAuthAutomation(email)
    
    # Run complete automation
    success = automation.run_complete_automation()
    
    if success:
        print("✅ Automation completed successfully!")
    else:
        print("❌ Automation completed with errors. Check the results file for details.")

if __name__ == "__main__":
    main()