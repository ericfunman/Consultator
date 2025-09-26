"""
Générateur automatique de tests après développement

Ce script surveille les changements de code et génère automatiquement
les tests de régression correspondants.
"""

import os
import ast
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime


class PostDevelopmentTestGenerator:
    def __init__(self):
        self.project_root = Path.cwd()
        self.tests_dir = self.project_root / 'tests'
        self.regression_dir = self.tests_dir / 'regression'
        self.auto_generated_dir = self.tests_dir / 'auto_generated'
        
        # Crée les dossiers nécessaires
        self.auto_generated_dir.mkdir(parents=True, exist_ok=True)
        
    def detect_code_changes(self) -> List[str]:
        """Détecte les fichiers Python modifiés récemment"""
        try:
            # Fichiers modifiés dans les derniers commits
            result = subprocess.run([
                'git', 'diff', '--name-only', 'HEAD~3', 'HEAD'
            ], capture_output=True, text=True, check=True)
            
            changed_files = []
            for line in result.stdout.strip().split('\n'):
                if line.endswith('.py') and not line.startswith('tests/'):
                    if Path(line).exists():
                        changed_files.append(line)
            
            return changed_files
            
        except subprocess.CalledProcessError:
            # Fallback: fichiers modifiés récemment
            recent_files = []
            for py_file in Path('app').rglob('*.py'):
                if py_file.stat().st_mtime > (datetime.now().timestamp() - 24*3600):  # 24h
                    recent_files.append(str(py_file))
            return recent_files
            
    def analyze_code_complexity(self, file_path: str) -> Dict:
        """Analyse la complexité du code pour adapter les tests"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                'functions': [],
                'classes': [],
                'imports': [],
                'complexity_score': 0,
                'has_database_calls': False,
                'has_external_dependencies': False,
                'has_error_handling': False
            }
            
            # Analyse AST
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'has_docstring': ast.get_docstring(node) is not None,
                        'line_number': node.lineno,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    }
                    analysis['functions'].append(func_info)
                    
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'methods': [],
                        'has_docstring': ast.get_docstring(node) is not None,
                        'line_number': node.lineno
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append({
                                'name': item.name,
                                'args': [arg.arg for arg in item.args.args],
                                'is_property': any(
                                    isinstance(d, ast.Name) and d.id == 'property'
                                    for d in item.decorator_list
                                )
                            })
                    
                    analysis['classes'].append(class_info)
                    
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis['imports'].append(alias.name)
                    else:
                        if node.module:
                            analysis['imports'].append(node.module)
                            
                elif isinstance(node, ast.Try):
                    analysis['has_error_handling'] = True
            
            # Détection de patterns spécifiques
            content_lower = content.lower()
            if any(keyword in content_lower for keyword in ['session', 'query', 'commit', 'rollback']):
                analysis['has_database_calls'] = True
            
            if any(lib in content_lower for lib in ['requests', 'http', 'api', 'streamlit']):
                analysis['has_external_dependencies'] = True
            
            # Score de complexité simple
            analysis['complexity_score'] = (
                len(analysis['functions']) * 2 +
                len(analysis['classes']) * 3 +
                (10 if analysis['has_database_calls'] else 0) +
                (5 if analysis['has_external_dependencies'] else 0) +
                (3 if analysis['has_error_handling'] else 0)
            )
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Erreur analyse de {file_path}: {e}")
            return {'functions': [], 'classes': [], 'complexity_score': 0}
    
    def generate_test_for_file(self, file_path: str) -> str:
        """Génère un fichier de test complet pour un fichier donné"""
        analysis = self.analyze_code_complexity(file_path)
        
        if not analysis['functions'] and not analysis['classes']:
            return None
        
        # Prépare les imports
        module_path = file_path.replace('/', '.').replace('\\', '.').replace('.py', '')
        test_imports = ['import pytest', 'from unittest.mock import Mock, patch, MagicMock']
        
        if analysis['has_database_calls']:
            test_imports.extend([
                'from app.database.database import get_session',
                'from sqlalchemy.orm import Session'
            ])
        
        if analysis['has_external_dependencies']:
            test_imports.append('import requests_mock')
        
        test_content = f'''"""
Tests automatiquement générés pour {file_path}
Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️  ATTENTION: Ces tests sont des templates de base.
Ils doivent être adaptés selon la logique métier spécifique.
"""

{chr(10).join(test_imports)}

try:
    from {module_path} import *
except ImportError as e:
    pytest.skip(f"Cannot import {module_path}: {{e}}", allow_module_level=True)


'''
        
        # Génère les tests de classes
        for class_info in analysis['classes']:
            test_content += self.generate_class_tests(class_info, analysis)
        
        # Génère les tests de fonctions
        for func_info in analysis['functions']:
            test_content += self.generate_function_tests(func_info, analysis)
        
        return test_content
    
    def generate_class_tests(self, class_info: Dict, analysis: Dict) -> str:
        """Génère les tests pour une classe"""
        class_name = class_info['name']
        
        test_code = f'''

class Test{class_name}:
    """Tests automatiquement générés pour {class_name}"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        # TODO: Initialiser les mocks et données de test
        pass
    
    def test_{class_name.lower()}_init(self):
        """Test d'initialisation de {class_name}"""
        # TODO: Tester la création d'instance
        instance = {class_name}()
        assert instance is not None
    
