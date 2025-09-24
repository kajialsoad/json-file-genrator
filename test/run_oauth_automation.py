#!/usr/bin/env python3
"""
Gmail OAuth Automation Runner
Simple interface to run the backend automation
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_accounts_file():
    """Check if accounts file exists and has content"""
    accounts_file = Path("accounts.txt")
    if not accounts_file.exists():
        print("❌ accounts.txt file not found!")
        print("Please create accounts.txt with your Gmail accounts (email:password format)")
        return False
    
    with open(accounts_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not lines:
        print("❌ No accounts found in accounts.txt!")
        print("Please add your Gmail accounts in email:password format")
        return False
    
    print(f"✅ Found {len(lines)} accounts in accounts.txt")
    return True

def main():
    print("🚀 Gmail OAuth Backend Automation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("gmail_oauth_backend_automation.py").exists():
        print("❌ gmail_oauth_backend_automation.py not found!")
        print("Please run this script from the correct directory")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check accounts file
    if not check_accounts_file():
        return
    
    print("\n🎯 Choose automation mode:")
    print("1. Single email test")
    print("2. Bulk processing (all accounts)")
    print("3. Headless mode (background processing)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        email = input("Enter email address: ").strip()
        if email:
            cmd = [sys.executable, "gmail_oauth_backend_automation.py", "--single", email]
            subprocess.run(cmd)
    
    elif choice == "2":
        print("\n🚀 Starting bulk processing...")
        cmd = [sys.executable, "gmail_oauth_backend_automation.py"]
        subprocess.run(cmd)
    
    elif choice == "3":
        print("\n🚀 Starting headless bulk processing...")
        cmd = [sys.executable, "gmail_oauth_backend_automation.py", "--headless"]
        subprocess.run(cmd)
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()