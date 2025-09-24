#!/usr/bin/env python3
"""
Complete Gmail OAuth Automation Script
Handles all steps: Login → Project Creation → Gmail API Enable → OAuth Credentials → JSON Download
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

class CompleteGmailOAuthAutomation:
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
        """Setup Chrome driver with appropriate options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
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
            self.wait = WebDriverWait(self.driver, 20)
            
            self.log_step("Driver setup completed successfully")
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
    
    def login_to_google_cloud(self):
        """Step 1: Login to Google Cloud Console"""
        try:
            self.log_step("Starting login to Google Cloud Console")
            self.driver.get("https://console.cloud.google.com/")
            time.sleep(3)
            
            # Check if already logged in
            if "console.cloud.google.com" in self.driver.current_url and "getting-started" in self.driver.current_url:
                self.log_step("Already logged in to Google Cloud Console")
                return True
            
            # Enter email
            email_field = self.wait.until(EC.element_to_be_clickable((By.ID, "identifierId")))
            email_field.clear()
            email_field.send_keys(self.email)
            self.log_step(f"Entered email: {self.email}")
            
            # Click Next
            next_button = self.wait.until(EC.element_to_be_clickable((By.ID, "identifierNext")))
            next_button.click()
            time.sleep(3)
            
            # Enter password
            password_field = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_field.clear()
            password_field.send_keys(self.password)
            self.log_step("Entered password")
            
            # Click Sign in
            signin_button = self.wait.until(EC.element_to_be_clickable((By.ID, "passwordNext")))
            signin_button.click()
            time.sleep(5)
            
            # Wait for login to complete
            self.wait.until(lambda driver: "console.cloud.google.com" in driver.current_url)
            self.log_step("Successfully logged in to Google Cloud Console")
            return True
            
        except Exception as e:
            self.log_error(f"Login failed: {str(e)}")
            return False
    
    def create_project(self):
        """Step 2: Create a new project"""
        try:
            self.log_step("Starting project creation")
            
            # Navigate to project selector
            try:
                # Try to find project selector dropdown
                project_selector = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='project-switcher-button'], .cfc-project-switcher-button, [aria-label*='project'], [aria-label*='Project']")))
                project_selector.click()
                time.sleep(2)
                self.log_step("Clicked project selector")
            except:
                # Alternative: Navigate directly to project creation
                self.driver.get("https://console.cloud.google.com/projectcreate")
                time.sleep(3)
                self.log_step("Navigated directly to project creation")
            
            # Look for "New Project" button
            try:
                new_project_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'New Project') or contains(text(), 'NEW PROJECT') or contains(text(), 'Create Project')]")))
                new_project_button.click()
                time.sleep(2)
                self.log_step("Clicked New Project button")
            except:
                # If already on project creation page
                self.log_step("Already on project creation page")
            
            # Enter project name
            project_name_field = self.wait.until(EC.element_to_be_clickable((By.ID, "projectId")))
            project_name_field.clear()
            project_name_field.send_keys(self.project_name)
            self.log_step(f"Entered project name: {self.project_name}")
            
            # Click Create button
            create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create') or contains(text(), 'CREATE')]")))
            create_button.click()
            self.log_step("Clicked Create button")
            
            # Wait for project creation to complete
            time.sleep(10)
            self.log_step("Project creation completed")
            return True
            
        except Exception as e:
            self.log_error(f"Project creation failed: {str(e)}")
            return False
    
    def enable_gmail_api(self):
        """Step 3: Enable Gmail API"""
        try:
            self.log_step("Starting Gmail API enablement")
            
            # Navigate to API Library
            self.driver.get("https://console.cloud.google.com/apis/library")
            time.sleep(3)
            
            # Search for Gmail API
            search_box = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Search'], input[aria-label*='Search']")))
            search_box.clear()
            search_box.send_keys("Gmail API")
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            self.log_step("Searched for Gmail API")
            
            # Click on Gmail API
            gmail_api_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'gmail') or .//span[contains(text(), 'Gmail API')]]")))
            gmail_api_link.click()
            time.sleep(3)
            self.log_step("Clicked on Gmail API")
            
            # Enable the API
            try:
                enable_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enable') or contains(text(), 'ENABLE')]")))
                enable_button.click()
                time.sleep(5)
                self.log_step("Clicked Enable button for Gmail API")
            except:
                self.log_step("Gmail API might already be enabled")
            
            return True
            
        except Exception as e:
            self.log_error(f"Gmail API enablement failed: {str(e)}")
            return False
    
    def create_oauth_credentials(self):
        """Step 4: Create OAuth credentials"""
        try:
            self.log_step("Starting OAuth credentials creation")
            
            # Navigate to Credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(3)
            
            # Click Create Credentials
            create_credentials_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create Credentials') or contains(text(), 'CREATE CREDENTIALS')]")))
            create_credentials_button.click()
            time.sleep(2)
            self.log_step("Clicked Create Credentials")
            
            # Select OAuth client ID
            oauth_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'OAuth client ID')]")))
            oauth_option.click()
            time.sleep(3)
            self.log_step("Selected OAuth client ID")
            
            # Select application type (Desktop application)
            app_type_dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select, .mat-select-trigger")))
            if app_type_dropdown.tag_name == "select":
                select = Select(app_type_dropdown)
                select.select_by_visible_text("Desktop application")
            else:
                app_type_dropdown.click()
                time.sleep(1)
                desktop_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Desktop application')]")))
                desktop_option.click()
            
            self.log_step("Selected Desktop application type")
            
            # Enter name for OAuth client
            name_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label*='Name'], input[placeholder*='Name']")))
            oauth_name = f"Gmail OAuth Client {self.email.split('@')[0]}"
            name_field.clear()
            name_field.send_keys(oauth_name)
            self.log_step(f"Entered OAuth client name: {oauth_name}")
            
            # Click Create
            create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create') or contains(text(), 'CREATE')]")))
            create_button.click()
            time.sleep(5)
            self.log_step("Clicked Create for OAuth credentials")
            
            return True
            
        except Exception as e:
            self.log_error(f"OAuth credentials creation failed: {str(e)}")
            return False
    
    def download_json_file(self):
        """Step 5: Download JSON file with proper naming"""
        try:
            self.log_step("Starting JSON file download")
            
            # Look for download button in the success dialog
            try:
                download_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Download') or contains(text(), 'DOWNLOAD')]")))
                download_button.click()
                time.sleep(3)
                self.log_step("Clicked Download button from success dialog")
            except:
                # Alternative: Look for download icon in credentials list
                download_icon = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label*='download'], .download-icon, [title*='Download']")))
                download_icon.click()
                time.sleep(3)
                self.log_step("Clicked Download icon from credentials list")
            
            # Wait for download to complete
            time.sleep(5)
            
            # Find the downloaded file and rename it
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
            self.log_error(f"JSON file download failed: {str(e)}")
            return False
    
    def run_complete_automation(self):
        """Run the complete automation process"""
        try:
            self.log_step("Starting complete Gmail OAuth automation")
            
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
            self.log_step("Complete automation finished successfully!")
            return True
            
        except Exception as e:
            self.log_error(f"Complete automation failed: {str(e)}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
            
            # Save results
            results_file = f"complete_automation_results_{self.email.split('@')[0]}_{int(time.time())}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"\nResults saved to: {results_file}")
            return self.results["success"]

def main():
    """Test the complete automation with nilamb010@gmail.com"""
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    print(f"Starting complete Gmail OAuth automation for: {email}")
    
    automation = CompleteGmailOAuthAutomation(email, password)
    success = automation.run_complete_automation()
    
    if success:
        print(f"\n✅ SUCCESS! Complete automation finished successfully!")
        print(f"JSON file created: {automation.results.get('json_file_path', 'Not found')}")
    else:
        print(f"\n❌ FAILED! Automation encountered errors.")
        print("Check the results file for detailed error information.")

if __name__ == "__main__":
    main()