#!/usr/bin/env python3
"""
Force logout and test password filling with new credentials
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

def test_password_filling_force():
    """
    Force logout and test password filling with new credentials
    """
    print("🧪 Force Logout and Test Password Filling")
    print("=" * 60)
    
    # New credentials provided by user
    test_email = "nilamb010@gmail.com"
    test_password = ",lkjghf9854"
    
    print(f"📧 Testing with email: {test_email}")
    print(f"🔐 Testing with password: {'*' * len(test_password)}")
    
    driver = None
    try:
        # Setup Chrome driver with fresh profile
        print("🚀 Setting up Chrome WebDriver with fresh profile...")
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--user-data-dir=C:\\temp\\chrome_test_profile')
        chrome_options.add_argument('--profile-directory=Default')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        print("✅ Chrome WebDriver initialized")
        
        # First, force logout by going to logout URL
        print("🚪 Forcing logout...")
        driver.get("https://accounts.google.com/logout")
        time.sleep(3)
        
        # Clear all cookies and local storage
        print("🧹 Clearing cookies and storage...")
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        
        # Navigate to Google Cloud Console
        print("🌐 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        
        # Wait for login page
        print("⏳ Waiting for login page...")
        WebDriverWait(driver, 30).until(
            lambda d: "accounts.google.com" in d.current_url
        )
        
        current_url = driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        # Enter email
        print("📧 Entering email address...")
        try:
            # Wait for email field
            email_field = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "identifierId"))
            )
            email_field.clear()
            email_field.send_keys(test_email)
            
            # Click Next
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            print("✅ Email entered successfully")
        except Exception as e:
            print(f"❌ Failed to enter email: {str(e)}")
            return False
        
        # Wait for password field with multiple selectors (like main.py)
        print("🔐 Waiting for password field...")
        password_input = None
        
        # Check for error messages first
        try:
            error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab, .Ekjuhf")
            for error in error_elements:
                if error.text.strip():
                    print(f"❌ Error message detected: {error.text}")
                    return False
        except:
            pass
        
        # Use the same selectors as main.py
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
            # Wait longer and try again
            print("⏳ Password field not found, waiting longer...")
            time.sleep(3)
            try:
                password_input = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "password"))
                )
                print("✅ Password field found after waiting")
            except TimeoutException:
                print("❌ Password field not found even after extended wait")
                print(f"📍 Current URL: {driver.current_url}")
                
                # Check for error messages again
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab, .Ekjuhf")
                    for error in error_elements:
                        if error.text.strip():
                            print(f"❌ Error message: {error.text}")
                except:
                    pass
                return False
        
        # Test password filling using main.py approach
        print("\n🔐 Entering password using main.py approach...")
        
        print(f"🔍 Password field element: {password_input}")
        print(f"🔍 Password field tag: {password_input.tag_name}")
        print(f"🔍 Password field enabled: {password_input.is_enabled()}")
        print(f"🔍 Password field displayed: {password_input.is_displayed()}")
        
        try:
            print("🚀 Starting password entry process...")
            # Wait for element to be fully interactive
            print("⏳ Waiting 2 seconds for element to be interactive...")
            time.sleep(2)
            print("✅ Wait completed, proceeding with password entry")
            
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
           
            # Use JavaScript to set value if normal method fails
            try:
                password_input.send_keys(test_password)
                print("✅ Password entered successfully (normal method)")
            except Exception as e:
                print(f"⚠️ Normal input failed: {e}")
                print("🔧 Trying JavaScript method...")
                try:
                    driver.execute_script(f"arguments[0].value = '{test_password}';", password_input)
                    # Trigger events to notify the page
                    driver.execute_script("""
                        var element = arguments[0];
                        var event = new Event('input', { bubbles: true });
                        element.dispatchEvent(event);
                        var changeEvent = new Event('change', { bubbles: true });
                        element.dispatchEvent(changeEvent);
                    """, password_input)
                    print("✅ Password entered via JavaScript")
                except Exception as js_e:
                    print(f"❌ Failed to enter password: {js_e}")
                    return False
                    
        except Exception as password_error:
            print(f"❌ Password entry process failed: {str(password_error)}")
            print(f"📍 Current URL: {driver.current_url}")
            return False
        
        # Try to find and click Next button
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
            except Exception:
                continue
        
        if next_button:
            try:
                # Ensure the button is clickable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(next_button)
                )
                next_button.click()
                print("✅ Next button clicked successfully")
            except Exception as e:
                print(f"❌ Failed to click Next button: {e}")
                # Try JavaScript click as fallback
                try:
                    driver.execute_script("arguments[0].click();", next_button)
                    print("✅ Next button clicked via JavaScript")
                except Exception as js_e:
                    print(f"❌ JavaScript click also failed: {js_e}")
                    return False
        else:
            print("❌ Next button not found")
            return False
        
        # Wait for login result
        print("\n⏳ Waiting for login result...")
        time.sleep(8)  # Give more time for processing
        
        current_url = driver.current_url
        print(f"📍 After login URL: {current_url}")
        
        # Check login result with correct order
        result = False
        if "challenge/pwd" in current_url:
            print("❌ LOGIN FAILED: Password challenge detected - incorrect password")
            result = False
        elif "console.cloud.google.com" in current_url:
            print("✅ LOGIN SUCCESS: Reached Google Cloud Console")
            result = True
        elif "challenge" in current_url:
            print("🔐 2FA REQUIRED: Two-factor authentication needed")
            result = True  # Consider 2FA as successful login
        elif "signin" in current_url:
            print("❌ LOGIN FAILED: Still on signin page")
            result = False
        elif "accounts.google.com" in current_url:
            print("⚠️ STILL ON LOGIN PAGE: Login may have failed or requires additional steps")
            result = False
        else:
            print(f"⚠️ UNKNOWN STATE: Unexpected URL - {current_url}")
            result = False
        
        # Keep browser open for inspection
        print("\n🔄 Keeping browser open for 30 seconds for manual inspection...")
        time.sleep(30)
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()
            print("🔄 Browser closed")

def main():
    print("🔧 Gmail OAuth Generator - Force Password Filling Test")
    print("=" * 60)
    
    success = test_password_filling_force()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 PASSWORD FILLING TEST PASSED: Credentials work correctly!")
    else:
        print("💥 PASSWORD FILLING TEST FAILED: Issues with password filling or credentials")
    
    print("\n👋 Test completed")

if __name__ == "__main__":
    main()