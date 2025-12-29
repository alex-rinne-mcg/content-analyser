# ZZUPER Meta Post Analysis - N8N Automation

Automated weekly system that analyzes ALL ZZUPER Facebook posts (video and non-video), identifies what drives performance, and generates actionable playbooks using AI.

## Overview

This N8N workflow runs every Monday at 9 AM to:
- Fetch new ZZUPER Facebook posts since last run (30 days on first run)
- Get comprehensive metrics (impressions, reach, reactions, comments, shares, clicks, video stats)
- Calculate performance scores
- AI analyzes ALL posts (video and non-video) for patterns
- Write everything to Google Sheets
- Generate weekly playbook with winning patterns and failures

## Prerequisites

1. **N8N Instance** (self-hosted or cloud)
2. **Meta Graph API Access**
   - Page ID: `185121598021398`
   - Required permissions: `pages_read_engagement`, `pages_show_list`
   - Long-lived access token
3. **Google Gemini API Key**
   - Model: `gemini-1.5-pro`
4. **Google Sheets**
   - Sheet ID: `1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY`
   - Edit access required
   - 4 tabs: `Post Performance Data`, `AI Analysis`, `Weekly Patterns`, `Tracker`

## Setup Instructions

### 1. Import Workflow

1. Open your N8N instance
2. Click **Workflows** → **Import from File**
3. Select `zzuper-meta-analysis-workflow.json`
4. The workflow will be imported with all 17 nodes

### 2. Configure Credentials

#### Meta API Token (HTTP Header Auth)

1. Go to **Credentials** → **New**
2. Select **HTTP Header Auth**
3. Name: `Meta API Token`
4. Configure:
   - **Name**: `Authorization`
   - **Value**: `Bearer YOUR_META_ACCESS_TOKEN`
5. Save

