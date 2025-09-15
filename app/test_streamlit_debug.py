"""
Test Streamlit minimal pour diagnostiquer le problème BM
"""

import os
import sys

import streamlit as st

# Ajouter le répertoire app au path
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

st.title("🔍 Test de diagnostic Business Managers")

st.write("**Répertoire courant:**", os.getcwd())
st.write("**Fichier courant:**", __file__)
st.write("**Répertoire du script:**", os.path.dirname(__file__))

# Test 1: Paths Python
st.subheader("1. Chemins Python")
for i, path in enumerate(sys.path):
    st.write(f"{i + 1}. {path}")

# Test 2: Existence des fichiers
st.subheader("2. Existence des fichiers")
files_to_check = [
    "database/models.py",
    "database/database.py",
    "pages_modules/business_managers_simple.py",
]

for file_path in files_to_check:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    exists = os.path.exists(full_path)
    st.write(f"📁 {file_path}: {'✅ Existe' if exists else '❌ Absent'}")

# Test 3: Imports
st.subheader("3. Test des imports")

try:
    st.write("Test import database.models...")
    from database.models import BusinessManager

    st.success("✅ database.models importé")
except Exception as e:
    st.error(f"❌ Erreur database.models: {e}")

try:
    st.write("Test import database.database...")
    from database.database import get_database_session

    st.success("✅ database.database importé")
except Exception as e:
    st.error(f"❌ Erreur database.database: {e}")

try:
    st.write("Test import pages_modules...")
    from pages_modules import business_managers_simple

    st.success("✅ pages_modules.business_managers_simple importé")
except Exception as e:
    st.error(f"❌ Erreur pages_modules: {e}")

# Test 4: Connexion DB
st.subheader("4. Test connexion base de données")
try:
    from database.database import get_database_session
    from database.models import BusinessManager

    session = get_database_session()
    count = session.query(BusinessManager).count()
    session.close()

    st.success(f"✅ Connexion DB OK: {count} Business Managers trouvés")
except Exception as e:
    st.error(f"❌ Erreur DB: {e}")
    import traceback

    st.code(traceback.format_exc())
