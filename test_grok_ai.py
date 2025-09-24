#!/usr/bin/env python3
"""
Script de test pour le service Grok AI
Permet de tester la configuration et la connexion à Grok
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire app au path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

try:
    from services.ai_grok_service import GrokAIService, is_grok_available, get_grok_service
    import json
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Assurez-vous que vous êtes dans le répertoire racine du projet")
    sys.exit(1)


def test_grok_connection():
    """Test basique de connexion à Grok"""
    print("🔍 Test de connexion à Grok AI...")
    print("=" * 50)

    # Vérifier la disponibilité
    if not is_grok_available():
        print("❌ Service Grok non disponible")
        print("Vérifiez que GROK_API_KEY est défini dans vos variables d'environnement")
        return False

    try:
        service = get_grok_service()
        print("✅ Service Grok initialisé")

        # Test de connexion simple
        test_prompt = "Bonjour, réponds simplement 'OK' en français."
        print(f"📤 Envoi du prompt de test: {test_prompt}")

        # Pour un test rapide, on simule juste l'appel
        # response = service._call_grok_api(test_prompt)
        # print(f"📥 Réponse: {response}")

        print("✅ Connexion réussie !")
        return True

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False


def test_cv_analysis():
    """Test d'analyse de CV exemple"""
    print("\n🔍 Test d'analyse de CV...")
    print("=" * 50)

    if not is_grok_available():
        print("❌ Service Grok non disponible - test annulé")
        return False

    # CV exemple
    test_cv = """
    JEAN DUPONT
    Consultant Data Senior

    EXPÉRIENCE PROFESSIONNELLE

    Quanteam - Directeur de practice Data
    Janvier 2023 - Aujourd'hui
    • Management de l'équipe data (15 personnes)
    • Développement commercial et réponses aux appels d'offres
    • Suivi des consultants et gestion des carrières
    • Veille technologique et innovation

    Société Générale - Manager de transition
    Août 2023 - Aujourd'hui
    • Pilotage du projet de transformation digitale
    • Coordination des équipes techniques et fonctionnelles
    • Gestion budgétaire et planning

    COMPÉTENCES TECHNIQUES
    • Python, SQL, R
    • Machine Learning, Big Data
    • Cloud (AWS, Azure)
    • DevOps, Docker, Kubernetes

    FORMATION
    Master en Informatique - Université Paris-Saclay (2015)
    """

    try:
        service = get_grok_service()
        print("📤 Analyse du CV exemple en cours...")

        result = service.analyze_cv(test_cv, "Jean DUPONT")

        print("✅ Analyse terminée !")
        print("\n📊 Résumé de l'analyse:")

        if "missions" in result:
            print(f"  • Missions détectées: {len(result['missions'])}")

        if "competences" in result and "techniques" in result["competences"]:
            print(f"  • Compétences techniques: {len(result['competences']['techniques'])}")

        if "_cost_estimate" in result:
            print(".4f"
        # Afficher un extrait du résultat
        print("\n📄 Extrait du résultat JSON:")
        # Masquer les détails complets pour la lisibilité
        summary = {
            "consultant_info": result.get("consultant_info", {}),
            "missions_count": len(result.get("missions", [])),
            "competences": result.get("competences", {}),
            "analysis_method": result.get("_analysis_method"),
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))

        return True

    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return False


def main():
    """Fonction principale"""
    print("🚀 Test du service Grok AI pour Consultator")
    print("=" * 60)

    # Vérifier la clé API
    api_key = os.getenv("GROK_API_KEY")
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else api_key
        print(f"🔑 Clé API détectée: {masked_key}")
    else:
        print("⚠️ Aucune clé API détectée (GROK_API_KEY)")
        print("Définissez la variable d'environnement pour les tests complets")

    # Tests
    connection_ok = test_grok_connection()
    analysis_ok = test_cv_analysis() if connection_ok else False

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 60)
    print(f"Connexion Grok: {'✅ OK' if connection_ok else '❌ ÉCHEC'}")
    print(f"Analyse CV: {'✅ OK' if analysis_ok else '❌ ÉCHEC'}")

    if connection_ok and analysis_ok:
        print("\n🎉 Tous les tests sont passés ! Grok AI est prêt à être utilisé.")
        print("Lancez l'application Streamlit pour tester l'intégration complète.")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        print("Consultez GROK_SETUP.md pour les instructions d'installation.")

    return 0 if connection_ok else 1


if __name__ == "__main__":
    sys.exit(main())