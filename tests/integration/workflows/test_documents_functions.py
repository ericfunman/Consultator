import os
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from app.pages_modules.documents_functions import delete_consultant_document
from app.pages_modules.documents_functions import save_consultant_document
from app.pages_modules.documents_functions import show_consultant_documents
from app.pages_modules.documents_functions import show_existing_documents


class MockConsultant:
    def __init__(self, id=1, prenom="Jean", nom="Dupont"):
        self.id = id
        self.prenom = prenom
        self.nom = nom


class MockUploadedFile:
    def __init__(self, name="test.pdf", size=1024, content=b"test content"):
        self.name = name
        self.size = size
        self._content = content

    def getbuffer(self):
        return self._content


@pytest.fixture
def mock_consultant():
    return MockConsultant()


@pytest.fixture
def mock_uploaded_file():
    return MockUploadedFile()


from tests.fixtures.base_test import BaseIntegrationTest


class TestShowConsultantDocuments(BaseIntegrationTest):
    @patch("app.pages_modules.documents_functions.st")
    @patch("app.pages_modules.documents_functions.show_existing_documents")
    def test_show_consultant_documents_basic_display(
        self, mock_show_existing, mock_st, mock_consultant
    ):
        """Test affichage de base de la section documents"""
        # Setup
        mock_file_uploader = MagicMock(return_value=None)

        # Mock Streamlit components
        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.file_uploader = mock_file_uploader
        mock_st.markdown = MagicMock()

        # Execute
        show_consultant_documents(mock_consultant)

        # Verify
        mock_st.subheader.assert_called_once_with(
            f" Documents de {mock_consultant.prenom} {mock_consultant.nom}"
        )
        mock_st.expander.assert_called_once()
        mock_st.file_uploader.assert_called_once()
        mock_show_existing.assert_called_once_with(mock_consultant)

    @patch("app.pages_modules.documents_functions.st")
    @patch("app.pages_modules.documents_functions.show_existing_documents")
    @patch("app.pages_modules.documents_functions.save_consultant_document")
    def test_show_consultant_documents_with_file_upload(
        self,
        mock_save_doc,
        mock_show_existing,
        mock_st,
        mock_consultant,
        mock_uploaded_file,
    ):
        """Test upload de fichier avec sauvegarde"""
        # Setup
        mock_file_uploader = MagicMock(return_value=mock_uploaded_file)
        mock_columns = [MagicMock(), MagicMock(), MagicMock()]
        mock_metric = MagicMock()
        mock_selectbox = MagicMock(return_value="CV")
        mock_text_area = MagicMock(return_value="Test description")
        mock_button_cols = [MagicMock(), MagicMock()]
        mock_save_button = MagicMock(return_value=True)
        mock_cancel_button = MagicMock(return_value=False)

        # Mock Streamlit components
        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.file_uploader = mock_file_uploader
        mock_st.columns = MagicMock(side_effect=[mock_columns, mock_button_cols])
        mock_st.metric = mock_metric
        mock_st.selectbox = mock_selectbox
        mock_st.text_area = mock_text_area
        mock_st.button = MagicMock(side_effect=[mock_save_button, mock_cancel_button])
        mock_st.markdown = MagicMock()

        # Execute
        show_consultant_documents(mock_consultant)

        # Verify
        mock_save_doc.assert_called_once_with(
            mock_uploaded_file, mock_consultant, "CV", "Test description"
        )


