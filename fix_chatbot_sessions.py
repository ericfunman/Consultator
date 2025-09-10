#!/usr/bin/env python3
"""
Script pour corriger les sessions de base de données dans ChatbotService
Remplace self.session par des sessions context-managed pour éviter les timeouts
"""

import re
import sys
from pathlib import Path


def fix_chatbot_sessions():
    """Corrige les utilisations de self.session dans le ChatbotService"""
    
    chatbot_file = Path("app/services/chatbot_service.py")
    
    if not chatbot_file.exists():
        print(f"❌ Fichier non trouvé: {chatbot_file}")
        return False
    
    print(f"🔧 Correction des sessions dans {chatbot_file}")
    
    # Lire le contenu
    with open(chatbot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Patterns à corriger
    corrections = [
        # Remplacer self.session.query par with get_database_session() as session:
        (
            r'(\s+)all_consultants = self\.session\.query\(Consultant\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    all_consultants = session.query(Consultant).all()'
        ),
        (
            r'(\s+)all_competences = self\.session\.query\(Competence\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    all_competences = session.query(Competence).all()'
        ),
        (
            r'(\s+)all_langues = self\.session\.query\(Langue\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    all_langues = session.query(Langue).all()'
        ),
        (
            r'(\s+)all_practices = self\.session\.query\(Practice\)\.filter\(Practice\.actif\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    all_practices = session.query(Practice).filter(Practice.actif).all()'
        ),
        (
            r'(\s+)consultants = self\.session\.query\(Consultant\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    consultants = session.query(Consultant).all()'
        ),
        (
            r'(\s+)practices = self\.session\.query\(Practice\)\.filter\(Practice\.actif\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    practices = session.query(Practice).filter(Practice.actif).all()'
        ),
    ]
    
    changes_made = 0
    
    for pattern, replacement in corrections:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)
            print(f"✅ Corrigé {len(matches)} occurrence(s) de: {pattern}")
    
    # Corrections plus complexes pour les requêtes multi-lignes
    complex_patterns = [
        # Disponibilité consultants
        (
            r'(\s+)self\.session\.query\(Consultant\)\.filter\(Consultant\.disponibilite\)\.all\(\)',
            r'\1with get_database_session() as session:\n\1    session.query(Consultant).filter(Consultant.disponibilite).all()'
        ),
        # Autres patterns complexes peuvent être ajoutés ici
    ]
    
    for pattern, replacement in complex_patterns:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)
            print(f"✅ Corrigé {len(matches)} pattern(s) complexe(s)")
    
    # Écrire le fichier modifié
    if content != original_content:
        with open(chatbot_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {changes_made} corrections appliquées dans {chatbot_file}")
        return True
    else:
        print("ℹ️ Aucune correction nécessaire")
        return False


if __name__ == "__main__":
    try:
        success = fix_chatbot_sessions()
        if success:
            print("\n🎉 Corrections terminées avec succès!")
            print("💡 Le chatbot utilise maintenant des sessions fraîches pour éviter les timeouts")
        else:
            print("\n⚠️ Aucune correction appliquée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
