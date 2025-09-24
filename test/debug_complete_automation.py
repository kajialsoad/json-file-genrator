#!/usr/bin/env python3
"""
Enhanced Gmail OAuth Automation with Step-by-Step Debugging
This script automates the complete Gmail OAuth setup process with detailed logging and error handling.
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import traceback

class GmailOAuthAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self.results = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "steps_completed": [],
            "errors": [],
            "success": False,
            "json_file_created": False
        }
        
    def log(self, message):
        """Enhanced logging with timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {message}")
        
    def save_screenshot(self, step_name):
        """Save screenshot for debugging"""
        try:
            screenshot_path = f"debug_screenshot_{step_name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            self.log(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.log(f"Failed to save screenshot: {str(e)}")
            return None
            
    def setup_driver(self):
        """Setup Chrome driver with enhanced options"""
        try:
            self.log("Setting up Chrome driver...")
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            self.log("Chrome driver setup completed successfully")
            return True
        except Exception as e:
            error_msg = f"Driver setup failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def login_to_google_cloud(self):
        """Enhanced login with detailed debugging"""
        try:
            self.log("Starting login to Google Cloud Console...")
            self.driver.get("https://console.cloud.google.com/")
            time.sleep(3)
            
            # Check if already logged in
            if "console.cloud.google.com" in self.driver.current_url and "signin" not in self.driver.current_url:
                self.log("Already logged in to Google Cloud Console")
                self.results["steps_completed"].append("login")
                return True
            
            # Wait for email input
            self.log("Waiting for email input field...")
            email_input = self.wait.until(EC.element_to_be_clickable((By.ID, "identifierId")))
            email_input.clear()
            email_input.send_keys(self.email)
            self.log(f"Entered email: {self.email}")
            
            # Click Next
            next_button = self.wait.until(EC.element_to_be_clickable((By.ID, "identifierNext")))
            next_button.click()
            self.log("Clicked Next button")
            time.sleep(3)
            
            # Wait for password input
            self.log("Waiting for password input field...")
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.clear()
            password_input.send_keys(self.password)
            self.log("Entered password")
            
            # Click Sign in
            signin_button = self.wait.until(EC.element_to_be_clickable((By.ID, "passwordNext")))
            signin_button.click()
            self.log("Clicked Sign in button")
            
            # Wait for successful login
            self.log("Waiting for login completion...")
            time.sleep(10)
            
            # Check if login was successful
            if "console.cloud.google.com" in self.driver.current_url:
                self.log("Successfully logged in to Google Cloud Console")
                self.results["steps_completed"].append("login")
                self.save_screenshot("login_success")
                return True
            else:
                error_msg = f"Login failed - Current URL: {self.driver.current_url}"
                self.log(error_msg)
                self.results["errors"].append(error_msg)
                self.save_screenshot("login_failed")
                return False
                
        except Exception as e:
            error_msg = f"Login failed with exception: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            self.save_screenshot("login_exception")
            return False
            
    def create_project(self):
        """Enhanced project creation with debugging"""
        try:
            self.log("Starting project creation...")
            
            # Look for project selector
            project_selectors = [
                "//span[contains(text(), 'Select a project')]",
                "//button[contains(@aria-label, 'Select a project')]",
                "//div[contains(@class, 'project-selector')]",
                "//button[contains(text(), 'Select a project')]"
            ]
            
            project_button = None
            for selector in project_selectors:
                try:
                    project_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found project selector with: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if not project_button:
                self.log("Could not find project selector, trying alternative approach...")
                # Try to navigate directly to project creation
                self.driver.get("https://console.cloud.google.com/projectcreate")
                time.sleep(5)
            else:
                project_button.click()
                self.log("Clicked project selector")
                time.sleep(3)
                
                # Look for "New Project" button
                new_project_selectors = [
                    "//span[contains(text(), 'New Project')]",
                    "//button[contains(text(), 'New Project')]",
                    "//a[contains(text(), 'New Project')]"
                ]
                
                new_project_button = None
                for selector in new_project_selectors:
                    try:
                        new_project_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        self.log(f"Found new project button with: {selector}")
                        break
                    except TimeoutException:
                        continue
                        
                if new_project_button:
                    new_project_button.click()
                    self.log("Clicked New Project button")
                    time.sleep(5)
                else:
                    self.log("Could not find New Project button, navigating directly...")
                    self.driver.get("https://console.cloud.google.com/projectcreate")
                    time.sleep(5)
            
            # Fill project name
            project_name = f"gmail-oauth-{int(time.time())}"
            name_selectors = [
                "//input[@id='projectId']",
                "//input[@name='projectId']",
                "//input[contains(@placeholder, 'project name')]",
                "//input[contains(@aria-label, 'Project name')]"
            ]
            
            name_input = None
            for selector in name_selectors:
                try:
                    name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found project name input with: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if name_input:
                name_input.clear()
                name_input.send_keys(project_name)
                self.log(f"Entered project name: {project_name}")
                
                # Click Create button
                create_selectors = [
                    "//button[contains(text(), 'Create')]",
                    "//span[contains(text(), 'Create')]//parent::button",
                    "//input[@value='Create']"
                ]
                
                create_button = None
                for selector in create_selectors:
                    try:
                        create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        self.log(f"Found create button with: {selector}")
                        break
                    except TimeoutException:
                        continue
                        
                if create_button:
                    create_button.click()
                    self.log("Clicked Create button")
                    
                    # Wait for project creation to complete
                    self.log("Waiting for project creation to complete...")
                    time.sleep(15)
                    
                    self.results["steps_completed"].append("project_creation")
                    self.save_screenshot("project_created")
                    return True
                else:
                    error_msg = "Could not find Create button"
                    self.log(error_msg)
                    self.results["errors"].append(error_msg)
                    self.save_screenshot("create_button_not_found")
                    return False
            else:
                error_msg = "Could not find project name input field"
                self.log(error_msg)
                self.results["errors"].append(error_msg)
                self.save_screenshot("name_input_not_found")
                return False
                
        except Exception as e:
            error_msg = f"Project creation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            self.save_screenshot("project_creation_exception")
            return False
            
    def enable_gmail_api(self):
        """Enable Gmail API with debugging"""
        try:
            self.log("Starting Gmail API enablement...")
            
            # Navigate to API Library
            self.driver.get("https://console.cloud.google.com/apis/library")
            time.sleep(5)
            
            # Search for Gmail API
            search_selectors = [
                "//input[@placeholder='Search for APIs & Services']",
                "//input[contains(@aria-label, 'Search')]",
                "//input[@type='search']"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found search input with: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if search_input:
                search_input.clear()
                search_input.send_keys("Gmail API")
                self.log("Searched for Gmail API")
                time.sleep(3)
                
                # Click on Gmail API result
                gmail_api_selectors = [
                    "//div[contains(text(), 'Gmail API')]",
                    "//span[contains(text(), 'Gmail API')]",
                    "//a[contains(text(), 'Gmail API')]"
                ]
                
                gmail_api_link = None
                for selector in gmail_api_selectors:
                    try:
                        gmail_api_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        self.log(f"Found Gmail API link with: {selector}")
                        break
                    except TimeoutException:
                        continue
                        
                if gmail_api_link:
                    gmail_api_link.click()
                    self.log("Clicked Gmail API")
                    time.sleep(5)
                    
                    # Click Enable button
                    enable_selectors = [
                        "//button[contains(text(), 'Enable')]",
                        "//span[contains(text(), 'Enable')]//parent::button"
                    ]
                    
                    enable_button = None
                    for selector in enable_selectors:
                        try:
                            enable_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            self.log(f"Found enable button with: {selector}")
                            break
                        except TimeoutException:
                            continue
                            
                    if enable_button:
                        enable_button.click()
                        self.log("Clicked Enable button")
                        time.sleep(10)
                        
                        self.results["steps_completed"].append("gmail_api_enabled")
                        self.save_screenshot("gmail_api_enabled")
                        return True
                    else:
                        error_msg = "Could not find Enable button"
                        self.log(error_msg)
                        self.results["errors"].append(error_msg)
                        return False
                else:
                    error_msg = "Could not find Gmail API in search results"
                    self.log(error_msg)
                    self.results["errors"].append(error_msg)
                    return False
            else:
                error_msg = "Could not find search input"
                self.log(error_msg)
                self.results["errors"].append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Gmail API enablement failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            self.save_screenshot("gmail_api_exception")
            return False
            
    def create_oauth_credentials(self):
        """Create OAuth credentials with debugging"""
        try:
            self.log("Starting OAuth credentials creation...")
            
            # Navigate to Credentials page
            self.driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(5)
            
            # Click Create Credentials
            create_creds_selectors = [
                "//button[contains(text(), 'CREATE CREDENTIALS')]",
                "//span[contains(text(), 'CREATE CREDENTIALS')]//parent::button",
                "//button[contains(text(), 'Create Credentials')]"
            ]
            
            create_creds_button = None
            for selector in create_creds_selectors:
                try:
                    create_creds_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found create credentials button with: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if create_creds_button:
                create_creds_button.click()
                self.log("Clicked Create Credentials")
                time.sleep(3)
                
                # Select OAuth client ID
                oauth_selectors = [
                    "//span[contains(text(), 'OAuth client ID')]",
                    "//div[contains(text(), 'OAuth client ID')]",
                    "//li[contains(text(), 'OAuth client ID')]"
                ]
                
                oauth_option = None
                for selector in oauth_selectors:
                    try:
                        oauth_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        self.log(f"Found OAuth client ID option with: {selector}")
                        break
                    except TimeoutException:
                        continue
                        
                if oauth_option:
                    oauth_option.click()
                    self.log("Selected OAuth client ID")
                    time.sleep(5)
                    
                    # Select application type (Desktop application)
                    app_type_selectors = [
                        "//span[contains(text(), 'Desktop application')]",
                        "//label[contains(text(), 'Desktop application')]",
                        "//input[@value='DESKTOP']//following-sibling::span"
                    ]
                    
                    app_type_option = None
                    for selector in app_type_selectors:
                        try:
                            app_type_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            self.log(f"Found desktop application option with: {selector}")
                            break
                        except TimeoutException:
                            continue
                            
                    if app_type_option:
                        app_type_option.click()
                        self.log("Selected Desktop application")
                        time.sleep(3)
                        
                        # Enter name for OAuth client
                        name_input_selectors = [
                            "//input[@id='name']",
                            "//input[@name='name']",
                            "//input[contains(@placeholder, 'name')]"
                        ]
                        
                        name_input = None
                        for selector in name_input_selectors:
                            try:
                                name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                                self.log(f"Found name input with: {selector}")
                                break
                            except TimeoutException:
                                continue
                                
                        if name_input:
                            oauth_name = f"Gmail OAuth Client {int(time.time())}"
                            name_input.clear()
                            name_input.send_keys(oauth_name)
                            self.log(f"Entered OAuth client name: {oauth_name}")
                            
                            # Click Create button
                            create_button_selectors = [
                                "//button[contains(text(), 'Create')]",
                                "//span[contains(text(), 'Create')]//parent::button"
                            ]
                            
                            create_button = None
                            for selector in create_button_selectors:
                                try:
                                    create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                                    self.log(f"Found create button with: {selector}")
                                    break
                                except TimeoutException:
                                    continue
                                    
                            if create_button:
                                create_button.click()
                                self.log("Clicked Create button for OAuth credentials")
                                time.sleep(10)
                                
                                self.results["steps_completed"].append("oauth_credentials_created")
                                self.save_screenshot("oauth_credentials_created")
                                return True
                            else:
                                error_msg = "Could not find Create button for OAuth credentials"
                                self.log(error_msg)
                                self.results["errors"].append(error_msg)
                                return False
                        else:
                            error_msg = "Could not find name input for OAuth client"
                            self.log(error_msg)
                            self.results["errors"].append(error_msg)
                            return False
                    else:
                        error_msg = "Could not find Desktop application option"
                        self.log(error_msg)
                        self.results["errors"].append(error_msg)
                        return False
                else:
                    error_msg = "Could not find OAuth client ID option"
                    self.log(error_msg)
                    self.results["errors"].append(error_msg)
                    return False
            else:
                error_msg = "Could not find Create Credentials button"
                self.log(error_msg)
                self.results["errors"].append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"OAuth credentials creation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            self.save_screenshot("oauth_credentials_exception")
            return False
            
    def download_json_file(self):
        """Download JSON credentials file with debugging"""
        try:
            self.log("Starting JSON file download...")
            
            # Look for download button
            download_selectors = [
                "//button[contains(text(), 'DOWNLOAD JSON')]",
                "//span[contains(text(), 'DOWNLOAD JSON')]//parent::button",
                "//button[contains(@aria-label, 'download')]",
                "//a[contains(text(), 'Download')]"
            ]
            
            download_button = None
            for selector in download_selectors:
                try:
                    download_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found download button with: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if download_button:
                download_button.click()
                self.log("Clicked download button")
                time.sleep(5)
                
                # Check if file was downloaded
                downloads_path = os.path.expanduser("~/Downloads")
                json_files = [f for f in os.listdir(downloads_path) if f.endswith('.json') and 'client_secret' in f]
                
                if json_files:
                    # Rename the file
                    latest_file = max([os.path.join(downloads_path, f) for f in json_files], key=os.path.getctime)
                    new_filename = f"{self.email.split('@')[0]}_gmail_oauth.json"
                    new_filepath = os.path.join(downloads_path, new_filename)
                    
                    os.rename(latest_file, new_filepath)
                    self.log(f"JSON file downloaded and renamed to: {new_filename}")
                    
                    self.results["steps_completed"].append("json_file_downloaded")
                    self.results["json_file_created"] = True
                    self.results["json_file_path"] = new_filepath
                    self.save_screenshot("json_downloaded")
                    return True
                else:
                    error_msg = "JSON file not found in downloads"
                    self.log(error_msg)
                    self.results["errors"].append(error_msg)
                    return False
            else:
                error_msg = "Could not find download button"
                self.log(error_msg)
                self.results["errors"].append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"JSON file download failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            self.save_screenshot("json_download_exception")
            return False
            
    def run_complete_automation(self):
        """Run the complete automation process"""
        try:
            self.log(f"Starting complete Gmail OAuth automation for: {self.email}")
            
            # Step 1: Setup driver
            if not self.setup_driver():
                return False
                
            # Step 2: Login
            if not self.login_to_google_cloud():
                return False
                
            # Step 3: Create project
            if not self.create_project():
                return False
                
            # Step 4: Enable Gmail API
            if not self.enable_gmail_api():
                return False
                
            # Step 5: Create OAuth credentials
            if not self.create_oauth_credentials():
                return False
                
            # Step 6: Download JSON file
            if not self.download_json_file():
                return False
                
            self.results["success"] = True
            self.log("Complete automation successful!")
            return True
            
        except Exception as e:
            error_msg = f"Complete automation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
        finally:
            # Save results
            results_filename = f"debug_automation_results_{self.email.split('@')[0]}_{int(time.time())}.json"
            with open(results_filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            self.log(f"Results saved to: {results_filename}")
            
            # Close driver
            if self.driver:
                self.driver.quit()
                self.log("Browser closed")

def main():
    # Test credentials
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    automation = GmailOAuthAutomation(email, password)
    success = automation.run_complete_automation()
    
    if success:
        print(f"\n✅ Complete automation successful for {email}")
        print(f"JSON file created: {automation.results.get('json_file_created', False)}")
    else:
        print(f"\n❌ Automation failed for {email}")
        print(f"Errors: {automation.results['errors']}")

if __name__ == "__main__":
    main()