class TestSaveConsultantDocument(BaseIntegrationTest):
    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.datetime")
    @patch("app.pages_modules.documents_functions.st")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_consultant_document_success(
        self,
        mock_file_open,
        mock_st,
        mock_datetime,
        mock_doc_service,
        mock_consultant,
        mock_uploaded_file,
    ):
        """Test sauvegarde réussie d'un document"""
        # Setup
        mock_upload_dir = MagicMock()
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        mock_doc_service.is_allowed_file.return_value = True
        mock_doc_service.get_file_extension.return_value = "pdf"

        mock_now = MagicMock()
        mock_now.strftime.return_value = "20231201_120000"
        mock_datetime.now.return_value = mock_now

        mock_st.success = MagicMock()
        mock_st.info = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.rerun = MagicMock()

        # Execute
        save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Test CV")

        # Verify
        mock_doc_service.init_upload_directory.assert_called_once()
        mock_doc_service.is_allowed_file.assert_called_once_with(
            mock_uploaded_file.name
        )
        mock_file_open.assert_called_once()
        mock_st.success.assert_called_once()
        mock_st.rerun.assert_called_once()

    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    def test_save_consultant_document_invalid_file_type(
        self, mock_st, mock_doc_service, mock_consultant, mock_uploaded_file
    ):
        """Test sauvegarde avec type de fichier invalide"""
        # Setup
        mock_doc_service.is_allowed_file.return_value = False
        mock_st.error = MagicMock()

        # Execute
        save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Test")

        # Verify
        mock_st.error.assert_called_once_with(" Type de fichier non supporte")

    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_consultant_document_with_exception(
        self,
        mock_file_open,
        mock_st,
        mock_doc_service,
        mock_consultant,
        mock_uploaded_file,
    ):
        """Test gestion d'exception lors de la sauvegarde"""
        # Setup
        mock_doc_service.init_upload_directory.return_value = MagicMock()
        mock_doc_service.is_allowed_file.return_value = True
        mock_file_open.side_effect = Exception("File write error")
        mock_st.error = MagicMock()

        # Execute
        save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Test")

        # Verify
        mock_st.error.assert_called_once()
        assert "Erreur lors de la sauvegarde" in mock_st.error.call_args[0][0]


class TestShowExistingDocuments(BaseIntegrationTest):
    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    def test_show_existing_documents_no_files(
        self, mock_st, mock_doc_service, mock_consultant
    ):
        """Test affichage quand aucun document n'existe"""
        # Setup
        mock_upload_dir = MagicMock()
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        mock_upload_dir.glob.return_value = []

        mock_st.info = MagicMock()

        # Execute
        show_existing_documents(mock_consultant)

        # Verify
        mock_st.info.assert_called_once_with(
            "📄 Aucun document trouve pour ce consultant"
        )

    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    @patch("app.pages_modules.documents_functions.delete_consultant_document")
    def test_show_existing_documents_with_files(
        self, mock_delete_doc, mock_st, mock_doc_service, mock_consultant
    ):
        """Test affichage des documents existants"""
        # Setup
        mock_upload_dir = MagicMock()
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir

        # Mock file with stats
        mock_file = MagicMock(spec=Path)
        mock_file.name = "Jean_Dupont_CV_20231201_120000.pdf"
        mock_file.stat.return_value = MagicMock(
            st_size=2048000, st_mtime=1701432000
        )  # 2MB, timestamp
        mock_upload_dir.glob.return_value = [mock_file]

        # Mock Streamlit components - need to handle multiple calls
        mock_columns_calls = [
            [
                MagicMock(),
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ],  # 4 columns for metrics
            [MagicMock(), MagicMock(), MagicMock()],  # 3 columns for buttons
        ]
        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.columns = MagicMock(side_effect=mock_columns_calls)
        mock_st.metric = MagicMock()
        mock_st.button = MagicMock(return_value=False)

        # Execute
        show_existing_documents(mock_consultant)

        # Verify
        mock_st.subheader.assert_called_once()
        mock_st.expander.assert_called_once()
        assert mock_st.columns.call_count == 2  # Should be called twice
        assert (
            mock_st.metric.call_count == 3
        )  # 3 metrics are actually called (size, modified, type)

    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    def test_show_existing_documents_with_exception(
        self, mock_st, mock_doc_service, mock_consultant
    ):
        """Test gestion d'exception lors de l'affichage"""
        # Setup
        mock_doc_service.init_upload_directory.side_effect = Exception(
            "Directory error"
        )
        mock_st.error = MagicMock()

        # Execute
        show_existing_documents(mock_consultant)

        # Verify
        mock_st.error.assert_called_once()
        assert "Erreur lors de l'affichage" in mock_st.error.call_args[0][0]


