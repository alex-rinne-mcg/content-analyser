#!/usr/bin/env python3
"""
Script to validate Meta API token by testing various endpoints
"""

import urllib.request
import urllib.parse
import json
import ssl
from datetime import datetime

# Disable SSL verification for testing
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Token to validate
SYSTEM_USER_TOKEN = "EAAyk1ciX1SsBQQNwiMsZBhr1v1pHdQuxkPNZCZC8b6rtipavM0dWxFXiwiHjOg1rDuD29ekMWy6Q3CZBpT4YMbR3hdxqphlZBO9Cc30FoREcFSZC9WmIEtT99ZBTI9znqYPqJcUAOd5f9I3GZADCCqYmUWO3n7RJHqFEKvIp82AdLqUcvFJywEN2gp2SJ63GZB4YvzHxzE0rVxCsmB1kP9ZBaW9Ylb2rOt8um03zoi"
PAGE_ACCESS_TOKEN = "EAAyk1ciX1SsBQduUGqj0UWwQDDpOSRZBj0D8h3Y4y5QYBklpT9j7nQKMUYwtN8ZACuLHKfO9grFeTTVxKRdv6wOZC2cgRpuUINyjrLCKnZBDxSwpEonUwdrUCcuTGyNUXW4ZAsCGTlxsRfMubESqF2hFnZCfnTovQPfZBNhZBWER27gtRBDcaS922pUmQaExkdYBLYwZD"
PAGE_ID = "185121598021398"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def test_token_info():
    """Test token info endpoint"""
    print("=" * 80)
    print("1. Testing Token Info")
    print("=" * 80)
    url = f"{BASE_URL}/debug_token"
    params = {
        "input_token": SYSTEM_USER_TOKEN,
        "access_token": SYSTEM_USER_TOKEN
    }
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            status_code = response.getcode()
            print(f"Status Code: {status_code}")
            data = json.loads(response.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "data" in data:
                token_data = data["data"]
                print(f"\n✅ Token Type: {token_data.get('type', 'Unknown')}")
                print(f"✅ App ID: {token_data.get('app_id', 'Unknown')}")
                print(f"✅ User ID: {token_data.get('user_id', 'Unknown')}")
                print(f"✅ Expires At: {token_data.get('expires_at', 'Unknown')}")
                if token_data.get('expires_at'):
                    expires = datetime.fromtimestamp(token_data['expires_at'])
                    print(f"   (Expires: {expires})")
                print(f"✅ Scopes: {token_data.get('scopes', [])}")
                print(f"✅ Valid: {token_data.get('is_valid', False)}")
            return data
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        try:
            data = json.loads(e.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            return data
        except:
            print(f"❌ Error: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_page_info():
    """Test getting page info"""
    print("\n" + "=" * 80)
    print("2. Testing Page Info")
    print("=" * 80)
    url = f"{BASE_URL}/{PAGE_ID}"
    params = {
        "access_token": SYSTEM_USER_TOKEN,
        "fields": "id,name,access_token"
    }
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            status_code = response.getcode()
            print(f"Status Code: {status_code}")
            data = json.loads(response.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "id" in data:
                print(f"\n✅ Page ID: {data.get('id')}")
                print(f"✅ Page Name: {data.get('name', 'Unknown')}")
                if "access_token" in data:
                    print(f"✅ Page Access Token: {data.get('access_token', 'Not available')[:50]}...")
            return data
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        try:
            data = json.loads(e.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            return data
        except:
            print(f"❌ Error: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_posts():
    """Test getting posts"""
    print("\n" + "=" * 80)
    print("3. Testing Posts Endpoint (with Page Access Token)")
    print("=" * 80)
    url = f"{BASE_URL}/{PAGE_ID}/posts"
    params = {
        "access_token": PAGE_ACCESS_TOKEN,
        "fields": "id,message,created_time,permalink_url,full_picture,comments_count,shares_count",
        "limit": "5"
    }
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            status_code = response.getcode()
            print(f"Status Code: {status_code}")
            data = json.loads(response.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "data" in data:
                posts = data["data"]
                print(f"\n✅ Retrieved {len(posts)} posts")
                if posts:
                    print(f"✅ First post ID: {posts[0].get('id', 'Unknown')}")
            elif "error" in data:
                error = data["error"]
                print(f"\n❌ Error Code: {error.get('code')}")
                print(f"❌ Error Message: {error.get('message')}")
                print(f"❌ Error Type: {error.get('type')}")
                if "error_subcode" in error:
                    print(f"❌ Error Subcode: {error.get('error_subcode')}")
            return data
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        try:
            data = json.loads(e.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            if "error" in data:
                error = data["error"]
                print(f"\n❌ Error Code: {error.get('code')}")
                print(f"❌ Error Message: {error.get('message')}")
                print(f"❌ Error Type: {error.get('type')}")
                if "error_subcode" in error:
                    print(f"❌ Error Subcode: {error.get('error_subcode')}")
            return data
        except:
            print(f"❌ Error: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_insights():
    """Test getting insights"""
    print("\n" + "=" * 80)
    print("4. Testing Insights Endpoint (with Page Access Token)")
    print("=" * 80)
    url = f"{BASE_URL}/{PAGE_ID}/insights"
    params = {
        "access_token": PAGE_ACCESS_TOKEN,
        "metric": "page_impressions",
        "period": "day"
    }
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            status_code = response.getcode()
            print(f"Status Code: {status_code}")
            data = json.loads(response.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "data" in data:
                insights = data["data"]
                print(f"\n✅ Retrieved {len(insights)} insights")
            elif "error" in data:
                error = data["error"]
                print(f"\n❌ Error Code: {error.get('code')}")
                print(f"❌ Error Message: {error.get('message')}")
                print(f"❌ Error Type: {error.get('type')}")
            return data
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        try:
            data = json.loads(e.read().decode())
            print(f"Response: {json.dumps(data, indent=2)}")
            if "error" in data:
                error = data["error"]
                print(f"\n❌ Error Code: {error.get('code')}")
                print(f"❌ Error Message: {error.get('message')}")
                print(f"❌ Error Type: {error.get('type')}")
            return data
        except:
            print(f"❌ Error: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("Meta API Token Validation")
    print("=" * 80)
    print(f"System User Token: {SYSTEM_USER_TOKEN[:50]}...")
    print(f"Page Access Token: {PAGE_ACCESS_TOKEN[:50]}...")
    print(f"Page ID: {PAGE_ID}")
    print(f"API Version: {API_VERSION}")
    print()
    
    # Run tests
    token_info = test_token_info()
    page_info = test_page_info()
    posts = test_posts()
    insights = test_insights()
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if token_info and "data" in token_info:
        token_data = token_info["data"]
        print(f"Token Valid: {token_data.get('is_valid', False)}")
        print(f"Token Type: {token_data.get('type', 'Unknown')}")
        print(f"Scopes: {', '.join(token_data.get('scopes', []))}")
        
        if token_data.get('expires_at'):
            expires = datetime.fromtimestamp(token_data['expires_at'])
            now = datetime.now()
            if expires > now:
                print(f"Token Expires: {expires} (Valid for {expires - now})")
            else:
                print(f"❌ Token Expired: {expires}")
    
    if page_info and "id" in page_info:
        print(f"✅ Page Info: Accessible")
    elif page_info and "error" in page_info:
        print(f"❌ Page Info: {page_info['error'].get('message')}")
    
    if posts and "data" in posts:
        print(f"✅ Posts: Accessible ({len(posts['data'])} posts retrieved)")
    elif posts and "error" in posts:
        print(f"❌ Posts: {posts['error'].get('message')}")
    
    if insights and "data" in insights:
        print(f"✅ Insights: Accessible")
    elif insights and "error" in insights:
        print(f"❌ Insights: {insights['error'].get('message')}")

if __name__ == "__main__":
    main()

