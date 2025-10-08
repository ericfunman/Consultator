"""
Tests unitaires pour enhanced_ui.py (Phase 51 - Couverture 80%)
Objectif: Tester AdvancedUIFilters, RealTimeSearch, DataTableEnhancer, etc.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime, date
import time
import pandas as pd

from app.ui.enhanced_ui import (
    AdvancedUIFilters,
    RealTimeSearch,
    DataTableEnhancer,
    LoadingSpinner,
    NotificationManager,
    create_metric_card,
    create_info_card,
    display_consultant_card
)


class TestAdvancedUIFiltersInit:
    """Tests pour l'initialisation d'AdvancedUIFilters"""

    def test_init_default_values(self):
        """Test valeurs par défaut à l'initialisation"""
        filters = AdvancedUIFilters()
        
        assert filters.filters["search_term"] == ""
        assert filters.filters["practice_filter"] is None
        assert filters.filters["grade_filter"] is None
        assert filters.filters["availability_filter"] is None
        assert filters.filters["salaire_min"] is None
        assert filters.filters["salaire_max"] is None
        assert filters.filters["experience_min"] is None
        assert filters.filters["experience_max"] is None
        assert filters.filters["societe_filter"] is None
        assert filters.filters["type_contrat_filter"] is None
        assert filters.filters["date_entree_min"] is None
        assert filters.filters["date_entree_max"] is None


class TestGetUniqueValues:
    """Tests pour _get_unique_values"""

    def test_get_unique_values_practice_name(self):
        """Test récupération des practices"""
        filters = AdvancedUIFilters()
        result = filters._get_unique_values("practice_name")
        
        assert "Digital" in result
        assert "Data" in result
        assert "Cloud" in result
        assert "Cybersecurity" in result

    def test_get_unique_values_grade(self):
        """Test récupération des grades"""
        filters = AdvancedUIFilters()
        result = filters._get_unique_values("grade")
        
        assert "Junior" in result
        assert "Confirmé" in result
        assert "Senior" in result
        assert "Expert" in result

    def test_get_unique_values_type_contrat(self):
        """Test récupération des types de contrat"""
        filters = AdvancedUIFilters()
        result = filters._get_unique_values("type_contrat")
        
        assert "CDI" in result
        assert "CDD" in result
        assert "Freelance" in result
        assert "Stagiaire" in result

    def test_get_unique_values_societe(self):
        """Test récupération des sociétés"""
        filters = AdvancedUIFilters()
        result = filters._get_unique_values("societe")
        
        assert "Quanteam" in result
        assert "Asigma" in result
        assert "Autres" in result

    def test_get_unique_values_unknown_field(self):
        """Test champ inconnu retourne liste vide"""
        filters = AdvancedUIFilters()
        result = filters._get_unique_values("unknown_field")
        
        assert result == []

    def test_get_unique_values_exception_handling(self):
        """Test gestion d'exception - le code actuel ne les gère pas"""
        filters = AdvancedUIFilters()
        # Le code retourne [] pour les champs inconnus
        result = filters._get_unique_values("unknown_field")
        assert result == []


class TestResetFilters:
    """Tests pour reset_filters"""

    def test_reset_filters_all_values(self):
        """Test réinitialisation de tous les filtres"""
        filters = AdvancedUIFilters()
        
        # Modifier les filtres
        filters.filters["search_term"] = "test search"
        filters.filters["practice_filter"] = "Digital"
        filters.filters["grade_filter"] = "Senior"
        filters.filters["salaire_min"] = 50000
        filters.filters["salaire_max"] = 100000
        filters.filters["experience_min"] = 5.0
        filters.filters["experience_max"] = 10.0
        
        # Réinitialiser
        filters.reset_filters()
        
        assert filters.filters["search_term"] == ""
        assert filters.filters["practice_filter"] is None
        assert filters.filters["grade_filter"] is None


