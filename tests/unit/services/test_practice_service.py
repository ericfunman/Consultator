"""
Tests pour le service PracticeService
Couverture des fonctionnalités CRUD et recherche
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from app.services.practice_service import PracticeService
from app.database.models import Practice, Consultant


class TestPracticeService:
    """Tests pour PracticeService"""

    def test_get_all_practices_success(self):
        """Test récupération de toutes les practices actives - cas succès"""
        # Mock practices
        mock_practice1 = Mock(spec=Practice)
        mock_practice1.id = 1
        mock_practice1.nom = "Data Science"
        mock_practice1.actif = True

        mock_practice2 = Mock(spec=Practice)
        mock_practice2.id = 2
        mock_practice2.nom = "Quant"
        mock_practice2.actif = True

        with patch('app.services.practice_service.get_database_session') as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__.return_value = None

            # Mock query chain
            mock_filtered = MagicMock()
            mock_ordered = MagicMock()
            mock_ordered.all.return_value = [mock_practice1, mock_practice2]
            mock_filtered.order_by.return_value = mock_ordered
            mock_session_instance.query.return_value.filter_by.return_value = mock_filtered

            # Test
            result = PracticeService.get_all_practices()

            # Vérifications
            assert len(result) == 2
            assert result[0].nom == "Data Science"
            assert result[1].nom == "Quant"

    def test_get_practice_by_id_found(self):
        """Test récupération practice par ID - trouvée"""
        mock_practice = Mock(spec=Practice)
        mock_practice.id = 1
        mock_practice.nom = "Data Science"

        with patch('app.services.practice_service.get_database_session') as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__.return_value = None

            # Mock query chain
            mock_filtered = MagicMock()
            mock_filtered.first.return_value = mock_practice
            mock_session_instance.query.return_value.filter_by.return_value = mock_filtered  # Fix: use filter_by

            # Test
            result = PracticeService.get_practice_by_id(1)

            # Vérifications
            assert result is not None
            assert result.id == 1
            assert result.nom == "Data Science"

    def test_get_practice_by_name_found(self):
        """Test récupération practice par nom - trouvée"""
        mock_practice = Mock(spec=Practice)
        mock_practice.id = 1
        mock_practice.nom = "Data Science"

        with patch('app.services.practice_service.get_database_session') as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__.return_value = None

            # Mock query chain
            mock_filtered = MagicMock()
            mock_filtered.first.return_value = mock_practice
            mock_session_instance.query.return_value.filter_by.return_value = mock_filtered  # Fix: use filter_by

            # Test
            result = PracticeService.get_practice_by_name("Data Science")

            # Vérifications
            assert result is not None
            assert result.nom == "Data Science"

    def test_create_practice_success(self):
        """Test création practice - cas succès"""
        with patch('app.services.practice_service.get_database_session') as mock_session, \
             patch('app.services.practice_service.st') as mock_st, \
             patch('app.services.practice_service.Practice') as mock_practice_class:

            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__.return_value = None

            # Mock practice créée
            mock_practice = Mock(spec=Practice)
            mock_practice.id = 1
            mock_practice.nom = "New Practice"
            mock_practice_class.return_value = mock_practice

            # Mock query pour vérifier existence (retourne None = n'existe pas)
            mock_filtered = MagicMock()
            mock_filtered.first.return_value = None
            mock_session_instance.query.return_value.filter_by.return_value = mock_filtered

            # Test
            result = PracticeService.create_practice("New Practice", "Description", "Responsable")

            # Vérifications
            assert result is not None
            mock_session_instance.add.assert_called_once_with(mock_practice)
            mock_session_instance.commit.assert_called_once()
            mock_st.success.assert_called_once_with("Practice 'New Practice' créée avec succès")

    def test_update_practice_success(self):
        """Test mise à jour practice - cas succès"""
        with patch('app.services.practice_service.get_database_session') as mock_session, \
             patch('app.services.practice_service.st') as mock_st:

            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__.return_value = None

            # Mock practice existante
            mock_practice = Mock(spec=Practice)
            mock_practice.id = 1
            mock_practice.nom = "Old Name"

            # Mock query
            mock_filtered = MagicMock()
            mock_filtered.first.return_value = mock_practice
            mock_session_instance.query.return_value.filter_by.return_value = mock_filtered

        # Test
        result = PracticeService.update_practice(1, nom="New Name", description="New Description")

        # Vérifications
        assert result is True
        assert mock_practice.nom == "New Name"
        assert mock_practice.description == "New Description"
        mock_session_instance.commit.assert_called_once()
        mock_st.success.assert_called_once_with("Practice mise à jour avec succès")

    def test_get_practice_statistics(self):
        """Test récupération statistiques practices"""
        with patch('app.services.practice_service.get_database_session') as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__.return_value = None

            # Mock practices
            mock_practice1 = Mock(spec=Practice)
            mock_practice1.id = 1
            mock_practice1.nom = "Data Science"
            mock_practice1.responsable = "John Doe"

            mock_practice2 = Mock(spec=Practice)
            mock_practice2.id = 2
            mock_practice2.nom = "Quant"
            mock_practice2.responsable = "Jane Smith"

            # Mock queries
            mock_query = MagicMock()
            mock_query.filter.return_value.all.return_value = [mock_practice1, mock_practice2]
            mock_query.filter.return_value.count.side_effect = [5, 3, 2, 1]
            mock_session_instance.query.return_value = mock_query

            # Test
            result = PracticeService.get_practice_statistics()

            # Vérifications
            assert result["total_practices"] == 2
            assert result["total_consultants"] == 11  # 5 + 3 + 2 + 1
            assert len(result["practices_detail"]) == 3  # 2 practices + "Sans Practice"
            assert result["practices_detail"][0]["nom"] == "Data Science"
            assert result["practices_detail"][0]["total_consultants"] == 5
            assert result["practices_detail"][0]["consultants_actifs"] == 3

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_get_all_practices_database_error(self, mock_st, mock_session):
        """Test récupération practices - erreur base de données"""
        from sqlalchemy.exc import SQLAlchemyError

        # Mock session qui lève une exception
        mock_session_instance = MagicMock()
        mock_session_instance.query.side_effect = SQLAlchemyError("Database connection failed")
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Test
        result = PracticeService.get_all_practices()

        # Vérifications
        assert result == []
        mock_st.error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    def test_get_practice_by_id_found(self, mock_session):
        """Test récupération practice par ID - trouvée"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock practice
        mock_practice = Mock(spec=Practice)
        mock_practice.id = 1
        mock_practice.nom = "Data Science"

        # Mock query chain
        mock_filtered = MagicMock()
        mock_filtered.first.return_value = mock_practice
        mock_session_instance.query.return_value.filter.return_value = mock_filtered

        # Test
        result = PracticeService.get_practice_by_id(1)

        # Vérifications
        assert result is not None
        assert result.id == 1
        assert result.nom == "Data Science"

    @patch('app.services.practice_service.get_database_session')
    def test_get_practice_by_id_not_found(self, mock_session):
        """Test récupération practice par ID - non trouvée"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock query qui ne trouve rien
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        # Test
        result = PracticeService.get_practice_by_id(999)

        # Vérifications
        assert result is None

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_get_practice_by_id_error(self, mock_st, mock_session):
        """Test récupération practice par ID - erreur base de données"""
        from sqlalchemy.exc import SQLAlchemyError

        # Mock session qui lève une exception
        mock_session_instance = MagicMock()
        mock_session_instance.query.side_effect = SQLAlchemyError("Database connection failed")
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Test
        result = PracticeService.get_practice_by_id(1)

        # Vérifications
        assert result is None
        mock_st.error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    def test_get_practice_by_name_found(self, mock_session):
        """Test récupération practice par nom - trouvée"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock practice
        mock_practice = Mock(spec=Practice)
        mock_practice.id = 1
        mock_practice.nom = "Data Science"

        # Mock query chain
        mock_filtered = MagicMock()
        mock_filtered.first.return_value = mock_practice
        mock_session_instance.query.return_value.filter.return_value = mock_filtered

        # Test
        result = PracticeService.get_practice_by_name("Data Science")

        # Vérifications
        assert result is not None
        assert result.nom == "Data Science"

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_create_practice_success(self, mock_st, mock_session):
        """Test création practice - cas succès"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock practice créée
        mock_practice = Mock(spec=Practice)
        mock_practice.id = 1
        mock_practice.nom = "New Practice"

        # Mock query pour vérifier existence (retourne None = n'existe pas)
        mock_filtered = MagicMock()
        mock_filtered.first.return_value = None
        mock_session_instance.query.return_value.filter_by.return_value = mock_filtered  # Fix: use filter_by

        # Mock Practice constructor
        with patch('app.services.practice_service.Practice') as mock_practice_class:
            mock_practice_class.return_value = mock_practice

            # Test
            result = PracticeService.create_practice("New Practice", "Description", "Responsable")

            # Vérifications
            assert result is not None
            mock_session_instance.add.assert_called_once_with(mock_practice)
            mock_session_instance.commit.assert_called_once()
            mock_st.success.assert_called_once_with("Practice 'New Practice' créée avec succès")

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_create_practice_already_exists(self, mock_st, mock_session):
        """Test création practice - practice existe déjà"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock practice existante
        mock_existing = Mock()
        mock_existing.nom = "Existing Practice"

        # Mock query qui trouve une practice existante
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_existing
        mock_session_instance.query.return_value = mock_query

        # Test
        result = PracticeService.create_practice("Existing Practice")

        # Vérifications
        assert result is None
        mock_st.error.assert_called_once_with("La practice 'Existing Practice' existe déjà")

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_update_practice_success(self, mock_st, mock_session):
        """Test mise à jour practice - cas succès"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock practice existante
        mock_practice = Mock()
        mock_practice.id = 1
        mock_practice.nom = "Old Name"

        # Mock query
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_practice
        mock_session_instance.query.return_value = mock_query

        # Mock commit
        mock_session_instance.commit = MagicMock()

        # Test
        result = PracticeService.update_practice(1, nom="New Name", description="New Description")

        # Vérifications
        assert result is True
        assert mock_practice.nom == "New Name"
        mock_session_instance.commit.assert_called_once()
        mock_st.success.assert_called_once_with("Practice mise à jour avec succès")

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_update_practice_not_found(self, mock_st, mock_session):
        """Test mise à jour practice - practice non trouvée"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock query qui ne trouve rien
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        # Test
        result = PracticeService.update_practice(999, nom="New Name")

        # Vérifications
        assert result is False
        mock_st.error.assert_called_once_with("Practice non trouvée")

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_assign_consultant_to_practice_success(self, mock_st, mock_session):
        """Test assignation consultant à practice - cas succès"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock consultant et practice
        mock_consultant = Mock()
        mock_consultant.id = 1

        mock_practice = Mock()
        mock_practice.id = 1
        mock_practice.nom = "Data Science"

        # Mock queries
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.side_effect = [mock_consultant, mock_practice]
        mock_session_instance.query.return_value = mock_query

        # Mock commit
        mock_session_instance.commit = MagicMock()

        # Test
        result = PracticeService.assign_consultant_to_practice(1, 1)

        # Vérifications
        assert result is True
        assert mock_consultant.practice_id == 1
        mock_session_instance.commit.assert_called_once()
        mock_st.success.assert_called_once_with("Consultant assigné à la practice Data Science")

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_assign_consultant_to_practice_remove_assignment(self, mock_st, mock_session):
        """Test retrait consultant de practice"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1

        # Mock query pour consultant seulement (pas de practice)
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.side_effect = [mock_consultant, None]
        mock_session_instance.query.return_value = mock_query

        # Mock commit
        mock_session_instance.commit = MagicMock()

        # Test (practice_id = None pour retirer)
        result = PracticeService.assign_consultant_to_practice(1, None)

        # Vérifications
        assert result is True
        assert mock_consultant.practice_id is None
        mock_st.success.assert_called_once_with("Consultant retiré de sa practice")

    @patch('app.services.practice_service.get_database_session')
    def test_get_practice_statistics(self, mock_session):
        """Test récupération statistiques practices"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock practices
        mock_practice1 = Mock()
        mock_practice1.id = 1
        mock_practice1.nom = "Data Science"
        mock_practice1.responsable = "John Doe"

        mock_practice2 = Mock()
        mock_practice2.id = 2
        mock_practice2.nom = "Quant"
        mock_practice2.responsable = "Jane Smith"

        # Mock queries
        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = [mock_practice1, mock_practice2]
        mock_query.filter.return_value.count.side_effect = [5, 3, 2, 1]  # Consultants par practice
        mock_session_instance.query.return_value = mock_query

        # Test
        result = PracticeService.get_practice_statistics()

        # Vérifications
        assert result["total_practices"] == 2
        assert result["total_consultants"] == 11  # 5 + 3 + 2 + 1
        assert len(result["practices_detail"]) == 3  # 2 practices + "Sans Practice"
        assert result["practices_detail"][0]["nom"] == "Data Science"
        assert result["practices_detail"][0]["total_consultants"] == 5
        assert result["practices_detail"][0]["consultants_actifs"] == 3

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_init_default_practices_success(self, mock_st, mock_session):
        """Test initialisation practices par défaut - cas succès"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock query qui retourne liste vide (aucune practice existante)
        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = []
        mock_session_instance.query.return_value = mock_query

        # Mock add et commit
        mock_session_instance.add = MagicMock()
        mock_session_instance.commit = MagicMock()

        # Test
        PracticeService.init_default_practices()

        # Vérifications
        # Doit ajouter 2 practices (Data et Quant)
        assert mock_session_instance.add.call_count == 2
        mock_session_instance.commit.assert_called_once()
        mock_st.success.assert_called_once_with("Practices par défaut initialisées : Data et Quant")

    @patch('app.services.practice_service.get_database_session')
    @patch('app.services.practice_service.st')
    def test_init_default_practices_already_exist(self, mock_st, mock_session):
        """Test initialisation practices par défaut - practices existent déjà"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock query qui retourne practices existantes
        mock_existing = Mock()
        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = [mock_existing]  # Au moins une practice existe
        mock_session_instance.query.return_value = mock_query

        # Test
        PracticeService.init_default_practices()

        # Vérifications
        # Ne doit rien ajouter si des practices existent déjà
        mock_session_instance.add.assert_not_called()
        mock_session_instance.commit.assert_not_called()
        mock_st.success.assert_not_called()
