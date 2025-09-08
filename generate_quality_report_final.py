#!/usr/bin/env python3
"""
Rapport de Qualité du Code - Consultator
Analyse complète de la qualité du code après améliorations
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict
from typing import List


class CodeQualityAnalyzer:
    """Analyseur de qualité du code pour le projet Consultator"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.app_dir = self.project_root / "app"
        self.python_files = []
        self._find_python_files()

    def _find_python_files(self):
        """Trouve tous les fichiers Python dans le projet"""
        for file_path in self.app_dir.rglob("*.py"):
            if not any(skip in str(file_path) for skip in ["__pycache__", ".git"]):
                self.python_files.append(file_path)

    def analyze_code_complexity(self) -> Dict[str, int]:
        """Analyse la complexité cyclomatique des fichiers"""
        complexity_results = {}

        for file_path in self.python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Compter les fonctions et méthodes
                functions = content.count("def ")
                classes = content.count("class ")
                ifs = content.count("if ")
                fors = content.count("for ")
                whiles = content.count("while ")

                # Complexité estimée (très simplifiée)
                complexity = functions + classes + (ifs * 2) + (fors * 2) + (whiles * 2)

                if complexity > 0:
                    complexity_results[
                        str(file_path.relative_to(self.project_root))
                    ] = complexity

            except Exception as e:
                print(f"Erreur lors de l'analyse de {file_path}: {e}")

        return dict(
            sorted(complexity_results.items(), key=lambda x: x[1], reverse=True)
        )

    def analyze_code_metrics(self) -> Dict[str, Dict]:
        """Analyse les métriques de base du code"""
        metrics = {}

        for file_path in self.python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Métriques de base
                total_lines = len(lines)
                code_lines = sum(
                    1
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                )
                comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
                empty_lines = sum(1 for line in lines if not line.strip())

                # Analyse du contenu
                imports = sum(
                    1 for line in lines if line.strip().startswith(("import ", "from "))
                )
                functions = sum(1 for line in lines if line.strip().startswith("def "))
                classes = sum(1 for line in lines if line.strip().startswith("class "))

                # Calcul du ratio commentaire/code
                comment_ratio = (
                    (comment_lines / code_lines * 100) if code_lines > 0 else 0
                )

                metrics[str(file_path.relative_to(self.project_root))] = {
                    "total_lines": total_lines,
                    "code_lines": code_lines,
                    "comment_lines": comment_lines,
                    "empty_lines": empty_lines,
                    "imports": imports,
                    "functions": functions,
                    "classes": classes,
                    "comment_ratio": round(comment_ratio, 1),
                }

            except Exception as e:
                print(f"Erreur lors de l'analyse des métriques de {file_path}: {e}")

        return metrics

    def check_best_practices(self) -> Dict[str, List[str]]:
        """Vérifie les bonnes pratiques de codage"""
        issues = {}

        for file_path in self.python_files:
            file_issues = []
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                # Vérifier les exceptions génériques
                if "except:" in content:
                    file_issues.append("Utilisation d'exceptions génériques 'except:'")

                # Vérifier les f-strings inutiles
                for i, line in enumerate(lines, 1):
                    if 'f"' in line and "{" not in line:
                        file_issues.append(
                            "Ligne {}: f-string inutile sans variables".format(i)
                        )

                # Vérifier les constantes dupliquées
                duplicate_literals = [
                    "Non affecté",
                    "En cours",
                    "N/A",
                    "✅ Disponible",
                    "🔴 Occupé",
                ]
                for literal in duplicate_literals:
                    if content.count(f"'{literal}'") > 2:
                        file_issues.append(
                            "Littéral '{}' dupliqué plusieurs fois".format(literal)
                        )

                # Vérifier la longueur des lignes
                long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 100]
                if long_lines:
                    file_issues.append(
                        f"{len(long_lines)} lignes trop longues (>100 caractères)"
                    )

                # Vérifier les fonctions trop longues
                current_function = []
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith("def "):
                        if len(current_function) > 50:
                            file_issues.append(
                                f"Fonction trop longue détectée autour de la ligne {i}"
                            )
                        current_function = [i]
                    elif (
                        line.strip()
                        and not line.startswith(" ")
                        and not line.startswith("\t")
                    ):
                        if current_function and len(current_function) > 50:
                            file_issues.append(
                                f"Fonction trop longue détectée autour de la ligne {current_function[0]}"
                            )
                        current_function = []

                if file_issues:
                    issues[str(file_path.relative_to(self.project_root))] = file_issues

            except Exception as e:
                print(
                    f"Erreur lors de l'analyse des bonnes pratiques de {file_path}: {e}"
                )

        return issues

    def generate_report(self) -> str:
        """Génère un rapport complet de qualité du code"""
        print("🔍 Analyse de la qualité du code en cours...")

        # Analyser la complexité
        complexity = self.analyze_code_complexity()

        # Analyser les métriques
        metrics = self.analyze_code_metrics()

        # Vérifier les bonnes pratiques
        issues = self.check_best_practices()

        # Générer le rapport
        report = []
        report.append("📊 RAPPORT DE QUALITÉ DU CODE - CONSULTATOR")
        report.append("=" * 50)
        report.append("")

        # Statistiques générales
        total_files = len(self.python_files)
        total_lines = sum(m["total_lines"] for m in metrics.values())
        total_code_lines = sum(m["code_lines"] for m in metrics.values())
        total_functions = sum(m["functions"] for m in metrics.values())
        total_classes = sum(m["classes"] for m in metrics.values())

        report.append("📈 STATISTIQUES GÉNÉRALES")
        report.append("-" * 30)
        report.append(f"• Fichiers Python analysés: {total_files}")
        report.append(f"• Lignes totales: {total_lines:,}")
        report.append(f"• Lignes de code: {total_code_lines:,}")
        report.append(f"• Fonctions: {total_functions}")
        report.append(f"• Classes: {total_classes}")
        report.append("")

        # Complexité
        report.append("🎯 ANALYSE DE COMPLEXITÉ")
        report.append("-" * 30)
        if complexity:
            report.append("Top 5 fichiers par complexité:")
            for i, (file, comp) in enumerate(list(complexity.items())[:5], 1):
                report.append(f"{i}. {file}: {comp} points")
        else:
            report.append("✅ Aucune complexité détectée")
        report.append("")

        # Métriques détaillées
        report.append("📋 MÉTRIQUES DÉTAILLÉES")
        report.append("-" * 30)
        for file, metric in sorted(metrics.items())[:10]:  # Top 10 fichiers
            report.append(f"📄 {file}:")
            report.append(
                f"   • Lignes: {metric['total_lines']} ({metric['code_lines']} code)"
            )
            report.append(
                f"   • Fonctions: {metric['functions']}, Classes: {metric['classes']}"
            )
            report.append(f"   • Ratio commentaires: {metric['comment_ratio']}%")
            report.append("")

        # Problèmes détectés
        report.append("⚠️ PROBLÈMES DÉTECTÉS")
        report.append("-" * 30)
        if issues:
            for file, file_issues in issues.items():
                report.append(f"📄 {file}:")
                for issue in file_issues:
                    report.append(f"   • {issue}")
                report.append("")
        else:
            report.append("✅ Aucun problème majeur détecté !")
        report.append("")

        # Recommandations
        report.append("💡 RECOMMANDATIONS")
        report.append("-" * 30)
        recommendations = []

        if any(m["comment_ratio"] < 10 for m in metrics.values()):
            recommendations.append(
                "• Augmenter le ratio de commentaires (< 10% dans certains fichiers)"
            )
        if any(m["functions"] > 20 for m in metrics.values()):
            recommendations.append(
                "• Découper les fichiers avec trop de fonctions (> 20)"
            )
        if issues:
            recommendations.append(
                "• Corriger les problèmes de bonnes pratiques détectés"
            )
        if not recommendations:
            recommendations.append("• Code de qualité ! Continuer les bonnes pratiques")

        for rec in recommendations:
            report.append(rec)
        report.append("")

        # Score global
        score = self._calculate_quality_score(metrics, issues)
        report.append("🏆 SCORE GLOBAL DE QUALITÉ")
        report.append("-" * 30)
        report.append(f"Score: {score}/100")

        if score >= 90:
            report.append("🎉 Excellent ! Code de très haute qualité")
        elif score >= 80:
            report.append("✅ Bon ! Quelques améliorations mineures possibles")
        elif score >= 70:
            report.append("⚠️ Correct ! Améliorations recommandées")
        else:
            report.append("🔴 À améliorer ! Refactorisation nécessaire")

        return "\n".join(report)

    def _calculate_quality_score(self, metrics: Dict, issues: Dict) -> int:
        """Calcule un score global de qualité"""
        score = 100

        # Pénalités pour les métriques
        for metric in metrics.values():
            if metric["comment_ratio"] < 5:
                score -= 10
            elif metric["comment_ratio"] < 15:
                score -= 5

            if metric["functions"] > 30:
                score -= 10
            elif metric["functions"] > 20:
                score -= 5

        # Pénalités pour les problèmes
        total_issues = sum(len(file_issues) for file_issues in issues.values())
        score -= min(total_issues * 2, 30)  # Max 30 points de pénalité

        return max(0, min(100, score))


def main():
    """Fonction principale"""
    project_root = Path(__file__).parent

    analyzer = CodeQualityAnalyzer(project_root)
    report = analyzer.generate_report()

    print(report)

    # Sauvegarder le rapport
    report_file = project_root / "quality_report_final.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 Rapport sauvegardé dans: {report_file}")


if __name__ == "__main__":
    main()
