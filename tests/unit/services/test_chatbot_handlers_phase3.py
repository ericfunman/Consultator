"""
Tests de couverture PHASE 3 : Handlers avancés du ChatbotService
Cible : +3-4% de couverture globale en testant les méthodes non couvertes
"""

import unittest
from datetime import date, datetime
from unittest.mock import Mock, MagicMock, patch
from app.services.chatbot_service import ChatbotService
from app.database.models import (
    Consultant, Mission, Practice, Langue, ConsultantLangue,
    Competence, ConsultantCompetence, CV
)


class TestChatbotHandlersPhase3(unittest.TestCase):
    """Tests massifs pour handlers avancés non couverts"""

    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.chatbot = ChatbotService()

    def _create_mock_consultant(self, nom="Dupont", prenom="Jean", salaire=75000,
                                email="jean.dupont@quanteam.com", telephone="0612345678",
                                disponibilite=True, date_disponibilite=None):
        """Helper pour créer un consultant mocké avec attributs complets"""
        consultant = Mock(spec=Consultant)
        consultant.id = 1
        consultant.nom = nom
        consultant.prenom = prenom
        consultant.email = email
        consultant.telephone = telephone
        consultant.salaire_actuel = salaire
        consultant.disponibilite = disponibilite
        consultant.date_disponibilite = date_disponibilite
        consultant.grade = "Senior"
        consultant.type_contrat = "CDI"
        consultant.societe = "Quanteam"
        consultant.date_premiere_mission = date(2018, 1, 15)
        consultant.date_entree_societe = date(2019, 6, 1)
        consultant.date_sortie_societe = None
        consultant.cv_path = "/path/to/cv.pdf"
        consultant.practice = None
        consultant.practice_id = None
        consultant.date_creation = datetime(2020, 1, 1)
        
        # Attributs itérables
        consultant.langues = []
        consultant.consultant_competences = []
        consultant.cvs = []
        
        # Mission par défaut
        default_mission = Mock(spec=Mission)
        default_mission.nom_mission = "Mission par défaut"
        default_mission.titre = "Mission par défaut"
        default_mission.client = "Client"
        default_mission.date_debut = date(2023, 1, 1)
        default_mission.date_fin = date(2023, 12, 31)
        default_mission.statut = "termine"
        default_mission.description = ""
        default_mission.taux_journalier = 500
        default_mission.tjm = None
        consultant.missions = [default_mission]
        
        return consultant

    def _create_mock_session(self, query_result=None):
        """Crée une session DB mockée"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        
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
        
        mock_query.filter.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.distinct.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.count.return_value = len(query_result) if isinstance(query_result, list) else 1
        mock_query.scalar.return_value = 500.0
        
        mock_session.query.return_value = mock_query
        return mock_session

    # ==================== TESTS: _handle_availability_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_availability_question_specific_consultant_available(self, mock_get_session):
        """Test disponibilité consultant marqué disponible"""
        consultant = self._create_mock_consultant(disponibilite=True)
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Dupont est-il disponible ?"
        
        result = self.chatbot._handle_availability_question(entities)
        
        self.assertEqual(result["intent"], "disponibilite")
        self.assertIn("response", result)
        self.assertIn("Dupont", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_availability_question_specific_consultant_busy(self, mock_get_session):
        """Test disponibilité consultant occupé"""
        consultant = self._create_mock_consultant(
            disponibilite=False,
            date_disponibilite=date(2025, 12, 31)
        )
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        result = self.chatbot._handle_availability_question(entities)
        
        self.assertEqual(result["intent"], "disponibilite")
        self.assertIn("response", result)

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_availability_question_general(self, mock_get_session):
        """Test question générale sur disponibilités"""
        c1 = self._create_mock_consultant(nom="A", disponibilite=True)
        c2 = self._create_mock_consultant(nom="B", disponibilite=False)
        
        mock_session = self._create_mock_session([c1, c2])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quels consultants sont disponibles ?"
        
        result = self.chatbot._handle_availability_question(entities)
        
        self.assertEqual(result["intent"], "disponibilite")
        self.assertIn("data", result)

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_availability_question_consultant_not_found(self, mock_get_session):
        """Test disponibilité consultant introuvable - retourne stats générales"""
        mock_session = self._create_mock_session(None)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Inconnu"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        result = self.chatbot._handle_availability_question(entities)
        
        # Quand consultant pas trouvé, retourne stats générales
        self.assertEqual(result["intent"], "disponibilite")
        self.assertIn("disponibilité", result["response"].lower())

    # ==================== TESTS: _handle_mission_tjm_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_mission_tjm_question_specific_consultant(self, mock_get_session):
        """Test question TJM pour un consultant spécifique"""
        consultant = self._create_mock_consultant()
        
        # Mission avec TJM
        mission = Mock(spec=Mission)
        mission.nom_mission = "Mission TJM"
        mission.client = "Client Test"
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = date(2024, 12, 31)
        mission.tjm = 600
        mission.taux_journalier = None
        consultant.missions = [mission]
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le TJM de Dupont ?"
        
        result = self.chatbot._handle_mission_tjm_question(entities)
        
        self.assertEqual(result["intent"], "tjm_mission")
        self.assertIn("response", result)

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_mission_tjm_question_consultant_no_tjm(self, mock_get_session):
        """Test TJM consultant sans TJM renseigné"""
        consultant = self._create_mock_consultant()
        consultant.missions = []
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        result = self.chatbot._handle_mission_tjm_question(entities)
        
        self.assertEqual(result["intent"], "tjm_mission")
        self.assertIn("Aucun TJM", result["response"])

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_mission_tjm_question_general_stats(self, mock_get_session):
        """Test statistiques TJM générales"""
        mock_session = self._create_mock_session([])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        self.chatbot.last_question = "Quel est le TJM moyen ?"
        
        result = self.chatbot._handle_mission_tjm_question(entities)
        
        self.assertEqual(result["intent"], "tjm_mission")
        self.assertIn("response", result)

    # ==================== TESTS: _handle_stats_question ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_stats_question_general(self, mock_get_session):
        """Test statistiques générales"""
        consultants = [
            self._create_mock_consultant(nom="A"),
            self._create_mock_consultant(nom="B"),
        ]
        
        mock_session = self._create_mock_session(consultants)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        self.chatbot.last_question = "Quelles sont les statistiques ?"
        
        result = self.chatbot._handle_stats_question()
        
        self.assertEqual(result["intent"], "statistiques")
        self.assertIn("response", result)
        self.assertIn("data", result)

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_stats_question_count_consultants(self, mock_get_session):
        """Test comptage consultants"""
        consultants = [self._create_mock_consultant(nom=f"C{i}") for i in range(10)]
        
        mock_session = self._create_mock_session(consultants)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        self.chatbot.last_question = "Combien de consultants ?"
        
        result = self.chatbot._handle_stats_question()
        
        self.assertEqual(result["intent"], "statistiques")
        self.assertIn("10", result["response"])

    # ==================== TESTS: Helper methods avancés ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultants_by_skill(self, mock_get_session):
        """Test recherche consultants par compétence"""
        c1 = self._create_mock_consultant(nom="Python1")
        c2 = self._create_mock_consultant(nom="Python2")
        
        mock_session = self._create_mock_session([c1, c2])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._find_consultants_by_skill("Python")
        
        self.assertEqual(len(result), 2)

    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultants_by_skill_with_type(self, mock_get_session):
        """Test recherche par compétence avec type"""
        c1 = self._create_mock_consultant(nom="Dev")
        
        mock_session = self._create_mock_session([c1])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._find_consultants_by_skill("Python", type_competence="technique")
        
        self.assertIsInstance(result, list)

    @patch("app.services.chatbot_service.get_database_session")
    def test_find_consultants_by_language(self, mock_get_session):
        """Test recherche consultants par langue"""
        c1 = self._create_mock_consultant(nom="Anglophone1")
        c2 = self._create_mock_consultant(nom="Anglophone2")
        
        mock_session = self._create_mock_session([c1, c2])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._find_consultants_by_language("anglais")
        
        self.assertEqual(len(result), 2)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_missions_by_company(self, mock_get_session):
        """Test récupération missions par entreprise"""
        m1 = Mock(spec=Mission)
        m1.client = "BNP Paribas"
        m1.nom_mission = "Mission 1"
        
        mock_session = self._create_mock_session([m1])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._get_missions_by_company("BNP Paribas")
        
        self.assertEqual(len(result), 1)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_missions_by_consultant(self, mock_get_session):
        """Test récupération missions d'un consultant"""
        m1 = Mock(spec=Mission)
        m1.nom_mission = "Mission A"
        m1.consultant_id = 1
        
        mock_session = self._create_mock_session([m1])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._get_missions_by_consultant(1)
        
        self.assertIsInstance(result, list)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_consultant_skills_all_types(self, mock_get_session):
        """Test récupération compétences consultant (tous types)"""
        mock_session = self._create_mock_session([])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._get_consultant_skills(1)
        
        self.assertIsInstance(result, list)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_consultant_skills_technical_only(self, mock_get_session):
        """Test récupération compétences techniques uniquement"""
        mock_session = self._create_mock_session([])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = self.chatbot._get_consultant_skills(1, type_competence="technique")
        
        self.assertIsInstance(result, list)

    def test_calculate_company_seniority_current_employee(self):
        """Test calcul ancienneté employé actuel"""
        consultant = self._create_mock_consultant()
        consultant.date_entree_societe = date(2020, 1, 1)
        consultant.date_sortie_societe = None
        
        seniority = self.chatbot._calculate_company_seniority(consultant)
        
        self.assertGreater(seniority, 5.0)

    def test_calculate_company_seniority_former_employee(self):
        """Test calcul ancienneté ancien employé"""
        consultant = self._create_mock_consultant()
        consultant.date_entree_societe = date(2020, 1, 1)
        consultant.date_sortie_societe = date(2023, 1, 1)
        
        seniority = self.chatbot._calculate_company_seniority(consultant)
        
        self.assertAlmostEqual(seniority, 3.0, delta=0.2)

    def test_calculate_company_seniority_no_entry_date(self):
        """Test ancienneté sans date d'entrée"""
        consultant = self._create_mock_consultant()
        consultant.date_entree_societe = None
        
        seniority = self.chatbot._calculate_company_seniority(consultant)
        
        self.assertEqual(seniority, 0)

    # ==================== TESTS: General stats helpers ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_get_general_stats(self, mock_get_session):
        """Test récupération statistiques générales"""
        consultants = [self._create_mock_consultant(nom=f"C{i}") for i in range(5)]
        
        mock_session = self._create_mock_session(consultants)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        stats = self.chatbot._get_general_stats()
        
        self.assertIn("consultants_total", stats)
        self.assertIn("missions_total", stats)

    # ==================== TESTS: Format helpers ====================
    def test_format_cv_details(self):
        """Test formatage détails CV"""
        cv = Mock()
        cv.fichier_nom = "cv_test.pdf"
        cv.date_upload = datetime(2024, 1, 1)
        cv.taille_fichier = 2048000
        cv.contenu_extrait = "Contenu test"
        
        result = self.chatbot._format_cv_details(cv, 1)
        
        self.assertIn("cv_test.pdf", result)
        self.assertIn("2024", result)

    def test_format_mission_details(self):
        """Test formatage détails mission"""
        mission = Mock(spec=Mission)
        mission.client = "Client Test"
        mission.nom_mission = "Mission Test"
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = date(2024, 12, 31)
        mission.statut = "en_cours"
        mission.taux_journalier = 500
        
        result = self.chatbot._format_mission_details(mission)
        
        self.assertIn("Client Test", result)
        self.assertIn("Mission Test", result)

    # ==================== TESTS: Edge cases ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_practices_question_empty_practice(self, mock_get_session):
        """Test practice sans consultants"""
        practice = Mock(spec=Practice)
        practice.nom = "Empty Practice"
        practice.consultants = []
        
        mock_session = self._create_mock_session(practice)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": [], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": ["Empty Practice"]}
        
        result = self.chatbot._handle_practices_question(entities)
        
        self.assertEqual(result["intent"], "practices")

    @patch("app.services.chatbot_service.get_database_session")
    def test_handle_cvs_question_multiple_cvs(self, mock_get_session):
        """Test consultant avec plusieurs CVs"""
        consultant = self._create_mock_consultant()
        
        cv1 = Mock()
        cv1.fichier_nom = "cv1.pdf"
        cv1.date_upload = datetime(2023, 1, 1)
        cv1.taille_fichier = 1024000
        cv1.contenu_extrait = "CV 1"
        
        cv2 = Mock()
        cv2.fichier_nom = "cv2.pdf"
        cv2.date_upload = datetime(2024, 1, 1)
        cv2.taille_fichier = 2048000
        cv2.contenu_extrait = "CV 2"
        
        consultant.cvs = [cv1, cv2]
        
        mock_session = self._create_mock_session(consultant)
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        entities = {"noms": ["Dupont"], "entreprises": [], "competences": [], "langues": [], "montants": [], "practices": []}
        
        result = self.chatbot._handle_cvs_question(entities)
        
        self.assertEqual(result["intent"], "cvs")
        self.assertIn("2", result["response"])

    # ==================== TESTS: Boundary cases ====================
    def test_calculate_cjm_boundary_values(self):
        """Test calcul CJM valeurs limites"""
        self.assertEqual(self.chatbot._calculate_cjm(0), 0.0)
        self.assertGreater(self.chatbot._calculate_cjm(100000), 0)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_salary_stats_empty_db(self, mock_get_session):
        """Test stats salaires avec DB vide"""
        mock_session = self._create_mock_session([])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        stats = self.chatbot._get_salary_stats()
        
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["moyenne"], 0)

    @patch("app.services.chatbot_service.get_database_session")
    def test_get_salary_stats_single_consultant(self, mock_get_session):
        """Test stats salaires avec un seul consultant"""
        consultant = self._create_mock_consultant(salaire=50000)
        
        mock_session = self._create_mock_session([consultant])
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        stats = self.chatbot._get_salary_stats()
        
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["moyenne"], 50000)
        self.assertEqual(stats["mediane"], 50000)

    # ==================== TESTS: Format response helpers ====================
    @patch("app.services.chatbot_service.get_database_session")
    def test_format_consultant_missions_list(self, mock_get_session):
        """Test formatage liste missions consultant"""
        consultant = self._create_mock_consultant()
        
        mission1 = Mock(spec=Mission)
        mission1.client = "Client 1"
        mission1.nom_mission = "Mission 1"
        mission1.date_debut = date(2023, 1, 1)
        mission1.date_fin = date(2023, 6, 30)
        mission1.statut = "termine"
        mission1.taux_journalier = 500
        
        missions = [mission1]
        
        response = self.chatbot._format_consultant_missions_list(consultant, missions)
        
        self.assertIn("Jean", response)
        self.assertIn("Dupont", response)
        self.assertIn("Mission 1", response)

    @patch("app.services.chatbot_service.get_database_session")
    def test_format_consultant_missions_count(self, mock_get_session):
        """Test formatage comptage missions"""
        consultant = self._create_mock_consultant()
        
        mission1 = Mock(spec=Mission)
        mission1.statut = "en_cours"
        
        mission2 = Mock(spec=Mission)
        mission2.statut = "termine"
        
        missions = [mission1, mission2]
        
        response = self.chatbot._format_consultant_missions_count(consultant, missions)
        
        self.assertIn("2", response)
        self.assertIn("Jean", response)

    # ==================== TESTS: Additional coverage ====================
    def test_get_response_empty_question(self):
        """Test get_response avec question vide"""
        result = self.chatbot.get_response("")
        
        self.assertIsInstance(result, str)

    def test_get_response_none_result(self):
        """Test get_response quand process_question retourne None"""
        self.chatbot.process_question = Mock(return_value={"response": None})
        
        result = self.chatbot.get_response("Test")
        
        self.assertIn("pas compris", result)


if __name__ == "__main__":
    unittest.main()