class TestApplyFilters:
    """Tests pour apply_filters"""

    def test_apply_filters_empty_data(self):
        """Test avec données vides"""
        filters = AdvancedUIFilters()
        result = filters.apply_filters([])
        
        assert result == []

    def test_apply_filters_search_term(self):
        """Test filtre de recherche textuelle"""
        filters = AdvancedUIFilters()
        filters.filters["search_term"] = "dupont"
        
        data = [
            {"nom": "Dupont", "prenom": "Jean", "email": "jean@test.com"},
            {"nom": "Martin", "prenom": "Marie", "email": "marie@test.com"}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"

    def test_apply_filters_practice_filter(self):
        """Test filtre par practice"""
        filters = AdvancedUIFilters()
        filters.filters["practice_filter"] = "Digital"
        
        data = [
            {"nom": "Dupont", "practice_name": "Digital"},
            {"nom": "Martin", "practice_name": "Data"},
            {"nom": "Bernard", "practice_name": "Digital"}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["practice_name"] == "Digital" for item in result)

    def test_apply_filters_grade_filter(self):
        """Test filtre par grade"""
        filters = AdvancedUIFilters()
        filters.filters["grade_filter"] = "Senior"
        
        data = [
            {"nom": "Dupont", "grade": "Senior"},
            {"nom": "Martin", "grade": "Junior"},
            {"nom": "Bernard", "grade": "Senior"}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["grade"] == "Senior" for item in result)

    def test_apply_filters_availability_filter_true(self):
        """Test filtre disponibilité = True"""
        filters = AdvancedUIFilters()
        filters.filters["availability_filter"] = True
        
        data = [
            {"nom": "Dupont", "disponibilite": True},
            {"nom": "Martin", "disponibilite": False},
            {"nom": "Bernard", "disponibilite": True}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["disponibilite"] is True for item in result)

    def test_apply_filters_availability_filter_false(self):
        """Test filtre disponibilité = False"""
        filters = AdvancedUIFilters()
        filters.filters["availability_filter"] = False
        
        data = [
            {"nom": "Dupont", "disponibilite": True},
            {"nom": "Martin", "disponibilite": False}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 1
        assert result[0]["disponibilite"] is False

    def test_apply_filters_societe_filter(self):
        """Test filtre par société"""
        filters = AdvancedUIFilters()
        filters.filters["societe_filter"] = "Quanteam"
        
        data = [
            {"nom": "Dupont", "societe": "Quanteam"},
            {"nom": "Martin", "societe": "Asigma"},
            {"nom": "Bernard", "societe": "Quanteam"}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["societe"] == "Quanteam" for item in result)

    def test_apply_filters_type_contrat_filter(self):
        """Test filtre par type de contrat"""
        filters = AdvancedUIFilters()
        filters.filters["type_contrat_filter"] = "CDI"
        
        data = [
            {"nom": "Dupont", "type_contrat": "CDI"},
            {"nom": "Martin", "type_contrat": "Freelance"},
            {"nom": "Bernard", "type_contrat": "CDI"}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["type_contrat"] == "CDI" for item in result)

    def test_apply_filters_salaire_min(self):
        """Test filtre salaire minimum"""
        filters = AdvancedUIFilters()
        filters.filters["salaire_min"] = 50000
        
        data = [
            {"nom": "Dupont", "salaire_actuel": 60000},
            {"nom": "Martin", "salaire_actuel": 45000},
            {"nom": "Bernard", "salaire_actuel": 70000}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["salaire_actuel"] >= 50000 for item in result)

    def test_apply_filters_salaire_max(self):
        """Test filtre salaire maximum"""
        filters = AdvancedUIFilters()
        filters.filters["salaire_max"] = 60000
        
        data = [
            {"nom": "Dupont", "salaire_actuel": 55000},
            {"nom": "Martin", "salaire_actuel": 70000},
            {"nom": "Bernard", "salaire_actuel": 60000}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["salaire_actuel"] <= 60000 for item in result)

    def test_apply_filters_experience_min(self):
        """Test filtre expérience minimum"""
        filters = AdvancedUIFilters()
        filters.filters["experience_min"] = 5.0
        
        data = [
            {"nom": "Dupont", "experience_annees": 7.0},
            {"nom": "Martin", "experience_annees": 3.0},
            {"nom": "Bernard", "experience_annees": 5.0}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["experience_annees"] >= 5.0 for item in result)

    def test_apply_filters_experience_max(self):
        """Test filtre expérience maximum"""
        filters = AdvancedUIFilters()
        filters.filters["experience_max"] = 10.0
        
        data = [
            {"nom": "Dupont", "experience_annees": 8.0},
            {"nom": "Martin", "experience_annees": 12.0},
            {"nom": "Bernard", "experience_annees": 10.0}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 2
        assert all(item["experience_annees"] <= 10.0 for item in result)

    def test_apply_filters_multiple_filters(self):
        """Test application de plusieurs filtres simultanés"""
        filters = AdvancedUIFilters()
        filters.filters["practice_filter"] = "Digital"
        filters.filters["grade_filter"] = "Senior"
        filters.filters["salaire_min"] = 50000
        
        data = [
            {"nom": "Dupont", "practice_name": "Digital", "grade": "Senior", "salaire_actuel": 60000},
            {"nom": "Martin", "practice_name": "Digital", "grade": "Junior", "salaire_actuel": 55000},
            {"nom": "Bernard", "practice_name": "Data", "grade": "Senior", "salaire_actuel": 65000},
            {"nom": "Durand", "practice_name": "Digital", "grade": "Senior", "salaire_actuel": 45000}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"


class TestRealTimeSearch:
    """Tests pour RealTimeSearch"""

    def test_init_default_values(self):
        """Test initialisation"""
        search = RealTimeSearch()
        
        assert search.last_search_time == 0
        assert search.search_debounce_ms == 300

    def test_should_search_first_time(self):
        """Test première recherche (devrait être autorisée)"""
        search = RealTimeSearch()
        
        result = search.should_search()
        
        assert result is True

    def test_should_search_debounce(self):
        """Test debounce (pas de recherche immédiate)"""
        search = RealTimeSearch()
        
        # Première recherche
        search.should_search()
        
        # Recherche immédiate (devrait être bloquée)
        result = search.should_search()
        
        assert result is False

    def test_should_search_after_debounce(self):
        """Test recherche après le délai de debounce"""
        search = RealTimeSearch()
        search.search_debounce_ms = 100  # 100ms pour le test
        
        # Première recherche
        search.should_search()
        
        # Attendre plus que le debounce
        time.sleep(0.15)
        
        # Recherche devrait être autorisée
        result = search.should_search()
        
        assert result is True

    @patch("app.ui.enhanced_ui.get_cached_consultants_list")
    def test_search_with_cache_empty_term(self, mock_cached_list):
        """Test recherche avec terme vide"""
        search = RealTimeSearch()
        mock_cached_list.return_value = [{"nom": "Dupont"}]
        
        result = search.search_with_cache("", 1, 50)
        
        mock_cached_list.assert_called_once_with(1, 50)
        assert result == [{"nom": "Dupont"}]

    @patch("app.ui.enhanced_ui.get_cached_search_results")
    def test_search_with_cache_with_term(self, mock_search_results):
        """Test recherche avec terme"""
        search = RealTimeSearch()
        mock_search_results.return_value = [{"nom": "Dupont"}]
        
        result = search.search_with_cache("dupont", 2, 100)
        
        mock_search_results.assert_called_once_with("dupont", 2, 100)
        assert result == [{"nom": "Dupont"}]

    @patch("app.ui.enhanced_ui.get_cached_consultants_list")
    def test_search_with_cache_whitespace_term(self, mock_cached_list):
        """Test recherche avec terme contenant seulement des espaces"""
        search = RealTimeSearch()
        mock_cached_list.return_value = []
        
        result = search.search_with_cache("   ", 1, 50)
        
        mock_cached_list.assert_called_once_with(1, 50)


class TestDataTableEnhancer:
    """Tests pour DataTableEnhancer"""

    @patch("streamlit.info")
    def test_render_enhanced_table_empty_data(self, mock_info):
        """Test avec données vides"""
        enhancer = DataTableEnhancer()
        result = enhancer.render_enhanced_table([])
        
        mock_info.assert_called_once_with("📝 Aucune donnée à afficher")
        assert result is None

    @patch("streamlit.dataframe")
    def test_render_enhanced_table_with_data(self, mock_dataframe):
        """Test avec données valides"""
        enhancer = DataTableEnhancer()
        data = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "jean@test.com",
                "salaire_actuel": 50000,
                "societe": "Quanteam",
                "grade": "Senior"
            }
        ]
        
        mock_dataframe.return_value = Mock()
        
        result = enhancer.render_enhanced_table(data, "test_table")
        
        mock_dataframe.assert_called_once()
        assert result is not None

    @patch("streamlit.dataframe")
    def test_render_enhanced_table_column_mapping(self, mock_dataframe):
        """Test mapping des colonnes"""
        enhancer = DataTableEnhancer()
        data = [
            {"id": 1, "prenom": "Jean", "nom": "Dupont"}
        ]
        
        mock_dataframe.return_value = Mock()
        
        enhancer.render_enhanced_table(data)
        
        # Vérifier que dataframe a été appelé avec un DataFrame
        call_args = mock_dataframe.call_args
        df_arg = call_args[0][0]
        
        assert isinstance(df_arg, pd.DataFrame)
        assert "ID" in df_arg.columns
        assert "Prénom" in df_arg.columns
        assert "Nom" in df_arg.columns

    def test_render_action_buttons_no_data(self):
        """Test boutons d'action sans données"""
        enhancer = DataTableEnhancer()
        result = enhancer.render_action_buttons(None, ["view", "edit", "delete"])
        
        assert result is None

    @patch("streamlit.button")
    @patch("streamlit.columns")
    @patch("streamlit.success")
    def test_render_action_buttons_view_action(self, mock_success, mock_cols, mock_button):
        """Test action 'view'"""
        enhancer = DataTableEnhancer()
        selected_data = {"prenom": "Jean", "nom": "Dupont", "id": 1}
        
        col1, col2, col3 = Mock(), Mock(), Mock()
        for col in [col1, col2, col3]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2, col3]
        mock_button.side_effect = [True, False, False]  # View clicked
        
        result = enhancer.render_action_buttons(selected_data, ["view", "edit", "delete"])
        
        assert result == "view"

    @patch("streamlit.button")
    @patch("streamlit.columns")
    @patch("streamlit.success")
    def test_render_action_buttons_edit_action(self, mock_success, mock_cols, mock_button):
        """Test action 'edit'"""
        enhancer = DataTableEnhancer()
        selected_data = {"prenom": "Jean", "nom": "Dupont", "id": 1}
        
        col1, col2, col3 = Mock(), Mock(), Mock()
        for col in [col1, col2, col3]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2, col3]
        mock_button.side_effect = [False, True, False]  # Edit clicked
        
        result = enhancer.render_action_buttons(selected_data, ["view", "edit", "delete"])
        
        assert result == "edit"

    @patch("streamlit.button")
    @patch("streamlit.columns")
    @patch("streamlit.success")
    def test_render_action_buttons_delete_action(self, mock_success, mock_cols, mock_button):
        """Test action 'delete'"""
        enhancer = DataTableEnhancer()
        selected_data = {"prenom": "Jean", "nom": "Dupont", "id": 1}
        
        col1, col2, col3 = Mock(), Mock(), Mock()
        for col in [col1, col2, col3]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2, col3]
        mock_button.side_effect = [False, False, True]  # Delete clicked
        
        result = enhancer.render_action_buttons(selected_data, ["view", "edit", "delete"])
        
        assert result == "delete"


