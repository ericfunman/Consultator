#!/usr/bin/env python3
"""
Script pour corriger l'encodage UTF-8 du fichier consultant_service.py
"""

def fix_encoding():
    file_path = r"c:\Users\b302gja\Documents\Consultator en cours\Consultator\app\services\consultant_service.py"

    # Lire avec latin-1
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()

    # Réécrire avec UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Fichier réencodé avec succès de latin-1 vers UTF-8")

    # Vérifier que ça fonctionne maintenant
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            test_content = f.read()
        print("✅ Le fichier peut maintenant être lu en UTF-8")
    except UnicodeDecodeError as e:
        print(f"❌ Problème persistant: {e}")

if __name__ == "__main__":
    fix_encoding()