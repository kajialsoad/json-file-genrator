#!/usr/bin/env python3
"""
Final test of the Gmail OAuth Generator automation with improved password filling.
This test uses the user's provided credentials to verify the automation works correctly.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def test_gmail_oauth_automation():
    """Test the complete Gmail OAuth automation process"""
    
    # Test credentials - using user provided credentials
    test_email = "nilamb010@gmail.com"
    test_password = ",lkjghf9854"
    
    print("🚀 Starting Gmail OAuth Generator automation test...")
    print(f"📧 Testing with email: {test_email}")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    
    try:
        # Initialize driver
        print("🌐 Initializing Chrome browser...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navigate to Google Cloud Console
        print("🔗 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        time.sleep(3)
        
        # Check if login is required
        current_url = driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        if "accounts.google.com" in current_url:
            print("🔐 Login page detected, proceeding with authentication...")
            
            # Step 1: Enter email
            print("📧 Step 1: Entering email...")
            try:
                email_input = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "identifierId"))
                )
                email_input.clear()
                email_input.send_keys(test_email)
                
                # Click Next
                next_button = driver.find_element(By.ID, "identifierNext")
                next_button.click()
                print("✅ Email entered and Next clicked")
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ Failed to enter email: {e}")
                return False
            
            # Step 2: Enter password with improved methods
            print("🔐 Step 2: Entering password with improved methods...")
            try:
                # Wait for password field
                password_input = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.NAME, "password"))
                )
                print("✅ Password field found")
                
                # Enhanced password filling with multiple methods
                password_filled = False
                
                # Method 1: Standard Selenium approach
                try:
                    print("🔧 Method 1: Standard Selenium input...")
                    password_input.click()
                    time.sleep(1)
                    password_input.clear()
                    time.sleep(0.5)
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
                
                # Method 2: JavaScript approach (proven to work)
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
                
                # Method 3: Character-by-character input as final fallback
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
                
                print(f"🔍 Final password field value length: {len(password_input.get_attribute('value'))}")
                
                # Step 3: Click Next button
                print("🔍 Step 3: Looking for Next button...")
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
                    next_button.click()
                    print("✅ Next button clicked successfully")
                    time.sleep(5)
                else:
                    print("❌ Next button not found")
                    return False
                
            except Exception as e:
                print(f"❌ Failed to enter password: {e}")
                return False
            
            # Step 4: Check login result
            print("⏳ Step 4: Checking login result...")
            current_url = driver.current_url
            print(f"📍 After login URL: {current_url}")
            
            # Analyze the result
            if "challenge/pwd" in current_url:
                print("❌ LOGIN FAILED: Password challenge detected - incorrect password")
                print("💡 Possible reasons:")
                print("   - Password is incorrect")
                print("   - Account has been locked due to multiple failed attempts")
                print("   - Account requires additional verification")
                return False
            elif "console.cloud.google.com" in current_url:
                print("✅ LOGIN SUCCESSFUL: Reached Google Cloud Console")
                return True
            elif "challenge" in current_url or "signin/v2/challenge" in current_url:
                print("🔐 2FA VERIFICATION REQUIRED")
                print("💡 The account requires two-factor authentication")
                print("🔄 This is normal for secure accounts")
                return True  # Consider this a success as the password was accepted
            elif "signin" in current_url:
                print("❌ LOGIN FAILED: Still on signin page")
                return False
            else:
                print(f"⚠️ UNEXPECTED RESULT: {current_url}")
                # Try to navigate to Cloud Console
                try:
                    driver.get("https://console.cloud.google.com/")
                    time.sleep(3)
                    if "console.cloud.google.com" in driver.current_url:
                        print("✅ Successfully navigated to Google Cloud Console")
                        return True
                    else:
                        print(f"❌ Failed to reach Cloud Console: {driver.current_url}")
                        return False
                except Exception as nav_e:
                    print(f"❌ Navigation error: {nav_e}")
                    return False
        else:
            print("✅ Already logged in - reached Google Cloud Console directly")
            return True
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        return False
        
    finally:
        if driver:
            print("🔄 Keeping browser open for 30 seconds for inspection...")
            time.sleep(30)
            print("🔄 Browser closed")
            driver.quit()

if __name__ == "__main__":
    print("============================================================")
    print("🧪 FINAL AUTOMATION TEST WITH IMPROVED PASSWORD FILLING")
    print("============================================================")
    
    success = test_gmail_oauth_automation()
    
    print("\n============================================================")
    if success:
        print("🎉 FINAL AUTOMATION TEST PASSED")
        print("✅ Password filling automation is working correctly!")
    else:
        print("💥 FINAL AUTOMATION TEST FAILED")
        print("❌ Please check the credentials or account settings")
    print("👋 Test completed")
    print("============================================================")