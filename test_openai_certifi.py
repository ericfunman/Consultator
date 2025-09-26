#!/usr/bin/env python3
"""
Test OpenAI avec certificats corrects
"""

import os

import certifi
import requests


def test_openai_with_certifi():
    """Test OpenAI avec certificats certifi"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY non définie")
        return False

    print(f"🔑 Test avec certificats certifi...")
    print(f"📄 Bundle CA: {certifi.where()}")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Bonjour"}],
        "max_tokens": 5,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
            verify=certifi.where(),  # Utiliser les certificats certifi
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
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    test_openai_with_certifi()
