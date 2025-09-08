"""
Module d'upload et gestion des documents pour les consultants
Permet l'upload de CV, documents et l'association aux profils consultants
"""

import os
import sys
from datetime import datetime

import streamlit as st

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Variables pour les imports
DocumentService = None
ConsultantService = None
imports_ok = False

try:
    from services.document_service import DocumentService

    imports_ok = True
except ImportError as e:
    st.error(f" Erreur d'import: {e}")

def show_document_upload_section(consultant_id=None):
    """Affiche la section d'upload de documents"""

    if not imports_ok:
        st.error(" Les services de documents ne sont pas disponibles")
        return

    st.subheader(" Upload de documents")

    # Interface d'upload
    uploaded_file = st.file_uploader(
        " Choisir un fichier",
        type=["pdf", "docx", "doc", "pptx", "ppt"],
        help="Formats supportés: PDF, Word (docx/doc), PowerPoint (pptx/ppt)",
        key="document_uploader",
    )

    if uploaded_file is not None:
        # Afficher les informations du fichier
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(" Nom du fichier", uploaded_file.name)

        with col2:
            file_size = uploaded_file.size / 1024  # en KB
            if file_size > 1024:
                size_display = f"{file_size / 1024:.1f} MB"
            else:
                size_display = f"{file_size:.1f} KB"
            st.metric(" Taille", size_display)

        # Boutons d'action
        if st.button(
            " Sauvegarder document", type="primary", key="save_document"
        ):
            save_uploaded_document(uploaded_file)

def save_uploaded_document(uploaded_file):
    """Sauvegarde le document uploadé"""

    try:
        # Initialiser le répertoire d'upload
        upload_dir = DocumentService.init_upload_directory()

        # Générer un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = DocumentService.get_file_extension(uploaded_file.name)
        safe_name = f"document_{timestamp}.{file_extension}"

        file_path = upload_dir / safe_name

        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f" Document sauvegardé: {safe_name}")
        st.info(f" Fichier sauvegardé dans: {file_path}")

    except Exception as e:
        st.error(f" Erreur lors de la sauvegarde: {e}")

def show():
    """Point d'entrée principal pour la page de gestion des documents"""

    st.title(" Gestion des documents")
    st.markdown("### Uploadez et gérez les documents")

    if not imports_ok:
        st.error(" Les services de documents ne sont pas disponibles")
        return

    show_document_upload_section()