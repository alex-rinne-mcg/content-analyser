#!/usr/bin/env python3
"""Final test - find working combination"""

import urllib.request
import json
import ssl

page_id = "185121598021398"
page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Test: Without since, with all fields we need
fields = "id,message,created_time,type,permalink_url,full_picture,comments_count,shares_count"
url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&limit=5&access_token={page_token}"

print("Testing without 'since' parameter...")
print()

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        posts = data.get('data', [])
        
        print(f"✅ SUCCESS: Retrieved {len(posts)} posts!")
        if posts:
            print(f"   Latest post:")
            print(f"      ID: {posts[0].get('id', 'N/A')}")
            print(f"      Created: {posts[0].get('created_time', 'N/A')}")
            print(f"      Type: {posts[0].get('type', 'N/A')}")
            print(f"      Comments: {posts[0].get('comments_count', 0)}")
            print(f"      Shares: {posts[0].get('shares_count', 0)}")
            print()
            print("💡 SOLUTION: Remove 'since' parameter or use date filtering in N8N code node")
            print("   The workflow can fetch all posts and filter by date in the code node")
            
except Exception as e:
    print(f"❌ FAILED: {e}")


