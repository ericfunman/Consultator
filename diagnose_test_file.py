#!/usr/bin/env python3
"""
Script pour diagnostiquer et corriger les problèmes d'encodage dans test_consultants_page.py
"""

def diagnose_and_fix_test_file():
    file_path = r"c:\Users\b302gja\Documents\Consultator en cours\Consultator\tests\unit\pages_modules\test_consultants_page.py"

    # Lire en mode binaire pour voir les bytes
    with open(file_path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data)} bytes")

    # Chercher les séquences problématiques
    problematic_positions = []
    for i in range(len(data)):
        if data[i] == 0xe9:  # Caractère spécial é
            problematic_positions.append(i)

    print(f"Found {len(problematic_positions)} problematic positions with \\xe9:")
    for pos in problematic_positions[:5]:  # Afficher les 5 premiers
        context = data[max(0, pos-10):pos+10]
        print(f"Position {pos}: {repr(context)}")

    # Essayer de lire avec différents encodages
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✅ Successfully read with {encoding} encoding")

            # Chercher la ligne 21
            lines = content.split('\n')
            if len(lines) > 20:
                print(f"Line 21: {repr(lines[20])}")

            # Si latin-1 fonctionne, réencoder en UTF-8
            if encoding == 'latin-1':
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ File re-encoded from latin-1 to UTF-8")
            break
        except UnicodeDecodeError as e:
            print(f"❌ Failed with {encoding}: {e}")

if __name__ == "__main__":
    diagnose_and_fix_test_file()