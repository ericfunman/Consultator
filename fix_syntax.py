import re

# Read the file
with open("tests/test_consultants_comprehensive.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the syntax error
content = re.sub(
    r"mock_sqlalchemy_models\[\'consultant\'\]Competence",
    "mock_sqlalchemy_models['consultant_competence']",
    content,
)
content = re.sub(
    r"mock_sqlalchemy_models\[\'consultant\'\]Langue",
    "mock_sqlalchemy_models['consultant_langue']",
    content,
)

# Write back
with open("tests/test_consultants_comprehensive.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Syntax errors fixed")
