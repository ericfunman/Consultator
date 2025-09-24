"""
Tests de couverture complète pour documents_functions.py
Visant 90%+ de couverture pour améliorer le score global
"""

from unittest.mock import MagicMock, patch, mock_open
import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import os

from app.pages_modules.documents_functions import (
    show_consultant_documents,
    save_consultant_document,
    _get_file_size_display,
    _extract_document_type,
    _render_document_metrics,
    _render_document_actions,
    show_existing_documents,
    delete_consultant_document
)


class TestShowConsultantDocuments:
    """Tests pour show_consultant_documents"""
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.save_consultant_document')
    @patch('app.pages_modules.documents_functions.show_existing_documents')
    def test_show_consultant_documents_complete_flow(self, mock_show_existing, mock_save_doc, mock_st):
        """Test du flux complet d'affichage des documents"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        # Mock file upload
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.name = "cv.pdf"
        mock_uploaded_file.size = 1048576  # 1MB
        mock_uploaded_file.getbuffer.return_value = b"fake_pdf_content"
        
        # Mock Streamlit components - Need 2 different column calls
        mock_st.file_uploader.return_value = mock_uploaded_file
        mock_st.selectbox.return_value = "CV"
        mock_st.text_area.return_value = "CV principal"
        mock_st.columns.side_effect = [
            [MagicMock(), MagicMock(), MagicMock()],  # First call: 3 columns for metrics
            [MagicMock(), MagicMock()]                # Second call: 2 columns for buttons
        ]
        mock_st.button.return_value = True  # Save button clicked
        
        show_consultant_documents(mock_consultant)
        
        # Verify calls
        mock_st.subheader.assert_called_once()
        mock_st.file_uploader.assert_called_once()
        mock_show_existing.assert_called_once_with(mock_consultant)
        mock_save_doc.assert_called_once()
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.show_existing_documents')
    def test_show_consultant_documents_no_file(self, mock_show_existing, mock_st):
        """Test sans fichier uploadé"""
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        # No file uploaded
        mock_st.file_uploader.return_value = None
        
        show_consultant_documents(mock_consultant)
        
        mock_st.subheader.assert_called_once()
        mock_show_existing.assert_called_once()
        # Metrics should not be called if no file
        mock_st.metric.assert_not_called()
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.show_existing_documents')
    def test_show_consultant_documents_large_file(self, mock_show_existing, mock_st):
        """Test avec un gros fichier"""
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        # Large file (2MB)
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.name = "large_document.pdf"
        mock_uploaded_file.size = 2097152  # 2MB
        
        mock_st.file_uploader.return_value = mock_uploaded_file
        mock_st.columns.side_effect = [
            [MagicMock(), MagicMock(), MagicMock()],  # First call: 3 columns for metrics
            [MagicMock(), MagicMock()]                # Second call: 2 columns for buttons  
        ]
        
        show_consultant_documents(mock_consultant)
        
        # Verify MB display is used for large files
        mock_st.metric.assert_called()
        # Check that metrics were called for name, size, and type selection
        assert mock_st.metric.call_count >= 2


class TestSaveConsultantDocument:
    """Tests pour save_consultant_document"""
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    @patch('builtins.open', new_callable=mock_open)
    @patch('app.pages_modules.documents_functions.datetime')
    def test_save_consultant_document_success(self, mock_datetime, mock_file_open, mock_doc_service, mock_st):
        """Test sauvegarde réussie"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = "20240115_120000"
        mock_doc_service.init_upload_directory.return_value = Path("/fake/upload/dir")
        mock_doc_service.is_allowed_file.return_value = True
        mock_doc_service.get_file_extension.return_value = "pdf"
        mock_st.button.return_value = False  # Button not clicked
        
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.name = "test.pdf"
        mock_uploaded_file.getbuffer.return_value = b"fake_pdf_content"
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Description")
        
        # Verify success
        mock_st.success.assert_called_once()
        mock_st.info.assert_called_once()
        mock_st.rerun.assert_called_once()
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    def test_save_consultant_document_invalid_file(self, mock_doc_service, mock_st):
        """Test avec fichier invalide"""
        mock_doc_service.init_upload_directory.return_value = Path("/fake/upload/dir")
        mock_doc_service.is_allowed_file.return_value = False
        
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.name = "test.exe"
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Description")
        
        mock_st.error.assert_called_with(" Type de fichier non supporte")
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    def test_save_consultant_document_cv_analysis(self, mock_doc_service, mock_st):
        """Test proposition d'analyse pour un CV"""
        # Setup mocks for successful save
        mock_doc_service.init_upload_directory.return_value = Path("/fake/upload/dir")
        mock_doc_service.is_allowed_file.return_value = True
        mock_doc_service.get_file_extension.return_value = "pdf"
        
        with patch('app.pages_modules.documents_functions.datetime') as mock_datetime, \
             patch('builtins.open', mock_open()):
            
            mock_datetime.now.return_value.strftime.return_value = "20240115_120000"
            mock_st.button.return_value = True  # Analysis button clicked
            
            mock_uploaded_file = MagicMock()
            mock_uploaded_file.name = "cv.pdf"
            mock_uploaded_file.getbuffer.return_value = b"fake_pdf_content"
            
            mock_consultant = MagicMock()
            mock_consultant.prenom = "Jean"
            mock_consultant.nom = "Dupont"
            
            save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Description")
            
            # Verify CV analysis button is shown and clicked
            mock_st.button.assert_called()
            mock_st.info.assert_called()  # Analysis info shown
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_consultant_document_exception(self, mock_file_open, mock_doc_service, mock_st):
        """Test gestion d'exception"""
        mock_doc_service.init_upload_directory.return_value = Path("/fake/upload/dir")
        mock_doc_service.is_allowed_file.return_value = True
        mock_doc_service.get_file_extension.return_value = "pdf"
        
        # Force an exception
        mock_file_open.side_effect = Exception("Disk full")
        
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.name = "test.pdf"
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        save_consultant_document(mock_uploaded_file, mock_consultant, "CV", "Description")
        
        # Should catch exception and show error
        mock_st.error.assert_called()


