# Troubleshooting Guide: "Sheet with ID Tracker not found"

## Problem
The "Read Tracker" node fails with: `Sheet with ID Tracker not found`

## Root Cause
N8N cannot fetch the sheet list from Google Sheets API, even though:
- The Service Account has Editor access
- The sheet "Tracker" exists
- The credentials are configured

## Solutions (in order of preference)

### Solution 1: Change Sheet Mode to "By name" (Recommended)
**Status**: Already updated in `zzuper-meta-analysis-workflow.json` (line 32: `"mode": "name"`)

**Manual Steps in N8N UI**:
1. Open the "Read Tracker" node (double-click)
2. Find the "Sheet" field
3. Change from "From list" to "By name"
4. Enter: `Tracker` (exact name, case-sensitive)
5. Save the node

**Why this works**: Bypasses the need to fetch the sheet list from Google API.

---

### Solution 2: Use Sheet ID Instead of Name
If "By name" doesn't work, try using the sheet's GID (Google Sheet ID):

**Steps**:
1. Open your Google Sheet: `https://docs.google.com/spreadsheets/d/1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY/edit`
2. Click on the "Tracker" tab
3. Look at the URL - it should be: `.../edit#gid=XXXXX`
4. Copy the `gid` number (e.g., `1234567890`)
5. In N8N "Read Tracker" node:
   - Change Sheet mode to "By ID"
   - Enter the GID number

**Note**: This requires updating the workflow JSON to use `mode: "id"` for `sheetName`.

---

### Solution 3: Change Operation Type
Try changing the operation from "read" to "Get Row(s)":

**Steps**:
1. Open "Read Tracker" node
2. Change "Operation" from "Read" to "Get Row(s)"
3. Set "Sheet" to "By name" = `Tracker`
4. Set "Range" to `A1:C2` (or leave empty for all rows)
5. Save

---

### Solution 4: Verify Service Account Permissions
Double-check the Service Account has proper access:

**Steps**:
1. Open Google Sheet: `https://docs.google.com/spreadsheets/d/1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY/edit`
2. Click "Share" button
3. Verify `n8n-google-sheets@n8n-post-analyzer.iam.gserviceaccount.com` is listed
4. Ensure permission is "Editor" (not "Viewer")
5. If not listed, add it with "Editor" permission

---

### Solution 5: Use HTTP Request Node as Workaround
Replace "Read Tracker" with an HTTP Request node that directly calls Google Sheets API:

**Configuration**:
- **Method**: GET
- **URL**: `https://sheets.googleapis.com/v4/spreadsheets/1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY/values/Tracker!A1:C2`
- **Authentication**: OAuth2 or Service Account
- **Headers**: 
  - `Authorization: Bearer {{ $credentials.googleServiceAccount.accessToken }}`

**Note**: This requires getting the access token from the Service Account credential.

---

### Solution 6: Initialize Tracker Tab Manually
If the Tracker tab is empty or missing data:

**Steps**:
1. Open Google Sheet
2. Go to "Tracker" tab
3. Ensure Row 1 has headers: `Last Run Date | Last Post ID | Posts Added`
4. Add Row 2 with empty values (or initial values):
   - `Last Run Date`: (leave empty)
   - `Last Post ID`: (leave empty)
   - `Posts Added`: `0`

---

### Solution 7: Update All Google Sheets Nodes
Apply "By name" mode to ALL Google Sheets nodes to avoid similar issues:

**Nodes to update**:
1. Read Tracker → Sheet: "By name" = `Tracker`
2. Write Performance Data → Sheet: "By name" = `Post Performance Data`
3. Write AI Insights → Sheet: "By name" = `AI Analysis`
4. Write Weekly Patterns → Sheet: "By name" = `Weekly Patterns`
5. Update Tracker → Sheet: "By name" = `Tracker`

**Current status in JSON**:
- ✅ Read Tracker: `mode: "name"` (line 32)
- ❌ Write Performance Data: `mode: "list"` (line 320)
- ❌ Write AI Insights: `mode: "list"` (line 374)
- ❌ Write Weekly Patterns: `mode: "list"` (line 441)
- ❌ Update Tracker: `mode: "list"` (line 485)

---

### Solution 8: Test with a Simple Read First
Create a test node to verify connectivity:

**Steps**:
1. Add a new Google Sheets node
2. Configure:
   - Operation: "Read"
   - Document: `1ye1nbaT4GyREOJsWuiXVavc_nvXHcDMLU7hqwCqapqY`
   - Sheet: "By name" = `Tracker`
   - Range: `A1:C2`
3. Execute this node alone
4. If it works, the issue is with the original node configuration
5. If it fails, the issue is with credentials/permissions

---

## Quick Fix Script
If you have N8N API access, you can update the workflow programmatically. However, this requires an API key.

## Recommended Action Plan

1. **First**: Try Solution 1 (change to "By name" in UI) - this is the simplest
2. **If that fails**: Try Solution 2 (use Sheet GID)
3. **If still failing**: Verify Solution 4 (Service Account permissions)
4. **Last resort**: Use Solution 5 (HTTP Request workaround)

## Current Workflow JSON Status

The local file `zzuper-meta-analysis-workflow.json` already has:
- ✅ Read Tracker: `mode: "name"` (correct)
- ❌ Other nodes: Still using `mode: "list"` (should be updated)

**Next step**: Manually update the "Read Tracker" node in N8N UI to use "By name" mode, or update all nodes to use "By name" mode for consistency.


