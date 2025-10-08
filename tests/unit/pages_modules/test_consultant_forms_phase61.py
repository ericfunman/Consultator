"""
Tests Phase 61: consultant_forms.py - Coverage 65.7% → 90%+
Objectif: Tester les fonctions de validation, création, modification, suppression
Cible: 81 lignes manquantes → ~25 tests
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import pytest

# Import du module à tester
from app.pages_modules import consultant_forms


class TestValidateConsultantForm(unittest.TestCase):
    """Tests pour validate_consultant_form()"""

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_all_fields_valid(self, mock_st):
        """Test validation avec tous les champs valides"""
        result = consultant_forms.validate_consultant_form(
            prenom="Jean",
            nom="Dupont",
            email="jean.dupont@test.com",
            practice_id=1
        )
        
        assert result is True
        mock_st.error.assert_not_called()

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_prenom_empty(self, mock_st):
        """Test validation avec prénom vide"""
        result = consultant_forms.validate_consultant_form(
            prenom="",
            nom="Dupont",
            email="jean@test.com",
            practice_id=1
        )
        
        assert result is False
        mock_st.error.assert_called()

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_prenom_whitespace_only(self, mock_st):
        """Test validation avec prénom contenant seulement des espaces"""
        result = consultant_forms.validate_consultant_form(
            prenom="   ",
            nom="Dupont",
            email="jean@test.com",
            practice_id=1
        )
        
        assert result is False

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_nom_empty(self, mock_st):
        """Test validation avec nom vide"""
        result = consultant_forms.validate_consultant_form(
            prenom="Jean",
            nom="",
            email="jean@test.com",
            practice_id=1
        )
        
        assert result is False

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_email_empty(self, mock_st):
        """Test validation avec email vide"""
        result = consultant_forms.validate_consultant_form(
            prenom="Jean",
            nom="Dupont",
            email="",
            practice_id=1
        )
        
        assert result is False

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_email_invalid_no_at(self, mock_st):
        """Test validation avec email sans @"""
        result = consultant_forms.validate_consultant_form(
            prenom="Jean",
            nom="Dupont",
            email="jeandupont.com",
            practice_id=1
        )
        
        assert result is False
        # Vérifier qu'au moins 2 erreurs sont affichées (email obligatoire + format)
        assert mock_st.error.call_count >= 1

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_practice_id_none(self, mock_st):
        """Test validation avec practice_id None"""
        result = consultant_forms.validate_consultant_form(
            prenom="Jean",
            nom="Dupont",
            email="jean@test.com",
            practice_id=None
        )
        
        assert result is False

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_practice_id_zero(self, mock_st):
        """Test validation avec practice_id = 0 (falsy)"""
        result = consultant_forms.validate_consultant_form(
            prenom="Jean",
            nom="Dupont",
            email="jean@test.com",
            practice_id=0
        )
        
        assert result is False

    @patch('app.pages_modules.consultant_forms.st')
    def test_validate_form_multiple_errors(self, mock_st):
        """Test validation avec plusieurs erreurs"""
        result = consultant_forms.validate_consultant_form(
            prenom="",
            nom="",
            email="invalidemail",
            practice_id=None
        )
        
        assert result is False
        # Devrait avoir plusieurs appels à st.error
        assert mock_st.error.call_count >= 3


class TestCreateConsultant(unittest.TestCase):
    """Tests pour create_consultant()"""

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_create_consultant_success(self, mock_session_func, mock_st):
        """Test création consultant réussie"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        # Mock query pour vérifier email unique
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None  # Pas de doublon
        mock_session.query.return_value = mock_query
        
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0601020304",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes"
        }
        
        # Execute
        result = consultant_forms.create_consultant(data)
        
        # Assert
        assert result is True
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_st.info.assert_called_once()

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_create_consultant_email_already_exists(self, mock_session_func, mock_st):
        """Test création consultant avec email déjà existant"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        # Mock consultant existant
        existing_consultant = Mock()
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = existing_consultant
        mock_session.query.return_value = mock_query
        
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "existing@test.com",
            "telephone": "",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": ""
        }
        
        # Execute
        result = consultant_forms.create_consultant(data)
        
        # Assert
        assert result is False
        mock_session.add.assert_not_called()
        mock_st.error.assert_called_with("❌ Un consultant avec cet email existe déjà")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_create_consultant_with_none_values(self, mock_session_func, mock_st):
        """Test création consultant avec valeurs None (telephone, notes)"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        data = {
            "prenom": "Marie",
            "nom": "Martin",
            "email": "marie@test.com",
            "telephone": None,
            "salaire_actuel": 0,
            "practice_id": 2,
            "disponibilite": False,
            "notes": None
        }
        
        # Execute
        result = consultant_forms.create_consultant(data)
        
        # Assert
        assert result is True
        mock_session.add.assert_called_once()

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_create_consultant_database_error(self, mock_session_func, mock_st):
        """Test création consultant avec erreur de base de données"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        mock_session.query.side_effect = Exception("Database error")
        
        data = {
            "prenom": "Test",
            "nom": "User",
            "email": "test@test.com",
            "telephone": "",
            "salaire_actuel": 0,
            "practice_id": 1,
            "disponibilite": True,
            "notes": ""
        }
        
        # Execute
        result = consultant_forms.create_consultant(data)
        
        # Assert
        assert result is False
        mock_st.error.assert_called()


class TestUpdateConsultant(unittest.TestCase):
    """Tests pour update_consultant()"""

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_update_consultant_success(self, mock_session_func, mock_st):
        """Test modification consultant réussie"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        # Mock consultant existant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        # Premier query: récupère le consultant
        mock_query1 = MagicMock()
        mock_query1.filter.return_value.first.return_value = mock_consultant
        
        # Deuxième query: vérifie email unique
        mock_query2 = MagicMock()
        mock_query2.filter.return_value.first.return_value = None
        
        mock_session.query.side_effect = [mock_query1, mock_query2]
        
        data = {
            "prenom": "Jean-Updated",
            "nom": "Dupont-Updated",
            "email": "jean.updated@test.com",
            "telephone": "0612345678",
            "salaire_actuel": 60000,
            "practice_id": 2,
            "disponibilite": False,
            "notes": "Updated notes"
        }
        
        # Execute
        result = consultant_forms.update_consultant(1, data)
        
        # Assert
        assert result is True
        assert mock_consultant.prenom == "Jean-Updated"
        assert mock_consultant.nom == "Dupont-Updated"
        mock_session.commit.assert_called_once()

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_update_consultant_not_found(self, mock_session_func, mock_st):
        """Test modification consultant inexistant"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        data = {"prenom": "Test", "nom": "Test", "email": "test@test.com", 
                "telephone": "", "salaire_actuel": 0, "practice_id": 1,
                "disponibilite": True, "notes": ""}
        
        # Execute
        result = consultant_forms.update_consultant(999, data)
        
        # Assert
        assert result is False
        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_update_consultant_email_conflict(self, mock_session_func, mock_st):
        """Test modification avec email déjà utilisé par un autre consultant"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        # Consultant à modifier (ID 1)
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        # Autre consultant avec le même email (ID 2)
        mock_existing = Mock()
        mock_existing.id = 2
        
        mock_query1 = MagicMock()
        mock_query1.filter.return_value.first.return_value = mock_consultant
        
        mock_query2 = MagicMock()
        mock_query2.filter.return_value.first.return_value = mock_existing
        
        mock_session.query.side_effect = [mock_query1, mock_query2]
        
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "already.used@test.com",
            "telephone": "",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": ""
        }
        
        # Execute
        result = consultant_forms.update_consultant(1, data)
        
        # Assert
        assert result is False
        mock_st.error.assert_called_with("❌ Un autre consultant utilise déjà cet email")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_update_consultant_database_error(self, mock_session_func, mock_st):
        """Test modification avec erreur de base de données"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        mock_session.query.side_effect = Exception("DB Error")
        
        data = {"prenom": "Test", "nom": "Test", "email": "test@test.com",
                "telephone": "", "salaire_actuel": 0, "practice_id": 1,
                "disponibilite": True, "notes": ""}
        
        # Execute
        result = consultant_forms.update_consultant(1, data)
        
        # Assert
        assert result is False


class TestDeleteConsultant(unittest.TestCase):
    """Tests pour delete_consultant()"""

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_delete_consultant_success(self, mock_session_func, mock_st):
        """Test suppression consultant réussie"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = mock_consultant
        mock_session.query.return_value = mock_query
        
        # Execute
        result = consultant_forms.delete_consultant(1)
        
        # Assert
        assert result is True
        mock_session.delete.assert_called_once_with(mock_consultant)
        mock_session.commit.assert_called_once()
        mock_st.info.assert_called_with("✅ Consultant supprimé de la base de données")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_delete_consultant_not_found(self, mock_session_func, mock_st):
        """Test suppression consultant inexistant"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        
        # Execute
        result = consultant_forms.delete_consultant(999)
        
        # Assert
        assert result is False
        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_delete_consultant_database_error(self, mock_session_func, mock_st):
        """Test suppression avec erreur de base de données"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        mock_session.query.side_effect = Exception("DB Error")
        
        # Execute
        result = consultant_forms.delete_consultant(1)
        
        # Assert
        assert result is False
        mock_st.error.assert_called()


