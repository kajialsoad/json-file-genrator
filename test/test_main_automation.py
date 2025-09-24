#!/usr/bin/env python3
"""
Test the main.py automation with correct credentials
"""

import sys
import os
import time
import tkinter as tk
from main import GmailOAuthGenerator

def test_main_automation():
    """
    Test the main automation function with correct credentials
    """
    print("🧪 Testing Main Automation with Correct Credentials")
    print("=" * 60)
    
    # Test credentials
    test_email = "nilamb010@gmail.com"
    test_password = ",lkjghf9854"
    
    print(f"📧 Testing with: {test_email}")
    print(f"🔐 Password: {test_password}")
    
    try:
        # Create generator instance with dummy root
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        generator = GmailOAuthGenerator(root)
        
        # Create account object
        account = {
            'email': test_email,
            'password': test_password,
            'line_num': 1
        }
        
        print("\n🚀 Starting automation process...")
        print("📍 This will test the complete OAuth client creation process")
        
        # Test the automation
        success = generator.create_oauth_client(account)
        
        if success:
            print("\n✅ AUTOMATION TEST PASSED")
            print("🎉 OAuth client creation completed successfully!")
            return True
        else:
            print("\n❌ AUTOMATION TEST FAILED")
            print("💡 Check the logs above for details")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    print("============================================================")
    print("🧪 MAIN AUTOMATION TEST WITH CORRECT CREDENTIALS")
    print("============================================================")
    
    success = test_main_automation()
    
    print("\n============================================================")
    if success:
        print("🎉 MAIN AUTOMATION TEST PASSED")
        print("✅ Password filling and automation working correctly!")
    else:
        print("❌ MAIN AUTOMATION TEST FAILED")
        print("💡 Check the detailed logs above for troubleshooting")
    print("============================================================")