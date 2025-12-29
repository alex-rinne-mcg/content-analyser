# Automatische Workflow Sync Setup Guide

Deze guide legt uit hoe je de automatische sync workflow instelt die workflows uit GitHub haalt en automatisch importeert/updateert in N8N.

## 🎯 Wat doet deze workflow?

De "Sync Workflows from GitHub" workflow:
1. **Checkt elke 6 uur** of er updates zijn in GitHub
2. **Haalt de workflow op** uit GitHub (raw content URL)
3. **Vergelijkt** met bestaande workflow in N8N
4. **Importeert/updateert** automatisch als er wijzigingen zijn
5. **Logt** het resultaat

## 📋 Setup Stappen

### Stap 1: Import Sync Workflow

1. Open je N8N instance: `https://content-analyser-production.up.railway.app`
2. Command palette (⌘K) → "Import workflow from file"
3. Selecteer `workflow-sync-workflow.json`
4. Workflow wordt geïmporteerd

### Stap 2: Configureer N8N API Access

De sync workflow gebruikt de N8N REST API om workflows te importeren. Dit vereist authenticatie.

**Optie A: Gebruik N8N User Session (Aanbevolen)**

De workflow draait binnen N8N, dus gebruikt automatisch je ingelogde sessie. Geen extra configuratie nodig!

**Optie B: API Key (Voor geavanceerd gebruik)**

Als je een API key wilt gebruiken:

1. Ga naar **Settings** → **API**
2. Genereer een nieuwe API key
3. Voeg toe aan de "Import/Update Workflow" node als credential

### Stap 3: Test de Sync Workflow

1. Open de "Sync Workflows from GitHub" workflow
2. Klik op **"Execute Workflow"** (manual trigger)
3. Check de execution logs:
   - ✅ "Fetch Workflow from GitHub" - haalt workflow op
   - ✅ "Get Existing Workflows" - haalt bestaande workflows op
   - ✅ "Check Workflow Version" - vergelijkt versies
   - ✅ "If Needs Update" - beslist of update nodig is
   - ✅ "Import/Update Workflow" - importeert/updateert (als nodig)
   - ✅ "Log Sync Result" - logt resultaat

### Stap 4: Activeer de Workflow

1. Klik op **"Active"** toggle bovenaan de workflow
2. Workflow draait nu automatisch elke 6 uur
3. Je kunt de interval aanpassen in "Schedule Trigger" node

## ⚙️ Configuratie Opties

### Sync Interval Aanpassen

In de "Schedule Trigger (Every 6 hours)" node:

- **Elke 6 uur**: `0 */6 * * *` (standaard)
- **Elke uur**: `0 * * * *`
- **Elke dag om 9:00**: `0 9 * * *`
- **Elke 12 uur**: `0 */12 * * *`

### Workflow URL Aanpassen

In de "Fetch Workflow from GitHub" node:

- **Huidige URL**: `https://raw.githubusercontent.com/alex-rinne-mcg/content-analyser/main/zzuper-meta-analysis-workflow.json`
- **Andere branch**: Vervang `main` met branch naam
- **Andere workflow**: Vervang bestandsnaam

### Meerdere Workflows Syncen

Je kunt de workflow uitbreiden om meerdere workflows te syncen:

1. Voeg meerdere "Fetch Workflow from GitHub" nodes toe
2. Gebruik "Split In Batches" node om parallel te verwerken
3. Of maak een loop voor elke workflow

## 🔍 Troubleshooting

### Probleem: "Unauthorized" Error

**Oorzaak:** N8N API vereist authenticatie

**Oplossing:**
- Zorg dat je ingelogd bent in N8N
- De workflow gebruikt automatisch je sessie
- Als dit niet werkt, gebruik API key (zie Stap 2, Optie B)

### Probleem: Workflow wordt niet geüpdatet

**Oorzaak:** Version check detecteert geen verschillen

**Oplossing:**
- Check de "Check Workflow Version" node output
- Verifieer dat `needsUpdate: true` is
- Check of GitHub workflow daadwerkelijk is geüpdatet

### Probleem: "Fetch Workflow from GitHub" faalt

**Oorzaak:** GitHub URL is niet toegankelijk of repository is private

**Oplossing:**
- Verifieer dat de repository public is
- Of gebruik een GitHub token in de URL
- Check of de bestandsnaam correct is

### Probleem: Workflow wordt geïmporteerd maar credentials ontbreken

**Oorzaak:** Credentials worden niet meegenomen in workflow export (veiligheid)

**Oplossing:**
- Configureer credentials handmatig na import
- Of gebruik een "Configure Credentials" node na import

## 📊 Monitoring

### Check Sync Status

1. Ga naar **Executions** tab
2. Filter op "Sync Workflows from GitHub"
3. Check laatste execution:
   - ✅ Succes: Workflow is gesynced
   - ❌ Fout: Check error message

### Logs Bekijken

In de "Log Sync Result" node output zie je:
- `message`: Sync status
- `timestamp`: Wanneer gesynced
- `result`: Details van de sync

## 🔄 Workflow Update Proces

### Stap 1: Wijzig Workflow Lokaal

```bash
# Edit workflow
code zzuper-meta-analysis-workflow.json

# Test lokaal (indien mogelijk)
```

### Stap 2: Commit & Push naar GitHub

```bash
git add zzuper-meta-analysis-workflow.json
git commit -m "Update: [beschrijving]"
git push origin main
```

### Stap 3: Wacht op Auto-Sync

- Sync workflow checkt automatisch elke 6 uur
- Of trigger handmatig via "Execute Workflow"
- Workflow wordt automatisch geïmporteerd/geüpdatet

### Stap 4: Verifieer Import

1. Check N8N Executions voor sync workflow
2. Open de geüpdatete workflow
3. Verifieer dat wijzigingen zijn doorgevoerd
4. Test de workflow

## 🎛️ Geavanceerde Opties

### Webhook Trigger (Real-time Sync)

In plaats van periodieke checks, kun je een webhook gebruiken:

1. Maak een webhook in GitHub repository settings
2. Point naar N8N webhook URL
3. Vervang "Schedule Trigger" met "Webhook" node
4. Workflow sync nu direct na elke push

### Notificaties Toevoegen

Voeg een notificatie node toe na "Log Sync Result":

- **Email**: Stuur email bij succesvolle sync
- **Slack**: Stuur Slack bericht
- **Telegram**: Stuur Telegram bericht

### Multiple Workflows Sync

Maak een lijst van workflows om te syncen:

```javascript
const workflows = [
  'zzuper-meta-analysis-workflow.json',
  'other-workflow.json'
];
```

## ✅ Checklist

- [ ] Sync workflow geïmporteerd
- [ ] Sync workflow getest (manual execution)
- [ ] Sync workflow geactiveerd
- [ ] Eerste sync succesvol
- [ ] Monitoring ingesteld
- [ ] Notificaties geconfigureerd (optioneel)

## 🚀 Klaar!

Je workflows worden nu automatisch gesynced vanuit GitHub. Elke wijziging die je pusht naar GitHub wordt automatisch geïmporteerd in N8N binnen 6 uur (of direct met webhook).

