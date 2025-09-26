"""
Script de génération automatique de tests de non-régression

Ce script analyse les modifications de code et génère automatiquement
des tests de non-régression appropriés.
"""

import ast
import os
import inspect
from pathlib import Path
from typing import List, Dict, Set
import importlib.util


class TestGenerator:
    """Générateur automatique de tests de non-régression"""
    
    def __init__(self, app_path: str = "app"):
        self.app_path = Path(app_path)
        self.test_templates = {
            'service': self._generate_service_test,
            'model': self._generate_model_test,
            'function': self._generate_function_test,
            'class': self._generate_class_test
        }
    
    def analyze_changed_files(self, changed_files: List[str]) -> Dict[str, List[str]]:
        """
        Analyse les fichiers modifiés et identifie les fonctions/classes impactées
        
        Args:
            changed_files: Liste des fichiers modifiés
            
        Returns:
            Dictionnaire {file: [functions/classes]}
        """
        impacted_components = {}
        
        for file_path in changed_files:
            if not file_path.endswith('.py') or 'test' in file_path:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                components = self._extract_components(tree)
                
                if components:
                    impacted_components[file_path] = components
                    
            except Exception as e:
                print(f"Erreur analyse {file_path}: {e}")
        
        return impacted_components
    
    def _extract_components(self, tree: ast.AST) -> List[str]:
        """Extrait les fonctions et classes d'un AST"""
        components = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Fonctions publiques seulement
                    components.append(f"function:{node.name}")
            elif isinstance(node, ast.ClassDef):
                components.append(f"class:{node.name}")
        
        return components
    
    def generate_regression_tests(self, impacted_components: Dict[str, List[str]]) -> str:
        """
        Génère le code des tests de non-régression
        
        Args:
            impacted_components: Composants impactés par module
            
        Returns:
            Code des tests générés
        """
        test_code = []
        
        # Header
        test_code.append('"""')
        test_code.append('Tests de non-régression générés automatiquement')
        test_code.append('"""')
        test_code.append('import pytest')
        test_code.append('from unittest.mock import Mock, patch')
        test_code.append('')
        
        for file_path, components in impacted_components.items():
            module_name = self._path_to_module(file_path)
            
            for component in components:
                comp_type, comp_name = component.split(':', 1)
                
                if comp_type in self.test_templates:
                    test_method = self.test_templates[comp_type]
                    test_code.extend(test_method(module_name, comp_name))
                    test_code.append('')
        
        return '\n'.join(test_code)
    
    def _path_to_module(self, file_path: str) -> str:
        """Convertit un chemin de fichier en nom de module"""
        return file_path.replace('/', '.').replace('\\', '.').replace('.py', '')
    
    def _generate_service_test(self, module_name: str, service_name: str) -> List[str]:
        """Génère un test pour un service"""
        return [
            f"class Test{service_name}Regression:",
            f'    """Tests de non-régression pour {service_name}"""',
            "",
            f"    def test_{service_name.lower()}_basic_functionality(self, db_session):",
            f'        """Test de base pour {service_name}"""',
            f"        # Given - Données de test",
            f"        test_data = {{'test': 'data'}}",
            "",
            f"        # When - Appel de la méthode",
            f"        with patch('{module_name}') as mock_module:",
            f"            # Test implementation",
            f"            pass",
            "",
            f"        # Then - Vérifications",
            f"        assert True  # TODO: Implémenter les assertions",
        ]
    
    def _generate_model_test(self, module_name: str, model_name: str) -> List[str]:
        """Génère un test pour un modèle"""
        return [
            f"class Test{model_name}ModelRegression:",
            f'    """Tests de non-régression pour le modèle {model_name}"""',
            "",
            f"    def test_{model_name.lower()}_creation_regression(self, db_session):",
            f'        """Test de création {model_name}"""',
            f"        from {module_name} import {model_name}",
            "",
            f"        # Given - Données valides",
            f"        data = {{'name': 'test'}}",
            "",
            f"        # When - Création",
            f"        instance = {model_name}(**data)",
            f"        db_session.add(instance)",
            f"        db_session.commit()",
            "",
            f"        # Then - Instance créée",
            f"        assert instance.id is not None",
        ]
    
    def _generate_function_test(self, module_name: str, function_name: str) -> List[str]:
        """Génère un test pour une fonction"""
        return [
            f"class Test{function_name.title()}Regression:",
            f'    """Tests de non-régression pour {function_name}"""',
            "",
            f"    def test_{function_name}_regression(self):",
            f'        """Test de non-régression pour {function_name}"""',
            f"        from {module_name} import {function_name}",
            "",
            f"        # Given - Paramètres de test",
            f"        test_params = []",
            "",
            f"        # When - Appel de la fonction",
            f"        result = {function_name}(*test_params)",
            "",
            f"        # Then - Résultat attendu",
            f"        assert result is not None",
        ]
    
    def _generate_class_test(self, module_name: str, class_name: str) -> List[str]:
        """Génère un test pour une classe"""
        return [
            f"class Test{class_name}Regression:",
            f'    """Tests de non-régression pour {class_name}"""',
            "",
            f"    def test_{class_name.lower()}_instantiation_regression(self):",
            f'        """Test d\'instantiation {class_name}"""',
            f"        from {module_name} import {class_name}",
            "",
            f"        # Given - Paramètres de construction",
            f"        params = {{}",
            "",
            f"        # When - Création de l'instance",
            f"        instance = {class_name}(**params)",
            "",
            f"        # Then - Instance créée correctement",
            f"        assert instance is not None",
        ]
    
    def create_test_file(self, test_code: str, output_path: str):
        """Crée le fichier de test"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        print(f"✅ Tests générés : {output_path}")


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Génère des tests de non-régression')
    parser.add_argument('--files', nargs='+', help='Fichiers modifiés')
    parser.add_argument('--output', default='tests/regression/test_auto_generated.py', 
                       help='Fichier de sortie')
    
    args = parser.parse_args()
    
    if not args.files:
        print("ℹ️ Aucun fichier spécifié. Utilisation des modèles par défaut.")
        # Exemple avec les fichiers critiques
        args.files = [
            'app/services/consultant_service.py',
            'app/database/models.py',
            'app/pages_modules/consultant_info.py'
        ]
    
    generator = TestGenerator()
    impacted = generator.analyze_changed_files(args.files)
    
    if impacted:
        test_code = generator.generate_regression_tests(impacted)
        generator.create_test_file(test_code, args.output)
        
        print(f"📊 {len(impacted)} modules analysés")
        print(f"📝 Tests générés dans {args.output}")
    else:
        print("❌ Aucun composant impacté trouvé")


if __name__ == '__main__':
    main()