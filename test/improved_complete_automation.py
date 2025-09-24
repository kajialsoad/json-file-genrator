#!/usr/bin/env python3
"""
Improved Complete Gmail OAuth Automation Script
Enhanced with better error handling and robust selectors
"""

import time
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

class ImprovedGmailOAuthAutomation:
    def __init__(self, email, password, project_name=None):
        self.email = email
        self.password = password
        self.project_name = project_name or f"gmail-oauth-{email.split('@')[0]}-{int(time.time())}"
        self.driver = None
        self.wait = None
        self.results = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "success": False,
            "json_file_path": None,
            "errors": []
        }
    
    def setup_driver(self):
        """Setup Chrome driver with enhanced options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            
            # Set download directory
            download_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(download_dir, exist_ok=True)
            
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 30)
            
            self.log_step("Enhanced driver setup completed successfully")
            return True
            
        except Exception as e:
            self.log_error(f"Driver setup failed: {str(e)}")
            return False
    
    def log_step(self, message):
        """Log a step with timestamp"""
        step = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "url": self.driver.current_url if self.driver else "N/A"
        }
        self.results["steps"].append(step)
        print(f"[{step['timestamp']}] {message}")
    
    def log_error(self, error):
        """Log an error"""
        self.results["errors"].append({
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "url": self.driver.current_url if self.driver else "N/A"
        })
        print(f"ERROR: {error}")
    
    def safe_click(self, element):
        """Safely click an element using multiple methods"""
        try:
            # Method 1: Regular click
            element.click()
            return True
        except:
            try:
                # Method 2: JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                try:
                    # Method 3: Action chains
                    ActionChains(self.driver).move_to_element(element).click().perform()
                    return True
                except:
                    return False
    
    def safe_send_keys(self, element, text):
        """Safely send keys to an element"""
        try:
            element.clear()
            time.sleep(0.5)
            element.send_keys(text)
            return True
        except:
            try:
                # Alternative method using JavaScript
                self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
                return True
            except:
                return False
    
    def login_to_google_cloud(self):
        """Enhanced login to Google Cloud Console"""
        try:
            self.log_step("Starting enhanced login to Google Cloud Console")
            self.driver.get("https://console.cloud.google.com/")
            time.sleep(5)
            
            # Check if already logged in
            if "console.cloud.google.com" in self.driver.current_url and ("getting-started" in self.driver.current_url or "home" in self.driver.current_url):
                self.log_step("Already logged in to Google Cloud Console")
                return True
            
            # Multiple selectors for email field
            email_selectors = [
                "input[type='email']",
                "#identifierId",
                "input[name='identifier']",
                "input[aria-label*='email']",
                "input[placeholder*='email']"
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not email_field:
                self.log_error("Could not find email field")
                return False
            
            # Enter email
            if not self.safe_send_keys(email_field, self.email):
                self.log_error("Failed to enter email")
                return False
            
            self.log_step(f"Entered email: {self.email}")
            time.sleep(2)
            
            # Click Next button
            next_selectors = [
                "#identifierNext",
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Next')",
                "[data-testid='next-button']"
            ]
            
            next_button = None
            for selector in next_selectors:
                try:
                    next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not next_button:
                # Try XPath
                try:
                    next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]/..")))
                except:
                    self.log_error("Could not find Next button")
                    return False
            
            if not self.safe_click(next_button):
                self.log_error("Failed to click Next button")
                return False
            
            self.log_step("Clicked Next button")
            time.sleep(5)
            
            # Multiple selectors for password field
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password",
                "input[aria-label*='password']",
                "input[placeholder*='password']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not password_field:
                self.log_error("Could not find password field")
                return False
            
            # Enter password
            if not self.safe_send_keys(password_field, self.password):
                self.log_error("Failed to enter password")
                return False
            
            self.log_step("Entered password")
            time.sleep(2)
            
            # Click Sign in button
            signin_selectors = [
                "#passwordNext",
                "button[type='submit']",
                "input[type='submit']",
                "[data-testid='signin-button']"
            ]
            
            signin_button = None
            for selector in signin_selectors:
                try:
                    signin_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not signin_button:
                # Try XPath
                try:
                    signin_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next') or contains(text(), 'Sign in')]/..")))
                except:
                    self.log_error("Could not find Sign in button")
                    return False
            
            if not self.safe_click(signin_button):
                self.log_error("Failed to click Sign in button")
                return False
            
            self.log_step("Clicked Sign in button")
            time.sleep(10)
            
            # Wait for login to complete - check multiple possible URLs
            success_urls = [
                "console.cloud.google.com",
                "cloud.google.com/console"
            ]
            
            max_wait = 30
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                current_url = self.driver.current_url
                if any(url in current_url for url in success_urls):
                    self.log_step("Successfully logged in to Google Cloud Console")
                    return True
                time.sleep(2)
            
            self.log_error("Login timeout - did not reach Google Cloud Console")
            return False
            
        except Exception as e:
            self.log_error(f"Enhanced login failed: {str(e)}")
            return False
    
    def create_project(self):
        """Enhanced project creation"""
        try:
            self.log_step("Starting enhanced project creation")
            
            # Navigate directly to project creation
            self.driver.get("https://console.cloud.google.com/projectcreate")
            time.sleep(5)
            
            # Wait for page to load
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input, form")))
            except:
                self.log_error("Project creation page did not load")
                return False
            
            # Find project name field
            name_selectors = [
                "#projectId",
                "input[name='projectId']",
                "input[placeholder*='project']",
                "input[aria-label*='project']"
            ]
            
            project_field = None
            for selector in name_selectors:
                try:
                    project_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not project_field:
                self.log_error("Could not find project name field")
                return False
            
            # Enter project name
            if not self.safe_send_keys(project_field, self.project_name):
                self.log_error("Failed to enter project name")
                return False
            
            self.log_step(f"Entered project name: {self.project_name}")
            time.sleep(2)
            
            # Find and click Create button
            create_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "[data-testid='create-button']"
            ]
            
            create_button = None
            for selector in create_selectors:
                try:
                    create_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not create_button:
                # Try XPath
                try:
                    create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create') or contains(text(), 'CREATE')]/..")))
                except:
                    self.log_error("Could not find Create button")
                    return False
            
            if not self.safe_click(create_button):
                self.log_error("Failed to click Create button")
                return False
            
            self.log_step("Clicked Create button")
            time.sleep(15)  # Wait longer for project creation
            
            self.log_step("Project creation completed")
            return True
            
        except Exception as e:
            self.log_error(f"Enhanced project creation failed: {str(e)}")
            return False
    
    def enable_gmail_api(self):
        """Enhanced Gmail API enablement"""
        try:
            self.log_step("Starting enhanced Gmail API enablement")
            
            # Navigate to API Library
            self.driver.get("https://console.cloud.google.com/apis/library")
            time.sleep(5)
            
            # Search for Gmail API
            search_selectors = [
                "input[placeholder*='Search']",
                "input[aria-label*='Search']",
                "input[type='search']",
                "#search-input"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not search_box:
                self.log_error("Could not find search box")
                return False
            
            if not self.safe_send_keys(search_box, "Gmail API"):
                self.log_error("Failed to enter search term")
                return False
            
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)
            self.log_step("Searched for Gmail API")
            
            # Click on Gmail API
            try:
                gmail_api_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'gmail') or .//span[contains(text(), 'Gmail API')]]")))
                if not self.safe_click(gmail_api_link):
                    self.log_error("Failed to click Gmail API link")
                    return False
            except:
                self.log_error("Could not find Gmail API link")
                return False
            
            time.sleep(5)
            self.log_step("Clicked on Gmail API")
            
            # Enable the API
            try:
                enable_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enable') or contains(text(), 'ENABLE')]/..")))
                if not self.safe_click(enable_button):
                    self.log_step("Gmail API might already be enabled")
                else:
                    self.log_step("Clicked Enable button for Gmail API")
                    time.sleep(10)
            except:
                self.log_step("Gmail API might already be enabled")
            
            return True
            
        except Exception as e:
            self.log_error(f"Enhanced Gmail API enablement failed: {str(e)}")
            return False
    
    def create_oauth_credentials(self):
        """Enhanced OAuth credentials creation"""
        try:
            self.log_step("Starting enhanced OAuth credentials creation")
            
            # Navigate to Credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(5)
            
            # Click Create Credentials
            try:
                create_credentials_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create Credentials') or contains(text(), 'CREATE CREDENTIALS')]/..")))
                if not self.safe_click(create_credentials_button):
                    self.log_error("Failed to click Create Credentials")
                    return False
            except:
                self.log_error("Could not find Create Credentials button")
                return False
            
            time.sleep(3)
            self.log_step("Clicked Create Credentials")
            
            # Select OAuth client ID
            try:
                oauth_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'OAuth client ID')]/..")))
                if not self.safe_click(oauth_option):
                    self.log_error("Failed to click OAuth client ID")
                    return False
            except:
                self.log_error("Could not find OAuth client ID option")
                return False
            
            time.sleep(5)
            self.log_step("Selected OAuth client ID")
            
            # Select application type (Desktop application)
            try:
                # Try dropdown first
                app_type_dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select, .mat-select-trigger, [role='combobox']")))
                if app_type_dropdown.tag_name == "select":
                    select = Select(app_type_dropdown)
                    select.select_by_visible_text("Desktop application")
                else:
                    if not self.safe_click(app_type_dropdown):
                        self.log_error("Failed to click application type dropdown")
                        return False
                    time.sleep(2)
                    desktop_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Desktop application')]/..")))
                    if not self.safe_click(desktop_option):
                        self.log_error("Failed to select Desktop application")
                        return False
            except:
                self.log_error("Could not find application type selector")
                return False
            
            self.log_step("Selected Desktop application type")
            time.sleep(2)
            
            # Enter name for OAuth client
            name_selectors = [
                "input[aria-label*='Name']",
                "input[placeholder*='Name']",
                "input[name*='name']"
            ]
            
            name_field = None
            for selector in name_selectors:
                try:
                    name_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not name_field:
                self.log_error("Could not find name field")
                return False
            
            oauth_name = f"Gmail OAuth Client {self.email.split('@')[0]}"
            if not self.safe_send_keys(name_field, oauth_name):
                self.log_error("Failed to enter OAuth client name")
                return False
            
            self.log_step(f"Entered OAuth client name: {oauth_name}")
            time.sleep(2)
            
            # Click Create
            try:
                create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create') or contains(text(), 'CREATE')]/..")))
                if not self.safe_click(create_button):
                    self.log_error("Failed to click Create for OAuth credentials")
                    return False
            except:
                self.log_error("Could not find Create button for OAuth credentials")
                return False
            
            time.sleep(10)
            self.log_step("Clicked Create for OAuth credentials")
            
            return True
            
        except Exception as e:
            self.log_error(f"Enhanced OAuth credentials creation failed: {str(e)}")
            return False
    
    def download_json_file(self):
        """Enhanced JSON file download"""
        try:
            self.log_step("Starting enhanced JSON file download")
            
            # Look for download button in success dialog or credentials list
            download_selectors = [
                "//span[contains(text(), 'Download') or contains(text(), 'DOWNLOAD')]/..",
                "[aria-label*='download']",
                ".download-icon",
                "[title*='Download']",
                "//button[contains(@aria-label, 'download')]"
            ]
            
            download_button = None
            for selector in download_selectors:
                try:
                    if selector.startswith("//"):
                        download_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    else:
                        download_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not download_button:
                self.log_error("Could not find download button")
                return False
            
            if not self.safe_click(download_button):
                self.log_error("Failed to click download button")
                return False
            
            self.log_step("Clicked Download button")
            time.sleep(10)  # Wait longer for download
            
            # Find and rename the downloaded file
            download_dir = os.path.join(os.getcwd(), "output")
            downloaded_files = [f for f in os.listdir(download_dir) if f.endswith('.json')]
            
            if downloaded_files:
                # Get the most recent JSON file
                latest_file = max([os.path.join(download_dir, f) for f in downloaded_files], key=os.path.getctime)
                
                # Create new filename: gmail_[email].json
                email_prefix = self.email.split('@')[0]
                new_filename = f"gmail_{email_prefix}.json"
                new_filepath = os.path.join(download_dir, new_filename)
                
                # Rename the file
                os.rename(latest_file, new_filepath)
                self.results["json_file_path"] = new_filepath
                self.log_step(f"JSON file downloaded and renamed to: {new_filename}")
                
                return True
            else:
                self.log_error("No JSON file found in download directory")
                return False
                
        except Exception as e:
            self.log_error(f"Enhanced JSON file download failed: {str(e)}")
            return False
    
    def run_complete_automation(self):
        """Run the enhanced complete automation process"""
        try:
            self.log_step("Starting enhanced complete Gmail OAuth automation")
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Step 1: Login
            if not self.login_to_google_cloud():
                return False
            
            # Step 2: Create project
            if not self.create_project():
                return False
            
            # Step 3: Enable Gmail API
            if not self.enable_gmail_api():
                return False
            
            # Step 4: Create OAuth credentials
            if not self.create_oauth_credentials():
                return False
            
            # Step 5: Download JSON file
            if not self.download_json_file():
                return False
            
            self.results["success"] = True
            self.log_step("Enhanced complete automation finished successfully!")
            return True
            
        except Exception as e:
            self.log_error(f"Enhanced complete automation failed: {str(e)}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
            
            # Save results
            results_file = f"enhanced_automation_results_{self.email.split('@')[0]}_{int(time.time())}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"\nResults saved to: {results_file}")
            return self.results["success"]

def main():
    """Test the enhanced automation with nilamb010@gmail.com"""
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    print(f"Starting enhanced complete Gmail OAuth automation for: {email}")
    
    automation = ImprovedGmailOAuthAutomation(email, password)
    success = automation.run_complete_automation()
    
    if success:
        print(f"\n✅ SUCCESS! Enhanced automation finished successfully!")
        print(f"JSON file created: {automation.results.get('json_file_path', 'Not found')}")
    else:
        print(f"\n❌ FAILED! Enhanced automation encountered errors.")
        print("Check the results file for detailed error information.")

if __name__ == "__main__":
    main()