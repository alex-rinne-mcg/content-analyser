#!/usr/bin/env python3
"""
Extract Page Access Token from System User token
This is the token that should be used in N8N
"""

import urllib.request
import json
import ssl
import sys

def extract_page_access_token(system_user_token, page_id="185121598021398"):
    """
    Extract Page Access Token from System User token
    """
    print("=" * 70)
    print("🔑 EXTRACTING PAGE ACCESS TOKEN")
    print("=" * 70)
    print()
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Get page access tokens
    pages_url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={system_user_token}"
    
    try:
        req = urllib.request.Request(pages_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            pages = data.get('data', [])
            
            if not pages:
                print("❌ No pages found!")
                return None
            
            # Find the specific page
            target_page = None
            for page in pages:
                if page.get('id') == page_id:
                    target_page = page
                    break
            
            if not target_page:
                print(f"❌ Page {page_id} not found in accounts!")
                print(f"   Available pages:")
                for page in pages:
                    print(f"      - {page.get('name', 'N/A')} (ID: {page.get('id', 'N/A')})")
                return None
            
            page_token = target_page.get('access_token', '')
            if not page_token:
                print("❌ No access token found for this page!")
                return None
            
            print(f"✅ Found Page Access Token for: {target_page.get('name', 'N/A')}")
            print(f"   Page ID: {target_page.get('id', 'N/A')}")
            print()
            print("=" * 70)
            print("📋 PAGE ACCESS TOKEN (Use this in N8N):")
            print("=" * 70)
            print()
            print(page_token)
            print()
            print("=" * 70)
            print("📝 INSTRUCTIONS FOR N8N:")
            print("=" * 70)
            print()
            print("1. Go to N8N → Credentials → meta-api-token")
            print("2. Update the 'Value' field with:")
            print(f"   Bearer {page_token}")
            print("3. Save the credential")
            print("4. Test the workflow!")
            print()
            print("=" * 70)
            
            # Test the token
            print()
            print("🧪 TESTING PAGE ACCESS TOKEN:")
            print("-" * 70)
            
            # Test posts
            posts_url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id,message,created_time&limit=1&access_token={page_token}"
            try:
                req2 = urllib.request.Request(posts_url)
                with urllib.request.urlopen(req2, context=ssl_context) as response2:
                    data2 = json.loads(response2.read().decode())
                    posts = data2.get('data', [])
                    print(f"✅ Posts API: SUCCESS ({len(posts)} post(s) retrieved)")
            except Exception as e:
                print(f"❌ Posts API: FAILED - {e}")
            
            # Test insights
            insights_url = f"https://graph.facebook.com/v21.0/{page_id}/insights?metric=page_fans&period=day&access_token={page_token}"
            try:
                req3 = urllib.request.Request(insights_url)
                with urllib.request.urlopen(req3, context=ssl_context) as response3:
                    data3 = json.loads(response3.read().decode())
                    insights = data3.get('data', [])
                    print(f"✅ Insights API: SUCCESS ({len(insights)} metric(s) retrieved)")
            except Exception as e:
                print(f"⚠️  Insights API: {e}")
            
            print()
            print("=" * 70)
            print("✅ Token extraction and testing complete!")
            print("=" * 70)
            
            return page_token
            
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"❌ ERROR: {error_data.get('error', {}).get('message', 'Unknown error')}")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    system_user_token = "EAAyk1ciX1SsBQQNwiMsZBhr1v1pHdQuxkPNZCZC8b6rtipavM0dWxFXiwiHjOg1rDuD29ekMWy6Q3CZBpT4YMbR3hdxqphlZBO9Cc30FoREcFSZC9WmIEtT99ZBTI9znqYPqJcUAOd5f9I3GZADCCqYmUWO3n7RJHqFEKvIp82AdLqUcvFJywEN2gp2SJ63GZB4YvzHxzE0rVxCsmB1kP9ZBaW9Ylb2rOt8um03zoi"
    
    if len(sys.argv) > 1:
        system_user_token = sys.argv[1]
    
    extract_page_access_token(system_user_token)


