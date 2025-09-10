#!/usr/bin/env python3
"""
Script pour corriger automatiquement les erreurs F541 (f-strings sans placeholders)
"""

import os
import re
import subprocess
from pathlib import Path


def get_f541_errors():
    """Récupère la liste des erreurs F541"""
    result = subprocess.run([
        'python', '-m', 'flake8', '--select=F541',
        '--exclude=.venv_backup,venv,.git', '--format=%(path)s:%(row)d:%(col)d: %(text)s'
    ], capture_output=True, text=True)

    errors = []
    for line in result.stdout.strip().split('\n'):
        if line and 'F541' in line:
            parts = line.split(':')
            if len(parts) >= 4:
                file_path = parts[0]
                line_num = int(parts[1])
                errors.append((file_path, line_num))

    return errors


def fix_f541_in_file(file_path, line_num):
    """Corrige une erreur F541 dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if line_num <= len(lines):
            line = lines[line_num - 1]

            # Patterns pour détecter les f-strings sans placeholders
            # Pattern 1: f"text simple sans variables"
            if re.search(r'f["\'][^{]*["\']', line):
                # Remplacer f"text" par "text" si pas de {}
                new_line = re.sub(r'f(["\'][^{]*["\'])', r'\1', line)
                if new_line != line:
                    lines[line_num - 1] = new_line

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    print(f"✅ Corrigé {file_path}:{line_num}")
                    return True

        return False

    except Exception as e:
        print(f"❌ Erreur dans {file_path}:{line_num} - {e}")
        return False


def main():
    print("🔧 Correction automatique des erreurs F541...")

    errors = get_f541_errors()
    print(f"📊 {len(errors)} erreurs F541 trouvées")

    fixed_count = 0
    for file_path, line_num in errors:
        if fix_f541_in_file(file_path, line_num):
            fixed_count += 1

    print(f"\n✅ {fixed_count} erreurs F541 corrigées automatiquement")

    # Vérifier les erreurs restantes
    remaining_errors = get_f541_errors()
    print(f"📊 {len(remaining_errors)} erreurs F541 restantes")


if __name__ == "__main__":
    main()
