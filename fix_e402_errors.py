#!/usr/bin/env python3
"""
Script pour corriger automatiquement les erreurs E402 (import non en haut de fichier).
"""

import os
import re
import subprocess
from typing import List, Tuple, Dict


def get_e402_errors() -> List[Tuple[str, int, str]]:
    """Récupère toutes les erreurs E402 via flake8."""
    try:
        result = subprocess.run(
            ["python", "-m", "flake8", "--select=E402", "--exclude=.venv_backup,venv,.git"],
            capture_output=True,
            text=True,
            cwd="."
        )

        errors = []
        for line in result.stdout.strip().split('\n'):
            if line.strip() and 'E402' in line:
                parts = line.split(':')
                if len(parts) >= 4:
                    file_path = parts[0].strip('.')
                    if file_path.startswith('\\'):
                        file_path = file_path[1:]
                    line_num = int(parts[1])
                    message = ':'.join(parts[3:]).strip()
                    errors.append((file_path, line_num, message))

        return errors
    except Exception as e:
        print(f"Erreur lors de la récupération des erreurs E402: {e}")
        return []


def analyze_imports_in_file(file_path: str) -> Dict:
    """Analyse la structure des imports dans un fichier."""
    if not os.path.exists(file_path):
        return {"error": f"Fichier non trouvé: {file_path}"}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Trouver les imports et leur position
        imports = []
        non_import_lines = []
        shebang_lines = []
        encoding_lines = []
        docstring_end = 0

        in_docstring = False
        docstring_quotes = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Shebang
            if i == 0 and stripped.startswith('#!'):
                shebang_lines.append(i)
                continue

            # Encoding
            if i <= 1 and re.search(r'coding[:=]\s*([-\w.]+)', line):
                encoding_lines.append(i)
                continue

            # Docstring detection (simple)
            if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
                in_docstring = True
                docstring_quotes = stripped[:3]
                if stripped.count(docstring_quotes) >= 2:
                    # Docstring sur une seule ligne
                    in_docstring = False
                    docstring_end = i + 1
                continue

            if in_docstring and docstring_quotes in stripped:
                in_docstring = False
                docstring_end = i + 1
                continue

            if in_docstring:
                continue

            # Import statements
            if (stripped.startswith('import ') or
                    stripped.startswith('from ') or
                    (stripped.startswith('import') and ' ' in stripped) or
                    (stripped.startswith('from') and ' ' in stripped)):
                imports.append((i, line))
                continue

            # Ligne non vide qui n'est pas un import
            if stripped and not stripped.startswith('#'):
                non_import_lines.append(i)

        return {
            "imports": imports,
            "non_import_lines": non_import_lines,
            "shebang_lines": shebang_lines,
            "encoding_lines": encoding_lines,
            "docstring_end": docstring_end,
            "total_lines": len(lines)
        }

    except Exception as e:
        return {"error": f"Erreur lors de l'analyse de {file_path}: {e}"}


def fix_e402_in_file(file_path: str) -> int:
    """Corrige les erreurs E402 dans un fichier en déplaçant les imports."""
    analysis = analyze_imports_in_file(file_path)

    if "error" in analysis:
        print(f"  ❌ {analysis['error']}")
        return 0

    imports = analysis["imports"]
    non_import_lines = analysis["non_import_lines"]

    if not imports:
        return 0

    # Vérifier s'il y a des imports après du code non-import
    problematic_imports = []
    first_non_import = min(non_import_lines) if non_import_lines else float('inf')

    for line_num, import_line in imports:
        if line_num > first_non_import:
            problematic_imports.append((line_num, import_line))

    if not problematic_imports:
        return 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Position où insérer les imports (après docstring, shebang, encoding)
        insert_position = max(
            analysis["docstring_end"],
            max(analysis["shebang_lines"], default=-1) + 1,
            max(analysis["encoding_lines"], default=-1) + 1
        )

        # Extraire les imports problématiques
        imports_to_move = []
        lines_to_remove = []

        for line_num, import_line in problematic_imports:
            imports_to_move.append(import_line)
            lines_to_remove.append(line_num)

        # Supprimer les imports de leur position actuelle
        for line_num in sorted(lines_to_remove, reverse=True):
            if 0 <= line_num < len(lines):
                lines.pop(line_num)

        # Insérer les imports à la bonne position
        for i, import_line in enumerate(imports_to_move):
            lines.insert(insert_position + i, import_line)

        # Sauvegarder le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"  ✅ {len(problematic_imports)} imports déplacés")
        return len(problematic_imports)

    except Exception as e:
        print(f"  ❌ Erreur lors de la correction: {e}")
        return 0


def main():
    print("🔧 Correction automatique des erreurs E402 (imports mal placés)")
    print("=" * 70)

    # Récupérer toutes les erreurs E402
    errors = get_e402_errors()
    if not errors:
        print("Aucune erreur E402 trouvée!")
        return

    print(f"📋 {len(errors)} erreurs E402 trouvées")

    # Grouper par fichier
    files_errors = {}
    for file_path, line_num, message in errors:
        if file_path not in files_errors:
            files_errors[file_path] = []
        files_errors[file_path].append(line_num)

    total_fixes = 0

    # Corriger fichier par fichier
    for file_path in sorted(files_errors.keys()):
        line_numbers = files_errors[file_path]
        print(f"\n📁 Correction de {file_path} ({len(line_numbers)} erreurs)")

        # Analyser le fichier pour voir s'il est "safe" à corriger
        if any(keyword in file_path.lower() for keyword in ['test_', 'debug', 'temp']):
            print("  ⚠️ Fichier de test/debug détecté - correction prudente")

        fixes = fix_e402_in_file(file_path)
        total_fixes += fixes

    print(f"\n🎯 Total: {total_fixes} corrections appliquées")

    # Vérification finale
    print("\n🔍 Vérification des corrections...")
    remaining_errors = get_e402_errors()
    print(f"📊 Erreurs E402 restantes: {len(remaining_errors)}")

    if len(remaining_errors) < len(errors):
        print(f"✅ Succès! {len(errors) - len(remaining_errors)} erreurs corrigées")
    else:
        print("❌ Aucune amélioration détectée")


if __name__ == "__main__":
    main()
