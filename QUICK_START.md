# Quick Start Guide

Get your ZZUPER Meta Post Analysis workflow running in 5 steps.

## Step 1: Import Workflow (2 minutes)

1. Open N8N
2. Click **Workflows** → **Import from File**
3. Select `zzuper-meta-analysis-workflow.json`
4. Workflow imported! ✅

## Step 2: Set Up Credentials (10 minutes)

### Meta API Token
1. Get long-lived Page Access Token from [Meta Developers](https://developers.facebook.com/)
2. In N8N: **Credentials** → **New** → **HTTP Header Auth**
3. Name: `Meta API Token`
4. Header: `Authorization` = `Bearer YOUR_TOKEN`

### Google Sheets OAuth2
1. In N8N: **Credentials** → **New** → **Google Sheets OAuth2 API**
2. Name: `Google Sheets OAuth2`
3. Follow OAuth flow to authorize
4. Grant edit access to your sheet

### Gemini API Key
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. In N8N: **Settings** → **Environment Variables**
3. Add: `GEMINI_API_KEY` = `YOUR_KEY`

## Step 3: Prepare Google Sheet (5 minutes)

Create 4 tabs with these exact names:
- `Post Performance Data` (headers: see README.md)
- `AI Analysis` (headers: see README.md)
- `Weekly Patterns` (headers: see README.md)
- `Tracker` (headers: Last Run Date | Last Post ID | Posts Added)

**Important**: Leave Row 2 of Tracker tab empty (will be auto-populated)

## Step 4: Configure Workflow (2 minutes)

1. Open the imported workflow
2. Verify these settings:
   - **Schedule Trigger**: `0 9 * * 1` (Monday 9 AM)
   - **Read Tracker**: Sheet ID = `1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY`
   - **Fetch Posts**: Page ID = `185121598021398`
   - All Google Sheets nodes: Verify Sheet ID matches

## Step 5: Test Run (5 minutes)

1. Click **Execute Workflow** (manual trigger)
2. Watch execution in real-time
3. Check Google Sheets for data
4. Verify no errors

## ✅ You're Done!

The workflow will now run automatically every Monday at 9 AM.

---

## First Run Behavior

- **First run**: Processes last 30 days of posts
- **Subsequent runs**: Only new posts since last run
- **No duplicates**: Tracker prevents re-processing

## Troubleshooting

**"No posts found"**
- Check date range
- Verify Page ID is correct
- Ensure posts exist in date range

**"Authentication error"**
- Re-check all credentials
- Verify token formats
- Test API access manually

**"Sheet not found"**
- Verify Sheet ID
- Check tab names (case-sensitive)
- Ensure OAuth2 has edit access

---

**Need help?** See `README.md` for detailed documentation.


