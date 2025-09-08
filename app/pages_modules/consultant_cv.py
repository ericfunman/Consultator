"""
Module d'analyse CV pour les consultants
Fonctions pour analyser et afficher les résultats d'analyse de CV
"""

import os
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import streamlit as st

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Imports des modèles
from database.models import Client

# Variables pour les imports
ConsultantService = None
get_database_session = None
Consultant = None
imports_ok = False

try:
    from database.database import get_database_session
    from database.models import Client
    from database.models import Competence
    from database.models import Consultant
    from database.models import ConsultantCompetence
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError as e:
    # Imports échoués, on continue quand même
    pass


def show_cv_missions(missions: List[Dict], consultant):
    """Affiche les missions extraites du CV"""

    if not missions:
        st.info("ℹ️ Aucune mission détectée dans le CV")
        return

    st.markdown("#### 🚀 Missions extraites du CV")

    for i, mission in enumerate(missions, 1):
        with st.expander(f"📋 Mission {i}: {mission.get('titre', 'Sans titre')}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Client :** {mission.get('client', 'N/A')}")
                st.write(f"**Période :** {mission.get('periode', 'N/A')}")

            with col2:
                st.write(f"**Technologies :** {mission.get('technologies', 'N/A')}")

            if mission.get('description'):
                st.markdown("**Description :**")
                st.write(mission['description'])

            # Actions sur la mission
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(
                    "➕ Créer mission",
                    key=f"create_mission_{i}_{
                        consultant.id}"):
                    create_mission_from_cv(mission, consultant)

            with col2:
                if st.button("🔍 Analyser", key=f"analyze_mission_{i}_{consultant.id}"):
                    analyze_mission_details(mission)

            with col3:
                if st.button("📋 Copier", key=f"copy_mission_{i}_{consultant.id}"):
                    copy_mission_to_clipboard(mission)


def show_cv_skills(analysis: Dict):
    """Affiche les compétences extraites du CV"""

    if not analysis or "competences" not in analysis:
        st.info("ℹ️ Aucune compétence détectée dans le CV")
        return

    competences = analysis["competences"]
    if not competences:
        st.info("ℹ️ Aucune compétence détectée dans le CV")
        return

    st.markdown("#### 🛠️ Compétences extraites du CV")

    # Organiser par catégorie
    skills_by_category = {}
    for skill in competences:
        # Essayer de déterminer la catégorie
        category = categorize_skill(skill)
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)

    for category, skills in skills_by_category.items():
        st.markdown(f"**{category}**")
        cols = st.columns(min(len(skills), 4))

        for i, skill in enumerate(skills):
            with cols[i % len(cols)]:
                # Vérifier si la compétence existe déjà pour le consultant
                existing = check_existing_skill(
                    skill, st.session_state.get('view_consultant_profile'))
                status = "✅ Existe" if existing else "➕ Nouveau"

                if st.button(
                    f"{skill} ({status})",
                    key=f"skill_{category}_{i}_{
                        st.session_state.get(
                            'view_consultant_profile',
                            0)}"):
                    if not existing:
                        add_skill_from_cv(
                            skill, st.session_state.get('view_consultant_profile'))
                    else:
                        st.info(f"📋 La compétence '{skill}' existe déjà")

    # Statistiques des compétences
    show_cv_skills_statistics(competences)


