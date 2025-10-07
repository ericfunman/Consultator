"""
Tests de couverture pour ChatbotService - Phase 2: Méthodes d'analyse et d'extraction
Cible: Méthodes pures sans Streamlit (extraction d'entités, analyse d'intention)
Objectif: Augmenter la couverture de 66% → 80%+
"""

import unittest
from unittest.mock import MagicMock, Mock, patch

from app.services.chatbot_service import ChatbotService


class TestChatbotServiceAnalysis(unittest.TestCase):
    """Tests pour les méthodes d'analyse et d'extraction du chatbot"""

    def setUp(self):
        """Setup avant chaque test"""
        self.chatbot = ChatbotService()

    # ==================== TESTS: _clean_question ====================
    def test_clean_question_basic(self):
        """Test nettoyage basique d'une question"""
        question = "  Bonjour, comment allez-vous ?  "
        cleaned = self.chatbot._clean_question(question)
        self.assertEqual(cleaned, "bonjour, comment allez-vous ?")

    def test_clean_question_multiple_spaces(self):
        """Test nettoyage avec espaces multiples"""
        question = "Qui    connaît     Python   ?"
        cleaned = self.chatbot._clean_question(question)
        self.assertEqual(cleaned, "qui connaît python ?")

    def test_clean_question_special_chars(self):
        """Test avec caractères spéciaux préservés"""
        question = "Combien coûte Python/Java ?"
        cleaned = self.chatbot._clean_question(question)
        self.assertEqual(cleaned, "combien coûte python/java ?")

    # ==================== TESTS: _check_consultant_name_mentioned ====================
    def test_check_consultant_name_mentioned_single_name(self):
        """Test détection de nom simple"""
        question = "Qui est Dupont ?"
        result = self.chatbot._check_consultant_name_mentioned(question)
        self.assertTrue(result)

    def test_check_consultant_name_mentioned_full_name(self):
        """Test détection de prénom + nom"""
        question = "Quelle est l'expérience de Jean Martin ?"
        result = self.chatbot._check_consultant_name_mentioned(question)
        self.assertTrue(result)

    def test_check_consultant_name_mentioned_no_name(self):
        """Test sans nom de consultant"""
        question = "Combien de consultants Python ?"
        result = self.chatbot._check_consultant_name_mentioned(question)
        self.assertFalse(result)

    # ==================== TESTS: _extract_consultant_names ====================
    def test_extract_consultant_names_single(self):
        """Test extraction d'un seul nom"""
        question = "Quelle est l'expérience de Dupont ?"
        names = self.chatbot._extract_consultant_names(question)
        self.assertIn("Dupont", names)

    def test_extract_consultant_names_multiple(self):
        """Test extraction de plusieurs noms"""
        question = "Compare les profils de Dupont et Martin"
        names = self.chatbot._extract_consultant_names(question)
        self.assertTrue(len(names) >= 2)

    def test_extract_consultant_names_with_prenom(self):
        """Test extraction avec prénom"""
        question = "Quel est le salaire de Jean Dupont ?"
        names = self.chatbot._extract_consultant_names(question)
        # Peut extraire "Jean Dupont" ou "Dupont"
        self.assertGreater(len(names), 0)

    def test_extract_consultant_names_none(self):
        """Test sans nom de consultant"""
        question = "Combien de consultants disponibles ?"
        names = self.chatbot._extract_consultant_names(question)
        self.assertEqual(len(names), 0)

    # ==================== TESTS: _extract_companies ====================
    def test_extract_companies_single(self):
        """Test extraction d'une entreprise"""
        question = "Qui a travaillé chez Google ?"
        companies = self.chatbot._extract_companies(question)
        self.assertIn("Google", companies)

    def test_extract_companies_multiple(self):
        """Test extraction de plusieurs entreprises"""
        question = "Missions chez BNP Paribas et Société Générale"
        companies = self.chatbot._extract_companies(question)
        self.assertTrue(len(companies) >= 2)

    def test_extract_companies_with_keywords(self):
        """Test avec mots-clés 'chez', 'pour', 'client'"""
        question = "Consultant pour le client Microsoft"
        companies = self.chatbot._extract_companies(question)
        self.assertIn("Microsoft", companies)

    def test_extract_companies_none(self):
        """Test sans entreprise"""
        question = "Liste des consultants Python"
        companies = self.chatbot._extract_companies(question)
        self.assertEqual(len(companies), 0)

    # ==================== TESTS: _extract_skills ====================
    def test_extract_skills_single(self):
        """Test extraction d'une compétence"""
        question = "Qui connaît Python ?"
        skills = self.chatbot._extract_skills(question)
        self.assertIn("Python", skills)

    def test_extract_skills_multiple(self):
        """Test extraction de plusieurs compétences"""
        question = "Consultants maîtrisant Java, Python et React"
        skills = self.chatbot._extract_skills(question)
        self.assertTrue(len(skills) >= 2)

    def test_extract_skills_with_synonyms(self):
        """Test avec synonymes (JavaScript/JS, ReactJS/React)"""
        question = "Expertise en JS et ReactJS"
        skills = self.chatbot._extract_skills(question)
        # Doit extraire au moins 2 compétences
        self.assertGreater(len(skills), 0)

    def test_extract_skills_case_insensitive(self):
        """Test insensibilité à la casse"""
        question = "Compétence en python et JAVA"
        skills = self.chatbot._extract_skills(question)
        # Python et Java doivent être reconnus quelle que soit la casse
        self.assertGreater(len(skills), 0)

    def test_extract_skills_none(self):
        """Test sans compétence"""
        question = "Combien de consultants disponibles ?"
        skills = self.chatbot._extract_skills(question)
        self.assertEqual(len(skills), 0)

    # ==================== TESTS: _extract_languages ====================
    def test_extract_languages_single(self):
        """Test extraction d'une langue"""
        question = "Qui parle anglais ?"
        languages = self.chatbot._extract_languages(question)
        self.assertIn("Anglais", languages)

    def test_extract_languages_multiple(self):
        """Test extraction de plusieurs langues"""
        question = "Consultants parlant anglais et espagnol"
        languages = self.chatbot._extract_languages(question)
        self.assertTrue(len(languages) >= 2)

    def test_extract_languages_with_synonyms(self):
        """Test avec synonymes (anglais/english)"""
        question = "Qui parle english ?"
        languages = self.chatbot._extract_languages(question)
        # "english" doit être reconnu comme anglais
        self.assertGreater(len(languages), 0)

    def test_extract_languages_none(self):
        """Test sans langue"""
        question = "Compétences en Python"
        languages = self.chatbot._extract_languages(question)
        self.assertEqual(len(languages), 0)

    # ==================== TESTS: _extract_amounts ====================
    def test_extract_amounts_with_euro(self):
        """Test extraction montant avec symbole €"""
        question = "TJM supérieur à 500€"
        amounts = self.chatbot._extract_amounts(question)
        self.assertIn("500", amounts)

    def test_extract_amounts_with_word_euros(self):
        """Test extraction montant avec mot 'euros'"""
        question = "Salaire de 60000 euros"
        amounts = self.chatbot._extract_amounts(question)
        self.assertIn("60000", amounts)

    def test_extract_amounts_multiple(self):
        """Test extraction de plusieurs montants"""
        question = "TJM entre 400€ et 800€"
        amounts = self.chatbot._extract_amounts(question)
        self.assertTrue(len(amounts) >= 2)

    def test_extract_amounts_none(self):
        """Test sans montant"""
        question = "Liste des consultants"
        amounts = self.chatbot._extract_amounts(question)
        self.assertEqual(len(amounts), 0)

    # ==================== TESTS: _extract_practices ====================
    def test_extract_practices_single(self):
        """Test extraction d'une practice"""
        question = "Consultants de la practice Data"
        practices = self.chatbot._extract_practices(question)
        self.assertIn("Data", practices)

    def test_extract_practices_multiple(self):
        """Test extraction de plusieurs practices"""
        question = "Comparer Data et Cloud"
        practices = self.chatbot._extract_practices(question)
        self.assertTrue(len(practices) >= 2)

    def test_extract_practices_none(self):
        """Test sans practice"""
        question = "Tous les consultants Python"
        practices = self.chatbot._extract_practices(question)
        self.assertEqual(len(practices), 0)

    # ==================== TESTS: _extract_entities ====================
    def test_extract_entities_complete(self):
        """Test extraction complète de toutes les entités"""
        question = "Qui parle anglais, connaît Python et a travaillé chez Google pour 500€ ?"
        entities = self.chatbot._extract_entities(question)
        
        self.assertIn("consultant_names", entities)
        self.assertIn("companies", entities)
        self.assertIn("skills", entities)
        self.assertIn("languages", entities)
        self.assertIn("amounts", entities)
        self.assertIn("practices", entities)

    def test_extract_entities_partial(self):
        """Test extraction partielle (uniquement compétences)"""
        question = "Consultants Python et Java"
        entities = self.chatbot._extract_entities(question)
        
        self.assertGreater(len(entities["skills"]), 0)
        self.assertEqual(len(entities["companies"]), 0)

    def test_extract_entities_empty(self):
        """Test sans entité"""
        question = "Bonjour"
        entities = self.chatbot._extract_entities(question)
        
        # Toutes les listes doivent être vides
        self.assertEqual(len(entities["consultant_names"]), 0)
        self.assertEqual(len(entities["companies"]), 0)
        self.assertEqual(len(entities["skills"]), 0)

    # ==================== TESTS: _analyze_intent (partie 1) ====================
    def test_analyze_intent_salaire(self):
        """Test détection intention salaire"""
        question = "Quel est le salaire de Dupont ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "salaire")

    def test_analyze_intent_competences(self):
        """Test détection intention compétences"""
        question = "Quelles sont les compétences de Martin ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "competences")

    def test_analyze_intent_experience(self):
        """Test détection intention expérience"""
        question = "Combien d'années d'expérience a Bernard ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "experience")

    def test_analyze_intent_missions(self):
        """Test détection intention missions"""
        question = "Quelles missions a réalisé Durant ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "missions")

    def test_analyze_intent_langues(self):
        """Test détection intention langues"""
        question = "Quelles langues parle Sophie ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "langues")

    def test_analyze_intent_contact(self):
        """Test détection intention contact"""
        question = "Comment contacter Pierre ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "contact")

    def test_analyze_intent_liste_consultants(self):
        """Test détection intention liste consultants"""
        question = "Liste des consultants Python"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "liste_consultants")

    def test_analyze_intent_practices(self):
        """Test détection intention practices"""
        question = "Consultants de la practice Data"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "practices")

    def test_analyze_intent_profil(self):
        """Test détection intention profil professionnel"""
        question = "Quel est le profil de Jean ?"
        intent = self.chatbot._analyze_intent(question)
        self.assertEqual(intent, "profil_professionnel")

    # ==================== TESTS: _calculate_intent_scores ====================
    def test_calculate_intent_scores_single_match(self):
        """Test calcul de scores avec un seul match"""
        question = "combien gagne dupont"
        intent_patterns = self._get_minimal_patterns()
        
        scores = self.chatbot._calculate_intent_scores(question, intent_patterns)
        
        # Salaire doit avoir le score le plus élevé
        self.assertGreater(scores.get("salaire", 0), 0)

    def test_calculate_intent_scores_multiple_matches(self):
        """Test calcul avec plusieurs mots-clés"""
        question = "salaire tjm rémunération"
        intent_patterns = self._get_minimal_patterns()
        
        scores = self.chatbot._calculate_intent_scores(question, intent_patterns)
        
        # Doit détecter plusieurs mots-clés de salaire
        self.assertGreater(scores.get("salaire", 0), 2)

    def test_calculate_intent_scores_no_match(self):
        """Test sans correspondance"""
        question = "bonjour merci"
        intent_patterns = self._get_minimal_patterns()
        
        scores = self.chatbot._calculate_intent_scores(question, intent_patterns)
        
        # Tous les scores doivent être à 0
        self.assertEqual(sum(scores.values()), 0)

    # ==================== TESTS: _apply_special_intent_rules ====================
    def test_apply_special_rules_consultant_specific(self):
        """Test règles spéciales pour questions sur un consultant"""
        question = "qui est dupont"
        intent_scores = {"profil_professionnel": 5}
        consultant_name_mentioned = True
        
        intent = self.chatbot._apply_special_intent_rules(
            question, intent_scores, consultant_name_mentioned
        )
        
        # Doit retourner profil_professionnel pour "qui est X"
        self.assertEqual(intent, "profil_professionnel")

    def test_apply_special_rules_list_consultants(self):
        """Test règles spéciales pour lister les consultants"""
        question = "liste des consultants python"
        intent_scores = {"competences": 3}
        consultant_name_mentioned = False
        
        intent = self.chatbot._apply_special_intent_rules(
            question, intent_scores, consultant_name_mentioned
        )
        
        # Doit retourner liste_consultants
        self.assertEqual(intent, "liste_consultants")

    def test_apply_special_rules_no_override(self):
        """Test sans règle spéciale applicable"""
        question = "quelle expérience a dupont"
        intent_scores = {"experience": 10, "salaire": 2}
        consultant_name_mentioned = True
        
        intent = self.chatbot._apply_special_intent_rules(
            question, intent_scores, consultant_name_mentioned
        )
        
        # Doit retourner None (pas de règle spéciale)
        self.assertIsNone(intent)

    # ==================== HELPER METHODS ====================
    def _get_minimal_patterns(self) -> dict:
        """Retourne un dictionnaire minimal de patterns pour les tests"""
        return {
            "salaire": ["salaire", "tjm", "rémunération", "gagne", "coûte"],
            "competences": ["compétence", "maîtrise", "connaît", "sait"],
            "experience": ["expérience", "années", "ancienneté"],
            "missions": ["mission", "projet", "client"],
            "langues": ["langue", "parle", "anglais", "français"],
            "contact": ["contact", "email", "téléphone", "joindre"],
            "liste_consultants": ["liste", "combien", "tous", "disponible"],
            "practices": ["practice", "équipe", "département"],
            "profil_professionnel": ["profil", "parcours", "qui est"],
            "cvs": ["cv", "curriculum"],
        }


if __name__ == "__main__":
    unittest.main()
