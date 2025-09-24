#!/usr/bin/env python3
"""
Test the main.py login function with user credentials
"""

import sys
import os
import time
import tkinter as tk
from main import GmailOAuthGenerator

def test_main_login():
    """
    Test the main.py login function
    """
    print("🧪 Testing Main.py Login Function")
    print("=" * 50)
    
    # User provided credentials
    test_email = "diazdfc41@gmail.com"
    test_password = "dfgh85621"
    
    print(f"📧 Email: {test_email}")
    print(f"🔐 Password: {'*' * len(test_password)}")
    
    # Create root window for the generator
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    try:
        # Create generator instance
        generator = GmailOAuthGenerator(root)
        
        # Test account
        account = {
            'email': test_email,
            'password': test_password
        }
        
        print("\n🚀 Starting login test...")
        
        # Test login function directly
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Setup Chrome driver
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        try:
            # Test the login function from main.py
            print("\n🔐 Testing login_to_google_cloud function...")
            login_result = generator.login_to_google_cloud(driver, account)
            
            print(f"\n📊 Login Result: {login_result}")
            
            if login_result:
                print("✅ LOGIN TEST PASSED: Main.py login function works!")
            else:
                print("❌ LOGIN TEST FAILED: Main.py login function failed!")
            
            # Keep browser open for inspection
            print("\n🔄 Keeping browser open for 30 seconds for manual inspection...")
            time.sleep(30)
            
        finally:
            driver.quit()
            print("🔄 Browser closed")
            
        return login_result
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False
    finally:
        root.destroy()

if __name__ == "__main__":
    print("🧪 Starting Main.py Login Test")
    print("=" * 60)
    
    success = test_main_login()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 MAIN LOGIN TEST PASSED: Function works correctly!")
    else:
        print("❌ MAIN LOGIN TEST FAILED: Function needs fixing!")
    
    print("\n👋 Test completed")
    time.sleep(2)