class TestFileSizeDisplay:
    """Tests pour _get_file_size_display"""
    
    def test_get_file_size_kb(self):
        """Test affichage taille en KB"""
        result = _get_file_size_display(512)
        assert result == "0.5 KB"
        
        result = _get_file_size_display(1536)
        assert result == "1.5 KB"
    
    def test_get_file_size_mb(self):
        """Test affichage taille en MB"""
        result = _get_file_size_display(1048576)  # 1MB
        assert result == "1.0 MB"
        
        result = _get_file_size_display(2621440)  # 2.5MB
        assert result == "2.5 MB"


class TestExtractDocumentType:
    """Tests pour _extract_document_type"""
    
    def test_extract_cv_type(self):
        """Test extraction type CV"""
        result = _extract_document_type("Jean_Dupont_CV_20240115_120000.pdf")
        assert result == "CV"
    
    def test_extract_lettre_motivation_type(self):
        """Test extraction type lettre de motivation"""
        result = _extract_document_type("Jean_Dupont_Lettre_de_motivation_20240115_120000.docx")
        assert result == "Lettre de motivation"
    
    def test_extract_certificat_type(self):
        """Test extraction type certificat"""
        result = _extract_document_type("Jean_Dupont_Certificat_20240115_120000.pdf")
        assert result == "Certificat"
    
    def test_extract_unknown_type(self):
        """Test type inconnu"""
        result = _extract_document_type("Jean_Dupont_Document_20240115_120000.pdf")
        assert result == "Inconnu"


class TestRenderDocumentMetrics:
    """Tests pour _render_document_metrics"""
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.datetime')
    def test_render_document_metrics(self, mock_datetime, mock_st):
        """Test affichage des métriques"""
        # Mock file stats
        mock_file_stats = MagicMock()
        mock_file_stats.st_size = 1048576  # 1MB
        mock_file_stats.st_mtime = 1705320000  # timestamp
        
        # Mock datetime
        mock_datetime.fromtimestamp.return_value.strftime.return_value = "15/01/2024"
        
        # Mock columns
        mock_cols = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        
        result = _render_document_metrics(mock_file_stats, "CV")
        
        # Verify metrics were called
        mock_st.metric.assert_called()
        assert mock_st.metric.call_count == 3  # Size, Date, Type
        assert result == mock_cols[3]  # Should return col4