class TestValidateFormData(unittest.TestCase):
    """Tests pour validate_form_data() - nouvelle fonction"""

    def test_validate_form_data_all_valid(self):
        """Test validation avec toutes les données valides"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@example.com",
            "practice_id": 1
        }
        
        result = consultant_forms.validate_form_data(data)
        assert result is True

    def test_validate_form_data_missing_required_field(self):
        """Test validation avec champ requis manquant"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            # email manquant
            "practice_id": 1
        }
        
        result = consultant_forms.validate_form_data(data)
        assert result is False

    def test_validate_form_data_empty_required_field(self):
        """Test validation avec champ requis vide"""
        data = {
            "prenom": "",
            "nom": "Dupont",
            "email": "test@test.com",
            "practice_id": 1
        }
        
        result = consultant_forms.validate_form_data(data)
        assert result is False

    def test_validate_form_data_invalid_email_format(self):
        """Test validation avec format email invalide"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "not-an-email",
            "practice_id": 1
        }
        
        result = consultant_forms.validate_form_data(data)
        assert result is False

    def test_validate_form_data_email_without_domain(self):
        """Test validation email sans domaine"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "test@",
            "practice_id": 1
        }
        
        result = consultant_forms.validate_form_data(data)
        assert result is False

    def test_validate_form_data_valid_complex_email(self):
        """Test validation email complexe valide"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont+test@sub.example.co.uk",
            "practice_id": 1
        }
        
        result = consultant_forms.validate_form_data(data)
        assert result is True


class TestHelperFunctions(unittest.TestCase):
    """Tests pour les fonctions helper privées"""

    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_load_practices(self, mock_session_func):
        """Test _load_practices()"""
        # Setup
        mock_session = MagicMock()
        mock_session_func.return_value.__enter__.return_value = mock_session
        
        mock_practice1 = Mock()
        mock_practice1.id = 1
        mock_practice1.nom = "Practice Data"
        
        mock_practice2 = Mock()
        mock_practice2.id = 2
        mock_practice2.nom = "Practice Cloud"
        
        mock_query = MagicMock()
        mock_query.all.return_value = [mock_practice1, mock_practice2]
        mock_session.query.return_value = mock_query
        
        # Execute
        result = consultant_forms._load_practices()
        
        # Assert
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result[1] == "Practice Data"
        assert result[2] == "Practice Cloud"


class TestConstantsAndAliases(unittest.TestCase):
    """Tests pour les constantes et alias"""

    def test_error_constant_defined(self):
        """Test que la constante ERROR_CONSULTANT_NOT_FOUND est définie"""
        assert hasattr(consultant_forms, 'ERROR_CONSULTANT_NOT_FOUND')
        assert consultant_forms.ERROR_CONSULTANT_NOT_FOUND == "❌ Consultant introuvable"

    def test_imports_ok_variable_exists(self):
        """Test que la variable imports_ok existe"""
        assert hasattr(consultant_forms, 'imports_ok')
        # Dans les tests, imports_ok devrait être True
        assert consultant_forms.imports_ok is True


if __name__ == "__main__":
    unittest.main()