def show_cv_summary(analysis: Dict, consultant):
    """Affiche le résumé de l'analyse CV"""

    if not analysis:
        st.info("ℹ️ Analyse non disponible")
        return

    st.markdown("#### 📋 Résumé de l'analyse")

    col1, col2, col3 = st.columns(3)

    with col1:
        missions_count = len(analysis.get("missions", []))
        st.metric("Missions détectées", missions_count)

    with col2:
        skills_count = len(analysis.get("competences", []))
        st.metric("Compétences détectées", skills_count)

    with col3:
        # Calcul d'un score de qualité
        quality_score = calculate_cv_quality_score(analysis)
        st.metric("Score qualité CV", f"{quality_score}/100")

    # Résumé textuel
    if "resume" in analysis and analysis["resume"]:
        st.markdown("**Résumé général :**")
        st.write(analysis["resume"])

    # Informations de contact
    if "contact" in analysis and analysis["contact"]:
        st.markdown("**Informations de contact :**")
        contact = analysis["contact"]
        if contact.get('email'):
            st.write(f"📧 Email : {contact['email']}")
        if contact.get('telephone'):
            st.write(f"📞 Téléphone : {contact['telephone']}")
        if contact.get('linkedin'):
            st.write(f"💼 LinkedIn : {contact['linkedin']}")

    # Recommandations
    show_cv_recommendations(analysis, consultant)


def show_cv_actions(analysis: Dict, consultant):
    """Affiche les actions possibles sur l'analyse CV"""

    st.markdown("#### 🎯 Actions sur l'analyse")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Sauvegarder tout", key=f"save_all_{consultant.id}"):
            save_cv_analysis_to_profile(analysis, consultant)

    with col2:
        if st.button("📊 Générer rapport", key=f"generate_report_{consultant.id}"):
            generate_cv_analysis_report(analysis, consultant)

    with col3:
        if st.button("🔄 Réanalyser", key=f"reanalyze_{consultant.id}"):
            st.session_state.reanalyze_cv = consultant.id
            st.rerun()

    # Actions avancées
    st.markdown("**Actions avancées :**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 Comparer avec profil", key=f"compare_profile_{consultant.id}"):
            compare_cv_with_profile(analysis, consultant)

    with col2:
        if st.button("📈 Suggestions d'évolution", key=f"suggestions_{consultant.id}"):
            show_career_suggestions(analysis, consultant)


def categorize_skill(skill: str) -> str:
    """Catégorise une compétence"""

    skill_lower = skill.lower()

    # Technologies
    tech_keywords = [
        'python',
        'java',
        'javascript',
        'react',
        'angular',
        'vue',
        'node',
        'django',
        'flask',
        'spring',
        'hibernate',
        'sql',
        'mysql',
        'postgresql',
        'mongodb',
        'docker',
        'kubernetes',
        'aws',
        'azure',
        'git',
        'linux',
        'windows']

    # Méthodologies
    method_keywords = [
        'agile',
        'scrum',
        'kanban',
        'devops',
        'ci/cd',
        'tdd',
        'bdd',
        'uml']

    # Soft skills
    soft_keywords = [
        'management',
        'leadership',
        'communication',
        'présentation',
        'anglais',
        'français']

    for keyword in tech_keywords:
        if keyword in skill_lower:
            return "🛠️ Technologies"

    for keyword in method_keywords:
        if keyword in skill_lower:
            return "📋 Méthodologies"

    for keyword in soft_keywords:
        if keyword in skill_lower:
            return "🤝 Soft Skills"

    return "📚 Autres"


def check_existing_skill(skill_name: str, consultant_id: Optional[int]) -> bool:
    """Vérifie si une compétence existe déjà pour le consultant"""

    if not consultant_id or not imports_ok:
        return False

    try:
        with get_database_session() as session:
            existing = session.query(ConsultantCompetence)\
                .join(Competence)\
                .filter(
                    ConsultantCompetence.consultant_id == consultant_id,
                    Competence.nom.ilike(f"%{skill_name}%")
            )\
                .first()

            return existing is not None

    except Exception:
        return False


