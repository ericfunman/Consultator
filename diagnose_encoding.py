#!/usr/bin/env python3
"""
Script de diagnostic pour les problèmes d'encodage UTF-8
"""

def diagnose_encoding():
    file_path = r"c:\Users\b302gja\Documents\Consultator en cours\Consultator\app\services\consultant_service.py"

    with open(file_path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data)} bytes")

    # Chercher les séquences UTF-8 problématiques
    problematic_positions = []

    for i in range(len(data) - 1):
        # Chercher les séquences UTF-8 invalides (commençant par 0xc3 mais pas suivies correctement)
        if data[i] == 0xc3:
            if i + 1 < len(data):
                next_byte = data[i + 1]
                # 0xc3 doit être suivi de 0x80-0xbf pour être valide
                if not (0x80 <= next_byte <= 0xbf):
                    problematic_positions.append((i, hex(data[i]), hex(next_byte)))

    print(f"Found {len(problematic_positions)} problematic UTF-8 sequences:")
    for pos, byte1, byte2 in problematic_positions[:10]:  # Afficher les 10 premiers
        context = data[max(0, pos-10):pos+10]
        print(f"Position {pos}: {byte1} {byte2} - Context: {repr(context)}")

    # Essayer de lire avec différents encodages
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✅ Successfully read with {encoding} encoding")
            # Chercher la ligne 928
            lines = content.split('\n')
            if len(lines) > 927:
                print(f"Line 928: {repr(lines[927])}")
            break
        except UnicodeDecodeError as e:
            print(f"❌ Failed with {encoding}: {e}")
        except Exception as e:
            print(f"❌ Error with {encoding}: {e}")

if __name__ == "__main__":
    diagnose_encoding()