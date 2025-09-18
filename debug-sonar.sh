#!/bin/bash
echo "=== DEBUG SONARQUBE COVERAGE ==="
echo "Working directory: $(pwd)"
echo "Coverage files found:"
find . -name "coverage.xml" -type f
echo ""
echo "Coverage.xml content preview:"
head -20 coverage.xml
echo ""
echo "Coverage.xml size:"
wc -l coverage.xml
echo ""
echo "Sonar properties:"
grep -i coverage sonar-project.properties
echo "================================"