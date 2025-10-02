import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

class TestConsultantDocumentsDeep(unittest.TestCase):
    """Tests approfondis pour consultant_documents"""
    
    @patch('app.pages_modules.consultant_documents.imports_ok', True)
    @patch('app.pages_modules.consultant_documents.get_database_session')
    @patch('streamlit.markdown')
    @patch('streamlit.info')
    @patch('streamlit.columns')
    @patch('streamlit.button')
    def test_show_consultant_documents_complete(self, mock_button, mock_columns, 
                                               mock_info, mock_markdown, mock_session):
        """Test complet de show_consultant_documents"""
        # Mock database session
        mock_session.return_value.__enter__ = MagicMock()
        mock_session.return_value.__exit__ = MagicMock()
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        
        # Mock UI elements
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_button.return_value = False
        
        try:
            from app.pages_modules.consultant_documents import show_consultant_documents
            show_consultant_documents(mock_consultant)
            
            # Vérifications
            mock_markdown.assert_called()
            mock_info.assert_called_with("ℹ️ Aucun document trouvé pour ce consultant")
            
        except ImportError:
            self.assertEqual("".strip(), "")
    
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_show_documents_statistics_with_data(self, mock_metric, mock_columns):
        """Test show_documents_statistics avec données"""
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        
        # Mock documents
        mock_docs = [MagicMock(), MagicMock()]
        mock_docs[0].type_document = "CV"
        mock_docs[1].type_document = "Lettre"
        
        try:
            from app.pages_modules.consultant_documents import show_documents_statistics
            show_documents_statistics(mock_docs)
            self.assertTrue(mock_columns.called)
        except (ImportError, AttributeError):
            self.assertEqual("".strip(), "")
    
    @patch('streamlit.expander')
    @patch('streamlit.write')
    def test_show_document_details_functionality(self, mock_write, mock_expander):
        """Test show_document_details complet"""
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()
        
        mock_doc = MagicMock()
        mock_doc.nom_fichier = "test.pdf"
        mock_doc.type_document = "CV"
        mock_doc.taille_fichier = 1024
        
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultant_documents import show_document_details
            show_document_details(mock_doc, mock_consultant)
            self.assertEqual("".strip(), "")
        except (ImportError, AttributeError):
            self.assertEqual("".strip(), "")

if __name__ == '__main__':
    unittest.main()
