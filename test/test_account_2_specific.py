#!/usr/bin/env python3
"""
Specific test for nilamb010@gmail.com account with detailed logging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
import json

def test_account_2_detailed():
    """Test nilamb010@gmail.com with detailed logging"""
    
    # Test credentials
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    print(f"=== Testing Account 2: {email} ===")
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    test_results = {
        "email": email,
        "steps": [],
        "errors": [],
        "success": False,
        "final_url": "",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        print("1. Initializing Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        test_results["steps"].append("Chrome driver initialized successfully")
        
        print("2. Navigating to Google Cloud Console...")
        driver.get("https://console.cloud.google.com/")
        time.sleep(3)
        test_results["steps"].append("Navigated to Google Cloud Console")
        
        print("3. Looking for sign-in elements...")
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        test_results["steps"].append(f"Current URL: {current_url}")
        
        # Check if already on login page or need to click sign in
        if "accounts.google.com" not in current_url:
            try:
                # Look for sign in button
                sign_in_selectors = [
                    "//a[contains(text(), 'Sign in')]",
                    "//button[contains(text(), 'Sign in')]",
                    "//a[@data-action='sign in']",
                    ".gb_Bd.gb_Md.gb_Ld",
                    "[data-action='sign in']"
                ]
                
                sign_in_clicked = False
                for selector in sign_in_selectors:
                    try:
                        if selector.startswith("//"):
                            element = driver.find_element(By.XPATH, selector)
                        else:
                            element = driver.find_element(By.CSS_SELECTOR, selector)
                        element.click()
                        print(f"Clicked sign in button with selector: {selector}")
                        test_results["steps"].append(f"Clicked sign in with selector: {selector}")
                        sign_in_clicked = True
                        time.sleep(3)
                        break
                    except Exception as e:
                        continue
                
                if not sign_in_clicked:
                    print("No sign in button found, checking if already on login page...")
                    test_results["steps"].append("No sign in button found")
            except Exception as e:
                print(f"Error looking for sign in: {e}")
                test_results["errors"].append(f"Sign in error: {str(e)}")
        
        print("4. Entering email...")
        time.sleep(2)
        
        # Email input
        email_selectors = [
            "input[type='email']",
            "#identifierId",
            "input[name='identifier']",
            "input[autocomplete='username']"
        ]
        
        email_entered = False
        for selector in email_selectors:
            try:
                email_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                email_field.clear()
                email_field.send_keys(email)
                print(f"Email entered successfully with selector: {selector}")
                test_results["steps"].append(f"Email entered with selector: {selector}")
                email_entered = True
                break
            except Exception as e:
                print(f"Failed with email selector {selector}: {e}")
                continue
        
        if not email_entered:
            raise Exception("Could not find email input field")
        
        # Click Next button after email
        time.sleep(2)
        next_selectors = [
            "#identifierNext",
            "button[jsname='LgbsSe']",
            "//button[contains(text(), 'Next')]",
            "//div[@id='identifierNext']",
            ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.qIypjc.TrZEUc.lw1w4b"
        ]
        
        next_clicked = False
        for selector in next_selectors:
            try:
                if selector.startswith("//"):
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                else:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                next_button.click()
                print(f"Next button clicked with selector: {selector}")
                test_results["steps"].append(f"Next button clicked with selector: {selector}")
                next_clicked = True
                break
            except Exception as e:
                print(f"Failed with next selector {selector}: {e}")
                continue
        
        if not next_clicked:
            print("Warning: Could not click Next button, continuing...")
            test_results["errors"].append("Could not click Next button after email")
        
        print("5. Waiting for password field...")
        time.sleep(5)
        
        # Password input with multiple strategies
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "#password",
            "input[autocomplete='current-password']",
            "div[data-form-type='password'] input",
            ".whsOnd.zHQkBf"
        ]
        
        password_entered = False
        for selector in password_selectors:
            try:
                print(f"Trying password selector: {selector}")
                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                
                # Check if element is visible and interactable
                if password_field.is_displayed() and password_field.is_enabled():
                    # Try different methods to enter password
                    try:
                        password_field.clear()
                        password_field.send_keys(password)
                        print(f"Password entered successfully with selector: {selector}")
                        test_results["steps"].append(f"Password entered with selector: {selector}")
                        password_entered = True
                        break
                    except ElementNotInteractableException:
                        # Try JavaScript injection
                        driver.execute_script("arguments[0].value = arguments[1];", password_field, password)
                        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", password_field)
                        print(f"Password entered via JavaScript with selector: {selector}")
                        test_results["steps"].append(f"Password entered via JavaScript with selector: {selector}")
                        password_entered = True
                        break
                else:
                    print(f"Password field not interactable with selector: {selector}")
                    
            except Exception as e:
                print(f"Failed with password selector {selector}: {e}")
                test_results["errors"].append(f"Password selector {selector} failed: {str(e)}")
                continue
        
        if not password_entered:
            raise Exception("Could not enter password in any field")
        
        print("6. Clicking Next/Sign in button...")
        time.sleep(2)
        
        # Next/Sign in button after password
        signin_selectors = [
            "#passwordNext",
            "button[jsname='LgbsSe']",
            "//button[contains(text(), 'Next')]",
            "//button[contains(text(), 'Sign in')]",
            "//div[@id='passwordNext']",
            ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.qIypjc.TrZEUc.lw1w4b"
        ]
        
        signin_clicked = False
        for selector in signin_selectors:
            try:
                if selector.startswith("//"):
                    signin_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                else:
                    signin_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                signin_button.click()
                print(f"Sign in button clicked with selector: {selector}")
                test_results["steps"].append(f"Sign in button clicked with selector: {selector}")
                signin_clicked = True
                break
            except Exception as e:
                print(f"Failed with signin selector {selector}: {e}")
                continue
        
        if not signin_clicked:
            print("Warning: Could not click Sign in button")
            test_results["errors"].append("Could not click Sign in button")
        
        print("7. Waiting for login result...")
        time.sleep(10)
        
        # Check final URL and login status
        final_url = driver.current_url
        test_results["final_url"] = final_url
        print(f"Final URL: {final_url}")
        
        if "console.cloud.google.com" in final_url and "accounts.google.com" not in final_url:
            print("✅ LOGIN SUCCESSFUL!")
            test_results["success"] = True
            test_results["steps"].append("Login successful - reached Google Cloud Console")
        elif "challenge" in final_url:
            print("❌ LOGIN FAILED - Challenge/Verification required")
            test_results["errors"].append("Challenge/Verification required")
        elif "signin" in final_url or "accounts.google.com" in final_url:
            print("❌ LOGIN FAILED - Still on login page")
            test_results["errors"].append("Still on login page - credentials may be incorrect")
        else:
            print(f"❓ UNKNOWN STATE - URL: {final_url}")
            test_results["errors"].append(f"Unknown state - URL: {final_url}")
        
        # Take screenshot for debugging
        try:
            screenshot_path = f"test_account_2_screenshot_{int(time.time())}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
            test_results["steps"].append(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Could not save screenshot: {e}")
        
        # Wait for manual inspection
        print("Waiting 30 seconds for manual inspection...")
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        test_results["errors"].append(f"Test failed: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
        
        # Save detailed results
        results_file = "test_account_2_detailed_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== Test Results Saved to {results_file} ===")
        print(f"Success: {test_results['success']}")
        print(f"Steps completed: {len(test_results['steps'])}")
        print(f"Errors encountered: {len(test_results['errors'])}")
        
        return test_results

if __name__ == "__main__":
    test_account_2_detailed()