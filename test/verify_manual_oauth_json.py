#!/usr/bin/env python3
"""
Verification script for manually created Gmail OAuth JSON files
"""

import json
import os
import sys
from datetime import datetime

def verify_oauth_json(json_file_path):
    """Verify the structure and content of OAuth JSON file"""
    
    print(f"🔍 Verifying OAuth JSON file: {json_file_path}")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"❌ File not found: {json_file_path}")
        return False
    
    try:
        # Load JSON file
        with open(json_file_path, 'r') as f:
            oauth_data = json.load(f)
        
        print("✅ JSON file loaded successfully")
        
        # Check required structure
        required_keys = ['installed']
        if not all(key in oauth_data for key in required_keys):
            print("❌ Missing 'installed' key in JSON structure")
            return False
        
        installed = oauth_data['installed']
        required_installed_keys = [
            'client_id', 'project_id', 'auth_uri', 'token_uri',
            'auth_provider_x509_cert_url', 'client_secret', 'redirect_uris'
        ]
        
        missing_keys = [key for key in required_installed_keys if key not in installed]
        if missing_keys:
            print(f"❌ Missing required keys in 'installed': {missing_keys}")
            return False
        
        print("✅ All required keys present")
        
        # Verify key values
        if not installed['client_id'].endswith('.apps.googleusercontent.com'):
            print("❌ Invalid client_id format")
            return False
        
        if not installed['auth_uri'] == 'https://accounts.google.com/o/oauth2/auth':
            print("❌ Invalid auth_uri")
            return False
        
        if not installed['token_uri'] == 'https://oauth2.googleapis.com/token':
            print("❌ Invalid token_uri")
            return False
        
        if not installed['client_secret']:
            print("❌ Empty client_secret")
            return False
        
        if not installed['project_id']:
            print("❌ Empty project_id")
            return False
        
        print("✅ All key values are valid")
        
        # Display summary
        print("\n📊 OAuth JSON Summary:")
        print(f"   Project ID: {installed['project_id']}")
        print(f"   Client ID: {installed['client_id'][:20]}...")
        print(f"   Client Secret: {installed['client_secret'][:10]}...")
        print(f"   Redirect URIs: {installed['redirect_uris']}")
        
        print("\n✅ OAuth JSON file is valid and ready to use!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Error verifying file: {e}")
        return False

def main():
    """Main function to verify OAuth JSON files"""
    
    print("🚀 Gmail OAuth JSON Verification Tool")
    print("=" * 60)
    
    # Check for command line argument
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # Look for common OAuth JSON file names
        possible_files = [
            'gmail_oauth_nilamb010.json',
            'credentials.json',
            'oauth_credentials.json',
            'client_secret.json'
        ]
        
        json_file = None
        for file_name in possible_files:
            if os.path.exists(file_name):
                json_file = file_name
                break
        
        if not json_file:
            print("❌ No OAuth JSON file found!")
            print("Please provide the file path as an argument:")
            print("   python verify_manual_oauth_json.py <path_to_json_file>")
            print("\nOr place one of these files in the current directory:")
            for file_name in possible_files:
                print(f"   - {file_name}")
            return False
    
    # Verify the JSON file
    success = verify_oauth_json(json_file)
    
    if success:
        print(f"\n🎉 Success! {json_file} is ready for use with Gmail automation.")
    else:
        print(f"\n❌ Verification failed for {json_file}")
        print("Please check the manual guide and recreate the OAuth credentials.")
    
    return success

if __name__ == "__main__":
    main()