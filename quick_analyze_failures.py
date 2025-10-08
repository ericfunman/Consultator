"""
Script rapide pour identifier les fichiers de tests avec le plus d'échecs
"""

import subprocess
import re
from collections import defaultdict

def quick_analyze():
    """Analyse rapide des échecs par fichier"""
    print("🔍 Analyse rapide des tests en échec...")
    print("=" * 80)
    
    # Exécuter pytest avec sortie minimale
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "--tb=no", "-v", "--no-header"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore',
        timeout=180  # 3 minutes max
    )
    
    output = result.stdout + result.stderr
    
    # Extraire les FAILED avec le fichier
    failed_pattern = r"FAILED (tests/[^:]+\.py)"
    failures = re.findall(failed_pattern, output)
    
    # Compter par fichier
    file_counts = defaultdict(int)
    for file_path in failures:
        file_counts[file_path] += 1
    
    # Extraire le résumé final
    summary_pattern = r"(\d+) failed.*?(\d+) passed"
    summary = re.search(summary_pattern, output)
    
    if summary:
        failed_count = int(summary.group(1))
        passed_count = int(summary.group(2))
    else:
        failed_count = len(failures)
        passed_count = 0
    
    # Afficher les résultats
    print(f"\n📊 RÉSUMÉ GLOBAL")
    print("=" * 80)
    print(f"✅ Tests passés: {passed_count}")
    print(f"❌ Tests échoués: {failed_count}")
    print(f"📈 Taux de réussite: {passed_count/(passed_count+failed_count)*100:.1f}%")
    
    print(f"\n📁 TOP 20 FICHIERS AVEC LE PLUS D'ÉCHECS")
    print("=" * 80)
    
    sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    for i, (file_path, count) in enumerate(sorted_files, 1):
        file_name = file_path.split('/')[-1]
        estimated_coverage = count * 0.05  # Estimation
        print(f"{i:2d}. {file_name:60s} {count:3d} échecs (~+{estimated_coverage:.1f}% si corrigé)")
    
    print(f"\n💡 RECOMMANDATIONS")
    print("=" * 80)
    
    total_impact = sum(count for _, count in sorted_files[:10]) * 0.05
    print(f"🎯 Corriger les 10 fichiers prioritaires pourrait ajouter ~{total_impact:.1f}% de couverture")
    print(f"🔧 Correction estimée: {sum(count for _, count in sorted_files[:10]) * 15 / 60:.1f} heures")
    
    # Sauvegarder la liste complète
    with open("failing_tests_by_file.txt", "w", encoding='utf-8') as f:
        f.write("FICHIERS AVEC TESTS EN ÉCHEC\n")
        f.write("=" * 80 + "\n\n")
        for file_path, count in sorted_files:
            f.write(f"{file_path}: {count} échecs\n")
    
    print(f"\n✅ Liste complète sauvegardée dans: failing_tests_by_file.txt")
    
    return sorted_files

if __name__ == "__main__":
    try:
        files = quick_analyze()
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout: l'analyse a pris trop de temps")
    except Exception as e:
        print(f"❌ Erreur: {e}")
