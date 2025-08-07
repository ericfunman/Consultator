"""
Page de gestion des consultants
CRUD complet pour les consultants avec formulaires, tableaux et gestion de documents
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Import des modèles et services
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.consultant_service import ConsultantService
from services.document_analyzer import DocumentAnalyzer
from database.database import get_database_session
from database.models import Mission, ConsultantCompetence, Competence

def show():
    """Affiche la page de gestion des consultants"""
    
    st.title("👥 Gestion des consultants")
    st.markdown("### Gérez les profils de vos consultants")
    
    # Vérifier si on doit afficher le profil d'un consultant spécifique
    if 'view_consultant_profile' in st.session_state:
        show_consultant_profile()
        return
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs(["📋 Liste des consultants", "➕ Ajouter un consultant"])
    
    with tab1:
        show_consultants_list()
    
    with tab2:
        show_add_consultant_form()
    
    # Section CV Import
    st.markdown("---")
    st.subheader("📄 Import de CV et Documents")
    
    # Section de test de l'analyseur (pour debug)
    with st.expander("🧪 Tester l'analyseur de CV", expanded=False):
        st.info("💡 Testez l'algorithme d'analyse avec un texte d'exemple")
        
        if st.button("🚀 Lancer le test d'analyse", key="test_analyzer"):
            with st.spinner("🔄 Test de l'analyseur en cours..."):
                
                # Test avec texte d'exemple
                test_result = DocumentAnalyzer.test_analysis()
                
                st.success("✅ Test terminé !")
                
                # Afficher les résultats
                preview_text = DocumentAnalyzer.get_analysis_preview(test_result)
                st.markdown(preview_text)
        
        # Option pour tester avec un texte personnalisé
        custom_text = st.text_area(
            "📝 Ou testez avec votre propre texte CV :",
            height=150,
            placeholder="Collez ici un extrait de CV pour tester l'analyse..."
        )
        
        if custom_text and st.button("🔍 Analyser ce texte", key="test_custom"):
            with st.spinner("🔄 Analyse du texte personnalisé..."):
                
                custom_result = DocumentAnalyzer.analyze_cv_content(custom_text, "Test Personnalisé")
                
                st.success("✅ Analyse personnalisée terminée !")
                
                preview_text = DocumentAnalyzer.get_analysis_preview(custom_result)
                st.markdown(preview_text)
    
    st.markdown("---")
    
    show_cv_import()


def show_cv_import():
    """Affiche la section d'import de CV"""
    # Import CV simplifié directement ici
    consultants = ConsultantService.get_all_consultants()
    
    if consultants:
        # Sélection du consultant
        consultant_options = {}
        for consultant in consultants:
            key = f"{consultant.prenom} {consultant.nom} ({consultant.email})"
            consultant_options[key] = consultant
        
        selected_consultant_key = st.selectbox(
            "👤 Sélectionner le consultant",
            options=list(consultant_options.keys()),
            help="Choisissez le consultant auquel associer le CV"
        )
        
        selected_consultant = consultant_options[selected_consultant_key]
        st.info(f"📋 CV sera associé à: **{selected_consultant.prenom} {selected_consultant.nom}**")
        
        # Afficher le profil existant du consultant
        with st.expander(f"👤 Profil actuel de {selected_consultant.prenom} {selected_consultant.nom}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Informations générales")
                st.write(f"**Email:** {selected_consultant.email}")
                if selected_consultant.telephone:
                    st.write(f"**Téléphone:** {selected_consultant.telephone}")
                if selected_consultant.salaire_actuel:
                    st.write(f"**Salaire actuel:** {selected_consultant.salaire_actuel:,.0f} €")
                st.write(f"**Disponible:** {'✅ Oui' if selected_consultant.disponibilite else '❌ Non'}")
                
                # Afficher les missions existantes
                try:
                    
                    with get_database_session() as session:
                        missions = session.query(Mission).filter(Mission.consultant_id == selected_consultant.id).all()
                        
                        st.markdown("#### 🚀 Missions existantes")
                        if missions:
                            for mission in missions[-5:]:  # Dernières 5 missions
                                status_icon = "🟢" if mission.statut == "en_cours" else "🔵"
                                st.write(f"{status_icon} **{mission.client}** ({mission.date_debut} → {mission.date_fin or 'En cours'})")
                                if mission.technologies_utilisees:
                                    st.caption(f"Technologies: {mission.technologies_utilisees}")
                            
                            if len(missions) > 5:
                                st.caption(f"... et {len(missions) - 5} autres missions")
                        else:
                            st.write("Aucune mission enregistrée")
                except Exception as e:
                    st.error(f"Erreur lors du chargement des missions: {e}")
            
            with col2:
                try:
                    # Afficher les compétences existantes
                    with get_database_session() as session:
                        competences = session.query(ConsultantCompetence, Competence)\
                            .join(Competence)\
                            .filter(ConsultantCompetence.consultant_id == selected_consultant.id)\
                            .all()
                        
                        st.markdown("#### 💻 Compétences techniques")
                        tech_competences = [(cc, comp) for cc, comp in competences if comp.type_competence == 'technique']
                        if tech_competences:
                            for cc, comp in tech_competences[:10]:  # Top 10
                                niveau_icon = "🟢" if cc.niveau_maitrise == "expert" else ("🟡" if cc.niveau_maitrise == "intermediaire" else "🔴")
                                st.write(f"{niveau_icon} **{comp.nom}** ({cc.annees_experience:.1f} ans)")
                            
                            if len(tech_competences) > 10:
                                st.caption(f"... et {len(tech_competences) - 10} autres compétences techniques")
                        else:
                            st.write("Aucune compétence technique enregistrée")
                        
                        st.markdown("#### 🎯 Compétences fonctionnelles")
                        func_competences = [(cc, comp) for cc, comp in competences if comp.type_competence == 'fonctionnelle']
                        if func_competences:
                            for cc, comp in func_competences[:5]:  # Top 5
                                niveau_icon = "🟢" if cc.niveau_maitrise == "expert" else ("🟡" if cc.niveau_maitrise == "intermediaire" else "🔴")
                                st.write(f"{niveau_icon} **{comp.nom}** ({cc.annees_experience:.1f} ans)")
                            
                            if len(func_competences) > 5:
                                st.caption(f"... et {len(func_competences) - 5} autres compétences fonctionnelles")
                        else:
                            st.write("Aucune compétence fonctionnelle enregistrée")
                
                except Exception as e:
                    st.error(f"Erreur lors du chargement des compétences: {e}")
            
            st.info("💡 **Note**: L'analyse du CV ajoutera de nouvelles missions et compétences à ce profil existant. Les doublons seront automatiquement évités.")
        
        # Upload de fichier
        uploaded_file = st.file_uploader(
            "📎 Choisir un fichier CV",
            type=['pdf', 'docx', 'doc', 'pptx', 'ppt'],
            help="Formats supportés: PDF, Word (DOCX, DOC), PowerPoint (PPTX, PPT)"
        )
        
        if uploaded_file is not None:
            # Afficher les informations du fichier
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📄 Nom du fichier", uploaded_file.name)
            
            with col2:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.metric("💾 Taille", f"{file_size_mb:.2f} MB")
            
            with col3:
                st.metric("🔧 Type", uploaded_file.type or "Non détecté")
            
            # Bouton pour sauvegarder (basique)
            if st.button("💾 Sauvegarder le CV", type="primary", use_container_width=True):
                with st.spinner("🔄 Sauvegarde en cours..."):
                    # Créer le répertoire pour le consultant
                    consultant_dir = f"data/uploads/consultant_{selected_consultant.id}"
                    os.makedirs(consultant_dir, exist_ok=True)
                    
                    # Générer un nom de fichier unique
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_filename = f"{timestamp}_{uploaded_file.name}"
                    file_path = os.path.join(consultant_dir, safe_filename)
                    
                    # Sauvegarder le fichier
                    try:
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        st.success(f"✅ CV sauvegardé avec succès !")
                        st.success(f"📁 Fichier: {safe_filename}")
                        st.success(f"📍 Emplacement: {file_path}")
                        
                        # TODO: Ici on pourra ajouter l'analyse du contenu plus tard
                        st.info("🔍 Analyse du contenu - Fonctionnalité à venir")
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la sauvegarde: {e}")
            
            # Aperçu des documents existants
            consultant_dir = f"data/uploads/consultant_{selected_consultant.id}"
            if os.path.exists(consultant_dir):
                files = [f for f in os.listdir(consultant_dir) if os.path.isfile(os.path.join(consultant_dir, f))]
                
                if files:
                    st.markdown("### 📁 Documents existants")
                    for file in files:
                        file_path = os.path.join(consultant_dir, file)
                        file_size = os.path.getsize(file_path)
                        file_size_mb = file_size / (1024 * 1024)
                        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        # Conteneur pour chaque fichier
                        with st.container():
                            col1, col2, col3, col4, col5, col6 = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 0.7])
                            
                            with col1:
                                # Icône selon le type de fichier
                                if file.lower().endswith('.pdf'):
                                    icon = "📄"
                                elif file.lower().endswith(('.doc', '.docx')):
                                    icon = "📝"
                                elif file.lower().endswith(('.ppt', '.pptx')):
                                    icon = "📊"
                                else:
                                    icon = "�"
                                
                                st.write(f"{icon} **{file}**")
                                st.caption(f"📅 {file_modified.strftime('%d/%m/%Y %H:%M')} • 💾 {file_size_mb:.2f} MB")
                            
                            with col2:
                                # Bouton de téléchargement
                                try:
                                    with open(file_path, "rb") as f:
                                        file_bytes = f.read()
                                    
                                    st.download_button(
                                        label="📥",
                                        data=file_bytes,
                                        file_name=file,
                                        mime="application/octet-stream",
                                        key=f"download_{file}",
                                        help="Télécharger le fichier"
                                    )
                                except Exception as e:
                                    st.error(f"❌ Erreur lecture: {e}")
                            
                            with col3:
                                # Bouton de visualisation/aperçu
                                if st.button("👁️", key=f"view_{file}", help="Aperçu du fichier"):
                                    st.session_state[f"show_preview_{file}"] = True
                            
                            with col4:
                                # Bouton d'informations
                                if st.button("ℹ️", key=f"info_{file}", help="Informations détaillées"):
                                    st.session_state[f"show_info_{file}"] = True
                            
                            with col5:
                                # Bouton d'analyse de CV
                                if st.button("🔍", key=f"analyze_{file}", help="Analyser le CV"):
                                    # Déclencher l'analyse
                                    with st.spinner("🔄 Analyse du CV en cours..."):
                                        
                                        # Extraire le texte
                                        text = DocumentAnalyzer.extract_text_from_file(file_path)
                                        
                                        if text.strip():
                                            # Analyser le contenu
                                            analysis = DocumentAnalyzer.analyze_cv_content(
                                                text, 
                                                f"{selected_consultant.prenom} {selected_consultant.nom}"
                                            )
                                            
                                            # Sauvegarder l'analyse pour prévisualisation
                                            st.session_state[f"analysis_{file}"] = analysis
                                            st.session_state[f"show_analysis_{file}"] = True
                                            
                                            st.success("✅ Analyse terminée ! Vérifiez les résultats ci-dessous.")
                                            st.rerun()
                                        else:
                                            st.error("❌ Impossible d'extraire le texte du fichier")
                            
                            with col6:
                                # Bouton de suppression
                                if st.button("🗑️", key=f"del_{file}", help="Supprimer"):
                                    try:
                                        os.remove(file_path)
                                        st.success(f"✅ {file} supprimé")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Erreur: {e}")
                        
                        # Affichage conditionnel de l'aperçu
                        if st.session_state.get(f"show_preview_{file}", False):
                            with st.expander(f"👁️ Aperçu de {file}", expanded=True):
                                try:
                                    if file.lower().endswith('.pdf'):
                                        st.info("📄 Fichier PDF - Aperçu non disponible dans cette version")
                                        st.markdown(f"**Chemin complet:** `{file_path}`")
                                        
                                        # Option pour ouvrir avec l'application par défaut
                                        if st.button(f"🚀 Ouvrir avec l'application par défaut", key=f"open_{file}"):
                                            try:
                                                import subprocess
                                                import platform
                                                
                                                if platform.system() == 'Windows':
                                                    os.startfile(file_path)
                                                elif platform.system() == 'Darwin':  # macOS
                                                    subprocess.call(['open', file_path])
                                                else:  # Linux
                                                    subprocess.call(['xdg-open', file_path])
                                                
                                                st.success(f"🚀 Ouverture de {file}")
                                            except Exception as e:
                                                st.error(f"❌ Impossible d'ouvrir le fichier: {e}")
                                    
                                    elif file.lower().endswith(('.doc', '.docx')):
                                        st.info("📝 Fichier Word - Aperçu non disponible dans cette version")
                                        st.markdown(f"**Chemin complet:** `{file_path}`")
                                        
                                        # Option pour ouvrir avec l'application par défaut
                                        if st.button(f"🚀 Ouvrir avec Word", key=f"open_{file}"):
                                            try:
                                                os.startfile(file_path)
                                                st.success(f"🚀 Ouverture de {file}")
                                            except Exception as e:
                                                st.error(f"❌ Impossible d'ouvrir le fichier: {e}")
                                    
                                    elif file.lower().endswith(('.ppt', '.pptx')):
                                        st.info("📊 Fichier PowerPoint - Aperçu non disponible dans cette version")
                                        st.markdown(f"**Chemin complet:** `{file_path}`")
                                        
                                        # Option pour ouvrir avec l'application par défaut
                                        if st.button(f"🚀 Ouvrir avec PowerPoint", key=f"open_{file}"):
                                            try:
                                                os.startfile(file_path)
                                                st.success(f"🚀 Ouverture de {file}")
                                            except Exception as e:
                                                st.error(f"❌ Impossible d'ouvrir le fichier: {e}")
                                    
                                    else:
                                        st.warning("❓ Type de fichier non reconnu pour l'aperçu")
                                    
                                except Exception as e:
                                    st.error(f"❌ Erreur lors de l'aperçu: {e}")
                                
                                # Bouton pour fermer l'aperçu
                                if st.button("❌ Fermer l'aperçu", key=f"close_preview_{file}"):
                                    del st.session_state[f"show_preview_{file}"]
                                    st.rerun()
                        
                        # Affichage conditionnel des informations détaillées
                        if st.session_state.get(f"show_info_{file}", False):
                            with st.expander(f"ℹ️ Informations détaillées - {file}", expanded=True):
                                try:
                                    file_stat = os.stat(file_path)
                                    
                                    info_data = {
                                        "📄 Nom du fichier": file,
                                        "📁 Chemin complet": file_path,
                                        "💾 Taille": f"{file_size_mb:.2f} MB ({file_size:,} bytes)",
                                        "📅 Date de création": datetime.fromtimestamp(file_stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                                        "🔄 Dernière modification": file_modified.strftime("%d/%m/%Y %H:%M:%S"),
                                        "👤 Consultant associé": f"{selected_consultant.prenom} {selected_consultant.nom}",
                                        "🔧 Type MIME": "application/pdf" if file.lower().endswith('.pdf') else "application/octet-stream"
                                    }
                                    
                                    for key, value in info_data.items():
                                        st.write(f"**{key}:** {value}")
                                
                                except Exception as e:
                                    st.error(f"❌ Erreur lors de la récupération des informations: {e}")
                                
                                # Bouton pour fermer les informations
                                if st.button("❌ Fermer les informations", key=f"close_info_{file}"):
                                    del st.session_state[f"show_info_{file}"]
                                    st.rerun()
                        
                        # Affichage conditionnel de l'analyse de CV
                        if st.session_state.get(f"show_analysis_{file}", False):
                            analysis_data = st.session_state.get(f"analysis_{file}", {})
                            
                            with st.expander(f"🔍 Analyse du CV - {file}", expanded=True):
                                if analysis_data:
                                    # Afficher l'aperçu de l'analyse
                                    preview_text = DocumentAnalyzer.get_analysis_preview(analysis_data)
                                    st.markdown(preview_text)
                                    
                                    st.markdown("---")
                                    
                                    # Section de validation et modification
                                    st.subheader("✅ Validation et modification")
                                    st.info("🔧 Vous pouvez modifier les données détectées avant de les sauvegarder")
                                    
                                    # Formulaire d'édition des missions
                                    missions = analysis_data.get('missions', [])
                                    if missions:
                                        st.markdown("### 🚀 Missions détectées")
                                        
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
                                                        "Date début", 
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
                                                    "Résumé de mission", 
                                                    value=mission.get('resume', ''), 
                                                    key=f"edit_resume_{file}_{i}",
                                                    height=60
                                                )
                                                
                                                # Technologies de cette mission
                                                techs = st.text_input(
                                                    "Technologies (séparées par des virgules)", 
                                                    value=', '.join(mission.get('langages_techniques', [])), 
                                                    key=f"edit_techs_{file}_{i}"
                                                )
                                                
                                                # Sauvegarder la mission éditée
                                                edited_mission = {
                                                    'client': client,
                                                    'date_debut': date_debut,
                                                    'date_fin': date_fin,
                                                    'resume': resume,
                                                    'langages_techniques': [t.strip() for t in techs.split(',') if t.strip()]
                                                }
                                                edited_missions.append(edited_mission)
                                                
                                                st.divider()
                                    
                                    # Compétences techniques globales
                                    st.markdown("### 💻 Compétences techniques")
                                    current_techs = ', '.join(analysis_data.get('langages_techniques', []))
                                    edited_global_techs = st.text_area(
                                        "Technologies et langages (une par ligne ou séparées par des virgules)",
                                        value=current_techs,
                                        key=f"edit_global_techs_{file}",
                                        height=100
                                    )
                                    
                                    # Compétences fonctionnelles
                                    st.markdown("### 🎯 Compétences fonctionnelles")
                                    current_func = ', '.join(analysis_data.get('competences_fonctionnelles', []))
                                    edited_func_skills = st.text_area(
                                        "Compétences fonctionnelles (une par ligne ou séparées par des virgules)",
                                        value=current_func,
                                        key=f"edit_func_skills_{file}",
                                        height=100
                                    )
                                    
                                    st.markdown("---")
                                    
                                    # Boutons d'action
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        if st.button("💾 Sauvegarder dans le profil", key=f"save_analysis_{file}", type="primary"):
                                            # Préparer les données finales
                                            final_missions = [m for m in edited_missions if m['client'].strip()]
                                            
                                            # Parser les compétences techniques
                                            global_techs = []
                                            for tech in edited_global_techs.replace('\n', ',').split(','):
                                                tech = tech.strip()
                                                if tech:
                                                    global_techs.append(tech)
                                            
                                            # Parser les compétences fonctionnelles
                                            func_skills = []
                                            for skill in edited_func_skills.replace('\n', ',').split(','):
                                                skill = skill.strip()
                                                if skill:
                                                    func_skills.append(skill)
                                            
                                            # Préparer les données pour la sauvegarde
                                            final_analysis = {
                                                'missions': final_missions,
                                                'langages_techniques': global_techs,
                                                'competences_fonctionnelles': func_skills,
                                                'consultant': f"{selected_consultant.prenom} {selected_consultant.nom}"
                                            }
                                            
                                            # Sauvegarder en base de données
                                            try:
                                                success = ConsultantService.save_cv_analysis(selected_consultant.id, final_analysis)
                                                
                                                if success:
                                                    st.success(f"✅ Analyse sauvegardée avec succès dans le profil de {selected_consultant.prenom} {selected_consultant.nom} !")
                                                    st.balloons()
                                                    
                                                    # Afficher un résumé de ce qui a été sauvegardé
                                                    with st.expander("📋 Résumé des données sauvegardées", expanded=True):
                                                        st.write(f"**👤 Consultant:** {selected_consultant.prenom} {selected_consultant.nom}")
                                                        st.write(f"**🚀 Missions ajoutées:** {len(final_missions)}")
                                                        for mission in final_missions:
                                                            st.write(f"  • {mission['client']} ({mission['date_debut']} → {mission['date_fin']})")
                                                        st.write(f"**💻 Technologies ajoutées:** {len(global_techs)}")
                                                        if global_techs:
                                                            st.write(f"  {', '.join(global_techs[:10])}{'...' if len(global_techs) > 10 else ''}")
                                                        st.write(f"**🎯 Compétences fonctionnelles ajoutées:** {len(func_skills)}")
                                                        if func_skills:
                                                            st.write(f"  {', '.join(func_skills)}")
                                                        
                                                        st.info("💡 **Note:** Les compétences et missions en doublon ont été automatiquement ignorées.")
                                                        
                                                        # Proposer de voir le profil mis à jour
                                                        if st.button("👀 Voir le profil mis à jour", key=f"view_profile_{file}"):
                                                            st.session_state.view_consultant_id = selected_consultant.id
                                                            st.rerun()
                                                else:
                                                    st.error("❌ Erreur lors de la sauvegarde. Vérifiez les logs pour plus de détails.")
                                                    
                                            except Exception as e:
                                                st.error(f"❌ Erreur lors de la sauvegarde: {e}")
                                                st.exception(e)
                                            
                                            # Nettoyer les états de session après sauvegarde réussie
                                            if success:
                                                if f"analysis_{file}" in st.session_state:
                                                    del st.session_state[f"analysis_{file}"]
                                                if f"show_analysis_{file}" in st.session_state:
                                                    del st.session_state[f"show_analysis_{file}"]
                                    
                                    with col2:
                                        if st.button("🔄 Re-analyser", key=f"reanalyze_{file}"):
                                            # Relancer l'analyse
                                            with st.spinner("🔄 Nouvelle analyse en cours..."):
                                                
                                                text = DocumentAnalyzer.extract_text_from_file(file_path)
                                                if text.strip():
                                                    new_analysis = DocumentAnalyzer.analyze_cv_content(
                                                        text, 
                                                        f"{selected_consultant.prenom} {selected_consultant.nom}"
                                                    )
                                                    st.session_state[f"analysis_{file}"] = new_analysis
                                                    st.success("✅ Nouvelle analyse terminée !")
                                                    st.rerun()
                                    
                                    with col3:
                                        if st.button("❌ Fermer l'analyse", key=f"close_analysis_{file}"):
                                            # Nettoyer les états de session
                                            if f"analysis_{file}" in st.session_state:
                                                del st.session_state[f"analysis_{file}"]
                                            if f"show_analysis_{file}" in st.session_state:
                                                del st.session_state[f"show_analysis_{file}"]
                                            st.rerun()
                                else:
                                    st.error("❌ Aucune donnée d'analyse disponible")
                        
                        st.divider()
    else:
        st.warning("⚠️ Aucun consultant disponible. Ajoutez d'abord des consultants.")

