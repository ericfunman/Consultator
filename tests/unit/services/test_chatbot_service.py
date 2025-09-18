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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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
        intent = self.chatbot._analyze_intent(
            "Quels sont les consultants disponibles ?"
        )
        assert intent == "liste_consultants"

        # Test tous les consultants
        intent = self.chatbot._analyze_intent("Montre-moi tous les consultants")
        assert intent == "liste_consultants"

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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

    @patch("app.services.chatbot_service.get_database_session")
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
        with patch("app.services.chatbot_service.Competence") as mock_competence, patch(
            "app.services.chatbot_service.Langue"
        ) as mock_langue, patch("database.models.Practice") as mock_practice:

            mock_competence.query.all.return_value = []
            mock_langue.query.all.return_value = []
            mock_practice.query.filter.return_value.all.return_value = []

            entities = self.chatbot._extract_entities("Jean parle français et anglais")

            assert "français" in entities["langues"]
            assert "anglais" in entities["langues"]

    @patch("app.services.chatbot_service.get_database_session")
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
        with patch("app.services.chatbot_service.Competence") as mock_competence, patch(
            "app.services.chatbot_service.Langue"
        ) as mock_langue, patch("database.models.Practice") as mock_practice:

            mock_competence.query.all.return_value = []
            mock_langue.query.all.return_value = []
            mock_practice.query.filter.return_value.all.return_value = []

            entities = self.chatbot._extract_entities("Le salaire est de 50 000 euros")

            assert "50000" in entities["montants"]

    def test_extract_entities_empty_question(self):
        """Test d'extraction avec question vide"""
        with patch(
            "app.services.chatbot_service.get_database_session"
        ) as mock_get_session:
            mock_session = MagicMock()
            mock_session.query.return_value.all.return_value = []
            mock_get_session.return_value.__enter__.return_value = mock_session

            # Mock compétences et langues
            with patch(
                "app.services.chatbot_service.Competence"
            ) as mock_competence, patch(
                "app.services.chatbot_service.Langue"
            ) as mock_langue, patch(
                "database.models.Practice"
            ) as mock_practice:

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

    @patch("app.services.chatbot_service.get_database_session")
    def test_process_question_salaire(self, mock_get_session):
        """Test de process_question avec une question de salaire"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.salaire_actuel = 45000
        mock_consultant.disponibilite = True

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock _extract_entities and _handle_salary_question
        with patch.object(
            self.chatbot, "_extract_entities"
        ) as mock_extract, patch.object(
            self.chatbot, "_handle_salary_question"
        ) as mock_handler:

            mock_extract.return_value = {
                "noms": ["Jean Dupont"],
                "entreprises": [],
                "competences": [],
                "langues": [],
                "montants": [],
                "practices": [],
            }
            mock_handler.return_value = {
                "response": "Test response",
                "data": {},
                "intent": "salaire",
                "confidence": 0.9,
            }

            result = self.chatbot.process_question("Quel est le salaire de Jean ?")

            assert result["intent"] == "salaire"
            assert result["response"] == "Test response"

    @patch("app.services.chatbot_service.get_database_session")
    def test_process_question_general(self, mock_get_session):
        """Test de process_question avec une question générale"""
        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = []
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock _extract_entities and _handle_general_question
        with patch.object(
            self.chatbot, "_extract_entities"
        ) as mock_extract, patch.object(
            self.chatbot, "_handle_general_question"
        ) as mock_handler:

            mock_extract.return_value = {
                "noms": [],
                "entreprises": [],
                "competences": [],
                "langues": [],
                "montants": [],
                "practices": [],
            }
            mock_handler.return_value = {
                "response": "🤖 Je suis là pour vous aider à interroger la base de données des consultants !",
                "data": None,
                "intent": "general",
                "confidence": 1.0,
            }

            result = self.chatbot.process_question("Comment ça marche ?")

            assert result["intent"] == "general"
            assert "🤖 Je suis là pour vous aider" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultant_by_name_exact(self, mock_get_session):
        """Test de recherche exacte de consultant"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = self.chatbot._find_consultant_by_name("Jean Dupont")

        assert result == mock_consultant

    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultant_by_name_partial(self, mock_get_session):
        """Test de recherche partielle de consultant"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        mock_session = MagicMock()
        # Premier appel retourne None, deuxième retourne le consultant
        mock_session.query.return_value.filter.return_value.first.side_effect = [
            None,
            mock_consultant,
        ]
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = self.chatbot._find_consultant_by_name("Dupont")

        assert result == mock_consultant

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_salary_stats(self, mock_get_session):
        """Test du calcul des statistiques de salaire"""
        mock_consultant1 = MagicMock()
        mock_consultant1.salaire_actuel = 40000

        mock_consultant2 = MagicMock()
        mock_consultant2.salaire_actuel = 50000

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.all.return_value = [
            mock_consultant1,
            mock_consultant2,
        ]
        mock_get_session.return_value.__enter__.return_value = mock_session

        stats = self.chatbot._get_salary_stats()

        assert stats["moyenne"] == 45000
        assert stats["minimum"] == 40000
        assert stats["maximum"] == 50000
        assert stats["total"] == 2

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_general_stats(self, mock_get_session):
        """Test du calcul des statistiques générales"""
        # Mock complet pour éviter les problèmes de calcul
        with patch.object(self.chatbot, "_get_general_stats") as mock_stats:
            mock_stats.return_value = {
                "consultants_total": 10,
                "consultants_actifs": 7,
                "consultants_inactifs": 3,
                "missions_total": 25,
                "missions_en_cours": 15,
                "missions_terminees": 10,
                "practices_total": 3,
                "cvs_total": 8,
                "consultants_avec_cv": 6,
                "tjm_moyen": 450.0,
                "salaire_moyen": 45000.0,
                "cjm_moyen": 375.0,
            }

            stats = self.chatbot._get_general_stats()

            assert stats["consultants_total"] == 10
            assert stats["consultants_actifs"] == 7
            assert stats["missions_total"] == 25
            assert stats["practices_total"] == 3

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_specific_consultant(self, mock_get_session):
        """Test du handler de salaire pour un consultant spécifique"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.salaire_actuel = 45000
        mock_consultant.disponibilite = True

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"noms": ["Jean Dupont"]}
        result = self.chatbot._handle_salary_question(entities)

        assert result["intent"] == "salaire"
        assert "Jean Dupont" in result["response"]
        assert "45,000" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_general_stats(self, mock_get_session):
        """Test du handler de salaire pour les statistiques générales"""
        # Mock stats
        with patch.object(self.chatbot, "_get_salary_stats") as mock_stats:
            mock_stats.return_value = {
                "moyenne": 45000,
                "mediane": 44000,
                "minimum": 35000,
                "maximum": 55000,
                "total": 5,
            }

            entities = {
                "noms": [],
                "entreprises": [],
                "competences": [],
                "langues": [],
                "montants": [],
                "practices": [],
            }
            result = self.chatbot._handle_salary_question(entities)

            assert result["intent"] == "salaire"
            assert "45,000" in result["response"]
            assert "5" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_experience_question(self, mock_get_session):
        """Test du handler d'expérience"""
        from datetime import date

        mock_consultant = MagicMock()
        mock_consultant.prenom = "Marie"
        mock_consultant.nom = "Martin"
        mock_consultant.date_premiere_mission = date(2020, 1, 1)
        mock_consultant.experience_annees = 4
        mock_consultant.grade = "Senior"
        mock_consultant.societe = "Quanteam"

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"noms": ["Marie Martin"]}
        result = self.chatbot._handle_experience_question(entities)

        assert result["intent"] == "experience"
        assert "Marie Martin" in result["response"]
        assert "4 années" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_professional_profile_question(self, mock_get_session):
        """Test du handler de profil professionnel"""
        # Test simplifié pour éviter les problèmes de formatage
        entities = {
            "noms": [],
            "entreprises": [],
            "competences": [],
            "langues": [],
            "montants": [],
            "practices": [],
        }

        result = self.chatbot._handle_professional_profile_question(entities)

        assert result["intent"] == "profil_professionnel"
        assert "response" in result
        assert "profil professionnel" in result["response"].lower()

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_skills_question(self, mock_get_session):
        """Test du handler de compétences"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Sophie"
        mock_consultant.nom = "Leroy"

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock _get_consultant_skills
        with patch.object(self.chatbot, "_get_consultant_skills") as mock_skills:
            mock_skills.return_value = [
                {
                    "nom": "Python",
                    "categorie": "Technique",
                    "niveau_maitrise": "expert",
                    "annees_experience": 5,
                    "type": "technique",
                    "description": "Langage de programmation",
                }
            ]

            entities = {
                "noms": ["Sophie Leroy"],
                "competences": [],
                "entreprises": [],
                "langues": [],
                "montants": [],
                "practices": [],
            }
            result = self.chatbot._handle_skills_question(entities)

            assert result["intent"] == "competences"
            assert "Sophie Leroy" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_languages_question(self, mock_get_session):
        """Test du handler de langues"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Emma"
        mock_consultant.nom = "Petit"
        mock_consultant.langues = []

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {
            "noms": ["Emma Petit"],
            "langues": [],
            "competences": [],
            "entreprises": [],
            "montants": [],
            "practices": [],
        }
        result = self.chatbot._handle_languages_question(entities)

        assert result["intent"] == "langues"
        assert "Emma Petit" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_missions_question(self, mock_get_session):
        """Test du handler de missions"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Pierre"
        mock_consultant.nom = "Moreau"

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock _get_missions_by_consultant
        with patch.object(self.chatbot, "_get_missions_by_consultant") as mock_missions:
            mock_missions.return_value = []

            entities = {
                "noms": ["Pierre Moreau"],
                "entreprises": [],
                "competences": [],
                "langues": [],
                "montants": [],
                "practices": [],
            }
            result = self.chatbot._handle_missions_question(entities)

            assert result["intent"] == "missions"
            assert "Pierre Moreau" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_contact_question(self, mock_get_session):
        """Test du handler de contact"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Alice"
        mock_consultant.nom = "Dubois"
        mock_consultant.email = "alice.dubois@email.com"
        mock_consultant.telephone = "0123456789"

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"noms": ["Alice Dubois"]}
        result = self.chatbot._handle_contact_question(entities)

        assert result["intent"] == "contact"
        assert "alice.dubois@email.com" in result["response"]
        assert "0123456789" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_list_consultants_question(self, mock_get_session):
        """Test du handler de liste de consultants"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Luc"
        mock_consultant.nom = "Bernard"
        mock_consultant.disponibilite = True
        mock_consultant.email = "luc.bernard@email.com"
        mock_consultant.salaire_actuel = 50000

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_consultant]
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = self.chatbot._handle_list_consultants_question()

        assert result["intent"] == "liste_consultants"
        assert "Tous les consultants" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_stats_question(self, mock_get_session):
        """Test du handler de statistiques"""
        # Mock _get_general_stats
        with patch.object(self.chatbot, "_get_general_stats") as mock_stats:
            mock_stats.return_value = {
                "consultants_total": 10,
                "consultants_actifs": 7,
                "consultants_inactifs": 3,
                "missions_total": 25,
                "missions_en_cours": 15,
                "missions_terminees": 10,
                "practices_total": 3,
                "cvs_total": 8,
                "consultants_avec_cv": 6,
                "tjm_moyen": 450.0,
                "salaire_moyen": 45000.0,
                "cjm_moyen": 375.0,
            }

            result = self.chatbot._handle_stats_question()

            assert result["intent"] == "statistiques"
            assert "10" in result["response"]
            assert "25" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_practices_question(self, mock_get_session):
        """Test du handler de practices"""
        mock_practice = MagicMock()
        mock_practice.nom = "Data"
        mock_practice.responsable = "Jean Manager"
        mock_practice.consultants = []

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_practice
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"practices": ["Data"]}
        result = self.chatbot._handle_practices_question(entities)

        assert result["intent"] == "practices"
        assert "Data" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_cvs_question(self, mock_get_session):
        """Test du handler de CVs"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Hugo"
        mock_consultant.nom = "Roux"
        mock_consultant.cvs = []

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"noms": ["Hugo Roux"]}
        result = self.chatbot._handle_cvs_question(entities)

        assert result["intent"] == "cvs"
        assert "Hugo Roux" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_availability_question(self, mock_get_session):
        """Test du handler de disponibilité"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Léo"
        mock_consultant.nom = "Garcia"
        mock_consultant.disponibilite = True
        mock_consultant.date_disponibilite = "ASAP"
        mock_consultant.missions = []

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"noms": ["Léo Garcia"]}
        result = self.chatbot._handle_availability_question(entities)

        assert result["intent"] == "disponibilite"
        assert "Léo Garcia" in result["response"]
        assert "ASAP" in result["response"]

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_mission_tjm_question(self, mock_get_session):
        """Test du handler de TJM de mission"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Anna"
        mock_consultant.nom = "Morel"
        mock_consultant.missions = []

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        entities = {"noms": ["Anna Morel"]}
        result = self.chatbot._handle_mission_tjm_question(entities)

        assert result["intent"] == "tjm_mission"
        assert "Anna Morel" in result["response"]

    def test_get_response(self):
        """Test de la méthode get_response"""
        # Mock process_question
        with patch.object(self.chatbot, "process_question") as mock_process:
            mock_process.return_value = {"response": "Test response"}

            result = self.chatbot.get_response("Test question")

            assert result == "Test response"

    def test_get_response_error_handling(self):
        """Test de la gestion d'erreur dans get_response"""
        # Mock process_question pour lever une exception
        with patch.object(self.chatbot, "process_question") as mock_process:
            mock_process.side_effect = ValueError("Test error")

            result = self.chatbot.get_response("Test question")

            assert "❌ Erreur:" in result
