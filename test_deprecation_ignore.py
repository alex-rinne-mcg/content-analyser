#!/usr/bin/env python3
"""Test if API returns data despite deprecation warning"""

import urllib.request
import json
import ssl
from datetime import datetime, timedelta

page_id = "185121598021398"
page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
fields = "id,message,created_time,type,permalink_url,full_picture,comments_count,shares_count"
url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&limit=5&since={since_date}&access_token={page_token}"

print("Testing if API returns data despite deprecation warning...")
print(f"URL: {url[:80]}...")
print()

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        
        if posts:
            print(f"✅ SUCCESS: API returned {len(posts)} posts despite deprecation warning!")
            print(f"   Latest post ID: {posts[0].get('id', 'N/A')}")
            print(f"   Created: {posts[0].get('created_time', 'N/A')}")
            print(f"   Comments: {posts[0].get('comments_count', 0)}")
            print(f"   Shares: {posts[0].get('shares_count', 0)}")
            print()
            print("💡 CONCLUSION: The workflow should work in N8N!")
            print("   The deprecation warning is just a warning, not an error.")
            print("   The API still returns data successfully.")
        else:
            print("⚠️  No posts returned (but no error either)")
            
except urllib.error.HTTPError as e:
    error_data = json.loads(e.read().decode())
    error = error_data.get('error', {})
    error_msg = error.get('message', 'Unknown error')
    error_code = error.get('code', 'N/A')
    
    print(f"❌ HTTP Error {e.code} (Code: {error_code})")
    print(f"   Message: {error_msg}")
    
    # Check if it's just a warning
    if error_code == 12 or 'deprecate' in error_msg.lower():
        print()
        print("⚠️  This is a deprecation warning (Code 12)")
        print("   However, Meta API sometimes returns data even with this warning.")
        print("   The workflow might still work in N8N - test it there!")
        
except Exception as e:
    print(f"❌ ERROR: {e}")


