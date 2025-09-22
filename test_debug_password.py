from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
import traceback

def debug_password_filling():
    print("🚀 Starting detailed password filling debug test...")
    
    # User credentials
    email = "nilamb010@gmail.com"
    password = ",lkjghf9854"
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("🌐 Navigating to Google Cloud Console (which redirects to login)...")
        driver.get("https://console.cloud.google.com/")
        
        # Wait for page load
        time.sleep(5)
        print(f"📍 Current URL: {driver.current_url}")
        
        # Check if we're on login page
        if "accounts.google.com" not in driver.current_url:
            print("❌ Not redirected to login page. User might already be logged in.")
            print("🔄 Trying direct login URL...")
            driver.get("https://accounts.google.com/signin")
            time.sleep(3)
            print(f"📍 New URL: {driver.current_url}")
        
        # Step 1: Email entry
        print("📧 Step 1: Entering email...")
        try:
            email_field = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "identifierId"))
            )
            email_field.clear()
            email_field.send_keys(email)
            print(f"✅ Email entered: {email}")
            
            # Click Next
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "identifierNext"))
            )
            next_button.click()
            print("✅ Next button clicked after email")
            
        except Exception as e:
            print(f"❌ Email entry failed: {e}")
            print("🔍 Let's check what's on the page:")
            try:
                page_title = driver.title
                page_source_snippet = driver.page_source[:500]
                print(f"   Page title: {page_title}")
                print(f"   Page source snippet: {page_source_snippet}")
            except:
                pass
            return False
        
        # Wait for password page
        time.sleep(5)
        print(f"📍 After email, current URL: {driver.current_url}")
        
        # Step 2: Password entry with detailed debugging
        print("🔐 Step 2: Detailed password field analysis...")
        
        # Try multiple password field selectors
        password_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.CSS_SELECTOR, "input[name='password']"),
            (By.CSS_SELECTOR, "input[name='Passwd']"),
            (By.CSS_SELECTOR, "input[aria-label*='password']"),
            (By.CSS_SELECTOR, "input[aria-label*='Password']"),
            (By.XPATH, "//input[@type='password']"),
            (By.XPATH, "//input[@name='password']"),
            (By.XPATH, "//input[@name='Passwd']"),
        ]
        
        password_field = None
        successful_selector = None
        
        for i, (by, selector) in enumerate(password_selectors):
            try:
                print(f"🔍 Trying selector {i+1}: {by} = '{selector}'")
                field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                print(f"✅ Found password field with selector {i+1}")
                
                # Check field properties
                print(f"   - Tag: {field.tag_name}")
                print(f"   - Type: {field.get_attribute('type')}")
                print(f"   - Name: {field.get_attribute('name')}")
                print(f"   - ID: {field.get_attribute('id')}")
                print(f"   - Class: {field.get_attribute('class')}")
                print(f"   - Enabled: {field.is_enabled()}")
                print(f"   - Displayed: {field.is_displayed()}")
                print(f"   - Value: '{field.get_attribute('value')}'")
                print(f"   - Aria-label: {field.get_attribute('aria-label')}")
                
                # Check if clickable
                try:
                    clickable_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"   - Clickable: Yes")
                    password_field = clickable_field
                    successful_selector = (by, selector)
                    break
                except:
                    print(f"   - Clickable: No")
                    
            except Exception as e:
                print(f"   - Not found: {e}")
        
        if not password_field:
            print("❌ No password field found with any selector")
            print("🔍 Let's check all input fields on the page:")
            
            try:
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                print(f"   Found {len(all_inputs)} input fields:")
                for i, inp in enumerate(all_inputs):
                    print(f"   Input {i+1}:")
                    print(f"     - Type: {inp.get_attribute('type')}")
                    print(f"     - Name: {inp.get_attribute('name')}")
                    print(f"     - ID: {inp.get_attribute('id')}")
                    print(f"     - Class: {inp.get_attribute('class')}")
                    print(f"     - Placeholder: {inp.get_attribute('placeholder')}")
                    print(f"     - Aria-label: {inp.get_attribute('aria-label')}")
                    print(f"     - Enabled: {inp.is_enabled()}")
                    print(f"     - Displayed: {inp.is_displayed()}")
                    print(f"     - Value: '{inp.get_attribute('value')}'")
            except Exception as e:
                print(f"   Error listing inputs: {e}")
            
            return False
        
        # Try different password filling methods
        print(f"🔐 Attempting to fill password using successful selector: {successful_selector}")
        
        methods = [
            "standard_selenium",
            "javascript_direct",
            "javascript_with_events",
            "character_by_character",
            "focus_and_type"
        ]
        
        password_success = False
        
        for method in methods:
            try:
                print(f"🔄 Trying method: {method}")
                
                # Re-find the field to ensure it's fresh
                field = driver.find_element(*successful_selector)
                
                if method == "standard_selenium":
                    field.click()
                    time.sleep(0.5)
                    field.clear()
                    field.send_keys(password)
                    
                elif method == "javascript_direct":
                    driver.execute_script(f"arguments[0].value = '{password}';", field)
                    
                elif method == "javascript_with_events":
                    script = f"""
                    var field = arguments[0];
                    field.focus();
                    field.value = '{password}';
                    field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    field.dispatchEvent(new Event('keyup', {{ bubbles: true }}));
                    """
                    driver.execute_script(script, field)
                    
                elif method == "character_by_character":
                    field.click()
                    time.sleep(0.5)
                    field.clear()
                    for char in password:
                        field.send_keys(char)
                        time.sleep(0.1)
                        
                elif method == "focus_and_type":
                    driver.execute_script("arguments[0].focus();", field)
                    time.sleep(0.5)
                    field.clear()
                    field.send_keys(password)
                
                # Verify password was entered
                time.sleep(1)
                current_value = field.get_attribute('value')
                print(f"   - Password field value after {method}: '{current_value}'")
                print(f"   - Expected: '{password}'")
                print(f"   - Match: {current_value == password}")
                
                if current_value == password:
                    print(f"✅ Password successfully entered using {method}")
                    password_success = True
                    break
                else:
                    print(f"❌ Password not properly entered using {method}")
                    
            except Exception as e:
                print(f"❌ Method {method} failed: {e}")
                print(f"   Stack trace: {traceback.format_exc()}")
        
        if password_success:
            print("✅ Password filling successful!")
            
            # Try to click Next
            print("🔄 Looking for Next button...")
            next_selectors = [
                (By.ID, "passwordNext"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Next')]"),
                (By.XPATH, "//input[@value='Next']"),
                (By.XPATH, "//div[@id='passwordNext']"),
            ]
            
            next_clicked = False
            for by, selector in next_selectors:
                try:
                    next_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    next_btn.click()
                    print(f"✅ Next button clicked using: {selector}")
                    next_clicked = True
                    break
                except Exception as e:
                    print(f"❌ Next button selector failed: {selector} - {e}")
                    continue
            
            if not next_clicked:
                print("❌ Could not find or click Next button")
                print("🔍 Let's check all buttons on the page:")
                try:
                    all_buttons = driver.find_elements(By.TAG_NAME, "button")
                    all_divs = driver.find_elements(By.TAG_NAME, "div")
                    print(f"   Found {len(all_buttons)} buttons and {len(all_divs)} divs")
                    for i, btn in enumerate(all_buttons[:10]):  # Limit to first 10
                        print(f"   Button {i+1}: text='{btn.text}', id='{btn.get_attribute('id')}', class='{btn.get_attribute('class')}'")
                except Exception as e:
                    print(f"   Error listing buttons: {e}")
            
            # Wait and check result
            time.sleep(5)
            final_url = driver.current_url
            print(f"📍 Final URL: {final_url}")
            
            if "challenge/pwd" in final_url:
                print("❌ Login failed - incorrect password or account issue")
            elif "console.cloud.google.com" in final_url:
                print("✅ Login appears successful!")
            elif "signin" in final_url:
                print("❓ Still on signin page - check if Next button was clicked")
            else:
                print(f"❓ Unexpected URL: {final_url}")
        else:
            print("❌ Password filling failed - could not enter password with any method")
        
        # Keep browser open for inspection
        print("🔄 Keeping browser open for 30 seconds for manual inspection...")
        time.sleep(30)
        
    except Exception as e:
        print(f"💥 Test failed with error: {e}")
        print(f"Stack trace: {traceback.format_exc()}")
        return False
    finally:
        if driver:
            driver.quit()
            print("🔄 Browser closed")
    
    print("\n" + "="*60)
    print("🔍 DEBUG TEST COMPLETED")
    print("📋 Check the detailed logs above for password filling analysis")
    print("="*60)
    return True

if __name__ == "__main__":
    debug_password_filling()