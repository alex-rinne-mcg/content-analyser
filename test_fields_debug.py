#!/usr/bin/env python3
"""Debug field errors"""

import urllib.request
import json
import ssl

page_id = "185121598021398"
page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Test with minimal fields and get full error
print("Testing with minimal fields and getting full error...")
fields = "id,message,created_time"
url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&limit=2&access_token={page_token}"

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"✅ SUCCESS: {len(posts)} posts retrieved")
        if posts:
            print(f"   First post: {posts[0].get('id')}")
except urllib.error.HTTPError as e:
    error_data = json.loads(e.read().decode())
    error = error_data.get('error', {})
    print(f"❌ ERROR {e.code}:")
    print(f"   Message: {error.get('message', 'N/A')}")
    print(f"   Type: {error.get('type', 'N/A')}")
    print(f"   Code: {error.get('code', 'N/A')}")
    print(f"   Error Subcode: {error.get('error_subcode', 'N/A')}")
    if 'fbtrace_id' in error:
        print(f"   Trace ID: {error.get('fbtrace_id', 'N/A')}")
except Exception as e:
    print(f"❌ ERROR: {e}")


