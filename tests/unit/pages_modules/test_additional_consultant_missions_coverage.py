"""
Tests supplémentaires pour améliorer la couverture
"""

import pytest
from unittest.mock import Mock, patch
from datetime import date


class TestAdditionalConsultantMissionsCoverage:
    """Tests supplémentaires pour améliorer la couverture"""

    @pytest.fixture
    def mock_mission_active(self):
        """Mock d'une mission active"""
        mission = Mock()
        mission.id = 1
        mission.titre = "Projet Data Analytics"
        mission.client = Mock()
        mission.client.nom = "Société Générale"
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = None
        mission.en_cours = True
        mission.taux_journalier = 450
        mission.tjm = 450
        mission.salaire_mensuel = 0
        mission.description = "Développement d'un système d'analyse de données"
        mission.competences_requises = "Python, SQL"
        return mission

    @pytest.fixture
    def mock_mission_completed(self):
        """Mock d'une mission terminée"""
        mission = Mock()
        mission.id = 2
        mission.titre = "Migration Cloud"
        mission.client = Mock()
        mission.client.nom = "BNP Paribas"
        mission.date_debut = date(2023, 6, 1)
        mission.date_fin = date(2023, 12, 31)
        mission.en_cours = False
        mission.taux_journalier = 500
        mission.tjm = 500
        mission.salaire_mensuel = 0
        mission.description = "Migration des applications vers le cloud Azure"
        mission.competences_requises = "Azure, DevOps"
        return mission

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_period_active(self, mock_st, mock_mission_active):
        """Test de l'affichage de la période pour une mission active"""
        from app.pages_modules.consultant_missions import _display_mission_period

        _display_mission_period(mock_mission_active)

        mock_st.markdown.assert_called_with("**📅 Période**")
        mock_st.write.assert_any_call("**Statut :** 🔄 En cours")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_period_completed(self, mock_st, mock_mission_completed):
        """Test de l'affichage de la période pour une mission terminée"""
        from app.pages_modules.consultant_missions import _display_mission_period

        _display_mission_period(mock_mission_completed)

        mock_st.markdown.assert_called_with("**📅 Période**")
        mock_st.write.assert_any_call(f"**Fin :** {mock_mission_completed.date_fin.strftime('%d/%m/%Y')}")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_with_client(self, mock_st, mock_mission_active):
        """Test de l'affichage du client quand il existe"""
        from app.pages_modules.consultant_missions import _display_mission_client

        _display_mission_client(mock_mission_active)

        mock_st.markdown.assert_called_with("**🏢 Client**")
        mock_st.write.assert_any_call("**Nom :** Société Générale")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_without_client(self, mock_st):
        """Test de l'affichage du client quand il n'existe pas"""
        mission = Mock()
        mission.client = None

        from app.pages_modules.consultant_missions import _display_mission_client

        _display_mission_client(mission)

        mock_st.markdown.assert_called_with("**🏢 Client**")
        # Le code n'affiche rien d'autre quand client est None

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_remuneration_tjm(self, mock_st, mock_mission_active):
        """Test de l'affichage de la rémunération avec TJM"""
        from app.pages_modules.consultant_missions import _display_mission_remuneration

        _display_mission_remuneration(mock_mission_active)

        mock_st.markdown.assert_called_with("**💰 Rémunération**")
        mock_st.write.assert_any_call("**TJM Mission :** 450€")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_remuneration_taux_journalier(self, mock_st):
        """Test de l'affichage de la rémunération avec taux journalier ancien"""
        mission = Mock()
        mission.tjm = None
        mission.taux_journalier = 400
        mission.salaire_mensuel = 0

        from app.pages_modules.consultant_missions import _display_mission_remuneration

        _display_mission_remuneration(mission)

        mock_st.write.assert_any_call("**TJM (ancien) :** 400€")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_info_with_description(self, mock_st, mock_mission_active):
        """Test de l'affichage des informations avec description"""
        from app.pages_modules.consultant_missions import _display_mission_info

        _display_mission_info(mock_mission_active)

        mock_st.markdown.assert_called_with("**📊 Informations**")
        mock_st.write.assert_called_once()

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_actions(self, mock_st, mock_mission_active):
        """Test de l'affichage des actions de mission"""
        # Mock st.columns
        mock_columns = [Mock() for _ in range(3)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        # Mock boutons
        mock_st.button.side_effect = [False, False, False]

        from app.pages_modules.consultant_missions import _display_mission_actions

        _display_mission_actions(mock_mission_active)

        # Vérifier que les boutons ont été créés
        assert mock_st.button.call_count == 3

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_general_info_valid(self, mock_st):
        """Test du rendu des informations générales valides"""
        # Mock st.columns
        mock_columns = [Mock() for _ in range(2)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        # Mock inputs
        mock_st.text_input.return_value = "Test Mission"
        mock_st.selectbox.return_value = 1
        mock_st.date_input.side_effect = [date(2024, 1, 1), None]
        mock_st.checkbox.return_value = True

        from app.pages_modules.consultant_missions import _render_mission_general_info

        # Mock _load_clients_for_mission to return clients
        with patch("app.pages_modules.consultant_missions._load_clients_for_mission") as mock_load_clients:
            mock_load_clients.return_value = {1: "Test Client"}

            result = _render_mission_general_info()

            assert result is not None
            assert len(result) == 5
            assert result[0] == "Test Mission"

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_remuneration(self, mock_st):
        """Test du rendu de la rémunération"""
        # Mock st.columns
        mock_columns = [Mock() for _ in range(3)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        # Mock inputs
        mock_st.number_input.side_effect = [450, 450, 0]

        from app.pages_modules.consultant_missions import _render_mission_remuneration

        result = _render_mission_remuneration()

        assert len(result) == 3
        assert result[0] == 450  # taux_journalier
        assert result[1] == 450  # tjm
        assert result[2] == 0    # salaire_mensuel

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_description(self, mock_st):
        """Test du rendu de la description"""
        # Mock inputs
        mock_st.text_area.side_effect = ["Description test", "Compétences test"]

        from app.pages_modules.consultant_missions import _render_mission_description

        result = _render_mission_description()

        assert len(result) == 2
        assert result[0] == "Description test"
        assert result[1] == "Compétences test"

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_chronology_active(self, mock_st, mock_mission_active):
        """Test de l'affichage de la chronologie pour mission active"""
        from app.pages_modules.consultant_missions import _display_mission_chronology

        _display_mission_chronology(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 📅 Chronologie")
        mock_st.write.assert_any_call("**Statut :** 🔄 En cours")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_chronology_completed(self, mock_st, mock_mission_completed):
        """Test de l'affichage de la chronologie pour mission terminée"""
        from app.pages_modules.consultant_missions import _display_mission_chronology

        _display_mission_chronology(mock_mission_completed)

        mock_st.markdown.assert_called_with("#### 📅 Chronologie")
        # Vérifier le calcul de durée approximatif
        duration_days = (mock_mission_completed.date_fin - mock_mission_completed.date_debut).days
        duration_months = duration_days // 30
        mock_st.write.assert_any_call(f"**Durée :** {duration_months} mois ({duration_days} jours)")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_financial_aspects_with_tjm(self, mock_st, mock_mission_active):
        """Test de l'affichage des aspects financiers avec TJM"""
        from app.pages_modules.consultant_missions import _display_mission_financial_aspects

        _display_mission_financial_aspects(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 💰 Aspects financiers")
        mock_st.write.assert_any_call("**TJM Mission :** 450€")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_descriptions_with_data(self, mock_st, mock_mission_active):
        """Test de l'affichage des descriptions avec données"""
        from app.pages_modules.consultant_missions import _display_mission_descriptions

        _display_mission_descriptions(mock_mission_active)

        mock_st.markdown.assert_any_call("#### 📝 Description détaillée")
        mock_st.markdown.assert_any_call("#### 🛠️ Compétences requises")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_info_with_data(self, mock_st, mock_mission_active):
        """Test de l'affichage des informations client avec données"""
        # Mock st.columns
        mock_columns = [Mock() for _ in range(2)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_missions import _display_mission_client_info

        _display_mission_client_info(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 🏢 Informations client")

    @patch("app.pages_modules.consultant_missions.st")
    def test_calculate_mission_revenue_active(self, mock_st, mock_mission_active):
        """Test du calcul du revenu pour mission active"""
        from app.pages_modules.consultant_missions import _calculate_mission_revenue

        # Mock date.today pour contrôle
        with patch("app.pages_modules.consultant_missions.date") as mock_date:
            mock_date.today.return_value = date(2024, 6, 1)  # 5 mois après début
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs) if args else mock_date

            revenue = _calculate_mission_revenue(mock_mission_active)

            # Calcul attendu: 450 * (151 jours // 7 * 5)  450 * 105  47250
            assert revenue > 0

    @patch("app.pages_modules.consultant_missions.st")
    def test_calculate_mission_revenue_completed(self, mock_st, mock_mission_completed):
        """Test du calcul du revenu pour mission terminée"""
        from app.pages_modules.consultant_missions import _calculate_mission_revenue

        revenue = _calculate_mission_revenue(mock_mission_completed)

        # Calcul attendu pour mission terminée
        assert revenue > 0

    @patch("app.pages_modules.consultant_missions.st")
    def test_build_revenue_data(self, mock_st, mock_mission_active, mock_mission_completed):
        """Test de construction des données de revenus"""
        from app.pages_modules.consultant_missions import _build_revenue_data

        missions = [mock_mission_active, mock_mission_completed]
        revenue_data, total_revenue = _build_revenue_data(missions)

        assert isinstance(revenue_data, list)
        assert isinstance(total_revenue, (int, float))

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_imports_error(self, mock_st):
        """Test de show_consultant_missions avec erreur d'imports"""
        # Simuler l'erreur d'imports
        with patch("app.pages_modules.consultant_missions.imports_ok", False):
            from app.pages_modules.consultant_missions import show_consultant_missions
            
            mock_consultant = Mock()
            show_consultant_missions(mock_consultant)
            
            mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_consultant(self, mock_st):
        """Test de show_consultant_missions sans consultant"""
        from app.pages_modules.consultant_missions import show_consultant_missions
        
        show_consultant_missions(None)
        
        mock_st.error.assert_called_with("❌ Consultant non fourni")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_consultant_missions_exception(self, mock_get_session, mock_st, mock_consultant):
        """Test de show_consultant_missions avec exception"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Faire lever une exception lors de la requête
        mock_session.query.side_effect = Exception("Database error")
        
        from app.pages_modules.consultant_missions import show_consultant_missions
        show_consultant_missions(mock_consultant)
        
        mock_st.error.assert_called_with("❌ Erreur lors de l'affichage des missions: Database error")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_client(self, mock_st):
        """Test de validation avec client invalide"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=None,
            date_debut=date(2024, 1, 1),
            en_cours=True,
            date_fin=None
        )

        assert result is False
        mock_st.error.assert_called_with("❌ Le client est obligatoire")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_date(self, mock_st):
        """Test de validation avec date invalide"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=1,
            date_debut=None,
            en_cours=True,
            date_fin=None
        )

        assert result is False
        mock_st.error.assert_called_with("❌ La date de début est obligatoire")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_date_order(self, mock_st):
        """Test de validation avec dates dans le mauvais ordre"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=1,
            date_debut=date(2024, 6, 30),
            en_cours=False,
            date_fin=date(2024, 1, 1)
        )

        assert result is False
        mock_st.error.assert_called_with("❌ La date de fin doit être postérieure à la date de début")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_create_mission_exception(self, mock_get_session, mock_st):
        """Test de create_mission avec exception"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Faire lever une exception lors de l'ajout
        mock_session.add.side_effect = Exception("Database error")
        
        from app.pages_modules.consultant_missions import create_mission

        data = {
            "titre": "Test Mission",
            "client_id": 1,
            "date_debut": date(2024, 1, 1),
            "date_fin": None,
            "en_cours": True,
            "taux_journalier": 450,
            "tjm": 450,
            "salaire_mensuel": 0,
            "description": "Description test",
            "competences_requises": "Python, SQL"
        }

        result = create_mission(1, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Erreur lors de la création de la mission: Database error")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_update_mission_not_found(self, mock_get_session, mock_st):
        """Test de update_mission avec mission introuvable"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock de la requête qui ne trouve pas la mission
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        from app.pages_modules.consultant_missions import update_mission

        data = {"titre": "Titre modifié"}
        
        result = update_mission(999, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Mission introuvable")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_update_mission_exception(self, mock_get_session, mock_st, mock_mission_active):
        """Test de update_mission avec exception"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock de la requête qui trouve la mission
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_mission_active
        
        # Faire lever une exception lors du commit
        mock_session.commit.side_effect = Exception("Database error")

        from app.pages_modules.consultant_missions import update_mission

        data = {"titre": "Titre modifié"}
        
        result = update_mission(1, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Erreur lors de la mise à jour de la mission: Database error")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_delete_mission_not_found(self, mock_get_session, mock_st):
        """Test de delete_mission avec mission introuvable"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock de la requête qui ne trouve pas la mission
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        from app.pages_modules.consultant_missions import delete_mission

        result = delete_mission(999)

        assert result is False
        mock_st.error.assert_called_with("❌ Mission introuvable")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_delete_mission_exception(self, mock_get_session, mock_st, mock_mission_active):
        """Test de delete_mission avec exception"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock de la requête qui trouve la mission
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_mission_active
        
        # Faire lever une exception lors du delete
        mock_session.delete.side_effect = Exception("Database error")

        from app.pages_modules.consultant_missions import delete_mission

        result = delete_mission(1)

        assert result is False
        mock_st.error.assert_called_with("❌ Erreur lors de la suppression de la mission: Database error")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_statistics_empty(self, mock_st):
        """Test de show_missions_statistics avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_statistics

        show_missions_statistics([])
        
        # Ne devrait rien afficher pour une liste vide
        assert mock_st.markdown.call_count == 0

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis_empty(self, mock_st):
        """Test de show_missions_analysis avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_analysis

        show_missions_analysis([])
        
        mock_st.info.assert_called_with("ℹ️ Aucune mission à analyser")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_empty(self, mock_st):
        """Test de show_missions_revenues avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_revenues

        show_missions_revenues([])
        
        mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_no_revenue_data(self, mock_st):
        """Test de show_missions_revenues sans données de revenus"""
        # Mission sans taux journalier
        mission = Mock()
        mission.taux_journalier = None
        mission.tjm = None
        mission.en_cours = True
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = None
        mission.client = Mock()
        mission.client.nom = "Test Client"

        from app.pages_modules.consultant_missions import show_missions_revenues

        show_missions_revenues([mission])
        
        mock_st.info.assert_called_with("ℹ️ Aucune donnée de revenus disponible")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_add_mission_form_no_clients(self, mock_get_session, mock_st):
        """Test du formulaire d'ajout quand aucun client n'existe"""
        # Mock st.form
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form

        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Aucun client disponible
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = []

        from app.pages_modules.consultant_missions import show_add_mission_form

        show_add_mission_form(1)
        
        mock_st.warning.assert_called_with("⚠️ Aucun client trouvé. Veuillez créer des clients d'abord.")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_add_mission_form_exception(self, mock_get_session, mock_st):
        """Test du formulaire d'ajout avec exception"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Faire lever une exception lors du chargement des clients
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.all.side_effect = Exception("Database error")

        from app.pages_modules.consultant_missions import show_add_mission_form

        show_add_mission_form(1)
        
        mock_st.error.assert_called_with("❌ Erreur lors du chargement du formulaire: Database error")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_edit_mission_form_not_found(self, mock_get_session, mock_st):
        """Test du formulaire d'édition avec mission introuvable"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mission introuvable
        mock_query = Mock()
        mock_filtered = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_filtered
        mock_filtered.filter.return_value = mock_filtered
        mock_filtered.first.return_value = None

        from app.pages_modules.consultant_missions import show_edit_mission_form

        show_edit_mission_form(999)
        
        mock_st.error.assert_called_with("❌ Mission introuvable")

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_edit_mission_form_exception(self, mock_get_session, mock_st):
        """Test du formulaire d'édition avec exception"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Faire lever une exception lors du chargement
        mock_session.query.side_effect = Exception("Database error")

        from app.pages_modules.consultant_missions import show_edit_mission_form

        show_edit_mission_form(1)
        
        mock_st.error.assert_called_with("❌ Erreur lors du chargement du formulaire de modification: Database error")
