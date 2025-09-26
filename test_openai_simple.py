#!/usr/bin/env python3
"""
Script de test simple pour la clé API OpenAI
"""

import os

import requests


def test_openai_key():
    """Test basique de la clé API OpenAI"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY non définie")
        return False

    print(f"🔑 Test de la clé API: {api_key[:10]}...{api_key[-4:]}")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-3.5-turbo",  # Utilisons GPT-3.5 pour le test, plus économique
        "messages": [{"role": "user", "content": "Bonjour"}],
        "max_tokens": 10,
    }

    try:
        print("📡 Envoi de la requête de test...")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
            verify=False,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ Succès ! Réponse: {content.strip()}")
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False


if __name__ == "__main__":
    success = test_openai_key()
    exit(0 if success else 1)
