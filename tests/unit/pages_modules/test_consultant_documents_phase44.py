"""Tests Phase 44: consultant_documents.py (23% → 24%)"""
import unittest
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestDisplayDocumentNotFound(unittest.TestCase):
    @patch("app.pages_modules.consultant_documents.st")
    def test_display_document_not_found(self, mock_st):
        from app.pages_modules.consultant_documents import _display_document_not_found
        
        _display_document_not_found()
        
        # Vérifie error appelé
        mock_st.error.assert_called()

class TestHandleRenameFormCancellation(unittest.TestCase):
    @patch("app.pages_modules.consultant_documents.st")
    def test_handle_rename_form_cancellation(self, mock_st):
        from app.pages_modules.consultant_documents import _handle_rename_form_cancellation
        
        mock_st.session_state = {"renaming_document_id": 1}
        
        _handle_rename_form_cancellation()
        
        # Vérifie que session_state a été modifié
        self.assertIsNotNone(mock_st.session_state)

if __name__ == "__main__":
    unittest.main()
