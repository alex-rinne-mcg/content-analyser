# GitHub Secrets Setup Guide

Deze guide legt uit hoe je GitHub Secrets configureert voor automatische workflow sync van GitHub naar Railway N8N.

## Overzicht

De GitHub Action heeft 3 secrets nodig om automatisch workflows te syncen:
1. `N8N_BASE_URL` - De URL van je Railway N8N instance
2. `N8N_API_KEY` - Een API key gegenereerd in N8N
3. `N8N_WORKFLOW_ID` - De ID van de workflow die je wilt syncen

## Stap 1: Configureer N8N_BASE_URL

1. Ga naar je GitHub repository: `https://github.com/alex-rinne-mcg/content-analyser`
2. Klik op **Settings** (bovenaan de repository)
3. Klik op **Secrets and variables** → **Actions** (in het linker menu)
4. Klik op **New repository secret**
5. Vul in:
   - **Name**: `N8N_BASE_URL`
   - **Secret**: `https://content-analyser-production.up.railway.app`
6. Klik **Add secret**

**Verificatie:**
- Je ziet nu `N8N_BASE_URL` in de lijst van secrets
- De waarde is verborgen (veiligheid)

---

## Stap 2: Genereer en Configureer N8N_API_KEY

### 2.1: Genereer API Key in N8N

1. Open je Railway N8N instance: `https://content-analyser-production.up.railway.app`
2. Log in met je credentials
3. Ga naar **Settings** (linker menu, onderaan)
4. Klik op **API** (in de settings menu)
5. Klik op **Create API Key**
6. Vul in:
   - **Name**: `GitHub Action Sync` (of een andere beschrijvende naam)
   - **Expires**: Kies een datum (of laat leeg voor geen expiratie)
7. Klik **Create**
8. **BELANGRIJK**: Kopieer de API key direct - deze wordt maar één keer getoond!
9. Sla de key op in een veilige plek (password manager)

### 2.2: Voeg API Key toe aan GitHub Secrets

1. Ga terug naar GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Klik op **New repository secret**
3. Vul in:
   - **Name**: `N8N_API_KEY`
   - **Secret**: Plak de API key die je net hebt gekopieerd
4. Klik **Add secret**

**Verificatie:**
- Je ziet nu `N8N_API_KEY` in de lijst van secrets
- De waarde is verborgen (veiligheid)

**Belangrijk:**
- Als je de API key verliest, moet je een nieuwe genereren in N8N
- Oude API keys blijven werken tot ze expireren (als je een expiratie hebt ingesteld)

---

## Stap 3: Vind en Configureer N8N_WORKFLOW_ID

### Methode 1: Via Workflow URL (Eenvoudigst)

1. Open je Railway N8N instance: `https://content-analyser-production.up.railway.app`
2. Open de workflow die je wilt syncen (bijvoorbeeld "ZZUPER Meta Post Analysis")
3. Kijk naar de URL in je browser:
   ```
   https://content-analyser-production.up.railway.app/workflow/[WORKFLOW_ID]
   ```
