#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for OAuth client generation
"""

import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_google_cloud_access():
    """Test if we can access Google Cloud Console"""
    driver = None
    try:
        print("🚀 Initializing Chrome WebDriver...")
        
        # Chrome options setup
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        # chrome_options.add_argument('--headless')  # Comment out for debugging
        
        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        print("✅ Chrome WebDriver initialized successfully")
        
        # Navigate to Google Cloud Console
        print("🌐 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            lambda d: "accounts.google.com" in d.current_url or "console.cloud.google.com" in d.current_url
        )
        
        print(f"✅ Successfully navigated to: {driver.current_url}")
        print(f"📄 Page title: {driver.title}")
        
        # Check if login is required
        if "accounts.google.com" in driver.current_url:
            print("🔐 Login page detected - manual login required")
            print("Please complete login manually and press Enter to continue...")
            input()
            
            # Wait for redirect to console
            WebDriverWait(driver, 60).until(
                lambda d: "console.cloud.google.com" in d.current_url
            )
            print("✅ Successfully logged in to Google Cloud Console")
        else:
            print("✅ Already logged in to Google Cloud Console")
        
        return True
        
    except TimeoutException as e:
        print(f"❌ Timeout error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            print("🔄 Closing browser...")
            driver.quit()
            print("✅ Browser closed")

if __name__ == "__main__":
    print("=== Google Cloud Console Access Test ===")
    success = test_google_cloud_access()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
    
    print("\nPress Enter to exit...")
    input()