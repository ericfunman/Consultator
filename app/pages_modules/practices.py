"""
Page de gestion des practices
Affiche les consultants par practice et permet la gestion des practices
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from services.practice_service import PracticeService
from services.consultant_service import ConsultantService


def show():
    """Affiche la page de gestion des practices"""
    
    st.title("🏢 Gestion des Practices")
    st.markdown("### Vue d'ensemble des practices et de leurs consultants")
    
    # Initialiser les practices par défaut si nécessaire
    PracticeService.init_default_practices()
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "👥 Consultants par Practice", "⚙️ Gestion des Practices"])
    
    with tab1:
        show_practice_overview()
    
    with tab2:
        show_consultants_by_practice()
    
    with tab3:
        show_practice_management()


def show_practice_overview():
    """Affiche une vue d'ensemble des practices"""
    
    # Récupérer les statistiques
    stats = PracticeService.get_practice_statistics()
    
    # Métriques principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏢 Total Practices",
            value=stats["total_practices"]
        )
    
    with col2:
        st.metric(
            label="👥 Total Consultants",
            value=stats["total_consultants"]
        )
    
    with col3:
        consultants_actifs = sum([p["consultants_actifs"] for p in stats["practices_detail"]])
        st.metric(
            label="✅ Consultants Actifs",
            value=consultants_actifs
        )
    
    st.markdown("---")
    
    # Tableau détaillé par practice
    if stats["practices_detail"]:
        st.subheader("📋 Détail par Practice")
        
        df_practices = pd.DataFrame(stats["practices_detail"])
        df_practices = df_practices.rename(columns={
            "nom": "Practice",
            "total_consultants": "Total Consultants",
            "consultants_actifs": "Consultants Actifs",
            "responsable": "Responsable"
        })
        
        # Afficher le tableau avec formatting
        st.dataframe(
            df_practices,
            use_container_width=True,
            hide_index=True
        )
        
        # Graphique en barres
        if len(df_practices) > 0:
            st.subheader("📈 Répartition des Consultants")
            chart_data = df_practices.set_index("Practice")[["Total Consultants", "Consultants Actifs"]]
            st.bar_chart(chart_data)
    
    else:
        st.info("ℹ️ Aucune practice trouvée. Créez votre première practice dans l'onglet 'Gestion des Practices'.")


def show_consultants_by_practice():
    """Affiche les consultants regroupés par practice"""
    
    # Récupérer les consultants par practice
    consultants_by_practice = PracticeService.get_consultants_by_practice()
    
    if not consultants_by_practice:
        st.info("ℹ️ Aucun consultant trouvé.")
        return
    
    # Filtre par practice
    practices_names = list(consultants_by_practice.keys())
    selected_practice = st.selectbox(
        "🔍 Filtrer par Practice",
        options=["Toutes"] + practices_names,
        index=0
    )
    
    st.markdown("---")
    
    # Afficher les consultants
    if selected_practice == "Toutes":
        # Afficher toutes les practices
        for practice_name, consultants in consultants_by_practice.items():
            show_practice_consultants(practice_name, consultants)
    else:
        # Afficher une practice spécifique
        consultants = consultants_by_practice.get(selected_practice, [])
        show_practice_consultants(selected_practice, consultants)


