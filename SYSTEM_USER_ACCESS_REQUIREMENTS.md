# System User Access Requirements voor ZZUPER Meta Post Analysis

## Overzicht

De System User heeft toegang nodig tot de Facebook Page om:
1. Posts te lezen (inclusief berichten, comments, shares)
2. Insights/metrics te lezen (impressions, reach, engagement)
3. Video metadata te lezen (source, length, format)

---

## 1. Page-Level Access (in Meta Business Manager)

**Facebook Page: ZZUPER (ID: 185121598021398)**

De System User moet **toegang hebben tot de Page** met minimaal:

### ✅ Vereiste Page Permissions:
- **Content** - Om posts te lezen
- **Insights** - Om performance metrics te lezen
- **Community activity** - Om comments en engagement te lezen

**Huidige status:** ✅ "Partial access (Content, Messages, Community activity, Ads, Insights)"

Dit is **voldoende** voor de workflow!

---

## 2. App-Level Permissions (Token Permissions)

De System User token moet de volgende **permissions** hebben:

### ✅ Vereiste Permissions:

1. **`pages_read_user_content`** ⚠️ **KRITIEK - MIST NU!**
   - Vereist om posts te lezen via `/posts` endpoint
   - Zonder deze permission krijg je "Invalid OAuth 2.0 Access Token" bij posts

2. **`pages_read_engagement`** ✅ **HEB JE AL**
   - Vereist om engagement metrics te lezen (reactions, comments, shares)
   - Gebruikt voor insights endpoint

3. **`pages_show_list`** ✅ **HEB JE AL**
   - Vereist om de pagina te identificeren en te zien
   - Basis permission voor Page API access

### 📋 Optionele maar Aanbevolen Permissions:

4. **`pages_manage_ads`** ✅ **HEB JE AL**
   - Niet vereist voor deze workflow, maar kan handig zijn

5. **`business_management`** ✅ **HEB JE AL**
   - Niet vereist voor deze workflow, maar kan handig zijn

---

## 3. API Endpoints die de Workflow Gebruikt

### Endpoint 1: Fetch Posts
```
GET /v21.0/{page_id}/posts
```
**Vereist:**
- `pages_read_user_content` ⚠️ **MIST**
- Page access met "Content" permission ✅ **HEB JE**

**Fields die worden opgehaald:**
- `id, message, created_time, type, permalink_url, full_picture`
- `comments.summary(true)` - Comments count
- `shares` - Shares count
- `attachments` - Media attachments

### Endpoint 2: Get Insights
```
GET /v21.0/{post_id}/insights
```
**Vereist:**
- `pages_read_engagement` ✅ **HEB JE**
- Page access met "Insights" permission ✅ **HEB JE**

**Metrics die worden opgehaald:**
- `post_impressions`
- `post_reach`
- `post_reactions_by_type_total`
- `post_clicks`
- `post_engaged_users`
- `post_negative_feedback`

### Endpoint 3: Get Video URL
```
GET /v21.0/{video_id}?fields=source,length,format
```
**Vereist:**
- `pages_read_user_content` ⚠️ **MIST** (voor video content)
- Page access met "Content" permission ✅ **HEB JE**

---

## 4. Huidige Status vs. Vereisten

| Requirement | Status | Actie |
|------------|--------|-------|
| Page Access: Content | ✅ Heeft | Geen actie |
| Page Access: Insights | ✅ Heeft | Geen actie |
| Page Access: Community activity | ✅ Heeft | Geen actie |
| Permission: `pages_read_user_content` | ❌ Mist | **TOEVOEGEN** |
| Permission: `pages_read_engagement` | ✅ Heeft | Geen actie |
| Permission: `pages_show_list` | ✅ Heeft | Geen actie |

---

## 5. Oplossing: Voeg `pages_read_user_content` Toe

### Optie A: Zoek in Permissions Lijst

1. In de "Select permissions" modal:
   - Gebruik de zoekbalk
   - Zoek naar: `pages_read_user_content` of `read_user_content`
   - Selecteer het als je het vindt

### Optie B: App Configuratie Aanpassen

Als `pages_read_user_content` niet beschikbaar is in de lijst:

1. Ga naar de app instellingen: https://developers.facebook.com/apps/3558937820910891/
2. Ga naar **App Review** → **Permissions and Features**
3. Voeg `pages_read_user_content` toe aan de use case
4. Configureer de use case voor "Read Page Content"

### Optie C: Test Eerst met Huidige Setup

Aangezien de Page nu "Content" access heeft, kan het zijn dat posts nu werken zonder `pages_read_user_content` permission. Test eerst:

1. Test de workflow in N8N
2. Als het werkt: geen actie nodig
3. Als het niet werkt: voeg `pages_read_user_content` toe

---

## 6. Samenvatting

**Minimale Vereisten:**
- ✅ Page Access: Content, Insights, Community activity
- ✅ Token Permission: `pages_read_engagement`
- ✅ Token Permission: `pages_show_list`
- ⚠️ Token Permission: `pages_read_user_content` (waarschijnlijk nodig)

**Aanbevolen:**
- Alle bovenstaande permissions
- Long-lived token (60+ dagen of "Never")

---

## 7. Test Checklist

Na het toevoegen van permissions:

- [ ] Test "Fetch Posts" node in N8N
- [ ] Test "Get Insights" node in N8N
- [ ] Test "Get Video URL" node in N8N
- [ ] Voer volledige workflow uit
- [ ] Controleer Google Sheets output


