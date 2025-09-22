#!/usr/bin/env python3
"""
Simple Google Login Test Script
Tests basic Google authentication with provided credentials
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def test_google_login():
    """Test Google login with provided credentials"""
    
    # Test credentials
    email = "diazdfc41@gmail.com"
    password = "dfgh85621"
    
    print("🧪 Google Login Test")
    print("=" * 50)
    print(f"📧 Testing with email: {email}")
    print()
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    
    try:
        print("🚀 Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Chrome WebDriver initialized successfully")
        
        # Navigate to Google accounts login
        print("🌐 Navigating to Google login page...")
        driver.get("https://accounts.google.com/signin")
        
        # Wait for email field
        print("⏳ Waiting for email field...")
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        print("✅ Email field found")
        
        # Enter email
        print(f"📧 Entering email: {email}")
        email_input.clear()
        email_input.send_keys(email)
        
        # Click Next
        print("➡️ Clicking Next button...")
        next_button = driver.find_element(By.ID, "identifierNext")
        next_button.click()
        print("✅ Email submitted")
        
        # Wait for password field or error
        print("⏳ Waiting for password field...")
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
                    password_input = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    print(f"✅ Password field found with: {selector_type} = {selector_value}")
                    break
                except:
                    continue
            
            if password_input is None:
                print("⏳ Password field not found with common selectors, waiting longer...")
                time.sleep(3)
                password_input = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "password"))
                )
                print("✅ Password field found after waiting")
            
            # Enter password
            print("🔐 Entering password...")
            
            # Wait for element to be fully interactive
            time.sleep(2)
            
            # Try to click first to focus
            try:
                password_input.click()
                time.sleep(1)
            except:
                pass
            
            # Clear and enter password
            try:
                password_input.clear()
            except:
                pass
            
            # Use JavaScript to set value if normal method fails
            try:
                password_input.send_keys(password)
                print("✅ Password entered successfully")
            except Exception as e:
                print(f"⚠️ Normal input failed: {e}")
                print("🔧 Trying JavaScript method...")
                driver.execute_script(f"arguments[0].value = '{password}';", password_input)
                print("✅ Password entered via JavaScript")
            
            # Try multiple selectors for next button
            print("➡️ Looking for password Next button...")
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
                    print(f"✅ Next button found with: {selector_type} = {selector_value}")
                    break
                except:
                    continue
            
            if next_button:
                next_button.click()
                print("✅ Password submitted")
            else:
                print("❌ Password Next button not found")
                return False
            
            # Wait for result
            print("⏳ Waiting for login result...")
            time.sleep(5)
            
            current_url = driver.current_url
            print(f"📍 Current URL: {current_url}")
            
            # Check for different scenarios
            if "myaccount.google.com" in current_url or "accounts.google.com/b/0" in current_url:
                print("🎉 LOGIN SUCCESSFUL! Reached Google account dashboard")
                return True
            elif "challenge" in current_url:
                print("🔐 2FA verification required")
                print("⚠️ Manual verification needed in browser")
                input("Press Enter after completing 2FA verification...")
                
                current_url = driver.current_url
                print(f"📍 After 2FA URL: {current_url}")
                
                if "myaccount.google.com" in current_url or "accounts.google.com/b/0" in current_url:
                    print("🎉 LOGIN SUCCESSFUL after 2FA!")
                    return True
                else:
                    print("❌ Login failed even after 2FA")
                    return False
            elif "signin" in current_url:
                print("❌ LOGIN FAILED - Still on signin page")
                
                # Check for error messages
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab, .Ekjuhf")
                    for error in error_elements:
                        if error.text.strip():
                            print(f"❌ Error: {error.text}")
                except:
                    pass
                    
                return False
            else:
                print(f"⚠️ Unexpected URL: {current_url}")
                return False
                
        except TimeoutException:
            print("❌ Password field not found - checking for errors...")
            
            # Check for email errors
            try:
                error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab, .Ekjuhf")
                for error in error_elements:
                    if error.text.strip():
                        print(f"❌ Email Error: {error.text}")
            except:
                pass
                
            print(f"📍 Current URL: {driver.current_url}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        if driver:
            print(f"📍 Current URL: {driver.current_url}")
        return False
        
    finally:
        if driver:
            print("⏳ Waiting 10 seconds to observe result...")
            time.sleep(10)
            print("🔄 Closing browser...")
            driver.quit()

if __name__ == "__main__":
    success = test_google_login()
    print()
    print("=" * 50)
    if success:
        print("🎉 TEST PASSED: Login credentials are working!")
    else:
        print("💔 TEST FAILED: Login credentials have issues")
    print("🏁 Test finished")