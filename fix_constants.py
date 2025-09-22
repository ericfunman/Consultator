#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script pour remplacer les constantes dupliquées dans consultant_service.py"""

import re

def fix_constants():
    # Lire le fichier
    with open('app/services/consultant_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les statuts - première occurrence
    content = re.sub(
        r'"statut": "✅ Disponible" if row\.disponibilite else "🔴 Occupé"',
        '"statut": cls.STATUS_AVAILABLE if row.disponibilite else cls.STATUS_BUSY',
        content
    )
    
    # Remplacer tous les "En cours"
    content = re.sub(r'"En cours"', 'cls.STATUS_IN_PROGRESS', content)
    
    # Sauvegarder
    with open('app/services/consultant_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Constantes remplacées avec succès")

if __name__ == "__main__":
    fix_constants()