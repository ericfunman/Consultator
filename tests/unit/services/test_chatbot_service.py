"""
Tests unitaires pour le service chatbot
Couvre les méthodes utilitaires et de traitement de texte
"""

import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from app.services.chatbot_service import ChatbotService


class TestChatbotService:
    """Tests pour la classe ChatbotService"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.chatbot = ChatbotService()

    def test_clean_question(self):
        """Test du nettoyage des questions"""
        # Test avec ponctuation excessive
        assert self.chatbot._clean_question("!!!???") == "!?"

        # Test avec espaces multiples
        assert self.chatbot._clean_question("  hello   world  ") == "hello world"

        # Test avec ponctuation normale
        assert self.chatbot._clean_question("Hello world!") == "hello world!"

        # Test avec casse
        assert self.chatbot._clean_question("HELLO WORLD") == "hello world"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_salaire(self, mock_get_session):
        """Test d'analyse d'intention pour les questions de salaire"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question salaire
        intent = self.chatbot._analyze_intent("Quel est le salaire de Jean ?")
        assert intent == "salaire"

        # Test question rémunération
        intent = self.chatbot._analyze_intent("Quelle est la rémunération de Jean ?")
        assert intent == "salaire"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_experience(self, mock_get_session):
        """Test d'analyse d'intention pour les questions d'expérience"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Marie"
        mock_consultant.nom = "Martin"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question expérience
        intent = self.chatbot._analyze_intent("Quelle est l'expérience de Marie ?")
        assert intent == "experience"

        # Test question ancienneté
        intent = self.chatbot._analyze_intent("Quelle est l'ancienneté de Marie ?")
        assert intent == "experience"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_competences(self, mock_get_session):
        """Test d'analyse d'intention pour les questions de compétences"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Paul"
        mock_consultant.nom = "Durand"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question compétences
        intent = self.chatbot._analyze_intent("Quelles sont les compétences de Paul ?")
        assert intent == "competences"

        # Test question technologies
        intent = self.chatbot._analyze_intent("Quelles technologies maîtrise Paul ?")
        assert intent == "competences"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_contact(self, mock_get_session):
        """Test d'analyse d'intention pour les questions de contact"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Sophie"
        mock_consultant.nom = "Leroy"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question email
        intent = self.chatbot._analyze_intent("Quel est l'email de Sophie ?")
        assert intent == "contact"

        # Test question téléphone
        intent = self.chatbot._analyze_intent("Quel est le téléphone de Sophie ?")
        assert intent == "contact"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_missions(self, mock_get_session):
        """Test d'analyse d'intention pour les questions de missions"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Pierre"
        mock_consultant.nom = "Moreau"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question missions
        intent = self.chatbot._analyze_intent("Quelles sont les missions de Pierre ?")
        assert intent == "missions"

        # Test question projets
        intent = self.chatbot._analyze_intent("Quels sont les projets de Pierre ?")
        assert intent == "missions"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_liste_consultants(self, mock_get_session):
        """Test d'analyse d'intention pour les listes de consultants"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Alice"
        mock_consultant.nom = "Dubois"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test liste consultants
        intent = self.chatbot._analyze_intent("Quels sont les consultants disponibles ?")
        assert intent == "liste_consultants"

        # Test tous les consultants
        intent = self.chatbot._analyze_intent("Montre-moi tous les consultants")
        assert intent == "liste_consultants"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_practices(self, mock_get_session):
        """Test d'analyse d'intention pour les questions de practices"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Luc"
        mock_consultant.nom = "Bernard"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question practice
        intent = self.chatbot._analyze_intent("Qui est dans la practice Data ?")
        assert intent == "practices"

        # Test question équipe
        intent = self.chatbot._analyze_intent("Qui est dans l'équipe Quant ?")
        assert intent == "practices"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_cvs(self, mock_get_session):
        """Test d'analyse d'intention pour les questions de CVs"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Emma"
        mock_consultant.nom = "Petit"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question CV avec mot-clé "cv"
        intent = self.chatbot._analyze_intent("Quel est le cv d'Emma ?")
        assert intent == "cvs"

        # Test question document
        intent = self.chatbot._analyze_intent("Quels documents a Emma ?")
        assert intent == "cvs"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_statistiques(self, mock_get_session):
        """Test d'analyse d'intention pour les questions statistiques"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Hugo"
        mock_consultant.nom = "Roux"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question statistiques avec mot-clé "statistiques"
        intent = self.chatbot._analyze_intent("Quelles sont les statistiques ?")
        assert intent == "statistiques"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_general(self, mock_get_session):
        """Test d'analyse d'intention pour les questions générales"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Léo"
        mock_consultant.nom = "Garcia"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Test question générale
        intent = self.chatbot._analyze_intent("Comment ça marche ?")
        assert intent == "general"

        # Test question sans pattern reconnu
        intent = self.chatbot._analyze_intent("Blabla blabla")
        assert intent == "general"

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_langues(self, mock_get_session):
        """Test d'extraction des langues"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock compétences et langues
        with patch('app.services.chatbot_service.Competence') as mock_competence, \
             patch('app.services.chatbot_service.Langue') as mock_langue, \
             patch('database.models.Practice') as mock_practice:

            mock_competence.query.all.return_value = []
            mock_langue.query.all.return_value = []
            mock_practice.query.filter.return_value.all.return_value = []

            entities = self.chatbot._extract_entities("Jean parle français et anglais")

            assert "français" in entities["langues"]
            assert "anglais" in entities["langues"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_montants(self, mock_get_session):
        """Test d'extraction des montants"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock compétences et langues
        with patch('app.services.chatbot_service.Competence') as mock_competence, \
             patch('app.services.chatbot_service.Langue') as mock_langue, \
             patch('database.models.Practice') as mock_practice:

            mock_competence.query.all.return_value = []
            mock_langue.query.all.return_value = []
            mock_practice.query.filter.return_value.all.return_value = []

            entities = self.chatbot._extract_entities("Le salaire est de 50 000 euros")

            assert "50000" in entities["montants"]

    def test_extract_entities_empty_question(self):
        """Test d'extraction avec question vide"""
        with patch('app.services.chatbot_service.get_database_session') as mock_get_session:
            mock_session = MagicMock()
            mock_session.query.return_value.all.return_value = []
            mock_get_session.return_value.__enter__.return_value = mock_session

            # Mock compétences et langues
            with patch('app.services.chatbot_service.Competence') as mock_competence, \
                 patch('app.services.chatbot_service.Langue') as mock_langue, \
                 patch('database.models.Practice') as mock_practice:

                mock_competence.query.all.return_value = []
                mock_langue.query.all.return_value = []
                mock_practice.query.filter.return_value.all.return_value = []

                entities = self.chatbot._extract_entities("")

                assert entities["noms"] == []
                assert entities["entreprises"] == []
                assert entities["competences"] == []
                assert entities["langues"] == []
                assert entities["montants"] == []
                assert entities["practices"] == []
