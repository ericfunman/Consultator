#!/usr/bin/env python3
"""
Script avancé pour corriger TOUS les usages de self.session dans ChatbotService
Approche par méthode pour gérer les context managers correctement
"""

import re
from pathlib import Path


def fix_method_sessions():
    """Corrige les méthodes qui utilisent self.session de manière intensive"""
    
    chatbot_file = Path("app/services/chatbot_service.py")
    
    if not chatbot_file.exists():
        print(f"❌ Fichier non trouvé: {chatbot_file}")
        return False
    
    print(f"🔧 Correction avancée des sessions dans {chatbot_file}")
    
    # Lire le contenu
    with open(chatbot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Fonction pour wrap une méthode avec un context manager
    def wrap_method_with_session(method_name, content):
        # Pattern pour trouver la méthode
        method_pattern = rf'(    def {method_name}\([^)]*\):[^:]*?:.*?\n)(.*?)(\n    def |\nclass |\Z)'
        
        match = re.search(method_pattern, content, re.DOTALL)
        if not match:
            return content, 0
        
        method_signature = match.group(1)
        method_body = match.group(2)
        next_section = match.group(3)
        
        # Vérifier si la méthode utilise self.session
        if 'self.session' not in method_body:
            return content, 0
        
        # Ajouter le context manager au début du corps de la méthode
        lines = method_body.split('\n')
        
        # Trouver la première ligne significative (pas les docstrings/commentaires)
        first_code_line_idx = 0
        in_docstring = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.endswith('"""') or stripped.endswith("'''"):
                    # Docstring sur une ligne
                    continue
                else:
                    # Début de docstring multi-ligne
                    in_docstring = not in_docstring
                    continue
            elif in_docstring:
                if stripped.endswith('"""') or stripped.endswith("'''"):
                    in_docstring = False
                continue
            elif stripped.startswith('#') or not stripped:
                continue
            else:
                first_code_line_idx = i
                break
        
        # Insérer le context manager
        indent = '        '  # 8 spaces pour être dans la méthode
        session_context = f"{indent}with get_database_session() as session:"
        
        # Remplacer self.session par session dans le corps
        new_body_lines = []
        for i, line in enumerate(lines):
            if i == first_code_line_idx:
                # Ajouter le context manager avant la première ligne de code
                new_body_lines.append(session_context)
                # Indenter la ligne actuelle
                new_line = line.replace('self.session', 'session')
                if line.strip():  # Si ce n'est pas une ligne vide
                    new_line = '    ' + new_line  # Ajouter 4 espaces d'indentation
                new_body_lines.append(new_line)
            else:
                # Remplacer self.session et ajuster l'indentation si nécessaire
                new_line = line.replace('self.session', 'session')
                if line.strip() and not line.startswith('        #') and 'self.session' in line:
                    # Ajouter indentation pour être dans le context manager
                    new_line = '    ' + new_line
                new_body_lines.append(new_line)
        
        new_method_body = '\n'.join(new_body_lines)
        
        # Reconstruire la méthode
        new_method = method_signature + new_method_body + next_section
        
        # Remplacer dans le contenu
        old_method = method_signature + method_body + next_section
        new_content = content.replace(old_method, new_method)
        
        return new_content, 1
    
    # Liste des méthodes critiques à corriger
    critical_methods = [
        '_generate_statistics',
        '_handle_availability_question',
        '_handle_cv_question',
        '_handle_performance_question',
        '_handle_statistics_question'
    ]
    
    for method_name in critical_methods:
        content, changes = wrap_method_with_session(method_name, content)
        changes_made += changes
        if changes:
            print(f"✅ Méthode {method_name} corrigée")
    
    # Corrections simples pour les lignes isolées restantes
    simple_replacements = [
        (r'(\s+)consultants_total = self\.session\.query\(Consultant\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    consultants_total = session.query(Consultant).count()'),
        (r'(\s+)missions_total = self\.session\.query\(Mission\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    missions_total = session.query(Mission).count()'),
        (r'(\s+)practices_total = self\.session\.query\(Practice\)\.filter\(Practice\.actif\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    practices_total = session.query(Practice).filter(Practice.actif).count()'),
        (r'(\s+)cvs_total = self\.session\.query\(CV\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    cvs_total = session.query(CV).count()'),
    ]
    
    for pattern, replacement in simple_replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made += 1
            print(f"✅ Pattern simple corrigé: {pattern[:50]}...")
    
    # Écrire le fichier modifié
    if content != original_content:
        with open(chatbot_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {changes_made} corrections avancées appliquées")
        return True
    else:
        print("ℹ️ Aucune correction avancée nécessaire")
        return False


if __name__ == "__main__":
    try:
        success = fix_method_sessions()
        if success:
            print("\n🎉 Corrections avancées terminées!")
            print("💡 Les méthodes critiques utilisent maintenant des sessions context-managed")
            print("⚡ Cela devrait éliminer les timeouts d'inactivité du chatbot")
        else:
            print("\n⚠️ Aucune correction avancée appliquée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
