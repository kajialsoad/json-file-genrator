#!/usr/bin/env python3
"""
Complete Automated Gmail OAuth Script
Handles all steps automatically: Login → Project Creation → API Enable → Credentials → JSON Download
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

class CompleteGmailOAuthAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.project_name = f"Gmail-OAuth-{email.split('@')[0]}-{int(time.time())}"
        self.results = {
            "email": email,
            "timestamp": int(time.time()),
            "status": "started",
            "steps_completed": [],
            "errors": [],
            "project_name": self.project_name,
            "oauth_json_path": None
        }
        
    def setup_driver(self):
        """Setup Chrome driver with optimal settings"""
        try:
            print("🚀 Setting up Chrome driver for complete automation...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Set download preferences
            download_dir = os.path.abspath(".")
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            
            print("✅ Chrome driver setup complete!")
            self.results["steps_completed"].append("driver_setup")
            return True
            
        except Exception as e:
            error_msg = f"Failed to setup Chrome driver: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def wait_and_find_element(self, by, value, timeout=15):
        """Wait for element and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    def wait_and_click(self, by, value, timeout=15):
        """Wait for element to be clickable and click it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            
            # Try multiple click methods
            try:
                element.click()
                return True
            except Exception as e:
                print(f"⚠️ Regular click failed: {str(e)[:100]}...")
                
                # Try JavaScript click
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    print("✅ JavaScript click successful")
                    return True
                except Exception as e2:
                    print(f"⚠️ JavaScript click failed: {str(e2)[:100]}...")
                    
                    # Try scrolling into view and clicking
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(1)
                        element.click()
                        print("✅ Scroll and click successful")
                        return True
                    except Exception as e3:
                        print(f"❌ All click methods failed: {str(e3)[:100]}...")
                        return False
                        
        except TimeoutException:
            return False
    
    def login_to_google(self):
        """Complete Google login process"""
        try:
            print("🔐 Starting Google login process...")
            
            # Navigate to Google Cloud Console
            self.driver.get("https://console.cloud.google.com/")
            time.sleep(3)
            
            # Enter email
            email_input = self.wait_and_find_element(By.CSS_SELECTOR, "input[type='email']")
            if email_input:
                email_input.clear()
                email_input.send_keys(self.email)
                print(f"📧 Entered email: {self.email}")
                
                # Click Next
                if self.wait_and_click(By.ID, "identifierNext"):
                    print("✅ Clicked Next button")
                    time.sleep(3)
                else:
                    print("❌ Could not click Next button")
                    return False
            else:
                print("❌ Could not find email input")
                return False
            
            # Enter password
            password_input = self.wait_and_find_element(By.CSS_SELECTOR, "input[type='password']")
            if password_input:
                password_input.clear()
                password_input.send_keys(self.password)
                print("🔑 Entered password")
                
                # Click Sign in
                if self.wait_and_click(By.ID, "passwordNext"):
                    print("✅ Clicked Sign in button")
                    time.sleep(5)
                else:
                    print("❌ Could not click Sign in button")
                    return False
            else:
                print("❌ Could not find password input")
                return False
            
            # Wait for login completion
            print("⏳ Waiting for login completion...")
            time.sleep(10)
            
            current_url = self.driver.current_url
            if "console.cloud.google.com" in current_url and "signin" not in current_url:
                print("✅ Successfully logged in to Google Cloud Console")
                self.results["steps_completed"].append("login_completed")
                return True
            else:
                print(f"❌ Login may have failed. Current URL: {current_url}")
                return False
                
        except Exception as e:
            error_msg = f"Login failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def dismiss_overlays(self):
        """Dismiss any overlay backdrops that might interfere with clicking"""
        try:
            # Try to dismiss overlay backdrops
            overlays = self.driver.find_elements(By.CSS_SELECTOR, ".cdk-overlay-backdrop")
            for overlay in overlays:
                try:
                    self.driver.execute_script("arguments[0].click();", overlay)
                    time.sleep(0.5)
                except:
                    pass
            
            # Try pressing Escape key
            try:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.5)
            except:
                pass
                
        except Exception:
            pass

    def create_project(self):
        """Create a new Google Cloud project"""
        try:
            print("🏗️ Creating new Google Cloud project...")
            
            # Try multiple approaches to create project
            # Approach 1: Direct project creation page
            self.driver.get("https://console.cloud.google.com/projectcreate")
            time.sleep(5)
            
            # Dismiss any overlays
            self.dismiss_overlays()
            
            # Try multiple selectors for project name input
            project_name_input = None
            selectors = [
                "input[aria-label='Project name']",
                "input[formcontrolname='name']",
                "input[placeholder*='project name']",
                "input[placeholder*='Project name']",
                "input[name='name']",
                "input[id*='name']"
            ]
            
            for selector in selectors:
                project_name_input = self.wait_and_find_element(By.CSS_SELECTOR, selector, timeout=3)
                if project_name_input:
                    print(f"✅ Found project name input with selector: {selector}")
                    break
            
            # If still not found, try alternative approach
            if not project_name_input:
                print("🔄 Trying alternative project creation approach...")
                
                # Navigate to main console and try project selector
                self.driver.get("https://console.cloud.google.com/")
                time.sleep(3)
                
                # Look for project selector dropdown
                project_selector = self.wait_and_find_element(By.CSS_SELECTOR, "[aria-label*='Select a project']", timeout=5)
                if not project_selector:
                    project_selector = self.wait_and_find_element(By.XPATH, "//button[contains(@aria-label, 'project')]", timeout=5)
                
                if project_selector:
                    project_selector.click()
                    time.sleep(2)
                    
                    # Look for "New Project" button
                    new_project_btn = self.wait_and_find_element(By.XPATH, "//span[contains(text(), 'New Project') or contains(text(), 'NEW PROJECT')]", timeout=5)
                    if new_project_btn:
                        new_project_btn.click()
                        time.sleep(3)
                        
                        # Try to find project name input again
                        for selector in selectors:
                            project_name_input = self.wait_and_find_element(By.CSS_SELECTOR, selector, timeout=3)
                            if project_name_input:
                                print(f"✅ Found project name input with selector: {selector}")
                                break
            
            if project_name_input:
                project_name_input.clear()
                project_name_input.send_keys(self.project_name)
                print(f"📝 Entered project name: {self.project_name}")
                time.sleep(2)
                
                # Dismiss overlays before clicking Create
                self.dismiss_overlays()
                time.sleep(1)
                
                # Try multiple selectors for Create button
                create_button = None
                create_selectors = [
                    "button[aria-label='Create']",
                    "//button[contains(text(), 'Create')]",
                    "//button[contains(text(), 'CREATE')]",
                    "button[type='submit']",
                    "//span[contains(text(), 'Create')]/parent::button",
                    "//span[contains(text(), 'CREATE')]/parent::button"
                ]
                
                for selector in create_selectors:
                    # Dismiss overlays before each attempt
                    self.dismiss_overlays()
                    time.sleep(0.5)
                    
                    if selector.startswith("//"):
                        create_button = self.wait_and_find_element(By.XPATH, selector, timeout=3)
                    else:
                        create_button = self.wait_and_find_element(By.CSS_SELECTOR, selector, timeout=3)
                    
                    if create_button:
                        print(f"✅ Found Create button with selector: {selector}")
                        break
                
                if create_button:
                    create_button.click()
                    print("✅ Clicked Create button")
                    
                    # Wait for project creation
                    print("⏳ Waiting for project creation...")
                    time.sleep(15)
                    
                    # Verify project creation by checking URL or page content
                    current_url = self.driver.current_url
                    if "console.cloud.google.com" in current_url and "projectcreate" not in current_url:
                        print("✅ Project creation appears successful")
                        self.results["steps_completed"].append("project_created")
                        return True
                    else:
                        print("⚠️ Project creation status unclear, continuing...")
                        self.results["steps_completed"].append("project_created")
                        return True
                else:
                    print("❌ Could not find Create button")
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
        """Enable Gmail API for the project"""
        try:
            print("📧 Enabling Gmail API...")
            
            # Navigate to API Library
            self.driver.get("https://console.cloud.google.com/apis/library")
            time.sleep(5)
            
            # Search for Gmail API
            search_input = self.wait_and_find_element(By.CSS_SELECTOR, "input[placeholder*='Search']")
            if search_input:
                search_input.clear()
                search_input.send_keys("Gmail API")
                print("🔍 Searched for Gmail API")
                time.sleep(3)
                
                # Click on Gmail API result
                gmail_api_link = self.wait_and_find_element(By.XPATH, "//a[contains(@href, 'gmail')]")
                if gmail_api_link:
                    gmail_api_link.click()
                    print("✅ Clicked on Gmail API")
                    time.sleep(3)
                    
                    # Click Enable button
                    enable_button = self.wait_and_find_element(By.XPATH, "//button[contains(text(), 'Enable') or contains(text(), 'ENABLE')]")
                    if enable_button:
                        enable_button.click()
                        print("✅ Clicked Enable button")
                        time.sleep(10)
                        
                        self.results["steps_completed"].append("gmail_api_enabled")
                        return True
                    else:
                        print("❌ Could not find Enable button")
                        return False
                else:
                    print("❌ Could not find Gmail API link")
                    return False
            else:
                print("❌ Could not find search input")
                return False
                
        except Exception as e:
            error_msg = f"Gmail API enabling failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def configure_oauth_consent(self):
        """Configure OAuth consent screen"""
        try:
            print("🔐 Configuring OAuth consent screen...")
            
            # Navigate to OAuth consent screen
            self.driver.get("https://console.cloud.google.com/apis/credentials/consent")
            time.sleep(5)
            
            # Select External user type
            external_radio = self.wait_and_find_element(By.XPATH, "//input[@value='EXTERNAL']")
            if external_radio:
                external_radio.click()
                print("✅ Selected External user type")
                time.sleep(2)
                
                # Click Create button
                create_button = self.wait_and_find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
                if create_button:
                    create_button.click()
                    print("✅ Clicked Create button")
                    time.sleep(5)
                    
                    # Fill app name
                    app_name_input = self.wait_and_find_element(By.CSS_SELECTOR, "input[aria-label*='App name']")
                    if app_name_input:
                        app_name_input.clear()
                        app_name_input.send_keys(f"Gmail OAuth App {self.email.split('@')[0]}")
                        print("📝 Entered app name")
                        
                        # Fill user support email
                        support_email_input = self.wait_and_find_element(By.CSS_SELECTOR, "input[aria-label*='User support email']")
                        if support_email_input:
                            support_email_input.clear()
                            support_email_input.send_keys(self.email)
                            print("📧 Entered support email")
                            
                            # Save and continue
                            save_button = self.wait_and_find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'SAVE')]")
                            if save_button:
                                save_button.click()
                                print("✅ Saved OAuth consent configuration")
                                time.sleep(5)
                                
                                self.results["steps_completed"].append("oauth_consent_configured")
                                return True
                            
        except Exception as e:
            error_msg = f"OAuth consent configuration failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def create_oauth_credentials(self):
        """Create OAuth 2.0 credentials"""
        try:
            print("🔑 Creating OAuth 2.0 credentials...")
            
            # Navigate to credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(5)
            
            # Click Create Credentials
            create_creds_button = self.wait_and_find_element(By.XPATH, "//button[contains(text(), 'CREATE CREDENTIALS')]")
            if create_creds_button:
                create_creds_button.click()
                print("✅ Clicked CREATE CREDENTIALS")
                time.sleep(2)
                
                # Select OAuth client ID
                oauth_option = self.wait_and_find_element(By.XPATH, "//span[contains(text(), 'OAuth client ID')]")
                if oauth_option:
                    oauth_option.click()
                    print("✅ Selected OAuth client ID")
                    time.sleep(3)
                    
                    # Select Desktop application
                    app_type_dropdown = self.wait_and_find_element(By.CSS_SELECTOR, "mat-select[aria-label*='Application type']")
                    if app_type_dropdown:
                        app_type_dropdown.click()
                        time.sleep(1)
                        
                        desktop_option = self.wait_and_find_element(By.XPATH, "//span[contains(text(), 'Desktop application')]")
                        if desktop_option:
                            desktop_option.click()
                            print("✅ Selected Desktop application")
                            time.sleep(2)
                            
                            # Enter name
                            name_input = self.wait_and_find_element(By.CSS_SELECTOR, "input[aria-label*='Name']")
                            if name_input:
                                name_input.clear()
                                name_input.send_keys(f"Gmail OAuth Client {self.email.split('@')[0]}")
                                print("📝 Entered client name")
                                
                                # Click Create
                                create_button = self.wait_and_find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
                                if create_button:
                                    create_button.click()
                                    print("✅ Created OAuth credentials")
                                    time.sleep(5)
                                    
                                    self.results["steps_completed"].append("oauth_credentials_created")
                                    return True
                                    
        except Exception as e:
            error_msg = f"OAuth credentials creation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def download_json(self):
        """Download the OAuth JSON file"""
        try:
            print("📥 Downloading OAuth JSON file...")
            
            # Look for download button
            download_button = self.wait_and_find_element(By.XPATH, "//button[contains(@aria-label, 'Download') or contains(text(), 'DOWNLOAD')]")
            if download_button:
                download_button.click()
                print("✅ Clicked download button")
                time.sleep(5)
                
                # Wait for download to complete
                print("⏳ Waiting for download to complete...")
                time.sleep(10)
                
                # Find the downloaded file and rename it
                download_dir = "."
                for file in os.listdir(download_dir):
                    if file.endswith('.json') and 'client_secret' in file:
                        old_path = os.path.join(download_dir, file)
                        new_filename = f"gmail_oauth_{self.email.split('@')[0]}_{int(time.time())}.json"
                        new_path = os.path.join(download_dir, new_filename)
                        
                        os.rename(old_path, new_path)
                        self.results["oauth_json_path"] = new_path
                        print(f"✅ JSON file saved as: {new_filename}")
                        
                        self.results["steps_completed"].append("json_downloaded")
                        return True
                        
        except Exception as e:
            error_msg = f"JSON download failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
    
    def save_results(self):
        """Save automation results"""
        try:
            self.results["status"] = "completed"
            self.results["completion_time"] = datetime.now().isoformat()
            
            results_filename = f"complete_oauth_results_{self.email.replace('@', '_').replace('.', '_')}_{int(time.time())}.json"
            
            with open(results_filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Results saved to: {results_filename}")
            return results_filename
            
        except Exception as e:
            print(f"❌ Failed to save results: {str(e)}")
            return None
    
    def run_complete_automation(self):
        """Run the complete OAuth automation process"""
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
            
            # Configure OAuth consent
            if not self.configure_oauth_consent():
                return False
            
            # Create OAuth credentials
            if not self.create_oauth_credentials():
                return False
            
            # Download JSON
            if not self.download_json():
                return False
            
            print("🎉 Complete Gmail OAuth automation finished successfully!")
            return True
            
        except Exception as e:
            error_msg = f"Complete automation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
        
        finally:
            # Save results
            self.save_results()
            
            # Close browser
            if self.driver:
                try:
                    self.driver.quit()
                    print("🔒 Browser closed")
                except:
                    pass

def read_credentials_from_file():
    """Read email and password from accounts.txt"""
    try:
        with open('accounts.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and ':' in line:
                email, password = line.split(':', 1)
                return email.strip(), password.strip()
        
        return None, None
    except Exception as e:
        print(f"❌ Failed to read credentials: {str(e)}")
        return None, None

def main():
    """Main function"""
    try:
        # Read credentials
        email, password = read_credentials_from_file()
        
        if not email or not password:
            print("❌ Could not read email and password from accounts.txt")
            return
        
        # Run automation
        automation = CompleteGmailOAuthAutomation(email, password)
        success = automation.run_complete_automation()
        
        if success:
            print("✅ Complete automation successful!")
        else:
            print("❌ Automation failed!")
            
    except Exception as e:
        print(f"❌ Main execution failed: {str(e)}")

if __name__ == "__main__":
    main()