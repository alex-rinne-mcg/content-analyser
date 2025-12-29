#!/usr/bin/env python3
"""
Test script to validate Meta API credential
This script tests if the access token can successfully authenticate with Meta Graph API
"""

import urllib.request
import urllib.parse
import json
import sys

def test_meta_api():
    """
    Test Meta Graph API access with a simple request
    """
    # Page ID from the workflow
    page_id = "185121598021398"
    
    # Base URL for Meta Graph API
    base_url = f"https://graph.facebook.com/v18.0/{page_id}"
    
    print("🔍 Testing Meta API Credential...")
    print(f"📄 Page ID: {page_id}")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Test 1: Get page info (simplest request)
    print("Test 1: Getting page info...")
    test_url = f"{base_url}?fields=id,name"
    
    # Note: In a real scenario, you would need to get the token from N8N
    # For now, we'll show what the request should look like
    print(f"   URL: {test_url}")
    print("   Headers: Authorization: Bearer YOUR_ACCESS_TOKEN")
    print()
    
    # Instructions for manual testing
    print("=" * 60)
    print("MANUAL TEST INSTRUCTIONS:")
    print("=" * 60)
    print()
    print("1. Get your access token from the N8N credential:")
    print("   - Go to: https://alexrinne.app.n8n.cloud/home/credentials/bi3V9te2bqwQGzgC")
    print("   - Open 'meta-api-token' credential")
    print("   - Copy the Value (should start with 'Bearer ')")
    print()
    print("2. Test the token using curl:")
    print(f"   curl -H 'Authorization: Bearer YOUR_TOKEN' '{test_url}'")
    print()
    print("3. Or test in browser console:")
    print(f"   fetch('{test_url}', {{")
    print("     headers: { 'Authorization': 'Bearer YOUR_TOKEN' }")
    print("   }).then(r => r.json()).then(console.log)")
    print()
    print("4. Expected successful response:")
    print('   {"id": "185121598021398", "name": "Your Page Name"}')
    print()
    print("5. If you get an error:")
    print("   - Check if token starts with 'Bearer ' (with space)")
    print("   - Verify token is not expired")
    print("   - Ensure token has 'pages_read_engagement' permission")
    print()
    
    # Alternative: Test via N8N workflow execution
    print("=" * 60)
    print("ALTERNATIVE: Test via N8N Workflow")
    print("=" * 60)
    print()
    print("You can also test by executing just the 'Fetch Posts' node:")
    print("1. Open workflow: https://alexrinne.app.n8n.cloud/workflow/FOanQ6fVJVYw5jAG")
    print("2. Click on 'Fetch Posts' node")
    print("3. Click 'Execute Node' button")
    print("4. Check the output for errors")
    print()

if __name__ == "__main__":
    test_meta_api()


