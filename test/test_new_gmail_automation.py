#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail OAuth Automation Test with New Credentials - Improved Version
নতুন Gmail credentials দিয়ে সম্পূর্ণ OAuth automation test (Enhanced)
"""

import sys
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def setup_chrome_driver():
    """Setup Chrome driver with optimal settings"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add user agent to avoid detection
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def safe_click(driver, element):
    """Safely click an element with multiple attempts"""
    for attempt in range(3):
        try:
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # Try regular click
            element.click()
            return True
        except Exception as e:
            print(f"Click attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(2)
            else:
                # Try JavaScript click as last resort
                try:
                    driver.execute_script("arguments[0].click();", element)
                    return True
                except:
                    return False
    return False

def safe_send_keys(driver, element, text):
    """Safely send keys to an element with multiple attempts"""
    for attempt in range(3):
        try:
            # Clear field first
            element.clear()
            time.sleep(0.5)
            
            # Send keys slowly
            for char in text:
                element.send_keys(char)
                time.sleep(0.1)
            
            return True
        except Exception as e:
            print(f"Send keys attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(2)
            else:
                # Try JavaScript input as last resort
                try:
                    driver.execute_script(f"arguments[0].value = '{text}';", element)
                    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
                    return True
                except:
                    return False
    return False

def login_to_google_cloud(driver, email, password):
    """Login to Google Cloud Console with enhanced error handling"""
    print(f"🔐 Logging in with email: {email}")
    
    try:
        # Navigate to Google Cloud Console
        driver.get("https://console.cloud.google.com/")
        time.sleep(5)
        
        # Check if already logged in
        current_url = driver.current_url
        if "console.cloud.google.com" in current_url and "signin" not in current_url:
            print("✅ Already logged in to Google Cloud Console")
            return True
            
        # Wait for email input with multiple selectors
        email_selectors = [
            (By.ID, "identifierId"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.CSS_SELECTOR, "input[autocomplete='username']"),
            (By.XPATH, "//input[@type='email']"),
            (By.NAME, "identifier")
        ]
        
        email_input = None
        for selector_type, selector_value in email_selectors:
            try:
                email_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"✅ Email field found with selector: {selector_type} = {selector_value}")
                break
            except TimeoutException:
                continue
                
        if not email_input:
            print("❌ Could not find email input field")
            return False
            
        # Enter email safely
        if not safe_send_keys(driver, email_input, email):
            print("❌ Failed to enter email")
            return False
        print("✅ Email entered successfully")
        
        # Click Next button
        next_selectors = [
            (By.ID, "identifierNext"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//span[text()='Next']/parent::button"),
            (By.XPATH, "//div[@id='identifierNext']"),
            (By.CSS_SELECTOR, "div[role='button'][data-primary-action-label]")
        ]
        
        next_button = None
        for selector_type, selector_value in next_selectors:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"✅ Next button found with selector: {selector_type} = {selector_value}")
                break
            except TimeoutException:
                continue
                
        if next_button:
            if not safe_click(driver, next_button):
                print("❌ Failed to click Next button")
                return False
            print("✅ Next button clicked")
        else:
            print("❌ Could not find Next button")
            return False
            
        # Wait for password page
        time.sleep(5)
        
        # Wait for password input with multiple selectors and better waiting
        password_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.CSS_SELECTOR, "div[data-form-input-type='password'] input"),
            (By.XPATH, "//input[@type='password']"),
            (By.XPATH, "//div[@id='password']//input"),
            (By.CSS_SELECTOR, "input[autocomplete='current-password']"),
            (By.CSS_SELECTOR, "input[aria-label*='password']"),
            (By.CSS_SELECTOR, "input[placeholder*='password']"),
            (By.XPATH, "//input[contains(@aria-label, 'password') or contains(@placeholder, 'password')]"),
        ]
        
        password_input = None
        for selector_type, selector_value in password_selectors:
            try:
                # Wait longer for password field
                password_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                
                # Check if element is actually interactable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                
                print(f"✅ Password field found with selector: {selector_type} = {selector_value}")
                break
            except TimeoutException:
                print(f"❌ Password field not found with selector: {selector_type} = {selector_value}")
                continue
                
        if not password_input:
            print("❌ Could not find password input field")
            # Take screenshot for debugging
            driver.save_screenshot("password_field_not_found.png")
            print("📸 Screenshot saved as password_field_not_found.png")
            return False
            
        # Wait a bit more to ensure field is ready
        time.sleep(3)
        
        # Enter password safely
        if not safe_send_keys(driver, password_input, password):
            print("❌ Failed to enter password")
            return False
        print("✅ Password entered successfully")
        
        # Click Next button for password
        password_next_selectors = [
            (By.ID, "passwordNext"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[@id='passwordNext']"),
            (By.XPATH, "//div[@id='passwordNext']"),
            (By.XPATH, "//span[text()='Next']/parent::button"),
            (By.CSS_SELECTOR, "div[role='button'][data-primary-action-label]"),
            (By.XPATH, "//div[@role='button' and contains(@data-primary-action-label, 'Next')]"),
        ]
        
        next_button = None
        for selector_type, selector_value in password_next_selectors:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"✅ Password Next button found with selector: {selector_type} = {selector_value}")
                break
            except TimeoutException:
                continue
                
        if next_button:
            if not safe_click(driver, next_button):
                print("❌ Failed to click password Next button")
                return False
            print("✅ Password Next button clicked")
        else:
            print("❌ Could not find password Next button")
            return False
            
        # Wait for login completion with longer timeout
        print("⏳ Waiting for login completion...")
        time.sleep(10)
        
        # Check login result
        current_url = driver.current_url
        print(f"🔍 Current URL after login: {current_url}")
        
        # Check for various success indicators
        if "console.cloud.google.com" in current_url:
            if "challenge" in current_url or "signin" in current_url:
                print("❌ Login failed - Still on authentication page")
                return False
            else:
                print("✅ Login successful - Reached Google Cloud Console")
                return True
        elif "accounts.google.com" in current_url:
            if "challenge" in current_url:
                print("❌ Login failed - Security challenge detected")
                return False
            else:
                print("❌ Login failed - Still on accounts page")
                return False
        else:
            print(f"⚠️ Unexpected URL: {current_url}")
            # Check if we can find Google Cloud Console elements
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='project-switcher-button'], .cfc-project-switcher-button"))
                )
                print("✅ Login successful - Found Google Cloud Console elements")
                return True
            except:
                print("❌ Login failed - No Google Cloud Console elements found")
                return False
            
    except Exception as e:
        print(f"❌ Login failed with error: {str(e)}")
        # Take screenshot for debugging
        try:
            driver.save_screenshot("login_error.png")
            print("📸 Screenshot saved as login_error.png")
        except:
            pass
        return False

