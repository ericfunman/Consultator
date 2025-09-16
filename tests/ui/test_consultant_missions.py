"""Tests pour le module consultant_missions - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime
import streamlit as st
from app.pages_modules.consultant_missions import (
    show_consultant_missions,
    show_mission_details,
    show_missions_statistics,
    show_add_mission_form,
    validate_mission_form,
    create_mission,
    show_edit_mission_form,
    update_mission,
    delete_mission,
    show_mission_full_details,
    show_missions_analysis,
    show_missions_revenues
)
from tests.fixtures.base_test import BaseUITest


class TestConsultantMissions(BaseUITest):
    """Tests pour le module de missions consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_missions)

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_basic(self, mock_service):
        """Test d'affichage basique des missions"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', False)
    def test_show_consultant_missions_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_missions_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_missions(None)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_with_data(self, mock_service):
        """Test d'affichage avec données de missions"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock missions
        mock_missions = [
            {
                'id': 1,
                'nom': 'Projet Web E-commerce',
                'client_nom': 'Client A',
                'date_debut': '2023-01-01',
                'date_fin': '2023-06-30',
                'statut': 'Terminée',
                'description': 'Développement d\'une plateforme e-commerce',
                'technologies': ['Python', 'Django', 'React'],
                'tarif_journalier': 550.0,
                'duree_jours': 120
            },
            {
                'id': 2,
                'nom': 'API REST Microservices',
                'client_nom': 'Client B',
                'date_debut': '2023-07-01',
                'date_fin': None,
                'statut': 'En cours',
                'description': 'Développement d\'API REST',
                'technologies': ['Python', 'FastAPI', 'Docker'],
                'tarif_journalier': 600.0,
                'duree_jours': None
            }
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_missions.return_value = mock_missions
        mock_service_instance.get_consultant_missions_stats.return_value = {
            'total_missions': 2,
            'missions_actives': 1,
            'missions_terminees': 1,
            'total_jours': 120,
            'ca_total': 66000.0
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_empty(self, mock_service):
        """Test d'affichage avec missions vides"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_missions.return_value = []
        mock_service_instance.get_consultant_missions_stats.return_value = {
            'total_missions': 0,
            'missions_actives': 0,
            'missions_terminees': 0,
            'total_jours': 0,
            'ca_total': 0.0
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_missions.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_missions as missions_module

        # Vérifier que les fonctions principales existent
        assert hasattr(missions_module, 'show_consultant_missions')

        # Vérifier que les variables d'import existent
        assert hasattr(missions_module, 'imports_ok')
        assert hasattr(missions_module, 'ConsultantService')

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_missions)

        # Vérifier le nombre de paramètres
        sig_missions = inspect.signature(show_consultant_missions)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_missions.parameters) >= 1

    def test_validate_mission_form_valid_data(self):
        """Test validation avec données valides"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=1,
            date_debut=date(2024, 1, 1),
            en_cours=False,
            date_fin=date(2024, 6, 30)
        )

        assert result is True

    def test_validate_mission_form_missing_title(self):
        """Test validation avec titre manquant"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="",
            client_id=1,
            date_debut=date(2024, 1, 1),
            en_cours=True,
            date_fin=None
        )

        assert result is False

    def test_validate_mission_form_invalid_dates(self):
        """Test validation avec dates invalides"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=1,
            date_debut=date(2024, 6, 30),
            en_cours=False,
            date_fin=date(2024, 1, 1)  # Date fin avant date début
        )

        assert result is False

    @patch('app.pages_modules.consultant_missions.st')
    @patch('app.pages_modules.consultant_missions.get_database_session')
    @patch('app.pages_modules.consultant_missions.Mission')
    def test_create_mission_success(self, mock_mission_class, mock_session, mock_st):
        """Test création de mission réussie"""
        from app.pages_modules.consultant_missions import create_mission

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock mission
        mock_mission = MagicMock()
        mock_mission_class.return_value = mock_mission

        # Test data
        data = {
            "titre": "Test Mission",
            "client_id": 1,
            "date_debut": date(2024, 1, 1),
            "date_fin": date(2024, 6, 30),
            "en_cours": False,
            "taux_journalier": 500,
            "tjm": 550,
            "salaire_mensuel": 0,
            "description": "Test description",
            "competences_requises": "Python, SQL"
        }

        result = create_mission(1, data)

        assert result is True
        mock_session_instance.add.assert_called_once_with(mock_mission)
        mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_missions.get_database_session')
    def test_create_mission_database_error(self, mock_session):
        """Test création de mission avec erreur DB"""
        from app.pages_modules.consultant_missions import create_mission

        # Mock session qui lève une exception
        mock_session_instance = MagicMock()
        mock_session_instance.commit.side_effect = Exception("DB Error")
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {
            "titre": "Test Mission",
            "client_id": 1,
            "date_debut": date(2024, 1, 1),
            "date_fin": None,
            "en_cours": True,
            "taux_journalier": 500,
            "tjm": 0,
            "salaire_mensuel": 0,
            "description": "",
            "competences_requises": ""
        }

        result = create_mission(1, data)

        assert result is False

    @patch('app.pages_modules.consultant_missions.st')
    @patch('app.pages_modules.consultant_missions.get_database_session')
    @patch('app.pages_modules.consultant_missions.Mission')
    def test_delete_mission_success(self, mock_mission_class, mock_session, mock_st):
        """Test suppression de mission réussie"""
        from app.pages_modules.consultant_missions import delete_mission

        # Mock session et mission
        mock_session_instance = MagicMock()
        mock_mission = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_mission
        mock_session.return_value.__enter__.return_value = mock_session_instance

        result = delete_mission(1)

        assert result is True
        mock_session_instance.delete.assert_called_once_with(mock_mission)
        mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_missions.get_database_session')
    def test_delete_mission_not_found(self, mock_session):
        """Test suppression de mission inexistante"""
        from app.pages_modules.consultant_missions import delete_mission

        # Mock session qui ne trouve pas la mission
        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None
        mock_session.return_value.__enter__.return_value = mock_session_instance

        result = delete_mission(999)

        assert result is False

    @patch('app.pages_modules.consultant_missions.st')
    def test_show_missions_statistics_with_data(self, mock_st):
        """Test affichage des statistiques avec données"""
        from app.pages_modules.consultant_missions import show_missions_statistics

        # Mock missions
        mock_missions = []
        for i in range(3):
            mission = MagicMock()
            mission.en_cours = i < 2  # 2 en cours, 1 terminée
            mission.taux_journalier = 500
            if i < 2:  # Missions en cours
                mission.date_fin = None
                mission.date_debut = date(2024, 1, 1)
            else:  # Mission terminée
                mission.date_debut = date(2024, 1, 1)
                mission.date_fin = date(2024, 6, 30)
            mock_missions.append(mission)

        # Mock streamlit columns
        mock_col = MagicMock()
        mock_st.columns.return_value = [mock_col, mock_col, mock_col, mock_col]

        show_missions_statistics(mock_missions)

        # Vérifier que metric a été appelé
        assert mock_st.metric.call_count >= 4  # Au moins 4 métriques

    @patch('app.pages_modules.consultant_missions.st')
    def test_show_missions_statistics_empty(self, mock_st):
        """Test affichage des statistiques sans données"""
        from app.pages_modules.consultant_missions import show_missions_statistics

        show_missions_statistics([])

        # Vérifier qu'aucune métrique n'est affichée
        mock_st.metric.assert_not_called()

    @patch('app.pages_modules.consultant_missions.st')
    @patch('app.pages_modules.consultant_missions.get_database_session')
    def test_show_add_mission_form_success(self, mock_session, mock_st):
        """Test formulaire d'ajout avec succès"""
        from app.pages_modules.consultant_missions import show_add_mission_form

        # Mock clients
        mock_client = MagicMock()
        mock_client.id = 1
        mock_client.nom = "Test Client"

        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.all.return_value = [mock_client]
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock form elements
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.text_input.return_value = "Test Mission"
        mock_st.selectbox.return_value = 1
        mock_st.date_input.return_value = date(2024, 1, 1)
        mock_st.checkbox.return_value = False
        mock_st.number_input.return_value = 500
        mock_st.text_area.return_value = "Description"
        mock_st.form_submit_button.return_value = True

        # Mock create_mission
        with patch('app.pages_modules.consultant_missions.create_mission', return_value=True):
            show_add_mission_form(1)

    @patch('app.pages_modules.consultant_missions.st')
    def test_show_mission_details_with_client(self, mock_st):
        """Test affichage des détails de mission avec client"""
        from app.pages_modules.consultant_missions import show_mission_full_details

        # Mock mission avec client
        mock_mission = MagicMock()
        mock_mission.id = 1
        mock_mission.titre = "Test Mission"
        mock_mission.date_debut = date(2024, 1, 1)
        mock_mission.date_fin = date(2024, 6, 30)
        mock_mission.en_cours = False
        mock_mission.taux_journalier = 500
        mock_mission.tjm = 550
        mock_mission.salaire_mensuel = None
        mock_mission.description = "Test description"
        mock_mission.competences_requises = "Python, SQL"

        mock_client = MagicMock()
        mock_client.nom = "Test Client"
        mock_client.secteur = "Tech"
        mock_mission.client = mock_client

        # Mock streamlit elements - 2 columns pour les détails
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.button.return_value = False

        show_mission_full_details(mock_mission)

        # Vérifier que les informations sont affichées
        mock_st.write.assert_called()

    @patch('app.pages_modules.consultant_missions.st')
    @patch('app.pages_modules.consultant_missions.date')
    def test_show_missions_analysis_with_data(self, mock_date_class, mock_st):
        """Test analyse des missions avec données"""
        from app.pages_modules.consultant_missions import show_missions_analysis

        # Mock date.today()
        mock_today = MagicMock()
        mock_today.today.return_value = date(2024, 12, 31)
        mock_date_class.today = mock_today.today
        mock_date_class.side_effect = lambda *args, **kwargs: date(*args, **kwargs) if args else mock_today

        # Mock missions
        mock_missions = []
        for i in range(2):
            mission = MagicMock()
            mission.client.nom = f"Client {i+1}"
            mission.en_cours = i == 0
            mission.date_debut = date(2024, 1, 1)
            mission.date_fin = date(2024, 6, 30) if not mission.en_cours else None
            mission.taux_journalier = 500
            mock_missions.append(mission)

        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        show_missions_analysis(mock_missions)

        # Vérifier que l'analyse est affichée
        mock_st.write.assert_called()

    @patch('app.pages_modules.consultant_missions.st')
    @patch('pandas.DataFrame')
    def test_show_missions_revenues_with_data(self, mock_dataframe, mock_st):
        """Test analyse des revenus avec données"""
        from app.pages_modules.consultant_missions import show_missions_revenues

        # Mock pandas DataFrame
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        mock_df.sort_values.return_value = mock_df

        # Mock missions avec revenus
        mock_missions = []
        for i in range(2):
            mission = MagicMock()
            mission.titre = f"Mission {i+1}"
            mission.client.nom = f"Client {i+1}"
            mission.taux_journalier = 500
            mission.en_cours = i == 0
            mission.date_debut = date(2024, 1, 1)
            mission.date_fin = date(2024, 6, 30) if not mission.en_cours else None
            mock_missions.append(mission)

        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_missions_revenues(mock_missions)

        # Vérifier que pandas a été utilisé
        mock_dataframe.assert_called()
        mock_st.dataframe.assert_called()
