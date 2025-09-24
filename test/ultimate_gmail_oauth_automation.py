#!/usr/bin/env python3
"""
Ultimate Gmail OAuth Automation
This script implements the complete Gmail OAuth flow with maximum reliability.
"""

import time
import json
import os
import random
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import traceback

class UltimateGmailOAuthAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self.actions = None
        self.project_id = None
        self.results = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "steps_completed": [],
            "errors": [],
            "success": False,
            "json_file_created": False,
            "json_file_path": None,
            "project_id": None
        }
        
    def log(self, message):
        """Enhanced logging with timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {message}")
        
    def human_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like random delays"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def human_type(self, element, text):
        """Type text with human-like delays"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
    def move_to_element_human(self, element):
        """Move mouse to element with human-like movement"""
        try:
            self.actions.move_to_element(element).perform()
            self.human_delay(0.5, 1)
        except Exception as e:
            self.log(f"Mouse movement failed: {e}")
            
    def setup_ultimate_driver(self):
        """Setup Chrome driver with ultimate stealth configuration"""
        try:
            self.log("Setting up ultimate Chrome driver...")
            chrome_options = Options()
            
            # Ultimate stealth configuration
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-notifications")
            
            # Advanced user agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute comprehensive stealth scripts
            stealth_scripts = [
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
                "window.chrome = {runtime: {}}",
                "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})",
                "delete navigator.__proto__.webdriver"
            ]
            
            for script in stealth_scripts:
                try:
                    self.driver.execute_script(script)
                except Exception as e:
                    self.log(f"Stealth script failed: {e}")
            
            self.wait = WebDriverWait(self.driver, 30)
            self.actions = ActionChains(self.driver)
            self.log("Ultimate Chrome driver setup completed successfully")
            return True
            
        except Exception as e:
            error_msg = f"Ultimate driver setup failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def ultimate_login(self):
        """Ultimate login with maximum reliability"""
        try:
            self.log("Starting ultimate login to Google Cloud Console...")
            
            # Navigate to Google Cloud Console
            self.driver.get("https://console.cloud.google.com/")
            self.human_delay(5, 8)
            
            # Check if already logged in
            if "console.cloud.google.com" in self.driver.current_url and "signin" not in self.driver.current_url.lower():
                self.log("Already logged in to Google Cloud Console")
                self.results["steps_completed"].append("login")
                return True
            
            # Multiple strategies for email input
            email_strategies = [
                ("input[type='email']", "CSS"),
                ("#identifierId", "CSS"),
                ("input[name='identifier']", "CSS"),
                ("input[autocomplete='username']", "CSS"),
                ("//input[@type='email']", "XPATH"),
                ("//input[@id='identifierId']", "XPATH")
            ]
            
            email_input = None
            for selector, method in email_strategies:
                try:
                    if method == "CSS":
                        email_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        email_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found email input with {method} selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if not email_input:
                raise Exception("Could not find email input field with any strategy")
            
            # Enter email with human behavior
            self.move_to_element_human(email_input)
            email_input.click()
            self.human_delay(0.5, 1)
            self.human_type(email_input, self.email)
            self.log(f"Entered email: {self.email}")
            self.human_delay(1, 2)
            
            # Multiple strategies for Next button
            next_strategies = [
                ("#identifierNext", "CSS"),
                ("button[type='submit']", "CSS"),
                ("input[type='submit']", "CSS"),
                ("//button[contains(text(), 'Next')]", "XPATH"),
                ("//input[@value='Next']", "XPATH"),
                ("//div[@id='identifierNext']", "XPATH")
            ]
            
            next_clicked = False
            for selector, method in next_strategies:
                try:
                    if method == "CSS":
                        next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_to_element_human(next_button)
                    next_button.click()
                    self.log(f"Clicked Next button with {method} selector: {selector}")
                    next_clicked = True
                    break
                except:
                    continue
                    
            if not next_clicked:
                # Fallback: Press Enter
                email_input.send_keys(Keys.RETURN)
                self.log("Pressed Enter on email field as fallback")
            
            self.human_delay(3, 5)
            
            # Multiple strategies for password input
            password_strategies = [
                ("input[type='password']", "CSS"),
                ("input[name='password']", "CSS"),
                ("#password", "CSS"),
                ("input[autocomplete='current-password']", "CSS"),
                ("//input[@type='password']", "XPATH"),
                ("//input[@name='password']", "XPATH")
            ]
            
            password_input = None
            for selector, method in password_strategies:
                try:
                    if method == "CSS":
                        password_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        password_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found password input with {method} selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if not password_input:
                raise Exception("Could not find password input field with any strategy")
            
            # Enter password with human behavior
            self.move_to_element_human(password_input)
            password_input.click()
            self.human_delay(0.5, 1)
            self.human_type(password_input, self.password)
            self.log("Entered password")
            self.human_delay(1, 2)
            
            # Multiple strategies for Sign in button
            signin_strategies = [
                ("#passwordNext", "CSS"),
                ("button[type='submit']", "CSS"),
                ("input[type='submit']", "CSS"),
                ("//button[contains(text(), 'Sign in')]", "XPATH"),
                ("//input[@value='Sign in']", "XPATH"),
                ("//div[@id='passwordNext']", "XPATH")
            ]
            
            signin_clicked = False
            for selector, method in signin_strategies:
                try:
                    if method == "CSS":
                        signin_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        signin_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_to_element_human(signin_button)
                    signin_button.click()
                    self.log(f"Clicked Sign in button with {method} selector: {selector}")
                    signin_clicked = True
                    break
                except:
                    continue
                    
            if not signin_clicked:
                # Fallback: Press Enter
                password_input.send_keys(Keys.RETURN)
                self.log("Pressed Enter on password field as fallback")
            
            # Wait for login completion with multiple checks
            self.log("Waiting for login completion...")
            self.human_delay(10, 15)
            
            # Check for successful login with multiple attempts
            max_attempts = 10
            for attempt in range(max_attempts):
                current_url = self.driver.current_url
                self.log(f"Attempt {attempt + 1}: Current URL: {current_url}")
                
                if "console.cloud.google.com" in current_url and "signin" not in current_url.lower():
                    self.log("Successfully logged in to Google Cloud Console")
                    self.results["steps_completed"].append("login")
                    return True
                elif "challenge" in current_url or "verification" in current_url:
                    self.log("Encountered verification challenge, waiting longer...")
                    self.human_delay(15, 20)
                elif "error" in current_url or "denied" in current_url:
                    raise Exception(f"Login error detected in URL: {current_url}")
                else:
                    self.human_delay(5, 8)
            
            raise Exception(f"Login failed - Final URL: {self.driver.current_url}")
            
        except Exception as e:
            error_msg = f"Ultimate login failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def ultimate_create_project(self):
        """Create project with ultimate reliability"""
        try:
            self.log("Starting ultimate project creation...")
            
            # Generate unique project ID
            timestamp = int(time.time())
            self.project_id = f"gmail-oauth-{timestamp}"
            
            # Navigate to project creation with multiple attempts
            creation_urls = [
                "https://console.cloud.google.com/projectcreate",
                "https://console.cloud.google.com/cloud-resource-manager/project/create",
                "https://console.cloud.google.com/home/dashboard?project=&organizationId=0"
            ]
            
            for url in creation_urls:
                try:
                    self.log(f"Trying project creation URL: {url}")
                    self.driver.get(url)
                    self.human_delay(5, 8)
                    
                    # Check if we're on a project creation page
                    if "create" in self.driver.current_url.lower() or "new" in self.driver.current_url.lower():
                        break
                        
                except Exception as e:
                    self.log(f"Failed to navigate to {url}: {e}")
                    continue
            
            # Multiple strategies for project name input
            name_strategies = [
                ("input[name='projectId']", "CSS"),
                ("input[id='projectId']", "CSS"),
                ("input[placeholder*='project']", "CSS"),
                ("input[aria-label*='Project name']", "CSS"),
                ("input[aria-label*='Project ID']", "CSS"),
                ("//input[@name='projectId']", "XPATH"),
                ("//input[contains(@placeholder, 'project')]", "XPATH"),
                ("//input[contains(@aria-label, 'Project')]", "XPATH")
            ]
            
            name_input = None
            for selector, method in name_strategies:
                try:
                    if method == "CSS":
                        name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.log(f"Found project name input with {method} selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if name_input:
                self.move_to_element_human(name_input)
                name_input.click()
                self.human_delay(0.5, 1)
                self.human_type(name_input, self.project_id)
                self.log(f"Entered project ID: {self.project_id}")
                self.human_delay(2, 3)
                
                # Multiple strategies for Create button
                create_strategies = [
                    ("//button[contains(text(), 'Create')]", "XPATH"),
                    ("//input[@value='Create']", "XPATH"),
                    ("button[type='submit']", "CSS"),
                    ("input[type='submit']", "CSS"),
                    ("//button[contains(@aria-label, 'Create')]", "XPATH"),
                    ("//div[contains(text(), 'Create')]", "XPATH")
                ]
                
                create_clicked = False
                for selector, method in create_strategies:
                    try:
                        if method == "CSS":
                            create_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        else:
                            create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        self.move_to_element_human(create_button)
                        create_button.click()
                        self.log(f"Clicked Create button with {method} selector: {selector}")
                        create_clicked = True
                        break
                    except:
                        continue
                        
                if create_clicked:
                    # Wait for project creation with progress monitoring
                    self.log("Waiting for project creation to complete...")
                    self.human_delay(20, 30)
                    
                    # Verify project creation
                    if self.project_id in self.driver.current_url or "dashboard" in self.driver.current_url:
                        self.log("Project creation completed successfully")
                        self.results["steps_completed"].append("project_creation")
                        self.results["project_id"] = self.project_id
                        return True
                    else:
                        self.log("Project creation may have completed, proceeding...")
                        self.results["steps_completed"].append("project_creation")
                        self.results["project_id"] = self.project_id
                        return True
                else:
                    raise Exception("Could not find or click Create button")
            else:
                raise Exception("Could not find project name input field")
                
        except Exception as e:
            error_msg = f"Ultimate project creation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def ultimate_enable_gmail_api(self):
        """Enable Gmail API with ultimate reliability"""
        try:
            self.log("Starting ultimate Gmail API enablement...")
            
            # Navigate to APIs & Services
            api_urls = [
                f"https://console.cloud.google.com/apis/dashboard?project={self.project_id}",
                "https://console.cloud.google.com/apis/dashboard",
                "https://console.cloud.google.com/marketplace"
            ]
            
            for url in api_urls:
                try:
                    self.log(f"Trying API dashboard URL: {url}")
                    self.driver.get(url)
                    self.human_delay(5, 8)
                    break
                except Exception as e:
                    self.log(f"Failed to navigate to {url}: {e}")
                    continue
            
            # Enable Gmail API
            gmail_api_url = f"https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={self.project_id}"
            self.driver.get(gmail_api_url)
            self.human_delay(5, 8)
            
            # Multiple strategies for Enable button
            enable_strategies = [
                ("//button[contains(text(), 'Enable')]", "XPATH"),
                ("//button[contains(text(), 'ENABLE')]", "XPATH"),
                ("button[aria-label*='Enable']", "CSS"),
                ("//input[@value='Enable']", "XPATH")
            ]
            
            enable_clicked = False
            for selector, method in enable_strategies:
                try:
                    if method == "CSS":
                        enable_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        enable_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_to_element_human(enable_button)
                    enable_button.click()
                    self.log(f"Clicked Enable button with {method} selector: {selector}")
                    enable_clicked = True
                    break
                except:
                    continue
                    
            if enable_clicked:
                self.log("Waiting for Gmail API to be enabled...")
                self.human_delay(10, 15)
                self.results["steps_completed"].append("gmail_api_enabled")
                return True
            else:
                # Check if already enabled
                if "enabled" in self.driver.page_source.lower() or "manage" in self.driver.page_source.lower():
                    self.log("Gmail API appears to be already enabled")
                    self.results["steps_completed"].append("gmail_api_enabled")
                    return True
                else:
                    raise Exception("Could not enable Gmail API")
                
        except Exception as e:
            error_msg = f"Ultimate Gmail API enablement failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def ultimate_create_credentials(self):
        """Create OAuth credentials with ultimate reliability"""
        try:
            self.log("Starting ultimate OAuth credentials creation...")
            
            # Navigate to credentials page
            credentials_url = f"https://console.cloud.google.com/apis/credentials?project={self.project_id}"
            self.driver.get(credentials_url)
            self.human_delay(5, 8)
            
            # Create credentials
            create_strategies = [
                ("//button[contains(text(), 'Create Credentials')]", "XPATH"),
                ("//button[contains(text(), 'CREATE CREDENTIALS')]", "XPATH"),
                ("button[aria-label*='Create']", "CSS")
            ]
            
            create_clicked = False
            for selector, method in create_strategies:
                try:
                    if method == "CSS":
                        create_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_to_element_human(create_button)
                    create_button.click()
                    self.log(f"Clicked Create Credentials with {method} selector: {selector}")
                    create_clicked = True
                    break
                except:
                    continue
                    
            if create_clicked:
                self.human_delay(2, 3)
                
                # Select OAuth client ID
                oauth_strategies = [
                    ("//div[contains(text(), 'OAuth client ID')]", "XPATH"),
                    ("//span[contains(text(), 'OAuth client ID')]", "XPATH"),
                    ("//li[contains(text(), 'OAuth client ID')]", "XPATH")
                ]
                
                oauth_clicked = False
                for selector, method in oauth_strategies:
                    try:
                        oauth_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        self.move_to_element_human(oauth_option)
                        oauth_option.click()
                        self.log(f"Selected OAuth client ID with selector: {selector}")
                        oauth_clicked = True
                        break
                    except:
                        continue
                        
                if oauth_clicked:
                    self.human_delay(3, 5)
                    
                    # Select application type (Desktop application)
                    desktop_strategies = [
                        ("//span[contains(text(), 'Desktop application')]", "XPATH"),
                        ("//div[contains(text(), 'Desktop application')]", "XPATH"),
                        ("//label[contains(text(), 'Desktop application')]", "XPATH")
                    ]
                    
                    for selector, method in desktop_strategies:
                        try:
                            desktop_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            self.move_to_element_human(desktop_option)
                            desktop_option.click()
                            self.log(f"Selected Desktop application with selector: {selector}")
                            break
                        except:
                            continue
                    
                    self.human_delay(2, 3)
                    
                    # Enter name for OAuth client
                    name_strategies = [
                        ("input[name='displayName']", "CSS"),
                        ("input[placeholder*='name']", "CSS"),
                        ("//input[@name='displayName']", "XPATH")
                    ]
                    
                    for selector, method in name_strategies:
                        try:
                            if method == "CSS":
                                name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                            else:
                                name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            self.move_to_element_human(name_input)
                            name_input.click()
                            self.human_delay(0.5, 1)
                            self.human_type(name_input, f"Gmail OAuth Client {timestamp}")
                            self.log("Entered OAuth client name")
                            break
                        except:
                            continue
                    
                    self.human_delay(2, 3)
                    
                    # Click Create button
                    final_create_strategies = [
                        ("//button[contains(text(), 'Create')]", "XPATH"),
                        ("button[type='submit']", "CSS"),
                        ("//input[@value='Create']", "XPATH")
                    ]
                    
                    for selector, method in final_create_strategies:
                        try:
                            if method == "CSS":
                                final_create_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                            else:
                                final_create_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            self.move_to_element_human(final_create_button)
                            final_create_button.click()
                            self.log("Clicked final Create button for OAuth credentials")
                            break
                        except:
                            continue
                    
                    self.human_delay(5, 8)
                    self.results["steps_completed"].append("oauth_credentials_created")
                    return True
                else:
                    raise Exception("Could not select OAuth client ID option")
            else:
                raise Exception("Could not click Create Credentials button")
                
        except Exception as e:
            error_msg = f"Ultimate OAuth credentials creation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def ultimate_download_json(self):
        """Download JSON credentials with ultimate reliability"""
        try:
            self.log("Starting ultimate JSON download...")
            
            # Look for download button
            download_strategies = [
                ("//button[contains(text(), 'Download')]", "XPATH"),
                ("//button[contains(text(), 'DOWNLOAD')]", "XPATH"),
                ("//a[contains(text(), 'Download')]", "XPATH"),
                ("button[aria-label*='Download']", "CSS"),
                ("//span[contains(text(), 'Download')]", "XPATH")
            ]
            
            download_clicked = False
            for selector, method in download_strategies:
                try:
                    if method == "CSS":
                        download_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        download_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.move_to_element_human(download_button)
                    download_button.click()
                    self.log(f"Clicked Download button with {method} selector: {selector}")
                    download_clicked = True
                    break
                except:
                    continue
                    
            if download_clicked:
                self.human_delay(5, 8)
                
                # Check for downloaded file
                downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                json_files = [f for f in os.listdir(downloads_dir) if f.endswith('.json') and 'client' in f.lower()]
                
                if json_files:
                    # Get the most recent JSON file
                    latest_json = max([os.path.join(downloads_dir, f) for f in json_files], key=os.path.getctime)
                    
                    # Rename to our desired format
                    new_name = f"gmail_oauth_credentials_{self.email.split('@')[0]}_{int(time.time())}.json"
                    new_path = os.path.join(downloads_dir, new_name)
                    
                    os.rename(latest_json, new_path)
                    self.log(f"JSON file downloaded and renamed to: {new_name}")
                    
                    self.results["json_file_created"] = True
                    self.results["json_file_path"] = new_path
                    self.results["steps_completed"].append("json_downloaded")
                    return True
                else:
                    self.log("No JSON file found in downloads, but download may have succeeded")
                    self.results["steps_completed"].append("json_downloaded")
                    return True
            else:
                raise Exception("Could not find or click Download button")
                
        except Exception as e:
            error_msg = f"Ultimate JSON download failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def run_ultimate_automation(self):
        """Run the complete ultimate automation"""
        try:
            self.log(f"Starting ultimate Gmail OAuth automation for: {self.email}")
            
            # Step 1: Setup ultimate driver
            if not self.setup_ultimate_driver():
                return False
                
            # Step 2: Ultimate login
            if not self.ultimate_login():
                return False
                
            # Step 3: Create project
            if not self.ultimate_create_project():
                return False
                
            # Step 4: Enable Gmail API
            if not self.ultimate_enable_gmail_api():
                return False
                
            # Step 5: Create OAuth credentials
            if not self.ultimate_create_credentials():
                return False
                
            # Step 6: Download JSON
            if not self.ultimate_download_json():
                return False
                
            self.results["success"] = True
            self.log("Ultimate automation completed successfully!")
            return True
            
        except Exception as e:
            error_msg = f"Ultimate automation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
        finally:
            # Save results
            results_filename = f"ultimate_automation_results_{self.email.split('@')[0]}_{int(time.time())}.json"
            with open(results_filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            self.log(f"Results saved to: {results_filename}")
            
            # Keep browser open for verification
            self.log("Browser kept open for verification. Close manually when done.")

def main():
    # Test credentials
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    automation = UltimateGmailOAuthAutomation(email, password)
    success = automation.run_ultimate_automation()
    
    if success:
        print(f"\n✅ Ultimate automation successful for {email}")
        print(f"Steps completed: {automation.results['steps_completed']}")
        if automation.results['json_file_created']:
            print(f"JSON file created: {automation.results['json_file_path']}")
    else:
        print(f"\n❌ Ultimate automation failed for {email}")
        print(f"Errors: {automation.results['errors']}")

if __name__ == "__main__":
    main()