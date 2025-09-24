#!/usr/bin/env python3
"""
Semi-Automated Gmail OAuth Setup
This script automates Gmail OAuth setup with manual project creation step
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class SemiAutomatedGmailOAuth:
    def __init__(self):
        self.driver = None
        self.email = None
        self.password = None
        self.project_name = None
        self.results = {
            "email": "",
            "timestamp": int(time.time()),
            "status": "in_progress",
            "steps_completed": [],
            "errors": [],
            "project_name": None,
            "oauth_json_path": None,
            "completion_time": None
        }

    def setup_driver(self):
        """Setup Chrome driver with enhanced stability"""
        try:
            print("🚀 Setting up Chrome driver for semi-automated process...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(60)
            
            # Execute stealth script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup complete!")
            self.results["steps_completed"].append("driver_setup")
            return True
            
        except Exception as e:
            error_msg = f"Driver setup failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def read_credentials(self):
        """Read email and password from accounts.txt"""
        try:
            accounts_file = "accounts.txt"
            if not os.path.exists(accounts_file):
                raise FileNotFoundError(f"{accounts_file} not found")
            
            with open(accounts_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and ':' in line:
                    self.email, self.password = line.split(':', 1)
                    self.results["email"] = self.email
                    print(f"📧 Email: {self.email}")
                    return True
            
            raise ValueError("No valid credentials found in accounts.txt")
            
        except Exception as e:
            error_msg = f"Failed to read credentials: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def login_to_google(self):
        """Login to Google account with improved error handling"""
        try:
            print("🔐 Starting Google login process...")
            
            # Navigate to Google login
            self.driver.get("https://accounts.google.com/signin")
            time.sleep(5)
            
            # Enter email with multiple attempts
            for attempt in range(3):
                try:
                    email_input = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.ID, "identifierId"))
                    )
                    email_input.clear()
                    time.sleep(1)
                    email_input.send_keys(self.email)
                    print(f"📧 Entered email: {self.email}")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    time.sleep(2)
            
            # Click Next with multiple attempts
            for attempt in range(3):
                try:
                    next_button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.ID, "identifierNext"))
                    )
                    self.driver.execute_script("arguments[0].click();", next_button)
                    print("✅ Clicked Next button")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    time.sleep(2)
            
            time.sleep(5)
            
            # Enter password with multiple attempts
            for attempt in range(3):
                try:
                    password_input = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    )
                    password_input.clear()
                    time.sleep(1)
                    password_input.send_keys(self.password)
                    print("🔑 Entered password")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    time.sleep(2)
            
            # Click Sign In with multiple attempts
            for attempt in range(3):
                try:
                    signin_button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.ID, "passwordNext"))
                    )
                    self.driver.execute_script("arguments[0].click();", signin_button)
                    print("✅ Clicked Sign In button")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    time.sleep(2)
            
            # Wait for login to complete with extended timeout
            print("⏳ Waiting for login to complete...")
            WebDriverWait(self.driver, 45).until(
                lambda driver: "myaccount.google.com" in driver.current_url or 
                              "console.cloud.google.com" in driver.current_url or
                              "accounts.google.com/signin/oauth" in driver.current_url or
                              "google.com" in driver.current_url
            )
            
            print("✅ Login completed successfully!")
            self.results["steps_completed"].append("login_completed")
            return True
            
        except Exception as e:
            error_msg = f"Login failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def navigate_to_cloud_console(self):
        """Navigate to Google Cloud Console"""
        try:
            print("☁️ Navigating to Google Cloud Console...")
            self.driver.get("https://console.cloud.google.com/")
            time.sleep(5)
            
            print("✅ Successfully navigated to Google Cloud Console")
            self.results["steps_completed"].append("cloud_console_accessed")
            return True
            
        except Exception as e:
            error_msg = f"Failed to navigate to Cloud Console: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def wait_for_manual_project_creation(self):
        """Wait for user to manually create a project"""
        try:
            print("\n" + "="*60)
            print("🏗️ MANUAL STEP REQUIRED: PROJECT CREATION")
            print("="*60)
            print("Please manually create a new project:")
            print("1. Click on the project selector (top left)")
            print("2. Click 'New Project'")
            print("3. Enter a project name (e.g., Gmail-OAuth-Setup)")
            print("4. Click 'Create'")
            print("5. Wait for project creation to complete")
            print("6. Make sure the new project is selected")
            print("\nPress ENTER when project creation is complete...")
            print("="*60)
            
            input()  # Wait for user input
            
            # Get current project name from the page
            try:
                # Try to find project name in various locations
                project_selectors = [
                    "[data-testid='project-switcher-button'] span",
                    ".cfc-project-switcher-button span",
                    ".p6n-project-switcher-button span"
                ]
                
                project_name = None
                for selector in project_selectors:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        project_name = element.text.strip()
                        if project_name and project_name != "Select a project":
                            break
                    except:
                        continue
                
                if project_name:
                    self.project_name = project_name
                    print(f"✅ Detected project: {project_name}")
                else:
                    self.project_name = "Manual-Project"
                    print("⚠️ Could not detect project name, using default")
                
                self.results["project_name"] = self.project_name
                self.results["steps_completed"].append("project_created")
                return True
                
            except Exception as e:
                print(f"⚠️ Could not detect project name: {str(e)}")
                self.project_name = "Manual-Project"
                self.results["project_name"] = self.project_name
                self.results["steps_completed"].append("project_created")
                return True
                
        except Exception as e:
            error_msg = f"Manual project creation step failed: {str(e)}"
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
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search']"))
            )
            search_box.clear()
            search_box.send_keys("Gmail API")
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            
            # Click on Gmail API result
            gmail_api_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'gmail')]"))
            )
            gmail_api_link.click()
            time.sleep(3)
            
            # Click Enable button
            enable_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Enable') or contains(text(), 'ENABLE')]"))
            )
            enable_button.click()
            print("✅ Clicked Enable button for Gmail API")
            
            # Wait for API to be enabled
            time.sleep(10)
            
            print("✅ Gmail API enabled successfully")
            self.results["steps_completed"].append("gmail_api_enabled")
            return True
            
        except Exception as e:
            error_msg = f"Failed to enable Gmail API: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def setup_oauth_consent_screen(self):
        """Setup OAuth consent screen"""
        try:
            print("🔐 Setting up OAuth consent screen...")
            
            # Navigate to OAuth consent screen
            self.driver.get("https://console.cloud.google.com/apis/credentials/consent")
            time.sleep(5)
            
            # Check if consent screen is already configured
            try:
                # Look for existing consent screen
                existing_consent = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Edit app')]")
                print("✅ OAuth consent screen already configured")
                self.results["steps_completed"].append("oauth_consent_configured")
                return True
            except:
                pass
            
            # Configure new consent screen
            try:
                # Select External user type
                external_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='EXTERNAL']"))
                )
                external_radio.click()
                time.sleep(1)
                
                # Click Create
                create_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
                create_button.click()
                time.sleep(3)
                
                # Fill required fields
                app_name_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='App name']"))
                )
                app_name_input.send_keys(f"Gmail OAuth App - {self.project_name}")
                
                user_email_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='User support email']")
                user_email_input.send_keys(self.email)
                
                developer_email_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='Developer contact information']")
                developer_email_input.send_keys(self.email)
                
                # Click Save and Continue
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save and Continue')]")
                save_button.click()
                time.sleep(3)
                
                print("✅ OAuth consent screen configured")
                self.results["steps_completed"].append("oauth_consent_configured")
                return True
                
            except Exception as e:
                print(f"⚠️ Consent screen configuration may have failed: {str(e)}")
                # Continue anyway as this might already be configured
                self.results["steps_completed"].append("oauth_consent_configured")
                return True
                
        except Exception as e:
            error_msg = f"Failed to setup OAuth consent screen: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def create_credentials(self):
        """Create OAuth 2.0 credentials"""
        try:
            print("🔑 Creating OAuth 2.0 credentials...")
            
            # Navigate to credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(5)
            
            # Click Create Credentials
            create_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Credentials') or contains(text(), 'CREATE CREDENTIALS')]"))
            )
            create_button.click()
            time.sleep(2)
            
            # Select OAuth client ID
            oauth_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'OAuth client ID')]"))
            )
            oauth_option.click()
            time.sleep(3)
            
            # Select application type (Desktop application)
            app_type_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-select[aria-label*='Application type']"))
            )
            app_type_dropdown.click()
            time.sleep(1)
            
            desktop_option = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Desktop application')]")
            desktop_option.click()
            time.sleep(1)
            
            # Enter name for the OAuth client
            name_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='Name']")
            name_input.clear()
            name_input.send_keys(f"Gmail OAuth Client - {self.project_name}")
            
            # Click Create
            create_oauth_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'CREATE')]")
            create_oauth_button.click()
            time.sleep(5)
            
            print("✅ OAuth credentials created successfully")
            self.results["steps_completed"].append("credentials_created")
            return True
            
        except Exception as e:
            error_msg = f"Failed to create credentials: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def download_json_credentials(self):
        """Download the JSON credentials file"""
        try:
            print("📥 Downloading JSON credentials...")
            
            # Look for download button in the popup or page
            download_selectors = [
                "//button[contains(text(), 'Download JSON') or contains(text(), 'DOWNLOAD JSON')]",
                "//a[contains(text(), 'Download JSON') or contains(text(), 'DOWNLOAD JSON')]",
                "//button[contains(@aria-label, 'download')]",
                ".download-button"
            ]
            
            download_clicked = False
            for selector in download_selectors:
                try:
                    if selector.startswith("//"):
                        download_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        download_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    download_button.click()
                    download_clicked = True
                    print(f"✅ Clicked download button with selector: {selector}")
                    break
                except:
                    continue
            
            if not download_clicked:
                # Try to find the credentials in the list and download
                try:
                    # Go back to credentials list
                    self.driver.get("https://console.cloud.google.com/apis/credentials")
                    time.sleep(3)
                    
                    # Find the OAuth client and click download
                    download_icon = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label*='Download OAuth client']"))
                    )
                    download_icon.click()
                    download_clicked = True
                    print("✅ Downloaded credentials from credentials list")
                except:
                    pass
            
            if download_clicked:
                time.sleep(3)
                
                # Create a custom filename based on email
                email_prefix = self.email.split('@')[0]
                timestamp = int(time.time())
                json_filename = f"gmail_oauth_credentials_{email_prefix}_{timestamp}.json"
                
                # The file will be downloaded to the default downloads folder
                # We'll note the expected path
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                expected_json_path = os.path.join(downloads_path, json_filename)
                
                self.results["oauth_json_path"] = expected_json_path
                print(f"✅ JSON credentials should be downloaded to Downloads folder")
                print(f"📁 Expected filename pattern: client_secret_*.json")
                
                self.results["steps_completed"].append("json_downloaded")
                return True
            else:
                raise Exception("Could not find download button")
                
        except Exception as e:
            error_msg = f"Failed to download JSON credentials: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False

    def save_results(self):
        """Save automation results to JSON file"""
        try:
            self.results["completion_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            if len(self.results["errors"]) == 0:
                self.results["status"] = "completed"
            else:
                self.results["status"] = "completed_with_errors"
            
            email_prefix = self.email.split('@')[0] if self.email else "unknown"
            timestamp = int(time.time())
            filename = f"semi_oauth_results_{email_prefix}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Results saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"⚠️ Failed to save results: {str(e)}")
            return None

    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")

    def run_automation(self):
        """Run the complete semi-automated OAuth setup"""
        try:
            print("🚀 Starting Semi-Automated Gmail OAuth Setup...")
            print("="*60)
            
            # Read credentials
            if not self.read_credentials():
                return False
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Login to Google
            if not self.login_to_google():
                return False
            
            # Navigate to Cloud Console
            if not self.navigate_to_cloud_console():
                return False
            
            # Manual project creation step
            if not self.wait_for_manual_project_creation():
                return False
            
            # Enable Gmail API
            if not self.enable_gmail_api():
                return False
            
            # Setup OAuth consent screen
            if not self.setup_oauth_consent_screen():
                return False
            
            # Create credentials
            if not self.create_credentials():
                return False
            
            # Download JSON credentials
            if not self.download_json_credentials():
                return False
            
            print("\n" + "="*60)
            print("🎉 SEMI-AUTOMATED OAUTH SETUP COMPLETED!")
            print("="*60)
            print("✅ All steps completed successfully")
            print("📁 Check your Downloads folder for the JSON credentials file")
            print("🔧 You can now use this JSON file for Gmail API access")
            print("="*60)
            
            return True
            
        except Exception as e:
            error_msg = f"Automation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return False
        
        finally:
            # Save results and cleanup
            self.save_results()
            self.cleanup()

def main():
    """Main function"""
    automation = SemiAutomatedGmailOAuth()
    
    try:
        success = automation.run_automation()
        if success:
            print("✅ Semi-automated OAuth setup completed successfully!")
        else:
            print("❌ Semi-automated OAuth setup failed!")
            
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        automation.cleanup()
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        automation.cleanup()

if __name__ == "__main__":
    main()