#!/usr/bin/env python3
"""
Playwright-based Gmail OAuth Automation
More reliable than Selenium for modern web automation
Supports bulk processing for multiple email accounts
"""

import json
import time
import os
from datetime import datetime
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('playwright_oauth_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PlaywrightGmailOAuthAutomation:
    def __init__(self):
        self.results = {}
        self.current_email = None
        self.current_password = None
        
    def load_accounts(self, accounts_file: str = "accounts.txt") -> List[Dict[str, str]]:
        """Load email accounts from file"""
        accounts = []
        try:
            with open(accounts_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        email, password = line.split(':', 1)
                        accounts.append({
                            'email': email.strip(),
                            'password': password.strip()
                        })
            logger.info(f"Loaded {len(accounts)} accounts from {accounts_file}")
            return accounts
        except FileNotFoundError:
            logger.error(f"Accounts file {accounts_file} not found")
            return []
        except Exception as e:
            logger.error(f"Error loading accounts: {e}")
            return []
    
    def save_results(self, email: str, success: bool = False, error: str = None, 
                    json_file: str = None, steps_completed: List[str] = None):
        """Save automation results"""
        timestamp = int(time.time())
        result_data = {
            'email': email,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'success': success,
            'error': error,
            'json_file': json_file,
            'steps_completed': steps_completed or [],
            'automation_type': 'playwright'
        }
        
        filename = f"playwright_oauth_results_{email.replace('@', '_').replace('.', '_')}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(result_data, f, indent=2)
            logger.info(f"Results saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return None
    
    def create_project_name(self, email: str) -> str:
        """Generate unique project name"""
        timestamp = int(time.time())
        clean_email = email.split('@')[0]
        return f"Gmail-OAuth-{clean_email}-{timestamp}"
    
    def wait_for_manual_input(self, message: str, timeout: int = 300) -> bool:
        """Wait for user to complete manual step"""
        logger.info(f"MANUAL STEP REQUIRED: {message}")
        print(f"\n{'='*60}")
        print(f"MANUAL STEP REQUIRED:")
        print(f"{message}")
        print(f"Press ENTER when completed (timeout: {timeout} seconds)")
        print(f"{'='*60}")
        
        try:
            # Wait for user input with timeout
            import select
            import sys
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                    input()
                    return True
                time.sleep(1)
            
            logger.warning("Manual step timed out")
            return False
        except:
            # Fallback for Windows
            try:
                input()
                return True
            except:
                return False
    
    def process_single_email(self, email: str, password: str) -> Dict[str, Any]:
        """Process single email account using Playwright MCP tools"""
        logger.info(f"Starting OAuth automation for {email}")
        
        self.current_email = email
        self.current_password = password
        steps_completed = []
        
        try:
            # Step 1: Navigate to Google Cloud Console
            logger.info("Step 1: Navigating to Google Cloud Console")
            
            # This will be implemented using Playwright MCP tools
            # For now, return a structured result that can be extended
            
            result = {
                'success': False,
                'email': email,
                'steps_completed': steps_completed,
                'error': 'Playwright automation implementation in progress',
                'json_file': None
            }
            
            # Save results
            self.save_results(
                email=email,
                success=result['success'],
                error=result['error'],
                steps_completed=steps_completed
            )
            
            return result
            
        except Exception as e:
            error_msg = f"Automation failed for {email}: {str(e)}"
            logger.error(error_msg)
            
            self.save_results(
                email=email,
                success=False,
                error=error_msg,
                steps_completed=steps_completed
            )
            
            return {
                'success': False,
                'email': email,
                'error': error_msg,
                'steps_completed': steps_completed
            }
    
    def process_bulk_emails(self, accounts_file: str = "accounts.txt", 
                          max_concurrent: int = 1) -> Dict[str, Any]:
        """Process multiple email accounts"""
        logger.info("Starting bulk email processing")
        
        accounts = self.load_accounts(accounts_file)
        if not accounts:
            return {'success': False, 'error': 'No accounts loaded'}
        
        results = {
            'total_accounts': len(accounts),
            'successful': 0,
            'failed': 0,
            'results': [],
            'start_time': datetime.now().isoformat()
        }
        
        for i, account in enumerate(accounts, 1):
            logger.info(f"Processing account {i}/{len(accounts)}: {account['email']}")
            
            result = self.process_single_email(account['email'], account['password'])
            results['results'].append(result)
            
            if result['success']:
                results['successful'] += 1
            else:
                results['failed'] += 1
            
            # Add delay between accounts to avoid rate limiting
            if i < len(accounts):
                time.sleep(5)
        
        results['end_time'] = datetime.now().isoformat()
        
        # Save bulk results
        timestamp = int(time.time())
        bulk_filename = f"bulk_oauth_results_{timestamp}.json"
        
        try:
            with open(bulk_filename, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Bulk results saved to {bulk_filename}")
        except Exception as e:
            logger.error(f"Error saving bulk results: {e}")
        
        return results

def main():
    """Main function for testing"""
    automation = PlaywrightGmailOAuthAutomation()
    
    # Test with single account first
    test_accounts = automation.load_accounts("accounts.txt")
    
    if test_accounts:
        logger.info("Testing with first account...")
        first_account = test_accounts[0]
        result = automation.process_single_email(
            first_account['email'], 
            first_account['password']
        )
        
        print(f"\nTest Result:")
        print(f"Email: {result['email']}")
        print(f"Success: {result['success']}")
        print(f"Error: {result.get('error', 'None')}")
        print(f"Steps completed: {result.get('steps_completed', [])}")
    else:
        logger.error("No test accounts available")

if __name__ == "__main__":
    main()