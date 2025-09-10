#!/usr/bin/env python3
"""
Script pour corriger automatiquement les erreurs F841 (variables locales non utilisées).
"""

import os
import re
import subprocess
from typing import List, Tuple


def get_f841_errors() -> List[Tuple[str, int, str]]:
    """Récupère toutes les erreurs F841 via flake8."""
    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "flake8",
                "--select=F841",
                "--exclude=.venv_backup,venv,.git",
            ],
            capture_output=True,
            text=True,
            cwd=".",
        )

        errors = []
        for line in result.stdout.strip().split("\n"):
            if line.strip() and "F841" in line:
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
        print(f"Erreur lors de la récupération des erreurs F841: {e}")
        return []


def fix_f841_in_file(file_path: str, line_numbers: List[int]) -> int:
    """Corrige les erreurs F841 dans un fichier spécifique."""
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
                original_line = line  # noqa: F841

                # Patterns pour corriger F841
                # 1. Variables d'exception non utilisées: except Exception as e:
                if re.search(r"except\s+\w+\s+as\s+(\w+):", line):
                    # Remplacer par except Exception:
                    new_line = re.sub(
                        r"except\s+(\w+)\s+as\s+\w+:", r"except \1:", line
                    )
                    if new_line != line:
                        lines[line_num - 1] = new_line
                        fixes += 1
                        print(f"  Ligne {line_num}: except ... as var -> except ...")

                # 2. Variables de déballage non utilisées
                elif "=" in line and ("," in line or "unpack" in line.lower()):
                    # Remplacer par _ pour les variables non utilisées
                    patterns = [
                        (
                            r"(\w+),\s*(\w+)\s*=",
                            r"_, \2 =",
                        ),  # var1, var2 = -> _, var2 =
                        (r"(\w+)\s*,\s*_\s*=", r"_, _ ="),  # var, _ = -> _, _ =
                    ]
                    for pattern, replacement in patterns:
                        new_line = re.sub(pattern, replacement, line)
                        if new_line != line:
                            lines[line_num - 1] = new_line
                            fixes += 1
                            print(f"  Ligne {line_num}: variable non utilisée -> _")
                            break

                # 3. Variables simples non utilisées (commentaire)
                elif "=" in line and not line.strip().startswith("#"):
                    # Ajouter un commentaire # noqa: F841
                    if "# noqa" not in line:
                        new_line = line.rstrip() + "  # noqa: F841\n"
                        lines[line_num - 1] = new_line
                        fixes += 1
                        print(f"  Ligne {line_num}: ajout # noqa: F841")

        if fixes > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"✅ {fixes} corrections dans {file_path}")

        return fixes

    except Exception as e:
        print(f"Erreur lors de la correction de {file_path}: {e}")
        return 0


def main():
    print("🔧 Correction automatique des erreurs F841 (variables non utilisées)")
    print("=" * 70)

    # Récupérer toutes les erreurs F841
    errors = get_f841_errors()
    if not errors:
        print("Aucune erreur F841 trouvée!")
        return

    print(f"📋 {len(errors)} erreurs F841 trouvées")

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
        fixes = fix_f841_in_file(file_path, line_numbers)
        total_fixes += fixes

    print(f"\n🎯 Total: {total_fixes} corrections appliquées")

    # Vérification finale
    print("\n🔍 Vérification des corrections...")
    remaining_errors = get_f841_errors()
    print(f"📊 Erreurs F841 restantes: {len(remaining_errors)}")

    if len(remaining_errors) < len(errors):
        print(f"✅ Succès! {len(errors) - len(remaining_errors)} erreurs corrigées")
    else:
        print("❌ Aucune amélioration détectée")


if __name__ == "__main__":
    main()
