# Credential Assignment Checklist

Use this checklist to ensure all credentials are properly assigned.

## ✅ Google Sheets OAuth2 Credential

Assign to these 5 nodes:
- [ ] **Read Tracker**
- [ ] **Write Performance Data**
- [ ] **Write AI Insights**
- [ ] **Write Weekly Patterns**
- [ ] **Update Tracker**

**How to assign:**
1. Click the node
2. Find "Credential to connect with" dropdown
3. Select "Google Sheets OAuth2"
4. Save

---

## ✅ Meta API Token (HTTP Header Auth)

Assign to these 3 nodes:
- [ ] **Fetch Posts**
- [ ] **Get Insights**
- [ ] **Get Video URL**

**How to assign:**
1. Click the node
2. Set "Authentication" = "Generic Credential Type"
3. Set "Generic Auth Type" = "HTTP Header Auth"
4. Select "Meta API Token" in credentials dropdown
5. Save

---

## ✅ Gemini API Key (Environment Variable)

- [ ] **GEMINI_API_KEY** is set in Settings → Environment Variables

**How to verify:**
1. Go to Settings → Environment Variables
2. Check for `GEMINI_API_KEY`
3. If missing, add it with your API key value

---

## 🧪 After Assigning All Credentials

1. [ ] Click "Execute Workflow" to test
2. [ ] Check execution logs for errors
3. [ ] Verify data appears in Google Sheets
4. [ ] Activate workflow if test is successful

---

**Status:** All credentials assigned and tested ✅


