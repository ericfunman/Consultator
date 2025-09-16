#!/usr/bin/env python3
"""
Script pour corriger automatiquement les f-strings multi-lignes
qui causent des erreurs de syntaxe sur Python 3.10/Linux
"""
import os
import re
import glob

def fix_multiline_fstrings(file_path):
    """Corrige les f-strings multi-lignes dans un fichier"""
    print(f"🔍 Traitement de {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern pour détecter les f-strings multi-lignes
    # f"...{
    #     variable...
    # }"
    pattern = r'f"([^"]*?){\s*\n\s*([^}]*?)\s*\n\s*([^}]*?)}'
    
    def replace_multiline_fstring(match):
        prefix = match.group(1)
        var_part1 = match.group(2).strip()
        var_part2 = match.group(3).strip()
        
        # Reconstituer la variable complète
        full_var = f"{var_part1}{var_part2}"
        
        # Retourner la f-string sur une seule ligne
        return f'f"{prefix}{{{full_var}}}'
    
    # Appliquer la correction
    content = re.sub(pattern, replace_multiline_fstring, content, flags=re.MULTILINE | re.DOTALL)
    
    # Pattern plus simple pour les cas basiques
    pattern2 = r'f"([^"]*?){\s*\n\s*([^}]*?)}'
    
    def replace_simple_multiline(match):
        prefix = match.group(1)
        var_part = match.group(2).strip()
        return f'f"{prefix}{{{var_part}}}'
    
    content = re.sub(pattern2, replace_simple_multiline, content, flags=re.MULTILINE | re.DOTALL)
    
    if content != original_content:
        print(f"✅ Corrections appliquées dans {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        print(f"ℹ️ Aucune correction nécessaire dans {file_path}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Correction automatique des f-strings multi-lignes")
    
    # Fichiers Python à traiter
    pattern = "app/**/*.py"
    files = glob.glob(pattern, recursive=True)
    
    fixed_count = 0
    for file_path in files:
        if fix_multiline_fstrings(file_path):
            fixed_count += 1
    
    print(f"\n✅ Terminé ! {fixed_count} fichier(s) corrigé(s)")

if __name__ == "__main__":
    main()
