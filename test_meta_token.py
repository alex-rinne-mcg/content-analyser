#!/usr/bin/env python3
"""
Test script to validate Meta API Page Access Token
This script tests if the access token can successfully authenticate with Meta Graph API
"""

import urllib.request
import urllib.parse
import json
import sys
import ssl

def test_meta_api():
    """
    Test Meta Graph API access with a simple request
    """
    # Page ID from the workflow
    page_id = "185121598021398"
    
    # The token provided by the user
    token = "EAAyk1ciX1SsBQTcCyVAN36ZCeIfL7XHkNo5VhKa1ZBWMFPUMvzu8GdAUvH5SjTUBbABc5QKOlhdmMZAzqXCsmn1frgPqc3fegAJzaG4DX60HuLZBVXIiZC5ggdXonbAbub84S8ZAnEG6n1RVbzefsY3BWV3iTKT6vujJKcUvuZCKWjo1ud0BZBdoSjiGZAtIHV8EgIQm6stKhzKHhZAQjWb2ho1kDFEDQwBUZB33FBz"
    
    # Base URL for Meta Graph API
    base_url = f"https://graph.facebook.com/v21.0/{page_id}"
    
    print("🔍 Testing Meta API Page Access Token...")
    print(f"📄 Page ID: {page_id}")
    print(f"🌐 API Version: v21.0")
    print()
    
    # Test 0: Check token permissions
    print("Test 0: Checking token permissions...")
    debug_url = f"https://graph.facebook.com/v21.0/debug_token?input_token={token}&access_token={token}"
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(debug_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            token_info = data.get('data', {})
            print(f"✅ Token type: {token_info.get('type', 'Unknown')}")
            print(f"   App ID: {token_info.get('app_id', 'Unknown')}")
            print(f"   User ID: {token_info.get('user_id', 'Unknown')}")
            print(f"   Scopes: {', '.join(token_info.get('scopes', []))}")
            print(f"   Is valid: {token_info.get('is_valid', False)}")
            print()
    except Exception as e:
        print(f"⚠️  Could not check token info: {str(e)}")
        print()
    
    # Test 1: Get page info (simplest request)
    print("Test 1: Getting page info...")
    test_url = f"{base_url}?fields=id,name&access_token={token}"
    
    try:
        # Create SSL context that doesn't verify certificates (for testing only)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(test_url)
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            print("✅ SUCCESS: Page info retrieved")
            print(f"   Page Name: {data.get('name', 'N/A')}")
            print(f"   Page ID: {data.get('id', 'N/A')}")
            print()
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"❌ FAILED: HTTP {e.code}")
        print(f"   Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
        print(f"   Type: {error_data.get('error', {}).get('type', 'Unknown')}")
        print(f"   Code: {error_data.get('error', {}).get('code', 'Unknown')}")
        if 'error_subcode' in error_data.get('error', {}):
            print(f"   Subcode: {error_data.get('error', {}).get('error_subcode')}")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 2: Get page posts (what the workflow needs)
    print("Test 2: Getting page posts (last 5)...")
    posts_url = f"{base_url}/posts?fields=id,message,created_time,type&limit=5&access_token={token}"
    
    try:
        # Create SSL context that doesn't verify certificates (for testing only)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(posts_url)
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            posts = data.get('data', [])
            print(f"✅ SUCCESS: Retrieved {len(posts)} posts")
            if posts:
                print(f"   Latest post ID: {posts[0].get('id', 'N/A')}")
                print(f"   Latest post date: {posts[0].get('created_time', 'N/A')}")
            print()
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"❌ FAILED: HTTP {e.code}")
        print(f"   Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
        print(f"   Type: {error_data.get('error', {}).get('type', 'Unknown')}")
        print(f"   Code: {error_data.get('error', {}).get('code', 'Unknown')}")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 3: Get page insights (what the workflow needs)
    print("Test 3: Getting page insights...")
    insights_url = f"{base_url}/insights?metric=page_fans&period=day&access_token={token}"
    
    try:
        # Create SSL context that doesn't verify certificates (for testing only)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(insights_url)
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            insights = data.get('data', [])
            print(f"✅ SUCCESS: Retrieved {len(insights)} insight metrics")
            print()
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"⚠️  WARNING: HTTP {e.code}")
        print(f"   Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
        print(f"   Note: This might be expected if the metric requires different permissions")
        print()
    except Exception as e:
        print(f"⚠️  WARNING: {str(e)}")
        print()
    
    print("=" * 60)
    print("✅ Token validation complete!")
    print("   The token appears to be working correctly.")
    print("   If you're still getting errors in N8N, check:")
    print("   1. The URL in the 'Fetch Posts' node uses v21.0")
    print("   2. The header name is 'Authorization' (not 'Autorize')")
    print("   3. The credential is assigned to all Meta API nodes")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_meta_api()
    sys.exit(0 if success else 1)

