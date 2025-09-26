# Consultator Test Management Makefile

.PHONY: test test-unit test-integration test-regression coverage coverage-html improve-coverage auto-tests setup-hooks clean-tests

# Tests basiques
test:
	python -m pytest tests/ -v --tb=short

test-unit:
	python -m pytest tests/unit/ -v --tb=short

test-integration:
	python -m pytest tests/integration/ -v --tb=short

test-regression:
	python -m pytest tests/regression/ -v --tb=short

# Couverture
coverage:
	python -m pytest --cov=app --cov-report=term-missing --cov-report=html:reports/htmlcov tests/

coverage-html:
	python -m pytest --cov=app --cov-report=html:reports/htmlcov tests/
	@echo "📊 Rapport HTML généré dans reports/htmlcov/index.html"

# Amélioration de la couverture
improve-coverage:
	python scripts/improve_coverage.py

auto-tests:
	python scripts/auto_test_generator.py

# Configuration
setup-hooks:
	python scripts/test_hooks.py --setup
	@echo "✅ Hooks Git configurés"

# Nettoyage
clean-tests:
	rm -rf tests/auto_generated/*
	rm -rf reports/*
	rm -rf .coverage
	rm -rf coverage.json
	@echo "🧹 Tests automatiques et rapports nettoyés"

# Processus complet d'amélioration
full-improvement:
	python scripts/improve_coverage.py
	python scripts/auto_test_generator.py
	python -m pytest tests/auto_generated/ --tb=short
	@echo "🚀 Processus d'amélioration terminé"

# Validation avant commit
pre-commit:
	python scripts/test_hooks.py --pre-commit

# Validation après merge  
post-merge:
	python scripts/test_hooks.py --post-merge
