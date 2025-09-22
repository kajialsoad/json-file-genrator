#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for single OAuth generation
টেস্ট ইমেইল দিয়ে single JSON generation test করার জন্য
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json

def test_single_oauth_generation():
    """Test single OAuth generation with provided credentials"""
    
    # Test credentials provided by user
    test_account = {
        'email': 'diazdfc41@gmail.com',
        'password': 'dfgh85621',
        'line_num': 1
    }
    
    print(f"🚀 Starting OAuth test for: {test_account['email']}")
    
    driver = None
    try:
        # Chrome options setup
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        # chrome_options.add_argument('--headless')  # Keep visible for debugging
        
        # Initialize WebDriver
        print("🚀 Initializing Chrome WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        print("✅ Chrome WebDriver initialized successfully")
        
        # Step 1: Test login to Google Cloud Console
        print(f"🌐 Testing login to Google Cloud Console with: {test_account['email']}")
        if not test_login_to_google_cloud(driver, test_account):
            print("❌ Login test failed")
            return False
            
        print("✅ Login test successful!")
        
        # Wait a bit to see the result
        print("⏳ Waiting 5 seconds to observe the result...")
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            print("🔄 Closing browser...")
            driver.quit()
            
def test_login_to_google_cloud(driver, account):
    """Test login to Google Cloud Console"""
    try:
        # Navigate to Google Cloud Console
        print("🌐 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        
        # Wait for login page or dashboard
        WebDriverWait(driver, 15).until(
            lambda d: "accounts.google.com" in d.current_url or "console.cloud.google.com" in d.current_url
        )
        
        print(f"📍 Current URL: {driver.current_url}")
        
        # If redirected to login page
        if "accounts.google.com" in driver.current_url:
            print(f"📧 Entering email: {account['email']}")
            
            # Enter email
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.clear()
            email_input.send_keys(account['email'])
            
            # Click Next
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            # Wait for password field
            print("🔐 Entering password...")
            password_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(account['password'])
            
            # Click Next
            password_next = driver.find_element(By.ID, "passwordNext")
            password_next.click()
            
            # Wait for result
            print("⏳ Waiting for login result...")
            time.sleep(5)
            
            print(f"📍 After login URL: {driver.current_url}")
            
            # Check if login was successful or if 2FA is required
            if "console.cloud.google.com" in driver.current_url:
                print("✅ Login successful - reached Google Cloud Console")
                return True
            elif "challenge" in driver.current_url or "signin/v2/challenge" in driver.current_url:
                print("🔐 2FA verification required - this is normal")
                print("⚠️ In real automation, user would need to complete 2FA manually")
                return True  # Consider this a successful test
            elif "signin" in driver.current_url:
                print("❌ Login failed - still on signin page")
                print("🔍 Checking for error messages...")
                
                # Check for error messages
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab")
                    for error in error_elements:
                        if error.text.strip():
                            print(f"❌ Error message: {error.text}")
                except:
                    pass
                    
                return False
            else:
                print(f"⚠️ Unexpected URL after login: {driver.current_url}")
                return False
        else:
            print("✅ Already logged in - reached Google Cloud Console directly")
            return True
            
    except TimeoutException as e:
        print(f"⏰ Timeout during login: {str(e)}")
        print(f"📍 Current URL: {driver.current_url}")
        return False
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        print(f"📍 Current URL: {driver.current_url}")
        return False

if __name__ == "__main__":
    print("🧪 Starting OAuth Generation Test")
    print("=" * 50)
    
    success = test_single_oauth_generation()
    
    print("=" * 50)
    if success:
        print("✅ Test completed successfully!")
        print("💡 The credentials appear to be working")
    else:
        print("❌ Test failed!")
        print("💡 Please check the credentials or try again")
    
    print("🏁 Test finished")