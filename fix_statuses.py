#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script pour remplacer les statuts restants dans consultant_service.py"""

import re

def fix_remaining_statuses():
    # Lire le fichier
    with open('app/services/consultant_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Contenu avant remplacement:")
    lines = content.split('\n')
    for i, line in enumerate(lines[226:230], 227):
        if 'statut' in line:
            print(f"Ligne {i}: {repr(line)}")
    
    # Remplacer toutes les occurrences restantes de statuts emoji
    # Utiliser une regex plus flexible pour capturer différents encodages
    content = re.sub(
        r'"statut": "[^"]*Disponible"[^"]*if[^"]*else[^"]*"[^"]*Occup[^"]*"',
        '"statut": cls.STATUS_AVAILABLE if row.disponibilite else cls.STATUS_BUSY',
        content,
        flags=re.DOTALL
    )
    
    # Sauvegarder
    with open('app/services/consultant_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Statuts restants remplacés avec succès")

if __name__ == "__main__":
    fix_remaining_statuses()