class TestRenderDocumentActions:
    """Tests pour _render_document_actions"""
    
    @patch('app.pages_modules.documents_functions.st')
    def test_render_document_actions_cv(self, mock_st):
        """Test actions pour un CV"""
        mock_file_path = MagicMock()
        mock_file_path.name = "cv.pdf"
        
        mock_cols = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        mock_st.button.side_effect = [True, False, False]  # Analyze clicked
        
        _render_document_actions(mock_file_path, "CV")
        
        # Verify analyze button for CV and info shown
        assert mock_st.button.call_count == 3
        mock_st.info.assert_called_with("🔍 Analyse de CV en cours de developpement...")
    
    @patch('app.pages_modules.documents_functions.st')
    def test_render_document_actions_download(self, mock_st):
        """Test action télécharger"""
        mock_file_path = MagicMock()
        mock_file_path.name = "document.pdf"
        
        mock_cols = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        mock_st.button.side_effect = [True, False]  # Download clicked
        
        _render_document_actions(mock_file_path, "Certificat")
        
        mock_st.info.assert_called_with("⬇️ Telechargement en cours de developpement...")
    
    @patch('app.pages_modules.documents_functions.st')
    def test_render_document_actions_preview(self, mock_st):
        """Test action prévisualiser"""
        mock_file_path = MagicMock()
        mock_file_path.name = "document.pdf"
        
        mock_cols = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        mock_st.button.side_effect = [False, True]  # Preview clicked
        
        _render_document_actions(mock_file_path, "Contrat")
        
        mock_st.info.assert_called_with("👁️ Previsualisation en cours de developpement...")


class TestShowExistingDocuments:
    """Tests pour show_existing_documents"""
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    @patch('app.pages_modules.documents_functions._render_document_metrics')
    @patch('app.pages_modules.documents_functions._render_document_actions')
    @patch('app.pages_modules.documents_functions.delete_consultant_document')
    def test_show_existing_documents_with_files(self, mock_delete, mock_render_actions, 
                                                mock_render_metrics, mock_doc_service, mock_st):
        """Test avec des fichiers existants"""
        # Mock upload directory and files
        mock_upload_dir = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.name = "Jean_Dupont_CV_20240115_120000.pdf"
        mock_file1.stat.return_value.st_mtime = 1705320000
        
        mock_file2 = MagicMock()
        mock_file2.name = "Jean_Dupont_Certificat_20240120_130000.pdf"
        mock_file2.stat.return_value.st_mtime = 1705752000
        
        # Sort by modification time (most recent first)
        mock_upload_dir.glob.return_value = [mock_file1, mock_file2]
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        
        # Mock columns and metrics return
        mock_render_metrics.return_value = MagicMock()  # col4 for delete button
        mock_cols = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        mock_st.button.side_effect = [True, False]  # Delete first file
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        show_existing_documents(mock_consultant)
        
        # Verify display
        mock_st.subheader.assert_called_once()
        mock_st.expander.assert_called()  # Called for each file
        mock_delete.assert_called_once()  # Delete called for first file
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    def test_show_existing_documents_no_files(self, mock_doc_service, mock_st):
        """Test sans fichiers"""
        mock_upload_dir = MagicMock()
        mock_upload_dir.glob.return_value = []  # No files
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        show_existing_documents(mock_consultant)
        
        mock_st.info.assert_called_with("📄 Aucun document trouve pour ce consultant")
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    def test_show_existing_documents_exception(self, mock_doc_service, mock_st):
        """Test gestion d'exception"""
        mock_doc_service.init_upload_directory.side_effect = Exception("Directory error")
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        show_existing_documents(mock_consultant)
        
        mock_st.error.assert_called()


class TestDeleteConsultantDocument:
    """Tests pour delete_consultant_document"""
    
    @patch('app.pages_modules.documents_functions.st')
    def test_delete_consultant_document_success(self, mock_st):
        """Test suppression réussie"""
        mock_file_path = MagicMock()
        mock_file_path.exists.return_value = True
        
        delete_consultant_document(mock_file_path)
        
        mock_file_path.unlink.assert_called_once()
        mock_st.success.assert_called_with(" Document supprime avec succes")
        mock_st.rerun.assert_called_once()
    
    @patch('app.pages_modules.documents_functions.st')
    def test_delete_consultant_document_not_found(self, mock_st):
        """Test fichier non trouvé"""
        mock_file_path = MagicMock()
        mock_file_path.exists.return_value = False
        
        delete_consultant_document(mock_file_path)
        
        mock_file_path.unlink.assert_not_called()
        mock_st.error.assert_called_with(" Fichier introuvable")
    
    @patch('app.pages_modules.documents_functions.st')
    def test_delete_consultant_document_exception(self, mock_st):
        """Test gestion d'exception"""
        mock_file_path = MagicMock()
        mock_file_path.exists.return_value = True
        mock_file_path.unlink.side_effect = Exception("Permission denied")
        
        delete_consultant_document(mock_file_path)
        
        mock_st.error.assert_called()


