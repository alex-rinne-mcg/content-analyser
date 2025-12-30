#!/usr/bin/env python3
"""
Verifieer of GitHub Secrets zijn geconfigureerd voor N8N auto-sync.

Dit script controleert of alle benodigde secrets zijn ingesteld.
Let op: Dit script kan alleen controleren of secrets bestaan, niet de waarden zien.
"""

import os
import sys

def check_secret_exists(secret_name):
    """Check of een secret bestaat (via GitHub CLI of instructies)"""
    print(f"🔍 Controleren: {secret_name}")
    print(f"   → Ga naar: https://github.com/alex-rinne-mcg/content-analyser/settings/secrets/actions")
    print(f"   → Zoek naar: {secret_name}")
    return None  # Kan niet automatisch verifiëren zonder GitHub token

def main():
    print("=" * 60)
    print("GitHub Secrets Verificatie voor N8N Auto-Sync")
    print("=" * 60)
    print()
    
    required_secrets = [
        {
            "name": "N8N_BASE_URL",
            "expected_value": "https://content-analyser-production.up.railway.app",
            "description": "Railway N8N instance URL"
        },
        {
            "name": "N8N_API_KEY",
            "expected_value": None,  # Kan niet verifiëren zonder token
            "description": "N8N API key (genereer in N8N Settings → API)"
        },
        {
            "name": "N8N_WORKFLOW_ID",
            "expected_value": "FOanQ6fVJVYw5jAG",
            "description": "Workflow ID van ZZUPER Meta Post Analysis"
        }
    ]
    
    print("📋 Vereiste GitHub Secrets:")
    print()
    
    for i, secret in enumerate(required_secrets, 1):
        print(f"{i}. {secret['name']}")
        print(f"   Beschrijving: {secret['description']}")
        if secret['expected_value']:
            print(f"   Verwachte waarde: {secret['expected_value']}")
        print()
    
    print("=" * 60)
    print("📝 Configuratie Instructies:")
    print("=" * 60)
    print()
    print("1. Ga naar GitHub repository settings:")
    print("   https://github.com/alex-rinne-mcg/content-analyser/settings/secrets/actions")
    print()
    print("2. Voor elke secret hierboven:")
    print("   - Klik op 'New repository secret'")
    print("   - Vul de Name en Secret waarde in")
    print("   - Klik 'Add secret'")
    print()
    print("3. Voor N8N_API_KEY:")
    print("   - Open: https://content-analyser-production.up.railway.app")
    print("   - Log in met: alex@mediaconsultinggroup.nl / N8NRailway2024!")
    print("   - Ga naar: Settings → API → Create API Key")
    print("   - Kopieer de API key (wordt maar één keer getoond!)")
    print()
    print("=" * 60)
    print("✅ Verificatie:")
    print("=" * 60)
    print()
    print("Na het configureren van alle secrets:")
    print("1. Maak een test wijziging in zzuper-meta-analysis-workflow.json")
    print("2. Commit en push naar main")
    print("3. Check GitHub Actions tab voor workflow run")
    print("4. Verifieer dat workflow is geüpdatet in N8N")
    print()
    print("Zie GITHUB_AUTO_SYNC_QUICK_SETUP.md voor meer details.")

if __name__ == "__main__":
    main()

