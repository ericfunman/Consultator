"""
Module de gestion des documents du consultant
Fonctions pour afficher, uploader et analyser les documents
"""

import json
import os
import sys
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
import streamlit as st

# Constantes pour éviter la duplication
ERROR_DOCUMENT_NOT_FOUND = "❌ Document introuvable"

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Variables pour les imports
ConsultantService = None
get_database_session = None
Consultant = None
imports_ok = False

try:
    from database.database import get_database_session
    from database.models import Consultant
    from database.models import Document
    from services.ai_openai_service import OpenAIChatGPTService
    from services.ai_openai_service import get_grok_service
    from services.ai_openai_service import is_grok_available
    from services.consultant_service import ConsultantService
    from services.document_analyzer import DocumentAnalyzer

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


def show_consultant_documents(consultant):
    """Affiche les documents du consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    if not consultant:
        st.error("❌ Consultant non fourni")
        return

    st.markdown("### 📁 Documents")

    try:
        # Récupérer les documents du consultant
        with get_database_session() as session:
            documents = (
                session.query(Document)
                .filter(Document.consultant_id == consultant.id)
                .order_by(Document.date_upload.desc())
                .all()
            )

        # Statistiques des documents
        show_documents_statistics(documents)

        # Liste des documents
        if documents:
            st.markdown("#### 📋 Documents disponibles")

            for doc in documents:
                with st.expander(f"📄 {doc.nom_fichier} - {doc.type_document}"):
                    show_document_details(doc, consultant)
        else:
            st.info("ℹ️ Aucun document trouvé pour ce consultant")

        # Actions générales
        st.markdown("#### 🎯 Actions générales")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📤 Uploader un document", key=f"upload_doc_{consultant.id}"):
                st.session_state.upload_document = consultant.id
                st.rerun()

        with col2:
            if st.button("🔍 Analyser CV", key=f"analyze_cv_{consultant.id}"):
                analyze_consultant_cv(consultant)

        with col3:
            if st.button("📊 Rapport documents", key=f"doc_report_{consultant.id}"):
                show_documents_report(documents)

        # Formulaire d'upload (si activé)
        if (
            "upload_document" in st.session_state
            and st.session_state.upload_document == consultant.id
        ):
            show_upload_document_form(consultant.id)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des documents: {e}")
        st.code(str(e))


def show_document_details(document, consultant):
    """Affiche les détails d'un document"""

    col1, col2 = st.columns(2)

    with col1:
        _display_document_basic_info(document)

    with col2:
        _display_document_metadata(document)

    # Contenu de l'analyse CV si disponible
    _display_cv_analysis_summary(document, consultant)

    # Actions sur le document
    _display_document_actions(document, consultant)

    # Formulaire de renommage (si activé)
    _handle_rename_form(document)


def show_documents_statistics(documents):
    """Affiche les statistiques des documents"""

    if not documents:
        return

    st.markdown("#### 📊 Statistiques")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_docs = len(documents)
        st.metric("Total documents", total_docs)

    with col2:
        # Types de documents
        types = {}
        for doc in documents:
            doc_type = doc.type_document or "Autre"
            types[doc_type] = types.get(doc_type, 0) + 1

        most_common_type = (
            max(types.items(), key=lambda x: x[1]) if types else ("N/A", 0)
        )
        st.metric("Type principal", most_common_type[0])

    with col3:
        # Documents avec analyse CV
        analyzed_docs = sum(1 for doc in documents if doc.analyse_cv)
        st.metric("Analysés CV", analyzed_docs)

    with col4:
        # Taille totale
        total_size = sum(doc.taille_fichier or 0 for doc in documents)
        total_size_mb = total_size / (1024 * 1024)
        st.metric("Taille totale", f"{total_size_mb:.1f} MB")


