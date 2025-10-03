"""
Tests ciblés pour consultant_documents - Amélioration couverture 54% -> 70%+
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st


class TestConsultantDocumentsCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture de consultant_documents"""

    @patch("app.pages_modules.consultant_documents.st")
    @patch("app.pages_modules.consultant_documents.imports_ok", True)
    def test_show_basic(self, mock_st):
        """Test de la fonction show() de base"""
        mock_st.title.return_value = None
        mock_st.session_state = {}

        from app.pages_modules.consultant_documents import show

        show()

        mock_st.title.assert_called_once_with("📁 Documents consultant")

    @patch("app.pages_modules.consultant_documents.st")
    def test_create_cv_upload_form(self, mock_st):
        """Test de création du formulaire d'upload CV"""
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.file_uploader.return_value = None
        mock_st.form_submit_button.return_value = False

        from app.pages_modules.consultant_documents import _create_cv_upload_form

        result = _create_cv_upload_form(123)

        self.assertIsNotNone(result)

    @patch("app.pages_modules.consultant_documents.st")
    def test_display_document_not_found(self, mock_st):
        """Test d'affichage document non trouvé"""
        mock_st.error.return_value = None
        mock_st.info.return_value = None

        from app.pages_modules.consultant_documents import _display_document_not_found

        _display_document_not_found()

        mock_st.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