4. Kopieer de `[WORKFLOW_ID]` uit de URL
   - Dit is meestal een nummer zoals `1`, `2`, `3`, etc.
   - Of een UUID zoals `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### Methode 2: Via N8N REST API

Als je de workflow ID niet uit de URL kunt halen:

1. Open een terminal
2. Voer uit (vervang `YOUR_API_KEY` met je N8N API key):
   ```bash
   curl -H "X-N8N-API-KEY: YOUR_API_KEY" \
     "https://content-analyser-production.up.railway.app/rest/workflows"
   ```
3. Zoek in de response naar je workflow naam
4. Kopieer de `id` waarde van die workflow

### Methode 3: Via Browser Developer Tools

1. Open je Railway N8N instance
2. Open Developer Tools (F12 of Cmd+Option+I)
3. Ga naar **Network** tab
4. Open de workflow die je wilt syncen
5. Zoek naar een request naar `/rest/workflows`
6. Klik op de request en bekijk de response
7. Zoek je workflow naam en kopieer de `id`

### 3.2: Voeg Workflow ID toe aan GitHub Secrets

1. Ga naar GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Klik op **New repository secret**
3. Vul in:
   - **Name**: `N8N_WORKFLOW_ID`
   - **Secret**: Plak de workflow ID die je hebt gevonden
4. Klik **Add secret**

**Verificatie:**
- Je ziet nu `N8N_WORKFLOW_ID` in de lijst van secrets
- De waarde is verborgen (veiligheid)

---

## Stap 4: Verifieer Alle Secrets

Controleer dat alle 3 secrets zijn geconfigureerd:

1. Ga naar **Settings** → **Secrets and variables** → **Actions**
2. Je zou moeten zien:
   - ✅ `N8N_BASE_URL`
   - ✅ `N8N_API_KEY`
   - ✅ `N8N_WORKFLOW_ID`

**Als een secret ontbreekt:**
- Volg de stappen hierboven om het toe te voegen

---

## Stap 5: Test de Configuratie

### 5.1: Test via GitHub Action

1. Maak een kleine wijziging in `zzuper-meta-analysis-workflow.json`
   - Bijvoorbeeld: voeg een comment toe of verander de workflow naam tijdelijk
2. Commit en push:
   ```bash
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Test: Verify GitHub Action auto-sync"
   git push origin main
   ```
3. Ga naar GitHub repository → **Actions** tab
4. Je zou een nieuwe workflow run moeten zien: "Update N8N Workflow"
5. Klik op de run om de logs te bekijken
6. Check of de workflow succesvol is:
   - ✅ Groen = Succesvol
   - ❌ Rood = Check de error logs

### 5.2: Verifieer in N8N

1. Open je Railway N8N instance
2. Open de workflow die je hebt geüpdatet
3. Verifieer dat je wijzigingen zijn doorgevoerd
4. Check de workflow naam, nodes, of andere wijzigingen die je hebt gemaakt

---

## Troubleshooting

### Probleem: "N8N_API_KEY secret is not set"

**Oorzaak:** Secret is niet geconfigureerd of heeft verkeerde naam

**Oplossing:**
1. Check of de secret exact `N8N_API_KEY` heet (hoofdletters, underscores)
2. Check of de secret is toegevoegd in **Settings** → **Secrets and variables** → **Actions**
3. Als je de secret hebt toegevoegd, wacht even en probeer opnieuw (GitHub kan een paar seconden nodig hebben)

### Probleem: "Failed to update N8N workflow" (HTTP 401)

**Oorzaak:** API key is ongeldig of heeft geen permissions

**Oplossing:**
1. Genereer een nieuwe API key in N8N
2. Update de `N8N_API_KEY` secret in GitHub
3. Verifieer dat de API key de juiste permissions heeft (workflow read/write)

### Probleem: "Failed to update N8N workflow" (HTTP 404)

**Oorzaak:** Workflow ID is ongeldig of workflow bestaat niet

**Oplossing:**
1. Verifieer de workflow ID via Methode 1, 2 of 3 hierboven
2. Check of de workflow bestaat in N8N
3. Update de `N8N_WORKFLOW_ID` secret in GitHub

### Probleem: "Failed to update N8N workflow" (HTTP 400)

**Oorzaak:** Workflow JSON is ongeldig of mist vereiste velden

**Oplossing:**
1. Check of `zzuper-meta-analysis-workflow.json` geldige JSON is
2. Verifieer dat het bestand de vereiste velden heeft: `name`, `nodes`, `connections`
3. Test de JSON met: `cat zzuper-meta-analysis-workflow.json | jq .`

### Probleem: GitHub Action draait niet

**Oorzaak:** Workflow file is niet gewijzigd of push is naar verkeerde branch

**Oplossing:**
1. Check of je naar `main` branch pusht
2. Check of `zzuper-meta-analysis-workflow.json` daadwerkelijk is gewijzigd
3. Check of de GitHub Action is geactiveerd in **Settings** → **Actions** → **General**

---

## Veiligheid

### Best Practices

1. **Deel API keys nooit publiekelijk**
   - API keys zijn secrets en moeten privé blijven
   - Commit nooit API keys in code

2. **Roteer API keys regelmatig**
   - Genereer nieuwe API keys periodiek
   - Verwijder oude API keys die niet meer worden gebruikt

3. **Gebruik expiratie voor API keys**
   - Stel een expiratie datum in voor API keys
   - Dit voorkomt dat oude keys voor altijd werken

4. **Beperk API key permissions**
   - Gebruik API keys alleen voor wat nodig is
   - N8N API keys hebben standaard workflow read/write permissions

---

## Volgende Stappen

Na het configureren van alle secrets:

1. ✅ Test de GitHub Action (zie Stap 5)
2. ✅ Verifieer dat workflows automatisch worden gesynced
3. ✅ Check de GitHub Actions logs regelmatig voor errors
4. ✅ Update API keys als ze expireren

---

## Checklist

- [ ] `N8N_BASE_URL` secret geconfigureerd
- [ ] `N8N_API_KEY` secret geconfigureerd (API key gegenereerd in N8N)
- [ ] `N8N_WORKFLOW_ID` secret geconfigureerd (workflow ID gevonden)
- [ ] Alle 3 secrets zichtbaar in GitHub Secrets
- [ ] GitHub Action getest met kleine wijziging
- [ ] Workflow succesvol geüpdatet in N8N
- [ ] Wijzigingen geverifieerd in N8N

---

**Klaar!** Je GitHub repository is nu gelinkt met Railway N8N. Elke wijziging aan `zzuper-meta-analysis-workflow.json` wordt automatisch gesynced naar N8N.

