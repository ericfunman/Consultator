"""
Tests de couverture pour ChatbotService - Phase 2B: Handlers avec DB
Cible: Méthodes _handle_*_question qui interrogent la base de données
Objectif: Couvrir les 444 lignes manquantes de chatbot_service (66% → 80%+)
"""

import unittest
from datetime import date, datetime
from unittest.mock import MagicMock, Mock, patch, PropertyMock

from app.database.models import Competence, Consultant, ConsultantCompetence, ConsultantLangue, Langue, Mission, Practice
from app.services.chatbot_service import ChatbotService


class TestChatbotHandlersCoverage(unittest.TestCase):
    """Tests pour les handlers de questions du chatbot avec mock DB complet"""

    def setUp(self):
        """Setup avant chaque test"""
        self.chatbot = ChatbotService()
        self.chatbot.last_question = ""  # Reset last question

    def _create_mock_consultant(
        self,
        nom="Dupont",
        prenom="Jean",
        salaire=60000,
        disponibilite=True,
        experience_annees=5,
        email="jean.dupont@test.com",
        telephone="0123456789",
        grade="Senior",
        societe="Quanteam",
    ):
        """Crée un consultant mock avec toutes les propriétés"""
        consultant = Mock(spec=Consultant)
        consultant.id = 1
        consultant.nom = nom
        consultant.prenom = prenom
        consultant.salaire_actuel = salaire
        consultant.disponibilite = disponibilite
        consultant.experience_annees = experience_annees
        consultant.email = email
        consultant.telephone = telephone
        consultant.grade = grade
        consultant.societe = societe
        consultant.date_premiere_mission = date(2018, 1, 15)
        consultant.date_entree_societe = date(2019, 6, 1)
        consultant.date_sortie_societe = None
        consultant.cv_path = "/path/to/cv.pdf"
        consultant.practice = None
        consultant.practice_id = None
        
        # Attributs itérables pour éviter "Mock object is not iterable"
        consultant.langues = []  # Liste vide par défaut
        consultant.consultant_competences = []  # Liste vide par défaut
        
        # Missions par défaut avec statut pour éviter AttributeError
        default_mission = Mock(spec=Mission)
        default_mission.nom_mission = "Mission par défaut"
        default_mission.titre = "Mission par défaut"
        default_mission.client = "Client"
        default_mission.date_debut = date(2023, 1, 1)
        default_mission.date_fin = date(2023, 12, 31)
        default_mission.statut = "termine"
        default_mission.description = ""
        consultant.missions = [default_mission]
        
        consultant.cvs = []  # Liste vide par défaut
        
        return consultant

    def _create_mock_session(self, query_result=None):
        """Crée une session DB mockée"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        
        # Configure la chaîne query().filter().all()/first()
        if query_result is not None:
            if isinstance(query_result, list):
                mock_query.all.return_value = query_result
                mock_query.first.return_value = query_result[0] if query_result else None
            else:
                mock_query.all.return_value = [query_result]
                mock_query.first.return_value = query_result
        else:
            mock_query.all.return_value = []
            mock_query.first.return_value = None
        
        # Mock filter, options, join, etc.
        mock_query.filter.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.distinct.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.offset.return_value = mock_query
        
        mock_session.query.return_value = mock_query
        return mock_session

    # ==================== TESTS: _handle_salary_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_specific_consultant_found(self, mock_get_session):
        """Test question salaire pour un consultant spécifique trouvé"""
        # Setup
        consultant = self._create_mock_consultant(nom="Martin", prenom="Paul", salaire=75000)
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Martin"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le salaire de Martin ?"
        
        # Execute
        result = self.chatbot._handle_salary_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "salaire")
        self.assertIn("response", result)
        self.assertIn("Paul", result["response"])
        self.assertIn("Martin", result["response"])
        self.assertIn("75", result["response"])  # 75 000 ou 75,000
        self.assertIn("data", result)
        self.assertEqual(result["data"]["consultant"]["nom"], "Martin")

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_consultant_not_found(self, mock_get_session):
        """Test question salaire pour un consultant introuvable"""
        # Setup - retourne None (consultant non trouvé)
        mock_session = self._create_mock_session(None)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Inconnu"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le salaire de Inconnu ?"
        
        # Execute
        result = self.chatbot._handle_salary_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "salaire")
        self.assertIn("Inconnu", result["response"])
        self.assertIn("pas trouvé", result["response"].lower())

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_cjm_calculation(self, mock_get_session):
        """Test question CJM avec calcul correct"""
        # Setup
        consultant = self._create_mock_consultant(salaire=64800)  # 64800 * 1.8 / 216 = 540
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le CJM de Dupont ?"
        
        # Execute
        result = self.chatbot._handle_salary_question(entities)
        
        # Assert
        self.assertIn("CJM", result["response"])
        self.assertIn("540", result["response"])  # CJM = 540€
        self.assertEqual(result["data"]["consultant"]["cjm"], 540.0)

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_general_stats(self, mock_get_session):
        """Test statistiques générales de salaire"""
        # Setup - multiple consultants pour stats
        consultants = [
            self._create_mock_consultant(nom="A", salaire=50000),
            self._create_mock_consultant(nom="B", salaire=60000),
            self._create_mock_consultant(nom="C", salaire=70000),
        ]
        mock_session = self._create_mock_session(consultants)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quels sont les salaires moyens ?"
        
        # Execute
        result = self.chatbot._handle_salary_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "salaire")
        self.assertIn("Statistiques", result["response"])
        self.assertIn("moyen", result["response"].lower())

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_salary_question_consultant_no_salary(self, mock_get_session):
        """Test consultant trouvé mais salaire non renseigné"""
        # Setup
        consultant = self._create_mock_consultant(salaire=None)
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le salaire de Dupont ?"
        
        # Execute
        result = self.chatbot._handle_salary_question(entities)
        
        # Assert
        self.assertIn("pas renseigné", result["response"].lower())

    # ==================== TESTS: _handle_experience_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_experience_question_specific_consultant(self, mock_get_session):
        """Test question expérience pour un consultant spécifique"""
        # Setup
        consultant = self._create_mock_consultant(experience_annees=8)
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quelle est l'expérience de Dupont ?"
        
        # Execute
        result = self.chatbot._handle_experience_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "experience")
        self.assertIn("8", result["response"])
        self.assertIn("années", result["response"].lower())

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_experience_question_consultant_not_found(self, mock_get_session):
        """Test question expérience consultant introuvable"""
        # Setup
        mock_session = self._create_mock_session(None)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Inconnu"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        # Execute
        result = self.chatbot._handle_experience_question(entities)
        
        # Assert
        self.assertIn("pas trouvé", result["response"].lower())

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_experience_question_with_dates(self, mock_get_session):
        """Test expérience avec dates de première mission et d'entrée société"""
        # Setup
        consultant = self._create_mock_consultant(experience_annees=10)
        consultant.date_premiere_mission = date(2013, 3, 15)
        consultant.date_entree_societe = date(2015, 9, 1)
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        # Execute
        result = self.chatbot._handle_experience_question(entities)
        
        # Assert
        self.assertIn("15/03/2013", result["response"])
        self.assertIn("01/09/2015", result["response"])

    # ==================== TESTS: _handle_skills_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    @patch.object(ChatbotService, '_get_consultant_skills')
    def test_handle_skills_question_specific_consultant(self, mock_get_skills, mock_get_session):
        """Test question compétences pour un consultant spécifique"""
        # Setup
        consultant = self._create_mock_consultant()
        
        # Mock _get_consultant_skills pour éviter la requête DB
        mock_get_skills.return_value = [
            {"nom": "Python", "categorie": "Langages", "type": "technique", "niveau_maitrise": "Expert", "annees_experience": 5, "description": ""},
            {"nom": "React", "categorie": "Frontend", "type": "technique", "niveau_maitrise": "Confirmé", "annees_experience": 3, "description": ""}
        ]
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quelles sont les compétences de Dupont ?"
        
        # Execute
        result = self.chatbot._handle_skills_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "competences")
        self.assertIn("Python", result["response"])
        self.assertIn("React", result["response"])
        self.assertIn("5", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    @patch.object(ChatbotService, '_get_consultant_skills')
    def test_handle_skills_question_consultant_no_skills(self, mock_get_skills, mock_get_session):
        """Test consultant sans compétences renseignées"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.consultant_competences = []
        
        # Mock _get_consultant_skills retourne liste vide
        mock_get_skills.return_value = []
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
    
        # Execute
        result = self.chatbot._handle_skills_question(entities)
        
        # Assert
        self.assertIn("aucune compétence", result["response"].lower())

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_skills_question_search_by_skill(self, mock_get_session):
        """Test recherche de consultants par compétence"""
        # Setup - plusieurs consultants avec Python
        c1 = self._create_mock_consultant(nom="Dupont")
        c2 = self._create_mock_consultant(nom="Martin")
        
        mock_session = self._create_mock_session([c1, c2])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": ["Python"], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Qui connaît Python ?"
        
        # Execute
        result = self.chatbot._handle_skills_question(entities)
        
        # Assert
        self.assertIn("Python", result["response"])
        # Devrait lister les consultants

    # ==================== TESTS: _handle_languages_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_languages_question_specific_consultant(self, mock_get_session):
        """Test question langues pour un consultant spécifique"""
        # Setup
        consultant = self._create_mock_consultant()
        
        # Mock consultant_langues ET langues (pour itération)
        langue1 = Mock(spec=Langue)
        langue1.nom = "Anglais"
        langue1.code = "EN"
        
        langue2 = Mock(spec=Langue)
        langue2.nom = "Espagnol"
        langue2.code = "ES"
        
        cl1 = Mock(spec=ConsultantLangue)
        cl1.langue = langue1
        cl1.niveau = "Courant"
        cl1.niveau_label = "Courant"
        cl1.commentaire = ""
        
        cl2 = Mock(spec=ConsultantLangue)
        cl2.langue = langue2
        cl2.niveau = "Intermédiaire"
        cl2.niveau_label = "Intermédiaire"
        cl2.commentaire = ""
        
        consultant.consultant_langues = [cl1, cl2]
        consultant.langues = [cl1, cl2]  # Attribut itérable pour _format_consultant_languages_response
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quelles langues parle Dupont ?"
        
        # Execute
        result = self.chatbot._handle_languages_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "langues")
        self.assertIn("Anglais", result["response"])
        self.assertIn("Espagnol", result["response"])
        self.assertIn("Courant", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_languages_question_consultant_no_languages(self, mock_get_session):
        """Test consultant sans langues renseignées"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.consultant_langues = []
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        # Execute
        result = self.chatbot._handle_languages_question(entities)
        
        # Assert
        self.assertIn("aucune langue", result["response"].lower())

    # ==================== TESTS: _handle_missions_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    @patch.object(ChatbotService, '_get_missions_by_consultant')
    def test_handle_missions_question_specific_consultant(self, mock_get_missions, mock_get_session):
        """Test question missions pour un consultant spécifique"""
        # Setup
        consultant = self._create_mock_consultant()
        
        # Mock missions avec TOUS les attributs nécessaires
        mission1 = Mock(spec=Mission)
        mission1.nom_mission = "Projet Backend"
        mission1.titre = "Projet Backend"
        mission1.client = "BNP Paribas"
        mission1.date_debut = date(2023, 1, 1)
        mission1.date_fin = date(2023, 12, 31)
        mission1.description = "Développement API"
        mission1.statut = "termine"
        mission1.taux_journalier = 500
        
        mission2 = Mock(spec=Mission)
        mission2.nom_mission = "Projet Frontend"
        mission2.titre = "Projet Frontend"
        mission2.client = "AXA"
        mission2.date_debut = date(2024, 1, 1)
        mission2.date_fin = None
        mission2.description = "Interface React"
        mission2.statut = "en_cours"
        mission2.taux_journalier = None
        
        # Mock _get_missions_by_consultant pour éviter la requête DB
        mock_get_missions.return_value = [mission1, mission2]
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quelles missions a réalisé Dupont ?"
        
        # Execute
        result = self.chatbot._handle_missions_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "missions")
        self.assertIn("Projet Backend", result["response"])
        self.assertIn("BNP Paribas", result["response"])
        self.assertIn("AXA", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    @patch.object(ChatbotService, '_get_missions_by_consultant')
    def test_handle_missions_question_consultant_no_missions(self, mock_get_missions, mock_get_session):
        """Test consultant sans missions"""
        # Setup
        consultant = self._create_mock_consultant()
        
        # Mock _get_missions_by_consultant retourne liste vide
        mock_get_missions.return_value = []
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        # Execute
        result = self.chatbot._handle_missions_question(entities)
        
        # Assert
        self.assertIn("aucune mission", result["response"].lower())

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_missions_question_by_company(self, mock_get_session):
        """Test recherche missions par entreprise"""
        # Setup
        c1 = self._create_mock_consultant(nom="Dupont")
        
        # Mock missions avec consultant attaché
        mission1 = Mock(spec=Mission)
        mission1.nom_mission = "Projet BNP"
        mission1.titre = "Projet BNP"
        mission1.client = "BNP Paribas"
        mission1.consultant = c1
        mission1.statut = "termine"
        mission1.date_debut = date(2023, 1, 1)
        mission1.date_fin = date(2023, 12, 31)
        
        mock_session = self._create_mock_session([mission1])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": ["BNP Paribas"], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Qui a travaillé chez BNP Paribas ?"
        
        # Execute
        result = self.chatbot._handle_missions_question(entities)
        
        # Assert
        self.assertIn("bnp paribas", result["response"].lower())

    # ==================== TESTS: _handle_contact_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_contact_question_specific_consultant(self, mock_get_session):
        """Test question contact pour un consultant spécifique"""
        # Setup
        consultant = self._create_mock_consultant(
            email="jean.dupont@quanteam.com",
            telephone="06 12 34 56 78"
        )
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Comment contacter Dupont ?"
        
        # Execute
        result = self.chatbot._handle_contact_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "contact")
        self.assertIn("jean.dupont@quanteam.com", result["response"])
        self.assertIn("06 12 34 56 78", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_contact_question_consultant_no_contact(self, mock_get_session):
        """Test consultant sans informations de contact"""
        # Setup
        consultant = self._create_mock_consultant(email=None, telephone=None)
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        # Execute
        result = self.chatbot._handle_contact_question(entities)
        
        # Assert
        self.assertIn("non renseigné", result["response"].lower())

    # ==================== TESTS: _handle_list_consultants_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_list_consultants_question(self, mock_get_session):
        """Test liste de tous les consultants"""
        # Setup
        consultants = [
            self._create_mock_consultant(nom="A", prenom="Alice"),
            self._create_mock_consultant(nom="B", prenom="Bob"),
            self._create_mock_consultant(nom="C", prenom="Charlie"),
        ]
        
        mock_session = self._create_mock_session(consultants)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        self.chatbot.last_question = "Liste de tous les consultants"
        
        # Execute
        result = self.chatbot._handle_list_consultants_question()
        
        # Assert
        self.assertIn("3", result["response"])  # 3 consultants
        self.assertIn("consultant", result["response"].lower())

    # ==================== TESTS: _handle_practices_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_practices_question_specific_practice(self, mock_get_session):
        """Test question sur une practice spécifique"""
        # Setup
        practice = Mock(spec=Practice)
        practice.nom = "Data"
        practice.description = "Practice Data Engineering"
        
        c1 = self._create_mock_consultant(nom="Dupont")
        c1.practice = practice
        c2 = self._create_mock_consultant(nom="Martin")
        c2.practice = practice
        
        # Attribut itérable pour practice.consultants
        practice.consultants = [c1, c2]
        
        mock_session = self._create_mock_session(practice)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": ["Data"]}
        self.chatbot.last_question = "Consultants de la practice Data"
        
        # Execute
        result = self.chatbot._handle_practices_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "practices")
        self.assertIn("Data", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_practices_question_general(self, mock_get_session):
        """Test question générale sur les practices"""
        # Setup
        practice1 = Mock(spec=Practice)
        practice1.nom = "Data"
        practice1.description = "Data Engineering"
        practice1.consultants = []  # Attribut itérable manquant
        
        practice2 = Mock(spec=Practice)
        practice2.nom = "Cloud"
        practice2.description = "Cloud Computing"
        practice2.consultants = []  # Attribut itérable manquant
        
        mock_session = self._create_mock_session([practice1, practice2])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quelles sont les practices ?"
        
        # Execute
        result = self.chatbot._handle_practices_question(entities)
        
        # Assert
        self.assertIn("practice", result["response"].lower())

    # ==================== TESTS: _handle_cvs_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_cvs_question_specific_consultant(self, mock_get_session):
        """Test question CV pour un consultant spécifique"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.cv_path = "/cvs/jean_dupont_2024.pdf"
        
        # Mock cvs comme liste itérable
        cv_mock = Mock()
        cv_mock.fichier = "jean_dupont_2024.pdf"
        cv_mock.date_maj = date(2024, 1, 1)
        cv_mock.taille_fichier = 1024000
        consultant.cvs = [cv_mock]
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Où est le CV de Dupont ?"
        
        # Execute
        result = self.chatbot._handle_cvs_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "cvs")
        self.assertIn("CV", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_cvs_question_consultant_no_cv(self, mock_get_session):
        """Test consultant sans CV"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.cv_path = None
        consultant.cvs = []  # Liste vide explicite
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        # Execute
        result = self.chatbot._handle_cvs_question(entities)
        
        # Assert
        self.assertTrue(
            "pas de cv" in result["response"].lower() or "aucun cv" in result["response"].lower()
        )

    # ==================== TESTS: _handle_professional_profile_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_professional_profile_question(self, mock_get_session):
        """Test question profil professionnel complet"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.consultant_competences = []
        consultant.consultant_langues = []
        consultant.missions = []
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le profil de Dupont ?"
        
        # Execute
        result = self.chatbot._handle_professional_profile_question(entities)
        
        # Assert
        self.assertEqual(result["intent"], "profil_professionnel")
        self.assertIn("Jean", result["response"])
        self.assertIn("Dupont", result["response"])

    # ==================== TESTS: Helper methods ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultant_by_name(self, mock_get_session):
        """Test recherche de consultant par nom"""
        # Setup
        consultant = self._create_mock_consultant(nom="Dupont", prenom="Jean")
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Execute
        result = self.chatbot._find_consultant_by_name("Dupont")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.nom, "Dupont")

    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultant_by_name_not_found(self, mock_get_session):
        """Test recherche consultant inexistant"""
        # Setup
        mock_session = self._create_mock_session(None)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Execute
        result = self.chatbot._find_consultant_by_name("Inconnu")
        
        # Assert
        self.assertIsNone(result)

    def test_calculate_cjm(self):
        """Test calcul CJM"""
        # Execute
        cjm = self.chatbot._calculate_cjm(64800)
        
        # Assert
        self.assertEqual(cjm, 540.0)  # 64800 * 1.8 / 216 = 540

    def test_calculate_cjm_zero_salary(self):
        """Test calcul CJM avec salaire 0"""
        # Execute
        cjm = self.chatbot._calculate_cjm(0)
        
        # Assert
        self.assertEqual(cjm, 0.0)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_salary_stats(self, mock_get_session):
        """Test récupération statistiques de salaire"""
        # Setup
        consultants = [
            self._create_mock_consultant(salaire=50000),
            self._create_mock_consultant(salaire=60000),
            self._create_mock_consultant(salaire=70000),
        ]
        mock_session = self._create_mock_session(consultants)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Execute
        stats = self.chatbot._get_salary_stats()
        
        # Assert
        self.assertIn("moyenne", stats)
        self.assertIn("mediane", stats)
        self.assertIn("minimum", stats)
        self.assertIn("maximum", stats)
        self.assertIn("total", stats)

    def test_calculate_company_seniority(self):
        """Test calcul ancienneté dans la société"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.date_entree_societe = date(2019, 1, 1)
        consultant.date_sortie_societe = None
        
        # Execute
        seniority = self.chatbot._calculate_company_seniority(consultant)
        
        # Assert
        self.assertGreater(seniority, 5)  # Plus de 5 ans depuis 2019
        self.assertIsInstance(seniority, float)

    def test_calculate_company_seniority_with_exit_date(self):
        """Test ancienneté avec date de sortie"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.date_entree_societe = date(2019, 1, 1)
        consultant.date_sortie_societe = date(2022, 1, 1)
        
        # Execute
        seniority = self.chatbot._calculate_company_seniority(consultant)
        
        # Assert
        self.assertAlmostEqual(seniority, 3.0, delta=0.2)  # ~3 ans

    def test_calculate_company_seniority_no_entry_date(self):
        """Test ancienneté sans date d'entrée"""
        # Setup
        consultant = self._create_mock_consultant()
        consultant.date_entree_societe = None
        
        # Execute
        seniority = self.chatbot._calculate_company_seniority(consultant)
        
        # Assert
        self.assertEqual(seniority, 0)


if __name__ == "__main__":
    unittest.main()