class TestLoadingSpinner:
    """Tests pour LoadingSpinner"""

    @patch("streamlit.spinner")
    def test_show_loading_default_text(self, mock_spinner):
        """Test spinner avec texte par défaut"""
        LoadingSpinner.show_loading()
        
        mock_spinner.assert_called_once_with("Chargement en cours...")

    @patch("streamlit.spinner")
    def test_show_loading_custom_text(self, mock_spinner):
        """Test spinner avec texte personnalisé"""
        LoadingSpinner.show_loading("Traitement des données...")
        
        mock_spinner.assert_called_once_with("Traitement des données...")

    @patch("streamlit.progress")
    def test_show_progress_normal(self, mock_progress):
        """Test barre de progression normale"""
        mock_progress_bar = Mock()
        mock_progress.return_value = mock_progress_bar
        
        result = LoadingSpinner.show_progress(50, 100, "Test...")
        
        mock_progress.assert_called_once_with(0, text="Test...")
        mock_progress_bar.progress.assert_called_once_with(0.5)

    @patch("streamlit.progress")
    def test_show_progress_zero_total(self, mock_progress):
        """Test barre de progression avec total = 0"""
        mock_progress_bar = Mock()
        mock_progress.return_value = mock_progress_bar
        
        LoadingSpinner.show_progress(5, 0, "Test...")
        
        mock_progress_bar.progress.assert_called_once_with(0)

    @patch("streamlit.progress")
    def test_show_progress_complete(self, mock_progress):
        """Test barre de progression complète"""
        mock_progress_bar = Mock()
        mock_progress.return_value = mock_progress_bar
        
        LoadingSpinner.show_progress(100, 100, "Terminé!")
        
        mock_progress_bar.progress.assert_called_once_with(1.0)


