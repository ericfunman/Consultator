#!/usr/bin/env python3
"""
Service d'analyse IA avec Grok (xAI)
Utilise l'API Grok pour analyser les CV et extraire les informations pertinentes
"""

import json
import logging
import os
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import requests
import streamlit as st

logger = logging.getLogger(__name__)


class GrokAIService:
    """Service d'analyse IA utilisant Grok (xAI)"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le service Grok

        Args:
            api_key: Clé API Grok. Si None, utilise la variable d'environnement
        """
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"  # Modèle Grok actuel

        if not self.api_key:
            raise ValueError("❌ Clé API Grok manquante. Configurez GROK_API_KEY")

    def analyze_cv(self, document_text: str) -> Dict[str, Any]:
        """
        Analyse un CV avec Grok et retourne les informations structurées

        Args:
            document_text: Texte brut du CV
            consultant_name: Nom du consultant (optionnel)

        Returns:
            Dictionnaire avec les informations extraites
        """
        try:
            # Construire le prompt d'analyse
            prompt = self._build_analysis_prompt(document_text)

            # Appeler l'API Grok
            response = self._call_grok_api(prompt)

            # Parser et valider la réponse
            return self._parse_and_validate_response(response, document_text)

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse IA: {e}")
            raise RuntimeError(f"❌ Échec de l'analyse IA: {str(e)}") from e

    def _build_analysis_prompt(self, document_text: str) -> str:
        """Construit le prompt d'analyse pour Grok"""

        # Limiter la longueur du texte pour éviter les dépassements de tokens
        max_length = 8000  # Environ 2000 tokens
        if len(document_text) > max_length:
            document_text = document_text[:max_length] + "...[texte tronqué]"

        prompt = f"""Tu es un expert en analyse de CV pour le recrutement dans l'informatique.
Ton objectif est d'extraire avec précision les informations clés d'un CV de consultant IT.

CV à analyser :
{document_text}

INSTRUCTIONS IMPORTANTES :
1. Analyse uniquement le contenu fourni - ne fais pas d'hypothèses
2. Sois précis sur les dates (format YYYY-MM-DD quand possible)
3. Pour les missions en cours, utilise "en cours" comme date de fin
4. Liste toutes les technologies/compétences techniques mentionnées
5. Structure ta réponse EXACTEMENT comme demandé ci-dessous

FORMAT DE RÉPONSE JSON OBLIGATOIRE :
{{
    "consultant_info": {{
        "nom": "Nom du consultant",
        "prenom": "Prénom du consultant",
        "email": "email@exemple.com",
        "telephone": "+33123456789",
        "experience_annees": 5,
        "niveau_etudes": "Master Informatique"
    }},
    "missions": [
        {{
            "client": "Nom du client/entreprise",
            "role": "Poste occupé (ex: Développeur, Chef de projet)",
            "date_debut": "YYYY-MM-DD",
            "date_fin": "YYYY-MM-DD ou 'en cours'",
            "description": "Description détaillée des responsabilités",
            "technologies": ["tech1", "tech2", "tech3"],
            "competences_fonctionnelles": ["gestion", "analyse", "management"]
        }}
    ],
    "competences": {{
        "techniques": ["Python", "SQL", "React", "Docker"],
        "fonctionnelles": ["Management", "Analyse métier", "Formation"],
        "langues": ["Français C2", "Anglais B2", "Espagnol B1"],
        "certifications": ["AWS Certified", "Scrum Master"]
    }},
    "formation": {{
        "diplome_principal": "Master en Informatique",
        "annee_obtention": 2020,
        "etablissement": "Université Paris-Saclay"
    }},
    "resume_general": "Résumé général du profil professionnel",
    "disponibilite": "immédiate ou date si mentionnée",
    "mobilite": "Paris, remote possible, etc.",
    "salaire_actuel": "montant si mentionné",
    "pretentions": "prétentions salariales si mentionnées"
}}

RÈGLES DE QUALITÉ :
- Si une information n'est pas présente, utilise null ou liste vide []
- Pour les dates floues, utilise le format "YYYY-MM-DD" le plus précis possible
- Liste TOUTES les technologies mentionnées (même si évidentes)
- Sépare clairement technologies vs compétences fonctionnelles
- Sois exhaustif mais précis

Réponds UNIQUEMENT avec du JSON valide, rien d'autre."""

        return prompt

    def _call_grok_api(self, prompt: str) -> Dict[str, Any]:
        """Appelle l'API Grok"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.1,  # Faible température pour plus de précision
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erreur API Grok: {str(e)}") from e

    def _parse_and_validate_response(
        self, api_response: Dict[str, Any], original_text: str
    ) -> Dict[str, Any]:
        """Parse et valide la réponse de Grok"""

        try:
            # Extraire le contenu de la réponse
            content = api_response["choices"][0]["message"]["content"]

            # Nettoyer le contenu (enlever les ```json si présents)
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            # Parser le JSON
            parsed_data = json.loads(content)

            # Validation basique
            if not isinstance(parsed_data, dict):
                raise ValueError("La réponse n'est pas un objet JSON valide")

            # Ajouter des métadonnées
            parsed_data["_metadata"] = {
                "analyzed_by": "grok_ai",
                "analysis_date": datetime.now().isoformat(),
                "text_length": len(original_text),
                "model_used": self.model,
            }

            return parsed_data

        except json.JSONDecodeError as e:
            logger.error(f"Erreur de parsing JSON: {e}")
            logger.error(f"Contenu reçu: {content[:500]}...")
            raise ValueError("❌ La réponse de Grok n'est pas un JSON valide") from e

        except KeyError as e:
            logger.error(f"Structure de réponse inattendue: {e}")
            raise ValueError("❌ Structure de réponse Grok inattendue") from e

    def get_cost_estimate(self, text_length: int) -> float:
        """
        Estime le coût d'une analyse en fonction de la longueur du texte

        Args:
            text_length: Longueur du texte en caractères

        Returns:
            Coût estimé en dollars
        """
        # Estimation basée sur les prix Grok (approximatif)
        # ~$0.001 par 1K tokens, 1 token ≈ 4 caractères
        estimated_tokens = text_length / 4
        cost_per_1k_tokens = 0.001
        return (estimated_tokens / 1000) * cost_per_1k_tokens


def get_grok_service() -> Optional[GrokAIService]:
    """Factory pour obtenir une instance du service Grok"""
    try:
        return GrokAIService()
    except ValueError:
        return None


def is_grok_available() -> bool:
    """Vérifie si le service Grok est disponible"""
    try:
        service = get_grok_service()
        return service is not None
    except Exception:
        return False


# Interface Streamlit pour la configuration
def show_grok_config_interface():
    """Interface Streamlit pour configurer Grok"""

    st.markdown("### 🤖 Configuration Grok AI")

    # Vérifier si la clé API est configurée
    api_key = os.getenv("GROK_API_KEY")

    if api_key:
        # Clé configurée
        masked_key = (
            api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else api_key
        )
        st.success(f"✅ Clé API configurée: `{masked_key}`")

        # Tester la connexion
        if st.button("🔍 Tester la connexion", key="test_grok_connection"):
            with st.spinner("Test de connexion en cours..."):
                try:
                    service = GrokAIService(api_key)
                    # Faire un petit test
                    service._call_grok_api("Bonjour, réponds simplement 'OK'")
                    st.success("✅ Connexion Grok réussie !")
                except Exception as e:
                    st.error(f"❌ Erreur de connexion: {e}")

    else:
        # Clé non configurée
        st.warning("⚠️ Clé API Grok non configurée")

        st.markdown(
            """
        **Pour utiliser Grok AI, vous devez :**

        1. **Obtenir une clé API** sur [x.ai](https://x.ai)
        2. **Ajouter la variable d'environnement** :
           ```bash
           export GROK_API_KEY="votre_clé_api_ici"
           ```
        3. **Redémarrer l'application**
        """
        )

        # Saisie temporaire de la clé API
        temp_api_key = st.text_input(
            "Clé API Grok (temporaire)",
            type="password",
            help="Saisissez votre clé API pour tester immédiatement",
        )

        if temp_api_key and st.button("🔍 Tester avec cette clé"):
            try:
                service = GrokAIService(temp_api_key)
                service._call_grok_api("Bonjour, réponds simplement 'OK'")
                st.success(
                    "✅ Clé API valide ! Configurez-la dans vos variables d'environnement."
                )
            except Exception as e:
                st.error(f"❌ Clé API invalide: {e}")


if __name__ == "__main__":
    # Test du service
    print("Test du service Grok AI...")

    if not is_grok_available():
        print("❌ Service Grok non disponible (clé API manquante)")
        exit(1)

    # Test avec un CV exemple
    test_cv = """
    Jean DUPONT
    Développeur Python Senior

    Expérience professionnelle :
    - Société Générale (2020-2023) : Développeur Python, gestion de bases de données SQL
    - BNP Paribas (2018-2020) : Analyste développeur, React, Node.js

    Compétences : Python, SQL, React, Docker, Kubernetes
    """

    try:
        service = get_grok_service()
        result = service.analyze_cv(test_cv, "Jean DUPONT")
        print("✅ Analyse réussie !")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Erreur: {e}")
