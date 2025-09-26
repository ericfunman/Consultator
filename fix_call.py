#!/usr/bin/env python3
import re

# Lire le fichier
with open("app/pages_modules/consultant_documents.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer l'appel spécifique dans perform_cv_analysis
pattern = r'(analysis_result = grok_service\.analyze_cv\(\s*extracted_text),\s*f"\{consultant\.prenom\} \{consultant\.nom\}"\s*\)'
replacement = r"\1)"

new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

# Écrire le fichier
with open("app/pages_modules/consultant_documents.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ Correction appliquée")
