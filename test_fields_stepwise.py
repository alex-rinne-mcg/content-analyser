#!/usr/bin/env python3
"""Add fields step by step to find the problematic one"""

import urllib.request
import json
import ssl

page_id = "185121598021398"
page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

base_fields = "id,message,created_time"
test_fields = [
    ("type", "type"),
    ("permalink_url", "permalink_url"),
    ("full_picture", "full_picture"),
    ("comments_count", "comments_count"),
    ("shares_count", "shares_count"),
]

current_fields = base_fields
print(f"Base fields: {base_fields}")
print()

for field_name, field_value in test_fields:
    test_fields_str = f"{current_fields},{field_value}"
    url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={test_fields_str}&limit=2&access_token={page_token}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            posts = data.get('data', [])
            print(f"✅ {field_name}: Works ({len(posts)} posts)")
            current_fields = test_fields_str
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        error = error_data.get('error', {})
        print(f"❌ {field_name}: FAILED - {error.get('message', 'Unknown')[:60]}")
        break
    except Exception as e:
        print(f"❌ {field_name}: FAILED - {str(e)[:60]}")
        break

print()
print(f"✅ Working fields: {current_fields}")