**How to get Meta Access Token:**
- Go to [Meta for Developers](https://developers.facebook.com/)
- Create/select your app
- Generate a long-lived Page Access Token
- Format: `Bearer YOUR_TOKEN_HERE`

#### Google Sheets OAuth2

1. Go to **Credentials** → **New**
2. Select **Google Sheets OAuth2 API**
3. Name: `Google Sheets OAuth2`
4. Follow OAuth2 setup:
   - Create OAuth2 credentials in Google Cloud Console
   - Add redirect URI from N8N
   - Authorize and connect
5. Ensure the service account has edit access to the Google Sheet

#### Gemini API Key (Environment Variable)

1. Go to **Settings** → **Environment Variables**
2. Add: `GEMINI_API_KEY` = `YOUR_GEMINI_API_KEY`
3. Or set in the AI Analysis node directly

**How to get Gemini API Key:**
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Copy and save securely

### 3. Prepare Google Sheets

Create 4 tabs in your Google Sheet with these headers:

#### Tab 1: "Post Performance Data"
```
Post ID | URL | Date | Type | Copy | Impressions | Reach | Reactions | Comments | Shares | Clicks | Engaged Users | Negative Feedback | Engagement Rate | Share Rate | Click Rate | Performance Score | Category | Video URL | Video Length | Video Format | Video Views | Video Completion Rate
```

#### Tab 2: "AI Analysis"
```
Post ID | URL | Hook Effectiveness | Pacing & Retention | Completion Factors | Visual Storytelling | Audio Impact | Copy Effectiveness | Shareability Factors | Audience Resonance | Engagement Triggers | Replication Framework | Format Effectiveness | Raw Analysis
```

#### Tab 3: "Weekly Patterns"
```
Week | Week Date | Posts Count | Avg Score | Avg Impressions | Avg Engagement Rate | Best Post URL | Best Post Score | Winning Patterns | Common Failures | Video Count | Non-Video Count | Playbook
```

#### Tab 4: "Tracker"
```
Last Run Date | Last Post ID | Posts Added
```

**Initial Tracker Setup:**
- Row 1: Headers (Last Run Date | Last Post ID | Posts Added)
- Row 2: Leave empty (will be populated on first run)

### 4. Configure Workflow Nodes

After importing, verify these node settings:

1. **Schedule Trigger**: Cron expression `0 9 * * 1` (Monday 9 AM)
2. **Read Tracker**: Verify Google Sheet ID and "Tracker" tab name
3. **Fetch Posts**: Verify Page ID `185121598021398`
4. **All Google Sheets nodes**: Verify Sheet ID and tab names match

### 5. Test the Workflow

1. Click **Execute Workflow** (manual trigger)
2. Monitor execution in the workflow view
3. Check Google Sheets for data
4. Verify all nodes execute successfully

## Workflow Structure

### 17 Nodes Flow:

1. **Schedule Trigger** → Runs Monday 9 AM
2. **Read Tracker** → Gets last run state from Sheets
3. **Calculate Date Range** → Determines date range (30 days first time, incremental after)
4. **Fetch Posts** → Gets posts from Meta Graph API
5. **Extract Posts** → Extracts posts array from API response
6. **Filter New** → Filters out already processed posts
7. **Get Insights** → Fetches performance metrics for each post
8. **Merge Insights** → Combines insights with post data
9. **Calculate Metrics** → Computes performance scores
10. **Filter Engagement** → Keeps only posts with >100 impressions
11. **Check If Video** → Identifies video vs non-video posts
12. **Get Video URL** → Fetches video metadata (if video)
13. **Merge Video Data** → Combines video data with post
14. **AI Analysis** → Sends to Gemini for content analysis
15. **Parse AI Response** → Extracts structured insights
16. **Write Performance Data** → Writes to "Post Performance Data" tab
17. **Write AI Insights** → Writes to "AI Analysis" tab
18. **Aggregate Posts** → Collects all processed posts
19. **Generate Summary** → Creates weekly playbook
20. **Write Weekly Patterns** → Writes summary to "Weekly Patterns" tab
21. **Update Tracker** → Updates last run state

## Performance Scoring

**Formula:**
```
Score = (engagementRate × 0.4) + (shareRate × 100 × 0.3) + (clickRate × 0.2) + (videoCompletionRate × 0.1)
```

**Categories:**
- **Exceptional**: >10
- **Good**: 5-10
- **Average**: 2-5
- **Poor**: <2

## AI Analysis

### For Video Posts:
- Hook effectiveness (first 3 seconds)
- Pacing and retention drivers
- Completion factors
- Visual storytelling
- Audio impact
- Copy effectiveness
- Shareability factors
- Audience resonance
- Engagement triggers
- Replication framework

### For Non-Video Posts:
- Copy effectiveness
- Shareability factors
- Audience resonance
- Format effectiveness
- Engagement triggers
- Replication framework

## Weekly Playbook Output

Example output format:
```
ZZUPER PLAYBOOK - Week 51
Posts: 12 | Avg Score: 6.3/10
Best: [URL] - 9.2/10

✅ WINNING: Question hooks, conversational tone, clear CTAs
❌ AVOID: Generic openers, text-heavy, no value prop
FORMAT: Video: 8 | Image/Text: 4
```

## Troubleshooting

### Common Issues:

1. **"Invalid access token"**
   - Verify Meta token is long-lived and has correct permissions
   - Check token format: `Bearer YOUR_TOKEN`

2. **"Sheet not found"**
   - Verify Google Sheet ID is correct
   - Ensure OAuth2 credentials have edit access
   - Check tab names match exactly (case-sensitive)

3. **"Gemini API error"**
   - Verify `GEMINI_API_KEY` environment variable is set
   - Check API key is valid and has quota

4. **"No posts found"**
   - Check date range calculation
   - Verify Page ID is correct
   - Ensure posts exist in the date range

5. **"Duplicate posts"**
   - Check Tracker tab is updating correctly
   - Verify "Last Post ID" is being tracked

## Maintenance

- **Weekly**: Workflow runs automatically
- **Monthly**: Review Google Sheets data
- **Quarterly**: Review and update AI prompts if needed
- **As needed**: Update Meta API token (tokens expire)

## Notes

- First run processes last 30 days of posts
- Subsequent runs are incremental (only new posts)
- Posts with <100 impressions are filtered out
- Video-specific metrics only available for video posts
- AI analysis may take time for large batches

## Support

For issues or questions:
1. Check N8N execution logs
2. Verify all credentials are valid
3. Check Google Sheets for data
4. Review node error messages

---

**Last Updated**: 2024-01-01


