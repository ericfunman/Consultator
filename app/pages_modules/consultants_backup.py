"""
Page de gestion des consultants
CRUD complet pour les consultants avec formulaires, tableaux et gestion de documents
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Import des modÃ¨les et services
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.consultant_service import ConsultantService
from services.document_analyzer import DocumentAnalyzer
from services.technology_service import TechnologyService
from components.technology_widget import technology_multiselect
from database.database import get_database_session
from database.models import Mission, ConsultantCompetence, Competence

def show():
    """Affiche la page de gestion des consultants"""
    
    st.title("ðŸ‘¥ Gestion des consultants")
    st.markdown("### GÃ©rez les profils de vos consultants")
    
    # VÃ©rifier si on doit afficher le profil d'un consultant spÃ©cifique
    if 'view_consultant_profile' in st.session_state:
        show_consultant_profile()
        return
    
    # Onglets pour organiser les fonctionnalitÃ©s
    tab1, tab2 = st.tabs(["ðŸ“‹ Liste des consultants", "âž• Ajouter un consultant"])
    
    with tab1:
        show_consultants_list()
    
    with tab2:
        show_add_consultant_form()
    
    # Section CV Import
    st.markdown("---")
    st.subheader("ðŸ“„ Import de CV et Documents")
    
    # Section de test de l'analyseur (pour debug)
    with st.expander("ðŸ§ª Tester l'analyseur de CV", expanded=False):
        st.info("ðŸ’¡ Testez l'algorithme d'analyse avec un texte d'exemple")
        
        if st.button("ðŸš€ Lancer le test d'analyse", key="test_analyzer"):
            with st.spinner("ðŸ”„ Test de l'analyseur en cours..."):
                
                # Test avec texte d'exemple
                test_result = DocumentAnalyzer.test_analysis()
                
                st.success("âœ… Test terminÃ© !")
                
                # Afficher les rÃ©sultats
                preview_text = DocumentAnalyzer.get_analysis_preview(test_result)
                st.markdown(preview_text)
        
        # Option pour tester avec un texte personnalisÃ©
        custom_text = st.text_area(
            "ðŸ“ Ou testez avec votre propre texte CV :",
            height=150,
            placeholder="Collez ici un extrait de CV pour tester l'analyse..."
        )
        
        if custom_text and st.button("ðŸ” Analyser ce texte", key="test_custom"):
            with st.spinner("ðŸ”„ Analyse du texte personnalisÃ©..."):
                
                custom_result = DocumentAnalyzer.analyze_cv_content(custom_text, "Test PersonnalisÃ©")
                
                st.success("âœ… Analyse personnalisÃ©e terminÃ©e !")
                
                preview_text = DocumentAnalyzer.get_analysis_preview(custom_result)
                st.markdown(preview_text)
    
    st.markdown("---")
    
    show_cv_import()


def show_cv_import():
    """Affiche la section d'import de CV"""
    # Import CV simplifiÃ© directement ici
    consultants = ConsultantService.get_all_consultants()
    
    if consultants:
        # SÃ©lection du consultant
        consultant_options = {}
        for consultant in consultants:
            key = f"{consultant.prenom} {consultant.nom} ({consultant.email})"
            consultant_options[key] = consultant
        
        selected_consultant_key = st.selectbox(
            "ðŸ‘¤ SÃ©lectionner le consultant",
            options=list(consultant_options.keys()),
            help="Choisissez le consultant auquel associer le CV"
        )
        
        selected_consultant = consultant_options[selected_consultant_key]
        st.info(f"ðŸ“‹ CV sera associÃ© Ã : **{selected_consultant.prenom} {selected_consultant.nom}**")
        
        # Afficher le profil existant du consultant
        with st.expander(f"ðŸ‘¤ Profil actuel de {selected_consultant.prenom} {selected_consultant.nom}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ðŸ“Š Informations gÃ©nÃ©rales")
                st.write(f"**Email:** {selected_consultant.email}")
                if selected_consultant.telephone:
                    st.write(f"**TÃ©lÃ©phone:** {selected_consultant.telephone}")
                if selected_consultant.salaire_actuel:
                    st.write(f"**Salaire actuel:** {selected_consultant.salaire_actuel:,.0f} â‚¬")
                st.write(f"**Disponible:** {'âœ… Oui' if selected_consultant.disponibilite else 'âŒ Non'}")
                
                # Afficher les missions existantes
                try:
                    
                    with get_database_session() as session:
                        missions = session.query(Mission).filter(Mission.consultant_id == selected_consultant.id).all()
                        
                        st.markdown("#### ðŸš€ Missions existantes")
                        if missions:
                            for mission in missions[-5:]:  # DerniÃ¨res 5 missions
                                status_icon = "ðŸŸ¢" if mission.statut == "en_cours" else "ðŸ”µ"
                                st.write(f"{status_icon} **{mission.client}** ({mission.date_debut} â†’ {mission.date_fin or 'En cours'})")
                                if mission.technologies_utilisees:
                                    st.caption(f"Technologies: {mission.technologies_utilisees}")
                            
                            if len(missions) > 5:
                                st.caption(f"... et {len(missions) - 5} autres missions")
                        else:
                            st.write("Aucune mission enregistrÃ©e")
                except Exception as e:
                    st.error(f"Erreur lors du chargement des missions: {e}")
            
            with col2:
                try:
                    # Afficher les compÃ©tences existantes
                    with get_database_session() as session:
                        competences = session.query(ConsultantCompetence, Competence)\
                            .join(Competence)\
                            .filter(ConsultantCompetence.consultant_id == selected_consultant.id)\
                            .all()
                        
                        st.markdown("#### ðŸ’» CompÃ©tences techniques")
                        tech_competences = [(cc, comp) for cc, comp in competences if comp.type_competence == 'technique']
                        if tech_competences:
                            for cc, comp in tech_competences[:10]:  # Top 10
                                niveau_icon = "ðŸŸ¢" if cc.niveau_maitrise == "expert" else ("ðŸŸ¡" if cc.niveau_maitrise == "intermediaire" else "ðŸ”´")
                                st.write(f"{niveau_icon} **{comp.nom}** ({cc.annees_experience:.1f} ans)")
                            
                            if len(tech_competences) > 10:
                                st.caption(f"... et {len(tech_competences) - 10} autres compÃ©tences techniques")
                        else:
                            st.write("Aucune compÃ©tence technique enregistrÃ©e")
                        
                        st.markdown("#### ðŸŽ¯ CompÃ©tences fonctionnelles")
                        func_competences = [(cc, comp) for cc, comp in competences if comp.type_competence == 'fonctionnelle']
                        if func_competences:
                            for cc, comp in func_competences[:5]:  # Top 5
                                niveau_icon = "ðŸŸ¢" if cc.niveau_maitrise == "expert" else ("ðŸŸ¡" if cc.niveau_maitrise == "intermediaire" else "ðŸ”´")
                                st.write(f"{niveau_icon} **{comp.nom}** ({cc.annees_experience:.1f} ans)")
                            
                            if len(func_competences) > 5:
                                st.caption(f"... et {len(func_competences) - 5} autres compÃ©tences fonctionnelles")
                        else:
                            st.write("Aucune compÃ©tence fonctionnelle enregistrÃ©e")
                
                except Exception as e:
                    st.error(f"Erreur lors du chargement des compÃ©tences: {e}")
            
            st.info("ðŸ’¡ **Note**: L'analyse du CV ajoutera de nouvelles missions et compÃ©tences Ã  ce profil existant. Les doublons seront automatiquement Ã©vitÃ©s.")
        
        # Upload de fichier
        uploaded_file = st.file_uploader(
            "ðŸ“Ž Choisir un fichier CV",
            type=['pdf', 'docx', 'doc', 'pptx', 'ppt'],
            help="Formats supportÃ©s: PDF, Word (DOCX, DOC), PowerPoint (PPTX, PPT)"
        )
        
        if uploaded_file is not None:
            # Afficher les informations du fichier
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("ðŸ“„ Nom du fichier", uploaded_file.name)
            
            with col2:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.metric("ðŸ’¾ Taille", f"{file_size_mb:.2f} MB")
            
            with col3:
                st.metric("ðŸ”§ Type", uploaded_file.type or "Non dÃ©tectÃ©")
            
            # Bouton pour sauvegarder (basique)
            if st.button("ðŸ’¾ Sauvegarder le CV", type="primary", use_container_width=True):
                with st.spinner("ðŸ”„ Sauvegarde en cours..."):
                    # CrÃ©er le rÃ©pertoire pour le consultant
                    consultant_dir = f"data/uploads/consultant_{selected_consultant.id}"
                    os.makedirs(consultant_dir, exist_ok=True)
                    
                    # GÃ©nÃ©rer un nom de fichier unique
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_filename = f"{timestamp}_{uploaded_file.name}"
                    file_path = os.path.join(consultant_dir, safe_filename)
                    
                    # Sauvegarder le fichier
                    try:
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        st.success(f"âœ… CV sauvegardÃ© avec succÃ¨s !")
                        st.success(f"ðŸ“ Fichier: {safe_filename}")
                        st.success(f"ðŸ“ Emplacement: {file_path}")
                        
                        # TODO: Ici on pourra ajouter l'analyse du contenu plus tard
                        st.info("ðŸ” Analyse du contenu - FonctionnalitÃ© Ã  venir")
                        
                    except Exception as e:
                        st.error(f"âŒ Erreur lors de la sauvegarde: {e}")
            
            # AperÃ§u des documents existants
            consultant_dir = f"data/uploads/consultant_{selected_consultant.id}"
            if os.path.exists(consultant_dir):
                files = [f for f in os.listdir(consultant_dir) if os.path.isfile(os.path.join(consultant_dir, f))]
                
                if files:
                    st.markdown("### ðŸ“ Documents existants")
                    for file in files:
                        file_path = os.path.join(consultant_dir, file)
                        file_size = os.path.getsize(file_path)
                        file_size_mb = file_size / (1024 * 1024)
                        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        # Conteneur pour chaque fichier
                        with st.container():
                            col1, col2, col3, col4, col5, col6 = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 0.7])
                            
                            with col1:
                                # IcÃ´ne selon le type de fichier
                                if file.lower().endswith('.pdf'):
                                    icon = "ðŸ“„"
                                elif file.lower().endswith(('.doc', '.docx')):
                                    icon = "ðŸ“"
                                elif file.lower().endswith(('.ppt', '.pptx')):
                                    icon = "ðŸ“Š"
                                else:
                                    icon = "ï¿½"
                                
                                st.write(f"{icon} **{file}**")
                                st.caption(f"ðŸ“… {file_modified.strftime('%d/%m/%Y %H:%M')} â€¢ ðŸ’¾ {file_size_mb:.2f} MB")
                            
                            with col2:
                                # Bouton de tÃ©lÃ©chargement
                                try:
                                    with open(file_path, "rb") as f:
                                        file_bytes = f.read()
                                    
                                    st.download_button(
                                        label="ðŸ“¥",
                                        data=file_bytes,
                                        file_name=file,
                                        mime="application/octet-stream",
                                        key=f"download_{file}",
                                        help="TÃ©lÃ©charger le fichier"
                                    )
                                except Exception as e:
                                    st.error(f"âŒ Erreur lecture: {e}")
                            
                            with col3:
                                # Bouton de visualisation/aperÃ§u
                                if st.button("ðŸ‘ï¸", key=f"view_{file}", help="AperÃ§u du fichier"):
                                    st.session_state[f"show_preview_{file}"] = True
                            
                            with col4:
                                # Bouton d'informations
                                if st.button("â„¹ï¸", key=f"info_{file}", help="Informations dÃ©taillÃ©es"):
                                    st.session_state[f"show_info_{file}"] = True
                            
                            with col5:
                                # Bouton d'analyse de CV
                                if st.button("ðŸ”", key=f"analyze_{file}", help="Analyser le CV"):
                                    # DÃ©clencher l'analyse
                                    with st.spinner("ðŸ”„ Analyse du CV en cours..."):
                                        
                                        # Extraire le texte
                                        text = DocumentAnalyzer.extract_text_from_file(file_path)
                                        
                                        if text.strip():
                                            # Analyser le contenu
                                            analysis = DocumentAnalyzer.analyze_cv_content(
                                                text, 
                                                f"{selected_consultant.prenom} {selected_consultant.nom}"
                                            )
                                            
                                            # Sauvegarder l'analyse pour prÃ©visualisation
                                            st.session_state[f"analysis_{file}"] = analysis
                                            st.session_state[f"show_analysis_{file}"] = True
                                            
                                            st.success("âœ… Analyse terminÃ©e ! VÃ©rifiez les rÃ©sultats ci-dessous.")
                                            st.rerun()
                                        else:
                                            st.error("âŒ Impossible d'extraire le texte du fichier")
                            
                            with col6:
                                # Bouton de suppression
                                if st.button("ðŸ—‘ï¸", key=f"del_{file}", help="Supprimer"):
                                    try:
                                        os.remove(file_path)
                                        st.success(f"âœ… {file} supprimÃ©")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"âŒ Erreur: {e}")
                        
                        # Affichage conditionnel de l'aperÃ§u
                        if st.session_state.get(f"show_preview_{file}", False):
                            with st.expander(f"ðŸ‘ï¸ AperÃ§u de {file}", expanded=True):
                                try:
                                    if file.lower().endswith('.pdf'):
                                        st.info("ðŸ“„ Fichier PDF - AperÃ§u non disponible dans cette version")
                                        st.markdown(f"**Chemin complet:** `{file_path}`")
                                        
                                        # Option pour ouvrir avec l'application par dÃ©faut
                                        if st.button(f"ðŸš€ Ouvrir avec l'application par dÃ©faut", key=f"open_{file}"):
                                            try:
                                                import subprocess
                                                import platform
                                                
                                                if platform.system() == 'Windows':
                                                    os.startfile(file_path)
                                                elif platform.system() == 'Darwin':  # macOS
                                                    subprocess.call(['open', file_path])
                                                else:  # Linux
                                                    subprocess.call(['xdg-open', file_path])
                                                
                                                st.success(f"ðŸš€ Ouverture de {file}")
                                            except Exception as e:
                                                st.error(f"âŒ Impossible d'ouvrir le fichier: {e}")
                                    
                                    elif file.lower().endswith(('.doc', '.docx')):
                                        st.info("ðŸ“ Fichier Word - AperÃ§u non disponible dans cette version")
                                        st.markdown(f"**Chemin complet:** `{file_path}`")
                                        
                                        # Option pour ouvrir avec l'application par dÃ©faut
                                        if st.button(f"ðŸš€ Ouvrir avec Word", key=f"open_{file}"):
                                            try:
                                                os.startfile(file_path)
                                                st.success(f"ðŸš€ Ouverture de {file}")
                                            except Exception as e:
                                                st.error(f"âŒ Impossible d'ouvrir le fichier: {e}")
                                    
                                    elif file.lower().endswith(('.ppt', '.pptx')):
                                        st.info("ðŸ“Š Fichier PowerPoint - AperÃ§u non disponible dans cette version")
                                        st.markdown(f"**Chemin complet:** `{file_path}`")
                                        
                                        # Option pour ouvrir avec l'application par dÃ©faut
                                        if st.button(f"ðŸš€ Ouvrir avec PowerPoint", key=f"open_{file}"):
                                            try:
                                                os.startfile(file_path)
                                                st.success(f"ðŸš€ Ouverture de {file}")
                                            except Exception as e:
                                                st.error(f"âŒ Impossible d'ouvrir le fichier: {e}")
                                    
                                    else:
                                        st.warning("â“ Type de fichier non reconnu pour l'aperÃ§u")
                                    
                                except Exception as e:
                                    st.error(f"âŒ Erreur lors de l'aperÃ§u: {e}")
                                
                                # Bouton pour fermer l'aperÃ§u
                                if st.button("âŒ Fermer l'aperÃ§u", key=f"close_preview_{file}"):
                                    del st.session_state[f"show_preview_{file}"]
                                    st.rerun()
                        
                        # Affichage conditionnel des informations dÃ©taillÃ©es
                        if st.session_state.get(f"show_info_{file}", False):
                            with st.expander(f"â„¹ï¸ Informations dÃ©taillÃ©es - {file}", expanded=True):
                                try:
                                    file_stat = os.stat(file_path)
                                    
                                    info_data = {
                                        "ðŸ“„ Nom du fichier": file,
                                        "ðŸ“ Chemin complet": file_path,
                                        "ðŸ’¾ Taille": f"{file_size_mb:.2f} MB ({file_size:,} bytes)",
                                        "ðŸ“… Date de crÃ©ation": datetime.fromtimestamp(file_stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                                        "ðŸ”„ DerniÃ¨re modification": file_modified.strftime("%d/%m/%Y %H:%M:%S"),
                                        "ðŸ‘¤ Consultant associÃ©": f"{selected_consultant.prenom} {selected_consultant.nom}",
                                        "ðŸ”§ Type MIME": "application/pdf" if file.lower().endswith('.pdf') else "application/octet-stream"
                                    }
                                    
                                    for key, value in info_data.items():
                                        st.write(f"**{key}:** {value}")
                                
                                except Exception as e:
                                    st.error(f"âŒ Erreur lors de la rÃ©cupÃ©ration des informations: {e}")
                                
                                # Bouton pour fermer les informations
                                if st.button("âŒ Fermer les informations", key=f"close_info_{file}"):
                                    del st.session_state[f"show_info_{file}"]
                                    st.rerun()
                        
                        # Affichage conditionnel de l'analyse de CV
                        if st.session_state.get(f"show_analysis_{file}", False):
                            analysis_data = st.session_state.get(f"analysis_{file}", {})
                            
                            with st.expander(f"ðŸ” Analyse du CV - {file}", expanded=True):
                                if analysis_data:
                                    # Afficher l'aperÃ§u de l'analyse
                                    preview_text = DocumentAnalyzer.get_analysis_preview(analysis_data)
                                    st.markdown(preview_text)
                                    
                                    st.markdown("---")
                                    
                                    # Section de validation et modification
                                    st.subheader("âœ… Validation et modification")
                                    st.info("ðŸ”§ Vous pouvez modifier les donnÃ©es dÃ©tectÃ©es avant de les sauvegarder")
                                    
                                    # Formulaire d'Ã©dition des missions
                                    missions = analysis_data.get('missions', [])
                                    if missions:
                                        st.markdown("### ðŸš€ Missions dÃ©tectÃ©es")
                                        
                                        edited_missions = []
                                        for i, mission in enumerate(missions):
                                            with st.container():
                                                st.markdown(f"**Mission {i+1}:**")
                                                
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    client = st.text_input(
                                                        "Client", 
                                                        value=mission.get('client', ''), 
                                                        key=f"edit_client_{file}_{i}"
                                                    )
                                                    date_debut = st.text_input(
                                                        "Date dÃ©but", 
                                                        value=mission.get('date_debut', ''), 
                                                        key=f"edit_debut_{file}_{i}"
                                                    )
                                                
                                                with col2:
                                                    date_fin = st.text_input(
                                                        "Date fin", 
                                                        value=mission.get('date_fin', ''), 
                                                        key=f"edit_fin_{file}_{i}"
                                                    )
                                                
                                                resume = st.text_area(
                                                    "RÃ©sumÃ© de mission", 
                                                    value=mission.get('resume', ''), 
                                                    key=f"edit_resume_{file}_{i}",
                                                    height=60
                                                )
                                                
                                                # Technologies de cette mission
                                                techs = st.text_input(
                                                    "Technologies (sÃ©parÃ©es par des virgules)", 
                                                    value=', '.join(mission.get('langages_techniques', [])), 
                                                    key=f"edit_techs_{file}_{i}"
                                                )
                                                
                                                # Sauvegarder la mission Ã©ditÃ©e
                                                edited_mission = {
                                                    'client': client,
                                                    'date_debut': date_debut,
                                                    'date_fin': date_fin,
                                                    'resume': resume,
                                                    'langages_techniques': [t.strip() for t in techs.split(',') if t.strip()]
                                                }
                                                edited_missions.append(edited_mission)
                                                
                                                st.divider()
                                    
                                    # CompÃ©tences techniques globales
                                    st.markdown("### ðŸ’» CompÃ©tences techniques")
                                    current_techs = ', '.join(analysis_data.get('langages_techniques', []))
                                    edited_global_techs = st.text_area(
                                        "Technologies et langages (une par ligne ou sÃ©parÃ©es par des virgules)",
                                        value=current_techs,
                                        key=f"edit_global_techs_{file}",
                                        height=100
                                    )
                                    
                                    # CompÃ©tences fonctionnelles
                                    st.markdown("### ðŸŽ¯ CompÃ©tences fonctionnelles")
                                    current_func = ', '.join(analysis_data.get('competences_fonctionnelles', []))
                                    edited_func_skills = st.text_area(
                                        "CompÃ©tences fonctionnelles (une par ligne ou sÃ©parÃ©es par des virgules)",
                                        value=current_func,
                                        key=f"edit_func_skills_{file}",
                                        height=100
                                    )
                                    
                                    st.markdown("---")
                                    
                                    # Boutons d'action
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        if st.button("ðŸ’¾ Sauvegarder dans le profil", key=f"save_analysis_{file}", type="primary"):
                                            # PrÃ©parer les donnÃ©es finales
                                            final_missions = [m for m in edited_missions if m['client'].strip()]
                                            
                                            # Parser les compÃ©tences techniques
                                            global_techs = []
                                            for tech in edited_global_techs.replace('\n', ',').split(','):
                                                tech = tech.strip()
                                                if tech:
                                                    global_techs.append(tech)
                                            
                                            # Parser les compÃ©tences fonctionnelles
                                            func_skills = []
                                            for skill in edited_func_skills.replace('\n', ',').split(','):
                                                skill = skill.strip()
                                                if skill:
                                                    func_skills.append(skill)
                                            
                                            # PrÃ©parer les donnÃ©es pour la sauvegarde
                                            final_analysis = {
                                                'missions': final_missions,
                                                'langages_techniques': global_techs,
                                                'competences_fonctionnelles': func_skills,
                                                'consultant': f"{selected_consultant.prenom} {selected_consultant.nom}"
                                            }
                                            
                                            # Sauvegarder en base de donnÃ©es
                                            try:
                                                success = ConsultantService.save_cv_analysis(selected_consultant.id, final_analysis)
                                                
                                                if success:
                                                    st.success(f"âœ… Analyse sauvegardÃ©e avec succÃ¨s dans le profil de {selected_consultant.prenom} {selected_consultant.nom} !")
                                                    st.balloons()
                                                    
                                                    # Afficher un rÃ©sumÃ© de ce qui a Ã©tÃ© sauvegardÃ©
                                                    with st.expander("ðŸ“‹ RÃ©sumÃ© des donnÃ©es sauvegardÃ©es", expanded=True):
                                                        st.write(f"**ðŸ‘¤ Consultant:** {selected_consultant.prenom} {selected_consultant.nom}")
                                                        st.write(f"**ðŸš€ Missions ajoutÃ©es:** {len(final_missions)}")
                                                        for mission in final_missions:
                                                            st.write(f"  â€¢ {mission['client']} ({mission['date_debut']} â†’ {mission['date_fin']})")
                                                        st.write(f"**ðŸ’» Technologies ajoutÃ©es:** {len(global_techs)}")
                                                        if global_techs:
                                                            st.write(f"  {', '.join(global_techs[:10])}{'...' if len(global_techs) > 10 else ''}")
                                                        st.write(f"**ðŸŽ¯ CompÃ©tences fonctionnelles ajoutÃ©es:** {len(func_skills)}")
                                                        if func_skills:
                                                            st.write(f"  {', '.join(func_skills)}")
                                                        
                                                        st.info("ðŸ’¡ **Note:** Les compÃ©tences et missions en doublon ont Ã©tÃ© automatiquement ignorÃ©es.")
                                                        
                                                        # Proposer de voir le profil mis Ã  jour
                                                        if st.button("ðŸ‘€ Voir le profil mis Ã  jour", key=f"view_profile_{file}"):
                                                            st.session_state.view_consultant_id = selected_consultant.id
                                                            st.rerun()
                                                else:
                                                    st.error("âŒ Erreur lors de la sauvegarde. VÃ©rifiez les logs pour plus de dÃ©tails.")
                                                    
                                            except Exception as e:
                                                st.error(f"âŒ Erreur lors de la sauvegarde: {e}")
                                                st.exception(e)
                                            
                                            # Nettoyer les Ã©tats de session aprÃ¨s sauvegarde rÃ©ussie
                                            if success:
                                                if f"analysis_{file}" in st.session_state:
                                                    del st.session_state[f"analysis_{file}"]
                                                if f"show_analysis_{file}" in st.session_state:
                                                    del st.session_state[f"show_analysis_{file}"]
                                    
                                    with col2:
                                        if st.button("ðŸ”„ Re-analyser", key=f"reanalyze_{file}"):
                                            # Relancer l'analyse
                                            with st.spinner("ðŸ”„ Nouvelle analyse en cours..."):
                                                
                                                text = DocumentAnalyzer.extract_text_from_file(file_path)
                                                if text.strip():
                                                    new_analysis = DocumentAnalyzer.analyze_cv_content(
                                                        text, 
                                                        f"{selected_consultant.prenom} {selected_consultant.nom}"
                                                    )
                                                    st.session_state[f"analysis_{file}"] = new_analysis
                                                    st.success("âœ… Nouvelle analyse terminÃ©e !")
                                                    st.rerun()
                                    
                                    with col3:
                                        if st.button("âŒ Fermer l'analyse", key=f"close_analysis_{file}"):
                                            # Nettoyer les Ã©tats de session
                                            if f"analysis_{file}" in st.session_state:
                                                del st.session_state[f"analysis_{file}"]
                                            if f"show_analysis_{file}" in st.session_state:
                                                del st.session_state[f"show_analysis_{file}"]
                                            st.rerun()
                                else:
                                    st.error("âŒ Aucune donnÃ©e d'analyse disponible")
                        
                        st.divider()
    else:
        st.warning("âš ï¸ Aucun consultant disponible. Ajoutez d'abord des consultants.")

# Copier toutes les autres fonctions depuis l'original
def show_consultant_profile():
    """Affiche le profil dÃ©taillÃ© d'un consultant"""
    
    consultant_id = st.session_state.view_consultant_profile
    consultant = ConsultantService.get_consultant_by_id(consultant_id)
    
    if not consultant:
        st.error("âŒ Consultant introuvable")
        del st.session_state.view_consultant_profile
        st.rerun()
        return
    
    # En-tÃªte avec bouton retour
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.title(f"ðŸ‘¤ Profil de {consultant.prenom} {consultant.nom}")
    
    with col2:
        if st.button("â† Retour", key="back_to_list"):
            del st.session_state.view_consultant_profile
            st.rerun()
    
    st.markdown("---")
    
    # Informations principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("ðŸ’° Salaire annuel", f"{consultant.salaire_actuel or 0:,}â‚¬", delta=None)
        
    with col2:
        status = "Disponible" if consultant.disponibilite else "En mission"
        st.metric("ðŸ“Š Statut", status)
        
    with col3:
        creation_date = consultant.date_creation.strftime("%d/%m/%Y") if consultant.date_creation else "N/A"
        st.metric("ðŸ“… Membre depuis", creation_date)
    
    st.markdown("---")
    
    # DÃ©tails du profil
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["ðŸ“‹ Informations", "ðŸ’¼ CompÃ©tences", "ðŸš€ Missions", "ðŸ“„ Documents", "âš™ï¸ Actions"])
    
    with tab1:
        show_consultant_info(consultant)
    
    with tab2:
        show_consultant_skills(consultant)
    
    with tab3:
        show_consultant_missions(consultant)
    
    with tab4:
        show_consultant_documents(consultant)
    
    with tab5:
        show_consultant_actions(consultant)

