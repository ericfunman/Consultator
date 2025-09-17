"""
Tests pour les formulaires de consultants
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class TestConsultantForms:
    """Tests pour les formulaires de consultants"""

    @patch('app.pages_modules.consultant_forms.st')
    def test_show_add_consultant_form_imports_failed(self, mock_st):
        """Test du formulaire quand les imports échouent"""
        # Simuler l'échec des imports
        with patch('app.pages_modules.consultant_forms.imports_ok', False):
            from app.pages_modules.consultant_forms import show_add_consultant_form

            show_add_consultant_form()

            mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.ConsultantService')
    @patch('app.pages_modules.consultant_forms.get_database_session')
    def test_show_add_consultant_form_success(self, mock_get_session, mock_consultant_service, mock_st):
        """Test du formulaire d'ajout avec succès"""
        # Mock des imports réussis
        with patch('app.pages_modules.consultant_forms.imports_ok', True):
            # Mock des composants Streamlit
            mock_form = Mock()
            mock_st.form.return_value.__enter__ = Mock(return_value=mock_form)
            mock_st.form.return_value.__exit__ = Mock(return_value=None)

            # Mock des champs du formulaire
            mock_st.text_input.side_effect = [
                "Dupont", "Jean", "jean.dupont@email.com", "06 12 34 56 78"
            ]
            mock_st.selectbox.return_value = "Senior"
            mock_st.date_input.return_value = Mock()
            mock_st.text_area.return_value = "Consultant expérimenté"
            mock_st.form_submit_button.return_value = True

            # Mock du service consultant
            mock_consultant_service.create_consultant.return_value = Mock(id=1)

            from app.pages_modules.consultant_forms import show_add_consultant_form

            show_add_consultant_form()

            # Vérifier que le service a été appelé
            mock_consultant_service.create_consultant.assert_called_once()
            mock_st.success.assert_called_with("✅ Consultant ajouté avec succès !")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.ConsultantService')
    def test_show_add_consultant_form_validation_error(self, mock_consultant_service, mock_st):
        """Test du formulaire avec erreur de validation"""
        with patch('app.pages_modules.consultant_forms.imports_ok', True):
            # Mock des composants Streamlit
            mock_form = Mock()
            mock_st.form.return_value.__enter__ = Mock(return_value=mock_form)
            mock_st.form.return_value.__exit__ = Mock(return_value=None)

            # Mock des champs vides (erreur de validation)
            mock_st.text_input.side_effect = ["", "", "", ""]
            mock_st.form_submit_button.return_value = True

            from app.pages_modules.consultant_forms import show_add_consultant_form

            show_add_consultant_form()

            # Vérifier qu'une erreur est affichée
            mock_st.error.assert_called_with("❌ Veuillez remplir tous les champs obligatoires")

    @patch('app.pages_modules.consultant_forms.st')
    @patch('app.pages_modules.consultant_forms.ConsultantService')
    def test_show_add_consultant_form_service_error(self, mock_consultant_service, mock_st):
        """Test du formulaire avec erreur du service"""
        with patch('app.pages_modules.consultant_forms.imports_ok', True):
            # Mock des composants Streamlit
            mock_form = Mock()
            mock_st.form.return_value.__enter__ = Mock(return_value=mock_form)
            mock_st.form.return_value.__exit__ = Mock(return_value=None)

            # Mock des champs valides
            mock_st.text_input.side_effect = [
                "Dupont", "Jean", "jean.dupont@email.com", "06 12 34 56 78"
            ]
            mock_st.selectbox.return_value = "Senior"
            mock_st.date_input.return_value = Mock()
            mock_st.text_area.return_value = "Consultant expérimenté"
            mock_st.form_submit_button.return_value = True

            # Mock du service qui lève une exception
            mock_consultant_service.create_consultant.side_effect = Exception("Erreur DB")

            from app.pages_modules.consultant_forms import show_add_consultant_form

            show_add_consultant_form()

            # Vérifier qu'une erreur est affichée
            mock_st.error.assert_called_with("❌ Erreur lors de l'ajout du consultant: Erreur DB")