class TestDocumentUtilityFunctions:
    """Tests pour les fonctions utilitaires additionnelles"""
    
    def test_file_size_edge_cases(self):
        """Test cas limites pour la taille de fichier"""
        # Exactly 1024 bytes -> should be 1.0 KB
        result = _get_file_size_display(1024)
        assert result == "1.0 KB"
        
        # Exactly 1024*1024 bytes -> should be 1.0 MB (not 1024.0 KB)
        result = _get_file_size_display(1024 * 1024)
        assert result == "1.0 MB"
    
    def test_document_type_all_types(self):
        """Test tous les types de documents"""
        test_cases = [
            ("Jean_Dupont_CV_20240115.pdf", "CV"),
            ("Jean_Dupont_Lettre_de_motivation_20240115.docx", "Lettre de motivation"),
            ("Jean_Dupont_Certificat_20240115.pdf", "Certificat"),
            ("Jean_Dupont_Contrat_20240115.pdf", "Contrat"),
            ("Jean_Dupont_Autre_20240115.txt", "Autre"),
            ("random_file_name.pdf", "Inconnu")
        ]
        
        for filename, expected_type in test_cases:
            result = _extract_document_type(filename)
            assert result == expected_type, f"Failed for {filename}"


class TestIntegrationScenarios:
    """Tests de scénarios d'intégration"""
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService')
    @patch('app.pages_modules.documents_functions.show_existing_documents')
    def test_full_upload_workflow(self, mock_show_existing, mock_doc_service, mock_st):
        """Test du workflow complet d'upload"""
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        # Simulate file upload workflow
        mock_uploaded_file = MagicMock()
        mock_uploaded_file.name = "cv.pdf"
        mock_uploaded_file.size = 1024
        
        # Mock the complete flow
        mock_st.file_uploader.return_value = mock_uploaded_file
        mock_st.selectbox.return_value = "CV"
        mock_st.text_area.return_value = "Mon CV principal"
        mock_st.columns.side_effect = [
            [MagicMock(), MagicMock(), MagicMock()],  # 3 columns for file info
            [MagicMock(), MagicMock()]  # 2 columns for buttons
        ]
        mock_st.button.side_effect = [True, False, False]  # Save clicked, Cancel not, Analyze not
        
        # Mock the save function components
        mock_doc_service.init_upload_directory.return_value = Path("/uploads")
        mock_doc_service.is_allowed_file.return_value = True
        mock_doc_service.get_file_extension.return_value = "pdf"
        
        with patch('builtins.open', mock_open()), \
             patch('app.pages_modules.documents_functions.datetime') as mock_dt:
            
            mock_dt.now.return_value.strftime.return_value = "20240115_120000"
            
            show_consultant_documents(mock_consultant)
            
            # Verify the complete workflow
            mock_st.file_uploader.assert_called_once()
            mock_st.selectbox.assert_called_once()
            mock_st.text_area.assert_called_once()
            mock_show_existing.assert_called_once_with(mock_consultant)
    
    @patch('app.pages_modules.documents_functions.st')
    @patch('app.pages_modules.documents_functions.DocumentService') 
    def test_document_listing_and_actions(self, mock_doc_service, mock_st):
        """Test listage et actions sur documents"""
        # Setup multiple files with different types
        mock_upload_dir = MagicMock()
        files = []
        for i, doc_type in enumerate(["CV", "Certificat", "Contrat"]):
            mock_file = MagicMock()
            mock_file.name = f"Jean_Dupont_{doc_type}_2024011{i+5}_120000.pdf"
            mock_file.stat.return_value.st_mtime = 1705320000 + i*1000
            mock_file.stat.return_value.st_size = (i+1) * 1024
            files.append(mock_file)
        
        mock_upload_dir.glob.return_value = files
        mock_doc_service.init_upload_directory.return_value = mock_upload_dir
        
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        # Mock UI interactions
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]
        mock_st.button.return_value = False  # No actions clicked
        
        show_existing_documents(mock_consultant)
        
        # Should show subheader with count
        mock_st.subheader.assert_called()
        # Should create expander for each file (at least one)
        mock_st.expander.assert_called()