#!/usr/bin/env python3
"""
Debug password field detection
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

def debug_password_field():
    """
    Debug what happens after email entry
    """
    print("🔍 Debugging Password Field Detection")
    print("=" * 50)
    
    # Test credentials
    test_email = 'nilamb010@gmail.com'
    
    driver = None
    try:
        # Setup Chrome WebDriver with anti-detection measures
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
        
        print(f"📍 Initial URL: {driver.current_url}")
        
        # Enter email first
        print("📧 Entering email...")
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.clear()
        email_input.send_keys(test_email)
        
        # Click Next
        next_button = driver.find_element(By.ID, "identifierNext")
        next_button.click()
        print("✅ Email entered and Next clicked")
        
        # Wait and check what happens
        print("⏳ Waiting for page transition...")
        time.sleep(5)
        
        print(f"📍 URL after email: {driver.current_url}")
        print(f"📄 Page title: {driver.title}")
        
        # Check for different possible password field selectors
        password_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.CSS_SELECTOR, "input[name='password']"),
            (By.CSS_SELECTOR, "input[aria-label*='password']"),
            (By.CSS_SELECTOR, "input[aria-label*='Password']"),
            (By.XPATH, "//input[@type='password']"),
            (By.XPATH, "//input[@name='password']"),
        ]
        
        print("\n🔍 Checking for password field with different selectors...")
        password_found = False
        
        for i, (by_type, selector) in enumerate(password_selectors, 1):
            try:
                element = driver.find_element(by_type, selector)
                print(f"✅ Method {i} ({by_type}, '{selector}'): Found password field")
                print(f"   - Tag: {element.tag_name}")
                print(f"   - Type: {element.get_attribute('type')}")
                print(f"   - Name: {element.get_attribute('name')}")
                print(f"   - ID: {element.get_attribute('id')}")
                print(f"   - Visible: {element.is_displayed()}")
                print(f"   - Enabled: {element.is_enabled()}")
                password_found = True
                break
            except Exception as e:
                print(f"❌ Method {i} ({by_type}, '{selector}'): {str(e)[:100]}")
        
        if not password_found:
            print("\n🔍 No password field found. Checking page source for clues...")
            page_source = driver.page_source
            
            # Look for password-related elements in page source
            password_keywords = ['password', 'Password', 'pwd', 'passwd']
            for keyword in password_keywords:
                if keyword in page_source:
                    print(f"✅ Found '{keyword}' in page source")
                    # Find lines containing the keyword
                    lines = page_source.split('\n')
                    for line_num, line in enumerate(lines):
                        if keyword in line and ('input' in line.lower() or 'field' in line.lower()):
                            print(f"   Line {line_num}: {line.strip()[:200]}")
            
            # Check for any input fields
            try:
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                print(f"\n📊 Found {len(all_inputs)} input fields on page:")
                for i, inp in enumerate(all_inputs[:10]):  # Show first 10
                    try:
                        print(f"   Input {i+1}: type='{inp.get_attribute('type')}', name='{inp.get_attribute('name')}', id='{inp.get_attribute('id')}'")
                    except:
                        print(f"   Input {i+1}: Could not get attributes")
            except Exception as e:
                print(f"❌ Could not find input fields: {e}")
        
        # Check if we're on a different page (like 2FA or account selection)
        if "challenge" in driver.current_url:
            print("\n⚠️ Redirected to challenge page - might need 2FA")
        elif "signin/v2/challenge" in driver.current_url:
            print("\n⚠️ Redirected to signin challenge - account might have additional security")
        elif "accounts.google.com/signin/v2/sl/pwd" in driver.current_url:
            print("\n✅ On password page - should have password field")
        
        print("\n🔄 Keeping browser open for 60 seconds for manual inspection...")
        time.sleep(60)
        
    except Exception as e:
        print(f"❌ Debug failed with exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("============================================================")
    print("🔍 PASSWORD FIELD DEBUG TEST")
    print("============================================================")
    
    debug_password_field()
    
    print("\n============================================================")
    print("🔍 DEBUG COMPLETE")
    print("============================================================")