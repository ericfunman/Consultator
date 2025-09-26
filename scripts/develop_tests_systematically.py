#!/usr/bin/env python3
"""
Script de développement systématique de tests.
Augmente progressivement la couverture en ciblant les modules prioritaires.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Configuration
WORKSPACE = Path(__file__).parent.parent
COVERAGE_TARGET = 80.0
MINIMUM_INCREMENT = 5.0  # Augmentation minimale par itération

class TestDeveloper:
    def __init__(self):
        self.workspace = WORKSPACE
        self.coverage_file = self.workspace / "reports" / "coverage_clean.json"
        
    def get_current_coverage(self) -> Tuple[float, Dict]:
        """Récupère la couverture actuelle"""
        if not self.coverage_file.exists():
            print("❌ Fichier de couverture non trouvé, exécution des tests...")
            self.run_tests()
            
        with open(self.coverage_file) as f:
            data = json.load(f)
            
        return data['totals']['percent_covered'], data['files']
    
    def run_tests(self) -> bool:
        """Exécute tous les tests fonctionnels"""
        test_command = [
            sys.executable, "-m", "pytest",
            "tests/unit/services/test_priority_services.py",
            "tests/unit/pages/test_consultant_pages.py", 
            "tests/regression/test_vsa_import_regression.py",
            "--cov=app",
            "--cov-report=json:reports/coverage_clean.json",
            "-v"
        ]
        
        result = subprocess.run(test_command, cwd=self.workspace, capture_output=True, text=True)
        return result.returncode == 0
    
    def identify_priority_modules(self, files_data: Dict) -> List[Tuple[str, float, int]]:
        """Identifie les modules prioritaires à tester"""
        modules = []
        
        for file, data in files_data.items():
            # Normaliser le chemin pour Windows (\\ vers /)
            normalized_file = file.replace('\\', '/')
            
            if (normalized_file.startswith('app/') and 
                not normalized_file.startswith('app/tests/') and
                data['summary']['num_statements'] > 50 and  # Seuil plus élevé
                data['summary']['percent_covered'] < 70):  # Seulement les modules mal couverts
                
                modules.append((
                    file,
                    data['summary']['percent_covered'], 
                    data['summary']['num_statements'],
                    data['summary']['missing_lines']
                ))
        
        # Trier par impact potentiel (lignes * (100 - couverture))
        modules.sort(key=lambda x: x[2] * (100 - x[1]), reverse=True)
        return modules[:5]  # Top 5 seulement
    
    def create_service_test_template(self, service_file: str) -> str:
        """Génère un template de test pour un service"""
        service_name = Path(service_file).stem
        class_name = ''.join(word.capitalize() for word in service_name.split('_'))
        
        return f'''"""
Tests pour {service_file}
Génération automatique - à compléter manuellement
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from app.services.{service_name} import *
    SERVICE_AVAILABLE = True
except ImportError as e:
    SERVICE_AVAILABLE = False
    pytest.skip(f"Service {{service_name}} non disponible: {{e}}", allow_module_level=True)


class Test{class_name}:
    """Tests pour {class_name}"""
    
    @pytest.fixture
    def mock_database(self):
        """Mock de la base de données"""
        with patch('app.database.database.get_database_session') as mock:
            mock_session = Mock()
            mock.__enter__ = Mock(return_value=mock_session)
            mock.__exit__ = Mock(return_value=False)
            mock.return_value = mock
            yield mock_session
    
    def test_service_initialization(self):
        """Test d'initialisation du service"""
        # TODO: Implémenter le test d'initialisation
        assert True  # Placeholder
    
    def test_basic_methods(self, mock_database):
        """Test des méthodes de base"""
        # TODO: Identifier et tester les méthodes principales
        mock_database.query.return_value.all.return_value = []
        # Ajouter les tests spécifiques
        assert True  # Placeholder
    
    def test_error_handling(self):
        """Test de la gestion d'erreurs"""
        # TODO: Tester les cas d'erreur
        assert True  # Placeholder
    
    def test_edge_cases(self):
        """Test des cas limites"""
        # TODO: Tester les cas limites
        assert True  # Placeholder


class Test{class_name}Integration:
    """Tests d'intégration pour {class_name}"""
    
    def test_database_integration(self, mock_database):
        """Test d'intégration avec la base de données"""
        # TODO: Tests d'intégration
        assert True  # Placeholder


