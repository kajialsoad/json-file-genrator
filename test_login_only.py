#!/usr/bin/env python3
"""
Test only the login functionality
"""

import sys
import os
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def test_login_only():
    """
    Test only the login step with detailed logging
    """
    print("🧪 Testing Login Only")
    print("=" * 50)
    
    # User provided credentials
    test_email = "diazdfc41@gmail.com"
    test_password = "dfgh85621"
    
    print(f"📧 Email: {test_email}")
    print(f"🔐 Password: {'*' * len(test_password)}")
    
    driver = None
    try:
        # Chrome options setup
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        # chrome_options.add_argument('--headless')  # Uncomment for headless mode
        
        print("\n🚀 Initializing Chrome WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        print("✅ Chrome WebDriver initialized successfully")
        
        # Navigate to Google Cloud Console
        print("\n🌐 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        
        # Wait for login page or dashboard
        print("⏳ Waiting for page to load...")
        WebDriverWait(driver, 30).until(
            lambda d: "accounts.google.com" in d.current_url or "console.cloud.google.com" in d.current_url
        )
        
        current_url = driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        # If redirected to login page
        if "accounts.google.com" in current_url:
            print("\n🔐 Login page detected, entering credentials...")
            
            # Enter email
            print(f"📧 Entering email: {test_email}")
            try:
                email_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "identifierId"))
                )
                email_input.clear()
                email_input.send_keys(test_email)
                
                # Click Next
                next_button = driver.find_element(By.ID, "identifierNext")
                next_button.click()
                print("✅ Email entered successfully")
            except Exception as e:
                print(f"❌ Failed to enter email: {str(e)}")
                return False
            
            # Wait for password field
            print("\n🔐 Waiting for password field...")
            try:
                # Try multiple selectors for password field
                password_input = None
                selectors = [
                    (By.NAME, "password"),
                    (By.ID, "password"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.CSS_SELECTOR, "input[name='Passwd']"),
                    (By.CSS_SELECTOR, "#password input"),
                    (By.XPATH, "//input[@type='password']"),
                    (By.XPATH, "//input[@name='password']"),
                    (By.XPATH, "//input[@name='Passwd']")
                ]
                
                for selector_type, selector_value in selectors:
                    try:
                        print(f"🔍 Trying selector: {selector_type} = {selector_value}")
                        password_input = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((selector_type, selector_value))
                        )
                        print(f"✅ Password field found with selector: {selector_type} = {selector_value}")
                        break
                    except Exception as sel_e:
                        print(f"❌ Selector failed: {selector_type} = {selector_value}, Error: {sel_e}")
                        continue
                
                if password_input is None:
                    print("❌ Password field not found with any selector")
                    return False
                
                # Enter password
                print("\n🔐 Entering password...")
                print(f"🔍 Password field element: {password_input}")
                print(f"🔍 Password field tag: {password_input.tag_name}")
                print(f"🔍 Password field enabled: {password_input.is_enabled()}")
                print(f"🔍 Password field displayed: {password_input.is_displayed()}")
                
                # Wait for element to be fully interactive
                print("⏳ Waiting 2 seconds for element to be interactive...")
                time.sleep(2)
                
                # Try to click first to focus
                print("🖱️ Attempting to click password field for focus...")
                try:
                    password_input.click()
                    print("✅ Password field clicked for focus")
                    time.sleep(1)
                except Exception as e:
                    print(f"⚠️ Failed to click password field: {e}")
                
                # Clear and enter password
                try:
                    password_input.clear()
                    print("✅ Password field cleared")
                except Exception as e:
                    print(f"⚠️ Failed to clear password field: {e}")
                
                # Enter password
                try:
                    password_input.send_keys(test_password)
                    print("✅ Password entered successfully (normal method)")
                except Exception as e:
                    print(f"⚠️ Normal input failed: {e}")
                    print("🔧 Trying JavaScript method...")
                    try:
                        driver.execute_script(f"arguments[0].value = '{test_password}';", password_input)
                        print("✅ Password entered via JavaScript")
                    except Exception as js_e:
                        print(f"❌ Failed to enter password: {js_e}")
                        return False
                
                # Find and click Next button
                print("\n🔍 Looking for Next button...")
                next_button = None
                next_selectors = [
                    (By.ID, "passwordNext"),
                    (By.CSS_SELECTOR, "#passwordNext"),
                    (By.XPATH, "//button[@id='passwordNext']"),
                    (By.XPATH, "//span[contains(text(), 'Next')]/parent::button"),
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.XPATH, "//div[@id='passwordNext']")
                ]
                
                for selector_type, selector_value in next_selectors:
                    try:
                        next_button = driver.find_element(selector_type, selector_value)
                        print(f"✅ Next button found with selector: {selector_type} = {selector_value}")
                        break
                    except Exception as e:
                        print(f"❌ Next button selector failed: {selector_type} = {selector_value}")
                        continue
                
                if next_button:
                    try:
                        next_button.click()
                        print("✅ Next button clicked successfully")
                    except Exception as e:
                        print(f"❌ Failed to click Next button: {e}")
                        return False
                else:
                    print("❌ Password Next button not found with any selector")
                    return False
                
                # Wait for result
                print("\n⏳ Waiting for login result...")
                time.sleep(5)  # Give more time for page to process
                
                # Check current URL after login attempt
                current_url = driver.current_url
                print(f"📍 After login URL: {current_url}")
                
                # Check for different scenarios
                if "console.cloud.google.com" in current_url:
                    print("✅ LOGIN SUCCESS - reached Google Cloud Console")
                    return True
                elif "challenge" in current_url or "signin/v2/challenge" in current_url:
                    print("🔐 2FA verification required")
                    print("⚠️ Please complete 2FA manually in the browser")
                    
                    # Wait for user to complete 2FA manually
                    print("⏳ Waiting up to 5 minutes for 2FA completion...")
                    try:
                        WebDriverWait(driver, 300).until(  # 5 minutes timeout
                            lambda d: "console.cloud.google.com" in d.current_url
                        )
                        print("✅ 2FA verification completed - LOGIN SUCCESS")
                        return True
                    except TimeoutException:
                        print("❌ 2FA verification timeout")
                        return False
                elif "signin" in current_url:
                    print("❌ LOGIN FAILED - still on signin page")
                    
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
                    print(f"⚠️ Unexpected URL after login: {current_url}")
                    return False
                
            except Exception as e:
                print(f"❌ Failed to enter password: {str(e)}")
                return False
        else:
            print("✅ Already logged in - reached Google Cloud Console directly")
            return True
        
    except Exception as e:
        print(f"❌ Login test error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            print("\n🔄 Keeping browser open for 30 seconds for manual inspection...")
            time.sleep(30)
            driver.quit()
            print("🔄 Browser closed")

def main():
    print("🔧 Gmail OAuth Generator - Login Test Only")
    print("=" * 60)
    
    success = test_login_only()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 LOGIN TEST PASSED: Credentials work correctly!")
    else:
        print("💥 LOGIN TEST FAILED: Issues with credentials or login process")
    
    print("\n👋 Test completed")

if __name__ == "__main__":
    main()