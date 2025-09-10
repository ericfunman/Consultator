#!/usr/bin/env python3
"""
Script de correction complet pour tous les problèmes de syntaxe
"""

import re
from pathlib import Path


def fix_all_syntax_issues():
    """Corrige tous les problèmes de syntaxe dans le fichier chatbot"""
    
    chatbot_file = Path("app/services/chatbot_service.py")
    
    print(f"🔧 Correction complète des problèmes de syntaxe dans {chatbot_file}")
    
    with open(chatbot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # 1. Corriger les return (with get_database_session()...
    pattern1 = r'(\s+)return \(\s*\n\s+with get_database_session\(\) as session:\s*\n\s+(session\.query\([^)]*\)(?:\s*\.[^)]*)*)\s*\)'
    
    def fix_return_with(match):
        indent = match.group(1)
        query = match.group(2)
        
        return f"""{indent}with get_database_session() as session:
{indent}    return {query}"""
    
    new_content = re.sub(pattern1, fix_return_with, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les return avec context managers")
    
    # 2. Corriger les assignations avec (
    pattern2 = r'(\s+)(\w+) = \(\s*\n\s+with get_database_session\(\) as session:\s*\n\s+(session\.query\([^)]*\)(?:\s*\.[^)]*)*)\s*\)'
    
    def fix_assignment_with(match):
        indent = match.group(1)
        var_name = match.group(2)
        query = match.group(3)
        
        return f"""{indent}with get_database_session() as session:
{indent}    {var_name} = {query}"""
    
    new_content = re.sub(pattern2, fix_assignment_with, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les assignations avec context managers")
    
    # 3. Corriger les return multilignes plus complexes
    complex_pattern = r'(\s+)return \(\s*\n\s+with get_database_session\(\) as session:\s*\n\s+(session\.query\([^)]*\)\s*\n\s*\.filter\([^)]*\)\s*\n\s*\.all\(\))\s*\)'
    
    def fix_complex_return(match):
        indent = match.group(1)
        query = match.group(2)
        
        # Nettoyer et reformater la requête
        query_lines = query.split('\n')
        formatted_query = '\n'.join([f"{indent}    {line.strip()}" for line in query_lines if line.strip()])
        
        return f"""{indent}with get_database_session() as session:
{formatted_query}"""
    
    new_content = re.sub(complex_pattern, fix_complex_return, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les return complexes avec context managers")
    
    # 4. Pattern plus général pour capturer tous les cas restants
    general_pattern = r'(\s+)return \(\s*\n\s+with get_database_session\(\) as session:\s*\n([^)]*)\s*\)'
    
    def fix_general_return(match):
        indent = match.group(1)
        query_content = match.group(2)
        
        # Nettoyer le contenu de la requête
        lines = query_content.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                formatted_lines.append(f"{indent}    {line.strip()}")
        
        formatted_query = '\n'.join(formatted_lines)
        
        # Si c'est un return, ajouter return à la première ligne de requête
        if formatted_lines:
            first_line = formatted_lines[0]
            if not first_line.strip().startswith('return'):
                first_line = first_line.replace(f"{indent}    ", f"{indent}    return ")
                formatted_lines[0] = first_line
        
        formatted_query = '\n'.join(formatted_lines)
        
        return f"""{indent}with get_database_session() as session:
{formatted_query}"""
    
    new_content = re.sub(general_pattern, fix_general_return, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        changes_made += 1
        content = new_content
        print("✅ Corrigé les patterns généraux")
    
    # Écrire le fichier modifié
    if content != original_content:
        with open(chatbot_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {changes_made} types de corrections appliquées")
        return True
    else:
        print("ℹ️ Aucune correction nécessaire")
        return False


if __name__ == "__main__":
    try:
        success = fix_all_syntax_issues()
        if success:
            print("\n🎉 Correction complète terminée!")
            print("🔍 Vérification de la syntaxe...")
            
            # Vérifier la syntaxe
            import subprocess
            result = subprocess.run(['python', '-m', 'py_compile', 'app/services/chatbot_service.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Syntaxe correcte !")
            else:
                print(f"❌ Erreurs de syntaxe restantes:\n{result.stderr}")
                
                # Afficher les premières lignes de l'erreur pour diagnostiquer
                lines = result.stderr.split('\n')
                for line in lines[:10]:
                    if line.strip():
                        print(f"  {line}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
