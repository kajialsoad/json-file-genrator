#!/usr/bin/env python3
"""
Comprehensive Gmail Login Test
Tests the complete login flow with enhanced debugging and security challenge handling
"""

import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def test_comprehensive_login():
    """
    Comprehensive test for Gmail login with enhanced debugging
    """
    
    # Test credentials - using user provided credentials
    test_email = "nilamb010@gmail.com"
    test_password = ",lkjghf9854"
    
    print("🚀 Starting Comprehensive Gmail Login Test")
    print(f"📧 Testing with email: {test_email}")
    print(f"🔑 Password length: {len(test_password)}")
    print("="*60)
    
    driver = None
    try:
        # Setup Chrome with incognito mode
        print("🔧 Setting up Chrome browser...")
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Browser started successfully")
        
        # Navigate to Google login
        print("🌐 Navigating to Google login...")
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        
        # Check if already logged in and force logout
        print("🔍 Checking for existing login...")
        try:
            logout_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'logout') or contains(@href, 'signout')]")
            if logout_elements:
                print("⚠️ Found existing login, forcing logout...")
                driver.get("https://accounts.google.com/logout")
                time.sleep(3)
                driver.get("https://accounts.google.com/signin")
                time.sleep(3)
        except:
            pass
            
        # Enter email with enhanced debugging
        print("📧 Entering email...")
        try:
            # Wait for email input field
            email_input = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "identifierId"))
            )
            
            # Clear and enter email
            email_input.clear()
            time.sleep(1)
            email_input.send_keys(test_email)
            
            # Verify email was entered
            entered_email = email_input.get_attribute("value")
            print(f"✅ Email entered: {entered_email}")
            
            if entered_email != test_email:
                print(f"⚠️ Email mismatch! Expected: {test_email}, Got: {entered_email}")
            
            # Click Next
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "identifierNext"))
            )
            next_button.click()
            print("✅ Email Next button clicked")
            
            # Wait for password page to load completely
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ Failed to enter email: {e}")
            print(f"📍 Current URL: {driver.current_url}")
            print(f"📄 Page title: {driver.title}")
            return False
        
        # Enhanced password field detection and filling
        print("🔑 Looking for password field...")
        password_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH, "//input[@type='password']"),
            (By.CSS_SELECTOR, "input[name='Passwd']"),
            (By.NAME, "Passwd")
        ]
        
        password_input = None
        for attempt in range(5):
            print(f"🔍 Password detection attempt {attempt + 1}/5")
            
            # Check for error messages first
            try:
                error_elements = driver.find_elements(By.CSS_SELECTOR, "[jsname='B34EJ'] span, .LXRPh, [data-error='true']")
                if error_elements:
                    for error in error_elements:
                        if error.text.strip():
                            print(f"⚠️ Error message detected: {error.text}")
            except:
                pass
            
            # Try each selector with clickable wait
            for selector_type, selector_value in password_selectors:
                try:
                    password_input = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    print(f"✅ Password field found and clickable with {selector_type}: {selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if password_input:
                break
            
            print(f"⏳ Waiting before retry... (attempt {attempt + 1})")
            time.sleep(3)
        
        if not password_input:
            print("❌ Password field not found after all attempts")
            print(f"📍 Current URL: {driver.current_url}")
            print(f"📄 Page title: {driver.title}")
            
            # Check if we're on a different page
            if "challenge" in driver.current_url:
                print("🔐 Detected security challenge page")
            elif "signin" not in driver.current_url:
                print("🔄 Redirected to unexpected page")
            
            return False
        
        # Enhanced password filling with multiple methods and better error handling
        print("🔑 Filling password...")
        password_filled = False
        
        # Method 1: Standard Selenium approach
        try:
            print("🔧 Method 1: Standard Selenium input...")
            
            # Ensure field is focused and ready
            password_input.click()
            time.sleep(1)
            
            # Clear any existing content
            password_input.clear()
            time.sleep(0.5)
            
            # Send password
            password_input.send_keys(test_password)
            time.sleep(1)
            
            # Verify
            password_value = password_input.get_attribute("value")
            if len(password_value) == len(test_password):
                print(f"✅ Method 1 successful - Password length: {len(password_value)}")
                password_filled = True
            else:
                print(f"⚠️ Method 1 partial - Expected: {len(test_password)}, Got: {len(password_value)}")
                
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
        
        # Method 2: JavaScript approach if Method 1 failed
        if not password_filled:
            try:
                print("🔧 Method 2: JavaScript input...")
                
                # Focus the element first
                driver.execute_script("arguments[0].focus();", password_input)
                time.sleep(0.5)
                
                # Clear and set value
                driver.execute_script("arguments[0].value = '';", password_input)
                time.sleep(0.5)
                driver.execute_script("arguments[0].value = arguments[1];", password_input, test_password)
                
                # Trigger events
                driver.execute_script("""
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """, password_input)
                
                time.sleep(1)
                
                # Verify
                password_value = password_input.get_attribute("value")
                if len(password_value) == len(test_password):
                    print(f"✅ Method 2 successful - Password length: {len(password_value)}")
                    password_filled = True
                else:
                    print(f"⚠️ Method 2 partial - Expected: {len(test_password)}, Got: {len(password_value)}")
                    
            except Exception as e:
                print(f"❌ Method 2 failed: {e}")
        
        # Method 3: Character-by-character input if previous methods failed
        if not password_filled:
            try:
                print("🔧 Method 3: Character-by-character input...")
                
                password_input.click()
                time.sleep(0.5)
                password_input.clear()
                time.sleep(0.5)
                
                # Send each character individually
                for char in test_password:
                    password_input.send_keys(char)
                    time.sleep(0.1)
                
                time.sleep(1)
                
                # Verify
                password_value = password_input.get_attribute("value")
                if len(password_value) == len(test_password):
                    print(f"✅ Method 3 successful - Password length: {len(password_value)}")
                    password_filled = True
                else:
                    print(f"⚠️ Method 3 partial - Expected: {len(test_password)}, Got: {len(password_value)}")
                    
            except Exception as e:
                print(f"❌ Method 3 failed: {e}")
        
        if not password_filled:
            print("❌ All password filling methods failed")
            return False
        
        # Enhanced Next button handling
        print("🔍 Looking for Next button...")
        next_selectors = [
            (By.ID, "passwordNext"),
            (By.CSS_SELECTOR, "#passwordNext"),
            (By.XPATH, "//div[@id='passwordNext']"),
            (By.CSS_SELECTOR, "[data-primary='true']"),
            (By.XPATH, "//span[contains(text(), 'Next')]/parent::button")
        ]
        
        next_button = None
        for selector_type, selector_value in next_selectors:
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"✅ Next button found with {selector_type}: {selector_value}")
                break
            except TimeoutException:
                continue
        
        if next_button:
            try:
                next_button.click()
                print("✅ Next button clicked successfully")
            except Exception as e:
                print(f"⚠️ Click failed, trying JavaScript: {e}")
                driver.execute_script("arguments[0].click();", next_button)
                print("✅ Next button clicked via JavaScript")
        else:
            print("❌ Next button not found")
            return False
        
        # Enhanced login result checking
        print("⏳ Waiting for login result...")
        time.sleep(8)
        
        current_url = driver.current_url
        print(f"📍 After login URL: {current_url}")
        
        # Detailed URL analysis
        if "challenge/pwd" in current_url:
            print("❌ LOGIN FAILED: Password challenge detected - incorrect password")
            print("💡 Possible reasons:")
            print("   - Password is incorrect")
            print("   - Account has been locked due to multiple failed attempts")
            print("   - Account requires additional verification")
            return False
        elif "challenge" in current_url:
            print("🔐 SECURITY CHALLENGE: Additional verification required")
            print("💡 This could be:")
            print("   - 2-factor authentication (2FA)")
            print("   - Phone verification")
            print("   - Captcha challenge")
            print("   - Suspicious activity detection")
            return False
        elif "signin" in current_url:
            print("❌ LOGIN FAILED: Still on signin page")
            return False
        elif "console.cloud.google.com" in current_url or "myaccount.google.com" in current_url:
            print("✅ LOGIN SUCCESS: Redirected to Google services")
            return True
        else:
            print(f"🤔 UNKNOWN STATE: Unexpected URL pattern: {current_url}")
            
            # Check page content for clues
            page_title = driver.title
            print(f"📄 Page title: {page_title}")
            
            if "Google" in page_title and "Sign" not in page_title:
                print("✅ LOGIN SUCCESS: Likely logged in based on page title")
                return True
            else:
                print("❌ LOGIN FAILED: Unable to determine success")
                return False
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        print("📋 Full traceback:")
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("🔄 Keeping browser open for 30 seconds for manual inspection...")
            time.sleep(30)
            driver.quit()
            print("🔄 Browser closed")

if __name__ == "__main__":
    print("🧪 Gmail Login Comprehensive Test")
    print("=" * 60)
    
    success = test_comprehensive_login()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 COMPREHENSIVE LOGIN TEST PASSED")
    else:
        print("💥 COMPREHENSIVE LOGIN TEST FAILED")
    print("👋 Test completed")