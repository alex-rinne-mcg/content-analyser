# Test Instructies voor GitHub Auto-Sync

## ⚠️ Belangrijk: Configureer Eerst GitHub Secrets

**VOORDAT je de test uitvoert**, moet je eerst de GitHub Secrets configureren:

1. Ga naar: https://github.com/alex-rinne-mcg/content-analyser/settings/secrets/actions
2. Configureer alle 3 secrets (zie `GITHUB_AUTO_SYNC_QUICK_SETUP.md`)
3. Verifieer dat alle secrets zichtbaar zijn

## Test Wijziging Gemaakt

Er is een test wijziging gemaakt in `zzuper-meta-analysis-workflow.json`:
- Workflow naam is tijdelijk veranderd naar: "ZZUPER Meta Post Analysis - GitHub Sync Test"

## Test Uitvoeren

### Optie 1: Test Nu (als secrets al zijn geconfigureerd)

```bash
git add zzuper-meta-analysis-workflow.json
git commit -m "Test: Verify GitHub Action auto-sync"
git push origin main
```

### Optie 2: Test Later (na secrets configureren)

1. Configureer eerst GitHub Secrets (zie hierboven)
2. Voer dan de commando's hierboven uit

## Verificatie

Na het pushen:

1. **Monitor GitHub Actions**:
   - Ga naar: https://github.com/alex-rinne-mcg/content-analyser/actions
   - Je zou een nieuwe workflow run moeten zien: "Update N8N Workflow"
   - Status: ✅ Groen = Succesvol, ❌ Rood = Check errors

2. **Verifieer in N8N**:
   - Open: https://content-analyser-production.up.railway.app
   - Open de workflow
   - Check of de naam is veranderd naar "ZZUPER Meta Post Analysis - GitHub Sync Test"

3. **Herstel Test Wijziging** (na verificatie):
   ```bash
   # Verander de naam terug naar origineel
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Revert: Test changes - restore original workflow name"
   git push origin main
   ```

## Troubleshooting

### GitHub Action faalt met "Secrets not set"
- **Oorzaak**: Secrets zijn niet geconfigureerd
- **Oplossing**: Configureer alle 3 secrets in GitHub repository settings

### GitHub Action faalt met HTTP 401
- **Oorzaak**: API key is ongeldig
- **Oplossing**: Genereer nieuwe API key in N8N en update `N8N_API_KEY` secret

### GitHub Action faalt met HTTP 404
- **Oorzaak**: Workflow ID is ongeldig
- **Oplossing**: Verifieer workflow ID: `FOanQ6fVJVYw5jAG`

### Workflow wordt niet geüpdatet
- **Oorzaak**: GitHub Action is niet getriggerd of gefaald
- **Oplossing**: Check GitHub Actions logs voor errors

