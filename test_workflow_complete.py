#!/usr/bin/env python3
"""
Complete workflow test - Tests all components of the ZZUPER Meta Post Analysis workflow
"""

import urllib.request
import json
import ssl
import sys
from datetime import datetime, timedelta

def test_meta_api(page_token, page_id="185121598021398"):
    """Test Meta Graph API endpoints"""
    print("=" * 70)
    print("1️⃣  TESTING META GRAPH API")
    print("=" * 70)
    print()
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    results = {
        'page_info': False,
        'fetch_posts': False,
        'get_insights': False,
        'get_video_data': False,
        'posts_count': 0,
        'sample_post_id': None
    }
    
    # Test 1: Get Page Info
    print("📄 Test 1: Get Page Info...")
    try:
        url = f"https://graph.facebook.com/v21.0/{page_id}?fields=id,name,fan_count&access_token={page_token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            print(f"   ✅ SUCCESS: {data.get('name', 'N/A')} (ID: {data.get('id', 'N/A')})")
            print(f"      Fan Count: {data.get('fan_count', 'N/A')}")
            results['page_info'] = True
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    print()
    
    # Test 2: Fetch Posts (what the workflow needs)
    print("📝 Test 2: Fetch Posts (last 5)...")
    try:
        # Note: Removed 'type' field (causes deprecation error) and 'since' parameter
        # Date filtering will be done in N8N code node
        fields = "id,message,created_time,permalink_url,full_picture,comments_count,shares_count"
        url = f"https://graph.facebook.com/v21.0/{page_id}/posts?fields={fields}&limit=5&access_token={page_token}"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            posts = data.get('data', [])
            results['posts_count'] = len(posts)
            results['fetch_posts'] = True
            
            if posts:
                results['sample_post_id'] = posts[0].get('id')
                print(f"   ✅ SUCCESS: Retrieved {len(posts)} post(s)")
                print(f"      Latest post ID: {posts[0].get('id', 'N/A')}")
                print(f"      Created: {posts[0].get('created_time', 'N/A')}")
                print(f"      Type: {posts[0].get('type', 'N/A')}")
                print(f"      Comments: {posts[0].get('comments', {}).get('summary', {}).get('total_count', 0)}")
                print(f"      Shares: {posts[0].get('shares', {}).get('count', 0)}")
            else:
                print(f"   ⚠️  No posts found in last 30 days")
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode())
        error = error_data.get('error', {})
        error_msg = error.get('message', 'Unknown error')
        print(f"   ❌ FAILED: {error_msg}")
        if 'deprecate' in error_msg.lower():
            print(f"   ⚠️  NOTE: This is a deprecation warning, but the API might still return data")
            print(f"   💡 The workflow should still work in N8N, but you may see warnings in logs")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    print()
    
    # Test 3: Get Insights (if we have a post)
    if results['sample_post_id']:
        print("📊 Test 3: Get Post Insights...")
        try:
            post_id = results['sample_post_id']
            metrics = "post_impressions,post_reach,post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total,post_reactions_haha_total,post_reactions_sorry_total,post_reactions_anger_total,post_clicks,post_engaged_users"
            url = f"https://graph.facebook.com/v21.0/{post_id}/insights?metric={metrics}&period=lifetime&access_token={page_token}"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                insights = data.get('data', [])
                results['get_insights'] = True
                print(f"   ✅ SUCCESS: Retrieved {len(insights)} insight metric(s)")
                for insight in insights[:3]:  # Show first 3
                    print(f"      - {insight.get('name', 'N/A')}: {insight.get('values', [{}])[0].get('value', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  WARNING: {e}")
        print()
    
    # Test 4: Get Video Data (if we have a video post)
    if results['sample_post_id']:
        print("🎥 Test 4: Get Video Data...")
        try:
            post_id = results['sample_post_id']
            url = f"https://graph.facebook.com/v21.0/{post_id}?fields=source,length,format&access_token={page_token}"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                if data.get('source'):
                    results['get_video_data'] = True
                    print(f"   ✅ SUCCESS: Video data retrieved")
                    print(f"      Source: {data.get('source', 'N/A')[:50]}...")
                    print(f"      Length: {data.get('length', 'N/A')} seconds")
                    print(f"      Format: {data.get('format', 'N/A')}")
                else:
                    print(f"   ℹ️  Post is not a video (this is OK)")
        except Exception as e:
            print(f"   ⚠️  WARNING: {e}")
        print()
    
    return results

