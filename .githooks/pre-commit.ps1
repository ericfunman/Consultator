# Hook pre-commit PowerShell pour Consultator
# Execute automatiquement les tests de regression avant chaque commit

Write-Host "Verification pre-commit - Consultator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Fonction d'affichage colore
function Write-Status {
    param($Message, $Status)
    switch ($Status) {
        "success" { Write-Host "[OK] $Message" -ForegroundColor Green }
        "warning" { Write-Host "[WARN] $Message" -ForegroundColor Yellow }
        "error" { Write-Host "[ERROR] $Message" -ForegroundColor Red }
    }
}

# 1. Vérifier que Python est disponible
try {
    python --version | Out-Null
} catch {
    Write-Status "Python n'est pas disponible" "error"
    Write-Host "   Installez Python pour continuer" -ForegroundColor Red
    exit 1
}

# 2. Vérifier la structure des tests
if (!(Test-Path "tests\regression")) {
    Write-Status "Dossier tests\regression manquant" "error"
    Write-Host "   Exécutez: python scripts\clean_test_environment.py" -ForegroundColor Red
    exit 1
}

# 3. Exécuter les tests de régression critiques
Write-Host ""
Write-Host "Tests de regression..." -ForegroundColor Blue

$testResult = python -m pytest tests\regression\test_vsa_import_regression.py -q
$testExitCode = $LASTEXITCODE

if ($testExitCode -ne 0) {
    Write-Status "ECHEC des tests de regression !" "error"
    Write-Host ""
    Write-Host "COMMIT BLOQUE" -ForegroundColor Red
    Write-Host "   Les tests de regression doivent passer avant le commit" -ForegroundColor Red
    Write-Host "   Corrigez les problemes et recommencez" -ForegroundColor Red
    exit 1
}

Write-Status "Tests de régression OK" "success"

# 4. Vérifier s'il y a de nouveaux fichiers Python sans tests
Write-Host ""
Write-Host "Verification des nouveaux fichiers..." -ForegroundColor Blue

# Récupérer les fichiers Python modifiés/ajoutés (si git est disponible)
try {
    $newPyFiles = git diff --cached --name-only --diff-filter=A | Where-Object { $_ -like "*.py" -and $_ -notlike "*test_*" -and $_ -notlike "*__pycache__*" }
    
    if ($newPyFiles) {
        Write-Status "Nouveaux fichiers Python detectes:" "warning"
        foreach ($file in $newPyFiles) {
            Write-Host "   File: $file" -ForegroundColor Yellow
        }
        
        Write-Host ""
        Write-Host "Recommandation:" -ForegroundColor Cyan
        Write-Host "   Apres ce commit, executez:" -ForegroundColor Cyan
        Write-Host "   python scripts\develop_tests_systematically.py 1" -ForegroundColor Cyan
        Write-Host "   pour generer les tests associes" -ForegroundColor Cyan
    }
} catch {
    Write-Host "   Git non disponible, vérification ignorée" -ForegroundColor Yellow
}

# 5. Vérifier la couverture si des tests ont été modifiés
try {
    $modifiedTests = git diff --cached --name-only | Where-Object { $_ -like "*test_*.py" }
    
    if ($modifiedTests) {
        Write-Host ""
        Write-Host "Tests modifies detectes..." -ForegroundColor Blue
        Write-Status "Execution des tests modifies" "success"
        
        # Exécuter uniquement les tests modifiés
        $testResult = python -m pytest $modifiedTests -q
        $testExitCode = $LASTEXITCODE
        
        if ($testExitCode -ne 0) {
            Write-Status "ECHEC des tests modifies !" "error"
            Write-Host ""
            Write-Host "COMMIT BLOQUE" -ForegroundColor Red
            Write-Host "   Les tests modifies doivent passer avant le commit" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "   Verification des tests modifies ignoree" -ForegroundColor Yellow
}

# 6. Message de fin
Write-Host ""
Write-Status "Pre-commit valide !" "success"
Write-Host "Le commit peut continuer..." -ForegroundColor Green
Write-Host ""

exit 0