"""
Tests pour améliorer la couverture de business_managers.py (28% -> 60%)
Tests fonctionnels et d'intégration pour le module business_managers.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, date

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock des modules Streamlit avant les imports
sys.modules['streamlit'] = Mock()
sys.modules['streamlit_option_menu'] = Mock()


class TestBusinessManagersCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture du module business_managers.py"""

    def setUp(self):
        """Configuration commune pour tous les tests"""
        # Mock streamlit et ses composants
        self.mock_st = Mock()

        # Mock pour st.tabs - retourne un tuple de 3 mocks context managers
        tab1 = Mock()
        tab1.__enter__ = Mock(return_value=tab1)
        tab1.__exit__ = Mock(return_value=None)
        tab2 = Mock()
        tab2.__enter__ = Mock(return_value=tab2)
        tab2.__exit__ = Mock(return_value=None)
        tab3 = Mock()
        tab3.__enter__ = Mock(return_value=tab3)
        tab3.__exit__ = Mock(return_value=None)
        self.mock_st.tabs.return_value = [tab1, tab2, tab3]

        # Mock pour st.form - context manager
        form_mock = Mock()
        form_mock.__enter__ = Mock(return_value=form_mock)
        form_mock.__exit__ = Mock(return_value=None)
        self.mock_st.form.return_value = form_mock

        # Mock pour st.columns - retourne des context managers selon le nombre demandé
        def mock_columns(n=2, **kwargs):
            cols = []
            for _ in range(n):
                col = Mock()
                col.__enter__ = Mock(return_value=col)
                col.__exit__ = Mock(return_value=None)
                cols.append(col)
            return cols

        self.mock_st.columns.side_effect = mock_columns

        # Configurer st.button pour retourner True seulement pour "Oui, supprimer"
        def mock_button(*args, **kwargs):
            result = True if args and "Oui, supprimer" in args[0] else False
            print(f"Button called with args={args}, kwargs={kwargs}, returning {result}")
            return result
        self.mock_st.button.side_effect = mock_button

        # Mock session_state avec support des attributs
        class MockSessionState(dict):
            """Mock session_state qui supporte l'accès par attribut et la suppression"""
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

            def __setattr__(self, name, value):
                self[name] = value

            def __delattr__(self, name):
                try:
                    del self[name]
                except KeyError:
                    raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

        self.mock_st.session_state = MockSessionState()

        # Configurer les champs de formulaire avec des valeurs par défaut
        self.mock_st.text_input.side_effect = lambda *args, **kwargs: "test_value"
        self.mock_st.text_area.return_value = "test_notes"
        self.mock_st.checkbox.return_value = True
        self.mock_st.form_submit_button.return_value = False  # Par défaut pas soumis

        # Créer un mock pour datetime
        mock_datetime_module = Mock()
        mock_datetime_module.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

        # Patcher les modules au niveau du système
        self.patches = [
            patch('app.pages_modules.business_managers.st', self.mock_st),
            patch('app.pages_modules.business_managers.get_database_session'),
            patch('app.pages_modules.business_managers.datetime', mock_datetime_module),
        ]

        for p in self.patches:
            p.start()

    def tearDown(self):
        """Nettoyage après chaque test"""
        for p in self.patches:
            p.stop()

    def test_validate_and_convert_bm_id_valid_string(self):
        """Test de validation d'un ID valide sous forme de chaîne"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        result = _validate_and_convert_bm_id("123")
        self.assertEqual(result, 123)

    def test_validate_and_convert_bm_id_valid_int(self):
        """Test de validation d'un ID valide sous forme d'entier"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        result = _validate_and_convert_bm_id(456)
        self.assertEqual(result, 456)

    def test_validate_and_convert_bm_id_invalid_string(self):
        """Test de validation d'un ID invalide sous forme de chaîne"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        result = _validate_and_convert_bm_id("abc")
        self.assertIsNone(result)
        self.mock_st.error.assert_called_once()

    def test_validate_and_convert_bm_id_none(self):
        """Test de validation d'un ID None"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        result = _validate_and_convert_bm_id(None)
        self.assertIsNone(result)

    def test_show_main_interface_no_profile_view(self):
        """Test de l'interface principale sans profil BM affiché"""
        # Mock pour que view_bm_profile ne soit pas dans session_state
        self.mock_st.session_state = {}

        from app.pages_modules.business_managers import show
        show()

        # Vérifier que le titre est affiché
        self.mock_st.title.assert_called_with("👔 Gestion des Business Managers")

    @patch('app.pages_modules.business_managers.show_bm_profile')
    def test_show_with_profile_view(self, mock_show_profile):
        """Test de l'interface principale avec un profil BM à afficher"""
        # Mock pour que view_bm_profile soit dans session_state
        self.mock_st.session_state = {"view_bm_profile": 123}

        from app.pages_modules.business_managers import show
        show()

        # Vérifier que show_bm_profile est appelée
        mock_show_profile.assert_called_once()

    @patch('app.pages_modules.business_managers.show_business_managers_list')
    @patch('app.pages_modules.business_managers.show_add_business_manager')
    @patch('app.pages_modules.business_managers.show_statistics')
    def test_show_tabs_creation(self, mock_stats, mock_add, mock_list):
        """Test de la création des onglets dans l'interface principale"""
        self.mock_st.session_state = {}

        from app.pages_modules.business_managers import show
        show()

        # Vérifier que st.tabs est appelée avec les bons arguments
        self.mock_st.tabs.assert_called_once_with(
            ["📋 Liste des BMs", "➕ Nouveau BM", "📊 Statistiques"]
        )

        # Vérifier que les fonctions d'onglets sont appelées
        mock_list.assert_called_once()
        mock_add.assert_called_once()
        mock_stats.assert_called_once()

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    @patch('app.pages_modules.business_managers._display_bm_header_and_info')
    @patch('app.pages_modules.business_managers._display_bm_general_info')
    @patch('app.pages_modules.business_managers._handle_bm_form_actions')
    @patch('app.pages_modules.business_managers.show_bm_consultants_management')
    def test_show_bm_profile_success(self, mock_consultants_mgmt, mock_form_actions,
                                   mock_display_info, mock_display_header, mock_validate):
        """Test de l'affichage réussi d'un profil BM"""
        mock_validate.return_value = 123

        # Ajouter view_bm_profile à session_state
        self.mock_st.session_state["view_bm_profile"] = 123

        # Mock BM
        mock_bm = Mock()
        mock_bm.id = 123
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"

        # Mock session
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_bm

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_bm_profile
            show_bm_profile()

            # Vérifier que les fonctions sont appelées
            mock_display_header.assert_called_once()
            mock_display_info.assert_called_once()
            mock_form_actions.assert_called_once()
            mock_consultants_mgmt.assert_called_once()

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    def test_show_bm_profile_invalid_id(self, mock_validate):
        """Test de l'affichage d'un profil BM avec ID invalide"""
        mock_validate.return_value = None

        # Ajouter view_bm_profile à session_state
        self.mock_st.session_state["view_bm_profile"] = 123

        from app.pages_modules.business_managers import show_bm_profile
        show_bm_profile()

        # Vérifier que st.rerun est appelée
        self.mock_st.rerun.assert_called_once()

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    def test_show_bm_profile_bm_not_found(self, mock_validate):
        """Test de l'affichage d'un profil BM introuvable"""
        mock_validate.return_value = 999

        # Ajouter view_bm_profile à session_state
        self.mock_st.session_state["view_bm_profile"] = 999

        # Mock session qui ne trouve pas le BM
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = None

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_bm_profile
            show_bm_profile()

            # Vérifier que l'erreur est affichée
            self.mock_st.error.assert_called_with("❌ Business Manager introuvable")

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    def test_show_bm_profile_database_error(self, mock_validate):
        """Test de gestion d'erreur de base de données dans show_bm_profile"""
        mock_validate.return_value = 123

        # Ajouter view_bm_profile à session_state
        self.mock_st.session_state["view_bm_profile"] = 123

        # Mock session qui lève une exception
        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(side_effect=Exception("DB Error"))
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_bm_profile
            show_bm_profile()

            # Vérifier que l'erreur est affichée
            self.mock_st.error.assert_called_with("❌ Erreur lors du chargement du profil : DB Error")

    @patch('app.pages_modules.business_managers.datetime')
    def test_show_edit_bm_form_success(self, mock_datetime):
        """Test de l'édition réussie d'un BM"""
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

        # Mock les champs du formulaire
        self.mock_st.text_input.side_effect = ["Dupont", "jean.dupont@test.com", "Jean", "0123456789"]
        self.mock_st.text_area.return_value = "Test notes"
        self.mock_st.checkbox.return_value = True
        self.mock_st.form_submit_button.return_value = True

        # Mock BM
        mock_bm = Mock()
        mock_bm.id = 123
        mock_bm.nom = "Dupont"
        mock_bm.prenom = "Jean"
        mock_bm.email = "jean.dupont@test.com"
        mock_bm.telephone = "0123456789"
        mock_bm.actif = True
        mock_bm.notes = "Test notes"

        # Mock session
        mock_session = Mock()
        mock_bm_to_update = Mock()
        mock_session.query.return_value.get.return_value = mock_bm_to_update

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_edit_bm_form
            show_edit_bm_form(mock_bm)

            # Vérifier que commit est appelée
            mock_session.commit.assert_called_once()

    def test_show_delete_bm_confirmation_with_assignments(self):
        """Test de la confirmation de suppression avec assignations actives"""
        # Définir delete_bm_mode pour que la fonction s'exécute
        self.mock_st.session_state = {"delete_bm_mode": True}

        # Mock pour st.columns - retourne un tuple de 3 mocks pour les boutons
        self.mock_st.columns.return_value = [Mock(), Mock(), Mock()]

        # Mock BM
        mock_bm = Mock()
        mock_bm.id = 123
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"

        # Mock session avec assignations
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.count.side_effect = [2, 5]  # assignations actives, total

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_delete_bm_confirmation
            show_delete_bm_confirmation(mock_bm)

            # Vérifier que l'avertissement est affiché
            self.mock_st.warning.assert_called_with("⚠️ Ce Business Manager a **2** consultant(s) actuellement assigné(s).")
            
            # Vérifier les appels à st.info dans l'ordre
            expected_calls = [
                (("La suppression clôturera automatiquement ces assignations.",), {}),
                (("📋 Historique total : **5** assignation(s)",), {})
            ]
            self.mock_st.info.assert_has_calls(expected_calls)

    def test_show_delete_bm_confirmation_success(self):
        """Test de la suppression réussie d'un BM"""
        # Mock BM
        mock_bm = Mock()
        mock_bm.id = 123
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"

        # Mock session pour les vérifications
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.count.return_value = 0  # Pas d'assignations
        mock_session.query.return_value.filter.return_value.all.return_value = []  # Liste vide pour les assignations

        # Mock pour la session de suppression
        mock_delete_session = Mock()
        mock_bm_to_delete = Mock()
        mock_delete_session.query.return_value.filter.return_value.first.return_value = mock_bm_to_delete

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        mock_delete_session_context = Mock()
        mock_delete_session_context.__enter__ = Mock(return_value=mock_delete_session)
        mock_delete_session_context.__exit__ = Mock(return_value=None)

        # Utiliser une liste mutable pour compter les appels
        call_counter = [0]

        def mock_get_session():
            call_counter[0] += 1
            if call_counter[0] == 1:
                return mock_session_context  # Première session pour vérifications
            else:
                return mock_delete_session_context  # Deuxième session pour suppression

        with patch('app.pages_modules.business_managers.get_database_session', side_effect=mock_get_session):
            # Patcher streamlit dans le module business_managers
            class MockSessionState(dict):
                """Mock session_state qui supporte l'accès par attribut et la suppression"""
                def __getattr__(self, name):
                    try:
                        return self[name]
                    except KeyError:
                        raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

                def __setattr__(self, name, value):
                    self[name] = value

                def __delattr__(self, name):
                    try:
                        del self[name]
                    except KeyError:
                        raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

            mock_st_module = Mock()
            mock_st_module.session_state = MockSessionState({"delete_bm_mode": True, "view_bm_profile": 123})

            # Mock pour st.columns - retourne des context managers
            def mock_columns(*args, **kwargs):
                col1 = Mock()
                col1.__enter__ = Mock(return_value=col1)
                col1.__exit__ = Mock(return_value=None)
                col2 = Mock()
                col2.__enter__ = Mock(return_value=col2)
                col2.__exit__ = Mock(return_value=None)
                col3 = Mock()
                col3.__enter__ = Mock(return_value=col3)
                col3.__exit__ = Mock(return_value=None)
                return [col1, col2, col3]

            mock_st_module.columns.side_effect = mock_columns

            # Mock pour st.button - retourne True pour le bouton de confirmation
            def mock_button(*args, **kwargs):
                if "Oui, supprimer" in str(args):
                    return True
                return False

            mock_st_module.button.side_effect = mock_button
            mock_st_module.success = Mock()
            mock_st_module.warning = Mock()
            mock_st_module.info = Mock()
            mock_st_module.error = Mock()
            mock_st_module.subheader = Mock()
            mock_st_module.write = Mock()
            mock_st_module.rerun = Mock()

            with patch('app.pages_modules.business_managers.st', mock_st_module):
                from app.pages_modules.business_managers import show_delete_bm_confirmation
                show_delete_bm_confirmation(mock_bm)

                # Vérifier que la suppression est appelée
                mock_delete_session.delete.assert_called_once_with(mock_bm_to_delete)
                mock_delete_session.commit.assert_called_once()

                # Vérifier que le succès est affiché
                mock_st_module.success.assert_called_with("✅ Business Manager Jean Dupont supprimé avec succès !")

                # Vérifier que les clés de session_state sont supprimées
                self.assertNotIn('view_bm_profile', mock_st_module.session_state)
                self.assertNotIn('delete_bm_mode', mock_st_module.session_state)

    @patch('app.pages_modules.business_managers.show_current_bm_consultants')
    @patch('app.pages_modules.business_managers.show_add_bm_assignment')
    @patch('app.pages_modules.business_managers.show_bm_assignments_history')
    def test_show_bm_consultants_management_tabs(self, mock_history, mock_add, mock_current):
        """Test de la gestion des consultants avec onglets"""
        mock_bm = Mock()
        mock_session = Mock()

        from app.pages_modules.business_managers import show_bm_consultants_management
        show_bm_consultants_management(mock_bm, mock_session)

        # Vérifier que st.tabs est appelée avec les bons arguments
        self.mock_st.tabs.assert_called_once_with(
            ["👥 Consultants actuels", "➕ Nouvelle assignation", "📊 Historique"]
        )

        # Vérifier que les fonctions d'onglets sont appelées
        mock_current.assert_called_once_with(mock_bm, mock_session)
        mock_add.assert_called_once_with(mock_bm, mock_session)
        mock_history.assert_called_once_with(mock_bm, mock_session)

    def test_get_current_assignments_query(self):
        """Test de la requête pour récupérer les assignations actuelles"""
        mock_session = Mock()
        mock_bm_id = 123

        from app.pages_modules.business_managers import _get_current_assignments
        _get_current_assignments(mock_bm_id, mock_session)

        # Vérifier que la requête est construite correctement
        mock_session.query.assert_called()

    def test_get_mission_data_with_mission(self):
        """Test de récupération des données de mission quand il y a une mission"""
        mock_consultant = Mock()
        mock_consultant.id = 456

        mock_mission = Mock()
        mock_mission.client = "Test Client"
        mock_mission.role = "Test Role"
        mock_mission.tjm = 500
        mock_mission.taux_journalier = None
        mock_mission.date_debut = date(2024, 1, 1)

        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_mission

        from app.pages_modules.business_managers import _get_mission_data
        result = _get_mission_data(mock_consultant, mock_session)

        self.assertEqual(result["client"], "Test Client")
        self.assertEqual(result["role"], "Test Role")
        self.assertEqual(result["tjm"], 500)

    def test_get_mission_data_no_mission(self):
        """Test de récupération des données de mission quand il n'y a pas de mission"""
        mock_consultant = Mock()
        mock_consultant.id = 456

        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        from app.pages_modules.business_managers import _get_mission_data
        result = _get_mission_data(mock_consultant, mock_session)

        self.assertEqual(result["client"], "N/A")
        self.assertEqual(result["role"], "N/A")
        self.assertEqual(result["tjm"], "N/A")

    def test_format_consultant_data_complete(self):
        """Test du formatage complet des données consultant"""
        mock_assignment = Mock()
        mock_assignment.date_debut = date(2024, 1, 1)

        mock_consultant = Mock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.type_contrat = "CDI"
        mock_consultant.disponibilite = True
        mock_consultant.salaire_actuel = 45000

        mission_data = {
            "client": "Test Client",
            "role": "Developer",
            "tjm": 500,
            "date_debut": "01/01/2024"
        }

        from app.pages_modules.business_managers import _format_consultant_data
        result = _format_consultant_data(mock_assignment, mock_consultant, mission_data)

        self.assertEqual(result["Consultant"], "Jean Dupont")
        self.assertEqual(result["Client actuel"], "Test Client")
        self.assertEqual(result["TJM"], "500€")
        self.assertEqual(result["Salaire"], "45000€")

    @patch('app.pages_modules.business_managers.datetime')
    def test_end_assignment_success(self, mock_datetime):
        """Test de la terminaison réussie d'une assignation"""
        mock_datetime.now.return_value.date.return_value = date(2024, 1, 1)
        mock_datetime.now.return_value.strftime.return_value = "01/01/2024"

        mock_assignment = Mock()
        mock_session = Mock()

        from app.pages_modules.business_managers import _end_assignment
        _end_assignment(mock_assignment, mock_session)

        # Vérifier que date_fin est définie
        self.assertEqual(mock_assignment.date_fin, date(2024, 1, 1))
        # Vérifier que commit est appelée
        mock_session.commit.assert_called_once()
        # Vérifier que success est affiché
        self.mock_st.success.assert_called_once()

    def test_end_assignment_error(self):
        """Test de la gestion d'erreur lors de la terminaison d'une assignation"""
        mock_assignment = Mock()
        mock_session = Mock()
        mock_session.commit.side_effect = Exception("DB Error")

        from app.pages_modules.business_managers import _end_assignment
        _end_assignment(mock_assignment, mock_session)

        # Vérifier que l'erreur est affichée
        self.mock_st.error.assert_called_with("❌ Erreur : DB Error")

    @patch('app.pages_modules.business_managers.datetime')
    def test_add_comment_to_assignment_success(self, mock_datetime):
        """Test de l'ajout réussi d'un commentaire à une assignation"""
        mock_datetime.now.return_value.strftime.return_value = "01/01/2024"

        mock_assignment = Mock()
        mock_assignment.commentaire = "Commentaire existant"
        mock_session = Mock()
        mock_session.query.return_value.get.return_value = mock_assignment

        from app.pages_modules.business_managers import _add_comment_to_assignment
        _add_comment_to_assignment(123, "Nouveau commentaire", mock_session)

        # Vérifier que le commentaire est ajouté
        self.assertIn("Nouveau commentaire", mock_assignment.commentaire)
        mock_session.commit.assert_called_once()

    def test_show_current_bm_consultants_no_assignments(self):
        """Test de l'affichage quand il n'y a pas d'assignations"""
        mock_bm = Mock()
        mock_bm.id = 123
        mock_session = Mock()

        # Mock pour retourner une liste vide
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = []

        from app.pages_modules.business_managers import show_current_bm_consultants
        show_current_bm_consultants(mock_bm, mock_session)

        # Vérifier que le message d'info est affiché
        self.mock_st.info.assert_called_with("👥 Aucun consultant actuellement assigné")

    def test_show_current_bm_consultants_with_data(self):
        """Test de l'affichage avec des données d'assignations"""
        mock_bm = Mock()
        mock_bm.id = 123
        mock_session = Mock()

        # Mock assignment et consultant
        mock_assignment = Mock()
        mock_assignment.date_debut = date(2024, 1, 1)
        mock_assignment.commentaire = "Test comment"

        mock_consultant = Mock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.type_contrat = "CDI"
        mock_consultant.disponibilite = True
        mock_consultant.salaire_actuel = 45000

        # Mock mission data
        with patch('app.pages_modules.business_managers._get_mission_data') as mock_get_mission:
            mock_get_mission.return_value = {
                "client": "Test Client",
                "role": "Developer",
                "tjm": 500,
                "date_debut": "01/01/2024"
            }

            mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [(mock_assignment, mock_consultant)]

            from app.pages_modules.business_managers import show_current_bm_consultants
            show_current_bm_consultants(mock_bm, mock_session)

            # Vérifier que dataframe est appelée
            self.mock_st.dataframe.assert_called()

    def test_show_business_managers_list_empty(self):
        """Test de l'affichage de la liste vide de BMs"""
        with patch('app.pages_modules.business_managers.BusinessManagerService') as mock_service:
            mock_service.get_all_business_managers.return_value = []

            from app.pages_modules.business_managers import show_business_managers_list
            show_business_managers_list()

            # Vérifier que info est appelée (le message exact peut varier selon la logique)
            self.mock_st.info.assert_called()

    def test_show_business_managers_list_with_data(self):
        """Test de l'affichage de la liste avec des données"""
        mock_bm_data = {
            "id": 123,
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "consultants_count": 5,
            "actif": True,
            "date_creation": datetime(2024, 1, 1)
        }

        with patch('app.pages_modules.business_managers.BusinessManagerService') as mock_service:
            mock_service.get_all_business_managers.return_value = [mock_bm_data]

            # Mock session pour le calcul des assignations
            mock_session = Mock()
            mock_session.query.return_value.filter.return_value.count.return_value = 10

            mock_session_context = Mock()
            mock_session_context.__enter__ = Mock(return_value=mock_session)
            mock_session_context.__exit__ = Mock(return_value=None)

            with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
                from app.pages_modules.business_managers import show_business_managers_list
                show_business_managers_list()

                # Vérifier que le tableau est affiché
                self.mock_st.markdown.assert_called()

    @patch('app.pages_modules.business_managers.datetime')
    def test_show_add_business_manager_success(self, mock_datetime):
        """Test de l'ajout réussi d'un Business Manager"""
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

        # Mock les champs du formulaire
        self.mock_st.text_input.side_effect = ["Dupont", "jean.dupont@test.com", "Jean", "0123456789"]
        self.mock_st.text_area.return_value = "Test notes"
        self.mock_st.checkbox.return_value = True
        self.mock_st.form_submit_button.return_value = True

        # Mock session
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = None  # Email unique

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_add_business_manager
            show_add_business_manager()

            # Vérifier que le BM est ajouté
            mock_session.add.assert_called()
            mock_session.commit.assert_called()

    @patch('app.pages_modules.business_managers.datetime')
    def test_show_add_business_manager_duplicate_email(self, mock_datetime):
        """Test de l'ajout d'un BM avec email déjà existant"""
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

        # Mock les champs du formulaire
        self.mock_st.text_input.side_effect = ["Dupont", "jean.dupont@test.com", "Jean", "0123456789"]
        self.mock_st.text_area.return_value = "Test notes"
        self.mock_st.checkbox.return_value = True
        self.mock_st.form_submit_button.return_value = True

        # Mock session avec email existant
        mock_existing_bm = Mock()
        mock_session = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_existing_bm

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_add_business_manager
            show_add_business_manager()

            # Vérifier que l'erreur est affichée
            self.mock_st.error.assert_called()

    def test_show_statistics_complete(self):
        """Test complet de l'affichage des statistiques"""
        # Mock session avec des données
        mock_session = Mock()

        # Configurer les counts pour les métriques générales
        mock_session.query.return_value.count.return_value = 5  # total_bms
        mock_session.query.return_value.filter.return_value.count.side_effect = [3, 2]  # active_bms, active_assignments

        # Mock pour les stats détaillées par BM
        mock_bm_stats = [(Mock(), Mock(), 3)]  # prenom, nom, consultants_count
        mock_bm_stats[0][0].prenom = "Jean"
        mock_bm_stats[0][0].nom = "Dupont"
        mock_bm_stats[0][0].actif = True

        # Mock pour la requête des stats par BM
        mock_query = Mock()
        mock_query.filter.return_value.all.return_value = mock_bm_stats
        mock_session.query.return_value.filter.return_value = mock_query

        mock_session_context = Mock()
        mock_session_context.__enter__ = Mock(return_value=mock_session)
        mock_session_context.__exit__ = Mock(return_value=None)

        with patch('app.pages_modules.business_managers.get_database_session', return_value=mock_session_context):
            from app.pages_modules.business_managers import show_statistics
            show_statistics()

            # Vérifier que les métriques sont affichées
            self.assertTrue(self.mock_st.write.called)  # Au moins un appel à write
            self.mock_st.subheader.assert_called_with("📊 Statistiques des Business Managers")

    def test_constants_definition(self):
        """Test que les constantes sont correctement définies"""
        from app.pages_modules.business_managers import (
            TELEPHONE_LABEL, DATE_FORMAT, DUREE_LABEL,
            ERROR_INVALID_BM_ID, ERROR_GENERIC, ERROR_ASSIGNMENT
        )
        self.assertEqual(TELEPHONE_LABEL, "Téléphone")
        self.assertEqual(DATE_FORMAT, "%d/%m/%Y")
        self.assertEqual(DUREE_LABEL, "Durée")
        self.assertEqual(ERROR_INVALID_BM_ID, "❌ Erreur : ID du Business Manager invalide")
        self.assertTrue(ERROR_GENERIC.startswith("❌ Erreur :"))
        self.assertTrue(ERROR_ASSIGNMENT.startswith("❌ Erreur lors de"))


if __name__ == '__main__':
    unittest.main()