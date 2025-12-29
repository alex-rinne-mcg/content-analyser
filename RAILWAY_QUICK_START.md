# Railway Quick Start - 5 Minuten Setup

Snelle setup guide om N8N op Railway te deployen met ondersteuning voor grote video bestanden.

## ⚡ Snelle Stappen

### 1. Railway Account (2 minuten)
- Ga naar https://railway.app/signup
- Login met GitHub
- Kies Hobby Plan ($5/maand)

### 2. Project Aanmaken (1 minuut)
- Klik "New Project"
- Kies "Deploy from GitHub repo"
- Selecteer deze repository

### 3. Environment Variables (2 minuten)
In Railway → Variables tab, voeg toe:

```bash
N8N_DEFAULT_BINARY_DATA_MODE=filesystem
N8N_BINARY_DATA_STORAGE_PATH=/home/node/.n8n/binaryData
```

**Optioneel (aanbevolen):**
```bash
# Genereer encryption key:
./generate-encryption-key.sh

# Voeg toe aan Railway:
N8N_ENCRYPTION_KEY=<gegenereerde-key>
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=<sterk-wachtwoord>
```

### 4. Deploy (automatisch)
- Railway start automatisch build
- Wacht 2-5 minuten
- Klik op de gegenereerde URL

### 5. Eerste Login
- Maak admin account aan
- Of gebruik Basic Auth credentials

### 6. Workflow Importeren
- Ga naar Workflows
- Import `zzuper-meta-analysis-workflow.json`
- Configureer credentials

## ✅ Klaar!

Je N8N draait nu op Railway met ondersteuning voor 50-100MB video's!

## 📚 Meer Details?

Zie [RAILWAY_SETUP.md](RAILWAY_SETUP.md) voor volledige documentatie.