def add_skill_from_cv(skill_name: str, consultant_id: Optional[int]):
    """Ajoute une compétence extraite du CV"""

    if not consultant_id or not imports_ok:
        st.error("❌ Impossible d'ajouter la compétence")
        return

    try:
        with get_database_session() as session:
            # Chercher ou créer la compétence
            competence = session.query(Competence)\
                .filter(Competence.nom.ilike(skill_name))\
                .first()

            if not competence:
                # Créer une nouvelle compétence
                competence = Competence(
                    nom=skill_name,
                    categorie=categorize_skill(skill_name).replace(
                        "🛠️ ",
                        "").replace(
                        "📋 ",
                        "").replace(
                        "🤝 ",
                        "").replace(
                        "📚 ",
                        ""),
                    description=f"Compétence extraite du CV")
                session.add(competence)
                session.flush()

            # Vérifier si l'association existe déjà
            existing_assoc = session.query(ConsultantCompetence)\
                .filter(
                    ConsultantCompetence.consultant_id == consultant_id,
                    ConsultantCompetence.competence_id == competence.id
            )\
                .first()

            if existing_assoc:
                st.info(f"📋 La compétence '{skill_name}' existe déjà")
                return

            # Créer l'association
            from datetime import datetime
            consultant_competence = ConsultantCompetence(
                consultant_id=consultant_id,
                competence_id=competence.id,
                niveau=3,  # Niveau par défaut
                annees_experience=2,  # Expérience par défaut
                date_acquisition=datetime.now()
            )

            session.add(consultant_competence)
            session.commit()

            st.success(f"✅ Compétence '{skill_name}' ajoutée avec succès !")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout de la compétence: {e}")


def show_cv_skills_statistics(competences: List[str]):
    """Affiche les statistiques des compétences extraites"""

    if not competences:
        return

    st.markdown("**Statistiques des compétences :**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total compétences", len(competences))

    with col2:
        # Compétences par catégorie
        categories = {}
        for skill in competences:
            category = categorize_skill(skill)
            categories[category] = categories.get(category, 0) + 1

        main_category = max(
            categories.items(),
            key=lambda x: x[1]) if categories else (
            "N/A",
            0)
        st.metric("Catégorie principale", main_category[0])

    with col3:
        # Score de diversité
        diversity_score = len(categories) * 10 if categories else 0
        st.metric("Score diversité", f"{diversity_score}/50")


def calculate_cv_quality_score(analysis: Dict) -> int:
    """Calcule un score de qualité du CV"""

    score = 0

    # Missions (30 points max)
    missions = analysis.get("missions", [])
    if missions:
        score += min(len(missions) * 5, 30)

    # Compétences (30 points max)
    competences = analysis.get("competences", [])
    if competences:
        score += min(len(competences) * 2, 30)

    # Informations de contact (20 points max)
    contact = analysis.get("contact", {})
    if contact.get('email'):
        score += 10
    if contact.get('telephone'):
        score += 5
    if contact.get('linkedin'):
        score += 5

    # Résumé (20 points max)
    if analysis.get("resume"):
        score += 20

    return min(score, 100)


def show_cv_recommendations(analysis: Dict, consultant=None):
    """Affiche les recommandations basées sur l'analyse CV"""

    st.markdown("**💡 Recommandations :**")

    recommendations = []

    # Vérifier les missions
    missions = analysis.get("missions", [])
    if len(missions) < 3:
        recommendations.append(
            "⚠️ Ajouter plus de missions dans le CV pour montrer l'expérience")

    # Vérifier les compétences
    competences = analysis.get("competences", [])
    if len(competences) < 5:
        recommendations.append("⚠️ Ajouter plus de compétences techniques")

    # Vérifier les informations de contact
    contact = analysis.get("contact", {})
    if not contact.get('email'):
        recommendations.append("⚠️ Ajouter une adresse email professionnelle")

    if not contact.get('linkedin'):
        recommendations.append("💼 Créer un profil LinkedIn si inexistant")

    # Vérifier la diversité des compétences
    if competences:
        categories = {}
        for skill in competences:
            category = categorize_skill(skill)
            categories[category] = categories.get(category, 0) + 1

        if len(categories) < 2:
            recommendations.append(
                "📚 Diversifier les compétences (techniques, méthodologiques, soft skills)")

    # Afficher les recommandations
    if recommendations:
        for rec in recommendations:
            st.write(f"• {rec}")
    else:
        st.success("✅ Le CV semble complet et bien structuré !")


