#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated test for single JSON generation
টেস্ট ইমেইল দিয়ে single JSON generation এর automated test
"""

import sys
import os
import time
import threading
from main import GmailOAuthGenerator
import tkinter as tk

def test_single_generation_automated():
    """Test single JSON generation programmatically"""
    
    print("🧪 Starting Automated Single JSON Generation Test")
    print("=" * 60)
    
    # Test credentials
    test_email = "diazdfc41@gmail.com"
    test_password = "dfgh85621"
    
    print(f"📧 Test Email: {test_email}")
    print(f"🔐 Test Password: {'*' * len(test_password)}")
    print()
    
    try:
        # Create Tkinter root (required for the app)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Create the OAuth generator instance
        print("🚀 Initializing Gmail OAuth Generator...")
        app = GmailOAuthGenerator(root)
        
        # Set the test credentials
        print("📝 Setting test credentials...")
        app.single_email.set(test_email)
        app.single_password.set(test_password)
        
        print("✅ Credentials set successfully")
        print()
        
        # Create a test account object
        test_account = {
            'email': test_email,
            'password': test_password,
            'line_num': 1
        }
        
        print("🔄 Starting OAuth client creation process...")
        print("⚠️ This will open a browser window for automation")
        print("⚠️ Manual intervention may be required for 2FA")
        print()
        
        # Test the create_oauth_client function directly
        success = app.create_oauth_client(test_account)
        
        print()
        print("=" * 60)
        if success:
            print("✅ Single JSON Generation Test PASSED!")
            print(f"📁 Check the output folder: {app.output_dir}")
            print("💡 JSON file should be created successfully")
        else:
            print("❌ Single JSON Generation Test FAILED!")
            print("💡 Check the logs above for error details")
            
        print("=" * 60)
        
        # Clean up
        root.destroy()
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_login_only():
    """Test only the login functionality"""
    
    print("🧪 Starting Login-Only Test")
    print("=" * 40)
    
    # Test credentials
    test_email = "diazdfc41@gmail.com"
    test_password = "dfgh85621"
    
    print(f"📧 Test Email: {test_email}")
    print()
    
    try:
        # Create Tkinter root (required for the app)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Create the OAuth generator instance
        print("🚀 Initializing Gmail OAuth Generator...")
        app = GmailOAuthGenerator(root)
        
        # Create a test account object
        test_account = {
            'email': test_email,
            'password': test_password,
            'line_num': 1
        }
        
        print("🔄 Testing login functionality only...")
        print("⚠️ This will open a browser window")
        print()
        
        # Test only the selenium setup and login
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        # Chrome options setup
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        print("🚀 Initializing Chrome WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        print("✅ Chrome WebDriver initialized successfully")
        
        try:
            # Test login
            print("🔐 Testing login to Google Cloud Console...")
            login_success = app.login_to_google_cloud(driver, test_account)
            
            print()
            print("=" * 40)
            if login_success:
                print("✅ Login Test PASSED!")
                print("💡 Credentials are working correctly")
            else:
                print("❌ Login Test FAILED!")
                print("💡 Check credentials or try manual verification")
                
            print("=" * 40)
            
            # Wait a bit to see the result
            print("⏳ Waiting 10 seconds to observe result...")
            time.sleep(10)
            
            return login_success
            
        finally:
            print("🔄 Closing browser...")
            driver.quit()
            root.destroy()
        
    except Exception as e:
        print(f"❌ Login test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Gmail OAuth Generator Test Suite")
    print("=" * 60)
    print()
    
    # Ask user which test to run
    print("Select test to run:")
    print("1. Login Only Test (recommended first)")
    print("2. Full Single JSON Generation Test")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        success = test_login_only()
    elif choice == "2":
        success = test_single_generation_automated()
    else:
        print("❌ Invalid choice. Running login test by default.")
        success = test_login_only()
    
    print()
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("💔 Test failed. Please check the logs above.")
    
    print("🏁 Test suite finished")