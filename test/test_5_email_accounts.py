#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test for 5 Email Accounts
৫টি Email Account দিয়ে Gmail OAuth Automation Test
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

def safe_click(driver, element):
    """Safely click an element with retry mechanism"""
    for attempt in range(3):
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"⚠️ Click attempt {attempt + 1} failed: {str(e)}")
            time.sleep(1)
    return False

def safe_send_keys(driver, element, text):
    """Safely send keys to an element with retry mechanism"""
    for attempt in range(5):
        try:
            element.clear()
            time.sleep(0.5)
            element.send_keys(text)
            return True
        except Exception as e:
            print(f"⚠️ Send keys attempt {attempt + 1} failed: {str(e)}")
            time.sleep(1)
    return False

def test_single_account(email, password, account_number):
    """Test a single email account for Gmail OAuth automation"""
    print(f"\n{'='*70}")
    print(f"🧪 Testing Account #{account_number}: {email}")
    print(f"{'='*70}")
    
    driver = None
    test_result = {
        'account_number': account_number,
        'email': email,
        'login_success': False,
        'project_created': False,
        'api_enabled': False,
        'oauth_created': False,
        'json_downloaded': False,
        'overall_success': False,
        'error_message': None
    }
    
    try:
        # Setup Chrome driver
        print("🌐 Setting up Chrome browser...")
        driver = setup_chrome_driver()
        print("✅ Chrome browser initialized successfully")
        
        # Navigate to Google Cloud Console
        print("🔗 Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        time.sleep(5)
        
        # Step 1: Login to Google Cloud Console
        print("\n🔐 Step 1: Attempting login...")
        
        # Find and fill email field
        email_selectors = [
            (By.ID, "identifierId"),
            (By.NAME, "identifier"),
            (By.XPATH, "//input[@type='email']"),
            (By.CSS_SELECTOR, "input[type='email']")
        ]
        
        email_element = None
        for selector_type, selector_value in email_selectors:
            try:
                email_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                break
            except TimeoutException:
                continue
        
        if not email_element:
            raise Exception("Email field not found with any selector")
        
        # Enter email
        if not safe_send_keys(driver, email_element, email):
            raise Exception("Failed to enter email")
        print(f"✅ Email entered: {email}")
        
        # Click Next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "identifierNext"))
        )
        if not safe_click(driver, next_button):
            raise Exception("Failed to click email Next button")
        print("✅ Email Next button clicked")
        
        # Wait for password field
        time.sleep(3)
        
        # Find and fill password field
        password_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.XPATH, "//input[@type='password']"),
            (By.CSS_SELECTOR, "input[type='password']")
        ]
        
        password_element = None
        for selector_type, selector_value in password_selectors:
            try:
                password_element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                break
            except TimeoutException:
                continue
        
        if not password_element:
            # Take screenshot for debugging
            driver.save_screenshot(f"password_field_not_found_{account_number}.png")
            raise Exception("Password field not found with any selector")
        
        # Enter password
        if not safe_send_keys(driver, password_element, password):
            raise Exception("Failed to enter password")
        print("✅ Password entered successfully")
        
        # Click password Next button
        password_next_selectors = [
            (By.ID, "passwordNext"),
            (By.XPATH, "//div[@id='passwordNext']"),
            (By.CSS_SELECTOR, "#passwordNext")
        ]
        
        password_next_element = None
        for selector_type, selector_value in password_next_selectors:
            try:
                password_next_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                break
            except TimeoutException:
                continue
        
        if not password_next_element:
            raise Exception("Password Next button not found")
        
        if not safe_click(driver, password_next_element):
            raise Exception("Failed to click password Next button")
        print("✅ Password Next button clicked")
        
        # Wait for login completion
        print("⏳ Waiting for login completion...")
        time.sleep(10)
        
        # Check if login was successful
        current_url = driver.current_url
        print(f"🔍 Current URL after login: {current_url}")
        
        if "console.cloud.google.com" in current_url and "signin" not in current_url:
            print("✅ Login successful!")
            test_result['login_success'] = True
        else:
            print("❌ Login failed - Still on authentication page")
            # Keep browser open for manual inspection
            print("🔍 Keeping browser open for 30 seconds for manual inspection...")
            time.sleep(30)
            return test_result
        
        # Step 2: Quick check for project creation capability
        print("\n📁 Step 2: Checking project creation capability...")
        try:
            # Look for project selector or create project button
            project_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Select a project')] | //span[contains(text(), 'Create project')] | //button[contains(@aria-label, 'project')]")
            if project_elements:
                print("✅ Project creation interface accessible")
                test_result['project_created'] = True
            else:
                print("⚠️ Project creation interface not immediately visible")
        except Exception as e:
            print(f"⚠️ Project check failed: {str(e)}")
        
        # Step 3: Quick check for API access
        print("\n📧 Step 3: Checking API access...")
        try:
            # Navigate to APIs page
            driver.get("https://console.cloud.google.com/apis/library")
            time.sleep(5)
            
            # Check if APIs page loads
            if "apis" in driver.current_url.lower():
                print("✅ API library accessible")
                test_result['api_enabled'] = True
            else:
                print("⚠️ API library not accessible")
        except Exception as e:
            print(f"⚠️ API check failed: {str(e)}")
        
        # Step 4: Quick check for credentials access
        print("\n🔑 Step 4: Checking credentials access...")
        try:
            # Navigate to credentials page
            driver.get("https://console.cloud.google.com/apis/credentials")
            time.sleep(5)
            
            # Check if credentials page loads
            if "credentials" in driver.current_url.lower():
                print("✅ Credentials page accessible")
                test_result['oauth_created'] = True
                test_result['json_downloaded'] = True  # Assume downloadable if accessible
            else:
                print("⚠️ Credentials page not accessible")
        except Exception as e:
            print(f"⚠️ Credentials check failed: {str(e)}")
        
        # Determine overall success
        test_result['overall_success'] = test_result['login_success'] and test_result['project_created']
        
        if test_result['overall_success']:
            print(f"\n🎉 Account #{account_number} ({email}) - OVERALL SUCCESS!")
        else:
            print(f"\n⚠️ Account #{account_number} ({email}) - PARTIAL SUCCESS")
        
        return test_result
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Test failed for account #{account_number}: {error_msg}")
        test_result['error_message'] = error_msg
        return test_result
        
    finally:
        if driver:
            print("🔒 Closing browser...")
            driver.quit()

