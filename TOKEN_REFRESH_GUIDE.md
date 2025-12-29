# Meta Token Refresh Guide

## Probleem
De Meta API Page Access Token kan verlopen, wat resulteert in de error "Invalid OAuth 2.0 Access Token" in de workflow.

## Oplossing
Gebruik het `refresh_meta_token.py` script om automatisch een nieuw Page Access Token te extraheren en de N8N credential bij te werken.

## Automatische Token Refresh

### Stap 1: Script uitvoeren
```bash
python3 refresh_meta_token.py
```

Het script:
1. Extraheert automatisch een nieuw Page Access Token uit het System User Token
2. Valideert het nieuwe token
3. Probeert de N8N credential automatisch bij te werken (als N8N_API_KEY is ingesteld)
4. Geeft instructies voor handmatige update als automatische update niet mogelijk is

### Stap 2: Handmatige Update (als automatische update faalt)
Als de automatische update niet werkt (bijv. omdat N8N_API_KEY niet is ingesteld):

1. Ga naar N8N → Credentials → "Header Auth account 4"
2. Klik op de credential om deze te openen
3. Update het "Value" veld met het token dat het script heeft gegenereerd:
   ```
   Bearer [TOKEN]
   ```
4. Klik op "Save"

## Automatische Update via N8N API (Optioneel)

Om volledig automatische updates te krijgen, stel de N8N API Key in:

```bash
export N8N_API_KEY="your-n8n-api-key"
export N8N_BASE_URL="https://alexrinne.app.n8n.cloud"
```

Vervolgens zal het script automatisch de credential bijwerken.

### N8N API Key verkrijgen
1. Ga naar N8N → Settings → API
2. Genereer een nieuwe API Key
3. Kopieer de key en stel deze in als environment variable

## Scheduled Refresh (Aanbevolen)

Om te voorkomen dat tokens verlopen, kun je het refresh script periodiek uitvoeren:

### Via Cron (Linux/Mac)
```bash
# Voeg toe aan crontab (crontab -e)
# Refresh token elke maandag om 8:00 AM (voor de workflow die om 9:00 AM draait)
0 8 * * 1 cd /path/to/project && python3 refresh_meta_token.py
```

### Via GitHub Actions (Cloud)
Maak een `.github/workflows/refresh-token.yml` bestand:
```yaml
name: Refresh Meta Token
on:
  schedule:
    - cron: '0 8 * * 1'  # Elke maandag om 8:00 AM UTC
  workflow_dispatch:  # Handmatige trigger

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Refresh Token
        env:
          N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
          N8N_BASE_URL: ${{ secrets.N8N_BASE_URL }}
        run: python3 refresh_meta_token.py
```

## Troubleshooting

### Token is nog steeds ongeldig na refresh
1. Controleer of het System User Token nog geldig is
2. Controleer of de System User de juiste permissions heeft:
   - `pages_read_engagement`
   - `pages_show_list`
   - `pages_read_user_content`
3. Genereer een nieuw System User Token in Meta Business Manager als nodig

### Script kan N8N credential niet vinden
- Controleer of de credential naam exact overeenkomt: "Header Auth account 4"
- Controleer of de N8N_API_KEY correct is ingesteld
- Controleer of de N8N_BASE_URL correct is ingesteld

### Script kan geen Page Access Token extraheren
- Controleer of het System User Token geldig is
- Controleer of de System User toegang heeft tot de Page (ID: 185121598021398)
- Controleer of de System User de juiste permissions heeft

## System User Token Configuratie

Het System User Token moet worden geconfigureerd in Meta Business Manager:

1. Ga naar Meta Business Manager → Business Settings → System Users
2. Selecteer de System User
3. Zorg dat de volgende permissions zijn toegewezen:
   - **Page-Level**: `pages_read_engagement`, `pages_show_list`, `pages_read_user_content`
   - **App-Level**: Zorg dat de app "Manage everything on your Page" use case heeft
4. Genereer een nieuw token met alle benodigde permissions

## Token Validiteit

- **System User Token**: Kan langlopend zijn (60+ dagen) of permanent
- **Page Access Token**: Wordt automatisch geëxtraheerd uit System User Token
- **Refresh Frequentie**: Aanbevolen om wekelijks te refreshen (voor de workflow die elke maandag draait)

## Belangrijke Notities

- Het script gebruikt het System User Token dat is geconfigureerd in `refresh_meta_token.py`
- Als het System User Token verandert, update de `SYSTEM_USER_TOKEN` variabele in het script
- Het nieuwe Page Access Token wordt automatisch gevalideerd voordat het wordt gebruikt
- De credential wordt alleen bijgewerkt als het nieuwe token succesvol is gevalideerd


