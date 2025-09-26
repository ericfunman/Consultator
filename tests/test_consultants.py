import os
import sys
from datetime import date
from unittest.mock import patch

# Ajouter le répertoire parent au path pour les imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Imports des fonctions à tester
from app.pages_modules.consultants import FORMAT_DATE
from app.pages_modules.consultants import LABEL_COMPETENCES
from app.pages_modules.consultants import LABEL_PRACTICE
from app.pages_modules.consultants import LABEL_STATUT
from app.pages_modules.consultants import LABEL_TAILLE
from app.pages_modules.consultants import LABEL_TECHNOLOGIES
from app.pages_modules.consultants import MSG_CHAMP_OBLIGATOIRE
from app.pages_modules.consultants import MSG_CHAMPS_OBLIGATOIRES
from app.pages_modules.consultants import MSG_FICHIER_INTROUVABLE
from app.pages_modules.consultants import STATUT_DISPONIBLE
from app.pages_modules.consultants import STATUT_NON_AFFECTE
from app.pages_modules.consultants import VALEUR_NON_SPECIFIE
from app.pages_modules.consultants import _add_extension_from_full_filename
from app.pages_modules.consultants import _add_extension_to_original_name
from app.pages_modules.consultants import _build_consultant_data
from app.pages_modules.consultants import _build_update_data
from app.pages_modules.consultants import _build_update_data_from_form
from app.pages_modules.consultants import _extract_original_name_from_parts
from app.pages_modules.consultants import _find_original_parts_before_timestamp
from app.pages_modules.consultants import _get_filename_remaining_parts
from app.pages_modules.consultants import _handle_extension_in_last_part
from app.pages_modules.consultants import _handle_no_timestamp_found
from app.pages_modules.consultants import _is_timestamp_part
from app.pages_modules.consultants import detect_document_type
from app.pages_modules.consultants import extract_original_filename
from app.pages_modules.consultants import get_mime_type
from app.pages_modules.consultants import show_validation_errors
from app.pages_modules.consultants import validate_mission_fields


