#!/usr/bin/env python3
"""
Script pour corriger les tests de régression qui utilisent l'ancienne API
"""

import os
import re

def fix_regression_tests():
    """Corrige les tests de régression avec la nouvelle API"""
    
    test_file = "tests/regression_backup/test_service_regression.py"
    
    if not os.path.exists(test_file):
        print(f"❌ Fichier {test_file} non trouvé")
        return
    
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Corriger l'import des modèles
    if 'from app.database.models import' in content:
        # Ajouter ConsultantCompetence aux imports
        content = re.sub(
            r'from app\.database\.models import ([^\n]+)',
            r'from app.database.models import \1, ConsultantCompetence',
            content
        )
    
    # 2. Corriger la création de Competence avec consultant_id
    # Remplacer:
    # competence = Competence(consultant_id=consultant.id, nom='Test Skill', niveau=3)
    # Par:
    # competence = Competence(nom='Test Skill', categorie='technique')
    # consultant_competence = ConsultantCompetence(consultant_id=consultant.id, competence_id=competence.id, niveau_maitrise='intermediaire')
    
    # Trouver et remplacer les patterns Competence
    patterns = [
        # Pattern pour Competence avec consultant_id
        (
            r'competence = Competence\(\s*consultant_id=consultant\.id,\s*nom=[\'"]([^\'\"]+)[\'"],\s*niveau=(\d+)\s*\)',
            r'''competence = Competence(
            nom="\\1",
            categorie="technique"
        )
        db_session.add(competence)
        db_session.flush()
        
        consultant_competence = ConsultantCompetence(
            consultant_id=consultant.id,
            competence_id=competence.id,
            niveau_maitrise="intermediaire",
            annees_experience=float(\\2)
        )'''
        ),
        
        # Pattern pour Mission si nécessaire - vérifier le modèle Mission
        # Pour l'instant on laisse tel quel car on ne sait pas si Mission a changé
        
        # Corriger les add_all pour inclure consultant_competence
        (
            r'db_session\.add_all\(\[competence, mission\]\)',
            'db_session.add_all([competence, consultant_competence, mission])'
        )
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    # 3. S'assurer que les imports sont corrects
    if 'ConsultantCompetence' not in content:
        # Ajouter l'import si pas déjà là
        content = content.replace(
            'from app.database.models import',
            'from app.database.models import ConsultantCompetence, '
        )
    
    # Sauvegarder
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fichier {test_file} corrigé")

def check_mission_model():
    """Vérifier si le modèle Mission a aussi changé"""
    models_file = "app/database/models.py"
    
    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher la définition de Mission
    if 'class Mission(' in content:
        start = content.find('class Mission(')
        if start != -1:
            # Trouver la fin de la classe (prochaine classe ou fin de fichier)
            end = content.find('\nclass ', start + 1)
            if end == -1:
                end = len(content)
            
            mission_def = content[start:end]
            print("📋 Définition du modèle Mission:")
            print("="*50)
            # Prendre les 30 premières lignes pour voir la structure
            lines = mission_def.split('\n')[:30]
            for i, line in enumerate(lines, 1):
                print(f"{i:2}: {line}")
            print("="*50)

if __name__ == "__main__":
    print("🔧 Correction des tests de régression...")
    check_mission_model()
    print()
    fix_regression_tests()
    print("✅ Correction terminée !")