# Ajouter plus de classes de test selon les besoins du service
'''

    def create_page_test_template(self, page_file: str) -> str:
        """Génère un template de test pour une page"""
        page_name = Path(page_file).stem
        class_name = ''.join(word.capitalize() for word in page_name.split('_'))
        
        return f'''"""
Tests pour {page_file}
Génération automatique - à compléter manuellement
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock Streamlit avant l'import
sys.modules['streamlit'] = Mock()

try:
    from app.pages_modules.{page_name} import *
    PAGE_AVAILABLE = True
except ImportError as e:
    PAGE_AVAILABLE = False
    pytest.skip(f"Page {{page_name}} non disponible: {{e}}", allow_module_level=True)


class Test{class_name}Page:
    """Tests pour la page {page_name}"""
    
    @pytest.fixture
    def mock_streamlit(self):
        """Mock de Streamlit"""
        with patch.dict(sys.modules, {{'streamlit': Mock()}}):
            import streamlit as st
            st.session_state = {{}}
            st.columns = Mock(return_value=[Mock(), Mock()])
            st.form = Mock()
            st.form_submit_button = Mock(return_value=False)
            st.selectbox = Mock(return_value="Test")
            st.text_input = Mock(return_value="Test")
            st.text_area = Mock(return_value="Test")
            st.number_input = Mock(return_value=0)
            st.date_input = Mock()
            st.success = Mock()
            st.error = Mock()
            st.warning = Mock()
            st.info = Mock()
            yield st
    
    def test_page_structure(self, mock_streamlit):
        """Test de la structure de la page"""
        # TODO: Tester la structure de la page
        assert True  # Placeholder
    
    def test_page_components(self, mock_streamlit):
        """Test des composants de la page"""
        # TODO: Tester les composants individuels
        assert True  # Placeholder
    
    def test_form_handling(self, mock_streamlit):
        """Test de la gestion des formulaires"""
        # TODO: Tester la soumission de formulaires
        assert True  # Placeholder
    
    def test_data_display(self, mock_streamlit):
        """Test de l'affichage des données"""
        # TODO: Tester l'affichage des données
        assert True  # Placeholder


class Test{class_name}Navigation:
    """Tests de navigation pour {page_name}"""
    
    def test_page_routing(self, mock_streamlit):
        """Test du routage de la page"""
        # TODO: Tests de navigation
        assert True  # Placeholder


# Ajouter plus de classes de test selon les besoins de la page
'''

    def generate_tests_for_module(self, module_file: str) -> str:
        """Génère des tests pour un module spécifique"""
        print(f"🔨 Génération de tests pour {module_file}")
        
        # Créer le répertoire de test approprié
        if 'services' in module_file:
            test_dir = self.workspace / "tests" / "unit" / "services"
            test_file = f"test_{Path(module_file).stem}_generated.py"
            template = self.create_service_test_template(module_file)
        elif 'pages_modules' in module_file:
            test_dir = self.workspace / "tests" / "unit" / "pages_modules" 
            test_file = f"test_{Path(module_file).stem}_generated.py"
            template = self.create_page_test_template(module_file)
        else:
            test_dir = self.workspace / "tests" / "unit" / "generic"
            test_file = f"test_{Path(module_file).stem}_generated.py"
            template = f'''# Tests génériques pour {module_file}
# TODO: Implémenter les tests
import pytest

def test_placeholder():
    assert True
