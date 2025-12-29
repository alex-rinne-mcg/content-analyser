# Meta API Token Permissions Fix

## Probleem
Het huidige token mist de `pages_read_user_content` permission, die nodig is om posts te lezen via de Meta Graph API.

## Huidige Token Permissions
✅ `pages_show_list`
✅ `pages_read_engagement`
✅ `pages_manage_ads`
✅ `ads_management`
✅ `ads_read`
✅ `business_management`
✅ `public_profile`

❌ **MIST:** `pages_read_user_content` (vereist voor posts)

## Oplossing

### Stap 1: Genereer nieuw token in Meta Business Manager

1. Ga naar: https://business.facebook.com/latest/settings/system_users?business_id=405413375398915&selected_user_id=61556291558356

2. Klik op "Generate token"

3. Selecteer app: "ZZUPER analytics"

4. Set expiration: "Never" (of 60 days)

5. **Bij "Assign permissions" - ZORG DAT JE HEBT:**
   - ✅ `pages_read_user_content` (BELANGRIJK - deze mist nu!)
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`
   - ✅ Andere permissions zoals nodig

6. Genereer het token

7. Kopieer het nieuwe token

### Stap 2: Update N8N Credential

1. Ga naar: https://alexrinne.app.n8n.cloud/home/credentials/bi3V9te2bqwQGzgC

2. Update het "Value" veld met: `Bearer [NIEUWE_TOKEN]`

3. Sla op

### Stap 3: Test

Voer het test script uit:
```bash
python3 test_meta_token.py
```

Of test direct in N8N door de "Fetch Posts" node uit te voeren.

## Belangrijke Permissions voor deze Workflow

Voor de ZZUPER Meta Post Analysis workflow heb je minimaal nodig:
- `pages_read_user_content` - Om posts te lezen
- `pages_read_engagement` - Om engagement metrics te lezen
- `pages_show_list` - Om pagina's te zien


