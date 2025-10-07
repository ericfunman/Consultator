"""
Tests unitaires pour le module practice_service.py - Phase 27
Coverage target: 63.5% → 80%+ (gain estimé +16-17%)

Stratégie:
- CRUD practices: get_all, get_by_id, get_by_name, create, update
- Gestion consultants par practice: get_consultants_by_practice
- Assignation consultants: assign_consultant_to_practice
- Statistiques: get_practice_statistics
- Initialisation: init_default_practices

Fonctions clés à tester (89 lignes manquantes):
- get_all_practices, get_practice_by_id, get_practice_by_name
- create_practice, update_practice
- get_consultants_by_practice (+ méthodes privées)
- assign_consultant_to_practice
- get_practice_statistics
- init_default_practices
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestGetAllPractices(unittest.TestCase):
    """Tests pour get_all_practices"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_all_practices_success(self, mock_st, mock_get_session):
        """Test récupération toutes practices réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice1 = Mock(id=1, nom="Data", actif=True)
        practice2 = Mock(id=2, nom="Quant", actif=True)

        mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
            practice1,
            practice2,
        ]

        result = PracticeService.get_all_practices()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].nom, "Data")
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_all_practices_error(self, mock_st, mock_get_session):
        """Test récupération practices avec erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.side_effect = SQLAlchemyError("Database error")

        result = PracticeService.get_all_practices()

        self.assertEqual(result, [])
        mock_st.error.assert_called_once()
        mock_session.close.assert_called_once()


class TestGetPracticeById(unittest.TestCase):
    """Tests pour get_practice_by_id"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_id_found(self, mock_st, mock_get_session):
        """Test récupération practice par ID existant"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice = Mock(id=1, nom="Data")
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        result = PracticeService.get_practice_by_id(1)

        self.assertIsNotNone(result)
        self.assertEqual(result.nom, "Data")
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_id_not_found(self, mock_st, mock_get_session):
        """Test récupération practice par ID inexistant"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.get_practice_by_id(999)

        self.assertIsNone(result)
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_id_error(self, mock_st, mock_get_session):
        """Test récupération practice avec erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.side_effect = SQLAlchemyError("Database error")

        result = PracticeService.get_practice_by_id(1)

        self.assertIsNone(result)
        mock_st.error.assert_called_once()


class TestGetPracticeByName(unittest.TestCase):
    """Tests pour get_practice_by_name"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_name_found(self, mock_st, mock_get_session):
        """Test récupération practice par nom existant"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice = Mock(id=1, nom="Data")
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        result = PracticeService.get_practice_by_name("Data")

        self.assertIsNotNone(result)
        self.assertEqual(result.nom, "Data")

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_name_not_found(self, mock_st, mock_get_session):
        """Test récupération practice par nom inexistant"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.get_practice_by_name("Inexistante")

        self.assertIsNone(result)


class TestCreatePractice(unittest.TestCase):
    """Tests pour create_practice"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_create_practice_success(self, mock_st, mock_get_session):
        """Test création practice réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        # Pas de practice existante
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.create_practice("Data", "Practice Data", "Jean Dupont")

        self.assertIsNotNone(result)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_create_practice_already_exists(self, mock_st, mock_get_session):
        """Test création practice déjà existante"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        # Practice existante
        existing = Mock(id=1, nom="Data")
        mock_session.query.return_value.filter.return_value.first.return_value = existing

        result = PracticeService.create_practice("Data", "Practice Data")

        self.assertIsNone(result)
        mock_st.error.assert_called_once()
        mock_session.add.assert_not_called()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_create_practice_error(self, mock_st, mock_get_session):
        """Test création practice avec erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        result = PracticeService.create_practice("Data")

        self.assertIsNone(result)
        mock_st.error.assert_called()


class TestUpdatePractice(unittest.TestCase):
    """Tests pour update_practice"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_update_practice_success(self, mock_st, mock_get_session):
        """Test mise à jour practice réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice = Mock(id=1, nom="Data", description="Ancienne description")
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        result = PracticeService.update_practice(1, description="Nouvelle description", responsable="Jean")

        self.assertTrue(result)
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_update_practice_not_found(self, mock_st, mock_get_session):
        """Test mise à jour practice inexistante"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.update_practice(999, nom="Test")

        self.assertFalse(result)
        mock_st.error.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_update_practice_error(self, mock_st, mock_get_session):
        """Test mise à jour practice avec erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice = Mock(id=1)
        mock_session.query.return_value.filter.return_value.first.return_value = practice
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        result = PracticeService.update_practice(1, nom="Test")

        self.assertFalse(result)
        mock_st.error.assert_called()


class TestGetConsultantsByPractice(unittest.TestCase):
    """Tests pour get_consultants_by_practice"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_consultants_by_practice_specific(self, mock_st, mock_get_session):
        """Test récupération consultants d'une practice spécifique"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice = Mock(id=1, nom="Data")
        consultant = Mock(id=1, nom="Dupont")

        # Mock pour la requête practice
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        # Mock pour la requête consultants
        mock_query = MagicMock()
        mock_session.query.return_value.options.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.all.return_value = [consultant]

        result = PracticeService.get_consultants_by_practice(practice_id=1)

        self.assertIn("Data", result)
        self.assertEqual(len(result["Data"]), 1)

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_consultants_by_practice_all(self, mock_st, mock_get_session):
        """Test récupération tous consultants groupés par practice"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice1 = Mock(id=1, nom="Data", actif=True)
        practice2 = Mock(id=2, nom="Quant", actif=True)

        # Mock practices
        mock_session.query.return_value.filter.return_value.all.return_value = [practice1, practice2]

        result = PracticeService.get_consultants_by_practice()

        self.assertIsInstance(result, dict)


