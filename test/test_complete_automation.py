#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Gmail OAuth Automation Test
নতুন ক্রেডেনশিয়াল দিয়ে সম্পূর্ণ অটোমেশন টেস্ট
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add current directory to path to import main module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import GmailOAuthGenerator

def test_complete_automation():
    """
    Test complete Gmail OAuth automation with new credentials
    """
    print("=" * 60)
    print("🚀 Gmail OAuth Complete Automation Test Started")
    print("=" * 60)
    
    # Test credentials
    email = "wt24980@gmail.com"
    password = "654qwert"
    
    print(f"📧 Testing with email: {email}")
    print(f"🔑 Password: {'*' * len(password)}")
    print()
    
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        
        # Initialize Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome browser initialized successfully")
        
        # Create a dummy root for the class (we won't use GUI)
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Initialize the generator class
        generator = GmailOAuthGenerator(root)
        
        print("✅ Gmail OAuth Generator initialized")
        
        # Test Step 1: Login to Google Cloud Console
        print("\n🔐 Step 1: Testing login to Google Cloud Console...")
        login_result = generator.login_to_google_cloud(driver, email, password)
        
        if login_result:
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")
            driver.quit()
            return False
            
        # Test Step 2: Create or Select Project
        print("\n📁 Step 2: Testing project creation/selection...")
        project_result = generator.create_or_select_project(driver)
        
        if project_result:
            print("✅ Project creation/selection successful!")
        else:
            print("❌ Project creation/selection failed!")
            
        # Test Step 3: Enable Gmail API
        print("\n📧 Step 3: Testing Gmail API enablement...")
        api_result = generator.enable_gmail_api(driver)
        
        if api_result:
            print("✅ Gmail API enabled successfully!")
        else:
            print("❌ Gmail API enablement failed!")
            
        # Test Step 4: Create OAuth Credentials
        print("\n🔑 Step 4: Testing OAuth credentials creation...")
        credentials_result = generator.create_oauth_credentials(driver)
        
        if credentials_result:
            print("✅ OAuth credentials created successfully!")
        else:
            print("❌ OAuth credentials creation failed!")
            
        # Test Step 5: Download JSON file
        print("\n💾 Step 5: Testing JSON file download...")
        download_result = generator.download_json_file(driver, email)
        
        if download_result:
            print("✅ JSON file downloaded successfully!")
            print(f"📁 File saved as: {email.split('@')[0]}.json")
        else:
            print("❌ JSON file download failed!")
            
        # Keep browser open for inspection
        print("\n🔍 Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        
        # Close browser
        driver.quit()
        root.destroy()
        
        print("\n" + "=" * 60)
        if login_result and project_result and api_result and credentials_result and download_result:
            print("🎉 COMPLETE AUTOMATION TEST PASSED!")
            print("✅ All steps completed successfully")
        else:
            print("⚠️ AUTOMATION TEST COMPLETED WITH SOME ISSUES")
            print(f"Login: {'✅' if login_result else '❌'}")
            print(f"Project: {'✅' if project_result else '❌'}")
            print(f"API: {'✅' if api_result else '❌'}")
            print(f"Credentials: {'✅' if credentials_result else '❌'}")
            print(f"Download: {'✅' if download_result else '❌'}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return False

if __name__ == "__main__":
    test_complete_automation()