def test_complete_gmail_automation():
    """Test complete Gmail OAuth automation with enhanced error handling"""
    print("=" * 70)
    print("🚀 Gmail OAuth Complete Automation Test Started (Enhanced)")
    print("=" * 70)
    
    # Test credentials
    email = "kannanfdjm987@gmail.com"
    password = "6548;lkjhgqw"
    
    print(f"📧 Testing with email: {email}")
    print(f"🔑 Password: {'*' * len(password)}")
    print()
    
    driver = None
    
    try:
        # Setup Chrome driver
        print("🌐 Setting up Chrome browser...")
        driver = setup_chrome_driver()
        print("✅ Chrome browser initialized successfully")
        
        # Test Step 1: Login to Google Cloud Console
        print("\n" + "="*50)
        print("🔐 Step 1: Testing login to Google Cloud Console")
        print("="*50)
        login_result = login_to_google_cloud(driver, email, password)
        
        if not login_result:
            print("❌ Login failed - stopping test")
            print("\n🔍 Keeping browser open for 60 seconds for manual inspection...")
            time.sleep(60)
            return False
        
        print("✅ Login successful! Continuing with remaining tests...")
        
        # Keep browser open for inspection
        print("\n🔍 Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        
        # Final results
        print("\n" + "=" * 70)
        print("📊 TEST RESULTS")
        print("=" * 70)
        print(f"🔐 Login: {'✅ PASSED' if login_result else '❌ FAILED'}")
        print("📁 Project: ⏳ SKIPPED (Login test only)")
        print("📧 Gmail API: ⏳ SKIPPED (Login test only)")
        print("🔑 OAuth Credentials: ⏳ SKIPPED (Login test only)")
        print("💾 JSON Download: ⏳ SKIPPED (Login test only)")
        print("=" * 70)
        
        if login_result:
            print("🎉 LOGIN TEST PASSED! The credentials are working!")
        else:
            print("⚠️ LOGIN TEST FAILED. Please check the credentials.")
            
        print("=" * 70)
        return login_result
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    success = test_complete_gmail_automation()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test completed with errors!")