#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Credentials Test
Test the automation with the exact credentials provided by the user
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def test_direct_credentials():
    """
    Test password filling with the exact credentials provided by user:
    Email: nilamb010@gmail.com
    Password: ,lkjghf9854
    """
    
    # Test credentials - using user provided credentials
    test_email = "nilamb010@gmail.com"
    test_password = ",lkjghf9854"
    
    print(f"🧪 Testing with credentials: {test_email}")
    print(f"🔐 Password length: {len(test_password)}")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("🚀 Starting Chrome browser...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Force logout and clear data
        print("🧹 Clearing browser data...")
        driver.get("https://accounts.google.com/logout")
        time.sleep(2)
        
        # Clear cookies and storage
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        print("✅ Browser data cleared")
        
        # Navigate to Google Cloud Console
        print("🌐 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        time.sleep(3)
        
        # Check if we're redirected to login
        current_url = driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        if "accounts.google.com" not in current_url:
            print("❌ Not redirected to login page")
            return False
            
        # Enter email (using correct selector from main.py)
        print("📧 Entering email...")
        try:
            email_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.clear()
            email_input.send_keys(test_email)
            print(f"✅ Email entered: {test_email}")
            
            # Click Next
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            print("✅ Email Next button clicked")
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Failed to enter email: {e}")
            return False
        
        # Wait for password field and enter password
        print("🔐 Waiting for password field...")
        try:
            # Multiple selectors for password field (from main.py)
            selectors = [
                ("NAME", "password"),
                ("ID", "password"),
                ("CSS_SELECTOR", "input[type='password']"),
                ("XPATH", "//input[@type='password']"),
                ("XPATH", "//input[@name='password']"),
                ("XPATH", "//input[@id='password']"),
                ("CSS_SELECTOR", "input[name='password']"),
                ("CSS_SELECTOR", "input[id='password']"),
                ("XPATH", "//input[contains(@class, 'password')]"),
                ("CSS_SELECTOR", "input[aria-label*='password' i]"),
                ("CSS_SELECTOR", "input[placeholder*='password' i]")
            ]
            
            password_input = None
            for attempt in range(3):  # Try 3 times
                print(f"🔄 Password field detection attempt {attempt + 1}/3")
                
                for selector_type, selector_value in selectors:
                    try:
                        print(f"🔍 Trying selector: {selector_type} = {selector_value}")
                        if selector_type == "NAME":
                            password_input = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.NAME, selector_value))
                            )
                        elif selector_type == "ID":
                            password_input = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.ID, selector_value))
                            )
                        elif selector_type == "CSS_SELECTOR":
                            password_input = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector_value))
                            )
                        elif selector_type == "XPATH":
                            password_input = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, selector_value))
                            )
                        
                        if password_input:
                            print(f"✅ Password field found with: {selector_type} = {selector_value}")
                            break
                            
                    except Exception as e:
                        print(f"⚠️ Selector {selector_type}={selector_value} failed: {e}")
                        continue
                
                if password_input:
                    break
                    
                print(f"⏳ Waiting 3 seconds before retry {attempt + 1}...")
                time.sleep(3)
            
            if not password_input:
                print("❌ Password field not found with any selector")
                print(f"📍 Current URL: {driver.current_url}")
                return False
            
            # Enter password using main.py approach
            print("🔐 Entering password...")
            print(f"🔍 Password field element: {password_input}")
            print(f"🔍 Password field tag: {password_input.tag_name}")
            print(f"🔍 Password field enabled: {password_input.is_enabled()}")
            print(f"🔍 Password field displayed: {password_input.is_displayed()}")
            
            # Wait for element to be fully interactive
            print("⏳ Waiting 2 seconds for element to be interactive...")
            time.sleep(2)
            
            # Try to click first to focus
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
            
            # Try normal input first, then JavaScript
            try:
                password_input.send_keys(test_password)
                print("✅ Password entered successfully (normal method)")
            except Exception as e:
                print(f"⚠️ Normal input failed: {e}")
                print("🔧 Trying JavaScript method...")
                try:
                    driver.execute_script(f"arguments[0].value = '{test_password}';", password_input)
                    # Trigger events
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
            
            # Verify password was entered
            try:
                entered_value = password_input.get_attribute("value")
                print(f"🔍 Password field value length: {len(entered_value) if entered_value else 0}")
            except Exception as e:
                print(f"⚠️ Could not verify password entry: {e}")
            
        except Exception as e:
            print(f"❌ Password field handling failed: {e}")
            return False
        
        # Click Next button
        print("🔍 Looking for Next button...")
        try:
            # Multiple selectors for Next button
            next_selectors = [
                ("ID", "passwordNext"),
                ("XPATH", "//button[@id='passwordNext']"),
                ("XPATH", "//span[contains(text(), 'Next')]/parent::button"),
                ("CSS_SELECTOR", "button[id='passwordNext']"),
                ("XPATH", "//div[@id='passwordNext']"),
                ("CSS_SELECTOR", "div[id='passwordNext']"),
                ("XPATH", "//input[@id='passwordNext']"),
                ("CSS_SELECTOR", "input[id='passwordNext']")
            ]
            
            next_button = None
            for selector_type, selector_value in next_selectors:
                try:
                    if selector_type == "ID":
                        next_button = driver.find_element(By.ID, selector_value)
                    elif selector_type == "XPATH":
                        next_button = driver.find_element(By.XPATH, selector_value)
                    elif selector_type == "CSS_SELECTOR":
                        next_button = driver.find_element(By.CSS_SELECTOR, selector_value)
                    
                    if next_button and next_button.is_displayed():
                        print(f"✅ Next button found with selector: {selector_type} = {selector_value}")
                        break
                except:
                    continue
            
            if next_button:
                next_button.click()
                print("✅ Next button clicked successfully")
            else:
                print("❌ Next button not found")
                return False
                
        except Exception as e:
            print(f"❌ Failed to click Next button: {e}")
            return False
        
        # Wait for login result
        print("⏳ Waiting for login result...")
        time.sleep(5)
        
        # Check current URL after login attempt
        current_url = driver.current_url
        print(f"📍 After login URL: {current_url}")
        
        # Check for different scenarios
        if "challenge/pwd" in current_url:
            print("❌ LOGIN FAILED: Password challenge detected - incorrect password")
            return False
        elif "console.cloud.google.com" in current_url:
            print("✅ LOGIN SUCCESS: Redirected to Google Cloud Console")
            return True
        elif "myaccount.google.com" in current_url:
            print("✅ LOGIN SUCCESS: Redirected to Google Account")
            return True
        elif "accounts.google.com" in current_url and "signin" not in current_url:
            print("✅ LOGIN SUCCESS: Google Accounts page (logged in)")
            return True
        else:
            print(f"⚠️ UNKNOWN STATE: Unexpected URL: {current_url}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        return False
        
    finally:
        if driver:
            print("🔄 Keeping browser open for 30 seconds for manual inspection...")
            time.sleep(30)
            driver.quit()
            print("🔄 Browser closed")

def main():
    print("🔧 Direct Credentials Test")
    print("=" * 60)
    print("Testing with user provided credentials:")
    print("Email: nilamb010@gmail.com")
    print("Password: ,lkjghf9854")
    print("=" * 60)
    
    success = test_direct_credentials()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ DIRECT CREDENTIALS TEST PASSED")
    else:
        print("💥 DIRECT CREDENTIALS TEST FAILED")
    
    print("👋 Test completed")

if __name__ == "__main__":
    main()