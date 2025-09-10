import os
import sys
from datetime import datetime

import pandas as pd
import streamlit as st

# Import des modèles et services
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.database import get_database_session
from database.models import Mission
from services.consultant_service import ConsultantService


def show():
    """Affiche la page de gestion des consultants"""

    st.title("👥 Gestion des consultants")
    st.markdown("### Gérez les profils de vos consultants")

    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs(["📋 Liste des consultants", "➕ Ajouter un consultant"])

    with tab1:
        show_consultants_list()

    with tab2:
        show_add_consultant_form()


def show_consultants_list():
    """Affiche la liste des consultants"""

    st.subheader("📋 Liste des consultants")

    try:
        consultants = ConsultantService.get_all_consultants()

        if consultants:
            # Préparer les données pour le tableau
            consultants_data = []
            for consultant in consultants:
                # Compter les missions
                try:
                    with get_database_session() as session:
                        nb_missions = (
                            session.query(Mission)
                            .filter(Mission.consultant_id == consultant.id)
                            .count()
                        )
                except Exception:
                    nb_missions = 0

                consultants_data.append(
                    {
                        "ID": consultant.id,
                        "Prénom": consultant.prenom,
                        "Nom": consultant.nom,
                        "Email": consultant.email,
                        "Salaire": f"{consultant.salaire_actuel or 0:,}€",
                        "Statut": (
                            "✅ Disponible" if consultant.disponibilite else "🔴 Occupé"
                        ),
                        "Missions": nb_missions,
                    }
                )

            # Afficher le tableau
            df = pd.DataFrame(consultants_data)

            st.dataframe(df, use_container_width=True, hide_index=True)

            # Métriques générales
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("👥 Total consultants", len(consultants))

            with col2:
                disponibles = len([c for c in consultants if c.disponibilite])
                st.metric("✅ Disponibles", disponibles)

            with col3:
                salaire_moyen = (
                    sum(c.salaire_actuel or 0 for c in consultants) / len(consultants)
                    if consultants
                    else 0
                )
                st.metric("💰 Salaire moyen", f"{salaire_moyen:,.0f}€")
        else:
            st.info("📝 Aucun consultant enregistré")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")


def show_add_consultant_form():
    """Affiche le formulaire d'ajout d'un nouveau consultant"""

    st.subheader("➕ Ajouter un nouveau consultant")

    with st.form("add_consultant_form"):
        col1, col2 = st.columns(2)

        with col1:
            prenom = st.text_input("👤 Prénom *", placeholder="Ex: Jean")
            email = st.text_input("📧 Email *", placeholder="jean.dupont@example.com")
            salaire = st.number_input(
                "💰 Salaire annuel (€)", min_value=0, value=45000, step=1000
            )

        with col2:
            nom = st.text_input("👤 Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input("📞 Téléphone", placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("✅ Disponible", value=True)

        submitted = st.form_submit_button("➕ Créer le consultant", type="primary")

        if submitted:
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                try:
                    consultant_data = {
                        "prenom": prenom.strip(),
                        "nom": nom.strip(),
                        "email": email.strip().lower(),
                        "telephone": telephone.strip() if telephone else None,
                        "salaire_actuel": salaire,
                        "disponibilite": disponibilite,
                    }

                    nouveau_consultant = ConsultantService.create_consultant(  # noqa: F841
                        consultant_data
                    )
                    st.success(f"✅ {prenom} {nom} a été créé avec succès !")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Erreur lors de la création: {e}")
