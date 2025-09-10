#!/usr/bin/env python3
"""
Script de correction complète pour éliminer TOUTES les références à self.session
"""

import re
from pathlib import Path


def fix_all_session_references():
    """Corrige toutes les références à self.session restantes"""
    
    chatbot_file = Path("app/services/chatbot_service.py")
    
    if not chatbot_file.exists():
        print(f"❌ Fichier non trouvé: {chatbot_file}")
        return False
    
    print(f"🔧 Correction complète des sessions dans {chatbot_file}")
    
    # Lire le contenu
    with open(chatbot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Remplacements simples ligne par ligne
    simple_replacements = [
        # Statistiques et comptages
        (r'(\s+)consultants_total = self\.session\.query\(Consultant\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    consultants_total = session.query(Consultant).count()'),
        
        (r'(\s+)missions_total = self\.session\.query\(Mission\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    missions_total = session.query(Mission).count()'),
        
        (r'(\s+)practices_total = self\.session\.query\(Practice\)\.filter\(Practice\.actif\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    practices_total = session.query(Practice).filter(Practice.actif).count()'),
        
        (r'(\s+)cvs_total = self\.session\.query\(CV\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    cvs_total = session.query(CV).count()'),
        
        (r'(\s+)consultants_avec_cv = self\.session\.query\(Consultant\)\.join\(CV\)\.distinct\(\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    consultants_avec_cv = session.query(Consultant).join(CV).distinct().count()'),
        
        # Requêtes avec filtres
        (r'(\s+)self\.session\.query\(Consultant\)\.filter\(Consultant\.disponibilite\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    session.query(Consultant).filter(Consultant.disponibilite).count()'),
        
        (r'(\s+)self\.session\.query\(Mission\)\.filter\(Mission\.statut == "en_cours"\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    session.query(Mission).filter(Mission.statut == "en_cours").count()'),
        
        # Moyennes et fonctions
        (r'(\s+)self\.session\.query\(func\.avg\(Mission\.taux_journalier\)\)',
         r'\1with get_database_session() as session:\n\1    session.query(func.avg(Mission.taux_journalier))'),
        
        (r'(\s+)self\.session\.query\(func\.avg\(Consultant\.salaire_actuel\)\)',
         r'\1with get_database_session() as session:\n\1    session.query(func.avg(Consultant.salaire_actuel))'),
    ]
    
    for pattern, replacement in simple_replacements:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes_made += 1
            print(f"✅ Corrigé pattern: {pattern[:60]}...")
    
    # Gestion des requêtes multi-lignes complexes
    complex_patterns = [
        # Pattern pour les requêtes qui s'étendent sur plusieurs lignes
        (r'(\s+)(cvs_total = )?self\.session\.query\(CV\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    \2session.query(CV).count()'),
        
        (r'(\s+)(consultants_avec_cv = )?self\.session\.query\(Consultant\)\.join\(CV\)\.distinct\(\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    \2session.query(Consultant).join(CV).distinct().count()'),
        
        # Queries dans des blocs
        (r'(\s+)self\.session\.query\(Consultant, func\.count\(CV\.id\)\.label\("nb_cvs"\)\)',
         r'\1with get_database_session() as session:\n\1    session.query(Consultant, func.count(CV.id).label("nb_cvs"))'),
        
        (r'(\s+)self\.session\.query\(Consultant\)',
         r'\1with get_database_session() as session:\n\1    session.query(Consultant)'),
        
        (r'(\s+)self\.session\.query\(Mission\)',
         r'\1with get_database_session() as session:\n\1    session.query(Mission)'),
        
        (r'(\s+)self\.session\.query\(Practice\)',
         r'\1with get_database_session() as session:\n\1    session.query(Practice)'),
        
        (r'(\s+)self\.session\.query\(ConsultantCompetence\)',
         r'\1with get_database_session() as session:\n\1    session.query(ConsultantCompetence)'),
    ]
    
    for pattern, replacement in complex_patterns:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes_made += 1
            print(f"✅ Corrigé pattern complexe: {pattern[:60]}...")
    
    # Correction spéciale pour les affectations directes restantes
    remaining_patterns = [
        (r'(\s+)disponibles_count = \n\s+self\.session\.query\(Consultant\)\.filter\(Consultant\.disponibilite\)\.count\(\)',
         r'\1with get_database_session() as session:\n\1    disponibles_count = session.query(Consultant).filter(Consultant.disponibilite).count()'),
    ]
    
    for pattern, replacement in remaining_patterns:
        old_content = content
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if content != old_content:
            changes_made += 1
            print(f"✅ Corrigé pattern spécial: {pattern[:60]}...")
    
    # Vérification finale - remplacement global de tous les self.session restants
    remaining_self_session = re.findall(r'self\.session', content)
    if remaining_self_session:
        print(f"⚠️ Attention: {len(remaining_self_session)} références à self.session encore trouvées")
        # Remplacement global basique
        content = content.replace('self.session', 'session')
        print("🔧 Remplacement global appliqué (à vérifier manuellement)")
        changes_made += 1
    
    # Écrire le fichier modifié
    if content != original_content:
        with open(chatbot_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {changes_made} corrections totales appliquées")
        return True
    else:
        print("ℹ️ Aucune correction nécessaire")
        return False


if __name__ == "__main__":
    try:
        success = fix_all_session_references()
        if success:
            print("\n🎉 Correction complète terminée!")
            print("⚠️ IMPORTANT: Vérifiez que les context managers sont correctement indentés")
            print("💡 Le chatbot ne devrait plus avoir d'erreurs 'session' maintenant")
        else:
            print("\n⚠️ Aucune correction appliquée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
