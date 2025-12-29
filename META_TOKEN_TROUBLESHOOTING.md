# Meta API Token Troubleshooting Guide

## Error: "(#200) Provide valid app ID"

Deze fout betekent dat je Meta API access token niet correct is geconfigureerd of niet geldig is.

## Oplossing: Verkrijg een geldige Page Access Token

### Stap 1: Ga naar Facebook Graph API Explorer

1. Open: https://developers.facebook.com/tools/explorer/
2. Log in met je Facebook account

### Stap 2: Selecteer je App en Page

1. **Select App**: Kies je Facebook App (of maak er een aan als je die nog niet hebt)
2. **Select Page**: Kies je Facebook Page (Page ID: `185121598021398`)

### Stap 3: Genereer een Page Access Token

1. Klik op **"Generate Access Token"** of **"Get Token"**
2. Selecteer **"Get Page Access Token"** (NIET User Access Token!)
3. Kies je pagina: `185121598021398`
4. Selecteer de volgende **permissions**:
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`
   - ✅ `pages_read_user_content` (optioneel, voor meer data)
5. Klik op **"Generate Access Token"**

### Stap 4: Kopieer de Token

1. Kopieer de gegenereerde token (zonder "Bearer " - dat voegen we later toe)
2. **BELANGRIJK**: Deze token is tijdelijk (meestal 1-2 uur geldig)

### Stap 5: Maak een Long-Lived Token (Aanbevolen)

Voor productie gebruik moet je een **Long-Lived Page Access Token** maken:

1. Ga naar: https://developers.facebook.com/tools/accesstoken/
2. Klik op je Page Access Token
3. Klik op **"Extend Access Token"** of gebruik de API:
   ```
   GET https://graph.facebook.com/v18.0/oauth/access_token?
     grant_type=fb_exchange_token&
     client_id=YOUR_APP_ID&
     client_secret=YOUR_APP_SECRET&
     fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
   ```

### Stap 6: Configureer in N8N

1. Ga naar: https://alexrinne.app.n8n.cloud/home/credentials/bi3V9te2bqwQGzgC
2. Open de **"meta-api-token"** credential
3. **Name** veld: `Authorization`
4. **Value** veld: `Bearer YOUR_PAGE_ACCESS_TOKEN`
   - Vervang `YOUR_PAGE_ACCESS_TOKEN` met je gekopieerde token
   - Zorg dat `Bearer ` (met spatie) voor de token staat
5. Klik op **"Save"**

## Alternatief: Via Meta Business Suite

1. Ga naar: https://business.facebook.com/
2. Selecteer je Business Account
3. Ga naar **Settings** → **System Users** of **Page Access Tokens**
4. Genereer een Page Access Token met de juiste permissions

## Veelvoorkomende Problemen

### ❌ Probleem 1: User Access Token in plaats van Page Access Token
**Oplossing**: Zorg dat je een **Page Access Token** gebruikt, niet een User Access Token.

### ❌ Probleem 2: Token is verlopen
**Oplossing**: Genereer een nieuwe token of maak een Long-Lived Token.

### ❌ Probleem 3: Token heeft niet de juiste permissions
**Oplossing**: Zorg dat de token `pages_read_engagement` en `pages_show_list` permissions heeft.

### ❌ Probleem 4: "Bearer " prefix ontbreekt of verkeerd
**Oplossing**: Controleer dat het Value veld exact is: `Bearer YOUR_TOKEN` (met spatie na "Bearer").

## Test je Token

Test je token met deze curl command:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://graph.facebook.com/v18.0/185121598021398?fields=id,name"
```

**Verwachte response**:
```json
{
  "id": "185121598021398",
  "name": "Your Page Name"
}
```

**Als je een error krijgt**:
```json
{
  "error": {
    "message": "(#200) Provide valid app ID",
    "type": "OAuthException",
    "code": 200
  }
}
```

Dan is je token niet geldig. Genereer een nieuwe Page Access Token.


