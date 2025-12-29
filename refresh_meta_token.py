#!/usr/bin/env python3
"""
Automatically refresh Meta Page Access Token and update N8N credential
This script:
1. Validates current token
2. Extracts new Page Access Token from System User Token if needed
3. Updates N8N credential automatically
"""

import urllib.request
import urllib.parse
import json
import ssl
import os
from datetime import datetime

# Configuration
SYSTEM_USER_TOKEN = "EAAyk1ciX1SsBQQNwiMsZBhr1v1pHdQuxkPNZCZC8b6rtipavM0dWxFXiwiHjOg1rDuD29ekMWy6Q3CZBpT4YMbR3hdxqphlZBO9Cc30FoREcFSZC9WmIEtT99ZBTI9znqYPqJcUAOd5f9I3GZADCCqYmUWO3n7RJHqFEKvIp82AdLqUcvFJywEN2gp2SJ63GZB4YvzHxzE0rVxCsmB1kP9ZBaW9Ylb2rOt8um03zoi"
PAGE_ID = "185121598021398"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# N8N Configuration (from environment or defaults)
N8N_BASE_URL = os.getenv("N8N_BASE_URL", "https://alexrinne.app.n8n.cloud")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")  # Set this in environment
CREDENTIAL_NAME = "Header Auth account 4"

# Disable SSL verification for testing
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def validate_current_token(page_token):
    """Validate if current Page Access Token is working"""
    print("=" * 80)
    print("🔍 VALIDATING CURRENT TOKEN")
    print("=" * 80)
    
    url = f"{BASE_URL}/{PAGE_ID}/posts"
    params = {
        "access_token": page_token,
        "fields": "id",
        "limit": "1"
    }
    
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
            if "data" in data:
                print("✅ Current token is VALID")
                return True
            elif "error" in data:
                error = data["error"]
                print(f"❌ Current token is INVALID: {error.get('message', 'Unknown error')}")
                return False
    except Exception as e:
        print(f"❌ Error validating token: {e}")
        return False

def extract_page_access_token():
    """Extract Page Access Token from System User Token"""
    print()
    print("=" * 80)
    print("🔑 EXTRACTING NEW PAGE ACCESS TOKEN")
    print("=" * 80)
    
    pages_url = f"{BASE_URL}/me/accounts?access_token={SYSTEM_USER_TOKEN}"
    
    try:
        req = urllib.request.Request(pages_url)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
            pages = data.get('data', [])
            
            if not pages:
                print("❌ No pages found!")
                return None
            
            # Find the specific page
            target_page = None
            for page in pages:
                if page.get('id') == PAGE_ID:
                    target_page = page
                    break
            
            if not target_page:
                print(f"❌ Page {PAGE_ID} not found in accounts!")
                return None
            
            page_token = target_page.get('access_token', '')
            if not page_token:
                print("❌ No access token found for this page!")
                return None
            
            print(f"✅ Successfully extracted Page Access Token")
            print(f"   Page: {target_page.get('name', 'N/A')}")
            print(f"   Token: {page_token[:50]}...")
            
            # Validate the new token
            if validate_current_token(page_token):
                return page_token
            else:
                print("❌ New token validation failed!")
                return None
                
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"❌ ERROR: {error_data.get('error', {}).get('message', 'Unknown error')}")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def get_n8n_credentials():
    """Get all credentials from N8N"""
    if not N8N_API_KEY:
        print("⚠️  N8N_API_KEY not set, skipping N8N update")
        return None
    
    url = f"{N8N_BASE_URL}/api/v1/credentials"
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('data', [])
    except Exception as e:
        print(f"❌ Error fetching N8N credentials: {e}")
        return None

def update_n8n_credential(new_token):
    """Update N8N credential with new token"""
    if not N8N_API_KEY:
        print("⚠️  N8N_API_KEY not set, cannot update N8N credential")
        print(f"   Please manually update '{CREDENTIAL_NAME}' with:")
        print(f"   Bearer {new_token}")
        return False
    
    credentials = get_n8n_credentials()
    if not credentials:
        print("❌ Could not fetch credentials from N8N")
        return False
    
    # Find the credential
    credential = None
    for cred in credentials:
        if cred.get('name') == CREDENTIAL_NAME:
            credential = cred
            break
    
    if not credential:
        print(f"❌ Credential '{CREDENTIAL_NAME}' not found in N8N")
        return False
    
    credential_id = credential.get('id')
    
    # Update credential
    url = f"{N8N_BASE_URL}/api/v1/credentials/{credential_id}"
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Get current credential data and update token
    credential_data = credential.get('data', {})
    credential_data['value'] = f"Bearer {new_token}"
    
    payload = {
        "name": CREDENTIAL_NAME,
        "type": "httpHeaderAuth",
        "data": credential_data
    }
    
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method='PATCH')
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Successfully updated N8N credential '{CREDENTIAL_NAME}'")
            return True
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"❌ Error updating N8N credential: {error_data.get('message', 'Unknown error')}")
        return False
    except Exception as e:
        print(f"❌ Error updating N8N credential: {e}")
        return False

def main():
    print()
    print("=" * 80)
    print("🔄 META TOKEN REFRESH AUTOMATION")
    print("=" * 80)
    print()
    
    # Step 1: Try to get current token from N8N (if API key is set)
    # For now, we'll just extract a new token
    
    # Step 2: Extract new Page Access Token
    new_token = extract_page_access_token()
    
    if not new_token:
        print()
        print("❌ Failed to extract new token. Please check System User Token.")
        return
    
    print()
    print("=" * 80)
    print("📋 NEW PAGE ACCESS TOKEN")
    print("=" * 80)
    print()
    print(f"Token: {new_token}")
    print()
    print(f"Format for N8N: Bearer {new_token}")
    print()
    
    # Step 3: Update N8N credential
    print("=" * 80)
    print("🔄 UPDATING N8N CREDENTIAL")
    print("=" * 80)
    print()
    
    if update_n8n_credential(new_token):
        print()
        print("=" * 80)
        print("✅ TOKEN REFRESH COMPLETE!")
        print("=" * 80)
        print()
        print("The workflow should now work correctly.")
    else:
        print()
        print("=" * 80)
        print("⚠️  MANUAL UPDATE REQUIRED")
        print("=" * 80)
        print()
        print(f"Please manually update the credential '{CREDENTIAL_NAME}' in N8N:")
        print(f"1. Go to N8N → Credentials → {CREDENTIAL_NAME}")
        print(f"2. Update the 'Value' field with: Bearer {new_token}")
        print(f"3. Save the credential")
        print(f"4. Test the workflow")

if __name__ == "__main__":
    main()