def show_upload_document_form(consultant_id: int):
    """Affiche le formulaire d'upload de document"""

    st.markdown("### 📤 Uploader un document")

    with st.form(f"upload_document_form_{consultant_id}", clear_on_submit=True):
        st.markdown("#### 📄 Informations du document")

        # Types de documents disponibles
        document_types = [
            "CV",
            "Lettre de motivation",
            "Diplôme",
            "Certification",
            "Contrat",
            "Évaluation",
            "Autre",
        ]

        type_document = st.selectbox(
            "Type de document *",
            options=document_types,
            help="Sélectionnez le type de document",
        )

        description = st.text_area(
            "Description", height=80, help="Description optionnelle du document"
        )

        st.markdown("#### 📎 Fichier à uploader")

        uploaded_file = st.file_uploader(
            "Sélectionnez un fichier",
            type=["pdf", "doc", "docx", "txt", "rtf"],
            help="Formats acceptés: PDF, DOC, DOCX, TXT, RTF",
        )

        # Boutons
        col1, col2, _ = st.columns([1, 1, 2])

        with col1:
            submitted = st.form_submit_button("📤 Uploader", type="primary")

        with col2:
            cancel = st.form_submit_button("❌ Annuler")

        if submitted:
            if not uploaded_file:
                st.error("❌ Veuillez sélectionner un fichier")
            else:
                success = upload_document(
                    consultant_id,
                    {
                        "file": uploaded_file,
                        "type_document": type_document,
                        "description": description,
                    },
                )

                if success:
                    st.success("✅ Document uploadé avec succès !")
                    if "upload_document" in st.session_state:
                        del st.session_state.upload_document
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'upload du document")

        if cancel:
            if "upload_document" in st.session_state:
                del st.session_state.upload_document
            st.rerun()


def perform_cv_analysis(cv_document, consultant, method: str) -> bool:
    """Effectue l'analyse du CV selon la méthode choisie"""

    try:
        # Extraire le texte du document
        if not os.path.exists(cv_document.chemin_fichier):
            st.error("❌ Fichier CV introuvable")
            return False

        extracted_text = DocumentAnalyzer.extract_text_from_file(
            cv_document.chemin_fichier
        )
        if not extracted_text:
            st.error("❌ Impossible d'extraire le texte du CV")
            return False

        # Choisir la méthode d'analyse
        if "Grok" in method:
            # Analyse avec OpenAI GPT-4
            grok_service = get_grok_service()
            if not grok_service:
                st.error("❌ Service OpenAI non disponible")
                return False

            analysis_result = grok_service.analyze_cv(extracted_text)

            # Ajouter des métadonnées
            analysis_result["_analysis_method"] = "openai_gpt4"
            analysis_result["_cost_estimate"] = grok_service.get_cost_estimate(
                len(extracted_text)
            )

        else:
            # Analyse classique
            analysis_result = DocumentAnalyzer.analyze_cv_content(
                extracted_text, f"{consultant.prenom} {consultant.nom}"
            )
            analysis_result["_analysis_method"] = "classic"

        # Sauvegarder l'analyse en base
        with get_database_session() as session:
            cv_document.analyse_cv = json.dumps(analysis_result, ensure_ascii=False)
            session.commit()

        return True

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {e}")
        return False


def analyze_consultant_cv(consultant):
    """Analyse le CV du consultant avec choix de méthode"""
    st.markdown("### 🔍 Analyse du CV")

    try:
        with get_database_session() as session:
            cv_document = _find_latest_cv(session, consultant.id)
            if not cv_document:
                st.warning("⚠️ Aucun CV trouvé pour ce consultant")
                return

            grok_available = is_grok_available()
            selected_method = _display_analysis_method_selection(grok_available)

            _display_current_analysis_status(cv_document, consultant)
            _handle_analysis_button(cv_document, consultant, selected_method)
            _display_ai_configuration(grok_available)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse du CV: {e}")


def _find_latest_cv(session, consultant_id):
    """Trouve le CV le plus récent du consultant"""
    return (
        session.query(Document)
        .filter(
            Document.consultant_id == consultant_id,
            Document.type_document == "CV",
        )
        .order_by(Document.date_upload.desc())
        .first()
    )


def _display_analysis_method_selection(grok_available):
    """Affiche le sélecteur de méthode d'analyse"""
    st.markdown("#### 🎯 Méthode d'analyse")

    if grok_available:
        analysis_methods = ["🤖 IA avec GPT-4 (recommandé)"]
        default_index = 0
    else:
        analysis_methods = ["🔍 Analyse classique"]
        default_index = 0

    return st.selectbox(
        "Choisissez la méthode d'analyse :",
        options=analysis_methods,
        index=default_index,
        help="OpenAI GPT-4 offre une analyse plus précise et détaillée",
    )


def _display_current_analysis_status(cv_document, consultant):
    """Affiche le statut de l'analyse actuelle"""
    if cv_document.analyse_cv:
        st.info("ℹ️ Une analyse existe déjà. Vous pouvez la régénérer.")

        if st.button("👁️ Voir analyse actuelle", key="view_current_analysis"):
            try:
                import json

                analysis = json.loads(cv_document.analyse_cv)
                show_full_cv_analysis(analysis, cv_document.nom_fichier, consultant)
            except Exception as e:
                st.error(f"❌ Erreur lors de l'affichage: {e}")
    else:
        st.info("ℹ️ Aucune analyse disponible. Lancez une nouvelle analyse.")


