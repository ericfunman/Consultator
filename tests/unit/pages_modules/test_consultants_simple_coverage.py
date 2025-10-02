"""
Tests ultra-simples pour consultants.py - Version simplifiée
Couvre les fonctions principales avec un minimum de mocking
"""

import pytest
from unittest.mock import patch, MagicMock


class TestConsultantsSimpleCoverage:
    """Tests ultra-simples pour couverture maximale de consultants.py"""

    @patch('app.pages_modules.consultants.imports_ok', False)
    @patch('app.pages_modules.consultants.st')
    def test_show_imports_not_ok(self, mock_st):
        """Test show() quand imports_ok=False - couvre lignes 58-62"""
        from app.pages_modules.consultants import show

        show()

        mock_st.title.assert_called_once_with("👥 Gestion des consultants")
        mock_st.error.assert_called_once_with("❌ Les services de base ne sont pas disponibles")
        mock_st.info.assert_called_once_with("Vérifiez que tous les modules sont correctement installés")

    @patch('app.pages_modules.consultants.imports_ok', True)
    @patch('app.pages_modules.consultants.st')
    def test_show_normal_flow(self, mock_st):
        """Test show() en conditions normales - couvre lignes 69-76"""
        from app.pages_modules.consultants import show

        # Mock session_state sans view_consultant_profile
        mock_session_state = MagicMock()
        del mock_session_state.view_consultant_profile  # Simuler absence
        mock_st.session_state = mock_session_state

        # Mock tabs pour éviter l'erreur de unpacking
        mock_tab1 = MagicMock()
        mock_tab2 = MagicMock()
        mock_st.tabs.return_value = [mock_tab1, mock_tab2]

        with patch('app.pages_modules.consultants.show_consultants_list') as mock_show_list, \
             patch('app.pages_modules.consultants.show_add_consultant_form') as mock_show_add:

            show()

            mock_st.title.assert_called_once_with("👥 Gestion des consultants")
            mock_st.tabs.assert_called_once_with([" Consultants", "➕ Ajouter un consultant"])
            mock_show_list.assert_called_once()
            mock_show_add.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_load_consultant_data_success(self, mock_st):
        """Test _load_consultant_data() succès - couvre lignes 141-158"""
        from app.pages_modules.consultants import _load_consultant_data

        with patch('app.pages_modules.consultants.get_database_session') as mock_get_session:
            mock_session = MagicMock()
            mock_consultant = MagicMock()
            mock_consultant.id = 123
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"
            mock_consultant.email = "jean@test.com"
            mock_consultant.telephone = "0123456789"
            mock_consultant.salaire_actuel = 50000
            mock_consultant.disponibilite = True
            mock_consultant.notes = "Test notes"
            mock_consultant.date_creation = MagicMock()

            mock_practice = MagicMock()
            mock_practice.nom = "Test Practice"
            mock_consultant.practice = mock_practice

            mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = mock_consultant
            mock_get_session.return_value.__enter__.return_value = mock_session

            result_data, result_consultant = _load_consultant_data(123)

            assert result_data is not None
            assert result_data["id"] == 123
            assert result_data["prenom"] == "Jean"
            assert result_data["practice_name"] == "Test Practice"
            assert result_consultant == mock_consultant

    @patch('app.pages_modules.consultants.st')
    def test_load_consultant_data_not_found(self, mock_st):
        """Test _load_consultant_data() consultant non trouvé - couvre lignes 141-158"""
        from app.pages_modules.consultants import _load_consultant_data

        with patch('app.pages_modules.consultants.get_database_session') as mock_get_session:
            mock_session = MagicMock()
            mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = None
            mock_get_session.return_value.__enter__.return_value = mock_session

            result_data, result_consultant = _load_consultant_data(999)

            assert result_data is None
            assert result_consultant is None

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_header(self, mock_st):
        """Test _display_consultant_header() - couvre lignes 161-170"""
        from app.pages_modules.consultants import _display_consultant_header

        consultant_data = {
            "prenom": "Jean",
            "nom": "Dupont"
        }

        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        _display_consultant_header(consultant_data)

        mock_st.title.assert_called_once_with("👤 Profil de Jean Dupont")
        mock_st.columns.assert_called_once_with([6, 1])

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_metrics(self, mock_st):
        """Test _display_consultant_metrics() - couvre lignes 173-200"""
        from app.pages_modules.consultants import _display_consultant_metrics

        consultant_data = {
            "salaire_actuel": 50000,
            "disponibilite": True,
            "date_creation": MagicMock(),
            "practice_name": "Test Practice"
        }

        # Mock strftime pour date_creation
        consultant_data["date_creation"].strftime.return_value = "01/01/2024"

        mock_st.columns.return_value = [MagicMock() for _ in range(5)]

        _display_consultant_metrics(consultant_data)

        # Vérifier les métriques principales
        mock_st.metric.assert_any_call("💰 Salaire annuel", "50,000€")
        mock_st.metric.assert_any_call("📊 Statut", "✅ Disponible")
        mock_st.metric.assert_any_call("📅 Membre depuis", "01/01/2024")
        mock_st.metric.assert_any_call("🏢 Practice", "Test Practice")

    @patch('app.pages_modules.consultants.st')
    def test_show_consultant_not_found(self, mock_st):
        """Test _show_consultant_not_found() - couvre lignes 203-210"""
        from app.pages_modules.consultants import _show_consultant_not_found

        _show_consultant_not_found()

        mock_st.error.assert_called_once_with("❌ Consultant introuvable")
        mock_st.button.assert_called_once_with("← Retour à la liste", key="back_to_list_error")

    @patch('app.pages_modules.consultants.st')
    def test_show_consultant_profile_not_found(self, mock_st):
        """Test show_consultant_profile() consultant non trouvé - couvre lignes 213-280"""
        from app.pages_modules.consultants import show_consultant_profile

        with patch('app.pages_modules.consultants._load_consultant_data') as mock_load_data, \
             patch('app.pages_modules.consultants._show_consultant_not_found') as mock_show_not_found:

            mock_load_data.return_value = (None, None)

            show_consultant_profile()

            mock_show_not_found.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_load_consultant_for_edit(self, mock_st):
        """Test _load_consultant_for_edit() - couvre lignes 294-310"""
        from app.pages_modules.consultants import _load_consultant_for_edit

        with patch('app.pages_modules.consultants.get_database_session') as mock_get_session, \
             patch('app.pages_modules.consultants._load_consultant_with_relations') as mock_load_relations, \
             patch('app.pages_modules.consultants._extract_business_manager_info') as mock_extract_bm, \
             patch('app.pages_modules.consultants._get_current_practice_id') as mock_get_practice_id:

            # Mocks
            mock_consultant = MagicMock()
            mock_load_relations.return_value = mock_consultant
            mock_extract_bm.return_value = ("John Manager", "john@test.com")
            mock_get_practice_id.return_value = 1

            mock_session = MagicMock()
            mock_practice = MagicMock()
            mock_practice.nom = "Test Practice"
            mock_practice.id = 1
            mock_session.query.return_value.filter.return_value.all.return_value = [mock_practice]
            mock_get_session.return_value.__enter__.return_value = mock_session

            result = _load_consultant_for_edit(123)

            assert len(result) == 5
            assert result[0] == mock_consultant
            assert result[1] == {"Test Practice": 1}
            assert result[2] == 1
            assert result[3] == "John Manager"
            assert result[4] == "john@test.com"

    def test_extract_business_manager_info_with_bm(self):
        """Test _extract_business_manager_info() avec BM - couvre lignes 323-328"""
        from app.pages_modules.consultants import _extract_business_manager_info

        mock_consultant = MagicMock()
        mock_bm = MagicMock()
        mock_bm.nom_complet = "John Manager"
        mock_bm.email = "john@test.com"
        mock_consultant.business_manager_actuel = mock_bm

        result = _extract_business_manager_info(mock_consultant)

        assert result == ("John Manager", "john@test.com")

    def test_extract_business_manager_info_without_bm(self):
        """Test _extract_business_manager_info() sans BM - couvre lignes 323-328"""
        from app.pages_modules.consultants import _extract_business_manager_info

        mock_consultant = MagicMock()
        mock_consultant.business_manager_actuel = None

        result = _extract_business_manager_info(mock_consultant)

        assert result == (None, None)

    def test_get_current_practice_id_with_practice_id(self):
        """Test _get_current_practice_id() avec practice_id - couvre lignes 331-333"""
        from app.pages_modules.consultants import _get_current_practice_id

        mock_consultant = MagicMock()
        mock_consultant.practice_id = 123

        result = _get_current_practice_id(mock_consultant)

        assert result == 123

    def test_get_current_practice_id_without_practice_id(self):
        """Test _get_current_practice_id() sans practice_id - couvre lignes 331-333"""
        from app.pages_modules.consultants import _get_current_practice_id

        mock_consultant = MagicMock()
        del mock_consultant.practice_id  # Simuler absence d'attribut

        result = _get_current_practice_id(mock_consultant)

        assert result is None

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status_with_experience(self, mock_st):
        """Test _display_consultant_status() avec expérience - couvre lignes 543-555"""
        from app.pages_modules.consultants import _display_consultant_status

        mock_consultant = MagicMock()
        mock_date = MagicMock()
        mock_consultant.date_premiere_mission = mock_date
        mock_consultant.experience_annees = 5

        _display_consultant_status(mock_consultant)

        mock_st.markdown.assert_called_with("---")
        mock_st.info.assert_called_with("📊 **Expérience calculée :** 5 années")

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status_without_experience(self, mock_st):
        """Test _display_consultant_status() sans expérience - couvre lignes 543-555"""
        from app.pages_modules.consultants import _display_consultant_status

        mock_consultant = MagicMock()
        mock_consultant.date_premiere_mission = None

        _display_consultant_status(mock_consultant)

        mock_st.info.assert_called_with("📊 **Expérience :** Non calculée (date première mission manquante)")

    @patch('app.pages_modules.consultants.st')
    def test_process_consultant_form_submission_success(self, mock_st):
        """Test _process_consultant_form_submission() succès - couvre lignes 558-583"""
        from app.pages_modules.consultants import _process_consultant_form_submission

        mock_consultant = MagicMock()
        mock_consultant.id = 123

        form_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com"
        }

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service, \
             patch('app.pages_modules.consultants._build_update_data') as mock_build:

            mock_service.get_consultant_by_email.return_value = None
            mock_service.update_consultant.return_value = True
            mock_build.return_value = {"test": "data"}

            result = _process_consultant_form_submission(mock_consultant, form_data)

            assert result == True
            mock_st.success.assert_called_with("✅ Jean Dupont modifié avec succès !")
            mock_st.rerun.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_process_consultant_form_submission_validation_error(self, mock_st):
        """Test _process_consultant_form_submission() erreur validation - couvre lignes 558-583"""
        from app.pages_modules.consultants import _process_consultant_form_submission

        mock_consultant = MagicMock()
        form_data = {
            "prenom": "",  # Vide
            "nom": "Dupont",
            "email": "jean@test.com"
        }

        result = _process_consultant_form_submission(mock_consultant, form_data)

        assert result == False
        mock_st.error.assert_called_with("❌ Veuillez remplir tous les champs obligatoires (*)")

    def test_build_update_data(self):
        """Test _build_update_data() - couvre lignes 586-604"""
        from app.pages_modules.consultants import _build_update_data

        form_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire": 50000,
            "disponibilite": True,
            "notes": "Test notes",
            "selected_practice_id": 1,
            "societe": "Quanteam",
            "date_entree": MagicMock(),
            "date_sortie": None,
            "date_premiere_mission": MagicMock(),
            "grade": "Senior",
            "type_contrat": "CDI"
        }

        result = _build_update_data(form_data)

        expected = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "disponibilite": True,
            "notes": "Test notes",
            "practice_id": 1,
            "societe": "Quanteam",
            "date_entree_societe": form_data["date_entree"],
            "date_sortie_societe": None,
            "date_premiere_mission": form_data["date_premiere_mission"],
            "grade": "Senior",
            "type_contrat": "CDI"
        }

        assert result == expected

    @patch('app.pages_modules.consultants.st')
    def test_display_no_functional_skills_message(self, mock_st):
        """Test _display_no_functional_skills_message() - couvre lignes 906-912"""
        from app.pages_modules.consultants import _display_no_functional_skills_message

        _display_no_functional_skills_message()

        mock_st.info.assert_called_with("📝 Aucune compétence fonctionnelle enregistrée")
        mock_st.write.assert_called_with(
            "Utilisez l'onglet **'Ajouter Compétences'** pour ajouter des compétences bancaires/assurance."
        )