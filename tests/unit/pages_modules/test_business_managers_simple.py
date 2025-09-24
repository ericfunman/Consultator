"""
Tests de couverture pour business_managers.py
Visant à améliorer la couverture de 69.3% vers 80%+
"""

from unittest.mock import MagicMock, patch, mock          show_business_managers_list()

        # Vérifier que le message d'information est affiché
        mock_st.info.assert_called_once()
        # Le message contient le terme de recherche (qui est un mock)
        call_args = mock_st.info.call_args[0][0]
        assert "0 Business Manager(s) trouvé(s) pour" in call_args  # Vérifier que le message d'information est affiché
        mock_st.info.assert_called_once()
        # Le message contient le terme de recherche (qui est un mock)
        call_args = mock_st.info.call_args[0][0]
        assert "0 Business Manager(s) trouvé(s) pour" in call_argspen
import pytest
import json
from datetime import datetime, date
from pathlib import Path
import tempfile

from app.pages_modules.business_managers import (
    show, show_bm_profile, show_business_managers_list,
    show_add_business_manager, show_statistics,
    _validate_and_convert_bm_id
)

class TestBusinessManagersBasic:
    """Tests de base pour les fonctions principales de business_managers.py"""

    @patch('app.pages_modules.business_managers.st')
    def test_show_basic_navigation(self, mock_st):
        """Test de la fonction show() - navigation basique"""
        # Mock session_state pour éviter l'affichage du profil
        mock_st.session_state = MagicMock()
        mock_st.session_state.get.return_value = None

        # Mock st.columns pour retourner des mocks
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Mock st.tabs pour retourner 3 onglets
        mock_tab1, mock_tab2, mock_tab3 = MagicMock(), MagicMock(), MagicMock()
        mock_st.tabs.return_value = [mock_tab1, mock_tab2, mock_tab3]

        show()

        # Vérifier que le titre est affiché
        mock_st.title.assert_called_with("👔 Gestion des Business Managers")

        # Vérifier que les onglets sont créés
        mock_st.tabs.assert_called_once()
        args, kwargs = mock_st.tabs.call_args
        assert len(args[0]) == 3  # 3 onglets
        assert "📋 Liste des BMs" in args[0]
        assert "➕ Nouveau BM" in args[0]
        assert "📊 Statistiques" in args[0]

    @patch('app.pages_modules.business_managers.st')
    def test_show_with_profile_view(self, mock_st):
        """Test de show() avec affichage de profil"""
        mock_st.session_state = MagicMock()
        mock_st.session_state.get.return_value = 1

        with patch('app.pages_modules.business_managers.show_bm_profile') as mock_show_profile:
            # Mock st.tabs pour éviter les erreurs
            mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
            
            show()

            # Vérifier que show_bm_profile est appelée
            mock_show_profile.assert_called_once()
            # Vérifier que les onglets ne sont pas affichés
            mock_st.tabs.assert_not_called()

    def test_validate_and_convert_bm_id_valid(self):
        """Test de validation d'ID valide"""
        with patch('app.pages_modules.business_managers.st') as mock_st:
            result = _validate_and_convert_bm_id("123")
            assert result == 123
            mock_st.error.assert_not_called()

    def test_validate_and_convert_bm_id_invalid_string(self):
        """Test de validation d'ID invalide (string non numérique)"""
        with patch('app.pages_modules.business_managers.st') as mock_st:
            result = _validate_and_convert_bm_id("abc")
            assert result is None
            mock_st.error.assert_called_once()

    def test_validate_and_convert_bm_id_already_int(self):
        """Test de validation d'ID déjà entier"""
        with patch('app.pages_modules.business_managers.st') as mock_st:
            result = _validate_and_convert_bm_id(456)
            assert result == 456
            mock_st.error.assert_not_called()

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_bm_profile_not_found(self, mock_session, mock_st):
        """Test d'affichage de profil BM non trouvé"""
        # Mock session_state
        mock_st.session_state = MagicMock()
        mock_st.session_state.view_bm_profile = 999

        # Mock la session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query qui retourne None
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        show_bm_profile()

        # Vérifier que l'erreur est affichée
        mock_st.error.assert_called_with("❌ Business Manager introuvable")
        # Vérifier que session_state est nettoyé
        assert not hasattr(mock_st.session_state, 'view_bm_profile')

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.get_database_session')
    @patch('app.pages_modules.business_managers._display_bm_header_and_info')
    @patch('app.pages_modules.business_managers._display_bm_general_info')
    @patch('app.pages_modules.business_managers._handle_bm_form_actions')
    @patch('app.pages_modules.business_managers.show_bm_consultants_management')
    def test_show_bm_profile_success(self, mock_show_consultants, mock_handle_forms,
                                   mock_display_info, mock_display_header, mock_session, mock_st):
        """Test d'affichage réussi du profil BM"""
        # Mock session_state
        mock_st.session_state = MagicMock()
        mock_st.session_state.view_bm_profile = 1

        # Mock BM
        mock_bm = MagicMock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"

        # Mock la session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query qui retourne le BM
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_bm
        mock_session_instance.query.return_value = mock_query

        show_bm_profile()

        # Vérifier que les fonctions d'affichage sont appelées
        mock_display_header.assert_called_once_with(mock_bm)
        mock_display_info.assert_called_once()
        mock_handle_forms.assert_called_once_with(mock_bm)
        mock_show_consultants.assert_called_once()

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.BusinessManagerService')
    def test_show_business_managers_list_empty(self, mock_service, mock_st):
        """Test de la liste vide des BMs"""
        mock_service.get_all_business_managers.return_value = []

        # Mock st.columns pour éviter les erreurs
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        show_business_managers_list()

        # Vérifier que le message d'information est affiché
        mock_st.info.assert_called_with("� 0 Business Manager(s) trouvé(s) pour ''")

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.BusinessManagerService')
    @patch('app.pages_modules.business_managers._build_bm_data_table')
    @patch('app.pages_modules.business_managers._apply_bm_list_css')
    @patch('app.pages_modules.business_managers._display_bm_table_header')
    @patch('app.pages_modules.business_managers._display_bm_table_row')
    @patch('app.pages_modules.business_managers._display_bm_metrics')
    def test_show_business_managers_list_with_data(self, mock_display_metrics, mock_display_row,
                                                 mock_display_header, mock_apply_css,
                                                 mock_build_table, mock_service, mock_st):
        """Test de la liste des BMs avec données"""
        # Mock données du service
        mock_bm_data = [{
            "id": 1, "prenom": "Jean", "nom": "Dupont", "email": "jean@test.com",
            "telephone": "0123456789", "consultants_count": 5, "actif": True,
            "date_creation": datetime.now()
        }]

        mock_service.get_all_business_managers.return_value = mock_bm_data

        # Mock données du tableau
        mock_table_data = [{
            "ID": 1, "Prénom": "Jean", "Nom": "Dupont", "Email": "jean@test.com",
            "Téléphone": "0123456789", "Consultants actuels": 5, "Total assignations": 10,
            "Statut": "🟢 Actif", "Créé le": "01/01/2024"
        }]

        mock_build_table.return_value = mock_table_data

        # Mock st.columns
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        show_business_managers_list()

        # Vérifier que les fonctions sont appelées
        mock_apply_css.assert_called_once()
        mock_display_header.assert_called_once()
        mock_display_row.assert_called_once()
        mock_display_metrics.assert_called_once()

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_add_business_manager_validation_error(self, mock_session, mock_st):
        """Test de validation d'erreur dans l'ajout de BM"""
        # Mock st.columns pour éviter les erreurs
        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        # Simuler la soumission du formulaire avec des champs vides
        with patch('streamlit.form') as mock_form:
            mock_form_instance = MagicMock()
            mock_form.return_value.__enter__.return_value = mock_form_instance
            mock_form_instance.form_submit_button.return_value = True

            # Mock les champs vides
            mock_st.text_input.side_effect = ["", "", "", ""]  # nom, email, prenom, telephone vides
            mock_st.text_area.return_value = ""

            show_add_business_manager()

            # Vérifier que l'erreur de validation est affichée
            mock_st.error.assert_called_with("❌ Les champs Nom, Prénom et Email sont obligatoires")

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_add_business_manager_success(self, mock_session, mock_st):
        """Test d'ajout réussi d'un BM"""
        # Mock st.columns
        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query pour vérifier l'unicité de l'email
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Email pas encore utilisé
        mock_session_instance.query.return_value = mock_query

        with patch('streamlit.form') as mock_form:
            mock_form_instance = MagicMock()
            mock_form.return_value.__enter__.return_value = mock_form_instance
            mock_form_instance.form_submit_button.return_value = True

            # Mock les champs valides
            mock_st.text_input.side_effect = ["Dupont", "jean@test.com", "Jean", "0123456789"]  # nom, email, prenom, telephone
            mock_st.text_area.return_value = "Notes test"
            mock_st.checkbox.return_value = True

            show_add_business_manager()

            # Vérifier que le BM est ajouté en base
            mock_session_instance.add.assert_called_once()
            mock_session_instance.commit.assert_called_once()

            # Vérifier le message de succès
            mock_st.success.assert_called_once()

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_statistics_basic(self, mock_session, mock_st):
        """Test d'affichage des statistiques de base"""
        # Mock st.columns pour retourner 4 colonnes
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock les compteurs
        mock_session_instance.query.return_value.count.side_effect = [5, 3, 12]  # total_bms, active_bms, assignments

        show_statistics()

        # Vérifier que les métriques sont affichées
        mock_st.subheader.assert_called_with("📊 Statistiques des Business Managers")
        # Vérifier que les colonnes sont créées
        assert mock_st.columns.call_count >= 1

    @patch('app.pages_modules.business_managers.st')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_statistics_with_bm_data(self, mock_session, mock_st):
        """Test des statistiques avec données de BM"""
        # Mock st.columns
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock les requêtes
        mock_session_instance.query.return_value.count.side_effect = [2, 2, 5]  # total_bms, active_bms, assignments

        # Mock la requête pour les stats par BM
        mock_bm_query = MagicMock()
        mock_bm_query.filter.return_value = mock_bm_query
        mock_bm_query.all.return_value = [("Jean", "Dupont", 3), ("Marie", "Martin", 2)]

        # Mock la sous-requête count
        mock_subquery = MagicMock()
        mock_subquery.count.return_value = MagicMock()
        mock_session_instance.query.return_value = mock_subquery

        show_statistics()

        # Vérifier que les sous-titres sont affichés
        mock_st.subheader.assert_any_call("📊 Répartition des consultants par BM")