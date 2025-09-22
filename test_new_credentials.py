import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Test credentials provided by user
test_email = "nilamb010@gmail.com"
test_password = ",lkjghf9854"

print(f"Testing with email: {test_email}")
print(f"Password length: {len(test_password)}")

# Setup Chrome with anti-detection options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")

driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Navigate to Google login
    print("\n🌐 Navigating to Google login...")
    driver.get("https://accounts.google.com/signin")
    time.sleep(3)
    
    # Enter email
    print("\n📧 Entering email...")
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "identifierId"))
    )
    email_input.clear()
    email_input.send_keys(test_email)
    print("✅ Email entered successfully")
    
    # Click Next
    next_button = driver.find_element(By.ID, "identifierNext")
    next_button.click()
    print("✅ Next button clicked")
    
    # Wait for password page
    time.sleep(3)
    print(f"\n📍 Current URL: {driver.current_url}")
    print(f"📍 Page title: {driver.title}")
    
    # Try updated password field selectors
    print("\n🔐 Testing password field detection...")
    password_input = None
    selectors = [
        (By.CSS_SELECTOR, "#password input"),  # Google's actual structure: div#password > input
        (By.XPATH, "//div[@id='password']//input"),  # Alternative xpath for div structure
        (By.CSS_SELECTOR, "div[data-initial-value] input"),  # Google's password div structure
        (By.NAME, "password"),
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[name='Passwd']"),
        (By.XPATH, "//input[@type='password']"),
        (By.XPATH, "//input[@name='password']"),
        (By.XPATH, "//input[@name='Passwd']")
    ]
    
    for i, (selector_type, selector_value) in enumerate(selectors, 1):
        try:
            print(f"🔍 Method {i}: Trying {selector_type} = {selector_value}")
            password_input = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((selector_type, selector_value))
            )
            print(f"✅ Method {i} SUCCESS: Password field found!")
            print(f"   Element tag: {password_input.tag_name}")
            print(f"   Element enabled: {password_input.is_enabled()}")
            print(f"   Element displayed: {password_input.is_displayed()}")
            break
        except Exception as e:
            print(f"❌ Method {i} failed: {str(e)[:100]}...")
            continue
    
    if password_input:
        print("\n🔐 Attempting to fill password...")
        
        # Method 1: Standard approach
        try:
            password_input.click()
            time.sleep(1)
            password_input.clear()
            password_input.send_keys(test_password)
            
            # Verify
            password_value = password_input.get_attribute("value")
            print(f"✅ Password filled - Length: {len(password_value)} (expected: {len(test_password)})")
            
            if len(password_value) == len(test_password):
                print("✅ PASSWORD FILLING SUCCESS!")
                
                # Try to click Next
                print("\n🔍 Looking for Next button...")
                next_selectors = [
                    (By.ID, "passwordNext"),
                    (By.CSS_SELECTOR, "#passwordNext"),
                    (By.XPATH, "//button[@id='passwordNext']"),
                    (By.XPATH, "//span[contains(text(), 'Next')]/parent::button"),
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.XPATH, "//div[@id='passwordNext']")
                ]
                
                next_button = None
                for selector_type, selector_value in next_selectors:
                    try:
                        next_button = driver.find_element(selector_type, selector_value)
                        print(f"✅ Next button found with: {selector_type} = {selector_value}")
                        break
                    except:
                        continue
                
                if next_button:
                    next_button.click()
                    print("✅ Next button clicked!")
                    time.sleep(5)
                    print(f"📍 Final URL: {driver.current_url}")
                else:
                    print("❌ Next button not found")
            else:
                print("❌ Password length mismatch")
                
        except Exception as e:
            print(f"❌ Password filling failed: {e}")
    else:
        print("❌ PASSWORD FIELD NOT FOUND WITH ANY SELECTOR")
    
    # Manual inspection window
    print("\n⏳ 30 second manual inspection window...")
    time.sleep(30)
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
    print("\n🏁 Test completed")