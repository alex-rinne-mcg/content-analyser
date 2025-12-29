#!/usr/bin/env python3
"""
Check the permissions of the current Meta API token
This script uses the debug_token endpoint to inspect token permissions
"""

import urllib.request
import urllib.parse
import json
import sys
import ssl

def check_token_permissions(token):
    """
    Check token permissions using Meta Graph API debug_token endpoint
    """
    page_id = "185121598021398"
    
    print("=" * 70)
    print("🔍 Checking Meta API Token Permissions")
    print("=" * 70)
    print()
    
    # Use debug_token endpoint to inspect the token
    debug_url = f"https://graph.facebook.com/v21.0/debug_token?input_token={token}&access_token={token}"
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(debug_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            token_info = data.get('data', {})
            
            print("📋 TOKEN INFORMATION:")
            print("-" * 70)
            print(f"   Token Type:     {token_info.get('type', 'Unknown')}")
            print(f"   App ID:         {token_info.get('app_id', 'Unknown')}")
            print(f"   User ID:        {token_info.get('user_id', 'Unknown')}")
            print(f"   Page ID:        {token_info.get('page_id', 'N/A')}")
            print(f"   Is Valid:       {token_info.get('is_valid', False)}")
            print(f"   Application:    {token_info.get('application', 'Unknown')}")
            
            expires_at = token_info.get('expires_at', 0)
            if expires_at == 0:
                print(f"   Expires At:     Never")
            else:
                from datetime import datetime
                exp_date = datetime.fromtimestamp(expires_at)
                print(f"   Expires At:     {exp_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            print()
            print("🔐 GRANTED PERMISSIONS (Scopes):")
            print("-" * 70)
            scopes = token_info.get('scopes', [])
            
            if not scopes:
                print("   ⚠️  No permissions found!")
            else:
                # Required permissions for the workflow
                required_permissions = [
                    'pages_read_user_content',
                    'pages_read_engagement',
                    'pages_show_list'
                ]
                
                # Check each permission
                for scope in sorted(scopes):
                    status = "✅" if scope in required_permissions else "   "
                    print(f"   {status} {scope}")
                
                print()
                print("📊 PERMISSION STATUS:")
                print("-" * 70)
                
                missing_permissions = []
                for perm in required_permissions:
                    if perm in scopes:
                        print(f"   ✅ {perm} - GRANTED")
                    else:
                        print(f"   ❌ {perm} - MISSING")
                        missing_permissions.append(perm)
                
                if missing_permissions:
                    print()
                    print("⚠️  WARNING: Missing required permissions!")
                    print(f"   Missing: {', '.join(missing_permissions)}")
                    print("   The workflow will not work correctly without these permissions.")
                else:
                    print()
                    print("✅ All required permissions are granted!")
            
            print()
            print("=" * 70)
            
            # Test actual API calls
            print()
            print("🧪 TESTING API CALLS:")
            print("=" * 70)
            
            # Test 1: Get page info
            print()
            print("Test 1: Get Page Info...")
            page_url = f"https://graph.facebook.com/v21.0/{page_id}?fields=id,name&access_token={token}"
            try:
                req = urllib.request.Request(page_url)
                with urllib.request.urlopen(req, context=ssl_context) as response:
                    data = json.loads(response.read().decode())
                    print(f"   ✅ SUCCESS: {data.get('name', 'N/A')} (ID: {data.get('id', 'N/A')})")
            except Exception as e:
                print(f"   ❌ FAILED: {str(e)}")
            
            # Test 2: Get posts (requires pages_read_user_content)
            print()
            print("Test 2: Get Page Posts...")
            posts_url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id,message,created_time&limit=1&access_token={token}"
            try:
                req = urllib.request.Request(posts_url)
                with urllib.request.urlopen(req, context=ssl_context) as response:
                    data = json.loads(response.read().decode())
                    posts = data.get('data', [])
                    if posts:
                        print(f"   ✅ SUCCESS: Retrieved {len(posts)} post(s)")
                    else:
                        print(f"   ⚠️  No posts found (but API call succeeded)")
            except urllib.error.HTTPError as e:
                error_data = json.loads(e.read().decode())
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                print(f"   ❌ FAILED: {error_msg}")
                if 'pages_read_user_content' not in scopes:
                    print(f"   💡 This is expected - missing 'pages_read_user_content' permission")
            except Exception as e:
                print(f"   ❌ FAILED: {str(e)}")
            
            # Test 3: Get insights (requires pages_read_engagement)
            print()
            print("Test 3: Get Page Insights...")
            insights_url = f"https://graph.facebook.com/v21.0/{page_id}/insights?metric=page_fans&period=day&access_token={token}"
            try:
                req = urllib.request.Request(insights_url)
                with urllib.request.urlopen(req, context=ssl_context) as response:
                    data = json.loads(response.read().decode())
                    insights = data.get('data', [])
                    print(f"   ✅ SUCCESS: Retrieved {len(insights)} insight metric(s)")
            except urllib.error.HTTPError as e:
                error_data = json.loads(e.read().decode())
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                print(f"   ❌ FAILED: {error_msg}")
                if 'pages_read_engagement' not in scopes:
                    print(f"   💡 This is expected - missing 'pages_read_engagement' permission")
            except Exception as e:
                print(f"   ❌ FAILED: {str(e)}")
            
            print()
            print("=" * 70)
            
            return {
                'valid': token_info.get('is_valid', False),
                'scopes': scopes,
                'missing': missing_permissions if 'missing_permissions' in locals() else []
            }
            
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        print(f"❌ ERROR: HTTP {e.code}")
        print(f"   Message: {error_data.get('error', {}).get('message', 'Unknown error')}")
        print(f"   Type: {error_data.get('error', {}).get('type', 'Unknown')}")
        print(f"   Code: {error_data.get('error', {}).get('code', 'Unknown')}")
        return None
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

if __name__ == "__main__":
    # Token from the previous test (the one currently in N8N)
    # Replace this with your current token if different
    token = "EAAyk1ciX1SsBQTcCyVAN36ZCeIfL7XHkNo5VhKa1ZBWMFPUMvzu8GdAUvH5SjTUBbABc5QKOlhdmMZAzqXCsmn1frgPqc3fegAJzaG4DX60HuLZBVXIiZC5ggdXonbAbub84S8ZAnEG6n1RVbzefsY3BWV3iTKT6vujJKcUvuZCKWjo1ud0BZBdoSjiGZAtIHV8EgIQm6stKhzKHhZAQjWb2ho1kDFEDQwBUZB33FBz"
    
    # If token is provided as command line argument, use that instead
    if len(sys.argv) > 1:
        token = sys.argv[1]
    
    result = check_token_permissions(token)
    
    if result:
        sys.exit(0 if result['valid'] and not result['missing'] else 1)
    else:
        sys.exit(1)


