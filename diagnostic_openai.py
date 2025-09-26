#!/usr/bin/env python3
"""
Test de diagnostic pour l'API OpenAI
"""

import os
import ssl

import requests


def test_openai_diagnostic():
    """Test diagnostic complet pour OpenAI"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY non définie")
        return False

    print(f"🔑 Clé API: {api_key[:10]}...{api_key[-4:]}")

    # Test 1: Résolution DNS
    print("\n1. Test résolution DNS...")
    try:
        import socket

        ip = socket.gethostbyname("api.openai.com")
        print(f"✅ DNS résolu: {ip}")
    except Exception as e:
        print(f"❌ Erreur DNS: {e}")
        return False

    # Test 2: Connexion HTTPS basique
    print("\n2. Test connexion HTTPS basique...")
    try:
        response = requests.get("https://api.openai.com", timeout=10)
        print(f"✅ Connexion réussie, status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

    # Test 3: Test avec différents paramètres SSL
    print("\n3. Test API avec SSL strict...")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Test"}],
        "max_tokens": 5,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        print(f"✅ Réponse API: {response.status_code}")
        if response.status_code != 200:
            print(f"📄 Réponse complète: {response.text}")
        return True
    except requests.exceptions.SSLError as e:
        print(f"❌ Erreur SSL: {e}")
        print("\n4. Test sans vérification SSL...")
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
                verify=False,
            )
            print(f"✅ Sans SSL: {response.status_code}")
            if response.status_code != 200:
                print(f"📄 Réponse: {response.text}")
        except Exception as e2:
            print(f"❌ Toujours erreur: {e2}")
            return False
    except Exception as e:
        print(f"❌ Autre erreur: {e}")
        return False


if __name__ == "__main__":
    test_openai_diagnostic()
