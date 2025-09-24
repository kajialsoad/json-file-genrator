# Manual Gmail OAuth JSON Generation Guide

## Overview
This guide will help you manually create OAuth JSON credentials for Gmail accounts when automation scripts face issues.

## Prerequisites
- Gmail account credentials
- Access to Google Cloud Console
- Web browser

## Step-by-Step Process

### Step 1: Login to Google Cloud Console
1. Open your web browser
2. Go to: https://console.cloud.google.com/
3. Login with your Gmail account: `nilamb010@gmail.com`
4. Enter password: `,lkjghf9854`

### Step 2: Create a New Project
1. Click on the project dropdown (top left, next to "Google Cloud")
2. Click "NEW PROJECT"
3. Enter project name: `Gmail-OAuth-nilamb010-[timestamp]`
4. Click "CREATE"
5. Wait for project creation to complete
6. Select the newly created project

### Step 3: Enable Gmail API
1. In the left sidebar, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on "Gmail API" from the results
4. Click "ENABLE"
5. Wait for the API to be enabled

### Step 4: Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" user type
3. Click "CREATE"
4. Fill in the required fields:
   - App name: `Gmail OAuth App`
   - User support email: `nilamb010@gmail.com`
   - Developer contact information: `nilamb010@gmail.com`
5. Click "SAVE AND CONTINUE"
6. On Scopes page, click "ADD OR REMOVE SCOPES"
7. Add these scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.modify`
8. Click "UPDATE" then "SAVE AND CONTINUE"
9. On Test users page, add: `nilamb010@gmail.com`
10. Click "SAVE AND CONTINUE"
11. Review and click "BACK TO DASHBOARD"

### Step 5: Create OAuth Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" > "OAuth client ID"
3. Select application type: "Desktop application"
4. Name: `Gmail OAuth Client`
5. Click "CREATE"
6. A popup will show your Client ID and Client Secret
7. Click "DOWNLOAD JSON"
8. Save the file as: `gmail_oauth_nilamb010.json`

### Step 6: Verify JSON File
The downloaded JSON file should contain:
```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Important Notes
- Keep the JSON file secure and never share it publicly
- The project name should be unique
- Make sure to enable the Gmail API before creating credentials
- The OAuth consent screen must be configured before creating credentials

## Troubleshooting
- If you get "Project creation failed", try a different project name
- If Gmail API is not found, make sure you're in the correct project
- If OAuth consent screen shows errors, ensure all required fields are filled
- If credential creation fails, verify that OAuth consent screen is properly configured

## Next Steps
Once you have the JSON file:
1. Place it in your project directory
2. Use it with your Gmail automation scripts
3. The first time you use it, you'll need to authorize the application in your browser

## Security Reminder
- Never commit OAuth JSON files to version control
- Store them securely
- Regenerate credentials if compromised