def show_practice_consultants(practice_name: str, consultants: list):
    """Affiche les consultants d'une practice"""
    
    if not consultants:
        st.markdown(f"### 🏢 {practice_name}")
        st.info("Aucun consultant dans cette practice")
        return
    
    st.markdown(f"### 🏢 {practice_name} ({len(consultants)} consultant{'s' if len(consultants) > 1 else ''})")
    
    # Créer un DataFrame pour affichage
    consultants_data = []
    for consultant in consultants:
        # Calculer le nombre de missions de manière sûre
        try:
            missions = consultant.missions
            nb_missions = len(missions) if missions else 0
        except:
            nb_missions = 0
        
        # Calculer le nombre de compétences de manière sûre
        try:
            competences = consultant.competences
            nb_competences = len(competences) if competences else 0
        except:
            nb_competences = 0
        
        consultants_data.append({
            "Nom": consultant.nom_complet,
            "Email": consultant.email,
            "Téléphone": consultant.telephone or "Non renseigné",
            "Salaire": f"{consultant.salaire_actuel:,.0f} €" if consultant.salaire_actuel else "Non renseigné",
            "Disponible": "✅" if consultant.disponibilite else "❌",
            "Missions": nb_missions,
            "Compétences": nb_competences
        })
    
    if consultants_data:
        df = pd.DataFrame(consultants_data)
        
        # Afficher le tableau
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Actions rapides
        with st.expander(f"⚡ Actions rapides - {practice_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"📊 Statistiques détaillées", key=f"stats_{practice_name}"):
                    show_practice_detailed_stats(practice_name, consultants)
            
            with col2:
                if st.button(f"📧 Exporter emails", key=f"export_{practice_name}"):
                    emails = [c.email for c in consultants if c.email]
                    st.code("; ".join(emails))
                    st.success(f"✅ {len(emails)} emails copiés")
    
    st.markdown("---")


def show_practice_detailed_stats(practice_name: str, consultants: list):
    """Affiche des statistiques détaillées pour une practice"""
    
    st.subheader(f"📊 Statistiques détaillées - {practice_name}")
    
    if not consultants:
        st.info("Aucune donnée disponible")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        disponibles = len([c for c in consultants if c.disponibilite])
        st.metric("Disponibles", disponibles)
    
    with col2:
        try:
            total_missions = sum([len(c.missions) if hasattr(c, 'missions') and c.missions else 0 for c in consultants])
        except:
            total_missions = 0
        st.metric("Total Missions", total_missions)
    
    with col3:
        salaires_valides = [c.salaire_actuel for c in consultants if c.salaire_actuel]
        if salaires_valides:
            avg_salary = sum(salaires_valides) / len(salaires_valides)
            st.metric("Salaire Moyen", f"{avg_salary:,.0f} €")
        else:
            st.metric("Salaire Moyen", "N/A")
    
    with col4:
        try:
            total_competences = sum([len(c.competences) if hasattr(c, 'competences') and c.competences else 0 for c in consultants])
        except:
            total_competences = 0
        st.metric("Total Compétences", total_competences)


def show_practice_management():
    """Interface de gestion des practices"""
    
    st.subheader("⚙️ Gestion des Practices")
    
    # Récupérer les practices existantes
    practices = PracticeService.get_all_practices()
    
    # Onglets pour les différentes actions
    mgmt_tab1, mgmt_tab2, mgmt_tab3 = st.tabs(["➕ Créer Practice", "✏️ Modifier Practice", "👤 Assigner Consultants"])
    
    with mgmt_tab1:
        show_create_practice_form()
    
    with mgmt_tab2:
        show_edit_practice_form(practices)
    
    with mgmt_tab3:
        show_assign_consultant_form(practices)


def show_create_practice_form():
    """Formulaire de création de practice"""
    
    st.markdown("#### ➕ Créer une nouvelle Practice")
    
    with st.form("create_practice_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input(
                "Nom de la Practice *",
                placeholder="Ex: DevOps, Cloud, etc."
            )
        
        with col2:
            responsable = st.text_input(
                "Responsable",
                placeholder="Nom du responsable (optionnel)"
            )
        
        description = st.text_area(
            "Description",
            placeholder="Description de la practice (optionnel)"
        )
        
        submitted = st.form_submit_button("🚀 Créer la Practice", type="primary")
        
        if submitted:
            if not nom.strip():
                st.error("❌ Le nom de la practice est obligatoire")
            else:
                practice = PracticeService.create_practice(
                    nom=nom.strip(),
                    description=description.strip(),
                    responsable=responsable.strip()
                )
                
                if practice:
                    st.rerun()


def show_edit_practice_form(practices: list):
    """Formulaire de modification de practice"""
    
    st.markdown("#### ✏️ Modifier une Practice")
    
    if not practices:
        st.info("Aucune practice à modifier")
        return
    
    # Sélection de la practice à modifier
    practice_options = {f"{p.nom}": p for p in practices}
    selected_name = st.selectbox(
        "Sélectionner la practice à modifier",
        options=list(practice_options.keys())
    )
    
    if selected_name:
        practice = practice_options[selected_name]
        
        with st.form(f"edit_practice_form_{practice.id}"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_nom = st.text_input(
                    "Nom de la Practice *",
                    value=practice.nom
                )
            
            with col2:
                new_responsable = st.text_input(
                    "Responsable",
                    value=practice.responsable or ""
                )
            
            new_description = st.text_area(
                "Description",
                value=practice.description or ""
            )
            
            new_actif = st.checkbox(
                "Practice active",
                value=practice.actif
            )
            
            submitted = st.form_submit_button("💾 Sauvegarder les modifications", type="primary")
            
            if submitted:
                if not new_nom.strip():
                    st.error("❌ Le nom de la practice est obligatoire")
                else:
                    success = PracticeService.update_practice(
                        practice.id,
                        nom=new_nom.strip(),
                        description=new_description.strip(),
                        responsable=new_responsable.strip(),
                        actif=new_actif
                    )
                    
                    if success:
                        st.rerun()


def show_assign_consultant_form(practices: list):
    """Formulaire d'assignation de consultants aux practices"""
    
    st.markdown("#### 👤 Assigner des Consultants aux Practices")
    
    # Récupérer tous les consultants
    consultants = ConsultantService.get_all_consultants()
    
    if not consultants:
        st.info("Aucun consultant trouvé")
        return
    
    # Sélection du consultant
    consultant_options = {f"{c.nom_complet} ({c.email})": c for c in consultants}
    selected_consultant_name = st.selectbox(
        "Sélectionner le consultant",
        options=list(consultant_options.keys())
    )
    
    if selected_consultant_name:
        consultant = consultant_options[selected_consultant_name]
        
        # Afficher la practice actuelle
        try:
            current_practice = consultant.practice.nom if consultant.practice else "Aucune"
        except:
            current_practice = "Aucune"
        st.info(f"Practice actuelle : **{current_practice}**")
        
        # Sélection de la nouvelle practice
        practice_options = {"Aucune practice": None}
        practice_options.update({p.nom: p.id for p in practices})
        
        selected_practice = st.selectbox(
            "Nouvelle practice",
            options=list(practice_options.keys()),
            index=0
        )
        
        if st.button("🔄 Assigner à la practice", type="primary"):
            practice_id = practice_options[selected_practice]
            
            success = PracticeService.assign_consultant_to_practice(
                consultant.id,
                practice_id
            )
            
            if success:
                st.rerun()
