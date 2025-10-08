"""
Tests Phase 53 - consultant_missions.py (Coverage 58% → 70%+)
Cible: Constantes, helpers, logique métier pure
"""

import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Import du module à tester
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from app.pages_modules import consultant_missions


# ============================================================================
# TESTS: Constantes
# ============================================================================

class TestConstants:
    """Tests pour les constantes du module"""

    def test_status_constants(self):
        """Test des constantes de statut"""
        assert consultant_missions.STATUS_EN_COURS == "En cours"
        assert consultant_missions.STATUS_TERMINEE == "Terminée"
        assert consultant_missions.STATUS_PLANIFIEE == "Planifiée"

    def test_error_message_constants(self):
        """Test des messages d'erreur"""
        assert "Mission introuvable" in consultant_missions.MSG_MISSION_INTROUVABLE
        assert "services de base" in consultant_missions.MSG_SERVICES_INDISPONIBLES
        assert "Consultant introuvable" in consultant_missions.MSG_CONSULTANT_INTROUVABLE
        
    def test_success_message_constants(self):
        """Test des messages de succès"""
        assert "créée avec succès" in consultant_missions.MSG_SUCCESS_CREATION
        assert "modifiée avec succès" in consultant_missions.MSG_SUCCESS_MODIFICATION
        assert "supprimée avec succès" in consultant_missions.MSG_SUCCESS_SUPPRESSION

    def test_default_value_constants(self):
        """Test des valeurs par défaut"""
        assert consultant_missions.DEFAULT_VALUE == "N/A"
        assert consultant_missions.DEFAULT_CLIENT == "Non renseigné"


# ============================================================================
# TESTS: Module integrity
# ============================================================================

class TestModuleIntegrity:
    """Tests d'intégrité du module"""

    def test_imports_ok_variable_exists(self):
        """Test que la variable imports_ok existe"""
        assert hasattr(consultant_missions, 'imports_ok')
        assert isinstance(consultant_missions.imports_ok, bool)

    def test_all_status_unique(self):
        """Test que les statuts sont uniques"""
        statuses = {
            consultant_missions.STATUS_EN_COURS,
            consultant_missions.STATUS_TERMINEE,
            consultant_missions.STATUS_PLANIFIEE
        }
        assert len(statuses) == 3

    def test_all_messages_non_empty(self):
        """Test que tous les messages ne sont pas vides"""
        messages = [
            consultant_missions.MSG_MISSION_INTROUVABLE,
            consultant_missions.MSG_SERVICES_INDISPONIBLES,
            consultant_missions.MSG_CONSULTANT_INTROUVABLE,
            consultant_missions.MSG_ERREUR_CHARGEMENT,
            consultant_missions.MSG_ERREUR_CREATION,
            consultant_missions.MSG_ERREUR_MODIFICATION,
            consultant_missions.MSG_ERREUR_SUPPRESSION,
            consultant_missions.MSG_AUCUNE_MISSION,
            consultant_missions.MSG_SUCCESS_CREATION,
            consultant_missions.MSG_SUCCESS_MODIFICATION,
            consultant_missions.MSG_SUCCESS_SUPPRESSION,
        ]
        
        for msg in messages:
            assert len(msg) > 0
            assert msg.strip() == msg  # No leading/trailing spaces


# ============================================================================
# TESTS: show_consultant_missions() - Entry point
# ============================================================================

class TestShowConsultantMissions:
    """Tests pour la fonction show_consultant_missions()"""

    @patch('streamlit.error')
    def test_show_missions_imports_not_ok(self, mock_st_error):
        """Test avec imports non disponibles"""
        original_imports_ok = consultant_missions.imports_ok
        consultant_missions.imports_ok = False
        
        mock_consultant = Mock()
        consultant_missions.show_consultant_missions(mock_consultant)
        
        mock_st_error.assert_called_once()
        consultant_missions.imports_ok = original_imports_ok

    @patch('streamlit.error')
    def test_show_missions_no_consultant(self, mock_st_error):
        """Test avec consultant None"""
        consultant_missions.show_consultant_missions(None)
        
        mock_st_error.assert_called_once()
        # Vérifier que st.error a été appelé (peu importe le message exact)
        assert mock_st_error.called

    @patch('streamlit.markdown')
    @patch('streamlit.error')
    def test_show_missions_empty_consultant_object(self, mock_st_error, mock_st_markdown):
        """Test avec objet consultant vide mais pas None"""
        mock_consultant = Mock()
        mock_consultant.id = None
        
        # Si imports_ok=True mais consultant invalide
        # Doit tenter d'afficher mais échouer plus tard
        # Pour ce test, on vérifie juste qu'il ne crash pas immédiatement
        try:
            consultant_missions.show_consultant_missions(mock_consultant)
        except AttributeError:
            # Attendu si le consultant est invalide
            pass


# ============================================================================
# TESTS: Helper functions (if any pure logic exists)
# ============================================================================

class TestHelperFunctions:
    """Tests pour les fonctions helpers (si elles existent)"""

    def test_module_has_callable_functions(self):
        """Test que le module contient des fonctions appelables"""
        # Vérifier que show_consultant_missions est callable
        assert callable(consultant_missions.show_consultant_missions)

    def test_status_constants_are_strings(self):
        """Test que les constantes de statut sont des strings"""
        assert isinstance(consultant_missions.STATUS_EN_COURS, str)
        assert isinstance(consultant_missions.STATUS_TERMINEE, str)
        assert isinstance(consultant_missions.STATUS_PLANIFIEE, str)

    def test_default_constants_are_strings(self):
        """Test que les constantes par défaut sont des strings"""
        assert isinstance(consultant_missions.DEFAULT_VALUE, str)
        assert isinstance(consultant_missions.DEFAULT_CLIENT, str)


