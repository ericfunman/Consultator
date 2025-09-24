"""
Tests de couverture pour consultant_documents.py
"""
from unittest.mock import MagicMock, patch
import pytest

from app.pages_modules.consultant_documents import show_consultant_documents

class TestBasicConsultantDocuments:
    """Tests de base pour consultant_documents"""

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.imports_ok', True)
    def test_show_consultant_documents_no_consultant(self, mock_st):
        """Test sans consultant fourni"""
        show_consultant_documents(None)
        mock_st.error.assert_called_with("❌ Consultant non fourni")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.imports_ok', False)
    def test_show_consultant_documents_no_imports(self, mock_st):
        """Test avec imports échoués"""
        mock_consultant = MagicMock()
        show_consultant_documents(mock_consultant)
        mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch('app.pages_modules.consultant_documents.show_documents_statistics')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    @patch('app.pages_modules.consultant_documents.st')
    def test_show_consultant_documents_with_consultant_no_documents(self, mock_st, mock_session, mock_show_stats):
        """Test avec consultant valide mais sans documents"""
        # Mock imports_ok to True and Document class
        with patch('app.pages_modules.consultant_documents.imports_ok', True), \
             patch('app.pages_modules.consultant_documents.Document', create=True):
            
            # Mock consultant
            mock_consultant = MagicMock()
            mock_consultant.id = 1
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"

            # Mock the database session to behave like SQLAlchemy
            documents = []
            mock_session_instance = MagicMock()
            mock_query = MagicMock()
            mock_query.filter.return_value = mock_query
            mock_query.order_by.return_value = mock_query
            mock_query.all.return_value = documents
            
            mock_session_instance.query.return_value = mock_query
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__ = lambda *args: None

            show_consultant_documents(mock_consultant)

            # Vérifier que les appels Streamlit ont été faits
            mock_st.markdown.assert_any_call("### 📁 Documents")
            mock_show_stats.assert_called_once_with([])
            mock_st.info.assert_called_with("ℹ️ Aucun document trouvé pour ce consultant")

    @patch('app.pages_modules.consultant_documents.show_documents_statistics')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    @patch('app.pages_modules.consultant_documents.st')
    def test_show_consultant_documents_with_documents(self, mock_st, mock_session, mock_show_stats):
        """Test avec consultant valide et documents"""
        # Mock imports_ok to True
        with patch('app.pages_modules.consultant_documents.imports_ok', True), \
             patch('app.pages_modules.consultant_documents.show_document_details') as mock_show_details:
            
            # Mock consultant
            mock_consultant = MagicMock()
            mock_consultant.id = 1
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"

            # Mock documents
            mock_doc1 = MagicMock()
            mock_doc1.nom_fichier = "cv.pdf"
            mock_doc1.type_document = "CV"
            mock_doc1.analyse_cv = None

            mock_doc2 = MagicMock()
            mock_doc2.nom_fichier = "diplome.pdf"
            mock_doc2.type_document = "Diplôme"
            mock_doc2.analyse_cv = None

    @patch('app.pages_modules.consultant_documents.show_documents_statistics')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    @patch('app.pages_modules.consultant_documents.st')
    def test_show_consultant_documents_with_documents(self, mock_st, mock_session, mock_show_stats):
        """Test avec consultant valide et documents"""
        # Mock imports_ok to True and Document class
        with patch('app.pages_modules.consultant_documents.imports_ok', True), \
             patch('app.pages_modules.consultant_documents.Document', create=True), \
             patch('app.pages_modules.consultant_documents.show_document_details') as mock_show_details:
            
            # Mock consultant
            mock_consultant = MagicMock()
            mock_consultant.id = 1
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"

            # Mock documents
            mock_doc1 = MagicMock()
            mock_doc1.nom_fichier = "cv.pdf"
            mock_doc1.type_document = "CV"
            mock_doc1.analyse_cv = None

            mock_doc2 = MagicMock()
            mock_doc2.nom_fichier = "diplome.pdf"
            mock_doc2.type_document = "Diplôme"
            mock_doc2.analyse_cv = None

            documents = [mock_doc1, mock_doc2]
            
            # Mock the database session to behave like SQLAlchemy
            mock_session_instance = MagicMock()
            mock_query = MagicMock()
            mock_query.filter.return_value = mock_query
            mock_query.order_by.return_value = mock_query
            mock_query.all.return_value = documents
            
            mock_session_instance.query.return_value = mock_query
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session.return_value.__exit__ = lambda *args: None

            show_consultant_documents(mock_consultant)

            # Vérifier que les appels Streamlit ont été faits
            mock_st.markdown.assert_any_call("### 📁 Documents")
            mock_st.markdown.assert_any_call("#### 📋 Documents disponibles")
            mock_show_stats.assert_called_once_with(documents)
            # Vérifier que show_document_details est appelé pour chaque document
            assert mock_show_details.call_count == 2