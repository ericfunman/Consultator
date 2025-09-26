"""
Tests de couverture pour consultant_documents.py - Version simplifiée
"""

import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.pages_modules.consultant_documents import show_documents_statistics


class TestConsultantDocumentsSimple:
    """Tests simples pour améliorer la couverture de consultant_documents.py"""

    @patch("app.pages_modules.consultant_documents.st")
    def test_show_documents_statistics_no_documents(self, mock_st):
        """Test des statistiques sans documents"""
        show_documents_statistics([])
        # Ne devrait rien afficher de spécial
        mock_st.markdown.assert_not_called()

    @patch("app.pages_modules.consultant_documents.st")
    def test_show_documents_statistics_with_documents(self, mock_st):
        """Test des statistiques avec documents"""
        # Mock st.columns pour retourner 4 mocks
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        # Créer des mocks de documents
        mock_doc1 = MagicMock()
        mock_doc1.type_document = "CV"
        mock_doc1.analyse_cv = '{"test": "data"}'
        mock_doc1.taille_fichier = 1024000  # 1MB

        mock_doc2 = MagicMock()
        mock_doc2.type_document = "Diplôme"
        mock_doc2.analyse_cv = None
        mock_doc2.taille_fichier = 512000  # 0.5MB

        documents = [mock_doc1, mock_doc2]

        show_documents_statistics(documents)

        # Vérifier les appels
        mock_st.markdown.assert_any_call("#### 📊 Statistiques")
        mock_st.metric.assert_any_call("Total documents", 2)
        mock_st.metric.assert_any_call("Type principal", "CV")
        mock_st.metric.assert_any_call("Analysés CV", 1)
        mock_st.metric.assert_any_call("Taille totale", "1.5 MB")


if __name__ == "__main__":
    import unittest

    unittest.main()