class TestConsultantList:
    """Tests pour l'affichage de la liste des consultants"""

    @patch('app.pages_modules.consultant_list.st')
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_success(self, mock_consultant_service, mock_st):
        """Test de l'affichage de la liste des consultants"""
        # Mock des consultants
        mock_consultant = Mock()
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "jean.dupont@email.com"
        mock_consultant.niveau = "Senior"

        mock_consultant_service.get_all_consultants.return_value = [mock_consultant]

        # Mock des colonnes
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_col4 = Mock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]

        from app.pages_modules.consultant_list import show_consultants_list

        show_consultants_list()

        # Vérifier que le service a été appelé
        mock_consultant_service.get_all_consultants.assert_called_once()

        # Vérifier que les informations sont affichées
        mock_st.write.assert_called()

    @patch('app.pages_modules.consultant_list.st')
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_empty(self, mock_consultant_service, mock_st):
        """Test de l'affichage quand il n'y a pas de consultants"""
        mock_consultant_service.get_all_consultants.return_value = []

        from app.pages_modules.consultant_list import show_consultants_list

        show_consultants_list()

        # Vérifier qu'un message d'information est affiché
        mock_st.info.assert_called_with("📝 Aucun consultant trouvé")

    @patch('app.pages_modules.consultant_list.st')
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_error(self, mock_consultant_service, mock_st):
        """Test de l'affichage avec erreur du service"""
        mock_consultant_service.get_all_consultants.side_effect = Exception("Erreur DB")

        from app.pages_modules.consultant_list import show_consultants_list

        show_consultants_list()

        # Vérifier qu'une erreur est affichée
        mock_st.error.assert_called_with("❌ Erreur lors du chargement des consultants: Erreur DB")


class TestConsultantProfile:
    """Tests pour l'affichage du profil consultant"""

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile.ConsultantService')
    def test_show_consultant_profile_success(self, mock_consultant_service, mock_st):
        """Test de l'affichage du profil consultant"""
        # Mock du consultant
        mock_consultant = Mock()
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "jean.dupont@email.com"
        mock_consultant.niveau = "Senior"
        mock_consultant.telephone = "06 12 34 56 78"
        mock_consultant.date_naissance = None
        mock_consultant.commentaires = "Consultant expérimenté"

        mock_consultant_service.get_consultant_by_id.return_value = mock_consultant

        from app.pages_modules.consultant_profile import show_consultant_profile

        show_consultant_profile(1)

        # Vérifier que le service a été appelé avec le bon ID
        mock_consultant_service.get_consultant_by_id.assert_called_with(1)

        # Vérifier que les informations sont affichées
        mock_st.subheader.assert_called_with("👤 Profil de Dupont Jean")

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile.ConsultantService')
    def test_show_consultant_profile_not_found(self, mock_consultant_service, mock_st):
        """Test de l'affichage quand le consultant n'est pas trouvé"""
        mock_consultant_service.get_consultant_by_id.return_value = None

        from app.pages_modules.consultant_profile import show_consultant_profile

        show_consultant_profile(999)

        # Vérifier qu'une erreur est affichée
        mock_st.error.assert_called_with("❌ Consultant non trouvé")

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile.ConsultantService')
    def test_show_consultant_profile_error(self, mock_consultant_service, mock_st):
        """Test de l'affichage avec erreur du service"""
        mock_consultant_service.get_consultant_by_id.side_effect = Exception("Erreur DB")

        from app.pages_modules.consultant_profile import show_consultant_profile

        show_consultant_profile(1)

        # Vérifier qu'une erreur est affichée
        mock_st.error.assert_called_with("❌ Erreur lors du chargement du profil: Erreur DB")