class TestNotificationManager:
    """Tests pour NotificationManager"""

    @patch("time.sleep")
    @patch("streamlit.empty")
    @patch("streamlit.success")
    def test_show_success_with_duration(self, mock_success, mock_empty, mock_sleep):
        """Test notification de succès avec durée"""
        NotificationManager.show_success("Opération réussie", duration=3)
        
        mock_success.assert_called_once_with("Opération réussie")
        mock_sleep.assert_called_once_with(3)
        mock_empty.assert_called_once()

    @patch("time.sleep")
    @patch("streamlit.success")
    def test_show_success_no_duration(self, mock_success, mock_sleep):
        """Test notification de succès sans durée"""
        NotificationManager.show_success("Opération réussie", duration=0)
        
        mock_success.assert_called_once_with("Opération réussie")
        assert not mock_sleep.called

    @patch("time.sleep")
    @patch("streamlit.empty")
    @patch("streamlit.error")
    def test_show_error_with_duration(self, mock_error, mock_empty, mock_sleep):
        """Test notification d'erreur avec durée"""
        NotificationManager.show_error("Erreur détectée", duration=5)
        
        mock_error.assert_called_once_with("Erreur détectée")
        mock_sleep.assert_called_once_with(5)
        mock_empty.assert_called_once()

    @patch("time.sleep")
    @patch("streamlit.empty")
    @patch("streamlit.warning")
    def test_show_warning_with_duration(self, mock_warning, mock_empty, mock_sleep):
        """Test notification d'avertissement avec durée"""
        NotificationManager.show_warning("Attention", duration=4)
        
        mock_warning.assert_called_once_with("Attention")
        mock_sleep.assert_called_once_with(4)
        mock_empty.assert_called_once()

    @patch("time.sleep")
    @patch("streamlit.empty")
    @patch("streamlit.info")
    def test_show_info_with_duration(self, mock_info, mock_empty, mock_sleep):
        """Test notification d'information avec durée"""
        NotificationManager.show_info("Information", duration=3)
        
        mock_info.assert_called_once_with("Information")
        mock_sleep.assert_called_once_with(3)
        mock_empty.assert_called_once()


