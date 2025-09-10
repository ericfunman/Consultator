#!/usr/bin/env python3
"""
Script pour corriger automatiquement les erreurs F541 (f-string sans placeholders).
"""

import os
import re
import subprocess
from typing import List, Tuple


def get_f541_errors() -> List[Tuple[str, int, str]]:
    """Récupère toutes les erreurs F541 via flake8."""
    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "flake8",
                "--select=F541",
                "--exclude=.venv_backup,venv,.git",
            ],
            capture_output=True,
            text=True,
            cwd=".",
        )

        errors = []
        for line in result.stdout.strip().split("\n"):
            if line.strip() and "F541" in line:
                parts = line.split(":")
                if len(parts) >= 4:
                    file_path = parts[0].strip(".")
                    if file_path.startswith("\\"):
                        file_path = file_path[1:]
                    line_num = int(parts[1])
                    message = ":".join(parts[3:]).strip()
                    errors.append((file_path, line_num, message))

        return errors
    except Exception as e:
        print(f"Erreur lors de la récupération des erreurs F541: {e}")
        return []


def fix_f541_in_file(file_path: str, line_numbers: List[int]) -> int:
    """Corrige les erreurs F541 dans un fichier spécifique."""
    if not os.path.exists(file_path):
        print(f"Fichier non trouvé: {file_path}")
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        fixes = 0
        for line_num in sorted(line_numbers, reverse=True):
            if 1 <= line_num <= len(lines):
                line = lines[line_num - 1]

                # Pattern pour détecter les f-strings sans placeholders
                # Recherche les f"..." ou f'...' qui ne contiennent pas de {}
                patterns = [
                    (r'f"([^"{}]*)"', r'"\1"'),  # f"string" -> "string"
                    (r"f'([^'{}]*)'", r"'\1'"),  # f'string' -> 'string'
                ]

                original_line = line
                for pattern, replacement in patterns:
                    # Vérifie qu'il n'y a pas de {} dans la chaîne
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        content = match.group(1)
                        if "{" not in content and "}" not in content:
                            line = re.sub(pattern, replacement, line, count=1)
                            fixes += 1
                            break

                if line != original_line:
                    lines[line_num - 1] = line
                    print(
                        f"  Ligne {line_num}: {original_line.strip()} -> {line.strip()}"
                    )

        if fixes > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"✅ {fixes} corrections dans {file_path}")

        return fixes

    except Exception as e:
        print(f"Erreur lors de la correction de {file_path}: {e}")
        return 0


def main():
    print("🔧 Correction automatique des erreurs F541 (f-string sans placeholders)")
    print("=" * 70)

    # Récupérer toutes les erreurs F541
    errors = get_f541_errors()
    if not errors:
        print("Aucune erreur F541 trouvée!")
        return

    print(f"📋 {len(errors)} erreurs F541 trouvées")

    # Grouper par fichier
    files_errors = {}
    for file_path, line_num, message in errors:
        if file_path not in files_errors:
            files_errors[file_path] = []
        files_errors[file_path].append(line_num)

    total_fixes = 0

    # Corriger fichier par fichier
    for file_path, line_numbers in files_errors.items():
        print(f"\n📁 Correction de {file_path} ({len(line_numbers)} erreurs)")
        fixes = fix_f541_in_file(file_path, line_numbers)
        total_fixes += fixes

    print(f"\n🎯 Total: {total_fixes} corrections appliquées")

    # Vérification finale
    print("\n🔍 Vérification des corrections...")
    remaining_errors = get_f541_errors()
    print(f"📊 Erreurs F541 restantes: {len(remaining_errors)}")

    if len(remaining_errors) < len(errors):
        print(f"✅ Succès! {len(errors) - len(remaining_errors)} erreurs corrigées")
    else:
        print("❌ Aucune amélioration détectée")


if __name__ == "__main__":
    main()
