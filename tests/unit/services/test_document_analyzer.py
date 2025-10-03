"""
Tests unitaires pour le service DocumentAnalyzer
Couvre l'extraction et l'analyse de contenu de CV
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.services.document_analyzer import DocumentAnalyzer


class TestDocumentAnalyzer:
    """Tests pour la classe DocumentAnalyzer"""

    def test_extract_technical_skills(self):
        """Test extraction des compétences techniques"""
        text = "Développement en Python avec Django et PostgreSQL. Utilisation de Docker et Kubernetes."

        skills = DocumentAnalyzer._extract_technical_skills(text)

        assert "Python" in skills
        assert "PostgreSQL" in skills
        assert "Docker" in skills
        assert "Kubernetes" in skills

    def test_extract_technical_skills_specialized(self):
        """Test extraction des compétences spécialisées Data/Finance"""
        text = "Travail sur Basel III, SWIFT messaging et Central Bank Reporting."

        skills = DocumentAnalyzer._extract_technical_skills(text)

        assert "Basel III" in skills
        assert "SWIFT" in skills
        assert "Central Bank Reporting" in skills

    def test_extract_technical_skills_empty(self):
        """Test extraction avec texte sans compétences"""
        text = "Texte sans aucune compétence technique mentionnée."

        skills = DocumentAnalyzer._extract_technical_skills(text)

        assert skills == []

    def test_find_dates_in_text_improved(self):
        """Test extraction de dates améliorée"""
        text = "Mission de janvier 2023 à mars 2024 chez BNP Paribas."

        dates = DocumentAnalyzer._find_dates_in_text_improved(text)

        assert "2023-01-01" in dates
        assert "2024-03-01" in dates

    def test_find_dates_in_text_ongoing(self):
        """Test extraction de dates avec mission en cours"""
        text = "Depuis janvier 2023 - En cours : Consultant senior."

        dates = DocumentAnalyzer._find_dates_in_text_improved(text)

        assert "2023-01-01" in dates
        assert "En cours" in dates

    def test_find_dates_in_text_range(self):
        """Test extraction de dates en plage"""
        text = "2019-2022 : Développement d'applications web."

        dates = DocumentAnalyzer._find_dates_in_text_improved(text)

        assert "2019-01-01" in dates
        assert "2022-12-31" in dates

    def test_month_name_to_number(self):
        """Test conversion mois texte vers numéro"""
        assert DocumentAnalyzer._month_name_to_number("janvier") == "01"
        assert DocumentAnalyzer._month_name_to_number("juillet") == "07"
        assert DocumentAnalyzer._month_name_to_number("décembre") == "12"
        assert DocumentAnalyzer._month_name_to_number("invalid") == "01"

    def test_find_client_in_block_improved_known_client(self):
        """Test recherche de client connu"""
        block = "Mission chez BNP Paribas pour développer une application."

        client = DocumentAnalyzer._find_client_in_block_improved(block)

        assert client == "BNP Paribas"

    def test_find_client_in_block_improved_pattern(self):
        """Test recherche de client par pattern"""
        block = "Consultant pour Société Générale - Développement Java."

        client = DocumentAnalyzer._find_client_in_block_improved(block)

        assert client == "Société Générale"

    def test_find_client_in_block_improved_no_client(self):
        """Test avec aucun client trouvé"""
        block = "Développement d'une application web sans client particulier mentionné."

        client = DocumentAnalyzer._find_client_in_block_improved(block)

        assert client == ""

    def test_extract_long_mission_summary(self):
        """Test extraction de résumé de mission long"""
        text = "Développement d'une plateforme de trading en temps réel. Conception de l'architecture microservices. Implémentation en Python avec FastAPI. Déploiement sur Kubernetes."

        summary = DocumentAnalyzer._extract_long_mission_summary(text)

        assert len(summary) > 50
        assert "développement" in summary.lower()
        assert "architecture" in summary.lower()

    def test_extract_functional_skills(self):
        """Test extraction des compétences fonctionnelles"""
        text = (
            "Management d'équipe de 5 développeurs. Gestion de projet Agile avec Scrum. Formation des équipes junior."
        )

        skills = DocumentAnalyzer._extract_functional_skills(text)

        assert "Management" in skills
        assert "Gestion De Projet" in skills
        assert "Scrum" in skills

    def test_extract_general_info_email(self):
        """Test extraction d'informations générales - email"""
        text = "Contact: jean.dupont@email.com Téléphone: 0123456789"

        info = DocumentAnalyzer._extract_general_info(text)

        assert info["email"] == "jean.dupont@email.com"
        assert info["telephone"] == "0123456789"

    def test_extract_general_info_no_info(self):
        """Test extraction d'informations générales - aucune info"""
        text = "Texte sans email ni téléphone."

        info = DocumentAnalyzer._extract_general_info(text)

        assert info == {}

    def test_clean_client_name(self):
        """Test nettoyage du nom de client"""
        assert DocumentAnalyzer._clean_client_name("BNP PARIBAS") == "Bnp Paribas"
        assert DocumentAnalyzer._clean_client_name("société générale!") == "Société Générale"
        assert DocumentAnalyzer._clean_client_name("ABC") == "Abc"

    def test_date_sort_key(self):
        """Test création de clé de tri pour dates"""
        assert DocumentAnalyzer._date_sort_key("2023-01-01") == "2023-01-01"
        assert DocumentAnalyzer._date_sort_key("2023") == "2023-01-01"
        assert DocumentAnalyzer._date_sort_key("En cours") == "9999-12-31"
        assert DocumentAnalyzer._date_sort_key("") == "9999-12-31"

    @patch("app.services.document_analyzer.DocumentAnalyzer._extract_missions")
    @patch("app.services.document_analyzer.DocumentAnalyzer._extract_technical_skills")
    @patch("app.services.document_analyzer.DocumentAnalyzer._extract_functional_skills")
    @patch("app.services.document_analyzer.DocumentAnalyzer._extract_general_info")
    def test_analyze_cv_content(self, mock_general_info, mock_functional, mock_technical, mock_missions):
        """Test analyse complète du contenu CV"""
        # Mocks
        mock_missions.return_value = [
            {
                "client": "BNP Paribas",
                "date_debut": "2023-01-01",
                "date_fin": "En cours",
                "langages_techniques": ["Python", "SQL"],
            }
        ]
        mock_technical.return_value = ["Python", "SQL", "Docker"]
        mock_functional.return_value = ["Management", "Agile"]
        mock_general_info.return_value = {"email": "test@email.com"}

        text = "Contenu du CV de test"
        result = DocumentAnalyzer.analyze_cv_content(text, "Test Consultant")

        assert result["consultant"] == "Test Consultant"
        assert len(result["missions"]) == 1
        assert "Python" in result["langages_techniques"]
        assert "Management" in result["competences_fonctionnelles"]
        assert result["informations_generales"]["email"] == "test@email.com"

    def test_clean_and_deduplicate_missions(self):
        """Test nettoyage et déduplication des missions"""
        missions = [
            {
                "client": "BNP Paribas",
                "date_debut": "2023-01-01",
                "date_fin": "En cours",
                "resume": "Développement application",
            },
            {
                "client": "BNP Paribas",
                "date_debut": "2023-01-01",
                "date_fin": "En cours",
                "resume": "Développement application",  # Doublon
            },
            {
                "client": "Société Générale",
                "date_debut": "2022-01-01",
                "date_fin": "2022-12-31",
                "resume": "Analyse fonctionnelle",
            },
        ]

        cleaned = DocumentAnalyzer._clean_and_deduplicate_missions(missions)

        assert len(cleaned) == 2  # Un doublon supprimé
        assert cleaned[0]["client"] == "BNP Paribas"
        assert cleaned[1]["client"] == "Société Générale"

    def test_extract_missions_by_patterns(self):
        """Test extraction de missions par patterns"""
        text = "2023-2024: Développement d'application chez BNP Paribas. 2021-2022: Analyse chez Société Générale."

        missions = DocumentAnalyzer._extract_missions_by_patterns(text)

        assert len(missions) >= 1
        # Les assertions spécifiques dépendent du contenu exact

    def test_extract_missions_by_known_clients(self):
        """Test extraction de missions par clients connus"""
        text = "Travail chez BNP Paribas depuis 2023. Mission chez Société Générale en 2022."

        missions = DocumentAnalyzer._extract_missions_by_known_clients(text)

        # Au moins une mission devrait être trouvée
        assert len(missions) >= 1

    def test_extract_client_from_text(self):
        """Test extraction de client depuis un texte"""
        text = "Mission chez BNP Paribas pour développer une application."

        client = DocumentAnalyzer._extract_client_from_text(text)

        assert client == "BNP Paribas"

    def test_extract_client_from_text_no_client(self):
        """Test extraction de client - aucun client trouvé"""
        text = "Développement d'une application sans client spécifique."

        client = DocumentAnalyzer._extract_client_from_text(text)

        assert client == ""

    def test_get_analysis_preview(self):
        """Test génération d'aperçu d'analyse"""
        analysis_data = {
            "consultant": "Jean Dupont",
            "missions": [
                {
                    "client": "BNP Paribas",
                    "date_debut": "2023-01-01",
                    "date_fin": "En cours",
                    "resume": "Développement d'application de trading",
                    "langages_techniques": ["Python", "SQL"],
                }
            ],
            "langages_techniques": ["Python", "SQL", "Docker"],
            "competences_fonctionnelles": ["Management", "Agile"],
            "informations_generales": {"email": "jean@email.com"},
            "texte_brut": "Aperçu du texte extrait...",
        }

        preview = DocumentAnalyzer.get_analysis_preview(analysis_data)

        assert "Jean Dupont" in preview
        assert "BNP Paribas" in preview
        assert "Python" in preview
        assert "Management" in preview

    def test_test_analysis(self):
        """Test la méthode de test d'analyse"""
        result = DocumentAnalyzer.test_analysis()

        assert "consultant" in result
        assert "missions" in result
        assert "langages_techniques" in result
        assert isinstance(result["missions"], list)
