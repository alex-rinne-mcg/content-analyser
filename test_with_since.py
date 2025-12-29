#!/usr/bin/env python3
"""Test with since parameter"""

import urllib.request
import json
import ssl
from datetime import datetime, timedelta

page_id = "185121598021398"
page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Calculate since (30 days ago)
since_date = datetime.now() - timedelta(days=30)
since_timestamp = int(since_date.timestamp())

print(f"Testing with since parameter (30 days ago, timestamp: {since_timestamp})...")
print()

# Test 1: Without since
print("Test 1: Without since parameter")
fields = "id,message,created_time,type,permalink_url,comments_count,shares_count"
url1 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&limit=5&access_token={page_token}"
try:
    req = urllib.request.Request(url1)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 2: With since (timestamp)
print("\nTest 2: With since (timestamp)")
url2 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&since={since_timestamp}&limit=5&access_token={page_token}"
try:
    req = urllib.request.Request(url2)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except urllib.error.HTTPError as e:
    error_data = json.loads(e.read().decode())
    error = error_data.get('error', {})
    print(f"   ❌ FAILED: {error.get('message', 'Unknown error')}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 3: With since and until
print("\nTest 3: With since and until")
until_timestamp = int(datetime.now().timestamp())
url3 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&since={since_timestamp}&until={until_timestamp}&limit=5&access_token={page_token}"
try:
    req = urllib.request.Request(url3)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except urllib.error.HTTPError as e:
    error_data = json.loads(e.read().decode())
    error = error_data.get('error', {})
    print(f"   ❌ FAILED: {error.get('message', 'Unknown error')}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 4: With full fields (as in workflow)
print("\nTest 4: With full fields (as in workflow)")
fields_full = "id,message,created_time,type,permalink_url,full_picture,comments_count,shares_count,attachments{media_type,subattachments{media_type,media{image{src}}}}"
url4 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields_full}&since={since_timestamp}&limit=5&access_token={page_token}"
try:
    req = urllib.request.Request(url4)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except urllib.error.HTTPError as e:
    error_data = json.loads(e.read().decode())
    error = error_data.get('error', {})
    print(f"   ❌ FAILED: {error.get('message', 'Unknown error')}")
    if 'deprecate' in error.get('message', '').lower():
        print(f"   ⚠️  This is a deprecation warning - API might still work but warns about deprecated fields")
except Exception as e:
    print(f"   ❌ FAILED: {e}")


