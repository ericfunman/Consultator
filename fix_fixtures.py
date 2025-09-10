import re

# Read the file
with open("tests/test_consultants_comprehensive.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace all occurrences
content = re.sub(
    r"mock_sqlalchemy_models\.Consultant",
    "mock_sqlalchemy_models['consultant']",
    content,
)
content = re.sub(
    r"mock_sqlalchemy_models\.Mission", "mock_sqlalchemy_models['mission']", content
)
content = re.sub(
    r"mock_sqlalchemy_models\.Competence",
    "mock_sqlalchemy_models['competence']",
    content,
)
content = re.sub(
    r"mock_sqlalchemy_models\.ConsultantCompetence",
    "mock_sqlalchemy_models['consultant_competence']",
    content,
)
content = re.sub(
    r"mock_sqlalchemy_models\.Langue", "mock_sqlalchemy_models['langue']", content
)
content = re.sub(
    r"mock_sqlalchemy_models\.ConsultantLangue",
    "mock_sqlalchemy_models['consultant_langue']",
    content,
)
content = re.sub(
    r"mock_sqlalchemy_models\.Practice", "mock_sqlalchemy_models['practice']", content
)

# Write back
with open("tests/test_consultants_comprehensive.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Replacements completed")
