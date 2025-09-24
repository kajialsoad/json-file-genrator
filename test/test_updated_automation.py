#!/usr/bin/env python3
"""
Test the updated main.py automation with new credentials and improved password field detection
"""

import sys
import os
import time
import tkinter as tk
from main import GmailOAuthGenerator

def test_updated_automation():
    """
    Test the updated automation with new credentials
    """
    print("🧪 Testing Updated Automation with New Credentials")
    print("=" * 60)
    print("Email: nilamb010@gmail.com")
    print("Password: ,lkjghf9854")
    print("=" * 60)
    
    # Test credentials
    test_account = {
        'email': 'nilamb010@gmail.com',
        'password': ',lkjghf9854'
    }
    
    try:
        # Create a minimal tkinter root for the generator
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Initialize the generator
        generator = GmailOAuthGenerator(root)
        
        # Test the login function
        print("\n🔐 Testing login_to_google_cloud function...")
        
        # Setup Chrome driver
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(10)
        
        try:
            print("\n🚀 Starting login test...")
            login_result = generator.login_to_google_cloud(driver, test_account)
            
            print(f"\n📊 Login Result: {login_result}")
            
            if login_result:
                print("✅ LOGIN TEST PASSED: Updated automation works!")
                print("✅ Password field detection and filling successful!")
                
                # Check current URL to see where we ended up
                current_url = driver.current_url
                print(f"📍 Final URL: {current_url}")
                
                if "console.cloud.google.com" in current_url:
                    print("🎉 Successfully reached Google Cloud Console!")
                elif "accounts.google.com" in current_url:
                    print("⚠️ Still on Google accounts page - may need additional verification")
                else:
                    print(f"📍 Unexpected URL: {current_url}")
                
                # Manual inspection window
                print("\n⏳ 30 second inspection window...")
                time.sleep(30)
                
                return True
            else:
                print("❌ LOGIN TEST FAILED: Check the logs above")
                return False
                
        except Exception as e:
            print(f"❌ Login test error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"❌ Test setup error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            root.destroy()
        except:
            pass

def test_password_field_detection():
    """
    Specifically test the password field detection improvements
    """
    print("\n🔍 Testing Password Field Detection Improvements")
    print("=" * 60)
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Navigate to Google login
        print("🌐 Navigating to Google login...")
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        
        # Enter email
        print("📧 Entering email...")
        email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "identifierId"))
        )
        email_input.clear()
        email_input.send_keys("nilamb010@gmail.com")
        
        # Click Next
        next_button = driver.find_element(By.ID, "identifierNext")
        next_button.click()
        time.sleep(3)
        
        # Test updated password field selectors
        print("🔐 Testing updated password field selectors...")
        selectors = [
            (By.CSS_SELECTOR, "#password input"),  # Google's actual structure: div#password > input
            (By.XPATH, "//div[@id='password']//input"),  # Alternative xpath for div structure
            (By.CSS_SELECTOR, "div[data-initial-value] input"),  # Google's password div structure
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.CSS_SELECTOR, "input[name='Passwd']"),
            (By.XPATH, "//input[@type='password']"),
            (By.XPATH, "//input[@name='password']"),
            (By.XPATH, "//input[@name='Passwd']")
        ]
        
        password_input = None
        successful_selector = None
        
        for i, (selector_type, selector_value) in enumerate(selectors, 1):
            try:
                print(f"🔍 Testing selector {i}: {selector_type} = {selector_value}")
                password_input = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                successful_selector = (selector_type, selector_value)
                print(f"✅ SUCCESS: Selector {i} found password field!")
                break
            except Exception as e:
                print(f"❌ Selector {i} failed: {str(e)[:50]}...")
                continue
        
        if password_input and successful_selector:
            print(f"\n🎉 Password field detection successful!")
            print(f"✅ Working selector: {successful_selector[0]} = {successful_selector[1]}")
            print(f"📋 Element tag: {password_input.tag_name}")
            print(f"📋 Element enabled: {password_input.is_enabled()}")
            print(f"📋 Element displayed: {password_input.is_displayed()}")
            return True
        else:
            print("❌ Password field detection failed with all selectors")
            return False
            
    except Exception as e:
        print(f"❌ Password field detection test error: {e}")
        return False
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("============================================================")
    print("🧪 UPDATED AUTOMATION TEST WITH NEW CREDENTIALS")
    print("============================================================")
    
    # Test password field detection first
    detection_success = test_password_field_detection()
    
    print("\n" + "=" * 60)
    
    # Test full automation
    automation_success = test_updated_automation()
    
    print("\n============================================================")
    print("📊 TEST RESULTS:")
    print(f"🔍 Password Field Detection: {'✅ PASSED' if detection_success else '❌ FAILED'}")
    print(f"🤖 Full Automation: {'✅ PASSED' if automation_success else '❌ FAILED'}")
    
    if detection_success and automation_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Password filling issue has been resolved!")
        print("✅ Automation is working correctly with new credentials!")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("💡 Check the detailed logs above for troubleshooting")
    
    print("============================================================")
    time.sleep(2)