'''
        
        # Tests pour chaque méthode
        for method in class_info['methods']:
            if method['name'].startswith('_') and not method['name'].startswith('__'):
                continue  # Skip private methods (mais pas les magic methods)
            
            method_name = method['name']
            test_code += f'''    def test_{method_name}(self):
        """Test de la méthode {method_name}"""
        # Given
        instance = {class_name}()
        # TODO: Préparer les données de test
        
        # When
        # TODO: Appeler la méthode à tester
        # result = instance.{method_name}(test_data)
        
        # Then
        # TODO: Vérifier le résultat
        pass
    
'''
        
        # Test d'intégration si base de données
        if analysis['has_database_calls']:
            test_code += f'''    @patch('app.database.get_session')
    def test_{class_name.lower()}_database_integration(self, mock_session):
        """Test d'intégration avec la base de données"""
        # Given
        mock_db = Mock()
        mock_session.return_value = mock_db
        instance = {class_name}()
        
        # When
        # TODO: Tester les interactions DB
        
        # Then
        # TODO: Vérifier les appels DB
        # mock_db.query.assert_called()
        pass
    
'''
        
        return test_code
    
    def generate_function_tests(self, func_info: Dict, analysis: Dict) -> str:
        """Génère les tests pour une fonction"""
        func_name = func_info['name']
        
        if func_name.startswith('_'):
            return ""  # Skip private functions
        
        test_code = f'''

def test_{func_name}():
    """Test automatiquement généré pour {func_name}"""
    # Given
    # TODO: Préparer les paramètres de test
    
    # When
    # TODO: Appeler la fonction
    # result = {func_name}(test_params)
    
    # Then
    # TODO: Vérifier le résultat
    pass


def test_{func_name}_edge_cases():
    """Test des cas limites pour {func_name}"""
    # TODO: Tester les cas d'erreur et cas limites
    pass

'''
        
        # Test avec mock si nécessaire
        if analysis['has_database_calls'] or analysis['has_external_dependencies']:
            test_code += f'''
@patch('requests.get')  # Adapter selon les dépendances
def test_{func_name}_with_mocks(mock_request):
    """Test de {func_name} avec mocks"""
    # Given
    mock_request.return_value.json.return_value = {{"test": "data"}}
    
    # When
    # TODO: Appeler avec mocks
    
    # Then
    # TODO: Vérifier les appels mocks
    pass

