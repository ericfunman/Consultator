"""
Page de gestion des Business Managers - Version simplifiée
"""

import os
import sys

import streamlit as st


def show():
    """Page principale des Business Managers - Version de test"""
    st.title("👥 Business Managers")

    # Debug des chemins
    st.write("🔍 **Debug des chemins Python:**")
    st.write(f"Current working dir: {os.getcwd()}")
    st.write(f"__file__: {__file__}")
    st.write(f"dirname(__file__): {os.path.dirname(__file__)}")
    st.write(f"Nombre de chemins Python: {len(sys.path)}")

    # Afficher les premiers chemins Python
    st.write("**Premiers chemins Python:**")
    for i, path in enumerate(sys.path[:5]):
        st.write(f"{i + 1}. {path}")

    try:
        st.write("🔍 **Test 1: Import des modèles...**")
        from app.database.models import BusinessManager
        from app.database.models import Consultant
        from app.database.models import ConsultantBusinessManager
        st.success("✅ Modèles importés avec succès")

        st.write("🔍 **Test 2: Import get_database_session...**")
        from app.database.database import get_database_session
        st.success("✅ get_database_session importé avec succès")

        st.write("🔍 **Test 3: Test de connexion...**")
        session = get_database_session()
        session.close()
        st.success("✅ Connexion DB testée avec succès")

        st.write("🔍 **Test 4: Test de requête...**")
        with get_database_session() as session:
            bm_count = session.query(BusinessManager).count()
            consultant_count = session.query(Consultant).count()

        st.success(
            f"✅ Requêtes réussies: {bm_count} BMs, {consultant_count} consultants")

        # Interface simple
        st.subheader("📋 Business Managers")

        with get_database_session() as session:
            bms = session.query(BusinessManager).filter(BusinessManager.actif).all()

            if bms:
                for bm in bms:
                    with st.expander(f"👨‍💼 {bm.nom_complet}"):
                        st.write(f"**Email:** {bm.email}")
                        st.write(f"**Téléphone:** {bm.telephone or 'Non renseigné'}")

                        # Consultants gérés
                        consultants = bm.consultants_actuels
                        if consultants:
                            st.write(f"**Consultants gérés ({len(consultants)}):**")
                            for consultant in consultants:
                                st.write(f"  • {consultant.nom_complet}")
                        else:
                            st.write("**Aucun consultant assigné**")
            else:
                st.info("Aucun Business Manager trouvé")

    except Exception as e:
        st.error("🚫 Erreur lors du chargement:")
        st.error(str(e))
        import traceback
        st.code(traceback.format_exc())
