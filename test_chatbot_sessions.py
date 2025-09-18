#!/usr/bin/env python3
"""
Test du chatbot après corrections des sessions
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from services.chatbot_service import ChatbotService


def test_chatbot():
    """Test du service chatbot"""

    print("🤖 Test du service ChatBot après corrections...")

    try:
        # Initialiser le service
        chatbot = ChatbotService()
        print("✅ ChatbotService initialisé avec succès")

        # Tester la requête qui causait l'erreur
        test_query = "qui maitrise docker"
        print(f"\n📝 Test de la requête: '{test_query}'")

        response = chatbot.get_response(test_query)
        print(f"✅ Réponse reçue:")
        print(f"📄 Longueur: {len(response)} caractères")
        print(f"🔤 Début: {response[:200]}...")

        # Tester d'autres requêtes
        test_queries = [
            "qui connait python",
            "consultants avec 5 ans d'expérience",
            "missions en cours",
        ]

        for query in test_queries:
            print(f"\n📝 Test: '{query}'")
            try:
                response = chatbot.get_response(query)
                print(f"✅ Réponse OK ({len(response)} caractères)")
            except Exception as exc:
                print(f"❌ Erreur: {exc}")

        print("\n🎉 Tests terminés avec succès !")

    except Exception as exc:
        print(f"❌ Erreur lors des tests: {exc}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_chatbot()