class TestUtilityFunctions:
    """Tests pour les fonctions utilitaires"""

    @patch("streamlit.metric")
    def test_create_metric_card_basic(self, mock_metric):
        """Test création de carte métrique basique"""
        create_metric_card("Label", 42)
        
        mock_metric.assert_called_once_with(label="Label", value=42, delta=None, delta_color="normal")

    @patch("streamlit.metric")
    def test_create_metric_card_with_delta(self, mock_metric):
        """Test création de carte métrique avec delta"""
        create_metric_card("Label", 100, delta=10, delta_color="inverse")
        
        mock_metric.assert_called_once_with(label="Label", value=100, delta=10, delta_color="inverse")

    @patch("streamlit.info")
    @patch("streamlit.markdown")
    def test_create_info_card_default_icon(self, mock_markdown, mock_info):
        """Test création de carte info avec icône par défaut"""
        create_info_card("Titre", "Contenu de test")
        
        mock_markdown.assert_called_once()
        assert "ℹ️" in mock_markdown.call_args[0][0]
        assert "Titre" in mock_markdown.call_args[0][0]
        mock_info.assert_called_once_with("Contenu de test")

    @patch("streamlit.info")
    @patch("streamlit.markdown")
    def test_create_info_card_custom_icon(self, mock_markdown, mock_info):
        """Test création de carte info avec icône personnalisée"""
        create_info_card("Titre", "Contenu", icon="⚠️")
        
        assert "⚠️" in mock_markdown.call_args[0][0]
        assert "Titre" in mock_markdown.call_args[0][0]

    @patch("streamlit.warning")
    def test_display_consultant_card_none(self, mock_warning):
        """Test affichage consultant None"""
        display_consultant_card(None)
        
        mock_warning.assert_called_once_with("⚠️ Aucun consultant fourni")

    @patch("streamlit.write")
    @patch("streamlit.columns")
    @patch("streamlit.markdown")
    def test_display_consultant_card_with_practice(self, mock_markdown, mock_cols, mock_write):
        """Test affichage carte consultant avec practice"""
        mock_consultant = Mock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.telephone = "0612345678"
        mock_consultant.actif = True
        mock_consultant.practice = Mock(nom="Digital")
        
        col1, col2 = Mock(), Mock()
        for col in [col1, col2]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2]
        
        display_consultant_card(mock_consultant)
        
        mock_markdown.assert_called_once()
        assert "Jean" in mock_markdown.call_args[0][0]
        assert "Dupont" in mock_markdown.call_args[0][0]

    @patch("streamlit.write")
    @patch("streamlit.columns")
    @patch("streamlit.markdown")
    def test_display_consultant_card_no_practice(self, mock_markdown, mock_cols, mock_write):
        """Test affichage carte consultant sans practice"""
        mock_consultant = Mock()
        mock_consultant.prenom = "Marie"
        mock_consultant.nom = "Martin"
        mock_consultant.email = "marie@test.com"
        mock_consultant.telephone = None
        mock_consultant.actif = False
        mock_consultant.practice = None
        
        col1, col2 = Mock(), Mock()
        for col in [col1, col2]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2]
        
        display_consultant_card(mock_consultant)
        
        # Vérifier que "N/A" est utilisé pour practice et téléphone
        assert mock_write.call_count >= 4


