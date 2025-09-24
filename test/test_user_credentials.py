#!/usr/bin/env python3
"""
Test with user provided credentials
"""

import sys
import os
import time
import tkinter as tk
from main import GmailOAuthGenerator

def test_with_user_credentials():
    """
    Test with user provided credentials: diazdfc41@gmail.com / dfgh85621
    """
    print("🧪 Testing with User Provided Credentials")
    print("=" * 50)
    
    # User provided credentials
    test_email = "diazdfc41@gmail.com"
    test_password = "dfgh85621"
    
    print(f"📧 Email: {test_email}")
    print(f"🔐 Password: {'*' * len(test_password)}")
    
    try:
        # Create generator instance
        root = tk.Tk()
        root.withdraw()  # Hide the window
        generator = GmailOAuthGenerator(root)
        
        # Create account object
        account = {
            'email': test_email,
            'password': test_password,
            'line_num': 1
        }
        
        print("\n🚀 Starting OAuth client creation...")
        print("📋 This will test the complete automation process:")
        print("   1. Login to Google Cloud Console")
        print("   2. Create/Select Project")
        print("   3. Enable Gmail API")
        print("   4. Create OAuth Credentials")
        print("   5. Save JSON file")
        print("\n" + "-" * 50)
        
        # Call the method with detailed tracking
        result = generator.create_oauth_client(account)
        
        print("\n" + "-" * 50)
        print(f"🔍 Final Result: {result}")
        
        if result:
            print("✅ SUCCESS: OAuth client creation completed!")
            
            # Check output folder
            output_folder = "output"
            if os.path.exists(output_folder):
                files = os.listdir(output_folder)
                json_files = [f for f in files if f.endswith('.json')]
                
                if json_files:
                    print(f"\n📁 Generated JSON files ({len(json_files)}):")
                    for file in json_files:
                        print(f"   - {file}")
                        
                        # Validate file content
                        file_path = os.path.join(output_folder, file)
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                                if 'client_id' in content and 'client_secret' in content:
                                    print(f"   ✅ {file} contains valid OAuth credentials")
                                else:
                                    print(f"   ⚠️ {file} may be incomplete")
                        except Exception as e:
                            print(f"   ❌ Error reading {file}: {e}")
                else:
                    print("\n⚠️ No JSON files found in output folder")
            else:
                print("\n⚠️ Output folder not found")
                
        else:
            print("❌ FAILED: OAuth client creation failed!")
            print("\n🔍 Possible reasons:")
            print("   - Login credentials incorrect")
            print("   - 2FA required")
            print("   - Google Cloud Console UI changed")
            print("   - Network/timeout issues")
            print("   - Selenium automation errors")
            
        return result
        
    except Exception as e:
        print(f"\n❌ Test Exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass

def main():
    print("🔧 Gmail OAuth Generator - User Credentials Test")
    print("=" * 60)
    
    success = test_with_user_credentials()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: User credentials work correctly!")
    else:
        print("💥 TEST FAILED: Issues with user credentials or automation")
    
    print("\n⏳ Test completed. Check the browser window for any manual steps needed.")
    print("Press Ctrl+C to exit if needed.")
    
    # Keep window open for manual intervention if needed
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")

if __name__ == "__main__":
    main()