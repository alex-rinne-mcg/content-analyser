# GitHub Auto-Sync Quick Setup

Snelle setup guide voor automatische synchronisatie van GitHub naar Railway N8N.

## Workflow ID

**Workflow ID**: `FOanQ6fVJVYw5jAG`  
**Workflow Naam**: ZZUPER Meta Post Analysis

## GitHub Secrets Configuratie

Configureer deze 3 secrets in GitHub repository settings:

### 1. N8N_BASE_URL
- **Waarde**: `https://content-analyser-production.up.railway.app`
- **Waar**: GitHub → Settings → Secrets and variables → Actions → New repository secret

### 2. N8N_API_KEY
- **Hoe te verkrijgen**:
  1. Open: `https://content-analyser-production.up.railway.app`
  2. Log in met: `alex@mediaconsultinggroup.nl` / `N8NRailway2024!`
  3. Ga naar: **Settings** → **API** → **Create API Key**
  4. Name: `GitHub Action Sync`
  5. Kopieer de API key (wordt maar één keer getoond!)
- **Waar**: GitHub → Settings → Secrets and variables → Actions → New repository secret

### 3. N8N_WORKFLOW_ID
- **Waarde**: `FOanQ6fVJVYw5jAG`
- **Waar**: GitHub → Settings → Secrets and variables → Actions → New repository secret

## Verificatie Checklist

- [ ] `N8N_BASE_URL` secret geconfigureerd
- [ ] `N8N_API_KEY` secret geconfigureerd (API key gegenereerd in N8N)
- [ ] `N8N_WORKFLOW_ID` secret geconfigureerd
- [ ] Alle 3 secrets zichtbaar in GitHub Secrets lijst

## Test de Setup

1. Maak een kleine wijziging in `zzuper-meta-analysis-workflow.json`
2. Commit en push:
   ```bash
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Test: Verify GitHub Action auto-sync"
   git push origin main
   ```
3. Monitor GitHub Actions tab voor workflow run
4. Verifieer dat workflow is geüpdatet in N8N

## Meer Informatie

- Zie [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) voor gedetailleerde instructies
- Zie [GITHUB_ACTION_TEST.md](GITHUB_ACTION_TEST.md) voor test en troubleshooting

