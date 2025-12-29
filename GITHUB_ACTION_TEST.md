# GitHub Action Test & Verificatie Guide

Deze guide helpt je om de GitHub Action te testen en te verifiëren dat workflows automatisch worden gesynced van GitHub naar Railway N8N.

## Test Procedure

### Stap 1: Voorbereiding

1. **Verifieer GitHub Secrets:**
   - Ga naar GitHub repository → **Settings** → **Secrets and variables** → **Actions**
   - Check dat alle 3 secrets aanwezig zijn:
     - ✅ `N8N_BASE_URL`
     - ✅ `N8N_API_KEY`
     - ✅ `N8N_WORKFLOW_ID`

2. **Verifieer Workflow Bestand:**
   - Check dat `zzuper-meta-analysis-workflow.json` bestaat
   - Verifieer dat het geldige JSON is:
     ```bash
     cat zzuper-meta-analysis-workflow.json | jq .
     ```
   - Als er een error is, fix de JSON eerst

3. **Noteer Huidige Workflow State:**
   - Open Railway N8N: `https://content-analyser-production.up.railway.app`
   - Open de "ZZUPER Meta Post Analysis" workflow
   - Noteer de workflow naam (voor verificatie later)
   - Of maak een screenshot van de workflow

---

### Stap 2: Maak Test Wijziging

1. **Open het workflow bestand:**
   ```bash
   code zzuper-meta-analysis-workflow.json
   ```

2. **Maak een kleine, veilige wijziging:**
   
   **Optie A: Update workflow naam (aanbevolen voor eerste test)**
   - Zoek naar: `"name": "ZZUPER Meta Post Analysis"`
   - Verander naar: `"name": "ZZUPER Meta Post Analysis - Test"`
   - Dit is veilig en makkelijk te verifiëren

   **Optie B: Voeg comment toe in een node**
   - Zoek naar een Code node
   - Voeg een comment toe: `// Test: GitHub Action sync`
   - Dit is ook veilig

   **Optie C: Update workflow settings**
   - Zoek naar `"settings": {`
   - Voeg toe: `"testSync": true` (tijdelijk)
   - Verwijder dit later weer

3. **Sla het bestand op**

---

### Stap 3: Commit en Push

1. **Check git status:**
   ```bash
   git status
   ```
   - Je zou `zzuper-meta-analysis-workflow.json` moeten zien als modified

2. **Stage het bestand:**
   ```bash
   git add zzuper-meta-analysis-workflow.json
   ```

3. **Commit:**
   ```bash
   git commit -m "Test: Verify GitHub Action auto-sync"
   ```

4. **Push naar GitHub:**
   ```bash
   git push origin main
   ```

---

### Stap 4: Monitor GitHub Action

1. **Ga naar GitHub repository:**
   - Open: `https://github.com/alex-rinne-mcg/content-analyser`

2. **Klik op Actions tab:**
   - Je zou een nieuwe workflow run moeten zien: "Update N8N Workflow"
   - Status kan zijn: ⏳ In progress, ✅ Success, of ❌ Failed

3. **Klik op de workflow run om details te zien**

4. **Check de logs:**
   - Klik op "Update N8N Workflow" job
   - Klik op "Update N8N Workflow" step
   - Je zou moeten zien:
     ```
     Updating N8N workflow...
     Sending request to: https://content-analyser-production.up.railway.app/rest/workflows/[ID]
     ✅ Successfully updated N8N workflow
     ```

---

### Stap 5: Verifieer in N8N

1. **Open Railway N8N:**
   - Ga naar: `https://content-analyser-production.up.railway.app`
   - Log in indien nodig

2. **Open de workflow:**
   - Ga naar **Workflows**
   - Open "ZZUPER Meta Post Analysis" (of de naam die je hebt geüpdatet)

3. **Verifieer wijzigingen:**
   - Check of je wijzigingen zijn doorgevoerd
   - Als je de naam hebt veranderd, check of de nieuwe naam zichtbaar is
   - Als je een comment hebt toegevoegd, check of deze aanwezig is

4. **Check workflow status:**
   - Verifieer dat de workflow nog steeds actief is (als deze actief was)
   - Check of credentials nog steeds zijn toegewezen
   - Verifieer dat nodes nog steeds correct zijn geconfigureerd

---

### Stap 6: Herstel Test Wijziging (Optioneel)

Als je een test wijziging hebt gemaakt die je niet wilt behouden:

1. **Herstel de wijziging:**
   ```bash
   git checkout zzuper-meta-analysis-workflow.json
   ```

2. **Of maak handmatig de wijziging ongedaan:**
   - Verander de naam terug naar origineel
   - Verwijder test comments
   - Verwijder test settings

3. **Commit en push:**
   ```bash
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Revert: Test changes"
   git push origin main
   ```

4. **Verifieer dat de wijziging is teruggedraaid in N8N**

---

## Verificatie Checklist

Gebruik deze checklist om te verifiëren dat alles werkt:

