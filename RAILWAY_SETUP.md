# Railway Setup Guide voor N8N

Deze guide helpt je om N8N te deployen op Railway met ondersteuning voor grote video bestanden (50-100MB).

## 📋 Vereisten

1. Railway account: https://railway.app/signup
2. GitHub account (voor version control)
3. Je N8N workflows (al in deze repository)

## 🚀 Stap 1: Railway Account Aanmaken

1. Ga naar https://railway.app/signup
2. Kies "Login with GitHub" (aanbevolen)
3. Selecteer het **Hobby Plan** ($5/maand) om te starten
4. Bevestig je account

## 🚀 Stap 2: Nieuw Project Aanmaken

1. In Railway dashboard, klik op **"New Project"**
2. Kies **"Deploy from GitHub repo"**
3. Selecteer deze repository (`N8N - Content analyzer`)
4. Railway detecteert automatisch de `Dockerfile`

## 🚀 Stap 3: Environment Variables Instellen

In Railway dashboard, ga naar je project → **Variables** tab en voeg toe:

### Verplichte Variables:

```bash
N8N_DEFAULT_BINARY_DATA_MODE=filesystem
N8N_BINARY_DATA_STORAGE_PATH=/home/node/.n8n/binaryData
```

### Optionele maar Aanbevolen Variables:

```bash
# Webhook URL (Railway genereert dit automatisch na eerste deploy)
WEBHOOK_URL=https://jouw-project.railway.app/

# Encryption key voor credentials (genereer een random string)
N8N_ENCRYPTION_KEY=je-random-encryption-key-hier

# Basic Auth (beveiliging)
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=je-sterke-wachtwoord-hier
```

### Hoe Environment Variables Toevoegen:

1. Ga naar je project in Railway
2. Klik op **"Variables"** tab
3. Klik op **"New Variable"**
4. Voeg elke variable toe (Name en Value)
5. Railway herstart automatisch na wijzigingen

## 🚀 Stap 4: Deploy

1. Railway start automatisch de build na het koppelen van GitHub
2. Wacht tot de build klaar is (2-5 minuten)
3. Railway genereert automatisch een public URL
4. Klik op de URL om N8N te openen

## 🔧 Stap 5: N8N Configureren

### Eerste Setup:

1. Open de Railway URL in je browser
2. Maak een admin account aan (als Basic Auth niet actief is)
3. Of log in met Basic Auth credentials

### Workflows Importeren:

1. Ga naar **Workflows** in N8N
2. Klik op **"Import from File"**
3. Upload `zzuper-meta-analysis-workflow.json`
4. Controleer of alle nodes correct zijn

### Credentials Migreren:

1. Export credentials van N8N Cloud (als mogelijk)
2. Of handmatig opnieuw instellen in Railway N8N:
   - **Meta Graph API** credential
   - **Google Service Account** credential
   - **Gemini API** credential

## 📊 Stap 6: Storage Configureren

Railway gebruikt automatisch volumes voor persistent storage. Voor grote video's:

1. Ga naar je project → **Settings**
2. Check **"Volume"** sectie
3. Railway wijst automatisch storage toe
4. Voor zware workloads, overweeg upgrade naar Pro plan

## ✅ Verificatie

Test of filesystem mode werkt:

1. Voer je workflow uit met een video post
2. Check de execution logs
3. Geen memory errors = succes! ✅

## 🔄 Migratie van N8N Cloud

### Workflows:

1. Export workflows van N8N Cloud:
   - Ga naar elke workflow
   - Klik op **"Download"** of gebruik N8N API
2. Import in Railway N8N:
   - **Import from File** in Railway N8N

### Credentials:

1. Noteer alle credentials die je gebruikt
2. Herstel ze handmatig in Railway N8N
3. Test elke credential

### Data:

- Workflow data wordt automatisch opgeslagen in Railway volumes
- Binary data (videos) worden opgeslagen in `binaryData` directory

## 💰 Kosten Monitoring

1. Ga naar Railway dashboard → **Usage**
2. Monitor je resource gebruik
3. Hobby plan heeft $5 gratis tegoed per maand
4. Upgrade naar Pro ($20/maand) als nodig

## 🐛 Troubleshooting

### Build Fails:

- Check Railway logs voor errors
- Verifieer dat `Dockerfile` correct is
- Check environment variables

### Memory Errors:

- Verifieer `N8N_DEFAULT_BINARY_DATA_MODE=filesystem` is ingesteld
- Check Railway logs
- Overweeg upgrade naar Pro plan voor meer RAM

### Workflows Werken Niet:

- Check credentials zijn correct ingesteld
- Verifieer webhook URLs zijn bijgewerkt
- Check execution logs voor errors

## 📚 Handige Links

- Railway Docs: https://docs.railway.app
- N8N Docs: https://docs.n8n.io
- Railway Pricing: https://railway.app/pricing

## 🎉 Klaar!

Je N8N instance draait nu op Railway met ondersteuning voor grote video bestanden!

