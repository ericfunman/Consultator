from datetime import datetime

import streamlit as st

from services.document_service import DocumentService
# Export pour les tests
from database.database import get_database_session


def show_consultant_documents(consultant):
    """Affiche et                 with col1:
        if doc_type == "CV" and st.button(
            " Analyser", key=f"analyze_existing_{file_path.name}"
        ):
            st.info(" Analyse de CV en cours de developpement...")

    with col2:
        if st.button(" Telecharger", key=f"download_{file_path.name}"):
            st.info(" Telechargement en cours de developpement...")

    with col3:
        if st.button(" Aperçu", key=f"preview_{file_path.name}"):
            st.info(" Aperçu en cours de developpement...")ments du consultant"""

    st.subheader(f" Documents de {consultant.prenom} {consultant.nom}")

    # Section d'upload de nouveaux documents
    with st.expander(" Ajouter un nouveau document", expanded=False):
        uploaded_file = st.file_uploader(
            "Choisir un fichier",
            type=["pdf", "docx", "doc", "pptx", "ppt"],
            help="Formats supportes: PDF, Word (docx/doc), PowerPoint (pptx/ppt)",
            key=f"document_uploader_{consultant.id}",
        )

        if uploaded_file is not None:
            # Afficher les informations du fichier
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(" Nom", uploaded_file.name)

            with col2:
                file_size = uploaded_file.size / 1024  # en KB
                if file_size > 1024:
                    size_display = f"{file_size / 1024:.1f} MB"
                else:
                    size_display = f"{file_size:.1f} KB"
                st.metric(" Taille", size_display)

            with col3:
                document_type = st.selectbox(
                    "Type",
                    options=[
                        "CV",
                        "Lettre de motivation",
                        "Certificat",
                        "Contrat",
                        "Autre",
                    ],
                    key=f"doc_type_{consultant.id}",
                )

            description = st.text_area(
                "Description (optionnel)",
                placeholder="Ajoutez une description pour ce document...",
                key=f"doc_desc_{consultant.id}",
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    " Sauvegarder",
                    type="primary",
                    key=f"save_doc_{consultant.id}",
                ):
                    save_consultant_document(uploaded_file, consultant, document_type, description)

            with col2:
                if st.button(" Annuler", key=f"cancel_doc_{consultant.id}"):
                    st.rerun()

    st.markdown("---")

    # Liste des documents existants
    show_existing_documents(consultant)


def save_consultant_document(uploaded_file, consultant, document_type, _):
    """Sauvegarde un document pour le consultant"""

    try:
        # Initialiser le repertoire d'upload
        upload_dir = DocumentService.init_upload_directory()

        # Verifier le type de fichier
        if not DocumentService.is_allowed_file(uploaded_file.name):
            st.error(" Type de fichier non supporte")
            return

        # Generer un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = DocumentService.get_file_extension(uploaded_file.name)

        # Nom du fichier: consultant_nom_type_timestamp.extension
        safe_name = f"{consultant.prenom}_{consultant.nom}_{document_type}_{timestamp}.{file_extension}"
        safe_name = safe_name.replace(" ", "_").replace("-", "_")

        file_path = upload_dir / safe_name

        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f" Document '{document_type}' sauvegarde avec succes !")
        st.info(f" Fichier: {safe_name}")

        # Si c'est un CV, proposer l'analyse automatique
        if document_type == "CV":
            if st.button(" Analyser ce CV", key=f"analyze_{consultant.id}"):
                st.info(" Analyse de CV en cours de developpement...")

        # Recharger la page pour afficher le nouveau document
        st.rerun()

    except Exception as e:
        st.error(f" Erreur lors de la sauvegarde: {e}")


def _get_file_size_display(file_size_bytes):
    """Formate la taille du fichier pour l'affichage"""
    file_size_kb = file_size_bytes / 1024
    if file_size_kb >= 1024:
        return f"{file_size_kb / 1024:.1f} MB"
    else:
        return f"{file_size_kb:.1f} KB"


def _extract_document_type(file_name):
    """Extrait le type de document du nom de fichier"""
    doc_types = ["CV", "Lettre_de_motivation", "Certificat", "Contrat", "Autre"]
    for dtype in doc_types:
        if dtype in file_name:
            return dtype.replace("_", " ")
    return "Inconnu"


def _render_document_metrics(file_stats, doc_type):
    """Affiche les métriques d'un document"""
    col1, col2, col3, col4 = st.columns(4)

    size_display = _get_file_size_display(file_stats.st_size)
    modified_time = datetime.fromtimestamp(file_stats.st_mtime)

    with col1:
        st.metric("📏 Taille", size_display)

    with col2:
        st.metric("📅 Modifie", modified_time.strftime("%d/%m/%Y"))

    with col3:
        st.metric("📄 Type", doc_type)

    return col4


def _render_document_actions(file_path, doc_type):
    """Affiche les boutons d'action pour un document"""
    col1, col2, col3 = st.columns(3)

    with col1:
        if doc_type == "CV" and st.button("🔍 Analyser", key=f"analyze_existing_{file_path.name}"):
            st.info("🔍 Analyse de CV en cours de developpement...")

    with col2:
        if st.button("⬇️ Telecharger", key=f"download_{file_path.name}"):
            st.info("⬇️ Telechargement en cours de developpement...")

    with col3:
        if st.button("👁️ Previsualiser", key=f"preview_{file_path.name}"):
            st.info("👁️ Previsualisation en cours de developpement...")


def show_existing_documents(consultant):
    """Affiche les documents existants du consultant"""
    try:
        upload_dir = DocumentService.init_upload_directory()

        # Chercher les fichiers du consultant
        consultant_pattern = f"{consultant.prenom}_{consultant.nom}_*"
        matching_files = list(upload_dir.glob(consultant_pattern))

        if not matching_files:
            st.info("📄 Aucun document trouve pour ce consultant")
            return

        st.subheader(f"📁 Documents existants ({len(matching_files)})")

        # Afficher chaque document dans un expander
        for file_path in sorted(matching_files, key=lambda x: x.stat().st_mtime, reverse=True):
            file_stats = file_path.stat()
            doc_type = _extract_document_type(file_path.name)

            with st.expander(f"📄 {doc_type} - {file_path.name}", expanded=False):
                # Métriques du document
                col4 = _render_document_metrics(file_stats, doc_type)

                # Bouton de suppression
                with col4:
                    if st.button("🗑️ Supprimer", key=f"delete_{file_path.name}"):
                        delete_consultant_document(file_path)

                # Boutons d'action
                _render_document_actions(file_path, doc_type)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des documents: {e}")


def delete_consultant_document(file_path):
    """Supprime un document du consultant"""

    try:
        if file_path.exists():
            file_path.unlink()
            st.success(" Document supprime avec succes")
            st.rerun()
        else:
            st.error(" Fichier introuvable")
    except Exception as e:
        st.error(f" Erreur lors de la suppression: {e}")