class TestDeleteConsultantDocument(BaseIntegrationTest):
    @patch("app.pages_modules.documents_functions.st")
    def test_delete_consultant_document_success(self, mock_st):
        """Test suppression réussie d'un document"""
        # Setup
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.exists.return_value = True
        mock_file_path.unlink = MagicMock()

        mock_st.success = MagicMock()
        mock_st.rerun = MagicMock()

        # Execute
        delete_consultant_document(mock_file_path)

        # Verify
        mock_file_path.unlink.assert_called_once()
        mock_st.success.assert_called_once_with(" Document supprime avec succes")
        mock_st.rerun.assert_called_once()

    @patch("app.pages_modules.documents_functions.st")
    def test_delete_consultant_document_file_not_found(self, mock_st):
        """Test suppression d'un fichier introuvable"""
        # Setup
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.exists.return_value = False

        mock_st.error = MagicMock()

        # Execute
        delete_consultant_document(mock_file_path)

        # Verify
        mock_st.error.assert_called_once_with(" Fichier introuvable")

    @patch("app.pages_modules.documents_functions.st")
    def test_delete_consultant_document_with_exception(self, mock_st):
        """Test gestion d'exception lors de la suppression"""
        # Setup
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.exists.return_value = True
        mock_file_path.unlink.side_effect = Exception("Delete error")

        mock_st.error = MagicMock()

        # Execute
        delete_consultant_document(mock_file_path)

        # Verify
        mock_st.error.assert_called_once()
        assert "Erreur lors de la suppression" in mock_st.error.call_args[0][0]


class TestIntegrationScenarios(BaseIntegrationTest):
    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    @patch("builtins.open", new_callable=mock_open)
    def test_complete_document_workflow(
        self, mock_file_open, mock_st, mock_doc_service, mock_consultant
    ):
        """Test workflow complet d'ajout et suppression de document"""
        # Setup
        mock_upload_dir = MagicMock()
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        mock_doc_service.is_allowed_file.return_value = True
        mock_doc_service.get_file_extension.return_value = "pdf"

        mock_uploaded_file = MockUploadedFile("test_cv.pdf", 1024000)

        # Mock datetime
        with patch("app.pages_modules.documents_functions.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.strftime.return_value = "20231201_120000"
            mock_datetime.now.return_value = mock_now

            # Mock Streamlit for success messages
            mock_st.success = MagicMock()
            mock_st.info = MagicMock()
            mock_st.button = MagicMock(return_value=False)
            mock_st.rerun = MagicMock()

            # Execute save
            save_consultant_document(
                mock_uploaded_file, mock_consultant, "CV", "Test CV"
            )

            # Verify save worked
            mock_st.success.assert_called_once()
            mock_st.rerun.assert_called_once()

    @patch("app.pages_modules.documents_functions.DocumentService")
    @patch("app.pages_modules.documents_functions.st")
    def test_file_size_display_logic(self, mock_st, mock_doc_service, mock_consultant):
        """Test logique d'affichage de la taille des fichiers"""
        # Setup
        mock_upload_dir = MagicMock()
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir

        # Mock small file (< 1MB)
        mock_small_file = MagicMock(spec=Path)
        mock_small_file.name = "Jean_Dupont_CV_small.pdf"
        mock_small_file.stat.return_value = MagicMock(
            st_size=512000, st_mtime=1701432000
        )  # 500KB
        mock_small_file.exists.return_value = True

        # Mock large file (> 1MB)
        mock_large_file = MagicMock(spec=Path)
        mock_large_file.name = "Jean_Dupont_CV_large.pdf"
        mock_large_file.stat.return_value = MagicMock(
            st_size=2097152, st_mtime=1701432000
        )  # 2MB
        mock_large_file.exists.return_value = True

        mock_upload_dir.glob.return_value = [mock_small_file, mock_large_file]

        # Mock Streamlit components with proper side effects
        mock_columns_calls = [
            [
                MagicMock(),
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ],  # 4 columns for metrics (first file)
            [
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ],  # 3 columns for buttons (first file)
            [
                MagicMock(),
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ],  # 4 columns for metrics (second file)
            [
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ],  # 3 columns for buttons (second file)
        ]

        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.columns = MagicMock(side_effect=mock_columns_calls)
        mock_st.metric = MagicMock()
        mock_st.button = MagicMock(return_value=False)

        # Execute
        show_existing_documents(mock_consultant)

        # Verify metrics were called (3 metrics per file = 6 total)
        assert mock_st.metric.call_count == 6
        assert mock_st.columns.call_count == 4  # 2 calls per file
