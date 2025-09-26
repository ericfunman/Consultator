"""
Tests pour le module documents_upload.py
"""

from io import BytesIO
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.pages_modules.documents_upload import save_uploaded_document
from app.pages_modules.documents_upload import show
from app.pages_modules.documents_upload import show_document_upload_section
from tests.fixtures.base_test import BaseIntegrationTest


class TestDocumentsUploadModule(BaseIntegrationTest):
    """Tests pour le module documents_upload"""

    @patch("app.pages_modules.documents_upload.imports_ok", True)
    @patch("app.pages_modules.documents_upload.st.title")
    @patch("app.pages_modules.documents_upload.st.markdown")
    @patch("app.pages_modules.documents_upload.show_document_upload_section")
    def test_show_success(self, mock_show_section, mock_markdown, mock_title):
        """Test de show() avec imports réussis"""
        show()

        mock_title.assert_called_once_with(" Gestion des documents")
        mock_markdown.assert_called_once_with("### Uploadez et gérez les documents")
        mock_show_section.assert_called_once()

    @patch("app.pages_modules.documents_upload.imports_ok", False)
    @patch("app.pages_modules.documents_upload.st.title")
    @patch("app.pages_modules.documents_upload.st.markdown")
    @patch("app.pages_modules.documents_upload.st.error")
    def test_show_imports_failed(self, mock_error, mock_markdown, mock_title):
        """Test de show() avec imports échoués"""
        show()

        mock_title.assert_called_once_with(" Gestion des documents")
        mock_markdown.assert_called_once_with("### Uploadez et gérez les documents")
        mock_error.assert_called_once_with(
            " Les services de documents ne sont pas disponibles"
        )

    @patch("app.pages_modules.documents_upload.imports_ok", True)
    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    def test_show_document_upload_section_no_file(self, mock_uploader, mock_subheader):
        """Test de show_document_upload_section() sans fichier uploadé"""
        mock_uploader.return_value = None

        show_document_upload_section()

        mock_subheader.assert_called_once_with(" Upload de documents")
        mock_uploader.assert_called_once()

    @patch("app.pages_modules.documents_upload.imports_ok", True)
    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    @patch("streamlit.columns")
    @patch("streamlit.metric")
    @patch("streamlit.button")
    def test_show_document_upload_section_with_file(
        self, mock_button, mock_metric, mock_columns, mock_uploader, mock_subheader
    ):
        """Test de show_document_upload_section() avec fichier uploadé"""
        # Mock fichier uploadé
        mock_file = Mock()
        mock_file.name = "test_document.pdf"
        mock_file.size = 1024 * 500  # 500 KB
        mock_uploader.return_value = mock_file

        # Mock colonnes
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        mock_button.return_value = False  # Ne pas cliquer sur sauvegarder

        show_document_upload_section()

        mock_subheader.assert_called_once_with(" Upload de documents")
        mock_uploader.assert_called_once()
        mock_columns.assert_called_once_with(3)
        mock_metric.assert_any_call("📄 Nom du fichier", "test_document.pdf")
        mock_metric.assert_any_call(" Taille", "500.0 KB")
        mock_button.assert_called_once_with(
            " Sauvegarder document", type="primary", key="save_document"
        )

    @patch("app.pages_modules.documents_upload.imports_ok", False)
    @patch("streamlit.error")
    def test_show_document_upload_section_imports_failed(self, mock_error):
        """Test de show_document_upload_section() avec imports échoués"""
        show_document_upload_section()

        mock_error.assert_called_once_with(
            " Les services de documents ne sont pas disponibles"
        )

    @patch("app.pages_modules.documents_upload.DocumentService")
    @patch("streamlit.success")
    @patch("streamlit.info")
    @patch("builtins.open", new_callable=MagicMock)
    def test_save_uploaded_document_success(
        self, mock_open, mock_info, mock_success, mock_doc_service
    ):
        """Test de save_uploaded_document() avec succès"""
        # Mock fichier
        mock_file = Mock()
        mock_file.name = "test.pdf"
        mock_file.getbuffer.return_value = b"test content"

        # Mock DocumentService
        mock_upload_dir = Mock()
        mock_upload_dir.__truediv__ = Mock(return_value="/path/to/file.pdf")
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        mock_doc_service.get_file_extension.return_value = "pdf"

        # Mock context manager pour open()
        mock_file_handle = Mock()
        mock_open.return_value.__enter__ = Mock(return_value=mock_file_handle)
        mock_open.return_value.__exit__ = Mock(return_value=None)

        save_uploaded_document(mock_file)

        mock_doc_service.init_upload_directory.assert_called_once()
        mock_doc_service.get_file_extension.assert_called_once_with("test.pdf")
        mock_open.assert_called_once_with("/path/to/file.pdf", "wb")
        mock_file_handle.write.assert_called_once_with(b"test content")
        mock_success.assert_called()
        mock_info.assert_called()

    @patch("app.pages_modules.documents_upload.DocumentService")
    @patch("streamlit.error")
    def test_save_uploaded_document_error(self, mock_error, mock_doc_service):
        """Test de save_uploaded_document() avec erreur"""
        # Mock fichier
        mock_file = Mock()
        mock_file.name = "test.pdf"

        # Mock DocumentService qui lève une exception
        mock_doc_service.init_upload_directory.side_effect = Exception("Test error")

        save_uploaded_document(mock_file)

        mock_error.assert_called_once()
        assert "Erreur lors de la sauvegarde" in str(mock_error.call_args[0][0])

    def test_module_imports(self):
        """Test des imports du module"""
        import app.pages_modules.documents_upload as upload_module

        # Vérifier que les fonctions existent
        assert hasattr(upload_module, "show")
        assert callable(upload_module.show)

        assert hasattr(upload_module, "show_document_upload_section")
        assert callable(upload_module.show_document_upload_section)

        assert hasattr(upload_module, "save_uploaded_document")
        assert callable(upload_module.save_uploaded_document)

        # Vérifier les variables d'import
        assert hasattr(upload_module, "DocumentService")
        assert hasattr(upload_module, "imports_ok")

    @patch("app.pages_modules.documents_upload.imports_ok", True)
    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    @patch("streamlit.columns")
    @patch("streamlit.metric")
    @patch("streamlit.button")
    @patch("app.pages_modules.documents_upload.save_uploaded_document")
    def test_show_document_upload_section_save_button_clicked(
        self,
        mock_save_func,
        mock_button,
        mock_metric,
        mock_columns,
        mock_uploader,
        mock_subheader,
    ):
        """Test de show_document_upload_section() avec clic sur sauvegarder"""
        # Mock fichier uploadé
        mock_file = Mock()
        mock_file.name = "test.pdf"
        mock_file.size = 1024 * 200  # 200 KB
        mock_uploader.return_value = mock_file

        # Mock colonnes
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        mock_button.return_value = True  # Clic sur sauvegarder

        show_document_upload_section()

        mock_save_func.assert_called_once_with(mock_file)

    @patch("app.pages_modules.documents_upload.imports_ok", True)
    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    @patch("streamlit.columns")
    @patch("streamlit.metric")
    def test_show_document_upload_section_large_file(
        self, mock_metric, mock_columns, mock_uploader, mock_subheader
    ):
        """Test de show_document_upload_section() avec fichier volumineux"""
        # Mock fichier volumineux
        mock_file = Mock()
        mock_file.name = "large_document.pdf"
        mock_file.size = 1024 * 1024 * 5  # 5 MB
        mock_uploader.return_value = mock_file

        # Mock colonnes
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        show_document_upload_section()

        mock_metric.assert_any_call("📄 Nom du fichier", "large_document.pdf")
        mock_metric.assert_any_call(" Taille", "5.0 MB")