'''
        
        test_dir.mkdir(parents=True, exist_ok=True)
        test_path = test_dir / test_file
        
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ Test généré: {test_path}")
        return str(test_path)
    
    def develop_iteration(self) -> Tuple[float, float]:
        """Une itération de développement de tests"""
        print("\n🔄 NOUVELLE ITÉRATION DE DÉVELOPPEMENT")
        print("=" * 50)
        
        # 1. Mesurer la couverture actuelle
        current_coverage, files_data = self.get_current_coverage()
        print(f"📊 Couverture actuelle: {current_coverage:.1f}%")
        
        # 2. Identifier les modules prioritaires
        priority_modules = self.identify_priority_modules(files_data)
        print(f"🎯 Modules prioritaires identifiés: {len(priority_modules)}")
        
        # 3. Sélectionner le module avec le plus gros impact
        if not priority_modules:
            print("✅ Tous les modules ont une bonne couverture")
            return current_coverage, current_coverage
        
        target_module, coverage, lines, missing = priority_modules[0]
        impact_score = lines * (100 - coverage)
        
        print(f"🔨 Module cible: {target_module}")
        print(f"   Couverture: {coverage:.1f}%")
        print(f"   Lignes: {lines}")
        print(f"   Score d'impact: {impact_score:.0f}")
        
        # 4. Générer des tests pour ce module
        self.generate_tests_for_module(target_module)
        
        # 5. Exécuter les tests et mesurer l'amélioration
        print("🧪 Exécution des tests...")
        self.run_tests()
        new_coverage, _ = self.get_current_coverage()
        
        improvement = new_coverage - current_coverage
        print(f"📈 Amélioration: +{improvement:.1f}% ({current_coverage:.1f}% → {new_coverage:.1f}%)")
        
        return current_coverage, new_coverage
    
    def run_development_cycle(self, max_iterations: int = 10):
        """Exécute un cycle complet de développement"""
        print("🚀 DÉMARRAGE DU CYCLE DE DÉVELOPPEMENT")
        print(f"🎯 Objectif: {COVERAGE_TARGET}%")
        print(f"🔄 Maximum {max_iterations} itérations")
        print("=" * 60)
        
        results = []
        
        for iteration in range(1, max_iterations + 1):
            print(f"\n📅 ITÉRATION {iteration}/{max_iterations}")
            
            old_coverage, new_coverage = self.develop_iteration()
            results.append((iteration, old_coverage, new_coverage))
            
            # Vérifier si l'objectif est atteint
            if new_coverage >= COVERAGE_TARGET:
                print(f"🎉 OBJECTIF ATTEINT! Couverture: {new_coverage:.1f}%")
                break
                
            # Vérifier si l'amélioration est suffisante
            improvement = new_coverage - old_coverage
            if improvement < MINIMUM_INCREMENT:
                print(f"⚠️ Amélioration insuffisante (+{improvement:.1f}% < {MINIMUM_INCREMENT}%)")
                print("💡 Conseil: Compléter manuellement les tests générés")
                
            print("⏱️ Pause avant prochaine itération...")
            
        # Rapport final
        self.generate_final_report(results)
    
    def generate_final_report(self, results: List[Tuple]):
        """Génère le rapport final"""
        report_file = self.workspace / "reports" / f"development_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        if not results:
            return
        
        final_coverage = results[-1][2]
        initial_coverage = results[0][1]
        total_improvement = final_coverage - initial_coverage
        
        content = f"""# Rapport de Développement de Tests

*Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📊 Résumé

- **Couverture initiale**: {initial_coverage:.1f}%
- **Couverture finale**: {final_coverage:.1f}%
- **Amélioration totale**: +{total_improvement:.1f}%
- **Objectif**: {COVERAGE_TARGET}%
- **Itérations**: {len(results)}

## 📈 Progression par Itération

| Itération | Avant | Après | Amélioration |
|-----------|-------|-------|--------------|
"""
        
        for iteration, before, after in results:
            improvement = after - before
            content += f"| {iteration} | {before:.1f}% | {after:.1f}% | +{improvement:.1f}% |\n"
        
        content += f"""
## 🎯 Statut

{"✅ **OBJECTIF ATTEINT**" if final_coverage >= COVERAGE_TARGET else "⚠️ **OBJECTIF NON ATTEINT**"}

## 🔄 Prochaines Actions

### Automatiques
- Tests générés dans `tests/unit/*/test_*_generated.py`
- Templates prêts à compléter

### Manuelles Recommandées
1. Compléter les tests générés avec la logique spécifique
2. Ajouter des tests d'intégration
3. Tester les cas d'erreur et cas limites
4. Valider avec des données réelles

### Outils Disponibles
- `python scripts/improve_coverage.py` - Analyse détaillée
- `python scripts/clean_test_environment.py` - Environnement propre
- `python scripts/develop_tests_systematically.py` - Ce script

## 📝 Tests Générés

Les nouveaux fichiers de test ont été créés avec des templates à compléter.
Chaque template contient:
- Structure de base des tests
- Mocks configurés
- Méthodes de test placeholder
- Documentation des TODO

**Important**: Les tests générés sont des templates. Ils doivent être complétés avec la logique métier spécifique pour être efficaces.
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n📋 Rapport final: {report_file}")

def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        max_iterations = int(sys.argv[1])
    else:
        max_iterations = 5
    
    developer = TestDeveloper()
    developer.run_development_cycle(max_iterations)

if __name__ == "__main__":
    main()