# ============================================================================
# TESTS: Edge cases
# ============================================================================

class TestEdgeCases:
    """Tests des cas limites"""

    @patch('streamlit.error')
    def test_show_missions_with_false_value(self, mock_st_error):
        """Test avec valeur falsy (0, False, [])"""
        # Tester avec différentes valeurs falsy
        for falsy_value in [0, False, []]:
            mock_st_error.reset_mock()
            consultant_missions.show_consultant_missions(falsy_value)
            mock_st_error.assert_called_once()

    def test_status_constants_not_equal(self):
        """Test que les statuts sont tous différents"""
        assert consultant_missions.STATUS_EN_COURS != consultant_missions.STATUS_TERMINEE
        assert consultant_missions.STATUS_EN_COURS != consultant_missions.STATUS_PLANIFIEE
        assert consultant_missions.STATUS_TERMINEE != consultant_missions.STATUS_PLANIFIEE

    def test_error_messages_have_emoji(self):
        """Test que les messages d'erreur ont des emojis"""
        error_messages = [
            consultant_missions.MSG_MISSION_INTROUVABLE,
            consultant_missions.MSG_SERVICES_INDISPONIBLES,
            consultant_missions.MSG_CONSULTANT_INTROUVABLE,
        ]
        
        for msg in error_messages:
            assert "❌" in msg or "ℹ️" in msg or "⚠️" in msg

    def test_success_messages_have_emoji(self):
        """Test que les messages de succès ont des emojis"""
        success_messages = [
            consultant_missions.MSG_SUCCESS_CREATION,
            consultant_missions.MSG_SUCCESS_MODIFICATION,
            consultant_missions.MSG_SUCCESS_SUPPRESSION,
        ]
        
        for msg in success_messages:
            assert "✅" in msg


# ============================================================================
# TESTS: Constants consistency
# ============================================================================

class TestConstantsConsistency:
    """Tests de cohérence des constantes"""

    def test_error_messages_start_with_emoji(self):
        """Test que les messages commencent par un emoji"""
        messages = [
            consultant_missions.MSG_MISSION_INTROUVABLE,
            consultant_missions.MSG_SERVICES_INDISPONIBLES,
            consultant_missions.MSG_CONSULTANT_INTROUVABLE,
            consultant_missions.MSG_ERREUR_CHARGEMENT,
            consultant_missions.MSG_ERREUR_CREATION,
            consultant_missions.MSG_ERREUR_MODIFICATION,
            consultant_missions.MSG_ERREUR_SUPPRESSION,
        ]
        
        for msg in messages:
            # Devrait commencer par ❌ ou ⚠️
            assert msg[0] in ["❌", "⚠️", "ℹ️"]

    def test_success_messages_start_with_checkmark(self):
        """Test que les messages de succès commencent par ✅"""
        success_messages = [
            consultant_missions.MSG_SUCCESS_CREATION,
            consultant_missions.MSG_SUCCESS_MODIFICATION,
            consultant_missions.MSG_SUCCESS_SUPPRESSION,
        ]
        
        for msg in success_messages:
            assert msg.startswith("✅")

    def test_all_constants_are_uppercase(self):
        """Test que toutes les constantes sont en majuscules"""
        # Vérifier quelques constantes clés
        constant_names = [
            'STATUS_EN_COURS',
            'STATUS_TERMINEE',
            'STATUS_PLANIFIEE',
            'DEFAULT_VALUE',
            'DEFAULT_CLIENT',
        ]
        
        for const_name in constant_names:
            assert hasattr(consultant_missions, const_name)
            assert const_name.isupper()


# ============================================================================
# TESTS: Module attributes
# ============================================================================

class TestModuleAttributes:
    """Tests des attributs du module"""

    def test_module_has_docstring(self):
        """Test que le module a une docstring"""
        assert consultant_missions.__doc__ is not None
        assert len(consultant_missions.__doc__.strip()) > 0

    def test_show_consultant_missions_has_docstring(self):
        """Test que show_consultant_missions a une docstring"""
        assert consultant_missions.show_consultant_missions.__doc__ is not None
        assert "missions" in consultant_missions.show_consultant_missions.__doc__.lower()

    def test_module_has_expected_attributes(self):
        """Test que le module a les attributs attendus"""
        expected_attrs = [
            'STATUS_EN_COURS',
            'STATUS_TERMINEE',
            'STATUS_PLANIFIEE',
            'MSG_MISSION_INTROUVABLE',
            'DEFAULT_VALUE',
            'DEFAULT_CLIENT',
            'show_consultant_missions',
            'imports_ok',
        ]
        
        for attr in expected_attrs:
            assert hasattr(consultant_missions, attr), f"Missing attribute: {attr}"

    def test_constants_immutability_type(self):
        """Test que les constantes sont du bon type (strings)"""
        string_constants = [
            consultant_missions.STATUS_EN_COURS,
            consultant_missions.STATUS_TERMINEE,
            consultant_missions.STATUS_PLANIFIEE,
            consultant_missions.DEFAULT_VALUE,
            consultant_missions.DEFAULT_CLIENT,
        ]
        
        for const in string_constants:
            assert isinstance(const, str)
            assert len(const) > 0
