#!/usr/bin/env python3
"""
Script de nettoyage automatique des imports inutilisés
Nettoie automatiquement les imports non utilisés dans le projet Python
"""

import ast
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ImportInfo:
    """Informations sur un import"""
    module: str
    name: str
    alias: str = None
    line_number: int = 0
    is_used: bool = False


@dataclass
class FileAnalysis:
    """Résultats d'analyse d'un fichier"""
    file_path: Path
    imports: List[ImportInfo]
    unused_imports: List[ImportInfo]
    used_imports: List[ImportInfo]


class ImportCleaner:
    """Classe principale pour nettoyer les imports"""

    def __init__(self, project_root: str, backup: bool = True):
        self.project_root = Path(project_root)
        self.backup = backup
        self.backup_dir = self.project_root / "backups" / "imports_cleaning"
        self.stats = {
            "files_analyzed": 0,
            "files_modified": 0,
            "imports_removed": 0,
            "errors": 0
        }

        if self.backup:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

    def find_python_files(self) -> List[Path]:
        """Trouve tous les fichiers Python du projet"""
        python_files = []
        exclude_dirs = {
            '__pycache__', '.git', '.venv', 'venv', 'env',
            'node_modules', '.pytest_cache', 'backups'
        }

        for root, dirs, files in os.walk(self.project_root):
            # Exclure les répertoires
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)

        return python_files

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """Analyse un fichier Python pour identifier les imports"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            imports = []
            used_names = set()

            # Analyser l'AST pour trouver les imports et utilisations
            for node in ast.walk(tree):
                # Collecter les imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(ImportInfo(
                            module=alias.name,
                            name=alias.name,
                            alias=alias.asname,
                            line_number=node.lineno
                        ))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports.append(ImportInfo(
                                module=node.module,
                                name=alias.name,
                                alias=alias.asname,
                                line_number=node.lineno
                            ))

                # Collecter les utilisations de noms
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Pour les attributs comme module.Class
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)

            # Marquer les imports utilisés
            for imp in imports:
                # Vérifier le nom principal
                if imp.alias:
                    is_used = imp.alias in used_names
                else:
                    is_used = imp.name in used_names

                # Vérifier aussi dans les commentaires et docstrings
                if not is_used:
                    is_used = self._check_usage_in_comments(content, imp)

                imp.is_used = is_used

            # Séparer imports utilisés et non utilisés
            used_imports = [imp for imp in imports if imp.is_used]
            unused_imports = [imp for imp in imports if not imp.is_used]

            return FileAnalysis(
                file_path=file_path,
                imports=imports,
                unused_imports=unused_imports,
                used_imports=used_imports
            )

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de {file_path}: {e}")
            self.stats["errors"] += 1
            return FileAnalysis(file_path, [], [], [])

    def _check_usage_in_comments(self, content: str, imp: ImportInfo) -> bool:
        """Vérifie si un import est utilisé dans les commentaires/docstrings"""
        lines = content.split('\n')
        if imp.line_number < len(lines):
            # Vérifier quelques lignes après l'import pour les commentaires
            start_line = max(0, imp.line_number - 1)
            end_line = min(len(lines), imp.line_number + 3)

            for i in range(start_line, end_line):
                line = lines[i]
                if '#' in line or '"""' in line or "'''" in line:
                    if imp.alias and imp.alias in line:
                        return True
                    elif imp.name in line:
                        return True

        return False

    def clean_file(self, analysis: FileAnalysis, dry_run: bool = True) -> bool:
        """Nettoie les imports inutilisés d'un fichier"""
        if not analysis.unused_imports:
            return False

        try:
            with open(analysis.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Créer une sauvegarde si demandé
            if self.backup and not dry_run:
                self._create_backup(analysis.file_path)

            lines = content.split('\n')
            lines_to_remove = set()

            # Identifier les lignes à supprimer
            for imp in analysis.unused_imports:
                if imp.line_number <= len(lines):
                    line_idx = imp.line_number - 1
                    line = lines[line_idx].strip()

                    # Vérifier que c'est bien un import
                    if line.startswith(('import ', 'from ')):
                        lines_to_remove.add(line_idx)

                        # Vérifier les lignes suivantes pour les imports multi-lignes
                        for i in range(line_idx + 1, len(lines)):
                            next_line = lines[i].strip()
                            if next_line.startswith(('import ', 'from ', '    ')) or next_line == '':
                                if next_line == '':
                                    lines_to_remove.add(i)
                                elif next_line.startswith('    ') or next_line.startswith('\t'):
                                    lines_to_remove.add(i)
                                else:
                                    break
                            else:
                                break

            if not lines_to_remove:
                return False

            # Supprimer les lignes (en ordre inverse pour préserver les indices)
            for line_idx in sorted(lines_to_remove, reverse=True):
                if line_idx < len(lines):
                    del lines[line_idx]

            # Recréer le contenu
            new_content = '\n'.join(lines)

            if dry_run:
                logger.info(f"[DRY RUN] {analysis.file_path}: {len(lines_to_remove)} lignes à supprimer")
                for imp in analysis.unused_imports:
                    logger.info(f"  - Import inutilisé: {imp.module}.{imp.name}" +
                                (f" as {imp.alias}" if imp.alias else ""))
                return True
            else:
                # Écrire le nouveau contenu
                with open(analysis.file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                logger.info(f"✅ {analysis.file_path}: {len(lines_to_remove)} lignes supprimées")
                self.stats["files_modified"] += 1
                self.stats["imports_removed"] += len(analysis.unused_imports)
                return True

        except Exception as e:
            logger.error(f"Erreur lors du nettoyage de {analysis.file_path}: {e}")
            self.stats["errors"] += 1
            return False

    def _create_backup(self, file_path: Path):
        """Crée une sauvegarde du fichier"""
        try:
            relative_path = file_path.relative_to(self.project_root)
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            import shutil
            shutil.copy2(file_path, backup_path)
            logger.debug(f"Sauvegarde créée: {backup_path}")

        except Exception as e:
            logger.warning(f"Impossible de créer la sauvegarde pour {file_path}: {e}")

    def run_analysis(self, dry_run: bool = True) -> Dict[str, FileAnalysis]:
        """Lance l'analyse complète du projet"""
        logger.info("🔍 Démarrage de l'analyse des imports...")
        logger.info(f"📁 Projet: {self.project_root}")

        python_files = self.find_python_files()
        logger.info(f"📄 {len(python_files)} fichiers Python trouvés")

        results = {}

        for file_path in python_files:
            logger.debug(f"Analysant: {file_path}")
            analysis = self.analyze_file(file_path)
            results[str(file_path)] = analysis
            self.stats["files_analyzed"] += 1

            if analysis.unused_imports:
                logger.info(f"⚠️  {file_path}: {len(analysis.unused_imports)} imports inutilisés")

        return results

    def run_cleaning(self, results: Dict[str, FileAnalysis], dry_run: bool = True) -> bool:
        """Lance le nettoyage basé sur les résultats d'analyse"""
        logger.info("🧹 Démarrage du nettoyage..." if not dry_run else "🧹 Simulation du nettoyage (DRY RUN)...")

        total_unused = sum(len(analysis.unused_imports) for analysis in results.values())

        if total_unused == 0:
            logger.info("✅ Aucun import inutilisé trouvé !")
            return True

        logger.info(f"📊 {total_unused} imports inutilisés trouvés dans {len(results)} fichiers")

        success = True
        for file_path, analysis in results.items():
            if analysis.unused_imports:
                if not self.clean_file(analysis, dry_run):
                    success = False

        return success

    def print_summary(self):
        """Affiche un résumé des opérations"""
        logger.info("\n" + "="*60)
        logger.info("📊 RÉSUMÉ DU NETTOYAGE DES IMPORTS")
        logger.info("="*60)
        logger.info(f"📄 Fichiers analysés: {self.stats['files_analyzed']}")
        logger.info(f"🔧 Fichiers modifiés: {self.stats['files_modified']}")
        logger.info(f"🗑️  Imports supprimés: {self.stats['imports_removed']}")
        logger.info(f"❌ Erreurs: {self.stats['errors']}")

        if self.backup:
            logger.info(f"💾 Sauvegardes: {self.backup_dir}")

        logger.info("="*60)


def main():
    """Fonction principale"""
    import argparse

    parser = argparse.ArgumentParser(description="Nettoyeur automatique d'imports Python")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Racine du projet à analyser (défaut: répertoire courant)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Mode simulation (pas de modification réelle)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Ne pas créer de sauvegardes"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mode verbeux"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialisation
    cleaner = ImportCleaner(args.project_root, backup=not args.no_backup)

    # Analyse
    results = cleaner.run_analysis()

    # Nettoyage
    success = cleaner.run_cleaning(results, dry_run=args.dry_run)

    # Résumé
    cleaner.print_summary()

    if args.dry_run:
        logger.info("\n💡 Utilisez --dry-run=False pour appliquer les changements")
        logger.info("⚠️  Pensez à faire un commit avant d'appliquer les changements !")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