# Copier toutes les autres fonctions depuis l'original
def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant"""
    
    consultant_id = st.session_state.view_consultant_profile
    consultant = ConsultantService.get_consultant_by_id(consultant_id)
    
    if not consultant:
        st.error("❌ Consultant introuvable")
        del st.session_state.view_consultant_profile
        st.rerun()
        return
    
    # En-tête avec bouton retour
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.title(f"👤 Profil de {consultant.prenom} {consultant.nom}")
    
    with col2:
        if st.button("← Retour", key="back_to_list"):
            del st.session_state.view_consultant_profile
            st.rerun()
    
    st.markdown("---")
    
    # Informations principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Salaire annuel", f"{consultant.salaire_actuel or 0:,}€", delta=None)
        
    with col2:
        status = "Disponible" if consultant.disponibilite else "En mission"
        st.metric("📊 Statut", status)
        
    with col3:
        creation_date = consultant.date_creation.strftime("%d/%m/%Y") if consultant.date_creation else "N/A"
        st.metric("📅 Membre depuis", creation_date)
    
    st.markdown("---")
    
    # Détails du profil
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Informations", "💼 Compétences", "🚀 Missions", "📄 Documents", "⚙️ Actions"])
    
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
    
    st.subheader("📋 Informations personnelles")
    
    # Formulaire toujours actif pour modification directe
    with st.form(f"edit_consultant_info_{consultant.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("👤 Prénom *", value=consultant.prenom, placeholder="Ex: Jean")
            email = st.text_input("📧 Email *", value=consultant.email, placeholder="jean.dupont@example.com")
            salaire = st.number_input("💰 Salaire annuel (€)", 
                                    min_value=0, 
                                    value=int(consultant.salaire_actuel or 0), 
                                    step=1000)
        
        with col2:
            nom = st.text_input("👤 Nom *", value=consultant.nom, placeholder="Ex: Dupont")
            telephone = st.text_input("📞 Téléphone", 
                                    value=consultant.telephone or "", 
                                    placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("✅ Disponible", value=consultant.disponibilite)
        
        # Notes
        notes = st.text_area("📝 Notes", 
                            value=consultant.notes or "",
                            height=100,
                            placeholder="Notes sur le consultant...")
        
        # Bouton de sauvegarde centré et visible
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col2:
            submitted = st.form_submit_button("💾 Sauvegarder les modifications", 
                                            use_container_width=True,
                                            type="primary")
        
        if submitted:
            # Validation
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Vérifier l'unicité de l'email (sauf pour le consultant actuel)
                existing_consultant = ConsultantService.get_consultant_by_email(email)
                if existing_consultant and existing_consultant.id != consultant.id:
                    st.error(f"❌ Un consultant avec l'email {email} existe déjà !")
                else:
                    try:
                        # Données de mise à jour
                        update_data = {
                            'prenom': prenom.strip(),
                            'nom': nom.strip(),
                            'email': email.strip().lower(),
                            'telephone': telephone.strip() if telephone else None,
                            'salaire_actuel': salaire,
                            'disponibilite': disponibilite,
                            'notes': notes.strip() if notes else None
                        }
                        
                        # Mettre à jour le consultant
                        ConsultantService.update_consultant(consultant.id, update_data)
                        
                        st.success(f"✅ {prenom} {nom} a été modifié avec succès !")
                        
                        # Actualiser la page de profil
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la modification: {e}")
    
    # Section de suppression
    st.markdown("---")
    st.subheader("🗑️ Zone de danger")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.warning("⚠️ **Attention**: La suppression du consultant est irréversible et effacera toutes ses données.")
    
    with col2:
        if st.button("🗑️ Supprimer le consultant", 
                    type="secondary", 
                    use_container_width=True,
                    key="delete_consultant_btn"):
            st.session_state.show_delete_confirmation = True
            st.rerun()
    
    # Boîte de dialogue de confirmation
    if st.session_state.get('show_delete_confirmation', False):
        with st.container():
            st.error("🚨 **Confirmation de suppression**")
            st.write(f"Voulez-vous vraiment supprimer **{consultant.prenom} {consultant.nom}** ?")
            st.write("Cette action supprimera définitivement :")
            st.write("• Toutes les informations personnelles")
            st.write("• Toutes les compétences associées")
            st.write("• Toutes les missions")
            st.write("• Tous les documents uploadés")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Oui, supprimer définitivement", 
                            type="primary", 
                            use_container_width=True,
                            key="confirm_delete"):
                    try:
                        # Supprimer le consultant
                        ConsultantService.delete_consultant(consultant.id)
                        
                        st.success(f"✅ {consultant.prenom} {consultant.nom} a été supprimé avec succès !")
                        
                        # Nettoyer les états de session
                        st.session_state.show_delete_confirmation = False
                        
                        # Retourner à la liste des consultants
                        del st.session_state.view_consultant_profile
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la suppression: {e}")
            
            with col2:
                if st.button("❌ Non, annuler", 
                            use_container_width=True,
                            key="cancel_delete"):
                    st.session_state.show_delete_confirmation = False
                    st.rerun()
    
    # Informations système (toujours en lecture seule)
    st.markdown("---")
    st.subheader("🔧 Informations système")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📅 Date de création**")
        creation_date = consultant.date_creation.strftime("%d/%m/%Y à %H:%M") if consultant.date_creation else "N/A"
        st.info(creation_date)
    
    with col2:
        st.write("**🔄 Dernière modification**")
        maj_date = consultant.derniere_maj.strftime("%d/%m/%Y à %H:%M") if consultant.derniere_maj else "N/A"
        st.info(maj_date)

def show_consultant_skills(consultant):
    """Affiche les compétences du consultant"""
    
    st.subheader("💼 Compétences")
    
    # TODO: Récupérer les vraies compétences depuis la base de données
    # Pour l'instant, simulation avec des données d'exemple
    
    skills_data = [
        {"Compétence": "Python", "Niveau": "Expert", "Années d'expérience": 5, "Dernière utilisation": "2024"},
        {"Compétence": "Machine Learning", "Niveau": "Avancé", "Années d'expérience": 3, "Dernière utilisation": "2024"},
        {"Compétence": "SQL", "Niveau": "Expert", "Années d'expérience": 4, "Dernière utilisation": "2024"},
        {"Compétence": "Docker", "Niveau": "Intermédiaire", "Années d'expérience": 2, "Dernière utilisation": "2023"},
    ]
    
    if skills_data:
        # Affichage des compétences sous forme de badges et tableau
        st.write("**🏷️ Badges de compétences**")
        
        cols = st.columns(4)
        for i, skill in enumerate(skills_data):
            with cols[i % 4]:
                level_color = {
                    "Expert": "🟢",
                    "Avancé": "🟡", 
                    "Intermédiaire": "🟠",
                    "Débutant": "🔴"
                }.get(skill["Niveau"], "⚪")
                
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; text-align: center;">
                    {level_color} <strong>{skill["Compétence"]}</strong><br>
                    <small>{skill["Niveau"]} • {skill["Années d'expérience"]} ans</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.write("**📊 Détail des compétences**")
        
        df_skills = pd.DataFrame(skills_data)
        st.dataframe(df_skills, use_container_width=True, hide_index=True)
        
        # Actions sur les compétences
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Ajouter une compétence"):
                st.info("🔧 Fonctionnalité à venir - Redirection vers gestion des compétences")
        
        with col2:
            if st.button("✏️ Modifier les compétences"):
                st.info("🔧 Fonctionnalité à venir - Édition des compétences")
        
        with col3:
            if st.button("📊 Analyse des compétences"):
                st.info("🔧 Fonctionnalité à venir - Analytics des compétences")
    
    else:
        st.info("📝 Aucune compétence enregistrée pour ce consultant")
        if st.button("➕ Ajouter des compétences"):
            st.info("🔧 Redirection vers la gestion des compétences...")

def show_consultant_missions(consultant):
    """Affiche l'historique des missions du consultant"""
    
    st.subheader("🚀 Historique des missions")
    
    # Récupérer les vraies missions depuis la base de données
    try:
        with get_database_session() as session:
            missions_db = session.query(Mission).filter(
                Mission.consultant_id == consultant.id
            ).order_by(Mission.date_debut.desc()).all()
            
        # Convertir en format d'affichage
        missions_data = []
        for mission in missions_db:
            missions_data.append({
                "Mission": mission.nom_mission,
                "Client": mission.client,
                "Role": mission.role or "Non spécifié",
                "Début": mission.date_debut.strftime("%Y-%m-%d") if mission.date_debut else "N/A",
                "Fin": mission.date_fin.strftime("%Y-%m-%d") if mission.date_fin else "En cours",
                "Statut": mission.statut.replace('_', ' ').title(),
                "Revenus": mission.revenus_generes or 0,
                "Technologies": mission.technologies_utilisees or "Non spécifiées",
                "Description": mission.description or "Aucune description"
            })
            
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des missions: {e}")
        missions_data = []
    
    if missions_data:
        # Métriques des missions
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenus = sum(m["Revenus"] for m in missions_data)
        missions_terminees = len([m for m in missions_data if m["Statut"] == "Terminee"])
        missions_en_cours = len([m for m in missions_data if m["Statut"] == "En Cours"])
        
        with col1:
            st.metric("💰 Revenus totaux", f"{total_revenus:,}€")
        
        with col2:
            st.metric("✅ Missions terminées", missions_terminees)
        
        with col3:
            st.metric("🔄 Missions en cours", missions_en_cours)
        
        with col4:
            st.metric("📊 Total missions", len(missions_data))
        
        st.markdown("---")
        
        # Liste détaillée des missions
        for i, mission in enumerate(missions_data):
            with st.expander(f"🚀 {mission['Client']} - {mission['Role']}", expanded=(i == 0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**🏢 Client**: {mission['Client']}")
                    st.write(f"**👤 Rôle**: {mission['Role']}")
                    st.write(f"**📅 Début**: {mission['Début']}")
                    st.write(f"**💰 Revenus**: {mission['Revenus']:,}€")
                
                with col2:
                    st.write(f"**📅 Fin**: {mission['Fin']}")
                    
                    # Statut avec couleur
                    if mission['Statut'] == 'Terminee':
                        st.success(f"✅ {mission['Statut']}")
                    elif mission['Statut'] == 'En Cours':
                        st.info(f"🔄 {mission['Statut']}")
                    else:
                        st.warning(f"⏸️ {mission['Statut']}")
                
                st.write(f"**🛠️ Technologies**: {mission['Technologies']}")
                
                # Description de la mission
                if mission['Description'] and mission['Description'] != "Aucune description":
                    st.write("**📝 Description**:")
                    st.text_area("", value=mission['Description'], height=100, key=f"desc_{i}", disabled=True)
        
        # Actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Ajouter une mission"):
                st.info("🔧 Fonctionnalité à venir - Redirection vers gestion des missions")
        
        with col2:
            if st.button("📊 Analyser les revenus"):
                st.info("🔧 Fonctionnalité à venir - Analytics des revenus")
        
        with col3:
            if st.button("📤 Exporter l'historique"):
                st.info("🔧 Fonctionnalité à venir - Export Excel/PDF")
    
    else:
        st.info("📝 Aucune mission enregistrée pour ce consultant")
        
        # Afficher un message encourageant à importer un CV
        st.markdown("""
        💡 **Astuce**: Pour ajouter automatiquement les missions d'un consultant:
        1. Utilisez la section "📄 Import de CV" en bas de la page
        2. Uploadez le CV du consultant 
        3. L'algorithme détectera automatiquement les missions, rôles et technologies
        """)
        
        if st.button("➕ Ajouter une mission"):
            st.info("🔧 Redirection vers la gestion des missions...")

def show_consultant_documents(consultant):
    """Affiche les documents associés au consultant"""
    
    st.subheader("📄 Documents")
    
    # Vérifier les documents uploadés 
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
    
    # Simulation de documents par défaut
    documents = [
        {"Type": "CV", "Nom": f"CV_{consultant.prenom}_{consultant.nom}_2024.pdf", "Taille": "245 KB", "Date": "2024-03-15", "Path": None},
        {"Type": "Contrat", "Nom": "Contrat_freelance_2024.pdf", "Taille": "156 KB", "Date": "2024-01-10", "Path": None},
        {"Type": "Certificat", "Nom": "Certification_AWS_Solutions_Architect.pdf", "Taille": "98 KB", "Date": "2023-11-20", "Path": None},
    ]
    
    # Combiner les vrais documents et les simulés
    all_docs = real_docs + documents
    
    if all_docs:
        for doc in all_docs:
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([3, 1.5, 1, 1, 1, 1])
                
                with col1:
                    icon = {"CV": "📄", "Contrat": "📋", "Certificat": "🏆", "Document": "📄"}.get(doc["Type"], "📄")
                    is_real = "🟢" if doc.get("Path") else "🔴"
                    st.write(f"{is_real} {icon} **{doc['Nom']}**")
                    st.caption(f"📂 {doc['Type']} • 💾 {doc['Taille']}")
                
                with col2:
                    st.write(f"� {doc['Date']}")
                
                with col3:
                    # Bouton de téléchargement pour les vrais fichiers
                    if doc.get("Path"):
                        try:
                            with open(doc["Path"], "rb") as f:
                                file_bytes = f.read()
                            
                            st.download_button(
                                label="📥",
                                data=file_bytes,
                                file_name=doc["Nom"],
                                mime="application/octet-stream",
                                key=f"download_profile_{doc['Nom']}",
                                help="Télécharger le fichier"
                            )
                        except Exception as e:
                            st.write("❌")
                    else:
                        if st.button("📥", key=f"download_sim_{doc['Nom']}", help="Document simulé"):
                            st.info(f"🔧 Document simulé - {doc['Nom']}")
                
                with col4:
                    # Bouton de visualisation pour les vrais fichiers
                    if doc.get("Path"):
                        if st.button("👁️", key=f"view_profile_{doc['Nom']}", help="Aperçu du fichier"):
                            st.session_state[f"show_profile_preview_{doc['Nom']}"] = True
                    else:
                        if st.button("👁️", key=f"view_sim_{doc['Nom']}", help="Aperçu simulé"):
                            st.info(f"� Aperçu simulé - {doc['Nom']}")
                
                with col5:
                    # Bouton d'informations
                    if doc.get("Path"):
                        if st.button("ℹ️", key=f"info_profile_{doc['Nom']}", help="Informations détaillées"):
                            st.session_state[f"show_profile_info_{doc['Nom']}"] = True
                    else:
                        if st.button("ℹ️", key=f"info_sim_{doc['Nom']}", help="Informations simulées"):
                            st.info(f"🔧 Informations simulées - {doc['Nom']}")
                
                with col6:
                    # Bouton de suppression
                    if doc.get("Path"):  # Fichier réel
                        if st.button("🗑️", key=f"delete_profile_{doc['Nom']}", help="Supprimer"):
                            try:
                                os.remove(doc["Path"])
                                st.success(f"✅ {doc['Nom']} supprimé")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                    else:  # Fichier simulé
                        if st.button("�️", key=f"delete_sim_{doc['Nom']}", help="Document simulé"):
                            st.info(f"🔧 Document simulé - {doc['Nom']}")
            
            # Affichage conditionnel de l'aperçu (fichiers réels seulement)
            if doc.get("Path") and st.session_state.get(f"show_profile_preview_{doc['Nom']}", False):
                with st.expander(f"👁️ Aperçu de {doc['Nom']}", expanded=True):
                    try:
                        file_path = doc["Path"]
                        file_name = doc["Nom"]
                        
                        if file_name.lower().endswith('.pdf'):
                            st.info("📄 Fichier PDF - Aperçu non disponible dans cette version")
                            st.markdown(f"**Chemin complet:** `{file_path}`")
                            
                            if st.button(f"🚀 Ouvrir avec l'application par défaut", key=f"open_profile_{file_name}"):
                                try:
                                    os.startfile(file_path)
                                    st.success(f"🚀 Ouverture de {file_name}")
                                except Exception as e:
                                    st.error(f"❌ Impossible d'ouvrir le fichier: {e}")
                        
                        elif file_name.lower().endswith(('.doc', '.docx')):
                            st.info("📝 Fichier Word - Aperçu non disponible dans cette version")
                            st.markdown(f"**Chemin complet:** `{file_path}`")
                            
                            if st.button(f"🚀 Ouvrir avec Word", key=f"open_profile_{file_name}"):
                                try:
                                    os.startfile(file_path)
                                    st.success(f"🚀 Ouverture de {file_name}")
                                except Exception as e:
                                    st.error(f"❌ Impossible d'ouvrir le fichier: {e}")
                        
                        elif file_name.lower().endswith(('.ppt', '.pptx')):
                            st.info("📊 Fichier PowerPoint - Aperçu non disponible dans cette version")
                            st.markdown(f"**Chemin complet:** `{file_path}`")
                            
                            if st.button(f"🚀 Ouvrir avec PowerPoint", key=f"open_profile_{file_name}"):
                                try:
                                    os.startfile(file_path)
                                    st.success(f"🚀 Ouverture de {file_name}")
                                except Exception as e:
                                    st.error(f"❌ Impossible d'ouvrir le fichier: {e}")
                        
                        else:
                            st.warning("❓ Type de fichier non reconnu pour l'aperçu")
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'aperçu: {e}")
                    
                    if st.button("❌ Fermer l'aperçu", key=f"close_profile_preview_{doc['Nom']}"):
                        del st.session_state[f"show_profile_preview_{doc['Nom']}"]
                        st.rerun()
            
            # Affichage conditionnel des informations détaillées (fichiers réels seulement)
            if doc.get("Path") and st.session_state.get(f"show_profile_info_{doc['Nom']}", False):
                with st.expander(f"ℹ️ Informations détaillées - {doc['Nom']}", expanded=True):
                    try:
                        file_path = doc["Path"]
                        file_stat = os.stat(file_path)
                        file_size_bytes = os.path.getsize(file_path)
                        
                        info_data = {
                            "📄 Nom du fichier": doc["Nom"],
                            "📁 Chemin complet": file_path,
                            "💾 Taille": f"{file_size_bytes / (1024 * 1024):.2f} MB ({file_size_bytes:,} bytes)",
                            "� Date de création": datetime.fromtimestamp(file_stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                            "🔄 Dernière modification": datetime.fromtimestamp(file_stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
                            "👤 Consultant associé": f"{consultant.prenom} {consultant.nom}",
                            "🔧 Type MIME": "application/pdf" if doc["Nom"].lower().endswith('.pdf') else "application/octet-stream"
                        }
                        
                        for key, value in info_data.items():
                            st.write(f"**{key}:** {value}")
                    
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la récupération des informations: {e}")
                    
                    if st.button("❌ Fermer les informations", key=f"close_profile_info_{doc['Nom']}"):
                        del st.session_state[f"show_profile_info_{doc['Nom']}"]
                        st.rerun()
            
            st.divider()
        
        # Actions sur les documents
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📎 Utilisez la section 'Import CV' ci-dessous pour ajouter de vrais documents")
        
        with col2:
            if st.button("🗂️ Organiser les documents"):
                st.info("🔧 Fonctionnalité à venir - Gestion documentaire")
        
        with col3:
            if st.button("📤 Envoyer par email"):
                st.info("🔧 Fonctionnalité à venir - Partage de documents")
    
    else:
        st.info("📝 Aucun document associé à ce consultant")
        st.info("💡 Utilisez la section 'Import CV' pour ajouter des documents")

def show_consultant_actions(consultant):
    """Affiche les actions possibles sur le consultant"""
    
    st.subheader("⚙️ Actions")
    
    # Utiliser des sous-onglets pour organiser les actions
    action_tab1, action_tab2 = st.tabs(["🗑️ Supprimer", "📊 Analytics"])
    
    with action_tab1:
        st.markdown("### 🗑️ Supprimer le consultant")
        st.info("💡 **Info**: Vous pouvez modifier les informations directement dans l'onglet 'Informations'")
        show_delete_consultant_inline(consultant)
    
    with action_tab2:
        st.markdown("### 📊 Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 Rapport de performance", key="performance_report", use_container_width=True):
                st.info("🔧 Fonctionnalité à venir - Rapport détaillé")
            
            if st.button("💰 Analyse des revenus", key="revenue_analysis", use_container_width=True):
                st.info("🔧 Fonctionnalité à venir - Analytics revenus")
        
        with col2:
            if st.button("🎯 Recommandations IA", key="ai_recommendations", use_container_width=True):
                st.info("🔧 Fonctionnalité à venir - IA recommendations")
            
            if st.button("📋 Dupliquer ce profil", key="duplicate_profile", use_container_width=True):
                st.info("🔧 Fonctionnalité à venir - Duplication de profil")


def show_edit_consultant_inline(consultant):
    """Formulaire de modification intégré dans le profil"""
    
    # Formulaire de modification
    with st.form(f"edit_consultant_inline_{consultant.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("Prénom *", value=consultant.prenom, placeholder="Ex: Jean")
            email = st.text_input("Email *", value=consultant.email, placeholder="jean.dupont@example.com")
            salaire = st.number_input("Salaire annuel (€)", 
                                    min_value=0, 
                                    value=int(consultant.salaire_actuel or 0), 
                                    step=1000)
        
        with col2:
            nom = st.text_input("Nom *", value=consultant.nom, placeholder="Ex: Dupont")
            telephone = st.text_input("Téléphone", 
                                    value=consultant.telephone or "", 
                                    placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("Disponible", value=consultant.disponibilite)
        
        # Boutons de soumission
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submitted = st.form_submit_button("✅ Sauvegarder", use_container_width=True)
        
        with col2:
            cancelled = st.form_submit_button("❌ Annuler", use_container_width=True)
        
        if submitted:
            # Validation
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
                return
            
            # Vérifier l'unicité de l'email (sauf pour le consultant actuel)
            existing_consultant = ConsultantService.get_consultant_by_email(email)
            if existing_consultant and existing_consultant.id != consultant.id:
                st.error(f"❌ Un consultant avec l'email {email} existe déjà !")
                return
            
            try:
                # Données de mise à jour
                update_data = {
                    'prenom': prenom.strip(),
                    'nom': nom.strip(),
                    'email': email.strip().lower(),
                    'telephone': telephone.strip() if telephone else None,
                    'salaire_actuel': salaire,
                    'disponibilite': disponibilite
                }
                
                # Mettre à jour le consultant
                ConsultantService.update_consultant(consultant.id, update_data)
                
                st.success(f"✅ {prenom} {nom} a été modifié avec succès !")
                
                # Actualiser la page de profil
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la modification: {e}")
        
        if cancelled:
            st.info("❌ Modification annulée")


def show_delete_consultant_inline(consultant):
    """Interface de suppression intégrée dans le profil"""
    
    st.warning("⚠️ **Attention**: Cette action est irréversible et supprimera définitivement toutes les données du consultant.")
    
    # Afficher les informations à supprimer
    with st.expander("📋 Données qui seront supprimées", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**👤 Informations personnelles**")
            st.write(f"• Nom: {consultant.nom}")
            st.write(f"• Prénom: {consultant.prenom}")
            st.write(f"• Email: {consultant.email}")
            st.write(f"• Téléphone: {consultant.telephone or 'N/A'}")
        
        with col2:
            st.write("**💼 Données professionnelles**")
            st.write(f"• Salaire: {consultant.salaire_actuel or 0:,}€")
            st.write(f"• Statut: {'Disponible' if consultant.disponibilite else 'En mission'}")
            
            # Récupérer les statistiques de manière sécurisée
            consultant_stats = ConsultantService.get_consultant_with_stats(consultant.id)
            if consultant_stats:
                competences_count = consultant_stats['competences_count']
                missions_count = consultant_stats['missions_count']
            else:
                competences_count = 0
                missions_count = 0
            st.write(f"• Compétences: {competences_count}")
            st.write(f"• Missions: {missions_count}")
    
    # Confirmation de suppression
    st.markdown("---")
    st.markdown("### � Confirmation de suppression")
    
    # Demander la confirmation textuelle
    confirmation_text = st.text_input(
        f"**Pour confirmer la suppression, tapez:** `{consultant.prenom} {consultant.nom}`",
        placeholder=f"Tapez: {consultant.prenom} {consultant.nom}"
    )
    
    # Vérifier la confirmation
    expected_text = f"{consultant.prenom} {consultant.nom}"
    is_confirmed = confirmation_text.strip() == expected_text
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("�️ SUPPRIMER DÉFINITIVEMENT", 
                    disabled=not is_confirmed,
                    use_container_width=True,
                    key="delete_confirmed"):
            if is_confirmed:
                try:
                    ConsultantService.delete_consultant(consultant.id)
                    st.success(f"✅ {consultant.prenom} {consultant.nom} a été supprimé avec succès !")
                    
                    # Retourner à la liste
                    del st.session_state.view_consultant_profile
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de la suppression: {e}")
    
    with col2:
        if st.button("❌ Annuler", use_container_width=True, key="delete_cancel"):
            st.info("❌ Suppression annulée")
    
    st.markdown("---")
    
    # Actions avancées
    st.markdown("### 🚀 Actions avancées")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Exporter le profil complet", use_container_width=True):
            st.info("🔧 Export PDF - Fonctionnalité à venir")
    
    with col2:
        if st.button("✉️ Envoyer par email", use_container_width=True):
            st.info("🔧 Email integration - Fonctionnalité à venir")
    
    with col3:
        if st.button("🔗 Partager le profil", use_container_width=True):
            st.info("🔧 Partage sécurisé - Fonctionnalité à venir")

def clear_cache_and_refresh(keep_edit_id=False):
    """Nettoie le cache et force le rafraîchissement des données"""
    # Nettoyer le cache Streamlit
    st.cache_data.clear()
    
    # Nettoyer les états de session liés aux sélections
    keys_to_clear = [
        'selected_consultant_id', 
        'selected_consultant_name', 
        'show_delete_dialog'
    ]
    
    # Ajouter edit_consultant_id à la liste seulement si on ne veut pas le garder
    if not keep_edit_id:
        keys_to_clear.append('edit_consultant_id')
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def show_consultants_list():
    """Affiche la liste des consultants avec options de filtrage"""
    
    st.subheader("📋 Liste des consultants")
    
    # Vérifier si un consultant vient d'être ajouté
    if 'newly_added_consultant' in st.session_state:
        consultant_name = st.session_state.newly_added_consultant
        st.success(f"🎉 **Nouveau consultant ajouté** : {consultant_name}")
        del st.session_state.newly_added_consultant
    
    # Filtres et bouton de rafraîchissement
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        search_name = st.text_input("🔍 Rechercher par nom", placeholder="Nom ou prénom...")
    
    with col2:
        filter_availability = st.selectbox(
            "📊 Disponibilité",
            ["Tous", "Disponible", "En mission"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "📈 Trier par",
            ["Nom", "Date d'ajout", "Dernière mise à jour"]
        )
    
    with col4:
        st.write("")  # Espacement
        if st.button("🔄", help="Actualiser la liste", key="refresh_consultants"):
            clear_cache_and_refresh(keep_edit_id=True)
            st.rerun()
    
    # Récupérer les consultants depuis la base de données
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
                    "Prénom": consultant.prenom,
                    "Email": consultant.email,
                    "Téléphone": consultant.telephone or "-",
                    "Salaire": consultant.salaire_actuel or 0,
                    "Disponibilité": "✅ Disponible" if consultant.disponibilite else "🔴 En mission",
                    "Dernière MAJ": consultant.derniere_maj.strftime("%Y-%m-%d") if consultant.derniere_maj else "-"
                })
            
            df = pd.DataFrame(consultants_data)
            
            # Appliquer le filtre de disponibilité
            if filter_availability != "Tous":
                status = "✅ Disponible" if filter_availability == "Disponible" else "🔴 En mission"
                df = df[df['Disponibilité'] == status]
            
            # Afficher le tableau avec sélection
            if not df.empty:
                st.markdown("### 👥 Consultants - Cliquez sur une ligne pour voir le profil détaillé")
                
                event = st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Nom": st.column_config.TextColumn(
                            "Nom",
                            help="Cliquez sur la ligne pour voir le profil détaillé"
                        ),
                        "Prénom": st.column_config.TextColumn(
                            "Prénom", 
                            help="Cliquez sur la ligne pour voir le profil détaillé"
                        ),
                        "Salaire": st.column_config.NumberColumn(
                            "Salaire (€)",
                            format="€%d"
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
                
                # Vérifier si une ligne est sélectionnée
                if event.selection.rows:
                    selected_row_index = event.selection.rows[0]
                    selected_consultant = df.iloc[selected_row_index]
                    
                    # Stocker les données du consultant sélectionné
                    st.session_state.selected_consultant_id = int(selected_consultant['ID'])
                    st.session_state.selected_consultant_name = f"{selected_consultant['Prénom']} {selected_consultant['Nom']}"
                    
                    # NOUVEAU : Définir automatiquement l'ID pour la modification
                    st.session_state.edit_consultant_id = int(selected_consultant['ID'])
                    
                    # Afficher automatiquement le profil détaillé
                    st.session_state.view_consultant_profile = int(selected_consultant['ID'])
                    st.rerun()
                else:
                    st.info("👆 Cliquez sur une ligne du tableau pour sélectionner un consultant")
                

                
                # Actions en lot
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Bouton de téléchargement CSV direct
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="� Télécharger CSV",
                        data=csv,
                        file_name=f"consultants_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("📊 Générer rapport"):
                        st.info("📊 Génération de rapport - Fonctionnalité à venir !")
                
                with col3:
                    if st.button("✉️ Email groupé"):
                        st.info("✉️ Email groupé - Fonctionnalité à venir !")
            
            else:
                st.info("Aucun consultant ne correspond aux critères de recherche.")
        
        else:
            st.info("📝 Aucun consultant enregistré. Utilisez l'onglet 'Ajouter un consultant' pour commencer !")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des consultants: {e}")
        st.info("🔧 Vérifiez que la base de données est initialisée.")

def show_add_consultant_form():
    """Affiche le formulaire d'ajout de consultant"""
    
    st.subheader("➕ Ajouter un nouveau consultant")
    
    # Générer une clé unique pour le formulaire pour forcer la réinitialisation
    form_key = f"add_consultant_form_{st.session_state.get('form_reset_counter', 0)}"
    
    with st.form(form_key):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("Prénom *", placeholder="Ex: Jean")
            email = st.text_input("Email *", placeholder="jean.dupont@example.com")
            salaire = st.number_input("Salaire annuel (€)", min_value=0, value=45000, step=1000)
        
        with col2:
            nom = st.text_input("Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input("Téléphone", placeholder="01.23.45.67.89")
            disponible = st.checkbox("Disponible", value=True)
        
        notes = st.text_area("Notes", placeholder="Informations complémentaires...")
        
        # Boutons du formulaire
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("✅ Ajouter le consultant", type="primary")
        
        with col2:
            reset = st.form_submit_button("🔄 Réinitialiser")
        
        with col3:
            preview = st.form_submit_button("👁️ Aperçu")
        
        if submitted:
            # Validation des champs obligatoires
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (Prénom, Nom, Email)")
            else:
                # Préparer les données
                consultant_data = {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire': salaire,
                    'disponible': disponible,
                    'notes': notes
                }
                
                # Sauvegarder en base de données
                if ConsultantService.create_consultant(consultant_data):
                    st.success(f"✅ Consultant {prenom} {nom} ajouté avec succès !")
                    st.balloons()
                    
                    # Nettoyer le cache pour rafraîchir les données
                    clear_cache_and_refresh()
                    
                    # Afficher un aperçu des données saisies
                    with st.expander("👁️ Aperçu des données ajoutées"):
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
                    st.info("➡️ Redirection automatique vers la liste des consultants...")
                    
                    # Stocker le consultant ajouté pour le mettre en évidence
                    st.session_state.newly_added_consultant = f"{prenom} {nom}"
                    
                    # Incrémenter le compteur pour forcer la réinitialisation du formulaire
                    st.session_state.form_reset_counter = st.session_state.get('form_reset_counter', 0) + 1
                    
                    st.info("🔄 Consultant ajouté ! Allez voir la liste des consultants pour le retrouver.")
                    st.success("📝 Le formulaire est maintenant réinitialisé pour un nouvel ajout.")
                    
                    # Réinitialiser le formulaire en rechargeant la page
                    import time
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'ajout du consultant. Vérifiez la base de données.")
        
        if reset:
            st.rerun()
        
        if preview:
            st.info("👁️ Aperçu des données à sauvegarder")
            preview_data = {
                "Prénom": prenom,
                "Nom": nom,
                "Email": email,
                "Téléphone": telephone,
                "Salaire": f"{salaire}€",
                "Disponible": "Oui" if disponible else "Non",
                "Notes": notes or "Aucune"
            }
            st.table(preview_data)

def show_edit_consultant_form():
    """Affiche le formulaire de modification d'un consultant"""
    
    st.subheader("✏️ Modifier un consultant")
    
    # Debug: Afficher l'état de la session
    if st.checkbox("🔍 Debug: Voir l'état de la session", key="debug_session"):
        st.write("Session state:", dict(st.session_state))
    
    # Vérifier si un consultant a été sélectionné depuis la liste
    if 'edit_consultant_id' in st.session_state:
        # Récupérer le consultant sélectionné
        try:
            consultant_id = st.session_state.edit_consultant_id
            st.success(f"🎯 **ID consultant détecté**: {consultant_id}")
            
            consultant = ConsultantService.get_consultant_by_id(consultant_id)
            if not consultant:
                st.error("❌ Consultant introuvable")
                del st.session_state.edit_consultant_id
                return
                
            st.success(f"✏️ **Consultant sélectionné depuis la liste**: {consultant.prenom} {consultant.nom}")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {e}")
            del st.session_state.edit_consultant_id
            return
    else:
        st.warning("⚠️ Aucun consultant pré-sélectionné")
        # Sélection manuelle du consultant
        consultants = ConsultantService.get_all_consultants()
        
        if not consultants:
            st.info("📝 Aucun consultant à modifier. Ajoutez d'abord des consultants.")
            return
        
        # Options pour le selectbox
        consultant_options = {}
        for cons in consultants:
            key = f"{cons.prenom} {cons.nom} ({cons.email})"
            consultant_options[key] = cons
        
        selected_consultant_key = st.selectbox(
            "👤 Sélectionner le consultant à modifier",
            options=list(consultant_options.keys()),
            index=0
        )
        
        consultant = consultant_options[selected_consultant_key]
        st.info("💡 **Conseil**: Vous pouvez aussi sélectionner un consultant dans la 'Liste des consultants' puis cliquer sur 'Modifier'")
    
    st.info(f"📝 Modification de: **{consultant.prenom} {consultant.nom}**")
    
    with st.form("edit_consultant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("Prénom *", value=consultant.prenom)
            email = st.text_input("Email *", value=consultant.email)
            salaire = st.number_input("Salaire annuel (€)", min_value=0, value=int(consultant.salaire_actuel or 0), step=1000)
        
        with col2:
            nom = st.text_input("Nom *", value=consultant.nom)
            telephone = st.text_input("Téléphone", value=consultant.telephone or "")
            disponible = st.checkbox("Disponible", value=consultant.disponibilite)
        
        notes = st.text_area("Notes", value=consultant.notes or "")
        
        # Boutons du formulaire
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("✅ Mettre à jour", type="primary")
        
        with col2:
            cancel = st.form_submit_button("❌ Annuler")
        
        with col3:
            preview = st.form_submit_button("👁️ Aperçu")
        
        if submitted:
            # Validation des champs obligatoires
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (Prénom, Nom, Email)")
            else:
                # Préparer les données de mise à jour
                update_data = {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire_actuel': salaire,
                    'disponibilite': disponible,
                    'notes': notes
                }
                
                # Mettre à jour en base de données
                if ConsultantService.update_consultant(consultant.id, update_data):
                    st.success(f"✅ Consultant {prenom} {nom} mis à jour avec succès !")
                    st.balloons()
                    
                    # Supprimer la sélection de la session
                    if 'edit_consultant_id' in st.session_state:
                        del st.session_state.edit_consultant_id
                    
                    st.info("➡️ Retour automatique à la liste des consultants...")
                    
                    # Forcer le rafraîchissement et retourner à la liste
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la mise à jour du consultant.")
        
        if cancel:
            if 'edit_consultant_id' in st.session_state:
                del st.session_state.edit_consultant_id
            st.info("❌ Modification annulée")
            st.rerun()
        
        if preview:
            st.info("👁️ Aperçu des modifications")
            changes = {}
            if prenom != consultant.prenom:
                changes["Prénom"] = f"{consultant.prenom} → {prenom}"
            if nom != consultant.nom:
                changes["Nom"] = f"{consultant.nom} → {nom}"
            if email != consultant.email:
                changes["Email"] = f"{consultant.email} → {email}"
            if telephone != (consultant.telephone or ""):
                changes["Téléphone"] = f"{consultant.telephone or 'Vide'} → {telephone or 'Vide'}"
            if salaire != int(consultant.salaire_actuel or 0):
                changes["Salaire"] = f"{consultant.salaire_actuel or 0}€ → {salaire}€"
            if disponible != consultant.disponibilite:
                changes["Disponibilité"] = f"{'Oui' if consultant.disponibilite else 'Non'} → {'Oui' if disponible else 'Non'}"
            if notes != (consultant.notes or ""):
                changes["Notes"] = f"{'Modifiées' if notes != (consultant.notes or '') else 'Inchangées'}"
            
            if changes:
                st.table(changes)
            else:
                st.info("Aucune modification détectée")

def show_delete_consultant_form():
    """Affiche le formulaire de suppression d'un consultant"""
    
    st.subheader("🗑️ Supprimer un consultant")
    
    # Vérifier si un consultant a été sélectionné depuis la liste
    if 'selected_consultant_id' in st.session_state and 'selected_consultant_name' in st.session_state:
        # Récupérer le consultant sélectionné
        try:
            consultant_id = st.session_state.selected_consultant_id
            consultant_name = st.session_state.selected_consultant_name
            
            consultant = ConsultantService.get_consultant_by_id(consultant_id)
            if not consultant:
                st.error("❌ Consultant introuvable")
                del st.session_state.selected_consultant_id
                del st.session_state.selected_consultant_name
                return
                
            st.success(f"🎯 **Consultant sélectionné depuis la liste**: {consultant_name}")
            
            # Dialog de confirmation immédiat - Workflow simplifié
            st.error(f"### ⚠️ CONFIRMER LA SUPPRESSION")
            st.error(f"**Voulez-vous vraiment supprimer {consultant.prenom} {consultant.nom} ?**")
            
            # Informations résumées du consultant
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📧 **Email**: {consultant.email}")
                st.write(f"💰 **Salaire**: {consultant.salaire_actuel or 0}€")
            with col2:
                st.write(f"📞 **Téléphone**: {consultant.telephone or 'Non renseigné'}")
                st.write(f"✅ **Disponible**: {'Oui' if consultant.disponibilite else 'Non'}")
            
            st.warning("⚠️ Cette action est **IRRÉVERSIBLE** et supprimera toutes les données associées.")
            
            # Boutons de confirmation - Workflow direct
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("✅ OUI, SUPPRIMER", type="primary", key="confirm_delete"):
                    try:
                        result = ConsultantService.delete_consultant(consultant_id)
                        
                        if result:
                            st.success(f"✅ {consultant.prenom} {consultant.nom} a été supprimé avec succès !")
                            st.balloons()
                            
                            # Nettoyer tous les états
                            keys_to_clean = ['selected_consultant_id', 'selected_consultant_name', 'edit_consultant_id']
                            for key in keys_to_clean:
                                if key in st.session_state:
                                    del st.session_state[key]
                            
                            # Nettoyer le cache et rafraîchir
                            clear_cache_and_refresh()
                            
                            # Attendre un peu puis recharger
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression du consultant.")
                    except Exception as e:
                        st.error(f"❌ Erreur technique: {str(e)}")
            
            with col2:
                if st.button("❌ NON, ANNULER", key="cancel_delete"):
                    # Nettoyer les sélections
                    if 'selected_consultant_id' in st.session_state:
                        del st.session_state.selected_consultant_id
                    if 'selected_consultant_name' in st.session_state:
                        del st.session_state.selected_consultant_name
                    st.info("❌ Suppression annulée")
                    st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {e}")
            # Nettoyer les états en cas d'erreur
            if 'selected_consultant_id' in st.session_state:
                del st.session_state.selected_consultant_id
            if 'selected_consultant_name' in st.session_state:
                del st.session_state.selected_consultant_name
            return
    
    else:
        # Aucun consultant sélectionné
        st.warning("⚠️ Aucun consultant sélectionné")
        
        st.info("""
        **Workflow de suppression simplifié :**
        
        1. 📋 Allez dans l'onglet **'Liste des consultants'**
        2. 👆 **Cliquez sur une ligne** du tableau pour sélectionner un consultant
        3. 🗑️ **Revenez dans cet onglet** → Confirmation immédiate
        4. ✅ **Cliquez sur "OUI, SUPPRIMER"** → Suppression terminée !
        
        ➡️ Sélectionnez d'abord un consultant dans la liste !
        """)
        
        st.markdown("---")
        
        # Afficher un aperçu des consultants disponibles
        consultants = ConsultantService.get_all_consultants()
        
        if consultants:
            st.subheader("📊 Consultants disponibles pour suppression")
            
            consultant_info = []
            for consultant in consultants:
                consultant_info.append({
                    "Prénom": consultant.prenom,
                    "Nom": consultant.nom,
                    "Email": consultant.email,
                    "Disponible": "✅" if consultant.disponibilite else "❌"
                })
            
            df_info = pd.DataFrame(consultant_info)
            st.dataframe(df_info, use_container_width=True, hide_index=True)
            
            st.info(f"📈 **Total**: {len(consultants)} consultant(s) dans la base de données")
        else:
            st.warning("📝 Aucun consultant dans la base de données.")
        
        st.markdown("---")
        st.success("💡 **Conseil**: Sélectionnez un consultant dans la 'Liste des consultants' puis revenez ici")