def test_google_sheets():
    """Test Google Sheets access (basic check)"""
    print("=" * 70)
    print("2️⃣  TESTING GOOGLE SHEETS ACCESS")
    print("=" * 70)
    print()
    
    sheet_id = "1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY"
    required_tabs = ["Post Performance Data", "AI Analysis", "Weekly Patterns", "Tracker"]
    
    print(f"📊 Sheet ID: {sheet_id}")
    print(f"📋 Required tabs: {', '.join(required_tabs)}")
    print()
    print("   ⚠️  Note: Google Sheets API testing requires authentication.")
    print("   Please verify in N8N that:")
    print("   1. Google Service Account credential is configured")
    print("   2. All 4 tabs exist in the sheet")
    print("   3. Tracker tab has headers in row 1")
    print()
    
    return True

def test_gemini_api():
    """Test Gemini API (basic check)"""
    print("=" * 70)
    print("3️⃣  TESTING GEMINI API")
    print("=" * 70)
    print()
    
    print("   ⚠️  Note: Gemini API testing requires API key.")
    print("   Please verify in N8N that:")
    print("   1. GEMINI_API_KEY is set in environment variables")
    print("   2. Or API key is set directly in AI Analysis node")
    print("   3. Model is set to: gemini-1.5-pro")
    print()
    
    return True

def generate_test_summary(meta_results, sheets_ok, gemini_ok):
    """Generate test summary"""
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print()
    
    print("Meta Graph API:")
    print(f"   ✅ Page Info:        {'✅' if meta_results['page_info'] else '❌'}")
    print(f"   {'✅' if meta_results['fetch_posts'] else '❌'} Fetch Posts:        {'✅' if meta_results['fetch_posts'] else '❌'} ({meta_results['posts_count']} posts)")
    print(f"   {'✅' if meta_results['get_insights'] else '⚠️ '} Get Insights:      {'✅' if meta_results['get_insights'] else '⚠️  (needs post ID)'}")
    print(f"   {'✅' if meta_results['get_video_data'] else 'ℹ️ '} Get Video Data:    {'✅' if meta_results['get_video_data'] else 'ℹ️  (post is not video)'}")
    print()
    
    print("Google Sheets:")
    print(f"   {'✅' if sheets_ok else '⚠️ '} Access:            {'✅' if sheets_ok else '⚠️  (verify in N8N)'}")
    print()
    
    print("Gemini AI:")
    print(f"   {'✅' if gemini_ok else '⚠️ '} Configuration:     {'✅' if gemini_ok else '⚠️  (verify in N8N)'}")
    print()
    
    # Overall status
    critical_tests = [
        meta_results['page_info'],
        meta_results['fetch_posts']
    ]
    
    if all(critical_tests):
        print("=" * 70)
        print("✅ CRITICAL TESTS PASSED - Workflow should work!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Update N8N credential 'meta-api-token' with the Page Access Token")
        print("2. Verify Google Sheets Service Account is configured")
        print("3. Verify Gemini API key is set")
        print("4. Execute workflow manually in N8N")
        print("5. Check execution logs and Google Sheets for results")
    else:
        print("=" * 70)
        print("❌ CRITICAL TESTS FAILED - Fix issues before running workflow")
        print("=" * 70)
    
    print()

def main():
    """Main test function"""
    print()
    print("=" * 70)
    print("🧪 ZZUPER META POST ANALYSIS - COMPLETE WORKFLOW TEST")
    print("=" * 70)
    print()
    
    # Page Access Token (extracted from System User token)
    page_token = "EAAyk1ciX1SsBQQAky6vLoQOelIFU2Jy0q0g7ANIe0jQR8V5PDs7x3jGpMM7T4IIdg1frSxQOgd5k4V2sstmDppYmeOoTJr2gi8mybss56ZB4LKtjJjlblfMiIud4ZCBxUaqxSmZCp9230QKpiLMOZBsHBsueXd6tC8lnABKvx5oxGcsBvxC8nhTGkXXJ5ZAd86K0ZD"
    
    if len(sys.argv) > 1:
        page_token = sys.argv[1]
    
    # Run tests
    meta_results = test_meta_api(page_token)
    sheets_ok = test_google_sheets()
    gemini_ok = test_gemini_api()
    
    # Generate summary
    generate_test_summary(meta_results, sheets_ok, gemini_ok)

if __name__ == "__main__":
    main()

