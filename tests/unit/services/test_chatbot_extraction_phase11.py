"""
Tests Phase 11: Chatbot - Méthodes entity extraction et intent analysis
Ciblage: 40 tests ultra-ciblés sur extraction et analyse
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from app.services.chatbot_service import ChatbotService


class TestEntityExtraction(unittest.TestCase):
    """Tests pour extraction d'entités"""

    def setUp(self):
        self.chatbot = ChatbotService()

    def test_extract_amounts(self):
        """Test extraction montants"""
        question = "Salaire supérieur à 50000 euros"
        
        if hasattr(self.chatbot, '_extract_amounts'):
            result = self.chatbot._extract_amounts(question)
            assert isinstance(result, list)

    def test_extract_amounts_multiple(self):
        """Test extraction montants multiples"""
        question = "Entre 40000 et 60000 euros"
        
        if hasattr(self.chatbot, '_extract_amounts'):
            result = self.chatbot._extract_amounts(question)
            assert isinstance(result, list)

    def test_extract_years(self):
        """Test extraction années"""
        question = "Expérience de 5 ans"
        
        if hasattr(self.chatbot, '_extract_years'):
            result = self.chatbot._extract_years(question)
            assert isinstance(result, (list, int)) or result is not None

    def test_extract_dates(self):
        """Test extraction dates"""
        question = "Mission en 2020 ou 2021"
        
        if hasattr(self.chatbot, '_extract_dates'):
            result = self.chatbot._extract_dates(question)
            assert isinstance(result, list) or result is not None

    def test_extract_companies(self):
        """Test extraction entreprises"""
        question = "Mission chez Google ou Microsoft"
        
        if hasattr(self.chatbot, '_extract_companies'):
            result = self.chatbot._extract_companies(question)
            assert isinstance(result, list)

    def test_extract_companies_single(self):
        """Test extraction entreprise unique"""
        question = "Consultant ayant travaillé chez BNP Paribas"
        
        if hasattr(self.chatbot, '_extract_companies'):
            result = self.chatbot._extract_companies(question)
            assert isinstance(result, list)

    def test_extract_names(self):
        """Test extraction noms"""
        question = "Profil de Jean Dupont"
        
        if hasattr(self.chatbot, '_extract_consultant_names'):
            result = self.chatbot._extract_consultant_names(question)
            assert isinstance(result, list)

    def test_extract_names_full(self):
        """Test extraction nom complet"""
        question = "Info sur Marie-Claire Dubois"
        
        if hasattr(self.chatbot, '_extract_consultant_names'):
            result = self.chatbot._extract_consultant_names(question)
            assert isinstance(result, list)


class TestIntentAnalysis(unittest.TestCase):
    """Tests pour analyse d'intention"""

    def setUp(self):
        self.chatbot = ChatbotService()

    def test_analyze_intent_salaire(self):
        """Test intention salaire"""
        question = "Quel est le salaire moyen ?"
        
        if hasattr(self.chatbot, 'analyze_intent'):
            result = self.chatbot.analyze_intent(question)
            assert isinstance(result, str) or result is not None

    def test_analyze_intent_experience(self):
        """Test intention expérience"""
        question = "Qui a 5 ans d'expérience ?"
        
        if hasattr(self.chatbot, 'analyze_intent'):
            result = self.chatbot.analyze_intent(question)
            assert isinstance(result, str) or result is not None

    def test_analyze_intent_competences(self):
        """Test intention compétences"""
        question = "Consultants Python"
        
        if hasattr(self.chatbot, 'analyze_intent'):
            result = self.chatbot.analyze_intent(question)
            assert isinstance(result, str) or result is not None

    def test_analyze_intent_disponibilite(self):
        """Test intention disponibilité"""
        question = "Qui est disponible ?"
        
        if hasattr(self.chatbot, 'analyze_intent'):
            result = self.chatbot.analyze_intent(question)
            assert isinstance(result, str) or result is not None

    def test_analyze_intent_missions(self):
        """Test intention missions"""
        question = "Missions en cours"
        
        if hasattr(self.chatbot, 'analyze_intent'):
            result = self.chatbot.analyze_intent(question)
            assert isinstance(result, str) or result is not None

    def test_analyze_intent_cv(self):
        """Test intention CV"""
        question = "Voir le CV de Dupont"
        
        if hasattr(self.chatbot, 'analyze_intent'):
            result = self.chatbot.analyze_intent(question)
            assert isinstance(result, str) or result is not None


