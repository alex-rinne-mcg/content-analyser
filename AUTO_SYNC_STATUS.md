# GitHub Auto-Sync Status

## ✅ Voltooid

1. **Workflow ID gevonden**: `FOanQ6fVJVYw5jAG`
   - Workflow: ZZUPER Meta Post Analysis
   - Locatie: Regel 919 in `zzuper-meta-analysis-workflow.json`

2. **GitHub Action workflow bestaat**: `.github/workflows/update-n8n.yml`
   - Configured om te triggeren bij push naar `main` branch
   - Alleen wanneer `zzuper-meta-analysis-workflow.json` is gewijzigd
   - Gebruikt PUT request naar N8N REST API

3. **Documentatie aangemaakt**:
   - `GITHUB_AUTO_SYNC_QUICK_SETUP.md` - Quick reference guide
   - `verify_github_secrets.py` - Verificatie script

## ⏳ Nog Te Doen (Handmatig in GitHub UI)

### Stap 1: Configureer GitHub Secrets

Ga naar: https://github.com/alex-rinne-mcg/content-analyser/settings/secrets/actions

#### Secret 1: N8N_BASE_URL
- **Name**: `N8N_BASE_URL`
- **Value**: `https://content-analyser-production.up.railway.app`
- Klik "Add secret"

#### Secret 2: N8N_API_KEY
- **Name**: `N8N_API_KEY`
- **Value**: (Genereer in N8N)
  1. Open: https://content-analyser-production.up.railway.app
  2. Log in: `alex@mediaconsultinggroup.nl` / `N8NRailway2024!`
  3. Ga naar: **Settings** → **API** → **Create API Key**
  4. Name: `GitHub Action Sync`
  5. Kopieer de API key (wordt maar één keer getoond!)
  6. Plak in GitHub Secret
- Klik "Add secret"

#### Secret 3: N8N_WORKFLOW_ID
- **Name**: `N8N_WORKFLOW_ID`
- **Value**: `FOanQ6fVJVYw5jAG`
- Klik "Add secret"

### Stap 2: Verifieer Secrets

Controleer dat alle 3 secrets zichtbaar zijn in de lijst:
- ✅ N8N_BASE_URL
- ✅ N8N_API_KEY
- ✅ N8N_WORKFLOW_ID

### Stap 3: Test de Setup

1. Maak een kleine test wijziging:
   ```bash
   # Bijvoorbeeld: verander de workflow naam tijdelijk
   # In zzuper-meta-analysis-workflow.json, regel 2:
   # "name": "ZZUPER Meta Post Analysis - Test"
   ```

2. Commit en push:
   ```bash
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Test: Verify GitHub Action auto-sync"
   git push origin main
   ```

3. Monitor GitHub Actions:
   - Ga naar: https://github.com/alex-rinne-mcg/content-analyser/actions
   - Je zou een nieuwe workflow run moeten zien: "Update N8N Workflow"
   - Check of deze succesvol is (groen)

4. Verifieer in N8N:
   - Open: https://content-analyser-production.up.railway.app
   - Open de workflow "ZZUPER Meta Post Analysis"
   - Check of je wijzigingen zijn doorgevoerd

## 📚 Referenties

- **Quick Setup**: [GITHUB_AUTO_SYNC_QUICK_SETUP.md](GITHUB_AUTO_SYNC_QUICK_SETUP.md)
- **Gedetailleerde Setup**: [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)
- **Test Guide**: [GITHUB_ACTION_TEST.md](GITHUB_ACTION_TEST.md)
- **Verificatie Script**: `python3 verify_github_secrets.py`

## 🔄 Hoe Het Werkt

```
Git Push → GitHub Action Triggers → Leest workflow JSON → 
PUT Request naar N8N API → Workflow wordt geüpdatet in Railway N8N
```

**Belangrijk:**
- Action triggert alleen bij wijzigingen aan `zzuper-meta-analysis-workflow.json` op `main` branch
- Credentials worden niet meegenomen (veiligheid) - moeten handmatig opnieuw worden toegewezen na sync
- Alleen toegestane velden worden gesynced (name, nodes, connections, settings, staticData)

