# Script de validation avant push - Consultator (PowerShell)
# Lance toutes les vérifications du CI/CD en local

Write-Host "🔍 ==================================" -ForegroundColor Cyan
Write-Host "   VALIDATION PRE-PUSH CONSULTATOR" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# Étape 1: Black
Write-Host "📋 Étape 1/5: Vérification Black (formatage code)" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$blackResult = python -m black --check --diff --line-length 120 app/ tests/ 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Black: Code correctement formaté" -ForegroundColor Green
} else {
    Write-Host "❌ Black: Code mal formaté" -ForegroundColor Red
    Write-Host "Pour corriger: python -m black app/ tests/ --line-length 120" -ForegroundColor Yellow
    $ErrorCount++
}
Write-Host ""

# Étape 2: isort
Write-Host "📋 Étape 2/5: Vérification isort (ordre imports)" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$isortResult = python -m isort --check-only --diff app/ tests/ 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ isort: Imports correctement ordonnés" -ForegroundColor Green
} else {
    Write-Host "⚠️  isort: Imports mal ordonnés (non-bloquant en CI/CD)" -ForegroundColor Yellow
    Write-Host "Pour corriger: python -m isort app/ tests/" -ForegroundColor Yellow
}
Write-Host ""

# Étape 3: Flake8
Write-Host "📋 Étape 3/5: Vérification Flake8 (linting)" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$flake8Result = python -m flake8 app/ --max-line-length=150 --extend-ignore=E203,W503,F401,F841,W291,W293,E501,C901,E722,F541 --max-complexity=20 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Flake8: Pas d'erreurs de linting" -ForegroundColor Green
} else {
    Write-Host "⚠️  Flake8: Avertissements détectés (non-bloquants)" -ForegroundColor Yellow
}
Write-Host ""

# Étape 4: Tests de régression
Write-Host "📋 Étape 4/5: Tests de régression" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
if (Test-Path "tests/regression") {
    $testResult = python -m pytest tests/regression/ -v --tb=short 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Tests de régression: OK" -ForegroundColor Green
    } else {
        Write-Host "❌ Tests de régression: ÉCHEC" -ForegroundColor Red
        $ErrorCount++
    }
} else {
    Write-Host "⚠️  Pas de tests de régression trouvés" -ForegroundColor Yellow
}
Write-Host ""

# Étape 5: Base de données
Write-Host "📋 Étape 5/5: Vérification base de données" -ForegroundColor Yellow
Write-Host "---------------------------------------------------"
$dbResult = python -c "from app.database.database import init_database; init_database(); print('✅ DB OK')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Base de données: Initialisable" -ForegroundColor Green
} else {
    Write-Host "❌ Base de données: Erreur d'initialisation" -ForegroundColor Red
    $ErrorCount++
}
Write-Host ""

# Résultat final
Write-Host "==================================" -ForegroundColor Cyan
if ($ErrorCount -eq 0) {
    Write-Host "✅ TOUTES LES VALIDATIONS PASSÉES !" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Vous pouvez pousser en toute sécurité:" -ForegroundColor Green
    Write-Host "   git push origin master" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host "❌ $ErrorCount ERREUR(S) DÉTECTÉE(S)" -ForegroundColor Red
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  Corrigez les erreurs avant de pousser" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
