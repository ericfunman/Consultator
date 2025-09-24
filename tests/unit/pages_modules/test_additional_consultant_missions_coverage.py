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
    def test_display_revenue_statistics(self, mock_st, mock_mission_active):
        """Test de l'affichage des statistiques de revenus"""
        # Mock st.columns
        mock_columns = [Mock() for _ in range(3)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_missions import _display_revenue_statistics

        missions = [mock_mission_active]
        _display_revenue_statistics(missions, 100000)

        # Vérifier que st.metric a été appelé
        assert mock_st.metric.call_count > 0
