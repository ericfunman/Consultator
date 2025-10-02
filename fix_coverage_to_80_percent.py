#!/usr/bin/env python3
"""
Script pour améliorer la couverture de tests de 76% vers 80%+
Focus sur les corrections critiques et nouveaux tests ciblés
"""

import os
import sys
from pathlib import Path

def fix_pandas_mock_issues():
    """Corrige les problèmes de mocking avec pandas dans les tests"""
    
    # Correction des tests home qui échouent avec pandas DataFrame
    home_test_fixes = {
        "tests/unit/pages_modules/test_home_mega_coverage.py": [
            {
                "old": """from app.pages_modules.home import show_dashboard_charts
        show_dashboard_charts()""",
                "new": """with patch('app.pages_modules.home.pd.DataFrame') as mock_df, \\
             patch('app.pages_modules.home.pd.date_range') as mock_date_range, \\
             patch('app.pages_modules.home.px.line') as mock_px_line:
            
            mock_date_range.return_value = ["2024-01", "2024-02", "2024-03"]
            mock_df.return_value = MagicMock()
            mock_px_line.return_value = MagicMock()
            
            from app.pages_modules.home import show_dashboard_charts
            show_dashboard_charts()"""
            }
        ],
        "tests/unit/pages_modules/test_home_realistic.py": [
            {
                "old": """from app.pages_modules.home import show_dashboard_charts
        show_dashboard_charts()""",
                "new": """with patch('app.pages_modules.home.pd.DataFrame') as mock_df, \\
             patch('app.pages_modules.home.pd.date_range') as mock_date_range:
            
            mock_date_range.return_value = ["2024-01", "2024-02", "2024-03"]
            mock_df.return_value = MagicMock()
            
            from app.pages_modules.home import show_dashboard_charts
            show_dashboard_charts()"""
            }
        ]
    }
    
    return home_test_fixes

def create_targeted_coverage_tests():
    """Crée des tests ciblés pour les modules avec la plus faible couverture"""
    
    # Tests pour business_manager_service (48% -> 70%+)
    business_manager_tests = '''
"""
Tests ciblés pour business_manager_service - Amélioration couverture 48% -> 70%+
"""
import unittest
from unittest.mock import patch, MagicMock
from app.services.business_manager_service import BusinessManagerService

class TestBusinessManagerServiceCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture de business_manager_service"""
    
    def setUp(self):
        self.service = BusinessManagerService()
    
    @patch('app.services.business_manager_service.get_database_session')
    def test_get_all_business_managers(self, mock_session):
        """Test get_all_business_managers()"""
        mock_session.return_value.__enter__.return_value.query.return_value.all.return_value = []
        result = self.service.get_all_business_managers()
        self.assertEqual(result, [])
    
    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_manager_by_id(self, mock_session):
        """Test get_business_manager_by_id()"""
        mock_bm = MagicMock()
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.first.return_value = mock_bm
        result = self.service.get_business_manager_by_id(1)
        self.assertEqual(result, mock_bm)
    
    @patch('app.services.business_manager_service.get_database_session')
    def test_create_business_manager(self, mock_session):
        """Test create_business_manager()"""
        mock_session_obj = mock_session.return_value.__enter__.return_value
        data = {"nom_complet": "Test Manager", "email": "test@test.com"}
        
        result = self.service.create_business_manager(data)
        
        mock_session_obj.add.assert_called_once()
        mock_session_obj.commit.assert_called_once()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
'''
    
    # Tests pour consultant_documents (54% -> 70%+)
    consultant_documents_tests = '''
"""
Tests ciblés pour consultant_documents - Amélioration couverture 54% -> 70%+
"""
import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

class TestConsultantDocumentsCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture de consultant_documents"""
    
    @patch('app.pages_modules.consultant_documents.st')
    @patch('app.pages_modules.consultant_documents.imports_ok', True)
    def test_show_basic(self, mock_st):
        """Test de la fonction show() de base"""
        mock_st.title.return_value = None
        mock_st.session_state = {}
        
        from app.pages_modules.consultant_documents import show
        show()
        
        mock_st.title.assert_called_once_with("📁 Documents consultant")
    
    @patch('app.pages_modules.consultant_documents.st')
    def test_create_cv_upload_form(self, mock_st):
        """Test de création du formulaire d'upload CV"""
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.file_uploader.return_value = None
        mock_st.form_submit_button.return_value = False
        
        from app.pages_modules.consultant_documents import _create_cv_upload_form
        result = _create_cv_upload_form(123)
        
        self.assertIsNotNone(result)
    
    @patch('app.pages_modules.consultant_documents.st')
    def test_display_document_not_found(self, mock_st):
        """Test d'affichage document non trouvé"""
        mock_st.error.return_value = None
        mock_st.info.return_value = None
        
        from app.pages_modules.consultant_documents import _display_document_not_found
        _display_document_not_found()
        
        mock_st.error.assert_called_once()

if __name__ == '__main__':
    unittest.main()
'''
    
    return {
        "tests/unit/services/test_business_manager_service_coverage.py": business_manager_tests,
        "tests/unit/pages_modules/test_consultant_documents_coverage.py": consultant_documents_tests
    }

