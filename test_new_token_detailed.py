#!/usr/bin/env python3
"""
Detailed test of the new Meta API token to understand why API calls fail
even though pages_read_user_content permission is granted
"""

import urllib.request
import urllib.parse
import json
import sys
import ssl

def test_token_detailed(token):
    """
    Detailed test of token capabilities
    """
    page_id = "185121598021398"
    
    print("=" * 70)
    print("🔍 DETAILED TOKEN TEST")
    print("=" * 70)
    print()
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # First, check token info
    print("1️⃣  TOKEN DEBUG INFO:")
    print("-" * 70)
    debug_url = f"https://graph.facebook.com/v21.0/debug_token?input_token={token}&access_token={token}"
    try:
        req = urllib.request.Request(debug_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            token_info = data.get('data', {})
            print(f"   Type: {token_info.get('type', 'Unknown')}")
            print(f"   App ID: {token_info.get('app_id', 'Unknown')}")
            print(f"   User ID: {token_info.get('user_id', 'Unknown')}")
            print(f"   Page ID: {token_info.get('page_id', 'N/A')}")
            print(f"   Scopes: {', '.join(token_info.get('scopes', []))}")
            print()
            
            # Check if it's a Page Access Token
            if token_info.get('page_id'):
                print("   ✅ This is a Page Access Token")
            else:
                print("   ⚠️  This is NOT a Page Access Token (might be System User token)")
                print("   💡 For posts, we might need to exchange for Page Access Token")
            print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    # Test 2: Try to get page access tokens from the system user token
    print("2️⃣  ATTEMPTING TO GET PAGE ACCESS TOKEN:")
    print("-" * 70)
    try:
        # Try to get page access tokens
        pages_url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={token}"
        req = urllib.request.Request(pages_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            pages = data.get('data', [])
            if pages:
                print(f"   ✅ Found {len(pages)} page(s)")
                for page in pages:
                    print(f"      - {page.get('name', 'N/A')} (ID: {page.get('id', 'N/A')})")
                    page_token = page.get('access_token', '')
                    if page_token:
                        print(f"        Page Access Token: {page_token[:20]}...")
                        print()
                        print("   🧪 Testing with Page Access Token...")
                        # Test posts with page token
                        posts_url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id,message,created_time&limit=1&access_token={page_token}"
                        try:
                            req2 = urllib.request.Request(posts_url)
                            with urllib.request.urlopen(req2, context=ssl_context) as response2:
                                data2 = json.loads(response2.read().decode())
                                posts = data2.get('data', [])
                                print(f"      ✅ SUCCESS: Retrieved {len(posts)} post(s) with Page Access Token!")
                                if posts:
                                    print(f"         Latest post: {posts[0].get('id', 'N/A')}")
                        except Exception as e:
                            print(f"      ❌ FAILED with Page Access Token: {e}")
            else:
                print("   ⚠️  No pages found (this might be expected for System User token)")
    except Exception as e:
        print(f"   ⚠️  Could not get page access tokens: {e}")
        print("   💡 This is expected if the token doesn't have pages_show_list or if it's already a Page Access Token")
    print()
    
    # Test 3: Try posts with system user token directly
    print("3️⃣  TESTING POSTS WITH SYSTEM USER TOKEN:")
    print("-" * 70)
    posts_url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id,message,created_time&limit=1&access_token={token}"
    try:
        req = urllib.request.Request(posts_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            posts = data.get('data', [])
            print(f"   ✅ SUCCESS: Retrieved {len(posts)} post(s) with System User Token!")
            if posts:
                print(f"      Latest post: {posts[0].get('id', 'N/A')}")
                print(f"      Created: {posts[0].get('created_time', 'N/A')}")
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        error = error_data.get('error', {})
        print(f"   ❌ FAILED: {error.get('message', 'Unknown error')}")
        print(f"      Code: {error.get('code', 'N/A')}")
        print(f"      Type: {error.get('type', 'N/A')}")
        if 'error_subcode' in error:
            print(f"      Subcode: {error.get('error_subcode')}")
        print()
        print("   💡 Possible solutions:")
        print("      1. Exchange System User token for Page Access Token")
        print("      2. Use the Page Access Token from /me/accounts endpoint")
        print("      3. Check if page permissions are correctly assigned in Business Manager")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    print()
    
    # Test 4: Try insights
    print("4️⃣  TESTING INSIGHTS:")
    print("-" * 70)
    insights_url = f"https://graph.facebook.com/v21.0/{page_id}/insights?metric=page_fans&period=day&access_token={token}"
    try:
        req = urllib.request.Request(insights_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            insights = data.get('data', [])
            print(f"   ✅ SUCCESS: Retrieved {len(insights)} insight metric(s)")
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        error = error_data.get('error', {})
        print(f"   ❌ FAILED: {error.get('message', 'Unknown error')}")
        print(f"      Code: {error.get('code', 'N/A')}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    print()
    
    print("=" * 70)
    print("✅ Test complete!")
    print("=" * 70)

if __name__ == "__main__":
    token = "EAAyk1ciX1SsBQQNwiMsZBhr1v1pHdQuxkPNZCZC8b6rtipavM0dWxFXiwiHjOg1rDuD29ekMWy6Q3CZBpT4YMbR3hdxqphlZBO9Cc30FoREcFSZC9WmIEtT99ZBTI9znqYPqJcUAOd5f9I3GZADCCqYmUWO3n7RJHqFEKvIp82AdLqUcvFJywEN2gp2SJ63GZB4YvzHxzE0rVxCsmB1kP9ZBaW9Ylb2rOt8um03zoi"
    
    if len(sys.argv) > 1:
        token = sys.argv[1]
    
    test_token_detailed(token)


