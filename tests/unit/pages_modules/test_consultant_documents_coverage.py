"""
Tests complets pour consultant_documents.py - Amélioration de la couverture
"""
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, patch, mock_open
import pytest

from app.pages_modules.consultant_documents import (
    show_consultant_documents,
    show_document_details,
    show_documents_statistics,
    show_upload_document_form,
    upload_document,
    analyze_consultant_cv,
    perform_cv_analysis,
    show_full_cv_analysis,
    show_documents_report,
    download_document,
    reanalyze_document,
    rename_document,
    delete_document,
    show_rename_document_form,
    generate_cv_report,
)


class TestConsultantDocumentsCoverage:
    """Tests complets pou        mock_st.columns.assert_called_with(2)
        assert mock_st.button.call_count == 2


if __name__ == "__main__":
    import unittest
    unittest.main()rer la couverture de consultant_documents.py"""

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_show_documents_statistics_no_documents(self, mock_session, mock_st):
        """Test des statistiques sans documents"""
        show_documents_statistics([])
        # Ne devrait rien afficher de spécial
        mock_st.markdown.assert_not_called()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_show_documents_statistics_with_documents(self, mock_session, mock_st):
        """Test des statistiques avec documents"""
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
        mock_st.metric.assert_any_call("Taille totale", "1.4 MB")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_show_upload_document_form_display(self, mock_session, mock_st):
        """Test de l'affichage du formulaire d'upload"""
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_upload_document_form(1)

        mock_st.markdown.assert_any_call("### 📤 Uploader un document")
        mock_st.markdown.assert_any_call("#### 📄 Informations du document")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.upload_document')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_show_upload_document_form_submit_success(self, mock_session, mock_upload, mock_st):
        """Test de soumission réussie du formulaire d'upload"""
        mock_upload.return_value = True

        # Mock form submission
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.form_submit_button.side_effect = [True, False]  # submitted=True, cancel=False
        mock_st.file_uploader.return_value = MagicMock()
        mock_st.selectbox.return_value = "CV"
        mock_st.text_area.return_value = "Test description"
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_upload_document_form(1)

        mock_upload.assert_called_once()
        mock_st.success.assert_called_with("✅ Document uploadé avec succès !")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.upload_document')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_show_upload_document_form_submit_no_file(self, mock_session, mock_upload, mock_st):
        """Test de soumission sans fichier"""
        # Mock form submission
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.form_submit_button.side_effect = [True, False]  # submitted=True, cancel=False
        mock_st.file_uploader.return_value = None  # No file
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_upload_document_form(1)

        mock_st.error.assert_called_with("❌ Veuillez sélectionner un fichier")
        mock_upload.assert_not_called()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.os.makedirs')
    @patch('app.pages_modules.consultant_documents.DocumentAnalyzer')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_upload_document_success(self, mock_session, mock_analyzer, mock_makedirs, mock_st):
        """Test d'upload de document réussi"""
        # Mock file
        mock_file = MagicMock()
        mock_file.name = "test.pdf"
        mock_file.getbuffer.return_value = b"test content"
        mock_file.type = "application/pdf"

        # Mock analyzer
        mock_analyzer.extract_text_from_file.return_value = "extracted text"
        mock_analyzer.analyze_cv_content.return_value = {"test": "analysis"}

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {
            "file": mock_file,
            "type_document": "CV",
            "description": "Test CV"
        }

        with patch('builtins.open', mock_open()):
            result = upload_document(1, data)

        assert result is True
        mock_session_instance.add.assert_called_once()
        mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_upload_document_error(self, mock_session, mock_st):
        """Test d'upload avec erreur"""
        # Mock session to raise exception
        mock_session.return_value.__enter__.side_effect = Exception("DB Error")

        mock_file = MagicMock()
        data = {"file": mock_file, "type_document": "CV", "description": ""}

        result = upload_document(1, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Erreur lors de l'upload: DB Error")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_analyze_consultant_cv_no_cv_found(self, mock_session, mock_st):
        """Test d'analyse CV quand aucun CV n'est trouvé"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = None  # No CV found

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        mock_consultant = MagicMock()
        mock_consultant.id = 1

        analyze_consultant_cv(mock_consultant)

        mock_st.warning.assert_called_with("⚠️ Aucun CV trouvé pour ce consultant")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.is_grok_available')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_analyze_consultant_cv_with_cv_no_grok(self, mock_session, mock_is_grok, mock_st):
        """Test d'analyse CV avec CV trouvé mais pas de Grok"""
        mock_is_grok.return_value = False

        # Mock CV document
        mock_cv = MagicMock()
        mock_cv.analyse_cv = None

        # Mock session
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = mock_cv

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        mock_consultant = MagicMock()
        mock_consultant.id = 1

        analyze_consultant_cv(mock_consultant)

        mock_st.markdown.assert_any_call("### 🔍 Analyse du CV")
        mock_st.selectbox.assert_called_with(
            "Choisissez la méthode d'analyse :",
            options=["🔍 Analyse classique"],
            index=0,
            help="OpenAI GPT-4 offre une analyse plus précise et détaillée"
        )

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.perform_cv_analysis')
    @patch('app.pages_modules.consultant_documents.is_grok_available')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_analyze_consultant_cv_start_analysis(self, mock_session, mock_is_grok, mock_perform, mock_st):
        """Test du démarrage de l'analyse CV"""
        mock_is_grok.return_value = True
        mock_perform.return_value = True

        # Mock CV document
        mock_cv = MagicMock()
        mock_cv.analyse_cv = None

        # Mock session
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = mock_cv

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock button click
        mock_st.button.return_value = True

        analyze_consultant_cv(mock_consultant)

        mock_perform.assert_called_once()
        mock_st.success.assert_called_with("✅ Analyse terminée avec succès !")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.DocumentAnalyzer')
    @patch('app.pages_modules.consultant_documents.get_grok_service')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_perform_cv_analysis_grok_method(self, mock_session, mock_grok, mock_analyzer, mock_st):
        """Test d'analyse CV avec méthode Grok"""
        # Mock file existence
        with patch('os.path.exists', return_value=True):
            # Mock text extraction
            mock_analyzer.extract_text_from_file.return_value = "test cv content"

            # Mock Grok service
            mock_grok_service = MagicMock()
            mock_grok_service.analyze_cv.return_value = {"test": "analysis"}
            mock_grok_service.get_cost_estimate.return_value = 0.05
            mock_grok.return_value = mock_grok_service

            # Mock document and consultant
            mock_cv_doc = MagicMock()
            mock_cv_doc.chemin_fichier = "/path/to/cv.pdf"

            mock_consultant = MagicMock()
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"

            # Mock session
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance

            result = perform_cv_analysis(mock_cv_doc, mock_consultant, "🤖 IA avec GPT-4")

            assert result is True
            mock_grok_service.analyze_cv.assert_called_once_with("test cv content")
            mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.DocumentAnalyzer')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_perform_cv_analysis_classic_method(self, mock_session, mock_analyzer, mock_st):
        """Test d'analyse CV avec méthode classique"""
        # Mock file existence
        with patch('os.path.exists', return_value=True):
            # Mock text extraction
            mock_analyzer.extract_text_from_file.return_value = "test cv content"
            mock_analyzer.analyze_cv_content.return_value = {"test": "classic_analysis"}

            # Mock document and consultant
            mock_cv_doc = MagicMock()
            mock_cv_doc.chemin_fichier = "/path/to/cv.pdf"

            mock_consultant = MagicMock()
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"

            # Mock session
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance

            result = perform_cv_analysis(mock_cv_doc, mock_consultant, "🔍 Analyse classique")

            assert result is True
            mock_analyzer.analyze_cv_content.assert_called_once_with("test cv content", "Jean Dupont")
            mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    def test_perform_cv_analysis_file_not_found(self, mock_st):
        """Test d'analyse CV quand le fichier n'existe pas"""
        with patch('os.path.exists', return_value=False):
            mock_cv_doc = MagicMock()
            mock_cv_doc.chemin_fichier = "/path/to/missing.pdf"

            result = perform_cv_analysis(mock_cv_doc, MagicMock(), "test method")

            assert result is False
            mock_st.error.assert_called_with("❌ Fichier CV introuvable")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents._display_cv_resume')
    @patch('app.pages_modules.consultant_documents._display_cv_missions')
    @patch('app.pages_modules.consultant_documents._display_cv_competences')
    @patch('app.pages_modules.consultant_documents._display_cv_contact')
    @patch('app.pages_modules.consultant_documents._display_cv_actions')
    def test_show_full_cv_analysis_complete(self, mock_actions, mock_contact, mock_competences,
                                          mock_missions, mock_resume, mock_st):
        """Test d'affichage complet de l'analyse CV"""
        analysis = {
            "resume": "Test resume",
            "missions": [{"titre": "Test mission"}],
            "competences": ["Python", "SQL"],
            "contact": {"email": "test@test.com"}
        }

        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        show_full_cv_analysis(analysis, "cv.pdf", mock_consultant)

        mock_st.markdown.assert_any_call("### 🔍 Analyse complète du CV : cv.pdf")
        mock_resume.assert_called_once_with(analysis)
        mock_missions.assert_called_once_with(analysis)
        mock_competences.assert_called_once_with(analysis)
        mock_contact.assert_called_once_with(analysis)
        mock_actions.assert_called_once_with(analysis, mock_consultant)

    @patch('app.pages_modules.consultant_documents.st')
    def test_show_documents_report_no_documents(self, mock_st):
        """Test du rapport de documents sans documents"""
        show_documents_report([])

        mock_st.info.assert_called_with("ℹ️ Aucun document à analyser")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('pandas.DataFrame')
    def test_show_documents_report_with_documents(self, mock_df, mock_st):
        """Test du rapport de documents avec documents"""
        # Mock documents
        mock_doc1 = MagicMock()
        mock_doc1.nom_fichier = "cv.pdf"
        mock_doc1.type_document = "CV"
        mock_doc1.taille_fichier = 1024000
        mock_doc1.date_upload = datetime.now()
        mock_doc1.analyse_cv = '{"test": "data"}'

        mock_doc2 = MagicMock()
        mock_doc2.nom_fichier = "diplome.pdf"
        mock_doc2.type_document = "Diplôme"
        mock_doc2.taille_fichier = 512000
        mock_doc2.date_upload = datetime.now()
        mock_doc2.analyse_cv = None

        documents = [mock_doc1, mock_doc2]

        show_documents_report(documents)

        mock_st.markdown.assert_any_call("### 📊 Rapport des documents")
        mock_st.dataframe.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('builtins.open', new_callable=mock_open, read_data=b"test content")
    @patch('os.path.exists')
    def test_download_document_success(self, mock_exists, mock_file, mock_st):
        """Test de téléchargement de document réussi"""
        mock_exists.return_value = True

        mock_document = MagicMock()
        mock_document.chemin_fichier = "/path/to/document.pdf"
        mock_document.nom_fichier = "document.pdf"
        mock_document.mimetype = "application/pdf"

        download_document(mock_document)

        mock_st.download_button.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('os.path.exists')
    def test_download_document_file_not_found(self, mock_exists, mock_st):
        """Test de téléchargement quand le fichier n'existe pas"""
        mock_exists.return_value = False

        mock_document = MagicMock()
        mock_document.chemin_fichier = "/path/to/missing.pdf"

        download_document(mock_document)

        mock_st.error.assert_called_with("❌ Fichier introuvable sur le serveur")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.DocumentAnalyzer')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_reanalyze_document_success(self, mock_session, mock_analyzer, mock_st):
        """Test de réanalyse de document réussie"""
        # Mock analyzer
        mock_analyzer.extract_text_from_file.return_value = "new content"
        mock_analyzer.analyze_cv_content.return_value = {"new": "analysis"}

        # Mock document
        mock_document = MagicMock()
        mock_document.chemin_fichier = "/path/to/document.pdf"

        # Mock session
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_document

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        mock_consultant = MagicMock()

        with patch('os.path.exists', return_value=True):
            result = reanalyze_document(1, mock_consultant)

        assert result is True
        mock_st.success.assert_called_with("✅ Document réanalysé avec succès !")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_reanalyze_document_not_found(self, mock_session, mock_st):
        """Test de réanalyse de document non trouvé"""
        # Mock session - document not found
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        result = reanalyze_document(999, MagicMock())

        assert result is False
        mock_st.error.assert_called_with("❌ Document introuvable")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_rename_document_success(self, mock_session, mock_st):
        """Test de renommage de document réussi"""
        # Mock document
        mock_document = MagicMock()

        # Mock session
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_document

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {"new_name": "new_name.pdf", "new_description": "New description"}

        result = rename_document(1, data)

        assert result is True
        assert mock_document.nom_fichier == "new_name.pdf"
        assert mock_document.description == "New description"
        mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('os.remove')
    @patch('os.path.exists')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_delete_document_success(self, mock_session, mock_exists, mock_remove, mock_st):
        """Test de suppression de document réussie"""
        mock_exists.return_value = True

        # Mock document
        mock_document = MagicMock()
        mock_document.chemin_fichier = "/path/to/document.pdf"

        # Mock session
        mock_session_instance = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_document

        mock_session_instance.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session_instance

        result = delete_document(1)

        assert result is True
        mock_remove.assert_called_once_with("/path/to/document.pdf")
        mock_session_instance.delete.assert_called_once_with(mock_document)
        mock_session_instance.commit.assert_called_once()
        mock_st.info.assert_called_with("✅ Document supprimé")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents._load_document_for_rename')
    @patch('app.pages_modules.consultant_documents.get_database_session')
    def test_show_rename_document_form_display(self, mock_session, mock_load, mock_st):
        """Test d'affichage du formulaire de renommage"""
        # Mock document
        mock_document = MagicMock()
        mock_document.nom_fichier = "old_name.pdf"
        mock_document.description = "Old description"
        mock_load.return_value = mock_document

        # Mock form
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_rename_document_form(1)

        mock_st.markdown.assert_any_call("### ✏️ Renommer un document")

    @patch('app.pages_modules.consultant_documents.st')
    def test_generate_cv_report_success(self, mock_st):
        """Test de génération de rapport CV réussi"""
        analysis = {
            "resume": "Test resume",
            "missions": [{"titre": "Mission 1", "client": "Client A", "periode": "2023", "description": "Test"}],
            "competences": ["Python", "SQL"]
        }

        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        generate_cv_report(analysis, mock_consultant)

        mock_st.download_button.assert_called_once()
        mock_st.success.assert_called_with("✅ Rapport généré avec succès !")

    # Tests pour les fonctions helper de show_document_details

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_document_basic_info(self, mock_st):
        """Test d'affichage des informations de base du document"""
        from app.pages_modules.consultant_documents import _display_document_basic_info

        mock_document = MagicMock()
        mock_document.nom_fichier = "test.pdf"
        mock_document.type_document = "CV"
        mock_document.taille_fichier = 1024000
        mock_document.date_upload = datetime(2023, 1, 1, 12, 0)

        _display_document_basic_info(mock_document)

        mock_st.markdown.assert_called_with("**📄 Informations**")
        mock_st.write.assert_any_call("**Nom :** test.pdf")
        mock_st.write.assert_any_call("**Type :** CV")
        mock_st.write.assert_any_call("**Upload :** 01/01/2023 12:00")

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_document_metadata(self, mock_st):
        """Test d'affichage des métadonnées du document"""
        from app.pages_modules.consultant_documents import _display_document_metadata

        mock_document = MagicMock()
        mock_document.mimetype = "application/pdf"
        mock_document.chemin_fichier = "/path/to/file.pdf"
        mock_document.analyse_cv = '{"test": "data"}'

        _display_document_metadata(mock_document)

        mock_st.markdown.assert_called_with("**📊 Métadonnées**")
        mock_st.write.assert_any_call("**Analyse CV :** ✅ Disponible")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.show_full_cv_analysis')
    def test_display_cv_analysis_summary_with_analysis(self, mock_show_full, mock_st):
        """Test d'affichage du résumé d'analyse CV quand disponible"""
        from app.pages_modules.consultant_documents import _display_cv_analysis_summary

        mock_document = MagicMock()
        mock_document.id = 1
        mock_document.analyse_cv = '{"missions": [{"titre": "Mission 1"}], "competences": ["Python", "SQL"]}'

        mock_consultant = MagicMock()

        # Mock button click
        mock_st.button.return_value = True

        _display_cv_analysis_summary(mock_document, mock_consultant)

        mock_st.markdown.assert_called_with("**🔍 Analyse CV**")
        mock_st.write.assert_any_call("**Missions détectées :** 1")
        mock_st.write.assert_any_call("**Compétences détectées :** 2")
        mock_show_full.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_cv_analysis_summary_no_analysis(self, mock_st):
        """Test d'affichage du résumé d'analyse CV quand non disponible"""
        from app.pages_modules.consultant_documents import _display_cv_analysis_summary

        mock_document = MagicMock()
        mock_document.analyse_cv = None

        _display_cv_analysis_summary(mock_document, MagicMock())

        # Should not display anything
        mock_st.markdown.assert_not_called()

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.download_document')
    @patch('app.pages_modules.consultant_documents.reanalyze_document')
    def test_display_document_actions(self, mock_reanalyze, mock_download, mock_st):
        """Test d'affichage des actions sur le document"""
        from app.pages_modules.consultant_documents import _display_document_actions

        mock_document = MagicMock()
        mock_document.id = 1

        mock_consultant = MagicMock()

        # Mock columns and buttons
        mock_col1, mock_col2, mock_col3, mock_col4 = MagicMock(), MagicMock(), MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]
        mock_st.button.return_value = False  # No button clicked

        _display_document_actions(mock_document, mock_consultant)

        # Should create 4 columns
        mock_st.columns.assert_called_with(4)
        # Should have 4 button calls
        assert mock_st.button.call_count == 4

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.show_rename_document_form')
    def test_handle_rename_form_active(self, mock_show_form, mock_st):
        """Test de gestion du formulaire de renommage quand activé"""
        from app.pages_modules.consultant_documents import _handle_rename_form

        mock_document = MagicMock()
        mock_document.id = 1

        # Mock session state to have rename active
        with patch('app.pages_modules.consultant_documents.st.session_state', {'rename_document': 1}):
            _handle_rename_form(mock_document)

        mock_show_form.assert_called_once_with(1)

    @patch('app.pages_modules.consultant_documents.st')
    def test_handle_rename_form_inactive(self, mock_st):
        """Test de gestion du formulaire de renommage quand inactif"""
        from app.pages_modules.consultant_documents import _handle_rename_form

        mock_document = MagicMock()
        mock_document.id = 1

        # Mock session state without rename
        with patch('app.pages_modules.consultant_documents.st.session_state', {}):
            _handle_rename_form(mock_document)

        # Should not show form
        mock_st.markdown.assert_not_called()

    # Tests pour les fonctions d'affichage d'analyse CV

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_cv_resume(self, mock_st):
        """Test d'affichage du résumé CV"""
        from app.pages_modules.consultant_documents import _display_cv_resume

        analysis = {"resume": "This is a test resume"}

        _display_cv_resume(analysis)

        mock_st.markdown.assert_called_with("#### 📋 Résumé")
        mock_st.write.assert_called_with("This is a test resume")

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_cv_missions(self, mock_st):
        """Test d'affichage des missions CV"""
        from app.pages_modules.consultant_documents import _display_cv_missions

        analysis = {
            "missions": [
                {"titre": "Developer", "client": "Company A", "periode": "2020-2023", "description": "Dev work"}
            ]
        }

        _display_cv_missions(analysis)

        mock_st.markdown.assert_called_with("#### 🚀 Missions détectées")
        mock_st.expander.assert_called_once()

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_cv_competences(self, mock_st):
        """Test d'affichage des compétences CV"""
        from app.pages_modules.consultant_documents import _display_cv_competences

        analysis = {"competences": ["Python", "SQL", "JavaScript"]}

        _display_cv_competences(analysis)

        mock_st.markdown.assert_called_with("#### 🛠️ Compétences détectées")
        mock_st.write.assert_any_call("• Python")
        mock_st.write.assert_any_call("• SQL")
        mock_st.write.assert_any_call("• JavaScript")

    @patch('app.pages_modules.consultant_documents.st')
    def test_display_cv_contact(self, mock_st):
        """Test d'affichage des informations de contact CV"""
        from app.pages_modules.consultant_documents import _display_cv_contact

        analysis = {
            "contact": {
                "email": "test@test.com",
                "telephone": "0123456789"
            }
        }

        _display_cv_contact(analysis)

        mock_st.markdown.assert_called_with("#### 📞 Informations de contact")
        mock_st.write.assert_any_call("**Email :** test@test.com")
        mock_st.write.assert_any_call("**Téléphone :** 0123456789")

    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.generate_cv_report')
    def test_display_cv_actions(self, mock_generate, mock_st):
        """Test d'affichage des actions sur l'analyse CV"""
        from app.pages_modules.consultant_documents import _display_cv_actions

        analysis = {"test": "data"}
        mock_consultant = MagicMock()

        # Mock columns and buttons
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]
        mock_st.button.return_value = False  # No button clicked

        _display_cv_actions(analysis, mock_consultant)

        mock_st.columns.assert_called_with(2)
        assert mock_st.button.call_count == 2


if __name__ == "__main__":
    import unittest
    unittest.main()</content>

if __name__ == "__main__":
    import unittest
    unittest.main()
