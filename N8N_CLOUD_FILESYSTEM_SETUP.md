# N8N Cloud - Filesystem Mode Setup

## Stap-voor-stap Instructies

Als je N8N Cloud gebruikt (via browser), volg deze stappen:

### Stap 1: Log in op N8N Cloud

1. Ga naar je N8N Cloud dashboard (bijv. `https://app.n8n.cloud` of je custom URL)
2. Log in met je account

### Stap 2: Ga naar Settings

1. Klik op je **profiel/account icoon** (rechtsboven)
2. Selecteer **Settings** of **Instance Settings**
3. Of navigeer direct naar: **Settings** → **Environment Variables**

### Stap 3: Voeg Environment Variable toe

1. In de Settings pagina, zoek naar **"Environment Variables"** sectie
2. Klik op **"Add Variable"** of **"New Variable"** knop
3. Vul in:
   - **Variable Name**: `N8N_DEFAULT_BINARY_DATA_MODE`
   - **Variable Value**: `filesystem`
4. Klik op **"Save"** of **"Add"**

### Stap 4: Herstart je N8N Instance

1. Ga naar **Settings** → **Instance** of **General**
2. Zoek naar **"Restart Instance"** of **"Reboot"** knop
3. Klik op **"Restart"** om de wijzigingen toe te passen
4. Wacht tot N8N opnieuw is opgestart (meestal 1-2 minuten)

### Stap 5: Verifieer de Configuratie

1. Ga terug naar **Settings** → **Environment Variables**
2. Controleer dat `N8N_DEFAULT_BINARY_DATA_MODE=filesystem` zichtbaar is
3. Of test met een workflow die een groot bestand verwerkt

## Alternatieve Locaties (afhankelijk van N8N Cloud versie)

Als je de Environment Variables niet direct kunt vinden, probeer:

- **Settings** → **Configuration** → **Environment Variables**
- **Admin** → **Settings** → **Environment Variables**
- **Workspace Settings** → **Environment Variables**
- **Instance Settings** → **Environment Variables**

## Troubleshooting

**Problem**: Kan Environment Variables niet vinden
- **Solution**: 
  - Check of je admin/owner rechten hebt op de instance
  - Sommige N8N Cloud plans hebben mogelijk beperkte toegang
  - Neem contact op met N8N Cloud support als je de optie niet ziet

**Problem**: Instance restart optie niet beschikbaar
- **Solution**: 
  - De wijziging wordt mogelijk automatisch toegepast
  - Wacht een paar minuten en test de workflow
  - Of neem contact op met N8N Cloud support

**Problem**: Nog steeds memory errors na configuratie
- **Solution**:
  - Verifieer dat de variable correct is ingesteld (check spelling)
  - Wacht tot de instance volledig is herstart
  - Check N8N logs voor bevestiging
  - Neem contact op met N8N Cloud support als het probleem aanhoudt

## Verificatie na Setup

Na het instellen, test je workflow:

1. Voer de workflow uit met een video post
2. Check of video's worden gedownload zonder memory errors
3. Controleer de execution logs voor eventuele errors

## Contact N8N Cloud Support

Als je problemen hebt met het instellen van environment variables in N8N Cloud:

- **Email**: support@n8n.io
- **Documentation**: https://docs.n8n.io/hosting/scaling/binary-data/
- **Community Forum**: https://community.n8n.io/

## Belangrijke Notities

- **Disk Space**: Zorg dat je N8N Cloud plan voldoende storage heeft voor video bestanden
- **Plan Limits**: Sommige N8N Cloud plans hebben mogelijk limieten op binary data storage
- **Costs**: Extra storage kan extra kosten met zich meebrengen, check je plan details

