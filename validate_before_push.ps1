# Script de validation avant push - Consultator (PowerShell)
# Lance toutes les vérifications du CI/CD en local

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  VALIDATION PRE-PUSH CONSULTATOR" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# Étape 1: Black
Write-Host "[1/5] Verification Black (formatage code)" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$blackResult = python -m black --check --diff --line-length 120 app/ tests/ 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Black: Code correctement formate" -ForegroundColor Green
} else {
    Write-Host "[ERREUR] Black: Code mal formate" -ForegroundColor Red
    Write-Host "Pour corriger: python -m black app/ tests/ --line-length 120" -ForegroundColor Yellow
    $ErrorCount++
}
Write-Host ""

# Étape 2: isort
Write-Host "[2/5] Verification isort (ordre imports)" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$isortResult = python -m isort --check-only --diff app/ tests/ 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] isort: Imports correctement ordonnes" -ForegroundColor Green
} else {
    Write-Host "[WARNING] isort: Imports mal ordonnes (non-bloquant)" -ForegroundColor Yellow
    Write-Host "Pour corriger: python -m isort app/ tests/" -ForegroundColor Yellow
}
Write-Host ""

# Étape 3: Flake8
Write-Host "[3/5] Verification Flake8 (linting)" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$flake8Result = python -m flake8 app/ --max-line-length=150 --extend-ignore=E203,W503,F401,F841,W291,W293,E501,C901,E722,F541 --max-complexity=20 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Flake8: Pas d'erreurs de linting" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Flake8: Avertissements detectes (non-bloquants)" -ForegroundColor Yellow
}
Write-Host ""

# Étape 4: Tests de régression
Write-Host "[4/5] Tests de regression" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
if (Test-Path "tests/regression") {
    $testResult = python -m pytest tests/regression/ -v --tb=short 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Tests de regression: OK" -ForegroundColor Green
    } else {
        Write-Host "[ERREUR] Tests de regression: ECHEC" -ForegroundColor Red
        $ErrorCount++
    }
} else {
    Write-Host "[WARNING] Pas de tests de regression trouves" -ForegroundColor Yellow
}
Write-Host ""

# Étape 5: Base de données
Write-Host "[5/5] Verification base de donnees" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$dbResult = python -c "from app.database.database import init_database; init_database(); print('[OK] DB OK')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Base de donnees: Initialisable" -ForegroundColor Green
} else {
    Write-Host "[ERREUR] Base de donnees: Erreur d'initialisation" -ForegroundColor Red
    $ErrorCount++
}
Write-Host ""

# Résultat final
Write-Host "==================================" -ForegroundColor Cyan
if ($ErrorCount -eq 0) {
    Write-Host "[SUCCESS] TOUTES LES VALIDATIONS PASSEES !" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Vous pouvez pousser en toute securite:" -ForegroundColor Green
    Write-Host "   git push origin master" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host "[FAIL] $ErrorCount ERREUR(S) DETECTEE(S)" -ForegroundColor Red
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Corrigez les erreurs avant de pousser" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