def create_mission_from_cv(mission_data: Dict, consultant):
    """Crée une mission à partir des données extraites du CV"""

    st.markdown("### ➕ Créer une mission depuis le CV")

    try:
        with st.form(f"create_mission_cv_{consultant.id}", clear_on_submit=True):
            # Pré-remplir avec les données extraites
            titre = st.text_input(
                "Titre de la mission *",
                value=mission_data.get('titre', ''),
                help="Titre de la mission"
            )

            client_name = st.text_input(
                "Nom du client",
                value=mission_data.get('client', ''),
                help="Nom du client"
            )

            # Essayer de trouver le client dans la base
            client_options = ["Nouveau client"]
            if imports_ok:
                with get_database_session() as session:
                    clients = session.query(Client).all()
                    client_options.extend([c.nom for c in clients])

            selected_client = st.selectbox(
                "Client existant ou nouveau",
                options=client_options,
                help="Sélectionnez un client existant ou créez-en un nouveau"
            )

            col1, col2 = st.columns(2)

            with col1:
                date_debut = st.date_input(
                    "Date de début",
                    value=None,
                    help="Date de début de la mission"
                )

            with col2:
                date_fin = st.date_input(
                    "Date de fin",
                    value=None,
                    help="Date de fin de la mission (laisser vide si en cours)"
                )

            taux_journalier = st.number_input(
                "Taux journalier (€)",
                min_value=0,
                step=10,
                help="Taux journalier de la mission"
            )

            description = st.text_area(
                "Description",
                value=mission_data.get('description', ''),
                height=100,
                help="Description détaillée de la mission"
            )

            submitted = st.form_submit_button("💾 Créer la mission", type="primary")

            if submitted:
                if not titre:
                    st.error("❌ Le titre est obligatoire")
                else:
                    success = save_mission_from_cv({
                        'titre': titre,
                        'client_name': client_name,
                        'selected_client': selected_client,
                        'date_debut': date_debut,
                        'date_fin': date_fin,
                        'taux_journalier': taux_journalier,
                        'description': description,
                        'technologies': mission_data.get('technologies', '')
                    }, consultant.id)

                    if success:
                        st.success("✅ Mission créée avec succès !")
                    else:
                        st.error("❌ Erreur lors de la création de la mission")

    except Exception as e:
        st.error(f"❌ Erreur lors de la création du formulaire: {e}")


def save_mission_from_cv(data: Dict, consultant_id: int) -> bool:
    """Sauvegarde une mission créée depuis le CV"""

    try:
        with get_database_session() as session:
            # Gérer le client
            client_id = None
            if data['selected_client'] != "Nouveau client":
                # Chercher le client existant
                client = session.query(Client)\
                    .filter(Client.nom == data['selected_client'])\
                    .first()
                if client:
                    client_id = client.id
            else:
                # Créer un nouveau client
                if data['client_name']:
                    from database.models import Client
                    new_client = Client(
                        nom=data['client_name'],
                        secteur="Non spécifié"
                    )
                    session.add(new_client)
                    session.flush()
                    client_id = new_client.id

            # Créer la mission
            from datetime import datetime

            from database.models import Mission

            mission = Mission(
                consultant_id=consultant_id,
                titre=data['titre'],
                client_id=client_id,
                date_debut=data['date_debut'],
                date_fin=data['date_fin'],
                en_cours=not bool(
                    data['date_fin']),
                taux_journalier=data['taux_journalier'] if data['taux_journalier'] > 0 else None,
                description=data['description'],
                competences_requises=data['technologies'])

            session.add(mission)
            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")
        return False