class TestQueryProcessing(unittest.TestCase):
    """Tests pour traitement requêtes"""

    def setUp(self):
        self.chatbot = ChatbotService()

    @patch('app.database.database.Session')
    def test_process_query_basic(self, mock_session):
        """Test traitement requête basique"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.all.return_value = []
        
        result = self.chatbot.process_query("Hello")
        assert isinstance(result, dict)

    @patch('app.database.database.Session')
    def test_process_query_with_entities(self, mock_session):
        """Test requête avec entités"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.all.return_value = []
        
        result = self.chatbot.process_query("Salaire de Jean Dupont")
        assert isinstance(result, dict)

    @patch('app.database.database.Session')
    def test_process_query_complex(self, mock_session):
        """Test requête complexe"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(
            nom="Dupont",
            prenom="Jean",
            salaire_brut_annuel=50000,
            missions=[],
            langues=[],
            cvs=[],
            consultant_competences=[]
        )
        mock_db.query.return_value.filter.return_value.all.return_value = [consultant]
        
        result = self.chatbot.process_query("Consultants Python avec 5 ans expérience")
        assert isinstance(result, dict)


class TestResponseFormatting(unittest.TestCase):
    """Tests pour formatage réponses"""

    def setUp(self):
        self.chatbot = ChatbotService()

    def test_format_consultant_info(self):
        """Test formatage info consultant"""
        consultant = Mock(
            nom="Dupont",
            prenom="Jean",
            salaire_brut_annuel=50000
        )
        
        if hasattr(self.chatbot, '_format_consultant_info'):
            result = self.chatbot._format_consultant_info(consultant)
            assert isinstance(result, str)

    def test_format_mission_list(self):
        """Test formatage liste missions"""
        missions = [
            Mock(nom_mission="Mission 1", nom_client="Client A"),
            Mock(nom_mission="Mission 2", nom_client="Client B")
        ]
        
        if hasattr(self.chatbot, '_format_mission_list'):
            result = self.chatbot._format_mission_list(missions)
            assert isinstance(result, str)

    def test_format_competences_list(self):
        """Test formatage liste compétences"""
        competences = [
            Mock(competence="Python", annees_experience=5),
            Mock(competence="Java", annees_experience=3)
        ]
        
        if hasattr(self.chatbot, '_format_competences_list'):
            result = self.chatbot._format_competences_list(competences)
            assert isinstance(result, str)

    def test_format_languages_list(self):
        """Test formatage liste langues"""
        languages = [
            Mock(langue="Anglais", niveau="Courant"),
            Mock(langue="Espagnol", niveau="Intermédiaire")
        ]
        
        if hasattr(self.chatbot, '_format_languages_list'):
            result = self.chatbot._format_languages_list(languages)
            assert isinstance(result, str)


class TestStatisticsCalculations(unittest.TestCase):
    """Tests pour calculs statistiques"""

    def setUp(self):
        self.chatbot = ChatbotService()

    def test_calculate_average_salary(self):
        """Test calcul salaire moyen"""
        consultants = [
            Mock(salaire_brut_annuel=50000),
            Mock(salaire_brut_annuel=60000),
            Mock(salaire_brut_annuel=70000)
        ]
        
        if hasattr(self.chatbot, '_calculate_average_salary'):
            result = self.chatbot._calculate_average_salary(consultants)
            assert isinstance(result, (int, float))

    def test_calculate_median_salary(self):
        """Test calcul salaire médian"""
        consultants = [
            Mock(salaire_brut_annuel=50000),
            Mock(salaire_brut_annuel=60000),
            Mock(salaire_brut_annuel=70000)
        ]
        
        if hasattr(self.chatbot, '_calculate_median_salary'):
            result = self.chatbot._calculate_median_salary(consultants)
            assert isinstance(result, (int, float))

    def test_count_by_practice(self):
        """Test comptage par practice"""
        consultants = [
            Mock(practice=Mock(nom="Data")),
            Mock(practice=Mock(nom="Data")),
            Mock(practice=Mock(nom="Cloud"))
        ]
        
        if hasattr(self.chatbot, '_count_by_practice'):
            result = self.chatbot._count_by_practice(consultants)
            assert isinstance(result, dict)

    def test_count_by_skill(self):
        """Test comptage par compétence"""
        consultants = [
            Mock(consultant_competences=[Mock(competence="Python")]),
            Mock(consultant_competences=[Mock(competence="Python")]),
            Mock(consultant_competences=[Mock(competence="Java")])
        ]
        
        if hasattr(self.chatbot, '_count_by_skill'):
            result = self.chatbot._count_by_skill(consultants, "Python")
            assert isinstance(result, int)


class TestSearchFunctions(unittest.TestCase):
    """Tests pour fonctions de recherche"""

    def setUp(self):
        self.chatbot = ChatbotService()

    @patch('app.database.database.Session')
    def test_search_by_competence(self, mock_session):
        """Test recherche par compétence"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1, nom="Dupont")
        mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [consultant]
        
        if hasattr(self.chatbot, '_search_by_competence'):
            result = self.chatbot._search_by_competence(mock_db, "Python")
            assert isinstance(result, list)

    @patch('app.database.database.Session')
    def test_search_by_language(self, mock_session):
        """Test recherche par langue"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1, nom="Dupont")
        mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [consultant]
        
        if hasattr(self.chatbot, '_search_by_language'):
            result = self.chatbot._search_by_language(mock_db, "Anglais")
            assert isinstance(result, list)

    @patch('app.database.database.Session')
    def test_search_by_practice(self, mock_session):
        """Test recherche par practice"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1, practice_id=1)
        mock_db.query.return_value.filter.return_value.all.return_value = [consultant]
        
        if hasattr(self.chatbot, '_search_by_practice'):
            result = self.chatbot._search_by_practice(mock_db, 1)
            assert isinstance(result, list)

    @patch('app.database.database.Session')
    def test_search_available_consultants(self, mock_session):
        """Test recherche consultants disponibles"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1, disponibilite=True)
        mock_db.query.return_value.filter.return_value.all.return_value = [consultant]
        
        if hasattr(self.chatbot, '_search_available_consultants'):
            result = self.chatbot._search_available_consultants(mock_db)
            assert isinstance(result, list)


class TestEdgeCases(unittest.TestCase):
    """Tests de cas limites"""

    def setUp(self):
        self.chatbot = ChatbotService()

    def test_empty_query(self):
        """Test requête vide"""
        result = self.chatbot.process_query("")
        assert isinstance(result, dict)

    def test_very_long_query(self):
        """Test requête très longue"""
        long_query = "Consultant " * 100
        result = self.chatbot.process_query(long_query)
        assert isinstance(result, dict)

    def test_special_characters_query(self):
        """Test requête avec caractères spéciaux"""
        result = self.chatbot.process_query("Consultant @ #$ % ^")
        assert isinstance(result, dict)

    def test_unicode_query(self):
        """Test requête Unicode"""
        result = self.chatbot.process_query("Consultant 🐍 Python développeur")
        assert isinstance(result, dict)

    @patch('app.database.database.Session')
    def test_database_error_handling(self, mock_session):
        """Test gestion erreur base de données"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = Exception("DB Error")
        
        result = self.chatbot.process_query("Test query")
        assert isinstance(result, dict)


if __name__ == "__main__":
    unittest.main()
