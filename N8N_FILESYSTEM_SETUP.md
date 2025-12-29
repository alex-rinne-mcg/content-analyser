# N8N Filesystem Mode Setup Guide

## Overzicht

Om grote video bestanden (50-100MB) te verwerken zonder memory issues, moet N8N geconfigureerd worden om binary data op de filesystem op te slaan in plaats van in memory.

**Environment Variable**: `N8N_DEFAULT_BINARY_DATA_MODE=filesystem`

## Installatie Methoden

### Methode 1: Docker (meest gebruikelijk)

#### Docker Compose

1. Open je `docker-compose.yml` bestand
2. Voeg de environment variable toe aan de N8N service:

```yaml
services:
  n8n:
    image: n8nio/n8n
    environment:
      - N8N_DEFAULT_BINARY_DATA_MODE=filesystem
      # ... andere environment variables
    volumes:
      - ./n8n_data:/home/node/.n8n  # Zorg dat deze volume bestaat
```

3. Herstart de container:
```bash
docker-compose down
docker-compose up -d
```

#### Docker Run Command

Als je N8N start met `docker run`:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e N8N_DEFAULT_BINARY_DATA_MODE=filesystem \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Methode 2: Systemd Service

1. Open je systemd service file (meestal `/etc/systemd/system/n8n.service` of `~/.config/systemd/user/n8n.service`)

2. Voeg de environment variable toe in de `[Service]` sectie:

```ini
[Unit]
Description=n8n workflow automation
After=network.target

[Service]
Type=simple
User=your-username
Environment="N8N_DEFAULT_BINARY_DATA_MODE=filesystem"
ExecStart=/usr/bin/n8n start
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Herlaad systemd en herstart de service:
```bash
sudo systemctl daemon-reload
sudo systemctl restart n8n
# Of voor user service:
systemctl --user daemon-reload
systemctl --user restart n8n
```

### Methode 3: NPM/Node.js Installatie

Als je N8N via npm hebt geïnstalleerd:

1. Maak of bewerk een `.env` bestand in je N8N directory (meestal `~/.n8n/.env`)

2. Voeg toe:
```
N8N_DEFAULT_BINARY_DATA_MODE=filesystem
```

3. Herstart N8N:
```bash
# Stop N8N (Ctrl+C of kill process)
# Start opnieuw
n8n start
```

### Methode 4: N8N Cloud

Als je N8N Cloud gebruikt:

1. Ga naar je N8N Cloud dashboard
2. Navigeer naar **Settings** → **Environment Variables**
3. Voeg nieuwe variable toe:
   - **Name**: `N8N_DEFAULT_BINARY_DATA_MODE`
   - **Value**: `filesystem`
4. Sla op en herstart je instance (indien nodig)

### Methode 5: Kubernetes

Als je N8N in Kubernetes draait:

1. Update je Deployment of StatefulSet:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n
spec:
  template:
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n
        env:
        - name: N8N_DEFAULT_BINARY_DATA_MODE
          value: "filesystem"
        volumeMounts:
        - name: n8n-data
          mountPath: /home/node/.n8n
      volumes:
      - name: n8n-data
        persistentVolumeClaim:
          claimName: n8n-pvc
```

2. Apply de wijzigingen:
```bash
kubectl apply -f n8n-deployment.yaml
kubectl rollout restart deployment/n8n
```

## Verificatie

Na het instellen, controleer of de configuratie werkt:

1. **Check environment variable**:
   - Ga naar N8N UI → Settings → Environment Variables
   - Controleer of `N8N_DEFAULT_BINARY_DATA_MODE=filesystem` zichtbaar is

2. **Test met een workflow**:
   - Maak een test workflow die een groot bestand downloadt
   - Controleer de N8N logs voor errors
   - Check of bestanden worden opgeslagen in `~/.n8n/.n8n/binaryData/` (of je data directory)

3. **Check logs**:
   ```bash
   # Docker
   docker logs n8n
   
   # Systemd
   journalctl -u n8n -f
   ```

## Belangrijke Notities

- **Disk Space**: Zorg dat je voldoende disk space hebt, want video's worden nu op disk opgeslagen
- **Permissions**: Zorg dat N8N schrijfrechten heeft op de data directory
- **Performance**: Filesystem mode is iets langzamer dan memory mode, maar voorkomt OOM errors
- **Cleanup**: Oude binary data wordt automatisch opgeschoond door N8N, maar je kunt handmatig opruimen in `~/.n8n/.n8n/binaryData/`

## Troubleshooting

**Problem**: Environment variable wordt niet herkend
- **Solution**: Zorg dat je N8N volledig herstart na het toevoegen van de variable

**Problem**: Permission denied errors
- **Solution**: Check file permissions op de data directory:
  ```bash
  chown -R n8n-user:n8n-group ~/.n8n
  chmod -R 755 ~/.n8n
  ```

**Problem**: Nog steeds memory issues
- **Solution**: 
  - Verifieer dat de variable correct is ingesteld
  - Check N8N logs voor bevestiging
  - Overweeg om N8N memory limits te verhogen als backup

## Meer Informatie

- [N8N Binary Data Documentation](https://docs.n8n.io/hosting/scaling/binary-data/)
- [N8N Environment Variables](https://docs.n8n.io/hosting/configuration/environment-variables/)