def analyze_mission_details(mission_data: Dict):
    """Analyse les détails d'une mission extraite"""

    st.markdown("### 🔍 Analyse de la mission")

    # Analyser la durée estimée
    periode = mission_data.get('periode', '')
    if periode:
        st.write(f"**Période détectée :** {periode}")

        # Essayer d'extraire les dates
        try:
            # Analyse simple de la période
            if 'à' in periode.lower() or '-' in periode:
                st.info("ℹ️ Mission avec période définie détectée")
            elif 'présent' in periode.lower() or 'actuellement' in periode.lower():
                st.info("ℹ️ Mission en cours détectée")
        except Exception as e:
            st.warning(f"⚠️ Erreur lors de l'extraction des dates: {e}")

    # Analyser les technologies
    technologies = mission_data.get('technologies', '')
    if technologies:
        st.write(f"**Technologies :** {technologies}")

        # Compter les technologies
        tech_list = [t.strip() for t in technologies.split(',') if t.strip()]
        st.write(f"**Nombre de technologies :** {len(tech_list)}")

    # Analyser la description
    description = mission_data.get('description', '')
    if description:
        word_count = len(description.split())
        st.write(f"**Longueur description :** {word_count} mots")

        # Détecter des mots-clés
        keywords = [
            'responsable',
            'développement',
            'conception',
            'maintenance',
            'migration']
        found_keywords = [kw for kw in keywords if kw in description.lower()]
        if found_keywords:
            st.write(f"**Mots-clés détectés :** {', '.join(found_keywords)}")


def copy_mission_to_clipboard(mission_data: Dict):
    """Copie les informations de la mission dans le presse-papiers virtuel"""

    mission_text = f"""
Titre: {mission_data.get('titre', 'N/A')}
Client: {mission_data.get('client', 'N/A')}
Période: {mission_data.get('periode', 'N/A')}
Technologies: {mission_data.get('technologies', 'N/A')}
Description: {mission_data.get('description', 'N/A')}
"""

    st.text_area(
        "Informations de la mission (copiez-collez)",
        value=mission_text.strip(),
        height=150,
        key="mission_clipboard"
    )

    st.info("ℹ️ Copiez le contenu ci-dessus pour l'utiliser ailleurs")


def save_cv_analysis_to_profile(analysis: Dict, consultant):
    """Sauvegarde l'analyse CV dans le profil du consultant"""

    try:
        # Cette fonction pourrait mettre à jour le profil avec les informations
        # extraites
        st.success("✅ Analyse sauvegardée dans le profil (fonctionnalité à implémenter)")

        # TODO: Implémenter la sauvegarde effective des données extraites

    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")


def generate_cv_analysis_report(analysis: Dict, consultant):
    """Génère un rapport d'analyse du CV"""

    try:
        from datetime import datetime

        report = f"""# Rapport d'analyse CV
**Consultant :** {consultant.prenom} {consultant.nom}
**Date :** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Score qualité
{calculate_cv_quality_score(analysis)}/100

## Résumé
{analysis.get('resume', 'Non disponible')}

## Missions détectées
{len(analysis.get('missions', []))} mission(s)

## Compétences détectées
{len(analysis.get('competences', []))} compétence(s)

## Recommandations
"""

        # Ajouter les recommandations
        recommendations = []

        missions = analysis.get("missions", [])
        if len(missions) < 3:
            recommendations.append("- Ajouter plus de missions dans le CV")

        competences = analysis.get("competences", [])
        if len(competences) < 5:
            recommendations.append("- Ajouter plus de compétences techniques")

        contact = analysis.get("contact", {})
        if not contact.get('email'):
            recommendations.append("- Ajouter une adresse email professionnelle")

        if not contact.get('linkedin'):
            recommendations.append("- Créer un profil LinkedIn")

        if not recommendations:
            recommendations.append("- Le CV semble complet et bien structuré")

        for rec in recommendations:
            report += f"{rec}\n"

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger le rapport",
            data=report,
            file_name=f"analyse_cv_{
                consultant.prenom}_{
                consultant.nom}_{
                datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            key="download_analysis_report")

        st.success("✅ Rapport généré avec succès !")

    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du rapport: {e}")


