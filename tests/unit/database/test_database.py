"""
Tests pour le module database
"""
import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class TestDatabaseModule:
    """Tests pour les fonctions de base de données"""

    @patch('app.database.database.st')
    @patch('app.database.database.create_engine')
    def test_get_database_engine(self, mock_create_engine, mock_st):
        """Test de la création de l'engine de base de données"""
        from app.database.database import get_database_engine

        # Mock de l'engine
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine

        result = get_database_engine()

        # Vérifier que create_engine a été appelé avec les bons paramètres
        mock_create_engine.assert_called_once()
        call_args = mock_create_engine.call_args

        # Vérifier les paramètres clés
        assert "sqlite:///" in call_args[0][0]  # URL SQLite
        assert call_args[1]["echo"] is False
        assert "poolclass" in call_args[1]
        assert "connect_args" in call_args[1]
        assert "pool_pre_ping" in call_args[1]
        assert "pool_recycle" in call_args[1]

        assert result == mock_engine

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.sessionmaker')
    def test_get_session_factory(self, mock_sessionmaker, mock_get_engine, mock_st):
        """Test de la création de la factory de sessions"""
        from app.database.database import get_session_factory

        # Mock de l'engine et de la sessionmaker
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine
        mock_factory = Mock()
        mock_sessionmaker.return_value = mock_factory

        result = get_session_factory()

        # Vérifier que sessionmaker a été appelé avec les bons paramètres
        mock_sessionmaker.assert_called_once_with(
            autocommit=False,
            autoflush=False,
            bind=mock_engine
        )

        assert result == mock_factory

    @patch('app.database.database.st')
    @patch('app.database.database.get_session_factory')
    def test_get_database_session(self, mock_get_factory, mock_st):
        """Test de l'obtention d'une session de base de données"""
        from app.database.database import get_database_session

        # Mock de la factory et de la session
        mock_factory = Mock()
        mock_get_factory.return_value = mock_factory
        mock_session = Mock()
        mock_factory.return_value = mock_session

        result = get_database_session()

        # Vérifier que la factory a été appelée
        mock_factory.assert_called_once()

        assert result == mock_session

    @patch('app.database.database.os.path.exists')
    @patch('app.database.database.get_database_engine')
    def test_get_database_info_exists(self, mock_get_engine, mock_exists):
        """Test de get_database_info quand la DB existe"""
        from app.database.database import get_database_info

        # Mock que la DB existe
        mock_exists.return_value = True

        # Mock de l'engine et de la session
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        with patch('app.database.database.get_database_session') as mock_get_session:
            mock_session = Mock()
            mock_get_session.return_value = mock_session

            # Mock des requêtes
            mock_result_consultants = Mock()
            mock_result_consultants.scalar.return_value = 150
            mock_result_missions = Mock()
            mock_result_missions.scalar.return_value = 75
            mock_result_practices = Mock()
            mock_result_practices.scalar.return_value = 8

            mock_session.execute.side_effect = [
                mock_result_consultants,
                mock_result_missions,
                mock_result_practices
            ]

            result = get_database_info()

            assert result["exists"] is True
            assert result["consultants_count"] == 150
            assert result["missions_count"] == 75
            assert result["practices_count"] == 8

    @patch('app.database.database.os.path.exists')
    def test_get_database_info_not_exists(self, mock_exists):
        """Test de get_database_info quand la DB n'existe pas"""
        from app.database.database import get_database_info

        # Mock que la DB n'existe pas
        mock_exists.return_value = False

        result = get_database_info()

        assert result["exists"] is False
        assert result["consultants_count"] == 0
        assert result["missions_count"] == 0
        assert result["practices_count"] == 0

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.Base')
    def test_init_database_success(self, mock_base, mock_get_engine, mock_st):
        """Test de l'initialisation réussie de la base de données"""
        from app.database.database import init_database

        # Mock de l'engine
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        # Mock de Base.metadata.create_all
        mock_base.metadata.create_all.return_value = None

        result = init_database()

        assert result is True
        mock_base.metadata.create_all.assert_called_once_with(bind=mock_engine)

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.Base')
    def test_init_database_error(self, mock_base, mock_get_engine, mock_st):
        """Test de l'initialisation avec erreur"""
        from app.database.database import init_database

        # Mock de l'engine
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        # Mock d'une exception lors de create_all
        mock_base.metadata.create_all.side_effect = Exception("Erreur DB")

        result = init_database()

        assert result is False

    @patch('app.database.database.os.path.exists')
    @patch('app.database.database.os.remove')
    @patch('app.database.database.init_database')
    def test_reset_database(self, mock_init_db, mock_remove, mock_exists):
        """Test de la remise à zéro de la base de données"""
        from app.database.database import reset_database

        # Mock que la DB existe
        mock_exists.return_value = True
        mock_init_db.return_value = True

        result = reset_database()

        assert result is True
        mock_remove.assert_called_once()
        mock_init_db.assert_called_once()

    @patch('app.database.database.os.path.exists')
    @patch('app.database.database.init_database')
    def test_reset_database_not_exists(self, mock_init_db, mock_exists):
        """Test de reset quand la DB n'existe pas"""
        from app.database.database import reset_database

        # Mock que la DB n'existe pas
        mock_exists.return_value = False
        mock_init_db.return_value = True

        result = reset_database()

        assert result is True
        mock_init_db.assert_called_once()


class TestDatabaseConstants:
    """Tests pour les constantes de base de données"""

    def test_database_path(self):
        """Test que le chemin de la base de données est correct"""
        from app.database.database import DATABASE_PATH

        # Vérifier que le chemin contient les bonnes parties
        assert "data" in DATABASE_PATH
        assert "consultator.db" in DATABASE_PATH

    def test_database_url(self):
        """Test que l'URL de la base de données est correcte"""
        from app.database.database import DATABASE_URL

        assert DATABASE_URL.startswith("sqlite:///")
        assert "consultator.db" in DATABASE_URL
