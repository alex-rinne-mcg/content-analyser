# Credentials Setup Template

Use this as a reference when setting up credentials for the ZZUPER Meta Post Analysis workflow.

## Required Credentials

### 1. Meta API Token (HTTP Header Auth)

**Type**: HTTP Header Auth  
**Name**: `Meta API Token`  
**Configuration**:
- Header Name: `Authorization`
- Header Value: `Bearer YOUR_META_ACCESS_TOKEN`

**How to Obtain**:
1. Go to https://developers.facebook.com/
2. Create or select your app
3. Add Facebook Login product
4. Go to Tools → Graph API Explorer
5. Select your page
6. Generate Page Access Token
7. Exchange for long-lived token (60 days)
8. Use format: `Bearer YOUR_TOKEN`

**Required Permissions**:
- `pages_read_engagement`
- `pages_show_list`

**Page ID**: `185121598021398`

---

### 2. Google Sheets OAuth2

**Type**: Google Sheets OAuth2 API  
**Name**: `Google Sheets OAuth2`

**Setup Steps**:
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable Google Sheets API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI from N8N
6. Copy Client ID and Client Secret
7. In N8N, create Google Sheets OAuth2 credential
8. Authorize and connect

**Required Access**:
- Edit access to Google Sheet
- Sheet ID: `1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY`

---

### 3. Gemini API Key

**Type**: Environment Variable  
**Name**: `GEMINI_API_KEY`  
**Value**: `YOUR_GEMINI_API_KEY`

**How to Obtain**:
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the API key
5. Set in N8N environment variables

**Alternative**: Set directly in AI Analysis node (less secure)

**Model**: `gemini-1.5-pro`

---

## Credential Checklist

- [ ] Meta API Token created and tested
- [ ] Google Sheets OAuth2 connected and authorized
- [ ] Gemini API Key set in environment variables
- [ ] All credentials tested in workflow
- [ ] Google Sheet has correct tabs and headers
- [ ] Tracker tab initialized (empty row 2)

---

## Security Notes

- **Never commit credentials to version control**
- Store API keys in environment variables when possible
- Use long-lived tokens for Meta API (refresh before expiration)
- Rotate API keys periodically
- Limit OAuth2 scopes to minimum required

---

## Testing Credentials

### Test Meta API Token:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://graph.facebook.com/v18.0/185121598021398/posts?limit=1"
```

### Test Gemini API Key:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Test Google Sheets:
- Manually access the sheet
- Verify edit permissions
- Check tab names match exactly

---

**Remember**: Keep credentials secure and never share them publicly!


