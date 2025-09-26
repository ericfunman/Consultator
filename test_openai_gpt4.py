#!/usr/bin/env python3
"""
Script de test pour le service OpenAI GPT-4
"""

import os
import sys

sys.path.append("app")

from services.ai_openai_service import OpenAIChatGPTService
from services.ai_openai_service import is_grok_available


def test_openai_api_key():
    """Test simple de la validité de la clé API"""

    print("� Test de la clé API OpenAI...")

    try:
        service = OpenAIChatGPTService()
        # Test simple avec un message court
        service._call_openai_api("Bonjour, réponds simplement 'OK'")
        print("✅ Clé API OpenAI valide !")
        return True
    except Exception as e:
        print(f"❌ Clé API OpenAI invalide: {e}")
        return False

    # Test avec un CV exemple
    test_cv = """
    Jean DUPONT
    Développeur Python Senior - 8 ans d'expérience

    EXPÉRIENCE PROFESSIONNELLE

    TechCorp (2020 - Présent)
    Architecte Logiciel Senior
    - Conception et développement d'applications web avec Python/Django
    - Gestion d'équipes de 5 développeurs
    - Migration vers microservices avec Docker/Kubernetes
    - Technologies: Python, Django, PostgreSQL, Redis, Docker, AWS

    DataSys (2018 - 2020)
    Développeur Full-Stack
    - Développement d'applications data avec React/Python
    - Analyse de données avec Pandas/NumPy
    - APIs REST avec FastAPI
    - Technologies: Python, React, SQL, Git

    FORMATION
    Master Informatique - Université Paris-Saclay (2018)
    Licence Mathématiques - Université Paris-Saclay (2016)

    COMPÉTENCES TECHNIQUES
    - Langages: Python (expert), JavaScript, SQL
    - Frameworks: Django, React, FastAPI
    - Outils: Docker, Kubernetes, Git, AWS
    - Base de données: PostgreSQL, MongoDB

    LANGUES
    - Français: langue maternelle
    - Anglais: courant (TOEIC 950)
    - Espagnol: intermédiaire

    CONTACT
    Email: jean.dupont@email.com
    Téléphone: +33 6 12 34 56 78
    """

    try:
        print("🚀 Test d'analyse CV...")
        service = OpenAIChatGPTService()
        result = service.analyze_cv(test_cv)

        print("✅ Analyse réussie !")
        print(f"📊 Méthode: {result.get('_metadata', {}).get('analyzed_by', 'N/A')}")
        print(f"🤖 Modèle: {result.get('_metadata', {}).get('model_used', 'N/A')}")

        # Afficher un résumé des résultats
        if "consultant_info" in result:
            info = result["consultant_info"]
            print(f"👤 Consultant: {info.get('prenom', '')} {info.get('nom', '')}")

        if "missions" in result and result["missions"]:
            print(f"💼 Missions détectées: {len(result['missions'])}")

        if "competences" in result and "techniques" in result["competences"]:
            print(
                f"🛠️ Compétences techniques: {len(result['competences']['techniques'])}"
            )

        # Estimation du coût
        cost = service.get_cost_estimate(len(test_cv))
        print(f"💰 Coût estimé: ${cost:.4f}")

        return True

    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False


if __name__ == "__main__":
    success = test_openai_api_key()
    sys.exit(0 if success else 1)