def show_consultant_info(consultant):
    """Affiche et permet la modification des informations de base du consultant"""
    
    st.subheader("ðŸ“‹ Informations personnelles")
    
    # Formulaire toujours actif pour modification directe
    with st.form(f"edit_consultant_info_{consultant.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("ðŸ‘¤ PrÃ©nom *", value=consultant.prenom, placeholder="Ex: Jean")
            email = st.text_input("ðŸ“§ Email *", value=consultant.email, placeholder="jean.dupont@example.com")
            salaire = st.number_input("ðŸ’° Salaire annuel (â‚¬)", 
                                    min_value=0, 
                                    value=int(consultant.salaire_actuel or 0), 
                                    step=1000)
        
        with col2:
            nom = st.text_input("ðŸ‘¤ Nom *", value=consultant.nom, placeholder="Ex: Dupont")
            telephone = st.text_input("ðŸ“ž TÃ©lÃ©phone", 
                                    value=consultant.telephone or "", 
                                    placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("âœ… Disponible", value=consultant.disponibilite)
        
        # Notes
        notes = st.text_area("ðŸ“ Notes", 
                            value=consultant.notes or "",
                            height=100,
                            placeholder="Notes sur le consultant...")
        
        # Bouton de sauvegarde centrÃ© et visible
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col2:
            submitted = st.form_submit_button("ðŸ’¾ Sauvegarder les modifications", 
                                            use_container_width=True,
                                            type="primary")
        
        if submitted:
            # Validation
            if not prenom or not nom or not email:
                st.error("âŒ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # VÃ©rifier l'unicitÃ© de l'email (sauf pour le consultant actuel)
                existing_consultant = ConsultantService.get_consultant_by_email(email)
                if existing_consultant and existing_consultant.id != consultant.id:
                    st.error(f"âŒ Un consultant avec l'email {email} existe dÃ©jÃ  !")
                else:
                    try:
                        # DonnÃ©es de mise Ã  jour
                        update_data = {
                            'prenom': prenom.strip(),
                            'nom': nom.strip(),
                            'email': email.strip().lower(),
                            'telephone': telephone.strip() if telephone else None,
                            'salaire_actuel': salaire,
                            'disponibilite': disponibilite,
                            'notes': notes.strip() if notes else None
                        }
                        
                        # Mettre Ã  jour le consultant
                        ConsultantService.update_consultant(consultant.id, update_data)
                        
                        st.success(f"âœ… {prenom} {nom} a Ã©tÃ© modifiÃ© avec succÃ¨s !")
                        
                        # Actualiser la page de profil
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"âŒ Erreur lors de la modification: {e}")
    
    # Section de suppression
    st.markdown("---")
    st.subheader("ðŸ—‘ï¸ Zone de danger")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.warning("âš ï¸ **Attention**: La suppression du consultant est irrÃ©versible et effacera toutes ses donnÃ©es.")
    
    with col2:
        if st.button("ðŸ—‘ï¸ Supprimer le consultant", 
                    type="secondary", 
                    use_container_width=True,
                    key="delete_consultant_btn"):
            st.session_state.show_delete_confirmation = True
            st.rerun()
    
    # BoÃ®te de dialogue de confirmation
    if st.session_state.get('show_delete_confirmation', False):
        with st.container():
            st.error("ðŸš¨ **Confirmation de suppression**")
            st.write(f"Voulez-vous vraiment supprimer **{consultant.prenom} {consultant.nom}** ?")
            st.write("Cette action supprimera dÃ©finitivement :")
            st.write("â€¢ Toutes les informations personnelles")
            st.write("â€¢ Toutes les compÃ©tences associÃ©es")
            st.write("â€¢ Toutes les missions")
            st.write("â€¢ Tous les documents uploadÃ©s")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("âœ… Oui, supprimer dÃ©finitivement", 
                            type="primary", 
                            use_container_width=True,
                            key="confirm_delete"):
                    try:
                        # Supprimer le consultant
                        ConsultantService.delete_consultant(consultant.id)
                        
                        st.success(f"âœ… {consultant.prenom} {consultant.nom} a Ã©tÃ© supprimÃ© avec succÃ¨s !")
                        
                        # Nettoyer les Ã©tats de session
                        st.session_state.show_delete_confirmation = False
                        
                        # Retourner Ã  la liste des consultants
                        del st.session_state.view_consultant_profile
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"âŒ Erreur lors de la suppression: {e}")
            
            with col2:
                if st.button("âŒ Non, annuler", 
                            use_container_width=True,
                            key="cancel_delete"):
                    st.session_state.show_delete_confirmation = False
                    st.rerun()
    
    # Informations systÃ¨me (toujours en lecture seule)
    st.markdown("---")
    st.subheader("ðŸ”§ Informations systÃ¨me")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**ðŸ“… Date de crÃ©ation**")
        creation_date = consultant.date_creation.strftime("%d/%m/%Y Ã  %H:%M") if consultant.date_creation else "N/A"
        st.info(creation_date)
    
    with col2:
        st.write("**ðŸ”„ DerniÃ¨re modification**")
        maj_date = consultant.derniere_maj.strftime("%d/%m/%Y Ã  %H:%M") if consultant.derniere_maj else "N/A"
        st.info(maj_date)

def show_consultant_skills(consultant):
    """Affiche les compÃ©tences du consultant"""
    
    st.subheader("ðŸ’¼ CompÃ©tences")
    
    # TODO: RÃ©cupÃ©rer les vraies compÃ©tences depuis la base de donnÃ©es
    # Pour l'instant, simulation avec des donnÃ©es d'exemple
    
    skills_data = [
        {"CompÃ©tence": "Python", "Niveau": "Expert", "AnnÃ©es d'expÃ©rience": 5, "DerniÃ¨re utilisation": "2024"},
        {"CompÃ©tence": "Machine Learning", "Niveau": "AvancÃ©", "AnnÃ©es d'expÃ©rience": 3, "DerniÃ¨re utilisation": "2024"},
        {"CompÃ©tence": "SQL", "Niveau": "Expert", "AnnÃ©es d'expÃ©rience": 4, "DerniÃ¨re utilisation": "2024"},
        {"CompÃ©tence": "Docker", "Niveau": "IntermÃ©diaire", "AnnÃ©es d'expÃ©rience": 2, "DerniÃ¨re utilisation": "2023"},
    ]
    
    if skills_data:
        # Affichage des compÃ©tences sous forme de badges et tableau
        st.write("**ðŸ·ï¸ Badges de compÃ©tences**")
        
        cols = st.columns(4)
        for i, skill in enumerate(skills_data):
            with cols[i % 4]:
                level_color = {
                    "Expert": "ðŸŸ¢",
                    "AvancÃ©": "ðŸŸ¡", 
                    "IntermÃ©diaire": "ðŸŸ ",
                    "DÃ©butant": "ðŸ”´"
                }.get(skill["Niveau"], "âšª")
                
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; text-align: center;">
                    {level_color} <strong>{skill["CompÃ©tence"]}</strong><br>
                    <small>{skill["Niveau"]} â€¢ {skill["AnnÃ©es d'expÃ©rience"]} ans</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.write("**ðŸ“Š DÃ©tail des compÃ©tences**")
        
        df_skills = pd.DataFrame(skills_data)
        st.dataframe(df_skills, use_container_width=True, hide_index=True)
        
        # Actions sur les compÃ©tences
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("âž• Ajouter une compÃ©tence"):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Redirection vers gestion des compÃ©tences")
        
        with col2:
            if st.button("âœï¸ Modifier les compÃ©tences"):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Ã‰dition des compÃ©tences")
        
        with col3:
            if st.button("ðŸ“Š Analyse des compÃ©tences"):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Analytics des compÃ©tences")
    
    else:
        st.info("ðŸ“ Aucune compÃ©tence enregistrÃ©e pour ce consultant")
        if st.button("âž• Ajouter des compÃ©tences"):
            st.info("ðŸ”§ Redirection vers la gestion des compÃ©tences...")

def show_consultant_missions(consultant):
    """Affiche l'historique des missions du consultant avec Ã©dition"""
    
    st.subheader("ðŸš€ Historique des missions")
    
    # Onglets pour organiser les fonctionnalitÃ©s
    tab1, tab2 = st.tabs(["ðŸ“‹ Missions existantes", "âž• Ajouter une mission"])
    
    with tab1:
        show_existing_missions(consultant)
    
    with tab2:
        show_add_mission_form(consultant)

def show_existing_missions(consultant):
    """Affiche et permet d'Ã©diter les missions existantes"""
    
    # RÃ©cupÃ©rer les vraies missions depuis la base de donnÃ©es
    try:
        with get_database_session() as session:
            missions_db = session.query(Mission).filter(
                Mission.consultant_id == consultant.id
            ).order_by(Mission.date_debut.desc()).all()
            
    except Exception as e:
        st.error(f"âŒ Erreur lors de la rÃ©cupÃ©ration des missions: {e}")
        missions_db = []
    
    if missions_db:
        # MÃ©triques des missions
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenus = sum(m.revenus_generes or 0 for m in missions_db)
        missions_terminees = len([m for m in missions_db if m.statut == "terminee"])
        missions_en_cours = len([m for m in missions_db if m.statut == "en_cours"])
        
        with col1:
            st.metric("ðŸ’° Revenus totaux", f"{total_revenus:,}â‚¬")
        
        with col2:
            st.metric("âœ… Missions terminÃ©es", missions_terminees)
        
        with col3:
            st.metric("ðŸ”„ Missions en cours", missions_en_cours)
        
        with col4:
            st.metric("ðŸ“Š Total missions", len(missions_db))
        
        st.markdown("---")
        
        # Mode Ã©dition
        if st.checkbox("âœï¸ Mode Ã©dition", key="edit_mode"):
            st.info("ðŸ“ Mode Ã©dition activÃ© - Vous pouvez maintenant modifier les missions")
            
            for i, mission in enumerate(missions_db):
                with st.expander(f"âœï¸ Ã‰diter: {mission.client} - {mission.role or 'RÃ´le non dÃ©fini'}", expanded=False):
                    edit_mission_form(mission, f"edit_{mission.id}")
        else:
            # Affichage normal (lecture seule)
            for i, mission in enumerate(missions_db):
                with st.expander(f"ðŸš€ {mission.client} - {mission.role or 'RÃ´le non dÃ©fini'}", expanded=(i == 0)):
                    show_mission_details(mission, i)
    else:
        st.info("ðŸ“ Aucune mission enregistrÃ©e pour ce consultant")
        st.markdown("ðŸ’¡ Vous pouvez:")
        st.markdown("- Utiliser l'onglet **'Ajouter une mission'** pour crÃ©er une mission manuellement")
        st.markdown("- Importer un CV dans l'onglet **'Import CV'** pour dÃ©tecter automatiquement les missions")

def show_mission_details(mission, index):
    """Affiche les dÃ©tails d'une mission en lecture seule"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**ðŸ¢ Client**: {mission.client}")
        st.write(f"**ðŸ‘¤ RÃ´le**: {mission.role or 'Non spÃ©cifiÃ©'}")
        st.write(f"**ðŸ“… DÃ©but**: {mission.date_debut.strftime('%Y-%m-%d') if mission.date_debut else 'N/A'}")
        st.write(f"**ðŸ’° Revenus**: {mission.revenus_generes or 0:,}â‚¬")
    
    with col2:
        st.write(f"**ðŸ“… Fin**: {mission.date_fin.strftime('%Y-%m-%d') if mission.date_fin else 'En cours'}")
        
        # Statut avec couleur
        if mission.statut == 'terminee':
            st.success("âœ… TerminÃ©e")
        elif mission.statut == 'en_cours':
            st.info("ðŸ”„ En cours")
        else:
            st.warning("â¸ï¸ En pause")
    
    st.write(f"**ðŸ› ï¸ Technologies**: {mission.technologies_utilisees or 'Non spÃ©cifiÃ©es'}")
    
    # Description de la mission
    if mission.description and mission.description != "Aucune description":
        st.write("**ðŸ“ Description**:")
        st.text_area("Description", value=mission.description, height=100, key=f"desc_readonly_{index}", disabled=True, label_visibility="collapsed")

def edit_mission_form(mission, key_prefix):
    """Formulaire d'Ã©dition d'une mission existante"""
    
    with st.form(f"edit_mission_form_{key_prefix}"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom_mission = st.text_input("ðŸ“‹ Nom de la mission", value=mission.nom_mission or "", key=f"{key_prefix}_nom")
            client = st.text_input("ðŸ¢ Client", value=mission.client or "", key=f"{key_prefix}_client")
            role = st.text_input("ðŸ‘¤ RÃ´le", value=mission.role or "", key=f"{key_prefix}_role")
            revenus = st.number_input("ðŸ’° Revenus (â‚¬)", value=float(mission.revenus_generes or 0), min_value=0.0, key=f"{key_prefix}_revenus")
        
        with col2:
            date_debut = st.date_input("ï¿½ Date dÃ©but", value=mission.date_debut if mission.date_debut else None, key=f"{key_prefix}_debut")
            date_fin = st.date_input("ðŸ“… Date fin", value=mission.date_fin if mission.date_fin else None, key=f"{key_prefix}_fin")
            statut = st.selectbox("ðŸ“Š Statut", 
                                ["en_cours", "terminee", "en_pause"], 
                                index=["en_cours", "terminee", "en_pause"].index(mission.statut) if mission.statut in ["en_cours", "terminee", "en_pause"] else 0,
                                key=f"{key_prefix}_statut")
        
        technologies = technology_multiselect(
            label=" Technologies",
            key=f"{key_prefix}_tech",
            default_values=mission.technologies_utilisees.split(", ") if mission.technologies_utilisees else []
        )
        description = st.text_area("ðŸ“ Description", value=mission.description or "", height=100, key=f"{key_prefix}_desc")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("ï¿½ Sauvegarder les modifications", type="primary"):
                save_mission_changes(mission.id, {
                    'nom_mission': nom_mission,
                    'client': client,
                    'role': role,
                    'date_debut': date_debut,
                    'date_fin': date_fin,
                    'statut': statut,
                    'revenus_generes': revenus,
                    'technologies_utilisees': technologies,
                    'description': description
                })
        
        with col2:
            if st.form_submit_button("ðŸ—‘ï¸ Supprimer la mission", type="secondary"):
                delete_mission(mission.id)

def show_add_mission_form(consultant):
    """Formulaire d'ajout d'une nouvelle mission"""
    
    st.markdown("### âž• Ajouter une nouvelle mission")
    
    with st.form("add_mission_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom_mission = st.text_input("ðŸ“‹ Nom de la mission", placeholder="Ex: DÃ©veloppement application mobile")
            client = st.text_input("ðŸ¢ Client", placeholder="Ex: SociÃ©tÃ© GÃ©nÃ©rale")
            role = st.text_input("ðŸ‘¤ RÃ´le", placeholder="Ex: Lead Developer")
            revenus = st.number_input("ï¿½ Revenus (â‚¬)", min_value=0.0, value=0.0)
        
        with col2:
            date_debut = st.date_input("ðŸ“… Date dÃ©but")
            date_fin = st.date_input("ðŸ“… Date fin (optionnel)", value=None)
            statut = st.selectbox("ï¿½ Statut", ["en_cours", "terminee", "en_pause"])
        
        technologies_str = technology_multiselect(
            label="ðŸ› ï¸ Technologies",
            key="new_mission_tech",
            default_values=[]
        )
        description = st.text_area("ðŸ“ Description", height=100, placeholder="DÃ©crivez les activitÃ©s rÃ©alisÃ©es durant cette mission...")
        
        if st.form_submit_button("ï¿½ Ajouter la mission", type="primary"):
            add_new_mission(consultant.id, {
                'nom_mission': nom_mission,
                'client': client,
                'role': role,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'statut': statut,
                'revenus_generes': revenus,
                'technologies_utilisees': technologies_str,
                'description': description
            })

def save_mission_changes(mission_id, mission_data):
    """Sauvegarde les modifications d'une mission"""
    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()
            
            if mission:
                # Mettre Ã  jour les champs
                mission.nom_mission = mission_data['nom_mission']
                mission.client = mission_data['client']
                mission.role = mission_data['role']
                mission.date_debut = mission_data['date_debut']
                mission.date_fin = mission_data['date_fin']
                mission.statut = mission_data['statut']
                mission.revenus_generes = mission_data['revenus_generes']
                mission.technologies_utilisees = mission_data['technologies_utilisees']
                mission.description = mission_data['description']
                
                session.commit()
                st.success("âœ… Mission mise Ã  jour avec succÃ¨s !")
                st.rerun()
            else:
                st.error("âŒ Mission non trouvÃ©e")
                
    except Exception as e:
        st.error(f"âŒ Erreur lors de la sauvegarde: {e}")

def delete_mission(mission_id):
    """Supprime une mission"""
    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()
            
            if mission:
                session.delete(mission)
                session.commit()
                st.success("âœ… Mission supprimÃ©e avec succÃ¨s !")
                st.rerun()
            else:
                st.error("âŒ Mission non trouvÃ©e")
                
    except Exception as e:
        st.error(f"âŒ Erreur lors de la suppression: {e}")

def add_new_mission(consultant_id, mission_data):
    """Ajoute une nouvelle mission"""
    
    if not mission_data['nom_mission'] or not mission_data['client']:
        st.error("âŒ Le nom de la mission et le client sont obligatoires")
        return
    
    try:
        with get_database_session() as session:
            nouvelle_mission = Mission(
                consultant_id=consultant_id,
                nom_mission=mission_data['nom_mission'],
                client=mission_data['client'],
                role=mission_data['role'],
                date_debut=mission_data['date_debut'],
                date_fin=mission_data['date_fin'],
                statut=mission_data['statut'],
                revenus_generes=mission_data['revenus_generes'],
                technologies_utilisees=mission_data['technologies_utilisees'],
                description=mission_data['description']
            )
            
            session.add(nouvelle_mission)
            session.commit()
            st.success("âœ… Nouvelle mission ajoutÃ©e avec succÃ¨s !")
            st.rerun()
            
    except Exception as e:
        st.error(f"âŒ Erreur lors de l'ajout: {e}")
        st.markdown("""
        ðŸ’¡ **Astuce**: Pour ajouter automatiquement les missions d'un consultant:
        1. Utilisez la section "ðŸ“„ Import de CV" en bas de la page
        2. Uploadez le CV du consultant 
        3. L'algorithme dÃ©tectera automatiquement les missions, rÃ´les et technologies
        """)
        
        if st.button("âž• Ajouter une mission"):
            st.info("ðŸ”§ Redirection vers la gestion des missions...")

def show_consultant_documents(consultant):
    """Affiche les documents associÃ©s au consultant"""
    
    st.subheader("ðŸ“„ Documents")
    
    # VÃ©rifier les documents uploadÃ©s 
    consultant_dir = f"data/uploads/consultant_{consultant.id}"
    real_docs = []
    
    if os.path.exists(consultant_dir):
        files = [f for f in os.listdir(consultant_dir) if os.path.isfile(os.path.join(consultant_dir, f))]
        for file in files:
            file_path = os.path.join(consultant_dir, file)
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            real_docs.append({
                "Type": "CV" if any(ext in file.lower() for ext in ['.pdf', '.doc']) else "Document",
                "Nom": file,
                "Taille": f"{file_size_mb:.2f} MB",
                "Date": mod_time.strftime("%d/%m/%Y %H:%M"),
                "Path": file_path
            })
    
    # Simulation de documents par dÃ©faut
    documents = [
        {"Type": "CV", "Nom": f"CV_{consultant.prenom}_{consultant.nom}_2024.pdf", "Taille": "245 KB", "Date": "2024-03-15", "Path": None},
        {"Type": "Contrat", "Nom": "Contrat_freelance_2024.pdf", "Taille": "156 KB", "Date": "2024-01-10", "Path": None},
        {"Type": "Certificat", "Nom": "Certification_AWS_Solutions_Architect.pdf", "Taille": "98 KB", "Date": "2023-11-20", "Path": None},
    ]
    
    # Combiner les vrais documents et les simulÃ©s
    all_docs = real_docs + documents
    
    if all_docs:
        for doc in all_docs:
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([3, 1.5, 1, 1, 1, 1])
                
                with col1:
                    icon = {"CV": "ðŸ“„", "Contrat": "ðŸ“‹", "Certificat": "ðŸ†", "Document": "ðŸ“„"}.get(doc["Type"], "ðŸ“„")
                    is_real = "ðŸŸ¢" if doc.get("Path") else "ðŸ”´"
                    st.write(f"{is_real} {icon} **{doc['Nom']}**")
                    st.caption(f"ðŸ“‚ {doc['Type']} â€¢ ðŸ’¾ {doc['Taille']}")
                
                with col2:
                    st.write(f"ï¿½ {doc['Date']}")
                
                with col3:
                    # Bouton de tÃ©lÃ©chargement pour les vrais fichiers
                    if doc.get("Path"):
                        try:
                            with open(doc["Path"], "rb") as f:
                                file_bytes = f.read()
                            
                            st.download_button(
                                label="ðŸ“¥",
                                data=file_bytes,
                                file_name=doc["Nom"],
                                mime="application/octet-stream",
                                key=f"download_profile_{doc['Nom']}",
                                help="TÃ©lÃ©charger le fichier"
                            )
                        except Exception as e:
                            st.write("âŒ")
                    else:
                        if st.button("ðŸ“¥", key=f"download_sim_{doc['Nom']}", help="Document simulÃ©"):
                            st.info(f"ðŸ”§ Document simulÃ© - {doc['Nom']}")
                
                with col4:
                    # Bouton de visualisation pour les vrais fichiers
                    if doc.get("Path"):
                        if st.button("ðŸ‘ï¸", key=f"view_profile_{doc['Nom']}", help="AperÃ§u du fichier"):
                            st.session_state[f"show_profile_preview_{doc['Nom']}"] = True
                    else:
                        if st.button("ðŸ‘ï¸", key=f"view_sim_{doc['Nom']}", help="AperÃ§u simulÃ©"):
                            st.info(f"ï¿½ AperÃ§u simulÃ© - {doc['Nom']}")
                
                with col5:
                    # Bouton d'informations
                    if doc.get("Path"):
                        if st.button("â„¹ï¸", key=f"info_profile_{doc['Nom']}", help="Informations dÃ©taillÃ©es"):
                            st.session_state[f"show_profile_info_{doc['Nom']}"] = True
                    else:
                        if st.button("â„¹ï¸", key=f"info_sim_{doc['Nom']}", help="Informations simulÃ©es"):
                            st.info(f"ðŸ”§ Informations simulÃ©es - {doc['Nom']}")
                
                with col6:
                    # Bouton de suppression
                    if doc.get("Path"):  # Fichier rÃ©el
                        if st.button("ðŸ—‘ï¸", key=f"delete_profile_{doc['Nom']}", help="Supprimer"):
                            try:
                                os.remove(doc["Path"])
                                st.success(f"âœ… {doc['Nom']} supprimÃ©")
                                st.rerun()
                            except Exception as e:
                                st.error(f"âŒ Erreur: {e}")
                    else:  # Fichier simulÃ©
                        if st.button("ï¿½ï¸", key=f"delete_sim_{doc['Nom']}", help="Document simulÃ©"):
                            st.info(f"ðŸ”§ Document simulÃ© - {doc['Nom']}")
            
            # Affichage conditionnel de l'aperÃ§u (fichiers rÃ©els seulement)
            if doc.get("Path") and st.session_state.get(f"show_profile_preview_{doc['Nom']}", False):
                with st.expander(f"ðŸ‘ï¸ AperÃ§u de {doc['Nom']}", expanded=True):
                    try:
                        file_path = doc["Path"]
                        file_name = doc["Nom"]
                        
                        if file_name.lower().endswith('.pdf'):
                            st.info("ðŸ“„ Fichier PDF - AperÃ§u non disponible dans cette version")
                            st.markdown(f"**Chemin complet:** `{file_path}`")
                            
                            if st.button(f"ðŸš€ Ouvrir avec l'application par dÃ©faut", key=f"open_profile_{file_name}"):
                                try:
                                    os.startfile(file_path)
                                    st.success(f"ðŸš€ Ouverture de {file_name}")
                                except Exception as e:
                                    st.error(f"âŒ Impossible d'ouvrir le fichier: {e}")
                        
                        elif file_name.lower().endswith(('.doc', '.docx')):
                            st.info("ðŸ“ Fichier Word - AperÃ§u non disponible dans cette version")
                            st.markdown(f"**Chemin complet:** `{file_path}`")
                            
                            if st.button(f"ðŸš€ Ouvrir avec Word", key=f"open_profile_{file_name}"):
                                try:
                                    os.startfile(file_path)
                                    st.success(f"ðŸš€ Ouverture de {file_name}")
                                except Exception as e:
                                    st.error(f"âŒ Impossible d'ouvrir le fichier: {e}")
                        
                        elif file_name.lower().endswith(('.ppt', '.pptx')):
                            st.info("ðŸ“Š Fichier PowerPoint - AperÃ§u non disponible dans cette version")
                            st.markdown(f"**Chemin complet:** `{file_path}`")
                            
                            if st.button(f"ðŸš€ Ouvrir avec PowerPoint", key=f"open_profile_{file_name}"):
                                try:
                                    os.startfile(file_path)
                                    st.success(f"ðŸš€ Ouverture de {file_name}")
                                except Exception as e:
                                    st.error(f"âŒ Impossible d'ouvrir le fichier: {e}")
                        
                        else:
                            st.warning("â“ Type de fichier non reconnu pour l'aperÃ§u")
                        
                    except Exception as e:
                        st.error(f"âŒ Erreur lors de l'aperÃ§u: {e}")
                    
                    if st.button("âŒ Fermer l'aperÃ§u", key=f"close_profile_preview_{doc['Nom']}"):
                        del st.session_state[f"show_profile_preview_{doc['Nom']}"]
                        st.rerun()
            
            # Affichage conditionnel des informations dÃ©taillÃ©es (fichiers rÃ©els seulement)
            if doc.get("Path") and st.session_state.get(f"show_profile_info_{doc['Nom']}", False):
                with st.expander(f"â„¹ï¸ Informations dÃ©taillÃ©es - {doc['Nom']}", expanded=True):
                    try:
                        file_path = doc["Path"]
                        file_stat = os.stat(file_path)
                        file_size_bytes = os.path.getsize(file_path)
                        
                        info_data = {
                            "ðŸ“„ Nom du fichier": doc["Nom"],
                            "ðŸ“ Chemin complet": file_path,
                            "ðŸ’¾ Taille": f"{file_size_bytes / (1024 * 1024):.2f} MB ({file_size_bytes:,} bytes)",
                            "ï¿½ Date de crÃ©ation": datetime.fromtimestamp(file_stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                            "ðŸ”„ DerniÃ¨re modification": datetime.fromtimestamp(file_stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
                            "ðŸ‘¤ Consultant associÃ©": f"{consultant.prenom} {consultant.nom}",
                            "ðŸ”§ Type MIME": "application/pdf" if doc["Nom"].lower().endswith('.pdf') else "application/octet-stream"
                        }
                        
                        for key, value in info_data.items():
                            st.write(f"**{key}:** {value}")
                    
                    except Exception as e:
                        st.error(f"âŒ Erreur lors de la rÃ©cupÃ©ration des informations: {e}")
                    
                    if st.button("âŒ Fermer les informations", key=f"close_profile_info_{doc['Nom']}"):
                        del st.session_state[f"show_profile_info_{doc['Nom']}"]
                        st.rerun()
            
            st.divider()
        
        # Actions sur les documents
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("ðŸ“Ž Utilisez la section 'Import CV' ci-dessous pour ajouter de vrais documents")
        
        with col2:
            if st.button("ðŸ—‚ï¸ Organiser les documents"):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Gestion documentaire")
        
        with col3:
            if st.button("ðŸ“¤ Envoyer par email"):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Partage de documents")
    
    else:
        st.info("ðŸ“ Aucun document associÃ© Ã  ce consultant")
        st.info("ðŸ’¡ Utilisez la section 'Import CV' pour ajouter des documents")

def show_consultant_actions(consultant):
    """Affiche les actions possibles sur le consultant"""
    
    st.subheader("âš™ï¸ Actions")
    
    # Utiliser des sous-onglets pour organiser les actions
    action_tab1, action_tab2 = st.tabs(["ðŸ—‘ï¸ Supprimer", "ðŸ“Š Analytics"])
    
    with action_tab1:
        st.markdown("### ðŸ—‘ï¸ Supprimer le consultant")
        st.info("ðŸ’¡ **Info**: Vous pouvez modifier les informations directement dans l'onglet 'Informations'")
        show_delete_consultant_inline(consultant)
    
    with action_tab2:
        st.markdown("### ðŸ“Š Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("ðŸ“ˆ Rapport de performance", key="performance_report", use_container_width=True):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Rapport dÃ©taillÃ©")
            
            if st.button("ðŸ’° Analyse des revenus", key="revenue_analysis", use_container_width=True):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Analytics revenus")
        
        with col2:
            if st.button("ðŸŽ¯ Recommandations IA", key="ai_recommendations", use_container_width=True):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - IA recommendations")
            
            if st.button("ðŸ“‹ Dupliquer ce profil", key="duplicate_profile", use_container_width=True):
                st.info("ðŸ”§ FonctionnalitÃ© Ã  venir - Duplication de profil")


def show_edit_consultant_inline(consultant):
    """Formulaire de modification intÃ©grÃ© dans le profil"""
    
    # Formulaire de modification
    with st.form(f"edit_consultant_inline_{consultant.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("PrÃ©nom *", value=consultant.prenom, placeholder="Ex: Jean")
            email = st.text_input("Email *", value=consultant.email, placeholder="jean.dupont@example.com")
            salaire = st.number_input("Salaire annuel (â‚¬)", 
                                    min_value=0, 
                                    value=int(consultant.salaire_actuel or 0), 
                                    step=1000)
        
        with col2:
            nom = st.text_input("Nom *", value=consultant.nom, placeholder="Ex: Dupont")
            telephone = st.text_input("TÃ©lÃ©phone", 
                                    value=consultant.telephone or "", 
                                    placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("Disponible", value=consultant.disponibilite)
        
        # Boutons de soumission
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submitted = st.form_submit_button("âœ… Sauvegarder", use_container_width=True)
        
        with col2:
            cancelled = st.form_submit_button("âŒ Annuler", use_container_width=True)
        
        if submitted:
            # Validation
            if not prenom or not nom or not email:
                st.error("âŒ Veuillez remplir tous les champs obligatoires (*)")
                return
            
            # VÃ©rifier l'unicitÃ© de l'email (sauf pour le consultant actuel)
            existing_consultant = ConsultantService.get_consultant_by_email(email)
            if existing_consultant and existing_consultant.id != consultant.id:
                st.error(f"âŒ Un consultant avec l'email {email} existe dÃ©jÃ  !")
                return
            
            try:
                # DonnÃ©es de mise Ã  jour
                update_data = {
                    'prenom': prenom.strip(),
                    'nom': nom.strip(),
                    'email': email.strip().lower(),
                    'telephone': telephone.strip() if telephone else None,
                    'salaire_actuel': salaire,
                    'disponibilite': disponibilite
                }
                
                # Mettre Ã  jour le consultant
                ConsultantService.update_consultant(consultant.id, update_data)
                
                st.success(f"âœ… {prenom} {nom} a Ã©tÃ© modifiÃ© avec succÃ¨s !")
                
                # Actualiser la page de profil
                st.rerun()
                
            except Exception as e:
                st.error(f"âŒ Erreur lors de la modification: {e}")
        
        if cancelled:
            st.info("âŒ Modification annulÃ©e")


def show_delete_consultant_inline(consultant):
    """Interface de suppression intÃ©grÃ©e dans le profil"""
    
    st.warning("âš ï¸ **Attention**: Cette action est irrÃ©versible et supprimera dÃ©finitivement toutes les donnÃ©es du consultant.")
    
    # Afficher les informations Ã  supprimer
    with st.expander("ðŸ“‹ DonnÃ©es qui seront supprimÃ©es", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**ðŸ‘¤ Informations personnelles**")
            st.write(f"â€¢ Nom: {consultant.nom}")
            st.write(f"â€¢ PrÃ©nom: {consultant.prenom}")
            st.write(f"â€¢ Email: {consultant.email}")
            st.write(f"â€¢ TÃ©lÃ©phone: {consultant.telephone or 'N/A'}")
        
        with col2:
            st.write("**ðŸ’¼ DonnÃ©es professionnelles**")
            st.write(f"â€¢ Salaire: {consultant.salaire_actuel or 0:,}â‚¬")
            st.write(f"â€¢ Statut: {'Disponible' if consultant.disponibilite else 'En mission'}")
            
            # RÃ©cupÃ©rer les statistiques de maniÃ¨re sÃ©curisÃ©e
            consultant_stats = ConsultantService.get_consultant_with_stats(consultant.id)
            if consultant_stats:
                competences_count = consultant_stats['competences_count']
                missions_count = consultant_stats['missions_count']
            else:
                competences_count = 0
                missions_count = 0
            st.write(f"â€¢ CompÃ©tences: {competences_count}")
            st.write(f"â€¢ Missions: {missions_count}")
    
    # Confirmation de suppression
    st.markdown("---")
    st.markdown("### ï¿½ Confirmation de suppression")
    
    # Demander la confirmation textuelle
    confirmation_text = st.text_input(
        f"**Pour confirmer la suppression, tapez:** `{consultant.prenom} {consultant.nom}`",
        placeholder=f"Tapez: {consultant.prenom} {consultant.nom}"
    )
    
    # VÃ©rifier la confirmation
    expected_text = f"{consultant.prenom} {consultant.nom}"
    is_confirmed = confirmation_text.strip() == expected_text
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("ï¿½ï¸ SUPPRIMER DÃ‰FINITIVEMENT", 
                    disabled=not is_confirmed,
                    use_container_width=True,
                    key="delete_confirmed"):
            if is_confirmed:
                try:
                    ConsultantService.delete_consultant(consultant.id)
                    st.success(f"âœ… {consultant.prenom} {consultant.nom} a Ã©tÃ© supprimÃ© avec succÃ¨s !")
                    
                    # Retourner Ã  la liste
                    del st.session_state.view_consultant_profile
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"âŒ Erreur lors de la suppression: {e}")
    
    with col2:
        if st.button("âŒ Annuler", use_container_width=True, key="delete_cancel"):
            st.info("âŒ Suppression annulÃ©e")
    
    st.markdown("---")
    
    # Actions avancÃ©es
    st.markdown("### ðŸš€ Actions avancÃ©es")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("ðŸ“¤ Exporter le profil complet", use_container_width=True):
            st.info("ðŸ”§ Export PDF - FonctionnalitÃ© Ã  venir")
    
    with col2:
        if st.button("âœ‰ï¸ Envoyer par email", use_container_width=True):
            st.info("ðŸ”§ Email integration - FonctionnalitÃ© Ã  venir")
    
    with col3:
        if st.button("ðŸ”— Partager le profil", use_container_width=True):
            st.info("ðŸ”§ Partage sÃ©curisÃ© - FonctionnalitÃ© Ã  venir")

def clear_cache_and_refresh(keep_edit_id=False):
    """Nettoie le cache et force le rafraÃ®chissement des donnÃ©es"""
    # Nettoyer le cache Streamlit
    st.cache_data.clear()
    
    # Nettoyer les Ã©tats de session liÃ©s aux sÃ©lections
    keys_to_clear = [
        'selected_consultant_id', 
        'selected_consultant_name', 
        'show_delete_dialog'
    ]
    
    # Ajouter edit_consultant_id Ã  la liste seulement si on ne veut pas le garder
    if not keep_edit_id:
        keys_to_clear.append('edit_consultant_id')
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def show_consultants_list():
    """Affiche la liste des consultants avec options de filtrage"""
    
    st.subheader("ðŸ“‹ Liste des consultants")
    
    # VÃ©rifier si un consultant vient d'Ãªtre ajoutÃ©
    if 'newly_added_consultant' in st.session_state:
        consultant_name = st.session_state.newly_added_consultant
        st.success(f"ðŸŽ‰ **Nouveau consultant ajoutÃ©** : {consultant_name}")
        del st.session_state.newly_added_consultant
    
    # Filtres et bouton de rafraÃ®chissement
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        search_name = st.text_input("ðŸ” Rechercher par nom", placeholder="Nom ou prÃ©nom...")
    
    with col2:
        filter_availability = st.selectbox(
            "ðŸ“Š DisponibilitÃ©",
            ["Tous", "Disponible", "En mission"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "ðŸ“ˆ Trier par",
            ["Nom", "Date d'ajout", "DerniÃ¨re mise Ã  jour"]
        )
    
    with col4:
        st.write("")  # Espacement
        if st.button("ðŸ”„", help="Actualiser la liste", key="refresh_consultants"):
            clear_cache_and_refresh(keep_edit_id=True)
            st.rerun()
    
    # RÃ©cupÃ©rer les consultants depuis la base de donnÃ©es
    try:
        if search_name:
            consultants = ConsultantService.search_consultants(search_name)
        else:
            consultants = ConsultantService.get_all_consultants()
        
        if consultants:
            # Convertir en DataFrame pour l'affichage
            consultants_data = []
            for consultant in consultants:
                consultants_data.append({
                    "ID": consultant.id,
                    "Nom": consultant.nom,
                    "PrÃ©nom": consultant.prenom,
                    "Email": consultant.email,
                    "TÃ©lÃ©phone": consultant.telephone or "-",
                    "Salaire": consultant.salaire_actuel or 0,
                    "DisponibilitÃ©": "âœ… Disponible" if consultant.disponibilite else "ðŸ”´ En mission",
                    "DerniÃ¨re MAJ": consultant.derniere_maj.strftime("%Y-%m-%d") if consultant.derniere_maj else "-"
                })
            
            df = pd.DataFrame(consultants_data)
            
            # Appliquer le filtre de disponibilitÃ©
            if filter_availability != "Tous":
                status = "âœ… Disponible" if filter_availability == "Disponible" else "ðŸ”´ En mission"
                df = df[df['DisponibilitÃ©'] == status]
            
            # Afficher le tableau avec sÃ©lection
            if not df.empty:
                st.markdown("### ðŸ‘¥ Consultants - Cliquez sur une ligne pour voir le profil dÃ©taillÃ©")
                
                event = st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Nom": st.column_config.TextColumn(
                            "Nom",
                            help="Cliquez sur la ligne pour voir le profil dÃ©taillÃ©"
                        ),
                        "PrÃ©nom": st.column_config.TextColumn(
                            "PrÃ©nom", 
                            help="Cliquez sur la ligne pour voir le profil dÃ©taillÃ©"
                        ),
                        "Salaire": st.column_config.NumberColumn(
                            "Salaire (â‚¬)",
                            format="â‚¬%d"
                        ),
                        "Email": st.column_config.TextColumn(
                            "Email",
                            width="medium"
                        )
                    },
                    on_select="rerun",
                    selection_mode="single-row",
                    key="consultants_table"
                )
                
                # VÃ©rifier si une ligne est sÃ©lectionnÃ©e
                if event.selection.rows:
                    selected_row_index = event.selection.rows[0]
                    selected_consultant = df.iloc[selected_row_index]
                    
                    # Stocker les donnÃ©es du consultant sÃ©lectionnÃ©
                    st.session_state.selected_consultant_id = int(selected_consultant['ID'])
                    st.session_state.selected_consultant_name = f"{selected_consultant['PrÃ©nom']} {selected_consultant['Nom']}"
                    
                    # NOUVEAU : DÃ©finir automatiquement l'ID pour la modification
                    st.session_state.edit_consultant_id = int(selected_consultant['ID'])
                    
                    # Afficher automatiquement le profil dÃ©taillÃ©
                    st.session_state.view_consultant_profile = int(selected_consultant['ID'])
                    st.rerun()
                else:
                    st.info("ðŸ‘† Cliquez sur une ligne du tableau pour sÃ©lectionner un consultant")
                

                
                # Actions en lot
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Bouton de tÃ©lÃ©chargement CSV direct
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="ï¿½ TÃ©lÃ©charger CSV",
                        data=csv,
                        file_name=f"consultants_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("ðŸ“Š GÃ©nÃ©rer rapport"):
                        st.info("ðŸ“Š GÃ©nÃ©ration de rapport - FonctionnalitÃ© Ã  venir !")
                
                with col3:
                    if st.button("âœ‰ï¸ Email groupÃ©"):
                        st.info("âœ‰ï¸ Email groupÃ© - FonctionnalitÃ© Ã  venir !")
            
            else:
                st.info("Aucun consultant ne correspond aux critÃ¨res de recherche.")
        
        else:
            st.info("ðŸ“ Aucun consultant enregistrÃ©. Utilisez l'onglet 'Ajouter un consultant' pour commencer !")
    
    except Exception as e:
        st.error(f"âŒ Erreur lors du chargement des consultants: {e}")
        st.info("ðŸ”§ VÃ©rifiez que la base de donnÃ©es est initialisÃ©e.")

def show_add_consultant_form():
    """Affiche le formulaire d'ajout de consultant"""
    
    st.subheader("âž• Ajouter un nouveau consultant")
    
    # GÃ©nÃ©rer une clÃ© unique pour le formulaire pour forcer la rÃ©initialisation
    form_key = f"add_consultant_form_{st.session_state.get('form_reset_counter', 0)}"
    
    with st.form(form_key):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("PrÃ©nom *", placeholder="Ex: Jean")
            email = st.text_input("Email *", placeholder="jean.dupont@example.com")
            salaire = st.number_input("Salaire annuel (â‚¬)", min_value=0, value=45000, step=1000)
        
        with col2:
            nom = st.text_input("Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input("TÃ©lÃ©phone", placeholder="01.23.45.67.89")
            disponible = st.checkbox("Disponible", value=True)
        
        notes = st.text_area("Notes", placeholder="Informations complÃ©mentaires...")
        
        # Boutons du formulaire
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("âœ… Ajouter le consultant", type="primary")
        
        with col2:
            reset = st.form_submit_button("ðŸ”„ RÃ©initialiser")
        
        with col3:
            preview = st.form_submit_button("ðŸ‘ï¸ AperÃ§u")
        
        if submitted:
            # Validation des champs obligatoires
            if not prenom or not nom or not email:
                st.error("âŒ Veuillez remplir tous les champs obligatoires (PrÃ©nom, Nom, Email)")
            else:
                # PrÃ©parer les donnÃ©es
                consultant_data = {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire': salaire,
                    'disponible': disponible,
                    'notes': notes
                }
                
                # Sauvegarder en base de donnÃ©es
                if ConsultantService.create_consultant(consultant_data):
                    st.success(f"âœ… Consultant {prenom} {nom} ajoutÃ© avec succÃ¨s !")
                    st.balloons()
                    
                    # Nettoyer le cache pour rafraÃ®chir les donnÃ©es
                    clear_cache_and_refresh()
                    
                    # Afficher un aperÃ§u des donnÃ©es saisies
                    with st.expander("ðŸ‘ï¸ AperÃ§u des donnÃ©es ajoutÃ©es"):
                        st.json({
                            "prenom": prenom,
                            "nom": nom,
                            "email": email,
                            "telephone": telephone,
                            "salaire": salaire,
                            "disponible": disponible,
                            "notes": notes,
                            "date_creation": datetime.now().isoformat()
                        })
                    
                    # Redirection automatique vers la liste des consultants
                    st.info("âž¡ï¸ Redirection automatique vers la liste des consultants...")
                    
                    # Stocker le consultant ajoutÃ© pour le mettre en Ã©vidence
                    st.session_state.newly_added_consultant = f"{prenom} {nom}"
                    
                    # IncrÃ©menter le compteur pour forcer la rÃ©initialisation du formulaire
                    st.session_state.form_reset_counter = st.session_state.get('form_reset_counter', 0) + 1
                    
                    st.info("ðŸ”„ Consultant ajoutÃ© ! Allez voir la liste des consultants pour le retrouver.")
                    st.success("ðŸ“ Le formulaire est maintenant rÃ©initialisÃ© pour un nouvel ajout.")
                    
                    # RÃ©initialiser le formulaire en rechargeant la page
                    import time
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("âŒ Erreur lors de l'ajout du consultant. VÃ©rifiez la base de donnÃ©es.")
        
        if reset:
            st.rerun()
        
        if preview:
            st.info("ðŸ‘ï¸ AperÃ§u des donnÃ©es Ã  sauvegarder")
            preview_data = {
                "PrÃ©nom": prenom,
                "Nom": nom,
                "Email": email,
                "TÃ©lÃ©phone": telephone,
                "Salaire": f"{salaire}â‚¬",
                "Disponible": "Oui" if disponible else "Non",
                "Notes": notes or "Aucune"
            }
            st.table(preview_data)

def show_edit_consultant_form():
    """Affiche le formulaire de modification d'un consultant"""
    
    st.subheader("âœï¸ Modifier un consultant")
    
    # Debug: Afficher l'Ã©tat de la session
    if st.checkbox("ðŸ” Debug: Voir l'Ã©tat de la session", key="debug_session"):
        st.write("Session state:", dict(st.session_state))
    
    # VÃ©rifier si un consultant a Ã©tÃ© sÃ©lectionnÃ© depuis la liste
    if 'edit_consultant_id' in st.session_state:
        # RÃ©cupÃ©rer le consultant sÃ©lectionnÃ©
        try:
            consultant_id = st.session_state.edit_consultant_id
            st.success(f"ðŸŽ¯ **ID consultant dÃ©tectÃ©**: {consultant_id}")
            
            consultant = ConsultantService.get_consultant_by_id(consultant_id)
            if not consultant:
                st.error("âŒ Consultant introuvable")
                del st.session_state.edit_consultant_id
                return
                
            st.success(f"âœï¸ **Consultant sÃ©lectionnÃ© depuis la liste**: {consultant.prenom} {consultant.nom}")
            
        except Exception as e:
            st.error(f"âŒ Erreur lors du chargement: {e}")
            del st.session_state.edit_consultant_id
            return
    else:
        st.warning("âš ï¸ Aucun consultant prÃ©-sÃ©lectionnÃ©")
        # SÃ©lection manuelle du consultant
        consultants = ConsultantService.get_all_consultants()
        
        if not consultants:
            st.info("ðŸ“ Aucun consultant Ã  modifier. Ajoutez d'abord des consultants.")
            return
        
        # Options pour le selectbox
        consultant_options = {}
        for cons in consultants:
            key = f"{cons.prenom} {cons.nom} ({cons.email})"
            consultant_options[key] = cons
        
        selected_consultant_key = st.selectbox(
            "ðŸ‘¤ SÃ©lectionner le consultant Ã  modifier",
            options=list(consultant_options.keys()),
            index=0
        )
        
        consultant = consultant_options[selected_consultant_key]
        st.info("ðŸ’¡ **Conseil**: Vous pouvez aussi sÃ©lectionner un consultant dans la 'Liste des consultants' puis cliquer sur 'Modifier'")
    
    st.info(f"ðŸ“ Modification de: **{consultant.prenom} {consultant.nom}**")
    
    with st.form("edit_consultant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("PrÃ©nom *", value=consultant.prenom)
            email = st.text_input("Email *", value=consultant.email)
            salaire = st.number_input("Salaire annuel (â‚¬)", min_value=0, value=int(consultant.salaire_actuel or 0), step=1000)
        
        with col2:
            nom = st.text_input("Nom *", value=consultant.nom)
            telephone = st.text_input("TÃ©lÃ©phone", value=consultant.telephone or "")
            disponible = st.checkbox("Disponible", value=consultant.disponibilite)
        
        notes = st.text_area("Notes", value=consultant.notes or "")
        
        # Boutons du formulaire
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("âœ… Mettre Ã  jour", type="primary")
        
        with col2:
            cancel = st.form_submit_button("âŒ Annuler")
        
        with col3:
            preview = st.form_submit_button("ðŸ‘ï¸ AperÃ§u")
        
        if submitted:
            # Validation des champs obligatoires
            if not prenom or not nom or not email:
                st.error("âŒ Veuillez remplir tous les champs obligatoires (PrÃ©nom, Nom, Email)")
            else:
                # PrÃ©parer les donnÃ©es de mise Ã  jour
                update_data = {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire_actuel': salaire,
                    'disponibilite': disponible,
                    'notes': notes
                }
                
                # Mettre Ã  jour en base de donnÃ©es
                if ConsultantService.update_consultant(consultant.id, update_data):
                    st.success(f"âœ… Consultant {prenom} {nom} mis Ã  jour avec succÃ¨s !")
                    st.balloons()
                    
                    # Supprimer la sÃ©lection de la session
                    if 'edit_consultant_id' in st.session_state:
                        del st.session_state.edit_consultant_id
                    
                    st.info("âž¡ï¸ Retour automatique Ã  la liste des consultants...")
                    
                    # Forcer le rafraÃ®chissement et retourner Ã  la liste
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("âŒ Erreur lors de la mise Ã  jour du consultant.")
        
        if cancel:
            if 'edit_consultant_id' in st.session_state:
                del st.session_state.edit_consultant_id
            st.info("âŒ Modification annulÃ©e")
            st.rerun()
        
        if preview:
            st.info("ðŸ‘ï¸ AperÃ§u des modifications")
            changes = {}
            if prenom != consultant.prenom:
                changes["PrÃ©nom"] = f"{consultant.prenom} â†’ {prenom}"
            if nom != consultant.nom:
                changes["Nom"] = f"{consultant.nom} â†’ {nom}"
            if email != consultant.email:
                changes["Email"] = f"{consultant.email} â†’ {email}"
            if telephone != (consultant.telephone or ""):
                changes["TÃ©lÃ©phone"] = f"{consultant.telephone or 'Vide'} â†’ {telephone or 'Vide'}"
            if salaire != int(consultant.salaire_actuel or 0):
                changes["Salaire"] = f"{consultant.salaire_actuel or 0}â‚¬ â†’ {salaire}â‚¬"
            if disponible != consultant.disponibilite:
                changes["DisponibilitÃ©"] = f"{'Oui' if consultant.disponibilite else 'Non'} â†’ {'Oui' if disponible else 'Non'}"
            if notes != (consultant.notes or ""):
                changes["Notes"] = f"{'ModifiÃ©es' if notes != (consultant.notes or '') else 'InchangÃ©es'}"
            
            if changes:
                st.table(changes)
            else:
                st.info("Aucune modification dÃ©tectÃ©e")

def show_delete_consultant_form():
    """Affiche le formulaire de suppression d'un consultant"""
    
    st.subheader("ðŸ—‘ï¸ Supprimer un consultant")
    
    # VÃ©rifier si un consultant a Ã©tÃ© sÃ©lectionnÃ© depuis la liste
    if 'selected_consultant_id' in st.session_state and 'selected_consultant_name' in st.session_state:
        # RÃ©cupÃ©rer le consultant sÃ©lectionnÃ©
        try:
            consultant_id = st.session_state.selected_consultant_id
            consultant_name = st.session_state.selected_consultant_name
            
            consultant = ConsultantService.get_consultant_by_id(consultant_id)
            if not consultant:
                st.error("âŒ Consultant introuvable")
                del st.session_state.selected_consultant_id
                del st.session_state.selected_consultant_name
                return
                
            st.success(f"ðŸŽ¯ **Consultant sÃ©lectionnÃ© depuis la liste**: {consultant_name}")
            
            # Dialog de confirmation immÃ©diat - Workflow simplifiÃ©
            st.error(f"### âš ï¸ CONFIRMER LA SUPPRESSION")
            st.error(f"**Voulez-vous vraiment supprimer {consultant.prenom} {consultant.nom} ?**")
            
            # Informations rÃ©sumÃ©es du consultant
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"ðŸ“§ **Email**: {consultant.email}")
                st.write(f"ðŸ’° **Salaire**: {consultant.salaire_actuel or 0}â‚¬")
            with col2:
                st.write(f"ðŸ“ž **TÃ©lÃ©phone**: {consultant.telephone or 'Non renseignÃ©'}")
                st.write(f"âœ… **Disponible**: {'Oui' if consultant.disponibilite else 'Non'}")
            
            st.warning("âš ï¸ Cette action est **IRRÃ‰VERSIBLE** et supprimera toutes les donnÃ©es associÃ©es.")
            
            # Boutons de confirmation - Workflow direct
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("âœ… OUI, SUPPRIMER", type="primary", key="confirm_delete"):
                    try:
                        result = ConsultantService.delete_consultant(consultant_id)
                        
                        if result:
                            st.success(f"âœ… {consultant.prenom} {consultant.nom} a Ã©tÃ© supprimÃ© avec succÃ¨s !")
                            st.balloons()
                            
                            # Nettoyer tous les Ã©tats
                            keys_to_clean = ['selected_consultant_id', 'selected_consultant_name', 'edit_consultant_id']
                            for key in keys_to_clean:
                                if key in st.session_state:
                                    del st.session_state[key]
                            
                            # Nettoyer le cache et rafraÃ®chir
                            clear_cache_and_refresh()
                            
                            # Attendre un peu puis recharger
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("âŒ Erreur lors de la suppression du consultant.")
                    except Exception as e:
                        st.error(f"âŒ Erreur technique: {str(e)}")
            
            with col2:
                if st.button("âŒ NON, ANNULER", key="cancel_delete"):
                    # Nettoyer les sÃ©lections
                    if 'selected_consultant_id' in st.session_state:
                        del st.session_state.selected_consultant_id
                    if 'selected_consultant_name' in st.session_state:
                        del st.session_state.selected_consultant_name
                    st.info("âŒ Suppression annulÃ©e")
                    st.rerun()
            
        except Exception as e:
            st.error(f"âŒ Erreur lors du chargement: {e}")
            # Nettoyer les Ã©tats en cas d'erreur
            if 'selected_consultant_id' in st.session_state:
                del st.session_state.selected_consultant_id
            if 'selected_consultant_name' in st.session_state:
                del st.session_state.selected_consultant_name
            return
    
    else:
        # Aucun consultant sÃ©lectionnÃ©
        st.warning("âš ï¸ Aucun consultant sÃ©lectionnÃ©")
        
        st.info("""
        **Workflow de suppression simplifiÃ© :**
        
        1. ðŸ“‹ Allez dans l'onglet **'Liste des consultants'**
        2. ðŸ‘† **Cliquez sur une ligne** du tableau pour sÃ©lectionner un consultant
        3. ðŸ—‘ï¸ **Revenez dans cet onglet** â†’ Confirmation immÃ©diate
        4. âœ… **Cliquez sur "OUI, SUPPRIMER"** â†’ Suppression terminÃ©e !
        
        âž¡ï¸ SÃ©lectionnez d'abord un consultant dans la liste !
        """)
        
        st.markdown("---")
        
        # Afficher un aperÃ§u des consultants disponibles
        consultants = ConsultantService.get_all_consultants()
        
        if consultants:
            st.subheader("ðŸ“Š Consultants disponibles pour suppression")
            
            consultant_info = []
            for consultant in consultants:
                consultant_info.append({
                    "PrÃ©nom": consultant.prenom,
                    "Nom": consultant.nom,
                    "Email": consultant.email,
                    "Disponible": "âœ…" if consultant.disponibilite else "âŒ"
                })
            
            df_info = pd.DataFrame(consultant_info)
            st.dataframe(df_info, use_container_width=True, hide_index=True)
            
            st.info(f"ðŸ“ˆ **Total**: {len(consultants)} consultant(s) dans la base de donnÃ©es")
        else:
            st.warning("ðŸ“ Aucun consultant dans la base de donnÃ©es.")
        
        st.markdown("---")
        st.success("ðŸ’¡ **Conseil**: SÃ©lectionnez un consultant dans la 'Liste des consultants' puis revenez ici")
