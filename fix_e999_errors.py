#!/usr/bin/env python3
"""
Script pour corriger automatiquement les erreurs E999 (problèmes de syntaxe et d'indentation).
"""

import os
import re
import subprocess
from typing import List, Tuple


def get_e999_errors() -> List[Tuple[str, int, str]]:
    """Récupère toutes les erreurs E999 via flake8."""
    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "flake8",
                "--select=E999",
                "--exclude=.venv_backup,venv,.git",
            ],
            capture_output=True,
            text=True,
            cwd=".",
        )

        errors = []
        for line in result.stdout.strip().split("\n"):
            if line.strip() and "E999" in line:
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
        print(f"Erreur lors de la récupération des erreurs E999: {e}")
        return []


def fix_indentation_in_file(file_path: str, error_lines: List[int]) -> int:
    """Corrige les erreurs d'indentation dans un fichier."""
    if not os.path.exists(file_path):
        print(f"Fichier non trouvé: {file_path}")
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        fixes = 0

        # Analyser chaque ligne d'erreur
        for error_line in error_lines:
            if 1 <= error_line <= len(lines):
                line = lines[error_line - 1]

                # Vérifier si c'est un problème d'import mal placé
                if (
                    "import" in line
                    and error_line > 5
                    and not line.strip().startswith("#")
                    and line.strip().startswith((" ", "\t"))
                ):
                    # Déplacer l'import vers le haut du fichier
                    import_line = line.strip()

                    # Supprimer la ligne actuelle
                    lines[error_line - 1] = ""

                    # Trouver où insérer l'import (après les imports existants)
                    insert_pos = 0
                    for i, l in enumerate(
                        lines[:20]
                    ):  # Chercher dans les 20 premières lignes
                        if l.strip().startswith(
                            ("import ", "from ")
                        ) and not l.strip().startswith("#"):
                            insert_pos = i + 1

                    # Insérer l'import
                    lines.insert(insert_pos, import_line + "\n")
                    fixes += 1
                    print(
                        f"  Import déplacé ligne {error_line} -> ligne {insert_pos + 1}"
                    )

                # Problème d'indentation après try/except/if
                elif "expected an indented block" in str(error_lines):
                    # Ajouter une instruction pass si le bloc est vide
                    if error_line <= len(lines) and lines[error_line - 1].strip() == "":
                        lines[error_line - 1] = "        pass\n"
                        fixes += 1
                        print(f"  Ajout de 'pass' ligne {error_line}")

        if fixes > 0:
            # Nettoyer les lignes vides multiples
            cleaned_lines = []
            empty_count = 0
            for line in lines:
                if line.strip() == "":
                    empty_count += 1
                    if empty_count <= 2:  # Maximum 2 lignes vides consécutives
                        cleaned_lines.append(line)
                else:
                    empty_count = 0
                    cleaned_lines.append(line)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(cleaned_lines)

            print(f"✅ {fixes} corrections dans {file_path}")

        return fixes

    except Exception as e:
        print(f"Erreur lors de la correction de {file_path}: {e}")
        return 0


def main():
    print("🔧 Correction automatique des erreurs E999 (syntaxe/indentation)")
    print("=" * 70)

    # Récupérer toutes les erreurs E999
    errors = get_e999_errors()
    if not errors:
        print("Aucune erreur E999 trouvée!")
        return

    print(f"📋 {len(errors)} erreurs E999 trouvées")

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
        fixes = fix_indentation_in_file(file_path, line_numbers)
        total_fixes += fixes

    print(f"\n🎯 Total: {total_fixes} corrections appliquées")

    # Vérification finale
    print("\n🔍 Vérification des corrections...")
    remaining_errors = get_e999_errors()
    print(f"📊 Erreurs E999 restantes: {len(remaining_errors)}")

    if len(remaining_errors) < len(errors):
        print(f"✅ Succès! {len(errors) - len(remaining_errors)} erreurs corrigées")
    else:
        print("❌ Aucune amélioration détectée - correction manuelle nécessaire")


if __name__ == "__main__":
    main()