class TestDocumentTypeDetection:
    """Tests pour la détection automatique du type de document"""

    def test_detect_document_type_cv_variations(self):
        """Test de détection des CV avec différentes variations"""
        test_cases = [
            ("mon_cv.pdf", "CV"),
            ("CV_Jean_Dupont.docx", "CV"),
            ("resume_martin.pptx", "CV"),
            ("curriculum_vitae.pdf", "CV"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_lettre_motivation(self):
        """Test de détection des lettres de motivation"""
        test_cases = [
            ("lettre_motivation.pdf", "Lettre de motivation"),
            ("cover_letter.docx", "Lettre de motivation"),
            ("motivation_jean.doc", "Lettre de motivation"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_certificats(self):
        """Test de détection des certificats"""
        test_cases = [
            ("certificat_python.pdf", "Certificat"),
            ("diploma_university.docx", "Certificat"),
            ("certificate_aws.pdf", "Certificat"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_contrats(self):
        """Test de détection des contrats"""
        test_cases = [
            ("contrat_cdi.pdf", "Contrat"),
            ("contract_freelance.docx", "Contrat"),
            ("convention_stage.pdf", "Contrat"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_presentations(self):
        """Test de détection des présentations"""
        test_cases = [
            ("presentation_projet.pptx", "Présentation"),
            ("slides_demo.ppt", "Présentation"),
            ("pitch_startup.pptx", "Présentation PowerPoint"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_extensions(self):
        """Test de détection basée sur les extensions"""
        test_cases = [
            ("document.pdf", "Document PDF"),
            ("report.docx", "Document Word"),
            ("data.xlsx", "Document"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_powerpoint_extensions(self):
        """Test de détection des fichiers PowerPoint par extension"""
        test_cases = [
            ("presentation_final.pptx", "Présentation"),
            ("meeting_notes.ppt", "Présentation PowerPoint"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"

    def test_detect_document_type_unknown(self):
        """Test avec des fichiers inconnus"""
        test_cases = [
            ("file.unknown", "Document"),
            ("random_file", "Document"),
            ("", "Document"),
        ]

        for filename, expected in test_cases:
            result = detect_document_type(filename)
            assert (
                result == expected
            ), f"Échec pour {filename}: attendu {expected}, obtenu {result}"


class TestMimeTypeDetection:
    """Tests pour la détection des types MIME"""

    def test_get_mime_type_pdf(self):
        """Test du type MIME pour PDF"""
        assert get_mime_type("document.pdf") == "application/pdf"

    def test_get_mime_type_word(self):
        """Test du type MIME pour Word"""
        assert (
            get_mime_type("document.docx")
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        assert get_mime_type("document.doc") == "application/msword"

    def test_get_mime_type_powerpoint(self):
        """Test du type MIME pour PowerPoint"""
        assert (
            get_mime_type("presentation.pptx")
            == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        assert get_mime_type("presentation.ppt") == "application/vnd.ms-powerpoint"

    def test_get_mime_type_unknown(self):
        """Test du type MIME par défaut"""
        assert get_mime_type("file.unknown") == "application/octet-stream"
        assert get_mime_type("file") == "application/octet-stream"


class TestFilenameExtraction:
    """Tests pour l'extraction du nom original des fichiers"""

    def test_extract_original_filename_simple(self):
        """Test d'extraction simple"""
        filename = "1_Jean_Dupont_CV_20231201_120000.pdf"
        result = extract_original_filename(filename)
        assert result == "CV.pdf"

    def test_extract_original_filename_complex(self):
        """Test d'extraction avec nom complexe"""
        filename = "1_Jean_Dupont_Lettre_Motivation_20231201_120000.pdf"
        result = extract_original_filename(filename)
        assert result == "Lettre_Motivation.pdf"

    def test_extract_original_filename_no_timestamp(self):
        """Test sans timestamp"""
        filename = "1_Jean_Dupont_CV.pdf"
        result = extract_original_filename(filename)
        assert result == "CV.pdf.pdf"

    def test_extract_original_filename_old_format(self):
        """Test avec l'ancien format"""
        filename = "Jean_Dupont_CV_20231201_120000.pdf"
        result = extract_original_filename(filename)
        assert result == "Jean_Dupont_CV_20231201_120000.pdf"

    def test_extract_original_filename_no_match(self):
        """Test avec nom qui ne correspond pas au format"""
        filename = "random_file.pdf"
        result = extract_original_filename(filename)
        assert result == "random_file.pdf"

    def test_extract_original_filename_empty(self):
        """Test avec chaîne vide"""
        result = extract_original_filename("")
        assert result == ""

    def test_is_timestamp_part_valid(self):
        """Test de détection de timestamp valide"""
        assert _is_timestamp_part("20231201") == True
        assert _is_timestamp_part("20240115") == True

    def test_is_timestamp_part_invalid(self):
        """Test de détection de timestamp invalide"""
        assert _is_timestamp_part("2023") == False
        assert _is_timestamp_part("abc12345") == False
        assert _is_timestamp_part("123456789") == False

    def test_get_filename_remaining_parts(self):
        """Test d'extraction des parties restantes"""
        parts = ["1", "Jean", "Dupont", "CV", "20231201", "120000.pdf"]
        result = _get_filename_remaining_parts(parts)
        assert result == ["CV", "20231201", "120000.pdf"]

    def test_handle_no_timestamp_found(self):
        """Test quand aucun timestamp n'est trouvé"""
        parts = ["CV", "Version", "Finale"]
        result = _handle_no_timestamp_found(parts)
        assert result == ["CV", "Version"]  # Retourne tout sauf le dernier

    def test_find_original_parts_before_timestamp(self):
        """Test de recherche des parties avant timestamp"""
        parts = ["CV", "20231201", "120000.pdf"]
        original_parts, timestamp_found = _find_original_parts_before_timestamp(parts)
        assert original_parts == ["CV"]
        assert timestamp_found == True

    def test_find_original_parts_no_timestamp(self):
        """Test quand pas de timestamp trouvé"""
        parts = ["CV", "Version", "Finale.pdf"]
        original_parts, timestamp_found = _find_original_parts_before_timestamp(parts)
        assert original_parts == ["CV", "Version"]
        assert timestamp_found == False

    def test_extract_original_name_from_parts_with_extension(self):
        """Test d'extraction avec extension dans les parties"""
        remaining_parts = ["CV", "20231201", "120000.pdf"]
        result = _extract_original_name_from_parts(remaining_parts, "full_name.pdf")
        assert result == "CV.pdf"

    def test_extract_original_name_from_parts_no_extension(self):
        """Test d'extraction sans extension dans les parties"""
        remaining_parts = ["CV", "Simple"]
        result = _extract_original_name_from_parts(remaining_parts, "full_name.pdf")
        assert result == "CV.pdf"

    def test_add_extension_to_original_name_with_dot(self):
        """Test d'ajout d'extension quand elle existe déjà"""
        result = _add_extension_to_original_name(
            "CV", ["20231201", "120000.pdf"], True, "full.pdf"
        )
        assert result == "CV.pdf"

    def test_add_extension_to_original_name_without_dot(self):
        """Test d'ajout d'extension depuis le nom complet"""
        result = _add_extension_to_original_name(
            "CV", ["20231201", "120000"], True, "full.pdf"
        )
        assert result == "CV.pdf"

    def test_handle_extension_in_last_part_timestamp(self):
        """Test de gestion d'extension dans la dernière partie avec timestamp"""
        result = _handle_extension_in_last_part("CV", "120000.pdf", True, "full.pdf")
        assert result == "CV.pdf"

    def test_handle_extension_in_last_part_no_timestamp(self):
        """Test de gestion d'extension sans timestamp"""
        result = _handle_extension_in_last_part("CV", "Final.pdf", False, "full.pdf")
        assert result == "CV.pdf"

    def test_add_extension_from_full_filename(self):
        """Test d'ajout d'extension depuis le nom complet"""
        result = _add_extension_from_full_filename("CV", "full.pdf")
        assert result == "CV.pdf"


class TestMissionValidation:
    """Tests pour la validation des missions"""

    def test_validate_mission_fields_valid(self):
        """Test de validation avec champs valides"""
        client = "Société Générale"
        titre = "Développeur Python"
        date_debut = date.today()

        errors = validate_mission_fields(client, titre, date_debut, 1)
        assert errors == []

    def test_validate_mission_fields_missing_client(self):
        """Test de validation sans client"""
        client = ""
        titre = "Développeur Python"
        date_debut = date.today()

        errors = validate_mission_fields(client, titre, date_debut, 1)
        assert "mission_1_client" in errors

    def test_validate_mission_fields_missing_title(self):
        """Test de validation sans titre"""
        client = "Société Générale"
        titre = ""
        date_debut = date.today()

        errors = validate_mission_fields(client, titre, date_debut, 1)
        assert "mission_1_titre" in errors

    def test_validate_mission_fields_missing_date(self):
        """Test de validation sans date de début"""
        client = "Société Générale"
        titre = "Développeur Python"
        date_debut = None

        errors = validate_mission_fields(client, titre, date_debut, 1)
        assert "mission_1_debut" in errors

    def test_validate_mission_fields_multiple_errors(self):
        """Test de validation avec plusieurs erreurs"""
        client = ""
        titre = ""
        date_debut = None

        errors = validate_mission_fields(client, titre, date_debut, 2)
        assert "mission_2_client" in errors
        assert "mission_2_titre" in errors
        assert "mission_2_debut" in errors

    def test_validate_mission_fields_whitespace_only(self):
        """Test de validation avec espaces seulement"""
        client = "   "
        titre = "   "
        date_debut = date.today()

        errors = validate_mission_fields(client, titre, date_debut, 1)
        assert "mission_1_client" in errors
        assert "mission_1_titre" in errors


class TestDataBuilding:
    """Tests pour la construction des données"""

    def test_build_consultant_data_complete(self):
        """Test de construction des données complètes"""
        basic_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@email.com",
            "telephone": "01.23.45.67.89",
            "salaire": 45000,
            "disponibilite": True,
            "practice_id": 1,
        }

        company_data = {
            "societe": "Quanteam",
            "date_entree": date(2020, 1, 15),
            "date_sortie": None,
            "date_premiere_mission": date(2020, 3, 1),
        }

        professional_data = {
            "grade": "Confirmé",
            "type_contrat": "CDI",
        }

        notes = "Consultant expérimenté"

        result = _build_consultant_data(
            basic_data, company_data, professional_data, notes
        )

        assert result["prenom"] == "Jean"
        assert result["nom"] == "Dupont"
        assert result["email"] == "jean.dupont@email.com"
        assert result["telephone"] == "01.23.45.67.89"
        assert result["salaire"] == 45000
        assert result["disponible"] == True
        assert result["practice_id"] == 1
        assert result["societe"] == "Quanteam"
        assert result["date_entree_societe"] == date(2020, 1, 15)
        assert result["date_sortie_societe"] is None
        assert result["date_premiere_mission"] == date(2020, 3, 1)
        assert result["grade"] == "Confirmé"
        assert result["type_contrat"] == "CDI"
        assert result["notes"] == "Consultant expérimenté"

    def test_build_consultant_data_minimal(self):
        """Test de construction des données minimales"""
        basic_data = {
            "prenom": "Marie",
            "nom": "Martin",
            "email": "marie.martin@email.com",
            "telephone": "",
            "salaire": 40000,
            "disponibilite": False,
            "practice_id": None,
        }

        company_data = {
            "societe": "Asigma",
            "date_entree": date(2021, 6, 1),
            "date_sortie": date(2023, 12, 31),
            "date_premiere_mission": None,
        }

        professional_data = {
            "grade": "Junior",
            "type_contrat": "CDD",
        }

        result = _build_consultant_data(basic_data, company_data, professional_data, "")

        assert result["prenom"] == "Marie"
        assert result["nom"] == "Martin"
        assert result["telephone"] is None
        assert result["practice_id"] is None
        assert result["date_sortie_societe"] == date(2023, 12, 31)
        assert result["date_premiere_mission"] is None
        assert result["notes"] is None

    def test_build_update_data_from_form(self):
        """Test de construction des données de mise à jour"""
        form_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@email.com",
            "telephone": "01.23.45.67.89",
            "salaire": 50000,
            "disponibilite": True,
            "selected_practice_id": 2,
            "notes": "Notes mises à jour",
            "societe": "Quanteam",
            "date_entree": date(2020, 1, 15),
            "date_sortie": None,
            "date_premiere_mission": date(2020, 3, 1),
            "grade": "Senior",
            "type_contrat": "CDI",
        }

        result = _build_update_data_from_form(form_data)

        assert result["prenom"] == "Jean"
        assert result["nom"] == "Dupont"
        assert result["email"] == "jean.dupont@email.com"
        assert result["telephone"] == "01.23.45.67.89"
        assert result["salaire_actuel"] == 50000
        assert result["disponibilite"] == True
        assert result["practice_id"] == 2
        assert result["societe"] == "Quanteam"
        assert result["grade"] == "Senior"
        assert result["type_contrat"] == "CDI"

    def test_build_update_data(self):
        """Test de construction des données de mise à jour (ancienne fonction)"""
        form_data = {
            "prenom": "Pierre",
            "nom": "Durand",
            "email": "pierre.durand@email.com",
            "telephone": "06.12.34.56.78",
            "salaire": 55000,
            "disponibilite": False,
            "selected_practice_id": 3,
            "notes": "Ancienne fonction",
            "societe": "Quanteam",
            "date_entree": date(2019, 9, 1),
            "date_sortie": date(2022, 8, 31),
            "date_premiere_mission": date(2019, 11, 1),
            "grade": "Manager",
            "type_contrat": "CDI",
        }

        result = _build_update_data(form_data)

        assert result["prenom"] == "Pierre"
        assert result["nom"] == "Durand"
        assert result["email"] == "pierre.durand@email.com"
        assert result["telephone"] == "06.12.34.56.78"
        assert result["salaire_actuel"] == 55000
        assert result["disponibilite"] == False
        assert result["practice_id"] == 3
        assert result["societe"] == "Quanteam"
        assert result["date_entree_societe"] == date(2019, 9, 1)
        assert result["date_sortie_societe"] == date(2022, 8, 31)
        assert result["date_premiere_mission"] == date(2019, 11, 1)
        assert result["grade"] == "Manager"
        assert result["type_contrat"] == "CDI"


class TestConstants:
    """Tests pour vérifier les constantes"""

    def test_constants_values(self):
        """Test des valeurs des constantes"""
        assert STATUT_NON_AFFECTE == "Non affecté"
        assert STATUT_DISPONIBLE == "✅ Disponible"
        assert LABEL_STATUT == "📊 Statut"
        assert FORMAT_DATE == "%d/%m/%Y"
        assert LABEL_PRACTICE == "🏢 Practice"
        assert LABEL_COMPETENCES == "💼 Compétences"
        assert VALEUR_NON_SPECIFIE == "Non spécifié"
        assert LABEL_TECHNOLOGIES == "🛠️ Technologies"
        assert LABEL_TAILLE == "📊 Taille"
        assert MSG_FICHIER_INTROUVABLE == "❌ Fichier introuvable"
        assert MSG_CHAMP_OBLIGATOIRE == "Ce champ est obligatoire"
        assert (
            MSG_CHAMPS_OBLIGATOIRES
            == "❌ Veuillez remplir tous les champs obligatoires (*)"
        )


@patch("app.pages_modules.consultants.st.markdown")
@patch("app.pages_modules.consultants.st.write")
class TestValidationDisplay:
    """Tests pour l'affichage des erreurs de validation"""

    def test_show_validation_errors_with_errors(self, mock_write, mock_markdown):
        """Test d'affichage des erreurs de validation"""
        errors = ["mission_1_client", "mission_1_titre"]
        result = show_validation_errors(errors, 1)

        assert result == True
        # Vérifier que markdown a été appelé pour le style
        mock_markdown.assert_called()

    def test_show_validation_errors_no_errors(self, mock_write, mock_markdown):
        """Test sans erreurs de validation"""
        errors = []
        result = show_validation_errors(errors, 1)

        assert result == False
        # Vérifier que rien n'a été affiché
        mock_markdown.assert_not_called()
        mock_write.assert_not_called()
