# GitHub Workflow Management Guide

Deze guide legt uit hoe je N8N workflows via GitHub kunt beheren en automatisch synchroniseren.

## 🎯 Voordelen van GitHub Management

1. **Version Control**: Alle workflow wijzigingen zijn getracked in Git
2. **Backup**: Workflows staan veilig in GitHub
3. **Collaboration**: Meerdere mensen kunnen workflows bewerken
4. **Automatische Sync**: Workflows worden automatisch geüpdatet in N8N
5. **Rollback**: Eenvoudig teruggaan naar eerdere versies

## 📋 Workflow Management Opties

### Optie 1: Handmatige Import (Eenvoudigst)

**Wanneer gebruiken:**
- Occasionele updates
- Wanneer je controle wilt over wanneer workflows worden geüpdatet

**Hoe het werkt:**
1. Wijzig workflow lokaal in `zzuper-meta-analysis-workflow.json`
2. Commit en push naar GitHub:
   ```bash
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Update workflow: [beschrijving]"
   git push origin main
   ```
3. In N8N: Import workflow via "Import workflow from file" of "Import workflow from URL"

**Voordelen:**
- ✅ Volledige controle
- ✅ Geen extra setup nodig
- ✅ Eenvoudig te begrijpen

**Nadelen:**
- ❌ Handmatige stap vereist
- ❌ Kan vergeten worden

---

### Optie 2: Automatische Sync Workflow (Aanbevolen)

**Wanneer gebruiken:**
- Regelmatige updates
- Wanneer workflows vaak worden aangepast
- Wanneer je automatische synchronisatie wilt

**Hoe het werkt:**
1. Import de "Sync Workflows from GitHub" workflow in N8N
2. Deze workflow checkt elke 6 uur of er updates zijn in GitHub
3. Als er updates zijn, worden workflows automatisch geïmporteerd/geüpdatet

**Setup:**
1. Import `workflow-sync-workflow.json` in N8N
2. Activeer de workflow
3. Workflow draait automatisch elke 6 uur

**Voordelen:**
- ✅ Volledig automatisch
- ✅ Geen handmatige stappen
- ✅ Altijd up-to-date

**Nadelen:**
- ❌ Vereist extra setup
- ❌ Kan onverwachte updates veroorzaken

---

### Optie 3: GitHub Webhook (Geavanceerd)

**Wanneer gebruiken:**
- Real-time synchronisatie nodig
- Wanneer je directe updates wilt na elke push

**Hoe het werkt:**
1. Configureer GitHub Webhook die N8N triggert bij elke push
2. N8N workflow haalt automatisch de nieuwe workflow op
3. Importeert/updateert de workflow direct

**Setup:**
1. Maak een webhook in GitHub repository settings
2. Point naar N8N webhook URL
3. Configureer workflow om webhook te ontvangen

**Voordelen:**
- ✅ Real-time updates
- ✅ Direct na elke push

**Nadelen:**
- ❌ Complexere setup
- ❌ Vereist publieke webhook URL

---

## 🚀 Aanbevolen Aanpak

Voor de meeste gebruikers is **Optie 1 (Handmatige Import)** het beste:

1. **Workflow Development:**
   - Wijzig lokaal in `zzuper-meta-analysis-workflow.json`
   - Test lokaal (indien mogelijk)
   - Commit met duidelijke message

2. **Deployment:**
   - Push naar GitHub
   - Import handmatig in N8N via "Import workflow from file"
   - Test in N8N
   - Activeer workflow

3. **Versioning:**
   - Gebruik Git tags voor belangrijke versies:
     ```bash
     git tag -a v1.0.0 -m "Stable version"
     git push origin v1.0.0
     ```

## 📝 Best Practices

1. **Commit Messages:**
   - Gebruik duidelijke commit messages
   - Bijvoorbeeld: "Fix: Update video download URL extraction"
   - Of: "Feature: Add AI config dynamic prompts"

2. **Branching:**
   - Gebruik branches voor experimentele wijzigingen
   - Merge naar `main` alleen na testing

3. **Testing:**
   - Test workflows altijd na import
   - Gebruik "Execute Workflow" om te testen
   - Check execution logs voor errors

4. **Backup:**
   - Export workflows regelmatig uit N8N
   - Push naar GitHub als backup

## 🔄 Workflow Update Proces

### Stap 1: Lokaal Wijzigen
```bash
# Edit workflow file
code zzuper-meta-analysis-workflow.json

# Test lokaal (indien mogelijk)
```

### Stap 2: Commit & Push
```bash
git add zzuper-meta-analysis-workflow.json
git commit -m "Update: [beschrijving van wijziging]"
git push origin main
```

### Stap 3: Import in N8N
1. Open N8N
2. Command palette (⌘K)
3. "Import workflow from file"
4. Selecteer `zzuper-meta-analysis-workflow.json`
5. Of gebruik "Import workflow from URL" met GitHub raw URL

### Stap 4: Test & Activate
1. Test workflow met "Execute Workflow"
2. Check execution logs
3. Activeer workflow als alles werkt

## 🛠️ Troubleshooting

### Probleem: "Unauthorized" bij GitHub URL import
**Oplossing:** Gebruik "Import workflow from file" in plaats van URL

### Probleem: Workflow import faalt
**Oplossing:** 
- Check of JSON valid is: `cat zzuper-meta-analysis-workflow.json | jq .`
- Check N8N logs voor specifieke errors

### Probleem: Credentials worden niet meegenomen
**Oplossing:** 
- Credentials worden niet geëxporteerd in workflow JSON (veiligheid)
- Configureer credentials handmatig na import

## 📚 Referenties

- [N8N Workflow Export/Import Docs](https://docs.n8n.io/workflows/export-import/)
- [GitHub Raw Content URLs](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file#viewing-or-downloading-raw-file-content)

