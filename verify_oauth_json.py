#!/usr/bin/env python3
"""
Gmail OAuth JSON Verification Script
This script verifies that the downloaded OAuth JSON file is valid and complete.
"""

import json
import os
import sys
from datetime import datetime

def find_oauth_json_files():
    """Find all potential OAuth JSON files in Downloads folder"""
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    
    if not os.path.exists(downloads_dir):
        print(f"❌ Downloads folder not found: {downloads_dir}")
        return []
    
    json_files = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.json'):
            # Check if it's likely an OAuth file
            if any(keyword in filename.lower() for keyword in ['client', 'oauth', 'gmail', 'credentials']):
                json_files.append(os.path.join(downloads_dir, filename))
    
    return json_files

def verify_oauth_json(file_path):
    """Verify that the JSON file has the correct OAuth structure"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"📁 Checking file: {os.path.basename(file_path)}")
        print(f"📅 File size: {os.path.getsize(file_path)} bytes")
        print(f"🕒 Modified: {datetime.fromtimestamp(os.path.getmtime(file_path))}")
        
        # Check for 'installed' key (Desktop application)
        if 'installed' in data:
            client_info = data['installed']
            print("✅ Found 'installed' configuration (Desktop application)")
            
            # Required fields for OAuth
            required_fields = [
                'client_id',
                'client_secret', 
                'auth_uri',
                'token_uri',
                'auth_provider_x509_cert_url'
            ]
            
            missing_fields = []
            present_fields = []
            
            for field in required_fields:
                if field in client_info:
                    present_fields.append(field)
                else:
                    missing_fields.append(field)
            
            print(f"✅ Present fields: {len(present_fields)}/{len(required_fields)}")
            for field in present_fields:
                if field == 'client_id':
                    print(f"   🔑 {field}: {client_info[field][:20]}...{client_info[field][-10:]}")
                elif field == 'client_secret':
                    print(f"   🔐 {field}: {client_info[field][:10]}...{client_info[field][-5:]}")
                else:
                    print(f"   ✓ {field}: {client_info[field]}")
            
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
                return False
            
            # Additional checks
            if 'redirect_uris' in client_info:
                print(f"✅ Redirect URIs: {len(client_info['redirect_uris'])} configured")
            
            print("🎉 OAuth JSON file is VALID and ready to use!")
            return True
            
        # Check for 'web' key (Web application)
        elif 'web' in data:
            print("⚠️  Found 'web' configuration - this is for web applications")
            print("   For desktop applications, you need 'installed' type credentials")
            return False
            
        else:
            print("❌ Invalid JSON structure - neither 'installed' nor 'web' key found")
            print("   Available keys:", list(data.keys()))
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Gmail OAuth JSON Verification Tool")
    print("=" * 50)
    
    # Find potential OAuth JSON files
    json_files = find_oauth_json_files()
    
    if not json_files:
        print("❌ No OAuth JSON files found in Downloads folder")
        print("\n💡 Make sure you have:")
        print("   1. Downloaded the OAuth credentials JSON file")
        print("   2. Saved it to your Downloads folder")
        print("   3. The filename contains 'client', 'oauth', 'gmail', or 'credentials'")
        return False
    
    print(f"📋 Found {len(json_files)} potential OAuth JSON file(s):")
    
    valid_files = []
    for i, file_path in enumerate(json_files, 1):
        print(f"\n--- File {i} ---")
        if verify_oauth_json(file_path):
            valid_files.append(file_path)
        print()
    
    if valid_files:
        print("🎉 VERIFICATION SUCCESSFUL!")
        print(f"✅ {len(valid_files)} valid OAuth JSON file(s) found")
        
        if len(valid_files) == 1:
            print(f"📁 Ready to use: {os.path.basename(valid_files[0])}")
        else:
            print("📁 Valid files:")
            for file_path in valid_files:
                print(f"   - {os.path.basename(file_path)}")
        
        print("\n🚀 Next steps:")
        print("   1. Use this JSON file in your Gmail API application")
        print("   2. Keep the file secure and don't share it publicly")
        print("   3. You can now authenticate with Gmail API")
        
        return True
    else:
        print("❌ VERIFICATION FAILED!")
        print("   No valid OAuth JSON files found")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you downloaded the correct file type (Desktop application)")
        print("   2. Check that the file isn't corrupted")
        print("   3. Verify you completed all OAuth setup steps")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)