"""
Tests unitaires pour ai_grok_service.py
Tests pour améliorer la couverture du service Grok AI
"""

import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Mock des modules externes avant les imports
sys.modules['streamlit'] = MagicMock()
sys.modules['requests'] = MagicMock()

from app.services.ai_grok_service import (
    GrokAIService,
    get_grok_service,
    is_grok_available,
    show_grok_config_interface
)


class TestGrokAIService(unittest.TestCase):
    """Tests pour la classe GrokAIService"""

    def setUp(self):
        """Configuration commune pour tous les tests"""
        self.test_api_key = "test_grok_api_key"
        self.test_cv_text = "Jean DUPONT\nDéveloppeur Python\nExpérience: 5 ans"

    @patch.dict('os.environ', {"GROK_API_KEY": "test_key"})
    def test_init_with_env_var(self):
        """Test initialisation avec variable d'environnement"""
        service = GrokAIService()

        self.assertEqual(service.api_key, "test_key")
        self.assertEqual(service.base_url, "https://api.x.ai/v1")
        self.assertEqual(service.model, "grok-beta")

    def test_init_with_api_key(self):
        """Test initialisation avec clé API fournie"""
        service = GrokAIService(self.test_api_key)

        self.assertEqual(service.api_key, self.test_api_key)

    def test_init_no_api_key(self):
        """Test initialisation sans clé API"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                GrokAIService()

            self.assertIn("Clé API Grok manquante", str(context.exception))

    @patch('app.services.ai_grok_service.requests.post')
    def test_analyze_cv_success(self, mock_post):
        """Test analyze_cv avec succès"""
        # Mock de la réponse API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"consultant_info": {"nom": "DUPONT", "prenom": "Jean"}}'
                }
            }]
        }
        mock_post.return_value = mock_response

        service = GrokAIService(self.test_api_key)
        result = service.analyze_cv(self.test_cv_text)

        # Vérifications
        self.assertIn("consultant_info", result)
        self.assertIn("_metadata", result)
        self.assertEqual(result["_metadata"]["analyzed_by"], "grok_ai")

    @patch('app.services.ai_grok_service.requests.post')
    def test_analyze_cv_api_error(self, mock_post):
        """Test analyze_cv avec erreur API"""
        mock_post.side_effect = Exception("API Error")

        service = GrokAIService(self.test_api_key)

        with self.assertRaises(RuntimeError) as context:
            service.analyze_cv(self.test_cv_text)

        self.assertIn("Échec de l'analyse IA", str(context.exception))

    def test_build_analysis_prompt(self):
        """Test _build_analysis_prompt"""
        service = GrokAIService(self.test_api_key)
        prompt = service._build_analysis_prompt(self.test_cv_text)

        # Vérifications
        self.assertIn("Tu es un expert en analyse de CV", prompt)
        self.assertIn(self.test_cv_text, prompt)
        self.assertIn("FORMAT DE RÉPONSE JSON", prompt)

    def test_build_analysis_prompt_long_text(self):
        """Test _build_analysis_prompt avec texte très long"""
        long_text = "A" * 10000
        service = GrokAIService(self.test_api_key)
        prompt = service._build_analysis_prompt(long_text)

        # Vérifier que le texte est tronqué
        self.assertIn("[texte tronqué]", prompt)
        # Vérifier que le prompt contient le texte tronqué
        self.assertIn("..." + "[texte tronqué]", prompt)
        # Vérifier que la longueur du texte dans le prompt est limitée
        # Le texte original fait 10000 chars, mais dans le prompt il devrait être limité
        text_in_prompt = prompt.split("CV à analyser :\n")[1].split("\n\nINSTRUCTIONS")[0]
        self.assertLess(len(text_in_prompt), 9000)  # Moins de 9000 chars (8000 + "...[texte tronqué]")

    @patch('app.services.ai_grok_service.requests.post')
    def test_call_grok_api_success(self, mock_post):
        """Test _call_grok_api avec succès"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "response"}
        mock_post.return_value = mock_response

        service = GrokAIService(self.test_api_key)
        result = service._call_grok_api("test prompt")

        # Vérifications
        self.assertEqual(result, {"test": "response"})
        mock_post.assert_called_once()

        # Vérifier les paramètres d'appel
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "https://api.x.ai/v1/chat/completions")

        # Vérifier les headers
        headers = call_args[1]["headers"]
        self.assertEqual(headers["Authorization"], f"Bearer {self.test_api_key}")

        # Vérifier le payload
        payload = call_args[1]["json"]
        self.assertEqual(payload["model"], "grok-beta")
        self.assertEqual(payload["messages"][0]["content"], "test prompt")

    @patch('app.services.ai_grok_service.requests.post')
    def test_call_grok_api_error(self, mock_post):
        """Test _call_grok_api avec erreur"""
        mock_post.side_effect = Exception("Connection failed")

        service = GrokAIService(self.test_api_key)

        with self.assertRaises(ConnectionError) as context:
            service._call_grok_api("test prompt")

        self.assertIn("Erreur API Grok", str(context.exception))

    def test_parse_and_validate_response_success(self):
        """Test _parse_and_validate_response avec succès"""
        api_response = {
            "choices": [{
                "message": {
                    "content": '{"test": "data"}'
                }
            }]
        }

        service = GrokAIService(self.test_api_key)
        result = service._parse_and_validate_response(api_response, "original text")

        # Vérifications
        self.assertEqual(result["test"], "data")
        self.assertIn("_metadata", result)
        self.assertEqual(result["_metadata"]["analyzed_by"], "grok_ai")

    def test_parse_and_validate_response_json_error(self):
        """Test _parse_and_validate_response avec JSON invalide"""
        api_response = {
            "choices": [{
                "message": {
                    "content": "invalid json"
                }
            }]
        }

        service = GrokAIService(self.test_api_key)

        with self.assertRaises(ValueError) as context:
            service._parse_and_validate_response(api_response, "original text")

        self.assertIn("JSON valide", str(context.exception))

    def test_parse_and_validate_response_structure_error(self):
        """Test _parse_and_validate_response avec structure invalide"""
        api_response = {"invalid": "structure"}

        service = GrokAIService(self.test_api_key)

        with self.assertRaises(ValueError) as context:
            service._parse_and_validate_response(api_response, "original text")

        self.assertIn("Structure de réponse", str(context.exception))

    def test_parse_and_validate_response_with_markdown(self):
        """Test _parse_and_validate_response avec markdown JSON"""
        api_response = {
            "choices": [{
                "message": {
                    "content": "```json\n{\"test\": \"data\"}\n```"
                }
            }]
        }

        service = GrokAIService(self.test_api_key)
        result = service._parse_and_validate_response(api_response, "original text")

        self.assertEqual(result["test"], "data")

    def test_get_cost_estimate(self):
        """Test get_cost_estimate"""
        service = GrokAIService(self.test_api_key)

        # Test avec 4000 caractères (environ 1000 tokens)
        cost = service.get_cost_estimate(4000)

        # Vérifier que le coût est calculé correctement
        # 1000 tokens / 1000 * 0.001 = 0.001
        self.assertAlmostEqual(cost, 0.001, places=5)

    @patch.dict('os.environ', {"GROK_API_KEY": "test_key"})
    def test_get_grok_service_success(self):
        """Test get_grok_service avec succès"""
        service = get_grok_service()

        self.assertIsInstance(service, GrokAIService)

    @patch.dict('os.environ', {}, clear=True)
    def test_get_grok_service_no_key(self):
        """Test get_grok_service sans clé API"""
        service = get_grok_service()

        self.assertIsNone(service)

    @patch('app.services.ai_grok_service.get_grok_service')
    def test_is_grok_available_true(self, mock_get_service):
        """Test is_grok_available retourne True"""
        mock_get_service.return_value = GrokAIService(self.test_api_key)

        result = is_grok_available()

        self.assertTrue(result)

    @patch('app.services.ai_grok_service.get_grok_service')
    def test_is_grok_available_false(self, mock_get_service):
        """Test is_grok_available retourne False"""
        mock_get_service.return_value = None

        result = is_grok_available()

        self.assertFalse(result)

    @patch('app.services.ai_grok_service.st')
    @patch.dict('os.environ', {"GROK_API_KEY": "test_key"})
    def test_show_grok_config_interface_with_key(self, mock_st):
        """Test show_grok_config_interface avec clé configurée"""
        show_grok_config_interface()

        # Vérifier que success est appelé
        mock_st.success.assert_called()

    @patch('app.services.ai_grok_service.st')
    @patch.dict('os.environ', {}, clear=True)
    def test_show_grok_config_interface_no_key(self, mock_st):
        """Test show_grok_config_interface sans clé"""
        show_grok_config_interface()

        # Vérifier que warning est appelé
        mock_st.warning.assert_called()

    @patch('app.services.ai_grok_service.st')
    @patch.dict('os.environ', {"GROK_API_KEY": "test_key"})
    def test_show_grok_config_interface_test_connection(self, mock_st):
        """Test show_grok_config_interface avec test de connexion"""
        # Simuler le clic sur le bouton de test
        mock_st.button.return_value = True

        with patch('app.services.ai_grok_service.GrokAIService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service

            show_grok_config_interface()

            # Vérifier que le service est instancié et testé
            mock_service_class.assert_called_with("test_key")
            mock_service._call_grok_api.assert_called()


if __name__ == '__main__':
    unittest.main()