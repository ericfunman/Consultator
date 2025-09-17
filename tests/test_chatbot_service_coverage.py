"""
Tests pour le service Chatbot - Amélioration de la couverture
Tests complets pour chatbot_service.py (40% de couverture actuelle)
"""

import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any, Optional

from app.services.chatbot_service import ChatbotService
from app.database.models import Consultant, Competence, ConsultantCompetence, Langue, ConsultantLangue, Mission, Practice, CV


class TestChatbotService:
    """Tests pour la classe ChatbotService"""

    @pytest.fixture
    def chatbot(self):
        """Fixture pour créer une instance du service chatbot"""
        return ChatbotService()

    @pytest.fixture
    def mock_session(self):
        """Fixture pour créer un mock de session de base de données"""
        return MagicMock()

    @pytest.fixture
    def mock_consultant(self):
        """Fixture pour créer un mock de consultant"""
        consultant = Mock(spec=Consultant)
        consultant.id = 1
        consultant.prenom = "Jean"
        consultant.nom = "Dupont"
        consultant.email = "jean.dupont@email.com"
        consultant.telephone = "0123456789"
        consultant.salaire_actuel = 45000
        consultant.disponibilite = True
        consultant.grade = "Senior"
        consultant.type_contrat = "CDI"
        consultant.societe = "Quanteam"
        consultant.date_premiere_mission = date(2020, 1, 1)
        consultant.date_entree_societe = date(2019, 6, 1)
        consultant.date_sortie_societe = None
        consultant.statut_societe = "En poste"
        consultant.date_creation = datetime(2023, 1, 1)
        consultant.date_disponibilite = "ASAP"
        consultant.missions = []
        consultant.cvs = []
        consultant.langues = []
        return consultant

    @patch('app.services.chatbot_service.get_database_session')
    def test_init(self, mock_get_session, chatbot):
        """Test de l'initialisation du service"""
        assert chatbot.conversation_history == []
        assert chatbot.last_question == ""

    @patch('app.services.chatbot_service.get_database_session')
    def test_get_session(self, mock_get_session, chatbot):
        """Test de la méthode _get_session"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = chatbot._get_session()
        # Vérifier que la méthode retourne bien une session mockée
        assert result is not None

    @patch('app.services.chatbot_service.get_database_session')
    def test_execute_with_fresh_session(self, mock_get_session, chatbot):
        """Test de la méthode _execute_with_fresh_session"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        def test_func(session):
            return "test_result"

        result = chatbot._execute_with_fresh_session(test_func)
        assert result == "test_result"

    def test_clean_question(self, chatbot):
        """Test de la méthode _clean_question"""
        # Test avec ponctuation excessive
        assert chatbot._clean_question("!!!???") == "!?"
        assert chatbot._clean_question("Bonjour!!!") == "bonjour!"
        assert chatbot._clean_question("Comment???") == "comment?"

        # Test avec espaces multiples
        assert chatbot._clean_question("  bonjour  monde  ") == "bonjour monde"

        # Test normal
        assert chatbot._clean_question("Bonjour le monde!") == "bonjour le monde!"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_salaire(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de salaire"""
        # Mock de la base de données
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question salaire simple
        intent = chatbot._analyze_intent("quel est le salaire de jean")
        assert intent == "salaire"

        # Test question CJM
        intent = chatbot._analyze_intent("quel est le cjm de jean")
        assert intent == "salaire"

        # Test question rémunération
        intent = chatbot._analyze_intent("quelle est la rémunération de jean")
        assert intent == "salaire"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_experience(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions d'expérience"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question expérience
        intent = chatbot._analyze_intent("quelle est l'expérience de jean")
        assert intent == "experience"

        # Test question âge professionnel
        intent = chatbot._analyze_intent("quel âge professionnel a jean")
        assert intent == "experience"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_competences(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de compétences"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question compétences
        intent = chatbot._analyze_intent("quelles sont les compétences de jean")
        assert intent == "competences"

        # Test question technologies
        intent = chatbot._analyze_intent("quelles technologies maîtrise jean")
        assert intent == "competences"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_langues(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de langues"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question langues
        intent = chatbot._analyze_intent("quelles langues parle jean")
        assert intent == "langues"

        # Test question bilingue
        intent = chatbot._analyze_intent("jean est-il bilingue")
        assert intent == "langues"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_missions(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de missions"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question missions
        intent = chatbot._analyze_intent("quelles sont les missions de jean")
        assert intent == "missions"

        # Test question projets
        intent = chatbot._analyze_intent("sur quels projets travaille jean")
        assert intent == "missions"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_contact(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de contact"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question email
        intent = chatbot._analyze_intent("quel est l'email de jean")
        assert intent == "contact"

        # Test question téléphone
        intent = chatbot._analyze_intent("quel est le téléphone de jean")
        assert intent == "contact"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_statistiques(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions statistiques"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question nombre consultants
        intent = chatbot._analyze_intent("combien y a-t-il de consultants")
        assert intent == "statistiques"

        # Test question moyenne
        intent = chatbot._analyze_intent("quel est le salaire moyen")
        assert intent == "statistiques"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_practices(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de practices"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question practice
        intent = chatbot._analyze_intent("dans quelle practice est jean")
        assert intent == "practices"

        # Test question équipe
        intent = chatbot._analyze_intent("jean est dans quelle équipe")
        assert intent == "practices"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_cvs(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de CVs"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question CV
        intent = chatbot._analyze_intent("jean a-t-il un cv")
        assert intent == "cvs"

        # Test question document
        intent = chatbot._analyze_intent("quels documents a jean")
        assert intent == "cvs"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_disponibilite(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de disponibilité"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question disponible
        intent = chatbot._analyze_intent("jean est-il disponible")
        assert intent == "disponibilite"

        # Test question libre
        intent = chatbot._analyze_intent("quand jean sera-t-il libre")
        assert intent == "disponibilite"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_tjm_mission(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour les questions de TJM mission"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question TJM mission
        intent = chatbot._analyze_intent("quel est le tjm de la mission de jean")
        assert intent == "tjm_mission"

        # Test question tarif mission
        intent = chatbot._analyze_intent("quel est le tarif de la mission de jean")
        assert intent == "tjm_mission"

    @patch('app.services.chatbot_service.get_database_session')
    def test_analyze_intent_recherche_consultant(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'analyse d'intention pour la recherche de consultant"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        # Test question qui est
        intent = chatbot._analyze_intent("qui est jean dupont")
        assert intent == "recherche_consultant"

        # Test question informations
        intent = chatbot._analyze_intent("quelles sont les informations sur jean")
        assert intent == "recherche_consultant"

    def test_analyze_intent_general(self, chatbot):
        """Test de l'analyse d'intention pour les questions générales"""
        # Test question sans intention claire
        intent = chatbot._analyze_intent("blablabla")
        assert intent == "general"

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_noms(self, mock_get_session, chatbot, mock_consultant):
        """Test de l'extraction d'entités pour les noms"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        entities = chatbot._extract_entities("parle avec jean dupont")

        assert "jean" in entities["noms"]
        assert "dupont" in entities["noms"]
        assert "jean dupont" in entities["noms"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_entreprises(self, mock_get_session, chatbot):
        """Test de l'extraction d'entités pour les entreprises"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        entities = chatbot._extract_entities("jean travaille chez bnp paribas")

        assert "bnp paribas" in entities["entreprises"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_competences(self, mock_get_session, chatbot):
        """Test de l'extraction d'entités pour les compétences"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        entities = chatbot._extract_entities("jean maîtrise python et sql")

        assert "python" in entities["competences"]
        assert "sql" in entities["competences"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_langues(self, mock_get_session, chatbot):
        """Test de l'extraction d'entités pour les langues"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        entities = chatbot._extract_entities("jean parle anglais et espagnol")

        assert "anglais" in entities["langues"]
        assert "espagnol" in entities["langues"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_extract_entities_montants(self, mock_get_session, chatbot):
        """Test de l'extraction d'entités pour les montants"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        entities = chatbot._extract_entities("jean gagne 45000 euros")

        assert "45000" in entities["montants"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_salary_question_with_name(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_salary_question avec un nom spécifique"""
        mock_find_consultant.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_salary_question(entities)

        assert result["intent"] == "salaire"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]
        assert "45,000" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_handle_salary_question_general(self, mock_get_session, chatbot):
        """Test de _handle_salary_question sans nom spécifique"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des statistiques de salaire
        mock_consultant1 = Mock()
        mock_consultant1.salaire_actuel = 40000
        mock_consultant2 = Mock()
        mock_consultant2.salaire_actuel = 50000

        mock_session.query.return_value.filter.return_value.all.return_value = [mock_consultant1, mock_consultant2]

        entities = {"noms": []}  # Ajouter les entités manquantes
        result = chatbot._handle_salary_question(entities)

        assert result["intent"] == "salaire"
        assert "Statistiques des salaires" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_experience_question(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_experience_question"""
        mock_find_consultant.return_value = mock_consultant

        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_experience_question(entities)

        assert result["intent"] == "experience"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_professional_profile_question(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_professional_profile_question"""
        mock_find_consultant.return_value = mock_consultant

        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_professional_profile_question(entities)

        assert result["intent"] == "profil_professionnel"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultants_by_skill')
    def test_handle_skills_question(self, mock_find_consultants, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_skills_question"""
        mock_find_consultants.return_value = [mock_consultant]

        entities = {"competences": ["python"]}
        result = chatbot._handle_skills_question(entities)

        assert result["intent"] == "competences"
        assert "Python" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultants_by_language')
    def test_handle_languages_question(self, mock_find_consultants, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_languages_question"""
        mock_find_consultants.return_value = [mock_consultant]

        entities = {"langues": ["anglais"]}
        result = chatbot._handle_languages_question(entities)

        assert result["intent"] == "langues"
        assert "anglais" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_get_missions_by_consultant')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_missions_question(self, mock_find_consultant, mock_get_missions, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_missions_question"""
        mock_find_consultant.return_value = mock_consultant
        mock_get_missions.return_value = []

        entities = {"noms": ["jean"], "entreprises": []}  # Ajouter les entités manquantes
        result = chatbot._handle_missions_question(entities)

        assert result["intent"] == "missions"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_handle_stats_question(self, mock_get_session, chatbot):
        """Test de _handle_stats_question"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des statistiques générales
        mock_session.query.return_value.count.side_effect = [100, 80, 20, 50, 30, 20, 5, 25, 15]

        result = chatbot._handle_stats_question()

        assert result["intent"] == "statistiques"
        assert "Statistiques générales" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_contact_question(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_contact_question"""
        mock_find_consultant.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_contact_question(entities)

        assert result["intent"] == "contact"
        assert "jean.dupont@email.com" in result["response"]
        assert "0123456789" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_handle_list_consultants_question(self, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_list_consultants_question"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = [mock_consultant]

        result = chatbot._handle_list_consultants_question()

        assert result["intent"] == "liste_consultants"
        assert "consultants" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_consultant_search(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_consultant_search"""
        mock_find_consultant.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_consultant_search(entities)

        assert result["intent"] == "recherche_consultant"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    def test_handle_general_question(self, chatbot):
        """Test de _handle_general_question"""
        result = chatbot._handle_general_question()

        assert result["intent"] == "general"
        assert "🤖 Je suis là pour vous aider" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_handle_practices_question(self, mock_get_session, chatbot):
        """Test de _handle_practices_question"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock d'une practice
        mock_practice = Mock()
        mock_practice.nom = "Data"
        mock_practice.responsable = "Marie Dupont"
        mock_practice.consultants = []

        mock_session.query.return_value.filter.return_value.first.return_value = mock_practice

        entities = {"practices": ["data"]}
        result = chatbot._handle_practices_question(entities)

        assert result["intent"] == "practices"
        assert "Data" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_cvs_question(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_cvs_question"""
        mock_find_consultant.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_cvs_question(entities)

        assert result["intent"] == "cvs"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_availability_question(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_availability_question"""
        mock_find_consultant.return_value = mock_consultant

        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_availability_question(entities)

        assert result["intent"] == "disponibilite"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_handle_mission_tjm_question(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _handle_mission_tjm_question"""
        mock_find_consultant.return_value = mock_consultant

        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = mock_consultant

        entities = {"noms": ["jean"]}
        result = chatbot._handle_mission_tjm_question(entities)

        assert result["intent"] == "tjm_mission"
        assert "Jean" in result["response"]
        assert "Dupont" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    @patch.object(ChatbotService, '_find_consultant_by_name')
    def test_find_consultant_by_name(self, mock_find_consultant, mock_get_session, chatbot, mock_consultant):
        """Test de _find_consultant_by_name"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = mock_consultant

        result = chatbot._find_consultant_by_name("jean")

        assert result == mock_consultant

    @patch('app.services.chatbot_service.get_database_session')
    def test_find_consultants_by_skill(self, mock_get_session, chatbot, mock_consultant):
        """Test de _find_consultants_by_skill"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.distinct.return_value.all.return_value = [mock_consultant]

        result = chatbot._find_consultants_by_skill("python")

        assert result == [mock_consultant]

    @patch('app.services.chatbot_service.get_database_session')
    def test_find_consultants_by_language(self, mock_get_session, chatbot, mock_consultant):
        """Test de _find_consultants_by_language"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.distinct.return_value.all.return_value = [mock_consultant]

        result = chatbot._find_consultants_by_language("anglais")

        assert result == [mock_consultant]

    @patch('app.services.chatbot_service.get_database_session')
    def test_get_missions_by_company(self, mock_get_session, chatbot):
        """Test de _get_missions_by_company"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.all.return_value = []

        result = chatbot._get_missions_by_company("bnp paribas")

        assert result == []

    @patch('app.services.chatbot_service.get_database_session')
    def test_get_missions_by_consultant(self, mock_get_session, chatbot):
        """Test de _get_missions_by_consultant"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        result = chatbot._get_missions_by_consultant(1)

        assert result == []

    @patch('app.services.chatbot_service.get_database_session')
    def test_get_consultant_skills(self, mock_get_session, chatbot):
        """Test de _get_consultant_skills"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = []

        result = chatbot._get_consultant_skills(1)

        assert result == []

    @patch('app.services.chatbot_service.get_database_session')
    def test_get_salary_stats(self, mock_get_session, chatbot):
        """Test de _get_salary_stats"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock de consultants avec salaires
        mock_consultant1 = Mock()
        mock_consultant1.salaire_actuel = 40000
        mock_consultant2 = Mock()
        mock_consultant2.salaire_actuel = 50000

        mock_session.query.return_value.filter.return_value.all.return_value = [mock_consultant1, mock_consultant2]

        result = chatbot._get_salary_stats()

        assert result["moyenne"] == 45000
        assert result["minimum"] == 40000
        assert result["maximum"] == 50000
        assert result["total"] == 2

    @patch('app.services.chatbot_service.get_database_session')
    def test_get_general_stats(self, mock_get_session, chatbot):
        """Test de _get_general_stats"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des compteurs - retourner des entiers au lieu de mocks
        mock_session.query.return_value.count.side_effect = [100, 80, 50, 30, 25, 15]
        mock_session.query.return_value.filter.return_value.scalar.side_effect = [450.0, 45000.0]

        result = chatbot._get_general_stats()

        assert result["consultants_total"] == 100
        assert result["consultants_actifs"] == 80
        assert result["missions_total"] == 50
        assert result["tjm_moyen"] == pytest.approx(450.0, rel=1e-2)
        assert result["salaire_moyen"] == pytest.approx(45000.0, rel=1e-2)

    @patch.object(ChatbotService, 'process_question')
    def test_get_response(self, mock_process_question, chatbot):
        """Test de get_response"""
        mock_process_question.return_value = {"response": "Test response"}

        result = chatbot.get_response("test question")

        assert result == "Test response"

    @patch.object(ChatbotService, 'process_question')
    def test_get_response_error(self, mock_process_question, chatbot):
        """Test de get_response avec erreur"""
        mock_process_question.side_effect = ValueError("Test error")

        result = chatbot.get_response("test question")

        assert "❌ Erreur:" in result

    @patch('app.services.chatbot_service.get_database_session')
    def test_process_question_error_handling(self, mock_get_session, chatbot):
        """Test de la gestion d'erreurs dans process_question"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        # Test avec une exception SQLAlchemy
        mock_session.query.side_effect = Exception("Database error")

        result = chatbot.process_question("test question")

        assert result["intent"] == "error"
        assert "❌ Désolé, j'ai rencontré une erreur" in result["response"]

    @patch('app.services.chatbot_service.get_database_session')
    def test_process_question_unknown_intent(self, mock_get_session, chatbot):
        """Test de process_question avec intention inconnue"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        result = chatbot.process_question("blablabla incomprehensible xyz123")

        assert result["intent"] == "general"
        assert "🤖 Je suis là pour vous aider" in result["response"]