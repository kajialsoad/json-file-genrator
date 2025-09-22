#!/usr/bin/env python3
"""
Automated test for single JSON generation
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import GmailOAuthGenerator

def test_single_json_generation():
    """
    Test single JSON generation with provided credentials
    """
    print("🧪 Testing Single JSON Generation")
    print("=" * 50)
    
    # Test credentials
    test_email = "diazdfc41@gmail.com"
    test_password = "dfgh85621"
    
    print(f"📧 Testing with: {test_email}")
    
    try:
        # Create generator instance with dummy root
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        generator = GmailOAuthGenerator(root)
        
        # Set credentials
        generator.single_email.set(test_email)
        generator.single_password.set(test_password)
        
        print("🚀 Starting single JSON generation...")
        
        # Create account object
        account = {
            'email': test_email,
            'password': test_password,
            'line_num': 1
        }
        
        # Call the create_oauth_client method directly
        try:
            print("🔄 Calling create_oauth_client method...")
            
            # Add detailed step tracking
            print("📋 Account details:")
            print(f"   Email: {account['email']}")
            print(f"   Password: {'*' * len(account['password'])}")
            
            # Call the method with detailed tracking
            result = generator.create_oauth_client(account)
            print(f"🔍 create_oauth_client returned: {result}")
        except Exception as e:
            print(f"❌ Exception in create_oauth_client: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        if result:
            print("✅ Single JSON generation completed successfully!")
            
            # Check if output folder exists and has files
            output_folder = "output"
            if os.path.exists(output_folder):
                files = os.listdir(output_folder)
                json_files = [f for f in files if f.endswith('.json')]
                
                if json_files:
                    print(f"📁 Found {len(json_files)} JSON file(s) in output folder:")
                    for file in json_files:
                        print(f"   - {file}")
                        
                        # Check file content
                        file_path = os.path.join(output_folder, file)
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                                if len(content) > 100:  # Basic validation
                                    print(f"   ✅ {file} appears to be valid (size: {len(content)} chars)")
                                else:
                                    print(f"   ⚠️ {file} seems too small (size: {len(content)} chars)")
                        except Exception as e:
                            print(f"   ❌ Error reading {file}: {e}")
                else:
                    print("⚠️ No JSON files found in output folder")
            else:
                print("⚠️ Output folder not found")
                
            return True
        else:
            print("❌ Single JSON generation failed!")
            print("🔍 Checking process log for details...")
            
            # Try to get more details from the log
            try:
                if hasattr(generator, 'process_log') and generator.process_log:
                    print("📋 Recent process log entries:")
                    for entry in generator.process_log[-10:]:  # Last 10 entries
                        print(f"   {entry}")
            except Exception as log_e:
                print(f"⚠️ Could not retrieve process log: {log_e}")
            
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    Main test function
    """
    print("🔧 Gmail OAuth JSON Generator - Single Generation Test")
    print("=" * 60)
    
    success = test_single_json_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Test completed successfully!")
        print("✅ Single JSON generation is working properly")
    else:
        print("💥 Test failed!")
        print("❌ Single JSON generation needs debugging")
    
    print("\n⏳ Waiting 10 seconds before exit...")
    time.sleep(10)

if __name__ == "__main__":
    main()