def create_enhanced_ui_tests():
    """Crée des tests pour enhanced_ui (64% -> 80%+)"""
    
    enhanced_ui_tests = '''
"""
Tests pour enhanced_ui - Amélioration couverture 64% -> 80%+
"""
import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

class TestEnhancedUICoverage(unittest.TestCase):
    """Tests pour améliorer la couverture d'enhanced_ui"""
    
    @patch('app.ui.enhanced_ui.st')
    def test_create_metric_card(self, mock_st):
        """Test de création de carte métrique"""
        mock_st.markdown.return_value = None
        
        from app.ui.enhanced_ui import create_metric_card
        create_metric_card("Test", "100", "↗️ +10%")
        
        mock_st.markdown.assert_called()
    
    @patch('app.ui.enhanced_ui.st')
    def test_create_info_card(self, mock_st):
        """Test de création de carte info"""
        mock_st.markdown.return_value = None
        
        from app.ui.enhanced_ui import create_info_card
        create_info_card("Titre", "Contenu", "info")
        
        mock_st.markdown.assert_called()
    
    @patch('app.ui.enhanced_ui.st')
    def test_display_consultant_card(self, mock_st):
        """Test d'affichage carte consultant"""
        mock_st.markdown.return_value = None
        mock_st.button.return_value = False
        
        consultant = MagicMock()
        consultant.prenom = "Jean"
        consultant.nom = "Dupont"
        consultant.practice = MagicMock()
        consultant.practice.nom = "Data"
        
        from app.ui.enhanced_ui import display_consultant_card
        display_consultant_card(consultant)
        
        mock_st.markdown.assert_called()

if __name__ == '__main__':
    unittest.main()
'''
    
    return enhanced_ui_tests