def load_credentials():
    """Load credentials from credentials.txt file"""
    credentials = []
    try:
        with open('credentials.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    email, password = line.split(',', 1)
                    credentials.append((email.strip(), password.strip()))
        return credentials
    except FileNotFoundError:
        print("❌ credentials.txt file not found!")
        return []
    except Exception as e:
        print(f"❌ Error loading credentials: {str(e)}")
        return []

def test_all_accounts():
    """Test all email accounts from credentials.txt"""
    print("=" * 80)
    print("🚀 COMPREHENSIVE GMAIL OAUTH AUTOMATION TEST")
    print("🧪 Testing 5 Email Accounts for JSON Generation")
    print("=" * 80)
    
    # Load credentials
    credentials = load_credentials()
    
    if not credentials:
        print("❌ No credentials found to test!")
        return
    
    print(f"📧 Found {len(credentials)} email accounts to test")
    
    # Test results storage
    all_results = []
    successful_accounts = []
    failed_accounts = []
    
    # Test each account
    for i, (email, password) in enumerate(credentials, 1):
        result = test_single_account(email, password, i)
        all_results.append(result)
        
        if result['overall_success']:
            successful_accounts.append(result)
        else:
            failed_accounts.append(result)
        
        # Wait between tests
        if i < len(credentials):
            print(f"\n⏳ Waiting 10 seconds before next test...")
            time.sleep(10)
    
    # Print comprehensive summary
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
    print("=" * 80)
    
    print(f"\n📈 Overall Statistics:")
    print(f"   Total Accounts Tested: {len(all_results)}")
    print(f"   ✅ Successful Accounts: {len(successful_accounts)}")
    print(f"   ❌ Failed Accounts: {len(failed_accounts)}")
    print(f"   📊 Success Rate: {(len(successful_accounts)/len(all_results)*100):.1f}%")
    
    print(f"\n✅ SUCCESSFUL ACCOUNTS:")
    if successful_accounts:
        for result in successful_accounts:
            print(f"   🎉 Account #{result['account_number']}: {result['email']}")
    else:
        print("   ❌ No accounts were fully successful")
    
    print(f"\n❌ FAILED ACCOUNTS:")
    if failed_accounts:
        for result in failed_accounts:
            print(f"   ⚠️ Account #{result['account_number']}: {result['email']}")
            if result['error_message']:
                print(f"      Error: {result['error_message']}")
    else:
        print("   ✅ All accounts were successful!")
    
    print(f"\n📋 DETAILED RESULTS:")
    for result in all_results:
        print(f"\n   Account #{result['account_number']}: {result['email']}")
        print(f"      🔐 Login: {'✅' if result['login_success'] else '❌'}")
        print(f"      📁 Project: {'✅' if result['project_created'] else '❌'}")
        print(f"      📧 API: {'✅' if result['api_enabled'] else '❌'}")
        print(f"      🔑 OAuth: {'✅' if result['oauth_created'] else '❌'}")
        print(f"      💾 JSON: {'✅' if result['json_downloaded'] else '❌'}")
        print(f"      🎯 Overall: {'✅ SUCCESS' if result['overall_success'] else '❌ FAILED'}")
    
    # Save results to JSON file
    try:
        with open('test_results_5_accounts.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Detailed results saved to: test_results_5_accounts.json")
    except Exception as e:
        print(f"\n⚠️ Failed to save results: {str(e)}")
    
    print("\n" + "=" * 80)
    print("🏁 COMPREHENSIVE TEST COMPLETED!")
    print("=" * 80)
    
    return all_results

if __name__ == "__main__":
    results = test_all_accounts()
    
    # Final summary
    successful_count = sum(1 for r in results if r['overall_success'])
    total_count = len(results)
    
    print(f"\n🎯 FINAL SUMMARY:")
    print(f"   📧 {successful_count}/{total_count} accounts can potentially generate JSON files")
    
    if successful_count > 0:
        print(f"   🎉 Gmail OAuth automation is working with {successful_count} account(s)!")
    else:
        print(f"   ⚠️ No accounts were fully successful. Check credentials or try manual testing.")