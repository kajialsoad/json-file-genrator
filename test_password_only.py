#!/usr/bin/env python3
"""
Test password filling specifically
"""

import sys
import os
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from main import GmailOAuthGenerator

def test_password_filling():
    """
    Test password filling specifically after email entry
    """
    print("🧪 Testing Password Filling Only")
    print("=" * 50)
    
    # Test credentials
    test_account = {
        'email': 'nilamb010@gmail.com',
        'password': ',lkjghf9854'
    }
    
    print(f"📧 Testing with: {test_account['email']}")
    print(f"🔐 Password: {test_account['password']}")
    
    driver = None
    try:
        # Create generator instance with dummy root
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        generator = GmailOAuthGenerator(root)
        # Initialize the UI to enable logging
        generator.setup_ui()
        
        # Setup Chrome WebDriver manually with anti-detection measures
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument('--headless')  # Comment out for debugging
        
        print("🚀 Initializing Chrome WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to hide WebDriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.implicitly_wait(10)
        print("✅ Chrome WebDriver initialized successfully")
        
        # Navigate to Google login page directly
        print("🌐 Navigating to Google login page...")
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        
        # Enter email first
        print("📧 Entering email...")
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.clear()
        email_input.send_keys(test_account['email'])
        
        # Click Next
        next_button = driver.find_element(By.ID, "identifierNext")
        next_button.click()
        print("✅ Email entered and Next clicked")
        
        # Wait for password field
        print("🔐 Waiting for password field...")
        time.sleep(3)
        
        try:
            password_input = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            print("✅ Password field found")
            
            # Test different password filling methods
            print("\n🧪 Testing Method 1: Standard send_keys")
            password_input.clear()
            password_input.send_keys(test_account['password'])
            password_value = password_input.get_attribute("value")
            print(f"📊 Password length after Method 1: {len(password_value)} (expected: {len(test_account['password'])})")
            
            if len(password_value) != len(test_account['password']):
                print("\n🧪 Testing Method 2: JavaScript approach")
                driver.execute_script("arguments[0].value = '';", password_input)
                driver.execute_script("arguments[0].value = arguments[1];", password_input, test_account['password'])
                driver.execute_script("""
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """, password_input)
                password_value = password_input.get_attribute("value")
                print(f"📊 Password length after Method 2: {len(password_value)} (expected: {len(test_account['password'])})")
            
            if len(password_value) != len(test_account['password']):
                print("\n🧪 Testing Method 3: Character by character")
                password_input.clear()
                for char in test_account['password']:
                    password_input.send_keys(char)
                    time.sleep(0.1)
                password_value = password_input.get_attribute("value")
                print(f"📊 Password length after Method 3: {len(password_value)} (expected: {len(test_account['password'])})")
            
            # Try to click Next
            print("\n🔍 Looking for password Next button...")
            try:
                password_next = driver.find_element(By.ID, "passwordNext")
                password_next.click()
                print("✅ Password Next button clicked")
                
                # Wait and check result
                time.sleep(5)
                current_url = driver.current_url
                print(f"📍 Final URL: {current_url}")
                
                if "challenge/pwd" in current_url:
                    print("❌ Password was rejected - incorrect password")
                    return False
                elif "console.cloud.google.com" in current_url or "myaccount.google.com" in current_url:
                    print("✅ Login successful!")
                    return True
                else:
                    print(f"⚠️ Unexpected URL: {current_url}")
                    return False
                    
            except Exception as e:
                print(f"❌ Failed to find/click password Next button: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to find password field: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass
        
        if driver:
            print("\n🔄 Keeping browser open for 30 seconds for manual inspection...")
            time.sleep(30)
            driver.quit()

if __name__ == "__main__":
    print("============================================================")
    print("🧪 PASSWORD FILLING TEST")
    print("============================================================")
    
    success = test_password_filling()
    
    print("\n============================================================")
    if success:
        print("🎉 PASSWORD FILLING TEST PASSED")
        print("✅ Password filling working correctly!")
    else:
        print("❌ PASSWORD FILLING TEST FAILED")
        print("💡 Check the detailed logs above for troubleshooting")
    print("============================================================")