def create_consultants_coverage_tests():
    """Crée des tests supplémentaires pour consultants.py (61% -> 75%+)"""
    
    consultants_tests = '''
"""
Tests supplémentaires pour consultants.py - Amélioration couverture 61% -> 75%+
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import date

class TestConsultantsCoverageBoost(unittest.TestCase):
    """Tests pour améliorer significativement la couverture de consultants.py"""
    
    @patch('app.pages_modules.consultants.st')
    def test_render_availability_field(self, mock_st):
        """Test du champ disponibilité"""
        mock_st.radio.return_value = "Disponible"
        
        from app.pages_modules.consultants import _render_availability_field
        result = _render_availability_field(MagicMock())
        
        self.assertEqual(result, "Disponible")
        mock_st.radio.assert_called_once()
    
    @patch('app.pages_modules.consultants.st')
    def test_render_practice_field(self, mock_st):
        """Test du champ practice"""
        mock_st.selectbox.return_value = 1
        
        from app.pages_modules.consultants import _render_practice_field
        result = _render_practice_field([MagicMock()], None)
        
        self.assertEqual(result, 1)
        mock_st.selectbox.assert_called_once()
    
    @patch('app.pages_modules.consultants.st')
    def test_render_manager_field(self, mock_st):
        """Test du champ manager"""
        mock_st.selectbox.return_value = 1
        
        from app.pages_modules.consultants import _render_manager_field
        result = _render_manager_field([MagicMock()], None)
        
        self.assertEqual(result, 1)
        mock_st.selectbox.assert_called_once()
    
    def test_validate_consultant_data_valid(self):
        """Test de validation avec données valides"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789"
        }
        
        from app.pages_modules.consultants import _validate_consultant_data
        errors = _validate_consultant_data(data)
        
        self.assertEqual(len(errors), 0)
    
    def test_validate_consultant_data_missing_required(self):
        """Test de validation avec données manquantes"""
        data = {
            "prenom": "",
            "nom": "Dupont",
            "email": "invalid-email",
            "telephone": "123"
        }
        
        from app.pages_modules.consultants import _validate_consultant_data
        errors = _validate_consultant_data(data)
        
        self.assertGreater(len(errors), 0)
    
    def test_format_consultant_display_name(self):
        """Test de formatage du nom d'affichage"""
        consultant = MagicMock()
        consultant.prenom = "Jean"
        consultant.nom = "Dupont"
        
        from app.pages_modules.consultants import _format_consultant_display_name
        result = _format_consultant_display_name(consultant)
        
        self.assertEqual(result, "Jean DUPONT")
    
    def test_calculate_experience_years(self):
        """Test de calcul des années d'expérience"""
        from app.pages_modules.consultants import _calculate_experience_years
        
        # Test avec date d'entrée
        result = _calculate_experience_years(date(2020, 1, 1), None)
        self.assertGreater(result, 3)
        
        # Test avec date de sortie
        result = _calculate_experience_years(date(2020, 1, 1), date(2023, 1, 1))
        self.assertEqual(result, 3)
    
    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status_active(self, mock_st):
        """Test d'affichage statut consultant actif"""
        mock_st.success.return_value = None
        
        consultant = MagicMock()
        consultant.date_sortie = None
        
        from app.pages_modules.consultants import _display_consultant_status
        _display_consultant_status(consultant)
        
        mock_st.success.assert_called_once()
    
    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status_inactive(self, mock_st):
        """Test d'affichage statut consultant inactif"""
        mock_st.warning.return_value = None
        
        consultant = MagicMock()
        consultant.date_sortie = date(2023, 12, 31)
        
        from app.pages_modules.consultants import _display_consultant_status
        _display_consultant_status(consultant)
        
        mock_st.warning.assert_called_once()

if __name__ == '__main__':
    unittest.main()
'''
    
    return consultants_tests

def main():
    """Fonction principale d'amélioration de la couverture"""
    print("🚀 Amélioration de la couverture de tests vers 80%+")
    print("=" * 60)
    
    # 1. Correction des problèmes de mocking pandas
    print("🔧 Correction des problèmes de mocking pandas...")
    pandas_fixes = fix_pandas_mock_issues()
    
    # 2. Création des tests ciblés pour modules faible couverture
    print("📝 Création des tests ciblés...")
    targeted_tests = create_targeted_coverage_tests()
    
    # 3. Tests pour enhanced_ui
    print("🎨 Création des tests enhanced_ui...")
    ui_tests = create_enhanced_ui_tests()
    
    # 4. Tests supplémentaires pour consultants.py
    print("👥 Création des tests consultants supplémentaires...")
    consultants_tests = create_consultants_coverage_tests()
    
    # Écriture des fichiers
    all_tests = {
        **targeted_tests,
        "tests/unit/ui/test_enhanced_ui_coverage.py": ui_tests,
        "tests/unit/pages_modules/test_consultants_coverage_boost.py": consultants_tests
    }
    
    for file_path, content in all_tests.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Créé: {file_path}")
    
    print(f"\n✨ {len(all_tests)} nouveaux fichiers de tests créés!")
    print("\n📊 Prochaines étapes:")
    print("1. Corriger les tests pandas existants")
    print("2. Exécuter les nouveaux tests")
    print("3. Vérifier l'amélioration de couverture")
    print("4. Cible: 76% → 80%+")

if __name__ == "__main__":
    main()