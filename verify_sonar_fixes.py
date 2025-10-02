#!/usr/bin/env python3
"""
Script de vérification des corrections SonarCloud
Vérifie que les 6 issues spécifiques ont été corrigées
"""

def check_sonar_fixes():
    """Vérifie les corrections des 6 issues SonarCloud spécifiques"""
    fixes = []
    
    # Issue 1: test_ai_openai_service.py ligne 283 - assertGreaterEqual
    print("🔍 Vérification Issue 1: assertGreaterEqual")
    try:
        with open("tests/unit/services/test_ai_openai_service.py", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_283 = lines[282].strip()  # ligne 283 (index 282)
        if "assertGreaterEqual" in line_283:
            print("✅ Issue 1 corrigée: assertGreaterEqual utilisé")
            fixes.append("Issue 1: ✅ Corrigée")
        else:
            print("❌ Issue 1 non corrigée")
            print(f"Ligne 283: {line_283}")
            fixes.append("Issue 1: ❌ Non corrigée")
    except Exception as e:
        print(f"❌ Erreur Issue 1: {e}")
        fixes.append("Issue 1: ❌ Erreur")
    
    # Issues 2-4: test_home.py lignes 63, 87, 108 - Expressions booléennes constantes
    print("\n🔍 Vérification Issues 2-4: Expressions booléennes constantes")
    try:
        with open("tests/ui/test_home.py", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        issues_corrected = 0
        
        # Ligne 63
        line_63 = lines[62].strip()
        if "assertTrue(True" not in line_63:
            print("✅ Issue 2 (ligne 63) corrigée")
            issues_corrected += 1
        else:
            print(f"❌ Issue 2 (ligne 63): {line_63}")
        
        # Ligne 87
        line_87 = lines[86].strip()
        if "assertTrue(True" not in line_87:
            print("✅ Issue 3 (ligne 87) corrigée")
            issues_corrected += 1
        else:
            print(f"❌ Issue 3 (ligne 87): {line_87}")
        
        # Ligne 108
        line_108 = lines[107].strip()
        if "assertTrue(True" not in line_108:
            print("✅ Issue 4 (ligne 108) corrigée")
            issues_corrected += 1
        else:
            print(f"❌ Issue 4 (ligne 108): {line_108}")
        
        fixes.append(f"Issues 2-4: {issues_corrected}/3 corrigées")
        
    except Exception as e:
        print(f"❌ Erreur Issues 2-4: {e}")
        fixes.append("Issues 2-4: ❌ Erreur")
    
    # Issue 5: test_consultants_advanced_coverage.py ligne 369 - assertTrue
    print("\n🔍 Vérification Issue 5: assertTrue")
    try:
        with open("tests/unit/pages_modules/test_consultants_advanced_coverage.py", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_369 = lines[368].strip()  # ligne 369 (index 368)
        if "assertTrue(result[5])" in line_369:
            print("✅ Issue 5 corrigée: assertTrue utilisé")
            fixes.append("Issue 5: ✅ Corrigée")
        else:
            print("❌ Issue 5 non corrigée")
            print(f"Ligne 369: {line_369}")
            fixes.append("Issue 5: ❌ Non corrigée")
    except Exception as e:
        print(f"❌ Erreur Issue 5: {e}")
        fixes.append("Issue 5: ❌ Erreur")
    
    # Issue 6: test_consultants_massive_coverage.py ligne 203 - assertIsNone
    print("\n🔍 Vérification Issue 6: assertIsNone")
    try:
        with open("tests/unit/pages_modules/test_consultants_massive_coverage.py", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_203 = lines[202].strip()  # ligne 203 (index 202)
        if "assertIsNone" in line_203:
            print("✅ Issue 6 corrigée: assertIsNone utilisé")
            fixes.append("Issue 6: ✅ Corrigée")
        else:
            print("❌ Issue 6 non corrigée")
            print(f"Ligne 203: {line_203}")
            fixes.append("Issue 6: ❌ Non corrigée")
    except Exception as e:
        print(f"❌ Erreur Issue 6: {e}")
        fixes.append("Issue 6: ❌ Erreur")
    
    # Résumé final
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES CORRECTIONS SONARCLOUD")
    print("="*60)
    
    corrected_issues = 0
    
    for fix in fixes:
        print(f"  {fix}")
        if "Issue 1: ✅ Corrigée" in fix:
            corrected_issues += 1
        elif "Issues 2-4: 3/3 corrigées" in fix:
            corrected_issues += 3  # 3 issues corrigées
        elif "Issue 5: ✅ Corrigée" in fix:
            corrected_issues += 1
        elif "Issue 6: ✅ Corrigée" in fix:
            corrected_issues += 1
    
    total_issues = 6
    
    print(f"\n🎯 Total: {corrected_issues}/{total_issues} issues corrigées")
    
    if corrected_issues == total_issues:
        print("🎉 TOUTES LES ISSUES SONARCLOUD ONT ÉTÉ CORRIGÉES!")
        return True
    else:
        print("⚠️ Certaines issues nécessitent encore des corrections")
        return False

if __name__ == "__main__":
    print("🔧 Vérification des corrections SonarCloud...")
    print("="*60)
    
    success = check_sonar_fixes()
    
    if success:
        print("\n✅ Script terminé avec succès - toutes les issues corrigées!")
    else:
        print("\n⚠️ Script terminé - certaines issues restent à corriger")