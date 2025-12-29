#!/usr/bin/env python3
"""Test different field combinations to find what works"""

import urllib.request
import json
import ssl

page_id = "185121598021398"
page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Test 1: Minimal fields
print("Test 1: Minimal fields")
fields1 = "id,message,created_time,type"
url1 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields1}&limit=2&access_token={page_token}"
try:
    req = urllib.request.Request(url1)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        print(f"   ✅ SUCCESS: {len(data.get('data', []))} posts")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 2: With comments_count and shares_count
print("\nTest 2: With comments_count and shares_count")
fields2 = "id,message,created_time,type,comments_count,shares_count"
url2 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields2}&limit=2&access_token={page_token}"
try:
    req = urllib.request.Request(url2)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
        if posts:
            print(f"      Post 1: comments={posts[0].get('comments_count')}, shares={posts[0].get('shares_count')}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 3: With permalink_url and full_picture
print("\nTest 3: With permalink_url and full_picture")
fields3 = "id,message,created_time,type,permalink_url,full_picture,comments_count,shares_count"
url3 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields3}&limit=2&access_token={page_token}"
try:
    req = urllib.request.Request(url3)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 4: With attachments (the problematic one)
print("\nTest 4: With attachments")
fields4 = "id,message,created_time,type,permalink_url,full_picture,comments_count,shares_count,attachments"
url4 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields4}&limit=2&access_token={page_token}"
try:
    req = urllib.request.Request(url4)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except Exception as e:
    error_msg = str(e)
    if "deprecate" in error_msg.lower():
        print(f"   ⚠️  DEPRECATION WARNING (but might still work)")
    else:
        print(f"   ❌ FAILED: {e}")

# Test 5: With simplified attachments
print("\nTest 5: With simplified attachments")
fields5 = "id,message,created_time,type,permalink_url,full_picture,comments_count,shares_count,attachments{media_type}"
url5 = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields5}&limit=2&access_token={page_token}"
try:
    req = urllib.request.Request(url5)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        print(f"   ✅ SUCCESS: {len(posts)} posts")
except Exception as e:
    error_msg = str(e)
    if "deprecate" in error_msg.lower():
        print(f"   ⚠️  DEPRECATION WARNING (but might still work)")
    else:
        print(f"   ❌ FAILED: {e}")

print("\n" + "="*70)
print("Recommendation: Use fields without attachments or with simplified attachments")


