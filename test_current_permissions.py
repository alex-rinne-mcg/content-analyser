#!/usr/bin/env python3
"""
Test script to determine what's possible with current Meta API permissions
"""

import urllib.request
import urllib.parse
import json
import sys
import ssl

def test_endpoint(name, url, token):
    """Test a specific endpoint and return success status"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url[:80]}...")
    print(f"{'='*60}")
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            print(f"✅ SUCCESS")
            
            # Show sample data
            if isinstance(data, dict):
                if 'data' in data:
                    items = data['data']
                    print(f"   Retrieved {len(items)} items")
                    if items and len(items) > 0:
                        print(f"   Sample: {json.dumps(items[0], indent=2)[:200]}...")
                elif 'name' in data or 'id' in data:
                    print(f"   Data: {json.dumps(data, indent=2)[:200]}...")
                else:
                    print(f"   Response keys: {list(data.keys())[:5]}")
            else:
                print(f"   Response type: {type(data)}")
            
            return True
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        error_info = error_data.get('error', {})
        print(f"❌ FAILED: HTTP {e.code}")
        print(f"   Error: {error_info.get('message', 'Unknown error')}")
        print(f"   Type: {error_info.get('type', 'Unknown')}")
        print(f"   Code: {error_info.get('code', 'Unknown')}")
        if 'error_subcode' in error_info:
            print(f"   Subcode: {error_info.get('error_subcode')}")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def main():
    page_id = "185121598021398"
    token = "EAAyk1ciX1SsBQTcCyVAN36ZCeIfL7XHkNo5VhKa1ZBWMFPUMvzu8GdAUvH5SjTUBbABc5QKOlhdmMZAzqXCsmn1frgPqc3fegAJzaG4DX60HuLZBVXIiZC5ggdXonbAbub84S8ZAnEG6n1RVbzefsY3BWV3iTKT6vujJKcUvuZCKWjo1ud0BZBdoSjiGZAtIHV8EgIQm6stKhzKHhZAQjWb2ho1kDFEDQwBUZB33FBz"
    
    print("🔍 Testing Current Permissions Capabilities")
    print(f"📄 Page ID: {page_id}")
    print(f"🌐 API Version: v21.0")
    
    results = {}
    
    # Test 1: Page Info (should work)
    url = f"https://graph.facebook.com/v21.0/{page_id}?fields=id,name,fan_count&access_token={token}"
    results['Page Info'] = test_endpoint("Page Info", url, token)
    
    # Test 2: Page Posts (what we need - likely fails)
    url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id,created_time,type&limit=5&access_token={token}"
    results['Page Posts'] = test_endpoint("Page Posts", url, token)
    
    # Test 3: Page Insights (should work)
    url = f"https://graph.facebook.com/v21.0/{page_id}/insights?metric=page_fans,page_impressions&period=day&limit=1&access_token={token}"
    results['Page Insights'] = test_endpoint("Page Insights", url, token)
    
    # Test 4: Get a specific post (if we can find one)
    # First try to get posts to find a post ID
    print(f"\n{'='*60}")
    print("Attempting to find a post ID...")
    print(f"{'='*60}")
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Try to get posts with minimal fields
        posts_url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id&limit=1&access_token={token}"
        req = urllib.request.Request(posts_url)
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            posts = data.get('data', [])
            
            if posts:
                post_id = posts[0]['id']
                print(f"✅ Found post ID: {post_id}")
                
                # Test 5: Get specific post details
                url = f"https://graph.facebook.com/v21.0/{post_id}?fields=id,message,created_time,type&access_token={token}"
                results['Post Details'] = test_endpoint("Post Details", url, token)
                
                # Test 6: Get post insights
                url = f"https://graph.facebook.com/v21.0/{post_id}/insights?metric=post_impressions,post_reach&period=lifetime&access_token={token}"
                results['Post Insights'] = test_endpoint("Post Insights", url, token)
            else:
                print("⚠️  No posts found (might be permission issue)")
                results['Post Details'] = None
                results['Post Insights'] = None
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        error_info = error_data.get('error', {})
        print(f"❌ Cannot get posts: {error_info.get('message', 'Unknown error')}")
        results['Post Details'] = None
        results['Post Insights'] = None
    except Exception as e:
        print(f"❌ Error finding posts: {str(e)}")
        results['Post Details'] = None
        results['Post Insights'] = None
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY: What You Can Do With Current Permissions")
    print(f"{'='*60}")
    
    capabilities = []
    limitations = []
    
    if results.get('Page Info'):
        capabilities.append("✅ Get page basic information (name, ID, fan count)")
    else:
        limitations.append("❌ Cannot get page basic information")
    
    if results.get('Page Posts'):
        capabilities.append("✅ Get page posts list")
    else:
        limitations.append("❌ Cannot get page posts (needs pages_read_user_content)")
    
    if results.get('Page Insights'):
        capabilities.append("✅ Get page-level insights (fans, impressions)")
    else:
        limitations.append("❌ Cannot get page-level insights")
    
    if results.get('Post Details'):
        capabilities.append("✅ Get individual post details (message, type, etc.)")
    else:
        limitations.append("❌ Cannot get post details (needs pages_read_user_content)")
    
    if results.get('Post Insights'):
        capabilities.append("✅ Get post-level insights (impressions, reach, engagement)")
    else:
        limitations.append("❌ Cannot get post-level insights")
    
    print("\n✅ CAPABILITIES:")
    for cap in capabilities:
        print(f"   {cap}")
    
    if limitations:
        print("\n❌ LIMITATIONS:")
        for lim in limitations:
            print(f"   {lim}")
    
    print(f"\n{'='*60}")
    print("💡 RECOMMENDATION:")
    if not results.get('Page Posts'):
        print("   Add 'pages_read_user_content' permission to enable:")
        print("   - Reading posts")
        print("   - Getting post details")
        print("   - Accessing post content for analysis")
    else:
        print("   Your current permissions are sufficient for the workflow!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()


