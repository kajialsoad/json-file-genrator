#!/usr/bin/env python3
"""
Direct test of the login_to_google_cloud method with enhanced debugging
"""

import sys
import os
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from main import GmailOAuthGenerator

def test_direct_login():
    """
    Test the login_to_google_cloud method directly with enhanced debugging
    """
    print("🧪 Testing Direct Login to Google Cloud")
    print("=" * 60)
    
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
        
        # Create account object
        account = {
            'email': test_account['email'],
            'password': test_account['password'],
            'line_num': 1
        }
        
        print("\n🚀 Starting direct login test...")
        print("📍 This will test ONLY the login_to_google_cloud method")
        
        # Test the login method directly
        login_result = generator.login_to_google_cloud(driver, account)
        
        print(f"\n📊 Login Result: {login_result}")
        print(f"📍 Final URL: {driver.current_url}")
        
        if login_result:
            print("\n✅ DIRECT LOGIN TEST PASSED")
            print("🎉 Login to Google Cloud Console successful!")
            return True
        else:
            print("\n❌ DIRECT LOGIN TEST FAILED")
            print("💡 Check the logs above for details")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
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
    print("🧪 DIRECT LOGIN TEST WITH CORRECT CREDENTIALS")
    print("============================================================")
    
    success = test_direct_login()
    
    print("\n============================================================")
    if success:
        print("🎉 DIRECT LOGIN TEST PASSED")
        print("✅ Login method working correctly!")
    else:
        print("❌ DIRECT LOGIN TEST FAILED")
        print("💡 Check the detailed logs above for troubleshooting")
    print("============================================================")