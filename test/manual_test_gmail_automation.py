#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual Gmail OAuth Automation Test
ম্যানুয়াল Gmail OAuth automation test - User interaction সহ
"""

import sys
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_chrome_driver():
    """Setup Chrome driver with optimal settings"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add user agent to avoid detection
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def manual_test_gmail_automation():
    """Manual test for Gmail OAuth automation with user interaction"""
    print("=" * 70)
    print("🚀 Manual Gmail OAuth Automation Test")
    print("=" * 70)
    
    # Test credentials
    email = "kannanfdjm987@gmail.com"
    password = "6548;lkjhgqw"
    
    print(f"📧 Testing with email: {email}")
    print(f"🔑 Password: {'*' * len(password)}")
    print()
    
    driver = None
    
    try:
        # Setup Chrome driver
        print("🌐 Setting up Chrome browser...")
        driver = setup_chrome_driver()
        print("✅ Chrome browser initialized successfully")
        
        # Navigate to Google Cloud Console
        print("\n🔗 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        time.sleep(3)
        
        print("\n" + "="*60)
        print("📋 MANUAL TEST INSTRUCTIONS")
        print("="*60)
        print("1. ✅ Chrome browser has opened with Google Cloud Console")
        print(f"2. 📧 Please manually login with: {email}")
        print(f"3. 🔑 Password: {password}")
        print("4. 🔐 Complete any security challenges (2FA, captcha, etc.)")
        print("5. 📁 Once logged in, try to create a new project")
        print("6. 📧 Enable Gmail API for the project")
        print("7. 🔑 Create OAuth 2.0 credentials (Desktop application)")
        print("8. 💾 Download the JSON credentials file")
        print("="*60)
        
        # Wait for user to complete manual steps
        print("\n⏳ Browser will stay open for 5 minutes for manual testing...")
        print("🔍 Please complete the steps above manually")
        print("📊 Check if each step works correctly with the provided credentials")
        
        # Keep browser open for 5 minutes
        for i in range(30):
            time.sleep(10)
            print(f"⏰ Time remaining: {(30-i)*10} seconds")
            
        print("\n" + "="*60)
        print("📊 MANUAL TEST RESULTS")
        print("="*60)
        print("Please verify the following manually:")
        print("🔐 Login: Did you successfully login with the credentials?")
        print("📁 Project: Were you able to create/select a project?")
        print("📧 Gmail API: Could you enable Gmail API?")
        print("🔑 OAuth Credentials: Did OAuth credential creation work?")
        print("💾 JSON Download: Was the JSON file downloaded successfully?")
        print("="*60)
        
        # Get user feedback
        print("\n🤔 Based on your manual testing:")
        login_success = input("Did login work? (y/n): ").lower().strip() == 'y'
        project_success = input("Did project creation work? (y/n): ").lower().strip() == 'y'
        api_success = input("Did Gmail API enablement work? (y/n): ").lower().strip() == 'y'
        oauth_success = input("Did OAuth credentials creation work? (y/n): ").lower().strip() == 'y'
        download_success = input("Did JSON file download work? (y/n): ").lower().strip() == 'y'
        
        print("\n" + "="*60)
        print("📊 FINAL MANUAL TEST RESULTS")
        print("="*60)
        print(f"🔐 Login: {'✅ PASSED' if login_success else '❌ FAILED'}")
        print(f"📁 Project: {'✅ PASSED' if project_success else '❌ FAILED'}")
        print(f"📧 Gmail API: {'✅ PASSED' if api_success else '❌ FAILED'}")
        print(f"🔑 OAuth Credentials: {'✅ PASSED' if oauth_success else '❌ FAILED'}")
        print(f"💾 JSON Download: {'✅ PASSED' if download_success else '❌ FAILED'}")
        print("="*60)
        
        all_passed = all([login_success, project_success, api_success, oauth_success, download_success])
        
        if all_passed:
            print("🎉 ALL MANUAL TESTS PASSED! Gmail OAuth automation credentials are working!")
        else:
            print("⚠️ Some manual tests failed. Please check the individual step results above.")
            
        print("="*60)
        return all_passed
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
        
    finally:
        if driver:
            input("\n🔒 Press Enter to close the browser...")
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    success = manual_test_gmail_automation()
    if success:
        print("\n✅ Manual test completed successfully!")
        print("🎯 The Gmail OAuth automation credentials are working correctly!")
    else:
        print("\n❌ Manual test completed with some issues!")
        print("🔍 Please check the credentials or try different ones.")