def _handle_analysis_button(cv_document, consultant, selected_method):
    """Gère le bouton d'analyse et l'exécution"""
    button_text = (
        "🚀 Analyser avec GPT-4"
        if "Grok" in selected_method
        else "🔍 Analyser classiquement"
    )

    if st.button(button_text, type="primary", key="start_analysis"):
        with st.spinner("Analyse en cours..."):
            success = perform_cv_analysis(cv_document, consultant, selected_method)

        if success:
            st.success("✅ Analyse terminée avec succès !")
            st.rerun()
        else:
            st.error("❌ Échec de l'analyse")


def _display_ai_configuration(grok_available):
    """Affiche la configuration IA"""
    if grok_available:
        with st.expander("⚙️ Configuration IA"):
            from services.ai_grok_service import show_grok_config_interface

            show_grok_config_interface()
    else:
        with st.expander("⚙️ Configuration IA"):
            st.warning("⚠️ OpenAI GPT-4 non configuré")
            st.markdown(
                """
            Pour activer l'analyse IA :

            1. **Obtenez une clé API** sur [platform.openai.com](https://platform.openai.com)
            2. **Ajoutez la variable d'environnement** :
               ```bash
               export OPENAI_API_KEY="votre_clé_api_ici"
               ```
            3. **Redémarrez l'application**
            """
            )


