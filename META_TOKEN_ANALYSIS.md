# Meta Access Token Probleem Analyse

## Huidige Situatie

### ✅ Wat werkt:
- **Read Tracker**: Werkt correct (gebruiker bevestigt dit)
- **Credential configuratie**: "Header Auth account 4" is correct ingesteld:
  - Name: `Authorization` ✅
  - Value: `Bearer EAAyk1ciX1SsBQbU92J6YoFsj7RhVbjATT5ta6F6JsbPmgeQQONWeZCdF68IgCIKsWF8IoBTqlpeBKO1sX6kIOAzxMcQe31cJQB78474ZBgQpE9n85oVHKWtCSlRNmsPjVK9BaJJsdriBNoUyfn81QTxloPK8uWDU6pa6J0ClRlBJHDKVLI1wWWuuCfpdjEZCvgZD` ✅
  - Laatst bijgewerkt: just now ✅

### ❌ Wat niet werkt:
- **Meta Access Token**: Fetch Posts node faalt met authenticatie error

## Mogelijke Problemen

### 1. Token Formaat
**Probleem**: Meta Graph API verwacht mogelijk alleen het token, niet "Bearer" prefix.

**Oplossing**: Testen zonder "Bearer" prefix:
- Huidige waarde: `Bearer EAAyk1ciX1SsBQbU92J6YoFsj7RhVbjATT5ta6F6JsbPmgeQQONWeZCdF68IgCIKsWF8IoBTqlpeBKO1sX6kIOAzxMcQe31cJQB78474ZBgQpE9n85oVHKWtCSlRNmsPjVK9BaJJsdriBNoUyfn81QTxloPK8uWDU6pa6J0ClRlBJHDKVLI1wWWuuCfpdjEZCvgZD`
- Te testen: `EAAyk1ciX1SsBQbU92J6YoFsj7RhVbjATT5ta6F6JsbPmgeQQONWeZCdF68IgCIKsWF8IoBTqlpeBKO1sX6kIOAzxMcQe31cJQB78474ZBgQpE9n85oVHKWtCSlRNmsPjVK9BaJJsdriBNoUyfn81QTxloPK8uWDU6pa6J0ClRlBJHDKVLI1wWWuuCfpdjEZCvgZD`

### 2. Token Validiteit
**Probleem**: Het token kan verlopen zijn of ongeldig zijn.

**Oplossing**: Valideer het token via Meta Graph API:
```bash
curl "https://graph.facebook.com/v21.0/debug_token?input_token=TOKEN&access_token=TOKEN"
```

### 3. Header Configuratie
**Probleem**: N8N HTTP Request node gebruikt mogelijk de verkeerde header configuratie.

**Huidige configuratie**:
- Authentication: Generic Credential Type
- Generic Auth Type: Header Auth
- Credential: Header Auth account 4
- Header Name: `Authorization`
- Header Value: `Bearer TOKEN`

**Mogelijke oplossing**: Meta API verwacht mogelijk:
- Header Name: `Authorization` (correct)
- Header Value: Alleen het token (zonder "Bearer")

### 4. Fetch Posts Node Configuratie
**Probleem**: De node configuratie kan verkeerd zijn ingesteld.

**Te controleren**:
- URL: `https://graph.facebook.com/v21.0/185121598021398/posts` ✅
- Method: `GET` ✅
- Authentication: `Generic Credential Type` met `Header Auth` ✅
- Credential: `Header Auth account 4` ✅

## Aanbevolen Oplossing

### Stap 1: Test token zonder "Bearer" prefix
1. Open credential "Header Auth account 4"
2. Verwijder "Bearer " prefix uit de Value
3. Sla op
4. Test workflow

### Stap 2: Als dat niet werkt, valideer token
1. Gebruik `refresh_meta_token.py` om een nieuw token te genereren
2. Controleer of het token geldig is
3. Update credential met nieuw token

### Stap 3: Controleer Fetch Posts node
1. Open Fetch Posts node
2. Controleer of credential correct is toegewezen
3. Controleer of URL en parameters correct zijn

## Belangrijke Opmerkingen

- De gebruiker zegt dat "Read Tracker wel werkt" - dit betekent dat Google Sheets credentials correct zijn
- De gebruiker zegt dat "Meta access code was correct" - dit suggereert dat het token zelf correct is, maar de configuratie mogelijk verkeerd is
- De error "Header name must be a valid HTTP token" suggereert dat er mogelijk een probleem is met hoe de header wordt geformatteerd