'''
        
        return test_code
    
    def create_regression_tests(self, changed_files: List[str]):
        """Crée des tests de régression pour les fichiers modifiés"""
        print(f"🔧 Génération de tests de régression pour {len(changed_files)} fichiers...")
        
        generated_files = []
        
        for file_path in changed_files:
            print(f"  📝 Traitement de {file_path}...")
            
            # Génère le contenu du test
            test_content = self.generate_test_for_file(file_path)
            
            if not test_content:
                print(f"    ⚠️ Aucun test générable pour {file_path}")
                continue
            
            # Determine le nom du fichier de test
            try:
                relative_path = Path(file_path).relative_to(self.project_root)
                test_file_name = f"test_{relative_path.stem}_auto.py"
            except ValueError:
                # Fichier hors du projet, utilise juste le nom
                test_file_name = f"test_{Path(file_path).stem}_auto.py"
            
            # Place dans le bon dossier
            if 'service' in file_path.lower():
                test_file_path = self.auto_generated_dir / 'services' / test_file_name
            elif 'pages' in file_path.lower():
                test_file_path = self.auto_generated_dir / 'pages' / test_file_name
            elif 'models' in file_path.lower():
                test_file_path = self.auto_generated_dir / 'models' / test_file_name
            else:
                test_file_path = self.auto_generated_dir / test_file_name
            
            # Crée le dossier si nécessaire
            test_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarde le test
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            generated_files.append(str(test_file_path))
            print(f"    ✅ Test généré : {test_file_path}")
        
        return generated_files
    
    def update_existing_tests(self, changed_files: List[str]):
        """Met à jour les tests existants si nécessaire"""
        print("🔄 Vérification des tests existants...")
        
        updated_tests = []
        
        for file_path in changed_files:
            # Cherche les tests existants
            possible_test_files = [
                f"test_{Path(file_path).stem}.py",
                f"test_{Path(file_path).stem}_test.py",
                f"{Path(file_path).stem}_test.py"
            ]
            
            for test_dir in [self.tests_dir, self.regression_dir]:
                for test_name in possible_test_files:
                    test_file = test_dir / test_name
                    if test_file.exists():
                        # Ajoute des commentaires de mise à jour
                        self.add_update_comment(test_file, file_path)
                        updated_tests.append(str(test_file))
                        break
        
        if updated_tests:
            print(f"  📝 {len(updated_tests)} tests existants marqués pour révision")
        
        return updated_tests
    
    def add_update_comment(self, test_file: Path, source_file: str):
        """Ajoute un commentaire de mise à jour dans un test existant"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            update_comment = f"""
# ⚠️  MISE À JOUR REQUISE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Le fichier source {source_file} a été modifié.
# Veuillez réviser ce test pour s'assurer qu'il couvre les nouveaux changements.

"""
            
            # Ajoute le commentaire au début (après les imports)
            lines = content.split('\n')
            insert_pos = 0
            
            # Trouve la fin des imports
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#') and not line.startswith('import') and not line.startswith('from'):
                    insert_pos = i
                    break
            
            lines.insert(insert_pos, update_comment.strip())
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
        except Exception as e:
            print(f"⚠️ Erreur mise à jour {test_file}: {e}")
    
    def run_generated_tests(self, test_files: List[str]) -> bool:
        """Exécute les tests générés pour vérifier qu'ils fonctionnent"""
        if not test_files:
            return True
        
        print("🧪 Exécution des tests générés...")
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest',
                *test_files,
                '-v',
                '--tb=short',
                '--disable-warnings'
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                print("✅ Tous les tests générés passent")
                return True
            else:
                print("⚠️ Certains tests générés échouent (normal pour des templates)")
                print("Consultez les fichiers pour les adapter à votre logique métier")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution des tests: {e}")
            return False
    
    def generate_test_summary(self, generated_files: List[str], updated_files: List[str]):
        """Génère un résumé des tests créés/mis à jour"""
        summary = f"""
# 📊 Résumé de génération de tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🆕 Tests générés automatiquement
"""
        
        if generated_files:
            for file in generated_files:
                summary += f"- {file}\n"
        else:
            summary += "Aucun nouveau test généré.\n"
        
        summary += """
## 🔄 Tests existants à réviser
"""
        
        if updated_files:
            for file in updated_files:
                summary += f"- {file}\n"
        else:
            summary += "Aucun test existant à réviser.\n"
        
        summary += """
## ⚡ Actions requises

### 1. Révision des tests générés
Les tests automatiquement générés sont des **templates de base**.
Vous devez les adapter selon votre logique métier spécifique:

- Remplacer les `# TODO:` par le code réel
- Ajouter les données de test appropriées
- Implémenter les assertions spécifiques
- Tester les cas d'erreur réels

### 2. Exécution et validation
```bash
# Exécuter les nouveaux tests
python -m pytest tests/auto_generated/ -v

# Vérifier la couverture
python -m pytest tests/auto_generated/ --cov=app --cov-report=term-missing
```

### 3. Intégration dans la suite de tests
Une fois adaptés, déplacer les tests vers les dossiers appropriés:
- `tests/unit/` pour les tests unitaires
- `tests/integration/` pour les tests d'intégration
- `tests/regression/` pour les tests de régression

## 🎯 Prochaines étapes recommandées
1. Réviser et adapter chaque test généré
2. Exécuter la suite complète de tests
3. Vérifier l'amélioration de la couverture
4. Commiter les tests finalisés
"""
        
        # Sauvegarde le résumé
        summary_file = self.auto_generated_dir / 'GENERATION_SUMMARY.md'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"📋 Résumé sauvegardé : {summary_file}")
        return summary


def main():
    """Fonction principale de génération post-développement"""
    print("🤖 GÉNÉRATEUR AUTOMATIQUE DE TESTS POST-DÉVELOPPEMENT")
    print("="*60)
    
    generator = PostDevelopmentTestGenerator()
    
    # Détecte les changements
    changed_files = generator.detect_code_changes()
    
    if not changed_files:
        print("✅ Aucun fichier Python modifié récemment")
        return
    
    print(f"📊 {len(changed_files)} fichiers modifiés détectés:")
    for file in changed_files:
        print(f"  - {file}")
    
    # Génère les tests
    generated_files = generator.create_regression_tests(changed_files)
    
    # Met à jour les tests existants
    updated_files = generator.update_existing_tests(changed_files)
    
    # Exécute les tests générés (mode template)
    generator.run_generated_tests(generated_files)
    
    # Génère le résumé
    generator.generate_test_summary(generated_files, updated_files)
    
    print("\n" + "="*60)
    print("✅ GÉNÉRATION TERMINÉE")
    print("="*60)
    print(f"🆕 {len(generated_files)} nouveaux tests générés")
    print(f"🔄 {len(updated_files)} tests existants à réviser")
    print("\n💡 Consultez tests/auto_generated/GENERATION_SUMMARY.md pour les prochaines étapes")


if __name__ == '__main__':
    main()