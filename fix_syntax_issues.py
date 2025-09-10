#!/usr/bin/env python3
"""
Script de correction spécifique pour les problèmes de syntaxe des parenthèses et context managers
"""

import re
from pathlib import Path


def fix_syntax_issues():
    """Corrige les problèmes de syntaxe causés par les corrections automatiques"""
    
    chatbot_file = Path("app/services/chatbot_service.py")
    
    print(f"🔧 Correction des problèmes de syntaxe dans {chatbot_file}")
    
    with open(chatbot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Pattern problématique : variable = ( \n with get_database_session()...
    problematic_pattern = r'(\s+)(\w+) = \(\s*\n\s+with get_database_session\(\) as session:\s*\n\s+(session\.query\([^)]+\)[^)]*\))\s*\)'
    
    def fix_parentheses_issue(match):
        indent = match.group(1)
        var_name = match.group(2)
        query = match.group(3)
        
        return f"""{indent}with get_database_session() as session:
{indent}    {var_name} = {query}"""
    
    # Appliquer la correction
    new_content = re.sub(problematic_pattern, fix_parentheses_issue, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les problèmes de parenthèses avec context managers")
    
    # Pattern pour les return statements
    return_pattern = r'(\s+)return \(\s*\n\s+with get_database_session\(\) as session:\s*\n\s+(session\.query\([^)]*\))\s*\)'
    
    def fix_return_issue(match):
        indent = match.group(1)
        query = match.group(2)
        
        return f"""{indent}with get_database_session() as session:
{indent}    return {query}"""
    
    new_content = re.sub(return_pattern, fix_return_issue, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les problèmes de return avec context managers")
    
    # Pattern plus général pour les assignations multi-lignes
    multiline_pattern = r'(\s+)(\w+) = \(\s*\n\s+with get_database_session\(\) as session:\s*\n(\s+)(session\.query\([^)]+\)(?:\s*\.[^)]+)*)\s*\)'
    
    def fix_multiline_assignment(match):
        indent = match.group(1)
        var_name = match.group(2)
        query_indent = match.group(3)
        query = match.group(4)
        
        return f"""{indent}with get_database_session() as session:
{indent}    {var_name} = (
{query_indent}    {query}
{indent}    )"""
    
    new_content = re.sub(multiline_pattern, fix_multiline_assignment, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les assignations multi-lignes")
    
    # Écrire le fichier modifié
    if content != original_content:
        with open(chatbot_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {changes_made} corrections de syntaxe appliquées")
        return True
    else:
        print("ℹ️ Aucune correction de syntaxe nécessaire")
        return False


if __name__ == "__main__":
    try:
        success = fix_syntax_issues()
        if success:
            print("\n🎉 Correction de syntaxe terminée!")
            print("🔍 Vérification de la syntaxe...")
            
            # Vérifier la syntaxe
            import subprocess
            result = subprocess.run(['python', '-m', 'py_compile', 'app/services/chatbot_service.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Syntaxe correcte !")
            else:
                print(f"❌ Erreurs de syntaxe restantes:\n{result.stderr}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
