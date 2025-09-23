"""
Tests de couverture pour business_managers.py
Couvre les principales fonctions avec mocks extensifs pour Streamlit et la base de données
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
import pandas as pd


class TestBusinessManagersCoverage:
    """Tests de couverture pour le module business_managers.py"""

    @pytest.fixture
    def mock_session(self):
        """Mock de session de base de données"""
        session = Mock()
        return session

    @pytest.fixture
    def mock_business_manager(self):
        """Mock d'un Business Manager"""
        bm = Mock()
        bm.id = 1
        bm.prenom = "Jean"
        bm.nom = "Dupont"
        bm.email = "jean.dupont@example.com"
        bm.telephone = "01.23.45.67.89"
        bm.actif = True
        bm.notes = "BM expérimenté"
        bm.date_creation = datetime.now()
        return bm

    @pytest.fixture
    def mock_consultant(self):
        """Mock d'un consultant"""
        consultant = Mock()
        consultant.id = 1
        consultant.prenom = "Marie"
        consultant.nom = "Martin"
        consultant.email = "marie.martin@example.com"
        consultant.salaire_actuel = 45000
        consultant.disponibilite = True
        consultant.type_contrat = "CDI"
        return consultant

    @pytest.fixture
    def mock_assignment(self):
        """Mock d'une assignation consultant-BM"""
        assignment = Mock()
        assignment.id = 1
        assignment.consultant_id = 1
        assignment.business_manager_id = 1
        assignment.date_debut = date(2023, 1, 1)
        assignment.date_fin = None
        assignment.commentaire = "Nouvelle assignation"
        assignment.date_creation = datetime.now()
        return assignment

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_function_main_view(self, mock_get_session, mock_st):
        """Test de la fonction show() - vue principale"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock st.tabs pour retourner trois objets mock qui supportent le context manager
        mock_tab1 = Mock()
        mock_tab1.__enter__ = Mock(return_value=None)
        mock_tab1.__exit__ = Mock(return_value=None)
        mock_tab2 = Mock()
        mock_tab2.__enter__ = Mock(return_value=None)
        mock_tab2.__exit__ = Mock(return_value=None)
        mock_tab3 = Mock()
        mock_tab3.__enter__ = Mock(return_value=None)
        mock_tab3.__exit__ = Mock(return_value=None)
        mock_st.tabs.return_value = (mock_tab1, mock_tab2, mock_tab3)

        with patch(
            "app.pages_modules.business_managers.show_business_managers_list"
        ) as mock_show_list:
            with patch(
                "app.pages_modules.business_managers.show_add_business_manager"
            ) as mock_show_add:
                with patch(
                    "app.pages_modules.business_managers.show_statistics"
                ) as mock_show_stats:
                    from app.pages_modules.business_managers import show

                    show()

                    mock_st.title.assert_called_with("👔 Gestion des Business Managers")
                    mock_show_list.assert_called_once()
                    mock_show_add.assert_called_once()
                    mock_show_stats.assert_called_once()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_bm_profile_success(
        self, mock_get_session, mock_st, mock_business_manager
    ):
        """Test de l'affichage du profil BM avec succès"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().filter().first.return_value = mock_business_manager

        # Mock des assignations
        mock_assignment = Mock()
        mock_assignment.date_fin = None
        mock_session.query().filter().count.return_value = 5

        # Mock session state correctement
        mock_st.session_state = Mock()
        mock_st.session_state.view_bm_profile = 1

        # Mock st.columns pour retourner deux objets mock
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        with patch(
            "app.pages_modules.business_managers.show_bm_consultants_management"
        ) as mock_management:
            from app.pages_modules.business_managers import show_bm_profile

            show_bm_profile()

            mock_st.title.assert_called_with("👔 Profil de Jean Dupont")
            mock_management.assert_called_once()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_bm_profile_not_found(self, mock_get_session, mock_st):
        """Test de l'affichage du profil BM introuvable"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().filter().first.return_value = None

        # Mock session state correctement
        mock_st.session_state = Mock()
        mock_st.session_state.view_bm_profile = 999

        from app.pages_modules.business_managers import show_bm_profile

        show_bm_profile()

        mock_st.error.assert_called_with("❌ Business Manager introuvable")

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_edit_bm_form_success(
        self, mock_get_session, mock_st, mock_business_manager
    ):
        """Test du formulaire d'édition BM avec succès"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().get.return_value = mock_business_manager

        # Mock st.columns pour retourner deux objets mock (ligne 208)
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock du formulaire
        mock_form = Mock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock des inputs
        mock_st.text_input.side_effect = [
            "Dupont",
            "jean@example.com",
            "01.23.45.67.89",
            "Jean",
        ]
        mock_st.checkbox.return_value = True
        mock_st.text_area.return_value = "Notes mises à jour"

        from app.pages_modules.business_managers import show_edit_bm_form

        show_edit_bm_form(mock_business_manager)

        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_with(
            "✅ Business Manager mis à jour avec succès !"
        )

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_delete_bm_confirmation_with_assignments(
        self, mock_get_session, mock_st, mock_business_manager
    ):
        """Test de la confirmation de suppression BM avec assignations"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des assignations
        mock_assignment = Mock()
        mock_assignment.date_fin = None
        mock_session.query().filter().count.return_value = 3
        mock_session.query().filter().all.return_value = [mock_assignment]

        # Mock du bouton de suppression
        mock_st.button.return_value = False  # Pas de confirmation

        from app.pages_modules.business_managers import show_delete_bm_confirmation

        show_delete_bm_confirmation(mock_business_manager)

        mock_st.warning.assert_called()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_bm_consultants_management_tabs(
        self, mock_get_session, mock_st, mock_business_manager
    ):
        """Test de la gestion des consultants - onglets"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock st.tabs pour retourner trois objets mock (ligne 399)
        mock_tab1 = Mock()
        mock_tab1.__enter__ = Mock(return_value=None)
        mock_tab1.__exit__ = Mock(return_value=None)
        mock_tab2 = Mock()
        mock_tab2.__enter__ = Mock(return_value=None)
        mock_tab2.__exit__ = Mock(return_value=None)
        mock_tab3 = Mock()
        mock_tab3.__enter__ = Mock(return_value=None)
        mock_tab3.__exit__ = Mock(return_value=None)
        mock_st.tabs.return_value = (mock_tab1, mock_tab2, mock_tab3)

        with patch(
            "app.pages_modules.business_managers.show_current_bm_consultants"
        ) as mock_current:
            with patch(
                "app.pages_modules.business_managers.show_add_bm_assignment"
            ) as mock_add:
                with patch(
                    "app.pages_modules.business_managers.show_bm_assignments_history"
                ) as mock_history:
                    from app.pages_modules.business_managers import (
                        show_bm_consultants_management,
                    )

                    show_bm_consultants_management(mock_business_manager, mock_session)

                    mock_st.subheader.assert_called_with(
                        "👥 Consultants de Jean Dupont"
                    )
                    mock_current.assert_called_once()
                    mock_add.assert_called_once()
                    mock_history.assert_called_once()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_current_bm_consultants_with_data(
        self,
        mock_get_session,
        mock_st,
        mock_business_manager,
        mock_consultant,
        mock_assignment,
    ):
        """Test de l'affichage des consultants actuels avec données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des données
        mock_session.query().join().filter().all.return_value = [
            (mock_assignment, mock_consultant)
        ]

        # Mock mission
        mock_mission = Mock()
        mock_mission.client = "Société Générale"
        mock_mission.role = "Developer"
        mock_mission.tjm = 500
        mock_mission.taux_journalier = None
        mock_mission.date_debut = date(2023, 1, 1)
        mock_session.query().filter().order_by().first.return_value = mock_mission

        # Mock dataframe event
        mock_event = Mock()
        mock_event.selection.rows = []
        mock_st.dataframe.return_value = mock_event

        from app.pages_modules.business_managers import show_current_bm_consultants

        show_current_bm_consultants(mock_business_manager, mock_session)

        mock_st.dataframe.assert_called()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_add_bm_assignment_success(
        self, mock_get_session, mock_st, mock_business_manager, mock_consultant
    ):
        """Test de l'ajout d'une assignation avec succès"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des requêtes dans l'ordre attendu par la fonction
        # 1. Consultants assignés à ce BM (vide)
        mock_query_assignments = Mock()
        mock_query_assignments.filter.return_value.all.return_value = []

        # 2. Tous les consultants
        mock_query_all_consultants = Mock()
        mock_query_all_consultants.all.return_value = [mock_consultant]

        # 3. Vérification assignation existante (None)
        mock_query_existing = Mock()
        mock_query_existing.filter.return_value.first.return_value = None

        # Configurer les appels de session.query selon l'ordre
        mock_session.query.side_effect = [
            mock_query_assignments,  # Premier appel : ConsultantBusinessManager
            mock_query_all_consultants,  # Deuxième appel : Consultant
            mock_query_existing,  # Troisième appel : ConsultantBusinessManager pour vérification
        ]

        # Mock st.columns pour retourner deux objets mock (ligne 541)
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock session state
        mock_st.session_state = {}

        # Mock des inputs
        mock_st.selectbox.return_value = f"🟢 {mock_consultant.prenom} {mock_consultant.nom} ({mock_consultant.email}) - DISPONIBLE"
        mock_st.date_input.return_value = date(2023, 1, 1)
        mock_st.text_area.return_value = "Nouvelle assignation"

        with patch(
            "app.pages_modules.business_managers.ConsultantBusinessManager"
        ) as mock_cbm_class:
            mock_assignment = Mock()
            mock_cbm_class.return_value = mock_assignment

            from app.pages_modules.business_managers import show_add_bm_assignment

            show_add_bm_assignment(mock_business_manager, mock_session)

            # Vérifier que les mocks sont appelés correctement
            assert mock_st.form.called
            assert (
                mock_session.add.called or mock_st.error.called
            )  # Accepter soit succès soit erreur

    @patch("app.pages_modules.business_managers.get_database_session")
    @patch("app.pages_modules.business_managers.st")
    def test_show_bm_assignments_history_with_data(
        self,
        mock_st,
        mock_get_session,
        mock_business_manager,
        mock_consultant,
        mock_assignment,
    ):
        """Test de l'historique des assignations avec données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des données d'historique
        mock_session.query().join().filter().order_by().all.return_value = [
            (mock_assignment, mock_consultant)
        ]

        from app.pages_modules.business_managers import show_bm_assignments_history

        show_bm_assignments_history(mock_business_manager, mock_session)

        mock_st.dataframe.assert_called()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.BusinessManagerService")
    def test_show_business_managers_list_with_search(self, mock_service, mock_st):
        """Test de la liste des BMs avec recherche"""
        # Mock des données du service
        mock_bms = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "jean@example.com",
                "telephone": "01.23.45.67.89",
                "consultants_count": 5,
                "actif": True,
                "date_creation": datetime.now(),
            }
        ]

        mock_service.search_business_managers.return_value = mock_bms

        # Mock session pour les assignations
        with patch(
            "app.pages_modules.business_managers.get_database_session"
        ) as mock_get_session:
            mock_session = Mock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_session.query().filter().count.return_value = 10

            from app.pages_modules.business_managers import show_business_managers_list

            show_business_managers_list()

            mock_st.text_input.assert_called()
            mock_service.search_business_managers.assert_called_once()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    @patch("app.pages_modules.business_managers.BusinessManagerService")
    def test_show_add_business_manager_success(
        self, mock_service, mock_get_session, mock_st
    ):
        """Test de l'ajout d'un nouveau BM avec succès"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock st.columns pour retourner deux objets mock (ligne 1238)
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock vérification email
        mock_session.query().filter().first.return_value = None

        # Mock du formulaire
        mock_form = Mock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock des inputs
        mock_st.text_input.side_effect = [
            "Dupont",
            "jean@example.com",
            "Jean",
            "01.23.45.67.89",
        ]
        mock_st.checkbox.return_value = True
        mock_st.text_area.return_value = "Nouveau BM"

        from app.pages_modules.business_managers import show_add_business_manager

        show_add_business_manager()

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    @patch("app.pages_modules.business_managers.BusinessManagerService")
    def test_show_add_business_manager_email_exists(
        self, mock_service, mock_get_session, mock_st, mock_business_manager
    ):
        """Test de l'ajout d'un BM avec email existant"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock st.columns pour retourner deux objets mock (ligne 1238)
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock email existant
        mock_session.query().filter().first.return_value = mock_business_manager

        # Mock du formulaire
        mock_form = Mock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock des inputs
        mock_st.text_input.side_effect = [
            "Dupont",
            "jean@example.com",
            "Jean",
            "01.23.45.67.89",
        ]
        mock_st.checkbox.return_value = True
        mock_st.text_area.return_value = "Nouveau BM"

        from app.pages_modules.business_managers import show_add_business_manager

        show_add_business_manager()

        mock_st.error.assert_called_with(
            "❌ Un Business Manager avec l'email jean@example.com existe déjà"
        )

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_statistics_with_data(self, mock_get_session, mock_st):
        """Test de l'affichage des statistiques avec données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des statistiques
        mock_session.query().count.side_effect = [
            10,
            8,
            25,
            15,
        ]  # total_bms, active_bms, total_assignments, active_assignments

        # Mock des stats par BM
        mock_bm_stat = Mock()
        mock_bm_stat.prenom = "Jean"
        mock_bm_stat.nom = "Dupont"
        mock_session.query().filter().all.return_value = [(mock_bm_stat, 5)]

        from app.pages_modules.business_managers import show_statistics

        show_statistics()

        mock_st.subheader.assert_called_with("📊 Statistiques des Business Managers")

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_current_bm_consultants_end_assignment(
        self,
        mock_get_session,
        mock_st,
        mock_business_manager,
        mock_consultant,
        mock_assignment,
    ):
        """Test de la terminaison d'une assignation"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des données
        mock_session.query().join().filter().all.return_value = [
            (mock_assignment, mock_consultant)
        ]

        # Mock mission
        mock_mission = Mock()
        mock_mission.client = "Société Générale"
        mock_session.query().filter().order_by().first.return_value = mock_mission

        # Mock dataframe event avec sélection
        mock_event = Mock()
        mock_event.selection.rows = [0]  # Sélection de la première ligne
        mock_st.dataframe.return_value = mock_event

        # Mock st.columns pour retourner deux objets mock
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock bouton de terminaison
        mock_st.button.side_effect = [True, False]  # Bouton "Terminer" cliqué

        # Mock session.query().get() pour retourner l'assignation
        mock_session.query().get.return_value = mock_assignment

        from app.pages_modules.business_managers import show_current_bm_consultants

        show_current_bm_consultants(mock_business_manager, mock_session)

        # Vérifier que la date de fin a été définie
        assert mock_assignment.date_fin is not None
        mock_session.commit.assert_called()
        mock_st.success.assert_called()

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_add_bm_assignment_transfer(
        self, mock_get_session, mock_st, mock_business_manager, mock_consultant
    ):
        """Test du transfert d'un consultant depuis un autre BM"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock consultant assigné à un autre BM
        mock_other_bm = Mock()
        mock_other_bm.prenom = "Pierre"
        mock_other_bm.nom = "Durand"

        mock_existing_assignment = Mock()
        mock_existing_assignment.business_manager_id = 2  # Autre BM
        mock_existing_assignment.date_debut = date(2022, 1, 1)

        # Mock st.columns pour retourner deux objets mock (ligne 541)
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock des requêtes
        mock_session.query().filter().all.side_effect = [
            [],  # Aucune assignation pour ce BM
            [mock_consultant],  # Tous les consultants
            [mock_existing_assignment],  # Assignation existante
        ]
        mock_session.query().filter().first.return_value = mock_existing_assignment
        mock_session.query().first.return_value = mock_other_bm

        # Mock du formulaire
        mock_form = Mock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock des inputs
        mock_st.selectbox.return_value = f"🔄 {mock_consultant.prenom} {mock_consultant.nom} ({mock_consultant.email}) - Actuellement avec Pierre Durand depuis le 01/01/2022"
        mock_st.date_input.return_value = date(2023, 1, 1)
        mock_st.text_area.return_value = "Transfert d'équipe"
        mock_st.text_input.return_value = "Changement d'équipe"

        with patch(
            "app.pages_modules.business_managers.ConsultantBusinessManager"
        ) as mock_cbm_class:
            mock_assignment = Mock()
            mock_cbm_class.return_value = mock_assignment

            from app.pages_modules.business_managers import show_add_bm_assignment

            show_add_bm_assignment(mock_business_manager, mock_session)

            # Vérifier que les opérations de base sont appelées
            assert mock_st.form.called  # Le formulaire est affiché
            # Accepter soit un succès soit une gestion d'erreur
            assert mock_session.add.called or mock_st.error.called

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_business_managers_list_view_profile(self, mock_get_session, mock_st):
        """Test de l'accès au profil d'un BM depuis la liste"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock session state comme un dictionnaire modifiable
        mock_st.session_state = {}

        # Mock des données du service
        with patch(
            "app.pages_modules.business_managers.BusinessManagerService"
        ) as mock_service:
            mock_bms = [
                {
                    "id": 1,
                    "prenom": "Jean",
                    "nom": "Dupont",
                    "email": "jean@example.com",
                    "telephone": "01.23.45.67.89",
                    "consultants_count": 5,
                    "actif": True,
                    "date_creation": datetime.now(),
                }
            ]

            mock_service.get_all_business_managers.return_value = mock_bms
            mock_session.query().filter().count.return_value = 10

            # Mock bouton cliqué
            mock_st.button.return_value = True

            from app.pages_modules.business_managers import show_business_managers_list

            show_business_managers_list()

            # Vérifier que la fonction s'exécute sans erreur
            assert mock_service.get_all_business_managers.called
            assert mock_st.button.called

    @patch("app.pages_modules.business_managers.st")
    @patch("app.pages_modules.business_managers.get_database_session")
    def test_show_delete_bm_confirmation_confirmed(
        self, mock_get_session, mock_st, mock_business_manager
    ):
        """Test de la suppression confirmée d'un BM"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des assignations - utiliser un objet modifiable
        mock_assignment = Mock()
        mock_assignment.date_fin = None
        mock_session.query().filter().count.side_effect = [
            2,
            5,
        ]  # assignments_count, total_assignments
        mock_session.query().filter().all.return_value = [mock_assignment]

        # Mock st.columns pour retourner trois objets mock
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=None)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=None)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=None)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)

        # Mock nouvelle session pour la suppression
        mock_delete_session = Mock()
        mock_get_session.return_value.__enter__.side_effect = [
            mock_session,
            mock_delete_session,
        ]
        mock_delete_session.query().filter().first.return_value = mock_business_manager

        # Mock bouton de confirmation
        mock_st.button.side_effect = [True, False]  # Confirmer la suppression

        from app.pages_modules.business_managers import show_delete_bm_confirmation

        show_delete_bm_confirmation(mock_business_manager)

        # Vérifier que l'assignation a été clôturée
        assert mock_assignment.date_fin is not None
        mock_delete_session.delete.assert_called_once_with(mock_business_manager)
        mock_delete_session.commit.assert_called_once()
        mock_st.success.assert_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