def compare_cv_with_profile(analysis: Dict, consultant):
    """Compare l'analyse CV avec le profil existant"""

    st.markdown("### 🔄 Comparaison CV / Profil")

    try:
        if not imports_ok:
            st.error("❌ Services non disponibles pour la comparaison")
            return

        with get_database_session() as session:
            # Récupérer les compétences du profil
            profile_skills = session.query(Competence)\
                .join(ConsultantCompetence)\
                .filter(ConsultantCompetence.consultant_id == consultant.id)\
                .all()

            profile_skill_names = [skill.nom.lower() for skill in profile_skills]

            # Compétences du CV
            cv_skills = [skill.lower() for skill in analysis.get('competences', [])]

            # Comparaison
            common_skills = set(profile_skill_names) & set(cv_skills)
            only_in_cv = set(cv_skills) - set(profile_skill_names)
            only_in_profile = set(profile_skill_names) - set(cv_skills)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Compétences communes", len(common_skills))

            with col2:
                st.metric("Nouvelles dans CV", len(only_in_cv))

            with col3:
                st.metric("Manquantes dans CV", len(only_in_profile))

            # Détails
            if common_skills:
                st.markdown("**✅ Compétences communes :**")
                for skill in sorted(common_skills):
                    st.write(f"• {skill}")

            if only_in_cv:
                st.markdown("**➕ Nouvelles compétences dans le CV :**")
                for skill in sorted(only_in_cv):
                    st.write(f"• {skill}")

            if only_in_profile:
                st.markdown("**⚠️ Compétences dans le profil mais pas dans le CV :**")
                for skill in sorted(only_in_profile):
                    st.write(f"• {skill}")

    except Exception as e:
        st.error(f"❌ Erreur lors de la comparaison: {e}")


def show_career_suggestions(analysis: Dict, consultant):
    """Affiche des suggestions d'évolution de carrière"""

    st.markdown("### 📈 Suggestions d'évolution")

    try:
        # Analyser les compétences
        competences = analysis.get('competences', [])
        missions = analysis.get('missions', [])

        suggestions = []

        # Suggestions basées sur les compétences
        if competences:
            # Détecter le domaine principal
            tech_count = sum(
                1 for skill in competences if categorize_skill(skill) == "🛠️ Technologies")
            method_count = sum(
                1 for skill in competences if categorize_skill(skill) == "📋 Méthodologies")

            if tech_count > method_count:
                suggestions.append(
                    "💡 Focus sur les aspects techniques - considérer une certification architecte")
            elif method_count > tech_count:
                suggestions.append(
                    "💡 Orientation management - formation en leadership d'équipe")

            # Détecter des lacunes
            has_cloud = any('aws' in skill.lower() or 'azure' in skill.lower()
                            for skill in competences)
            has_devops = any('docker' in skill.lower()
                             or 'kubernetes' in skill.lower() for skill in competences)

            if not has_cloud:
                suggestions.append(
                    "☁️ Acquérir des compétences cloud (AWS, Azure, GCP)")

            if not has_devops:
                suggestions.append("🔄 Se former aux pratiques DevOps et CI/CD")

        # Suggestions basées sur l'expérience
        if missions:
            avg_mission_length = len(missions)
            if avg_mission_length < 3:
                suggestions.append(
                    "📈 Accumuler plus d'expérience sur différents projets")

        # Suggestions générales
        suggestions.extend([
            "🎓 Poursuivre une formation continue",
            "🌍 Améliorer les compétences linguistiques",
            "🤝 Développer les soft skills (communication, leadership)"
        ])

        # Afficher les suggestions
        for suggestion in suggestions:
            st.write(f"• {suggestion}")

        st.info(
            "💡 Ces suggestions sont basées sur l'analyse de votre CV et peuvent être adaptées à vos objectifs")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse des suggestions: {e}")
