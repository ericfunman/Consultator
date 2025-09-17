"""
Tests pour le module database
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

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

        # Clear le cache Streamlit pour ce test
        if hasattr(get_database_engine, 'clear'):
            get_database_engine.clear()

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

        # Clear le cache Streamlit pour ce test
        if hasattr(get_session_factory, 'clear'):
            get_session_factory.clear()

        result = get_session_factory()

        # Vérifier que sessionmaker a été appelé avec les bons paramètres
        mock_sessionmaker.assert_called_once_with(
            autocommit=False,
            autoflush=False,
            bind=mock_engine
        )

        assert result == mock_factory

    def test_get_database_session(self):
        """Test de l'obtention d'une session de base de données"""
        from app.database.database import get_database_session

        # Test que la fonction s'exécute sans erreur
        result = get_database_session()

        # Vérifier que la fonction retourne quelque chose
        assert result is not None

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
            # Configurer le mock session pour supporter le context manager
            mock_session.__enter__ = Mock(return_value=mock_session)
            mock_session.__exit__ = Mock(return_value=None)

            # Mock des requêtes dans l'ordre réel : Consultant, Competence, Mission, Practice
            mock_session.query.return_value.count.side_effect = [150, 8, 75, 10]

            # Clear le cache pour ce test
            if hasattr(get_database_info, 'clear'):
                get_database_info.clear()

            result = get_database_info()

            assert result["exists"] is True
            assert result["consultants"] == 150
            assert result["missions"] == 75
            assert result["competences"] == 8
            assert result["practices"] == 10

    @patch('app.database.database.os.path.exists')
    def test_get_database_info_not_exists(self, mock_exists):
        """Test de get_database_info quand la DB n'existe pas"""
        from app.database.database import get_database_info

        # Mock que la DB n'existe pas
        mock_exists.return_value = False

        # Clear le cache pour ce test
        if hasattr(get_database_info, 'clear'):
            get_database_info.clear()

        result = get_database_info()

        assert result["exists"] is False
        # Les autres clés ne sont pas présentes quand la DB n'existe pas
        assert "consultants" not in result
        assert "missions" not in result
        assert "practices" not in result

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.Base')
    @patch('app.database.database.is_database_initialized')
    def test_init_database_success(self, mock_is_initialized, mock_base, mock_get_engine, mock_st):
        """Test de l'initialisation réussie de la base de données"""
        from app.database.database import init_database

        # Mock que la DB n'est pas encore initialisée
        mock_is_initialized.return_value = False

        # Mock de l'engine
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        # Mock de Base.metadata.create_all
        mock_base.metadata.create_all.return_value = None

        # Reset le flag global pour ce test
        import app.database.database as db_module
        db_module._database_initialized = False

        result = init_database()

        assert result is True
        mock_base.metadata.create_all.assert_called_once_with(bind=mock_engine)

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.Base')
    @patch('app.database.database.is_database_initialized')
    def test_init_database_error(self, mock_is_initialized, mock_base, mock_get_engine, mock_st):
        """Test de l'initialisation avec erreur"""
        from app.database.database import init_database

        # Mock que la DB n'est pas encore initialisée
        mock_is_initialized.return_value = False

        # Mock de l'engine
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        # Mock d'une exception lors de create_all
        mock_base.metadata.create_all.side_effect = Exception("Erreur DB")

        # Reset le flag global pour ce test
        import app.database.database as db_module
        db_module._database_initialized = False

        result = init_database()

        assert result is False

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.Base')
    def test_reset_database(self, mock_base, mock_get_engine, mock_st):
        """Test de la remise à zéro de la base de données"""
        from app.database.database import reset_database

        # Mock de l'engine
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        result = reset_database()

        assert result is True
        # Vérifier que drop_all et create_all ont été appelés
        mock_base.metadata.drop_all.assert_called_once_with(bind=mock_engine)
        mock_base.metadata.create_all.assert_called_once_with(bind=mock_engine)

    @patch('app.database.database.st')
    @patch('app.database.database.get_database_engine')
    @patch('app.database.database.Base')
    def test_reset_database_not_exists(self, mock_base, mock_get_engine, mock_st):
        """Test de reset quand la DB n'existe pas"""
        from app.database.database import reset_database

        # Mock de l'engine
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine

        result = reset_database()

        assert result is True
        # Même si la DB n'existe pas, drop_all et create_all sont quand même appelés
        mock_base.metadata.drop_all.assert_called_once_with(bind=mock_engine)
        mock_base.metadata.create_all.assert_called_once_with(bind=mock_engine)


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
