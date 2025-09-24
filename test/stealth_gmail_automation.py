#!/usr/bin/env python3
"""
Advanced Stealth Gmail OAuth Automation
This script uses advanced techniques to bypass Google's automation detection.
"""

import time
import json
import os
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import traceback

class StealthGmailOAuthAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self.actions = None
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
        self.actions.move_to_element(element).perform()
        self.human_delay(0.5, 1)
        
    def setup_stealth_driver(self):
        """Setup Chrome driver with advanced stealth options"""
        try:
            self.log("Setting up stealth Chrome driver...")
            chrome_options = Options()
            
            # Basic stealth options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Advanced stealth options
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-default-apps")
            
            # User agent rotation
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Window size randomization
            window_sizes = ["1366,768", "1920,1080", "1440,900", "1536,864"]
            chrome_options.add_argument(f"--window-size={random.choice(window_sizes)}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute stealth scripts
            stealth_scripts = [
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
                "window.chrome = {runtime: {}}",
                "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})"
            ]
            
            for script in stealth_scripts:
                self.driver.execute_script(script)
            
            self.wait = WebDriverWait(self.driver, 30)
            self.actions = ActionChains(self.driver)
            self.log("Stealth Chrome driver setup completed successfully")
            return True
            
        except Exception as e:
            error_msg = f"Stealth driver setup failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def stealth_login_to_google_cloud(self):
        """Enhanced stealth login with human-like behavior"""
        try:
            self.log("Starting stealth login to Google Cloud Console...")
            
            # Navigate with random delay
            self.driver.get("https://accounts.google.com/")
            self.human_delay(3, 5)
            
            # Navigate to Google Cloud Console
            self.driver.get("https://console.cloud.google.com/")
            self.human_delay(5, 8)
            
            # Check if already logged in
            if "console.cloud.google.com" in self.driver.current_url and "signin" not in self.driver.current_url:
                self.log("Already logged in to Google Cloud Console")
                self.results["steps_completed"].append("login")
                return True
            
            # Wait for email input with multiple selectors
            email_selectors = [
                "input[type='email']",
                "#identifierId",
                "input[name='identifier']",
                "input[autocomplete='username']"
            ]
            
            email_input = None
            for selector in email_selectors:
                try:
                    email_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.log(f"Found email input with selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if not email_input:
                raise Exception("Could not find email input field")
            
            # Human-like interaction with email field
            self.move_to_element_human(email_input)
            email_input.click()
            self.human_delay(0.5, 1)
            self.human_type(email_input, self.email)
            self.log(f"Entered email: {self.email}")
            self.human_delay(1, 2)
            
            # Find and click Next button
            next_selectors = [
                "#identifierNext",
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Next')"
            ]
            
            next_button = None
            for selector in next_selectors:
                try:
                    next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.log(f"Found next button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if next_button:
                self.move_to_element_human(next_button)
                next_button.click()
                self.log("Clicked Next button")
                self.human_delay(3, 5)
            else:
                # Try pressing Enter
                email_input.send_keys(Keys.RETURN)
                self.log("Pressed Enter on email field")
                self.human_delay(3, 5)
            
            # Wait for password input
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password",
                "input[autocomplete='current-password']"
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.log(f"Found password input with selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if not password_input:
                raise Exception("Could not find password input field")
            
            # Human-like interaction with password field
            self.move_to_element_human(password_input)
            password_input.click()
            self.human_delay(0.5, 1)
            self.human_type(password_input, self.password)
            self.log("Entered password")
            self.human_delay(1, 2)
            
            # Find and click Sign in button
            signin_selectors = [
                "#passwordNext",
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Sign in')"
            ]
            
            signin_button = None
            for selector in signin_selectors:
                try:
                    signin_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.log(f"Found signin button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if signin_button:
                self.move_to_element_human(signin_button)
                signin_button.click()
                self.log("Clicked Sign in button")
            else:
                # Try pressing Enter
                password_input.send_keys(Keys.RETURN)
                self.log("Pressed Enter on password field")
            
            # Wait for login completion with longer timeout
            self.log("Waiting for login completion...")
            self.human_delay(10, 15)
            
            # Check for successful login
            max_attempts = 5
            for attempt in range(max_attempts):
                current_url = self.driver.current_url
                self.log(f"Attempt {attempt + 1}: Current URL: {current_url}")
                
                if "console.cloud.google.com" in current_url and "signin" not in current_url:
                    self.log("Successfully logged in to Google Cloud Console")
                    self.results["steps_completed"].append("login")
                    return True
                elif "challenge" in current_url or "verification" in current_url:
                    self.log("Encountered verification challenge, waiting...")
                    self.human_delay(10, 15)
                else:
                    self.human_delay(5, 8)
            
            raise Exception(f"Login failed - Final URL: {self.driver.current_url}")
            
        except Exception as e:
            error_msg = f"Stealth login failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def stealth_create_project(self):
        """Create project with stealth techniques"""
        try:
            self.log("Starting stealth project creation...")
            
            # Navigate to project creation page
            self.driver.get("https://console.cloud.google.com/projectcreate")
            self.human_delay(5, 8)
            
            # Generate unique project name
            project_name = f"gmail-oauth-{int(time.time())}"
            
            # Find project name input
            name_selectors = [
                "input[name='projectId']",
                "input[id='projectId']",
                "input[placeholder*='project']",
                "input[aria-label*='Project name']"
            ]
            
            name_input = None
            for selector in name_selectors:
                try:
                    name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.log(f"Found project name input with selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if name_input:
                self.move_to_element_human(name_input)
                name_input.click()
                self.human_delay(0.5, 1)
                self.human_type(name_input, project_name)
                self.log(f"Entered project name: {project_name}")
                self.human_delay(2, 3)
                
                # Find and click Create button
                create_selectors = [
                    "button:contains('Create')",
                    "input[value='Create']",
                    "button[type='submit']"
                ]
                
                create_button = None
                for selector in create_selectors:
                    try:
                        if "contains" in selector:
                            create_button = self.driver.find_element(By.XPATH, f"//button[contains(text(), 'Create')]")
                        else:
                            create_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        self.log(f"Found create button with selector: {selector}")
                        break
                    except:
                        continue
                        
                if create_button:
                    self.move_to_element_human(create_button)
                    create_button.click()
                    self.log("Clicked Create button")
                    
                    # Wait for project creation
                    self.human_delay(15, 20)
                    self.results["steps_completed"].append("project_creation")
                    return True
                else:
                    raise Exception("Could not find Create button")
            else:
                raise Exception("Could not find project name input")
                
        except Exception as e:
            error_msg = f"Stealth project creation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
            
    def run_stealth_automation(self):
        """Run the complete stealth automation"""
        try:
            self.log(f"Starting stealth Gmail OAuth automation for: {self.email}")
            
            # Step 1: Setup stealth driver
            if not self.setup_stealth_driver():
                return False
                
            # Step 2: Stealth login
            if not self.stealth_login_to_google_cloud():
                return False
                
            # Step 3: Create project
            if not self.stealth_create_project():
                return False
                
            # For now, we'll focus on getting past the login and project creation
            # The remaining steps can be added once these work
            
            self.results["success"] = True
            self.log("Stealth automation completed successfully!")
            return True
            
        except Exception as e:
            error_msg = f"Stealth automation failed: {str(e)}"
            self.log(error_msg)
            self.results["errors"].append(error_msg)
            return False
        finally:
            # Save results
            results_filename = f"stealth_automation_results_{self.email.split('@')[0]}_{int(time.time())}.json"
            with open(results_filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            self.log(f"Results saved to: {results_filename}")
            
            # Keep browser open for debugging
            self.log("Browser kept open for debugging. Close manually when done.")

def main():
    # Test credentials
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    automation = StealthGmailOAuthAutomation(email, password)
    success = automation.run_stealth_automation()
    
    if success:
        print(f"\n✅ Stealth automation successful for {email}")
    else:
        print(f"\n❌ Stealth automation failed for {email}")
        print(f"Errors: {automation.results['errors']}")

if __name__ == "__main__":
    main()