class TestAssignConsultantToPractice(unittest.TestCase):
    """Tests pour assign_consultant_to_practice"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_assign_consultant_success(self, mock_st, mock_get_session):
        """Test assignation consultant à practice réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        consultant = Mock(id=1, practice_id=None)
        practice = Mock(id=1, nom="Data")

        # Premier appel: consultant, deuxième: practice
        mock_session.query.return_value.filter.return_value.first.side_effect = [consultant, practice]

        result = PracticeService.assign_consultant_to_practice(1, 1)

        self.assertTrue(result)
        self.assertEqual(consultant.practice_id, 1)
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_assign_consultant_remove_from_practice(self, mock_st, mock_get_session):
        """Test retrait consultant de sa practice"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        consultant = Mock(id=1, practice_id=1)
        mock_session.query.return_value.filter.return_value.first.return_value = consultant

        result = PracticeService.assign_consultant_to_practice(1, None)

        self.assertTrue(result)
        self.assertIsNone(consultant.practice_id)
        mock_st.success.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_assign_consultant_not_found(self, mock_st, mock_get_session):
        """Test assignation consultant inexistant"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.assign_consultant_to_practice(999, 1)

        self.assertFalse(result)
        mock_st.error.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_assign_consultant_practice_not_found(self, mock_st, mock_get_session):
        """Test assignation à practice inexistante"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        consultant = Mock(id=1)
        # Premier appel: consultant trouvé, deuxième: practice non trouvée
        mock_session.query.return_value.filter.return_value.first.side_effect = [consultant, None]

        result = PracticeService.assign_consultant_to_practice(1, 999)

        self.assertFalse(result)
        mock_st.error.assert_called()


class TestGetPracticeStatistics(unittest.TestCase):
    """Tests pour get_practice_statistics"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_statistics_success(self, mock_st, mock_get_session):
        """Test récupération statistiques practices"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        practice1 = Mock(id=1, nom="Data", responsable="Jean")
        practice2 = Mock(id=2, nom="Quant", responsable=None)

        mock_session.query.return_value.filter.return_value.all.return_value = [practice1, practice2]

        # Mock comptages
        mock_session.query.return_value.filter.return_value.count.side_effect = [
            5,  # Consultants practice 1
            3,  # Consultants actifs practice 1
            4,  # Consultants practice 2
            2,  # Consultants actifs practice 2
            2,  # Sans practice
            1,  # Sans practice actifs
        ]

        result = PracticeService.get_practice_statistics()

        self.assertEqual(result["total_practices"], 2)
        self.assertEqual(result["total_consultants"], 11)  # 5+4+2
        self.assertEqual(len(result["practices_detail"]), 3)  # 2 practices + sans practice

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_statistics_no_practices(self, mock_st, mock_get_session):
        """Test statistiques sans practices"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        mock_session.query.return_value.filter.return_value.all.return_value = []
        mock_session.query.return_value.filter.return_value.count.return_value = 0

        result = PracticeService.get_practice_statistics()

        self.assertEqual(result["total_practices"], 0)
        self.assertEqual(result["total_consultants"], 0)

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_statistics_error(self, mock_st, mock_get_session):
        """Test statistiques avec erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.side_effect = SQLAlchemyError("Database error")

        result = PracticeService.get_practice_statistics()

        self.assertEqual(result["total_practices"], 0)
        mock_st.error.assert_called_once()


class TestInitDefaultPractices(unittest.TestCase):
    """Tests pour init_default_practices"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_init_default_practices_empty_db(self, mock_st, mock_get_session):
        """Test initialisation practices dans DB vide"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        # Pas de practices existantes
        mock_session.query.return_value.all.return_value = []

        PracticeService.init_default_practices()

        # 2 practices ajoutées (Data et Quant)
        self.assertEqual(mock_session.add.call_count, 2)
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_init_default_practices_already_exists(self, mock_st, mock_get_session):
        """Test initialisation practices déjà existantes"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        # Practices existantes
        existing = [Mock(id=1, nom="Data")]
        mock_session.query.return_value.all.return_value = existing

        PracticeService.init_default_practices()

        # Aucune practice ajoutée
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_init_default_practices_error(self, mock_st, mock_get_session):
        """Test initialisation practices avec erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.side_effect = SQLAlchemyError("Database error")

        PracticeService.init_default_practices()

        mock_st.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