- [ ] GitHub Secrets zijn geconfigureerd
- [ ] Workflow bestand is geldige JSON
- [ ] Test wijziging is gemaakt
- [ ] Wijziging is gecommit en gepusht
- [ ] GitHub Action is getriggerd
- [ ] GitHub Action is succesvol (groen)
- [ ] Workflow is geüpdatet in N8N
- [ ] Wijzigingen zijn zichtbaar in N8N
- [ ] Workflow is nog steeds actief (als deze actief was)
- [ ] Credentials zijn nog steeds toegewezen
- [ ] Nodes zijn nog steeds correct geconfigureerd

---

## Troubleshooting

### Probleem: GitHub Action draait niet

**Symptomen:**
- Geen workflow run verschijnt in Actions tab
- Push naar GitHub maar geen automatische sync

**Oplossingen:**
1. Check of je naar `main` branch pusht
2. Check of `zzuper-meta-analysis-workflow.json` daadwerkelijk is gewijzigd
3. Check GitHub Actions settings:
   - Ga naar **Settings** → **Actions** → **General**
   - Verifieer dat "Allow all actions and reusable workflows" is ingeschakeld
4. Check of de GitHub Action file bestaat: `.github/workflows/update-n8n.yml`

---

### Probleem: GitHub Action faalt met "Secrets not set"

**Symptomen:**
- GitHub Action draait maar faalt met error over missing secrets
- Logs tonen: "❌ Error: N8N_API_KEY secret is not set"

**Oplossingen:**
1. Verifieer dat alle secrets zijn geconfigureerd:
   - `N8N_BASE_URL`
   - `N8N_API_KEY`
   - `N8N_WORKFLOW_ID`
2. Check of secret namen exact kloppen (hoofdletters, underscores)
3. Wacht een paar seconden en probeer opnieuw (GitHub kan tijd nodig hebben)

---

### Probleem: GitHub Action faalt met HTTP 401 (Unauthorized)

**Symptomen:**
- GitHub Action draait maar faalt met HTTP 401
- Logs tonen: "❌ Failed to update N8N workflow" met HTTP Code: 401

**Oplossingen:**
1. Verifieer dat de API key correct is:
   - Genereer een nieuwe API key in N8N
   - Update de `N8N_API_KEY` secret in GitHub
2. Check of de API key niet is geëxpireerd
3. Verifieer dat de API key de juiste permissions heeft

---

### Probleem: GitHub Action faalt met HTTP 404 (Not Found)

**Symptomen:**
- GitHub Action draait maar faalt met HTTP 404
- Logs tonen: "❌ Failed to update N8N workflow" met HTTP Code: 404

**Oplossingen:**
1. Verifieer de workflow ID:
   - Check de URL van de workflow in N8N
   - Of gebruik de N8N REST API om alle workflows op te halen
2. Update de `N8N_WORKFLOW_ID` secret in GitHub
3. Verifieer dat de workflow bestaat in N8N

---

### Probleem: GitHub Action faalt met HTTP 400 (Bad Request)

**Symptomen:**
- GitHub Action draait maar faalt met HTTP 400
- Logs tonen: "❌ Failed to update N8N workflow" met HTTP Code: 400

**Oplossingen:**
1. Verifieer dat de workflow JSON geldig is:
   ```bash
   cat zzuper-meta-analysis-workflow.json | jq .
   ```
2. Check of het bestand de vereiste velden heeft:
   - `name`
   - `nodes`
   - `connections`
3. Fix eventuele JSON syntax errors

---

### Probleem: Workflow wordt geüpdatet maar wijzigingen zijn niet zichtbaar

**Symptomen:**
- GitHub Action is succesvol
- Maar wijzigingen zijn niet zichtbaar in N8N

**Oplossingen:**
1. Refresh de N8N pagina (hard refresh: Cmd+Shift+R of Ctrl+Shift+R)
2. Check of je de juiste workflow bekijkt
3. Verifieer dat de workflow ID correct is
4. Check of er meerdere workflows zijn met dezelfde naam
5. Probeer de workflow opnieuw te openen

---

### Probleem: Credentials zijn verdwenen na sync

**Symptomen:**
- Workflow is geüpdatet
- Maar credentials zijn niet meer toegewezen aan nodes

**Oplossing:**
- Dit is normaal gedrag - credentials worden niet meegenomen in workflow export (veiligheid)
- Assign credentials handmatig opnieuw na import
- Of gebruik een "Configure Credentials" workflow na sync

---

## Succes Criteria

De GitHub Action werkt correct als:

1. ✅ GitHub Action draait automatisch bij push naar `main`
2. ✅ GitHub Action is succesvol (groen)
3. ✅ Workflow wordt geüpdatet in N8N binnen 30 seconden
4. ✅ Wijzigingen zijn zichtbaar in N8N
5. ✅ Workflow blijft actief (als deze actief was)
6. ✅ Nodes blijven correct geconfigureerd

---

## Regelmatige Verificatie

Voer deze checks periodiek uit:

1. **Wekelijks:**
   - Check GitHub Actions logs voor errors
   - Verifieer dat workflows up-to-date zijn

2. **Maandelijks:**
   - Check of API keys nog geldig zijn
   - Update API keys als ze bijna expireren

3. **Bij wijzigingen:**
   - Test altijd na grote workflow wijzigingen
   - Verifieer dat credentials nog steeds werken

---

**Klaar!** Je GitHub Action is nu getest en geverifieerd. Workflows worden automatisch gesynced van GitHub naar Railway N8N.