class TestEdgeCases:
    """Tests de cas limites"""

    def test_apply_filters_missing_fields(self):
        """Test filtres avec champs manquants dans les données"""
        filters = AdvancedUIFilters()
        filters.filters["salaire_min"] = 50000
        
        data = [
            {"nom": "Dupont"},  # Pas de salaire_actuel
            {"nom": "Martin", "salaire_actuel": 60000}
        ]
        
        result = filters.apply_filters(data)
        
        # L'élément sans salaire (0 par défaut) ne passe pas le filtre
        assert len(result) == 1
        assert result[0]["nom"] == "Martin"

    def test_apply_filters_none_values(self):
        """Test filtres avec valeurs None"""
        filters = AdvancedUIFilters()
        filters.filters["search_term"] = "test"
        
        data = [
            {"nom": "Dupont", "email": None},
            {"nom": None, "email": "test@example.com"}
        ]
        
        result = filters.apply_filters(data)
        
        assert len(result) == 1
        assert result[0]["email"] == "test@example.com"

    @patch("streamlit.dataframe")
    def test_render_enhanced_table_partial_columns(self, mock_dataframe):
        """Test tableau avec seulement certaines colonnes disponibles"""
        enhancer = DataTableEnhancer()
        data = [
            {"id": 1, "prenom": "Jean"}  # Colonnes minimales
        ]
        
        mock_dataframe.return_value = Mock()
        
        enhancer.render_enhanced_table(data)
        
        call_args = mock_dataframe.call_args
        df_arg = call_args[0][0]
        
        # Vérifier que seules les colonnes disponibles sont gardées
        assert "ID" in df_arg.columns
        assert "Prénom" in df_arg.columns
        assert "Salaire Actuel" not in df_arg.columns  # Pas dans les données d'origine

    def test_search_debounce_rapid_calls(self):
        """Test plusieurs appels rapides (debounce)"""
        search = RealTimeSearch()
        search.search_debounce_ms = 500
        
        results = []
        for _ in range(5):
            results.append(search.should_search())
            time.sleep(0.05)  # Très rapide
        
        # Seulement le premier devrait passer
        assert results[0] is True
        assert all(not r for r in results[1:])

    @patch("streamlit.progress")
    def test_show_progress_negative_current(self, mock_progress):
        """Test barre de progression avec valeur négative"""
        mock_progress_bar = Mock()
        mock_progress.return_value = mock_progress_bar
        
        LoadingSpinner.show_progress(-10, 100, "Test")
        
        # Même avec valeur négative, calcul donne un ratio
        mock_progress_bar.progress.assert_called_once()
        progress_value = mock_progress_bar.progress.call_args[0][0]
        assert progress_value == -0.1  # -10/100