def upload_document(consultant_id: int, data: Dict[str, Any]) -> bool:
    """Upload un document pour le consultant"""

    try:
        uploaded_file = data["file"]

        # Créer le répertoire d'upload s'il n'existe pas
        upload_dir = os.path.join("data", "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # Générer un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = uploaded_file.name
        file_extension = os.path.splitext(original_name)[1]
        unique_filename = (
            f"{consultant_id}_{data['type_document']}_{timestamp}{file_extension}"
        )
        file_path = os.path.join(upload_dir, unique_filename)

        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Analyser le document si c'est un CV
        analysis_result = None
        if data["type_document"] == "CV":
            try:
                # Extraire le texte du fichier
                extracted_text = DocumentAnalyzer.extract_text_from_file(file_path)

                # Analyser le contenu du CV
                if extracted_text:
                    analysis_result = DocumentAnalyzer.analyze_cv_content(
                        extracted_text, f"{consultant_id}"
                    )
            except Exception as e:
                st.warning(f"⚠️ Analyse CV non disponible: {e}")

        # Enregistrer en base de données
        with get_database_session() as session:
            document = Document(
                consultant_id=consultant_id,
                nom_fichier=original_name,
                chemin_fichier=file_path,
                type_document=data["type_document"],
                taille_fichier=len(uploaded_file.getbuffer()),
                mimetype=uploaded_file.type,
                description=(
                    data["description"].strip() if data["description"] else None
                ),
                date_upload=datetime.now(),
                analyse_cv=str(analysis_result) if analysis_result else None,
            )

            session.add(document)
            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de l'upload: {e}")
        return False


def download_document(document):
    """Télécharge un document"""

    try:
        if not os.path.exists(document.chemin_fichier):
            st.error("❌ Fichier introuvable sur le serveur")
            return

        with open(document.chemin_fichier, "rb") as f:
            file_data = f.read()

        st.download_button(
            label="📥 Télécharger maintenant",
            data=file_data,
            file_name=document.nom_fichier,
            mime=document.mimetype,
            key=f"download_btn_{document.id}",
        )

    except Exception as e:
        st.error(f"❌ Erreur lors du téléchargement: {e}")


def reanalyze_document(document_id: int, consultant) -> bool:
    """Réanalyse un document"""

    try:
        with get_database_session() as session:
            document = (
                session.query(Document).filter(Document.id == document_id).first()
            )

            if not document:
                st.error(ERROR_DOCUMENT_NOT_FOUND)
                return False

            if not os.path.exists(document.chemin_fichier):
                st.error("❌ Fichier introuvable sur le serveur")
                return False

            # Réanalyser le document
            extracted_text = DocumentAnalyzer.extract_text_from_file(
                document.chemin_fichier
            )
            if extracted_text:
                analysis_result = DocumentAnalyzer.analyze_cv_content(
                    extracted_text, f"{consultant.prenom} {consultant.nom}"
                )
            else:
                analysis_result = None

            # Mettre à jour la base de données
            document.analyse_cv = str(analysis_result) if analysis_result else None
            session.commit()

            st.success("✅ Document réanalysé avec succès !")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la réanalyse: {e}")
        return False


def _load_document_for_rename(document_id: int):
    """Charge un document pour renommage"""
    with get_database_session() as session:
        document = session.query(Document).filter(Document.id == document_id).first()
        if not document:
            st.error(ERROR_DOCUMENT_NOT_FOUND)
            return None
        return document


def _handle_rename_form_submission(
    document_id: int, new_name: str, new_description: str
):
    """Gère la soumission du formulaire de renommage"""
    if not new_name or not new_name.strip():
        st.error("❌ Le nom du fichier est obligatoire")
        return False

    success = rename_document(
        document_id,
        {
            "new_name": new_name.strip(),
            "new_description": (new_description.strip() if new_description else None),
        },
    )

    if success:
        st.success("✅ Document renommé avec succès !")
        if "rename_document" in st.session_state:
            del st.session_state.rename_document
        st.rerun()
        return True
    else:
        st.error("❌ Erreur lors du renommage")
        return False


def _handle_rename_form_cancellation():
    """Gère l'annulation du formulaire de renommage"""
    if "rename_document" in st.session_state:
        del st.session_state.rename_document
    st.rerun()


def show_rename_document_form(document_id: int):
    """Affiche le formulaire de renommage de document"""

    st.markdown("### ✏️ Renommer un document")

    try:
        document = _load_document_for_rename(document_id)
        if not document:
            return

        with st.form(f"rename_document_form_{document_id}", clear_on_submit=False):
            new_name = st.text_input(
                "Nouveau nom du fichier",
                value=document.nom_fichier,
                help="Entrez le nouveau nom du fichier (sans extension)",
            )

            new_description = st.text_area(
                "Nouvelle description",
                value=document.description or "",
                height=80,
                help="Description optionnelle du document",
            )

            # Boutons
            col1, col2, _ = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Renommer", type="primary")

            with col2:
                cancel = st.form_submit_button("❌ Annuler")

            if submitted:
                _handle_rename_form_submission(document_id, new_name, new_description)

            if cancel:
                _handle_rename_form_cancellation()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire: {e}")


def rename_document(document_id: int, data: Dict[str, Any]) -> bool:
    """Renomme un document"""

    try:
        with get_database_session() as session:
            document = (
                session.query(Document).filter(Document.id == document_id).first()
            )

            if not document:
                st.error(ERROR_DOCUMENT_NOT_FOUND)
                return False

            # Mettre à jour les informations
            document.nom_fichier = data["new_name"]
            document.description = data["new_description"]

            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors du renommage: {e}")
        return False


def delete_document(document_id: int) -> bool:
    """Supprime un document"""

    try:
        with get_database_session() as session:
            document = (
                session.query(Document).filter(Document.id == document_id).first()
            )

            if not document:
                st.error(ERROR_DOCUMENT_NOT_FOUND)
                return False

            # Supprimer le fichier physique
            if document.chemin_fichier and os.path.exists(document.chemin_fichier):
                try:
                    os.remove(document.chemin_fichier)
                except Exception as e:
                    st.warning(f"⚠️ Impossible de supprimer le fichier physique: {e}")

            # Supprimer de la base de données
            session.delete(document)
            session.commit()

            st.info("✅ Document supprimé")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")
        return False


def perform_cv_analysis(cv_document, consultant, method: str) -> bool:
    """Effectue l'analyse du CV selon la méthode choisie"""

    try:
        # Extraire le texte du document
        if not os.path.exists(cv_document.chemin_fichier):
            st.error("❌ Fichier CV introuvable")
            return False

        extracted_text = DocumentAnalyzer.extract_text_from_file(
            cv_document.chemin_fichier
        )
        if not extracted_text:
            st.error("❌ Impossible d'extraire le texte du CV")
            return False

        # Choisir la méthode d'analyse
        if "Grok" in method:
            # Analyse avec OpenAI GPT-4
            grok_service = get_grok_service()
            if not grok_service:
                st.error("❌ Service OpenAI non disponible")
                return False

            analysis_result = grok_service.analyze_cv(extracted_text)

            # Ajouter des métadonnées
            analysis_result["_analysis_method"] = "openai_gpt4"
            analysis_result["_cost_estimate"] = grok_service.get_cost_estimate(
                len(extracted_text)
            )

        else:
            # Analyse classique
            analysis_result = DocumentAnalyzer.analyze_cv_content(
                extracted_text, f"{consultant.prenom} {consultant.nom}"
            )
            analysis_result["_analysis_method"] = "classic"

        # Sauvegarder l'analyse en base
        with get_database_session() as session:
            cv_document.analyse_cv = json.dumps(analysis_result, ensure_ascii=False)
            session.commit()

        return True

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {e}")
        return False


def _display_cv_resume(analysis):
    """Affiche le résumé du CV"""
    if "resume" in analysis:
        st.markdown("#### 📋 Résumé")
        st.write(analysis["resume"])


def _display_cv_missions(analysis):
    """Affiche les missions détectées dans le CV"""
    if "missions" in analysis and analysis["missions"]:
        st.markdown("#### 🚀 Missions détectées")
        for i, mission in enumerate(analysis["missions"], 1):
            with st.expander(f"Mission {i}: {mission.get('titre', 'Sans titre')}"):
                st.write(f"**Client :** {mission.get('client', 'N/A')}")
                st.write(f"**Période :** {mission.get('periode', 'N/A')}")
                if mission.get("description"):
                    st.write(f"**Description :** {mission['description']}")


def _display_cv_competences(analysis):
    """Affiche les compétences détectées dans le CV"""
    if "competences" in analysis and analysis["competences"]:
        st.markdown("#### 🛠️ Compétences détectées")
        for competence in analysis["competences"]:
            st.write(f"• {competence}")


def _display_cv_contact(analysis):
    """Affiche les informations de contact détectées"""
    if "contact" in analysis and analysis["contact"]:
        st.markdown("#### 📞 Informations de contact")
        contact = analysis["contact"]
        if contact.get("email"):
            st.write(f"**Email :** {contact['email']}")
        if contact.get("telephone"):
            st.write(f"**Téléphone :** {contact['telephone']}")


def _display_cv_actions(analysis, consultant):
    """Affiche les actions disponibles sur l'analyse CV"""
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Sauvegarder l'analyse", key="save_analysis"):
            st.success("✅ Analyse sauvegardée dans le profil du consultant")

    with col2:
        if st.button("📊 Générer rapport", key="generate_cv_report"):
            generate_cv_report(analysis, consultant)


def show_full_cv_analysis(analysis, file_name, consultant):
    """Affiche l'analyse complète du CV"""

    st.markdown(f"### 🔍 Analyse complète du CV : {file_name}")
    st.markdown(f"**Consultant :** {consultant.prenom} {consultant.nom}")

    try:
        _display_cv_resume(analysis)
        _display_cv_missions(analysis)
        _display_cv_competences(analysis)
        _display_cv_contact(analysis)
        _display_cv_actions(analysis, consultant)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage de l'analyse complète: {e}")


def generate_cv_report(analysis, consultant):
    """Génère un rapport basé sur l'analyse du CV"""

    st.markdown("### 📊 Rapport d'analyse CV")

    try:
        report = f"""
# Rapport d'analyse CV
**Consultant :** {consultant.prenom} {consultant.nom}
**Date d'analyse :** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Résumé
{analysis.get('resume', 'Non disponible')}

## Missions ({len(analysis.get('missions', []))} détectées)
"""

        for i, mission in enumerate(analysis.get("missions", []), 1):
            report += f"""
### Mission {i}
- **Titre :** {mission.get('titre', 'N/A')}
- **Client :** {mission.get('client', 'N/A')}
- **Période :** {mission.get('periode', 'N/A')}
- **Description :** {mission.get('description', 'N/A')}
"""

        report += f"""
## Compétences ({len(analysis.get('competences', []))} détectées)
"""
        for competence in analysis.get("competences", []):
            report += f"- {competence}\n"

        # Télécharger le rapport
        st.download_button(
            label="📥 Télécharger le rapport",
            data=report,
            file_name=f"rapport_cv_{consultant.prenom}_{consultant.nom}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            key="download_cv_report",
        )

        st.success("✅ Rapport généré avec succès !")

    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du rapport: {e}")


def show_documents_report(documents):
    """Affiche un rapport détaillé des documents"""

    st.markdown("### 📊 Rapport des documents")

    if not documents:
        st.info("ℹ️ Aucun document à analyser")
        return

    # Statistiques détaillées
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Statistiques générales")
        st.write(f"**Total documents :** {len(documents)}")

        # Répartition par type
        types = {}
        for doc in documents:
            doc_type = doc.type_document or "Autre"
            types[doc_type] = types.get(doc_type, 0) + 1

        st.write("**Répartition par type :**")
        for doc_type, count in types.items():
            st.write(f"  - {doc_type} : {count}")

    with col2:
        st.markdown("#### 📊 Métriques")
        total_size = sum(doc.taille_fichier or 0 for doc in documents)
        st.write(f"**Taille totale :** {total_size / (1024 * 1024):.2f} MB")

        analyzed_count = sum(1 for doc in documents if doc.analyse_cv)
        st.write(f"**Documents analysés :** {analyzed_count}/{len(documents)}")

        # Documents par mois
        current_month = datetime.now().month
        current_year = datetime.now().year
        recent_docs = sum(
            1
            for doc in documents
            if doc.date_upload
            and doc.date_upload.month == current_month
            and doc.date_upload.year == current_year
        )
        st.write(f"**Documents ce mois :** {recent_docs}")

    # Liste détaillée
    st.markdown("#### 📋 Liste détaillée")

    doc_data = []
    for doc in documents:
        doc_data.append(
            {
                "Nom": doc.nom_fichier,
                "Type": doc.type_document or "N/A",
                "Taille (KB)": round((doc.taille_fichier or 0) / 1024, 1),
                "Date upload": (
                    doc.date_upload.strftime("%d/%m/%Y") if doc.date_upload else "N/A"
                ),
                "Analysé": "✅" if doc.analyse_cv else "❌",
            }
        )

    df = pd.DataFrame(doc_data)
    st.dataframe(df, width="stretch", hide_index=True)


# Helper methods pour show_document_details()


def _display_document_basic_info(document):
    """Affiche les informations de base du document."""
    st.markdown("**📄 Informations**")
    st.write(f"**Nom :** {document.nom_fichier}")
    st.write(f"**Type :** {document.type_document}")
    st.write(f"**Taille :** {document.taille_fichier or 'N/A'} octets")

    if document.date_upload:
        st.write(f"**Upload :** {document.date_upload.strftime('%d/%m/%Y %H:%M')}")


def _display_document_metadata(document):
    """Affiche les métadonnées du document."""
    st.markdown("**📊 Métadonnées**")
    if document.mimetype:
        st.write(f"**Type MIME :** {document.mimetype}")

    if document.chemin_fichier:
        st.write(f"**Chemin :** {document.chemin_fichier}")

    if document.analyse_cv:
        st.write("**Analyse CV :** ✅ Disponible")
    else:
        st.write("**Analyse CV :** ❌ Non disponible")


def _display_cv_analysis_summary(document, consultant):
    """Affiche le résumé de l'analyse CV si disponible."""
    if not document.analyse_cv:
        return

    st.markdown("**🔍 Analyse CV**")
    try:
        analysis = json.loads(document.analyse_cv)

        # Afficher un résumé de l'analyse
        if "missions" in analysis and analysis["missions"]:
            st.write(f"**Missions détectées :** {len(analysis['missions'])}")

        if "competences" in analysis and analysis["competences"]:
            st.write(f"**Compétences détectées :** {len(analysis['competences'])}")

        # Bouton pour voir l'analyse complète
        if st.button(
            "👁️ Voir analyse complète",
            key=f"view_analysis_{document.id}",
        ):
            show_full_cv_analysis(analysis, document.nom_fichier, consultant)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage de l'analyse: {e}")


def _display_document_actions(document, consultant):
    """Affiche les actions disponibles pour le document."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📥 Télécharger", key=f"download_doc_{document.id}"):
            download_document(document)

    with col2:
        if st.button("🔄 Réanalyser", key=f"reanalyze_doc_{document.id}"):
            if reanalyze_document(document.id, consultant):
                st.rerun()

    with col3:
        if st.button("✏️ Renommer", key=f"rename_doc_{document.id}"):
            st.session_state.rename_document = document.id
            st.rerun()

    with col4:
        if st.button("🗑️ Supprimer", key=f"delete_doc_{document.id}"):
            if delete_document(document.id):
                st.rerun()


def _handle_rename_form(document):
    """Gère l'affichage du formulaire de renommage si activé."""
    if (
        "rename_document" in st.session_state
        and st.session_state.rename_document == document.id
    ):
        show_rename_document_form(document.id)
