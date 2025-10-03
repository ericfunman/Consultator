"""
Service Chatbot pour interroger les données des consultants
Utilise l'IA pour répondre aux questions sur la base de données
"""

import json
import re
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import streamlit as st
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

# Imports des services existants
from database.database import get_database_session
from database.models import Competence
from database.models import Consultant
from database.models import ConsultantCompetence
from database.models import ConsultantLangue
from database.models import Langue
from database.models import Mission
from database.models import Practice

# Import de la fonction de calcul de disponibilité
try:
    from pages_modules.consultant_info import _calculate_availability_status
except ImportError:
    # Fallback en cas d'import impossible
    def _calculate_availability_status(consultant) -> str:
        return "✅ Disponible" if consultant.disponibilite else "❌ Non disponible"


class ChatbotService:
    """Service principal du chatbot pour Consultator"""

    # Constantes pour les chaînes de format répétées
    SECTION_HEADER_SUFFIX = "** :\n\n"
    YEARS_SUFFIX = " années\n"
    TOTAL_PREFIX = "\n📊 **Total : "
    CONSULTANT_FOUND_SUFFIX = " consultant(s) trouvé(s)**"
    STATS_PREFIX = "\n\n📊 **"
    BULLET_POINT = " • "
    BULLET_POINT_INDENT = "   • "
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self):
        # Suppression de la session partagée pour éviter les timeouts
        # Chaque méthode utilisera une session fraîche via context manager
        self.conversation_history = []
        self.last_question = ""

    def _get_session(self):
        """
        Retourne une session de base de données fraîche
        Utilisé pour éviter les timeouts de session après inactivité
        """
        return get_database_session()

    def _execute_with_fresh_session(self, query_func):
        """
        Exécute une fonction de requête avec une session fraîche
        Args:
            query_func: Fonction qui prend une session en paramètre et retourne un résultat
        """
        try:
            with get_database_session() as session:
                return query_func(session)
        except Exception as e:
            print(f"Erreur de session dans le chatbot: {e}")
            # Retry avec une nouvelle session
            try:
                with get_database_session() as session:
                    return query_func(session)
            except Exception as e2:
                print(f"Erreur lors du retry: {e2}")
                return None

    def _route_question_to_handler(self, intent: str, entities: dict) -> Dict[str, Any]:
        """Route la question vers le bon handler selon l'intention"""
        if intent == "salaire":
            return self._handle_salary_question(entities)
        elif intent == "experience":
            return self._handle_experience_question(entities)
        elif intent == "profil_professionnel":
            return self._handle_professional_profile_question(entities)
        elif intent == "competences":
            return self._handle_skills_question(entities)
        elif intent == "langues":
            return self._handle_languages_question(entities)
        elif intent == "missions":
            return self._handle_missions_question(entities)
        elif intent == "contact":
            return self._handle_contact_question(entities)
        elif intent == "liste_consultants":
            return self._handle_list_consultants_question()
        elif intent == "practices":
            return self._handle_practices_question(entities)
        elif intent == "cvs":
            return self._handle_cvs_question(entities)
        elif intent == "statistiques":
            return self._handle_stats_question()
        elif intent == "disponibilite":  # Nouveau handler V1.2.2
            return self._handle_availability_question(entities)
        elif intent == "tjm_mission":  # Nouveau handler V1.2.2
            return self._handle_mission_tjm_question(entities)
        elif intent == "recherche_consultant":
            return self._handle_consultant_search(entities)
        else:
            return self._handle_general_question()

    def process_question(self, question: str) -> Dict[str, Any]:
        """
        Traite une question et retourne une réponse structurée

        Args:
            question: Question de l'utilisateur

        Returns:
            Dict contenant la réponse, les données et métadonnées
        """
        try:
            # Nettoyer et analyser la question
            clean_question = self._clean_question(question)
            self.last_question = clean_question  # Stocker pour usage dans les handlers
            intent = self._analyze_intent(clean_question)
            entities = self._extract_entities(clean_question)

            # Router vers le bon handler
            return self._route_question_to_handler(intent, entities)

        except Exception as e:
            return {
                "response": f"❌ Désolé, j'ai rencontré une erreur : {str(e)}",
                "data": None,
                "intent": "error",
                "confidence": 0.0,
            }

    def _clean_question(self, question: str) -> str:
        """Nettoie et normalise la question"""
        # Supprimer la ponctuation excessive
        question = re.sub(r"!{2,}", "!", question)
        question = re.sub(r"\?{2,}", "?", question)

        # Normaliser les espaces
        question = re.sub(r"\s+", " ", question.strip())

        return question.lower()

    def _check_consultant_name_mentioned(self, question: str) -> bool:
        """Vérifie si un nom de consultant est mentionné dans la question"""
        with get_database_session() as session:
            all_consultants = session.query(Consultant).all()
            for consultant in all_consultants:
                if re.search(rf"\b{re.escape(consultant.prenom.lower())}\b", question) or re.search(
                    rf"\b{re.escape(consultant.nom.lower())}\b", question
                ):
                    return True
            return False

    def _get_intent_patterns(self) -> Dict[str, List[str]]:
        """Retourne les patterns pour identifier les intentions"""
        return {
            "salaire": [
                r"salaire",
                r"rémunération",
                r"paie",
                r"combien gagne",
                r"revenus",
                r"euros",
                r"€",
                r"salaire de",
                r"gagne",
                r"cjm",
                r"coût journalier",
            ],
            "experience": [
                r"expérience",
                r"experience",
                r"années d'expérience",
                r"annees d'experience",
                r"ancienneté",
                r"seniorité",
                r"séniorité",
                r"depuis quand",
                r"depuis combien",
                r"combien d'années",
                r"combien d'annees",
                r"quel âge",
                r"âge professionnel",
            ],
            "profil_professionnel": [
                r"grade",
                r"niveau",
                r"poste",
                r"fonction",
                r"junior",
                r"confirmé",
                r"senior",
                r"manager",
                r"directeur",
                r"type contrat",
                r"type de contrat",
                r"contrat",
                r"cdi",
                r"cdd",
                r"stagiaire",
                r"alternant",
                r"indépendant",
                r"freelance",
                r"société",
                r"societe",
                r"quanteam",
                r"asigma",
                r"entreprise",
            ],
            "competences": [
                r"compétences",
                r"competences",
                r"maîtrise",
                r"maitrise",
                r"sait faire",
                r"technologies",
                r"langages",
                r"outils",
                r"expertise",
                r"python",
                r"sql",
                r"java",
                r"quelles\s+(?:\w+\s+)*compétences",
                r"quelles\s+(?:\w+\s+)*competences",
                r"skills",
                r"techno",
                r"connaît",
                r"connait",
            ],
            "langues": [
                r"langues?",
                r"langue",
                r"parle",
                r"parlent",
                r"anglais",
                r"français",
                r"espagnol",
                r"allemand",
                r"italien",
                r"bilingue",
                r"niveau\s+(?:\w+\s+)*langue",
                r"parle\s+(?:\w+\s+)*anglais",
                r"qui\s+(?:\w+\s+)*parle",
                r"quelles\s+(?:\w+\s+)*langues",
                r"polyglotte",
                r"linguistique",
            ],
            "missions": [
                r"missions",
                r"mission",
                r"travaille",
                r"chez",
                r"entreprise",
                r"client",
                r"projet",
                r"bnp",
                r"paribas",
                r"société générale",
                r"combien\s+(?:\w+\s+)*missions?",
                r"nombre\s+(?:\w+\s+)*missions?",
                r"projets",
            ],
            "contact": [
                r"mail",
                r"email",
                r"e-mail",
                r"téléphone",
                r"tel",
                r"numéro",
                r"contact",
                r"joindre",
                r"coordonnées",
            ],
            "liste_consultants": [
                r"quels sont les consultants",
                r"liste des consultants",
                r"consultants disponibles",
                r"consultants actifs",
                r"tous les consultants",
                r"lister les consultants",
                r"qui sont les consultants",
                r"montrer les consultants",
            ],
            "practices": [
                r"practice",
                r"practices",
                r"qui est dans la practice",
                r"consultants de la practice",
                r"practice data",
                r"practice quant",
                r"équipe",
                r"dans quelle practice",
            ],
            "cvs": [
                r"cv",
                r"curriculum",
                r"document",
                r"fichier",
                r"upload",
                r"téléchargé",
            ],
            "statistiques": [
                r"combien\s+(?:[\w-]+\s+)*consultants",
                r"nombre\s+(?:[\w-]+\s+)*consultants",
                r"combien\s+(?:[\w-]+\s+)*dans\s+(?:[\w-]+\s+)*base",
                r"nombre",
                r"moyenne",
                r"total",
                r"statistiques",
                r"combien\s+(?:[\w-]+\s+)*missions",
                r"actifs",
                r"inactifs",
                r"tjm moyen",
                r"combien y a",
                r"il y a combien",
            ],
            "disponibilite": [  # Nouvelle intention V1.2.2
                r"disponible",
                r"disponibilité",
                r"libre",
                r"quand\s+(?:\w+\s+)*libre",
                r"quand\s+(?:\w+\s+)*disponible",
                r"date\s+(?:\w+\s+)*disponibilité",
                r"fin\s+(?:\w+\s+)*mission",
                r"libéré",
                r"fini",
                r"termine",
                r"asap",
                r"immédiatement",
                r"tout de suite",
                r"prochaine disponibilité",
            ],
            "tjm_mission": [  # Nouvelle intention V1.2.2
                r"tjm\s+(?:\w+\s+)*mission",
                r"taux\s+(?:\w+\s+)*mission",
                r"prix\s+(?:\w+\s+)*mission",
                r"coût\s+(?:\w+\s+)*mission",
                r"tarif\s+(?:\w+\s+)*mission",
                r"facturation\s+(?:\w+\s+)*mission",
                r"journalier\s+(?:\w+\s+)*mission",
                r"combien\s+(?:\w+\s+)*coûte\s+(?:\w+\s+)*mission",
                r"prix\s+(?:\w+\s+)*journée\s+(?:\w+\s+)*mission",
                r"tjm mission",
                r"prix mission",
                r"coût mission",
                r"tarif mission",
                r"taux journalier mission",
                r"combien coûte mission",
            ],
            "recherche_consultant": [
                r"qui est",
                r"consultant",
                r"profil",
                r"information sur",
                r"details",
            ],
        }

    def _calculate_intent_scores(self, question: str, intent_patterns: Dict[str, List[str]]) -> Dict[str, int]:
        """Calcule les scores pour chaque intention"""
        intent_scores: Dict[str, int] = {}
        for intent, patterns in intent_patterns.items():
            score: int = 0
            for pattern in patterns:
                if re.search(pattern, question):
                    score += 1
            intent_scores[intent] = score
        return intent_scores

    def _apply_special_intent_rules(
        self, question: str, intent_scores: Dict[str, int], has_consultant_name: bool
    ) -> Optional[str]:
        """Applique les règles spéciales pour déterminer l'intention"""

        # Vérifier les règles pour consultants nommés
        consultant_specific = self._check_consultant_specific_rules(question, intent_scores, has_consultant_name)
        if consultant_specific:
            return consultant_specific

        # Vérifier les règles générales basées sur les patterns
        pattern_based = self._check_pattern_based_rules(question, intent_scores)
        if pattern_based:
            return pattern_based

        return None

    def _check_consultant_specific_rules(
        self, question: str, intent_scores: Dict[str, int], has_consultant_name: bool
    ) -> Optional[str]:
        """Vérifie les règles spécifiques aux consultants nommés"""
        if not has_consultant_name:
            return None

        # Si un nom de consultant est mentionné et qu'on parle de salaire
        if intent_scores.get("salaire", 0) > 0:
            return "salaire"

        # Si un nom de consultant est mentionné et qu'on demande des coordonnées
        if intent_scores.get("contact", 0) > 0:
            return "contact"

        # Si un nom de consultant est mentionné et qu'on parle de missions
        if intent_scores.get("missions", 0) > 0:
            return "missions"

        # Si le mot "combien" est utilisé avec un nom de consultant, c'est probablement un salaire
        if re.search(r"combien", question):
            return "salaire"

        return None

    def _check_pattern_based_rules(self, question: str, intent_scores: Dict[str, int]) -> Optional[str]:
        """Vérifie les règles basées sur les patterns de texte"""

        # NOUVELLE RÈGLE V1.2.2 : Prioriser tjm_mission sur missions si TJM est mentionné
        if intent_scores.get("tjm_mission", 0) > 0 and re.search(r"tjm|taux|prix|coût|tarif", question):
            return "tjm_mission"

        # Questions de type "combien de consultants en CDI/CDD"
        if re.search(
            r"combien\s+(?:[\w-]+\s+)*consultants?\s+(?:[\w-]+\s+)*(?:cdi|cdd|stagiaire|alternant|indépendant)",
            question,
        ):
            return "profil_professionnel"

        # Questions de type "qui travaille chez" - utiliser des mots-clés simples pour éviter ReDoS
        question_lower = question.lower()
        if (
            "qui" in question_lower
            and ("travaille" in question_lower or "est" in question_lower)
            and ("chez" in question_lower or "dans" in question_lower)
            and ("quanteam" in question_lower or "asigma" in question_lower)
        ):
            return "profil_professionnel"

        # Questions de type "combien de missions"
        if re.search(r"combien\s+(?:\w+\s+)*missions?", question):
            return "missions"

        # Questions de type "combien de consultants"
        if re.search(
            r"combien\s+(?:\w+\s+){0,3}(?:consultants?|dans\s+(?:\w+\s+){0,3}base)",
            question,
        ):
            return "statistiques"

        return None

    def _analyze_intent(self, question: str) -> str:
        """Analyse l'intention de la question"""

        # D'abord, vérifier s'il y a un nom de consultant mentionné
        has_consultant_name = self._check_consultant_name_mentioned(question)

        # Patterns pour identifier les intentions
        intent_patterns = self._get_intent_patterns()

        # Scorer chaque intention
        intent_scores = self._calculate_intent_scores(question, intent_patterns)

        # Appliquer les règles spéciales
        special_intent = self._apply_special_intent_rules(question, intent_scores, has_consultant_name)
        if special_intent:
            return special_intent

        # Retourner l'intention avec le meilleur score
        if max(intent_scores.values()) > 0:
            best_intent = max(intent_scores, key=lambda k: intent_scores[k])
            return best_intent
        else:
            return "general"

    def _extract_consultant_names(self, question: str) -> List[str]:
        """Extrait les noms de consultants de la question"""
        noms = []
        question_lower = question.lower()

        with get_database_session() as session:
            all_consultants = session.query(Consultant).all()

        for consultant in all_consultants:
            # Chercher le prénom dans la question (insensible à la casse)
            if re.search(rf"\b{re.escape(consultant.prenom.lower())}\b", question_lower):
                noms.append(consultant.prenom)
            # Chercher le nom de famille dans la question
            if re.search(rf"\b{re.escape(consultant.nom.lower())}\b", question_lower):
                noms.append(consultant.nom)
            # Chercher le nom complet
            nom_complet: str = f"{consultant.prenom} {consultant.nom}".lower()
            if nom_complet in question_lower:
                noms.append(f"{consultant.prenom} {consultant.nom}")

        # Supprimer les doublons en gardant l'ordre
        return list(dict.fromkeys(noms))

    def _extract_companies(self, question: str) -> List[str]:
        """Extrait les noms d'entreprises de la question"""
        entreprises = []
        entreprises_connues: List[str] = [
            "bnp paribas",
            "société générale",
            "axa",
            "orange",
            "airbus",
            "renault",
            "peugeot",
            "total",
            "carrefour",
            "crédit agricole",
        ]
        for entreprise in entreprises_connues:
            if entreprise in question:
                entreprises.append(entreprise)
        return entreprises

    def _extract_skills(self, question: str) -> List[str]:
        """Extrait les compétences de la question"""
        from database.models import Competence

        competences = []

        # Compétences techniques prédéfinies
        competences_connues: List[str] = [
            "python",
            "java",
            "javascript",
            "sql",
            "react",
            "angular",
            "node.js",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "power bi",
            "agile",
            "scrum",
            "finance",
            "devops",
        ]
        for competence in competences_connues:
            if competence in question:
                competences.append(competence)

        # Chercher aussi dans la base de données des compétences
        with get_database_session() as session:
            all_competences = session.query(Competence).all()
        for competence in all_competences:
            if re.search(rf"\b{re.escape(competence.nom.lower())}\b", question):
                competences.append(competence.nom)

        # Supprimer les doublons
        return list(dict.fromkeys(competences))

    def _extract_languages(self, question: str) -> List[str]:
        """Extrait les langues de la question"""
        langues = []

        # Langues prédéfinies
        langues_connues: List[str] = [
            "français",
            "anglais",
            "espagnol",
            "allemand",
            "italien",
            "portugais",
            "chinois",
            "japonais",
            "arabe",
            "russe",
        ]

        # Chercher d'abord dans les langues prédéfinies
        for langue in langues_connues:
            if langue in question:
                langues.append(langue)

        # Chercher dans la base de données
        with get_database_session() as session:
            all_langues = session.query(Langue).all()
        for langue in all_langues:
            if re.search(rf"\b{re.escape(langue.nom.lower())}\b", question):
                langues.append(langue.nom)

        # Supprimer les doublons
        return list(dict.fromkeys(langues))

    def _extract_amounts(self, question: str) -> List[str]:
        """Extrait les montants de la question"""
        montants_pattern: str = r"(\d+(?:\s*\d{3})*)\s*(?:euros?|€)"
        montants_matches: List[str] = re.findall(montants_pattern, question)
        return [montant.replace(" ", "") for montant in montants_matches]

    def _extract_practices(self, question: str) -> List[str]:
        """Extrait les practices de la question"""
        from database.models import Practice

        practices = []
        with get_database_session() as session:
            all_practices = session.query(Practice).filter(Practice.actif).all()
        for practice in all_practices:
            if re.search(rf"\b{re.escape(practice.nom.lower())}\b", question):
                practices.append(practice.nom)
        return practices

    def _extract_entities(self, question: str) -> Dict[str, List[str]]:
        """Extrait les entités nommées de la question"""
        return {
            "noms": self._extract_consultant_names(question),
            "entreprises": self._extract_companies(question),
            "competences": self._extract_skills(question),
            "langues": self._extract_languages(question),
            "montants": self._extract_amounts(question),
            "practices": self._extract_practices(question),
        }

    def _calculate_cjm(self, salaire: float) -> float:
        """Calcule le CJM (Coût Journalier Moyen) à partir du salaire"""
        return salaire * 1.8 / 216

    def _format_salary_response(self, consultant, is_cjm_question: bool) -> str:
        """Formate la réponse pour un consultant spécifique selon le type de question"""
        if consultant.salaire_actuel and consultant.salaire_actuel > 0:
            if is_cjm_question:
                # Calculer le CJM
                cjm = self._calculate_cjm(consultant.salaire_actuel)
                response = (
                    "📈 Le CJM (Coût Journalier Moyen) de **"
                    + consultant.prenom
                    + " "
                    + consultant.nom
                    + "** est de **"
                    + f"{cjm:,.0f}"
                    + " €**."
                )
                response += f"\n💡 Calcul : {consultant.salaire_actuel:,.0f} € × 1.8 ÷ 216 = {cjm:,.0f} €"
            else:
                response = (
                    "💰 Le salaire de **"
                    + consultant.prenom
                    + " "
                    + consultant.nom
                    + "** est de **"
                    + f"{consultant.salaire_actuel:,.0f}"
                    + " €** par an."
                )

            if not consultant.disponibilite:
                response += "\n⚠️ Attention : ce consultant est actuellement indisponible."
        else:
            if is_cjm_question:
                response = f"❓ Désolé, le CJM de **{consultant.prenom} {consultant.nom}** ne peut pas être calculé car le salaire n'est pas renseigné."
            else:
                response = f"❓ Désolé, le salaire de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."

        return response

    def _handle_consultant_salary_inquiry(self, consultant, is_cjm_question: bool) -> Dict[str, Any]:
        """Gère la réponse pour un consultant spécifique"""
        response = self._format_salary_response(consultant, is_cjm_question)

        return {
            "response": response,
            "data": {
                "consultant": {
                    "nom": consultant.nom,
                    "prenom": consultant.prenom,
                    "salaire": consultant.salaire_actuel,
                    "cjm": (self._calculate_cjm(consultant.salaire_actuel) if consultant.salaire_actuel else None),
                    "disponibilite": consultant.disponibilite,
                }
            },
            "intent": "salaire",
            "confidence": 0.9,
        }

    def _handle_general_salary_stats(self) -> Dict[str, Any]:
        """Gère les statistiques générales de salaire"""
        stats = self._get_salary_stats()
        response = f"""📊 **Statistiques des salaires :**

• Salaire moyen : **{stats['moyenne']:,.0f} €**
• Salaire médian : **{stats['mediane']:,.0f} €**
• Salaire minimum : **{stats['minimum']:,.0f} €**
• Salaire maximum : **{stats['maximum']:,.0f} €**
• Nombre de consultants : **{stats['total']}**"""

        return {
            "response": response,
            "data": {"stats": stats},
            "intent": "salaire",
            "confidence": 0.8,
        }

    def _handle_salary_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les salaires et le CJM"""

        # Détecter si c'est une question sur le CJM
        is_cjm_question = "cjm" in self.last_question.lower() or "coût journalier" in self.last_question.lower()

        # Si un nom est mentionné, chercher ce consultant spécifique
        if entities["noms"]:
            nom_recherche: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom_recherche)

            if consultant:
                return self._handle_consultant_salary_inquiry(consultant, is_cjm_question)
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom_recherche}** dans la base de données.",
                    "data": None,
                    "intent": "salaire",
                    "confidence": 0.7,
                }

        # Sinon, donner des statistiques générales
        else:
            return self._handle_general_salary_stats()

    def _calculate_company_seniority(self, consultant_db) -> float:
        """Calcule l'ancienneté dans la société en années"""
        from datetime import date

        if not consultant_db.date_entree_societe:
            return 0

        today = date.today()
        if consultant_db.date_sortie_societe:
            fin_periode = consultant_db.date_sortie_societe
        else:
            fin_periode = today
        delta_societe = fin_periode - consultant_db.date_entree_societe
        return round(delta_societe.days / 365.25, 1)

    def _format_experience_details(self, consultant, consultant_db) -> str:
        """Formate les détails d'expérience d'un consultant"""
        experience_annees = consultant_db.experience_annees

        response = "📊 **Expérience de " + consultant.prenom + " " + consultant.nom + self.SECTION_HEADER_SUFFIX
        response += f"🚀 **Première mission :** {consultant_db.date_premiere_mission.strftime(self.DATE_FORMAT)}\n"
        response += f"⏱️ **Expérience totale :** **{experience_annees} années**\n"

        # Ajouter des informations contextuelles
        if consultant_db.grade:
            response += f"🎯 **Grade actuel :** {consultant_db.grade}\n"

        if consultant_db.societe:
            response += f"🏢 **Société :** {consultant_db.societe}\n"

        if consultant_db.date_entree_societe:
            response += (
                f"📅 **Date d'entrée société :** {consultant_db.date_entree_societe.strftime(self.DATE_FORMAT)}\n"
            )
            # Calculer l'ancienneté dans la société
            anciennete_societe = self._calculate_company_seniority(consultant_db)
            response += f"🏢 **Ancienneté société :** {anciennete_societe} années\n"

        # Statut société
        statut = consultant_db.statut_societe
        if statut == "En poste":
            response += f"✅ **Statut :** {statut}"
        elif statut == "Départ prévu":
            response += f"⚠️ **Statut :** {statut}"
        else:
            response += f"❌ **Statut :** {statut}"

        return response

    def _build_consultant_experience_data(self, consultant, consultant_db) -> Dict:
        """Construit les données structurées d'expérience d'un consultant"""
        return {
            "nom": consultant.nom,
            "prenom": consultant.prenom,
            "experience_annees": (getattr(consultant_db, "experience_annees", None) if consultant_db else None),
            "date_premiere_mission": (
                consultant_db.date_premiere_mission.isoformat()
                if consultant_db and consultant_db.date_premiere_mission
                else None
            ),
            "grade": (getattr(consultant_db, "grade", None) if consultant_db else None),
            "societe": (getattr(consultant_db, "societe", None) if consultant_db else None),
        }

    def _handle_consultant_experience_inquiry(self, consultant) -> Dict[str, Any]:
        """Gère les questions d'expérience pour un consultant spécifique"""
        try:
            with get_database_session() as session:
                consultant_db = (
                    session.query(Consultant)
                    .options(joinedload(Consultant.langues).joinedload(ConsultantLangue.langue))
                    .filter(Consultant.id == consultant.id)
                    .first()
                )

                if consultant_db:
                    if consultant_db.date_premiere_mission:
                        response = self._format_experience_details(consultant, consultant_db)
                    else:
                        response = f"❓ L'expérience de **{consultant.prenom} {consultant.nom}** ne peut pas être calculée car la date de première mission n'est pas renseignée."
                else:
                    response = f"❌ Impossible de récupérer les données de **{consultant.prenom} {consultant.nom}**."

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            response = f"❌ Erreur lors de la récupération des données d'expérience : {str(e)}"
            consultant_db = None

        return {
            "response": response,
            "data": {"consultant": self._build_consultant_experience_data(consultant, consultant_db)},
            "intent": "experience",
            "confidence": 0.9,
        }

    def _calculate_experience_statistics(self, consultants_avec_experience) -> str:
        """Calcule et formate les statistiques d'expérience générales"""
        experiences = [c.experience_annees for c in consultants_avec_experience]

        response = "📊 **Statistiques d'expérience :**\n\n"
        response += f"• **Consultants avec expérience renseignée :** {len(consultants_avec_experience)}\n"
        response += "• **Expérience moyenne :** " + str(sum(experiences) / len(experiences)) + self.YEARS_SUFFIX
        response += "• **Expérience minimum :** " + str(min(experiences)) + self.YEARS_SUFFIX
        response += "• **Expérience maximum :** " + str(max(experiences)) + self.YEARS_SUFFIX

        # Top 3 des plus expérimentés
        top_experienced = sorted(
            consultants_avec_experience,
            key=lambda c: c.experience_annees,
            reverse=True,
        )[:3]
        response += "\n🏆 **Top 3 des plus expérimentés :**\n"
        for i, consultant in enumerate(top_experienced, 1):
            response += (
                str(i)
                + ". **"
                + consultant.prenom
                + " "
                + consultant.nom
                + "** : "
                + str(consultant.experience_annees)
                + self.YEARS_SUFFIX
            )

        return response

    def _handle_general_experience_stats(self) -> Dict[str, Any]:
        """Gère les statistiques générales d'expérience"""
        try:
            with get_database_session() as session:
                consultants_avec_experience = (
                    session.query(Consultant).filter(Consultant.date_premiere_mission.isnot(None)).all()
                )

                if consultants_avec_experience:
                    response = self._calculate_experience_statistics(consultants_avec_experience)
                else:
                    response = "❓ Aucun consultant n'a d'expérience renseignée dans la base."

        except (
            SQLAlchemyError,
            OSError,
            ValueError,
            TypeError,
            AttributeError,
            KeyError,
        ) as e:
            response = f"❌ Erreur lors du calcul des statistiques : {str(e)}"
            consultants_avec_experience = []

        return {
            "response": response,
            "data": {"consultants_count": len(consultants_avec_experience)},
            "intent": "experience",
            "confidence": 0.8,
        }

    def _handle_experience_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur l'expérience des consultants"""

        # Si un nom est mentionné, chercher ce consultant spécifique
        if entities["noms"]:
            nom_recherche: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom_recherche)

            if consultant:
                return self._handle_consultant_experience_inquiry(consultant)
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom_recherche}** dans la base de données.",
                    "data": None,
                    "intent": "experience",
                    "confidence": 0.7,
                }

        # Statistiques générales sur l'expérience
        else:
            return self._handle_general_experience_stats()

    def _get_profile_response_for_grade(self, consultant, consultant_db):
        """Retourne la réponse pour une question sur le grade"""
        return f"🎯 **Grade de {consultant.prenom} {consultant.nom}** : **{consultant_db.grade or 'Non renseigné'}**"

    def _get_profile_response_for_contract(self, consultant, consultant_db):
        """Retourne la réponse pour une question sur le type de contrat"""
        return f"📋 **Type de contrat de {consultant.prenom} {consultant.nom}** : **{consultant_db.type_contrat or 'Non renseigné'}**"

    def _get_profile_response_for_company(self, consultant, consultant_db):
        """Retourne la réponse pour une question sur la société"""
        response = (
            f"🏢 **Société de {consultant.prenom} {consultant.nom}** : **{consultant_db.societe or 'Non renseigné'}**"
        )
        if consultant_db.date_entree_societe:
            response += f"\n📅 **Date d'entrée :** {consultant_db.date_entree_societe.strftime(self.DATE_FORMAT)}"
        if consultant_db.date_sortie_societe:
            response += f"\n📅 **Date de sortie :** {consultant_db.date_sortie_societe.strftime(self.DATE_FORMAT)}"
        else:
            response += "\n✅ **Toujours en poste**"
        return response

    def _get_complete_profile_response(self, consultant, consultant_db):
        """Retourne le profil professionnel complet"""
        response = f"👔 **Profil professionnel de {consultant.prenom} {consultant.nom}{self.SECTION_HEADER_SUFFIX}"
        response += f"🎯 **Grade :** {consultant_db.grade or 'Non renseigné'}\n"
        response += f"📋 **Type de contrat :** {consultant_db.type_contrat or 'Non renseigné'}\n"
        response += f"🏢 **Société :** {consultant_db.societe or 'Non renseigné'}\n"

        if consultant_db.date_entree_societe:
            response += (
                f"📅 **Date d'entrée société :** {consultant_db.date_entree_societe.strftime(self.DATE_FORMAT)}\n"
            )

        if consultant_db.date_sortie_societe:
            response += (
                f"📅 **Date de sortie société :** {consultant_db.date_sortie_societe.strftime(self.DATE_FORMAT)}\n"
            )
        else:
            response += "✅ **Statut :** Toujours en poste\n"

        if consultant_db.experience_annees:
            response += f"⏱️ **Expérience :** {consultant_db.experience_annees}{self.YEARS_SUFFIX}"

        # Informations salariales si disponibles
        if consultant_db.salaire_actuel:
            cjm = consultant_db.salaire_actuel * 1.8 / 216
            response += f"💰 **Salaire :** {consultant_db.salaire_actuel:,.0f} €/an\n"
            response += f"📈 **CJM :** {cjm:,.0f} €/jour"

        return response

    def _handle_individual_profile_question(self, entities: Dict, question_lower: str) -> Dict[str, Any]:
        """Gère les questions de profil pour un consultant spécifique"""
        nom_recherche: str = entities["noms"][0]
        consultant = self._find_consultant_by_name(nom_recherche)

        if not consultant:
            return {
                "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom_recherche}** dans la base de données.",
                "data": None,
                "intent": "profil_professionnel",
                "confidence": 0.7,
            }

        try:
            with get_database_session() as session:
                consultant_db = session.query(Consultant).filter(Consultant.id == consultant.id).first()

                if not consultant_db:
                    response = f"❌ Impossible de récupérer les données de **{consultant.prenom} {consultant.nom}**."
                else:
                    # Déterminer le type d'information demandée
                    if any(word in question_lower for word in ["grade", "niveau", "poste", "fonction"]):
                        response = self._get_profile_response_for_grade(consultant, consultant_db)
                    elif any(word in question_lower for word in ["contrat", "type contrat", "cdi", "cdd"]):
                        response = self._get_profile_response_for_contract(consultant, consultant_db)
                    elif any(
                        word in question_lower
                        for word in [
                            "société",
                            "societe",
                            "entreprise",
                            "quanteam",
                            "asigma",
                        ]
                    ):
                        response = self._get_profile_response_for_company(consultant, consultant_db)
                    else:
                        response = self._get_complete_profile_response(consultant, consultant_db)

        except (SQLAlchemyError, AttributeError, ValueError, TypeError) as e:
            response = f"❌ Erreur lors de la récupération du profil : {str(e)}"
            consultant_db = None

        return {
            "response": response,
            "data": {
                "consultant": {
                    "nom": consultant.nom,
                    "prenom": consultant.prenom,
                    "grade": (getattr(consultant_db, "grade", None) if consultant_db else None),
                    "type_contrat": (getattr(consultant_db, "type_contrat", None) if consultant_db else None),
                    "societe": (getattr(consultant_db, "societe", None) if consultant_db else None),
                }
            },
            "intent": "profil_professionnel",
            "confidence": 0.9,
        }

    def _group_consultants_by_grade(self, consultants) -> Dict[str, List]:
        """Groupe les consultants par grade"""
        grades_count: Dict[str, List[Consultant]] = {}
        for consultant in consultants:
            grade = consultant.grade
            if grade not in grades_count:
                grades_count[grade] = []
            grades_count[grade].append(consultant)
        return grades_count

    def _handle_grade_statistics(self, session) -> str:
        """Gère les statistiques par grade"""
        consultants = session.query(Consultant).filter(Consultant.grade.isnot(None)).all()

        if consultants:
            grades_count = self._group_consultants_by_grade(consultants)

            response = "🎯 **Répartition par grade :**\n\n"
            for grade, consultants_list in grades_count.items():
                response += f"• **{grade}** : {len(consultants_list)} consultant(s)\n"
                if len(consultants_list) <= 5:  # Afficher les noms si pas trop nombreux
                    for c in consultants_list:
                        response += f"  - {c.prenom} {c.nom}\n"
        else:
            response = "❓ Aucun consultant n'a de grade renseigné."

        return response

    def _count_consultants_by_contract_type(self, consultants, contract_type: str) -> int:
        """Compte les consultants d'un type de contrat spécifique"""
        if contract_type.upper() == "CDI":
            return len([c for c in consultants if c.type_contrat and c.type_contrat.upper() == "CDI"])
        elif contract_type.upper() == "CDD":
            return len([c for c in consultants if c.type_contrat and c.type_contrat.upper() == "CDD"])
        elif contract_type.lower() == "stagiaire":
            return len([c for c in consultants if c.type_contrat and c.type_contrat.lower() == "stagiaire"])
        return 0

    def _handle_contract_count_query(self, consultants, question_lower: str) -> str:
        """Gère les questions de comptage de consultants par contrat"""
        if "cdi" in question_lower:
            count = self._count_consultants_by_contract_type(consultants, "CDI")
            return f"📋 **{count} consultant(s) en CDI**"
        elif "cdd" in question_lower:
            count = self._count_consultants_by_contract_type(consultants, "CDD")
            return f"📋 **{count} consultant(s) en CDD**"
        elif "stagiaire" in question_lower:
            count = self._count_consultants_by_contract_type(consultants, "stagiaire")
            return f"📋 **{count} consultant(s) stagiaire(s)**"
        else:
            return self._get_all_contract_counts(consultants)

    def _get_all_contract_counts(self, consultants) -> str:
        """Retourne toutes les statistiques de contrats"""
        contrats_count: Dict[str, int] = {}
        for consultant in consultants:
            contrat = consultant.type_contrat
            if contrat not in contrats_count:
                contrats_count[contrat] = 0
            contrats_count[contrat] += 1

        response = "📋 **Nombre de consultants par type de contrat :**\n\n"
        for contrat, count in contrats_count.items():
            response += f"• **{contrat}** : {count} consultant(s)\n"
        return response

    def _get_contract_detailed_breakdown(self, consultants) -> str:
        """Retourne la répartition détaillée par type de contrat"""
        contrats_list: Dict[str, List[Consultant]] = {}
        for consultant in consultants:
            contrat = consultant.type_contrat
            if contrat not in contrats_list:
                contrats_list[contrat] = []
            contrats_list[contrat].append(consultant)

        response = "📋 **Répartition par type de contrat :**\n\n"
        for contrat, consultants_list in contrats_list.items():
            response += f"• **{contrat}** : {len(consultants_list)} consultant(s)\n"
            if len(consultants_list) <= 5:  # Afficher les noms si pas trop nombreux
                for c in consultants_list:
                    response += f"  - {c.prenom} {c.nom}\n"
        return response

    def _handle_contract_statistics(self, session, question_lower: str) -> str:
        """Gère les statistiques par type de contrat"""
        consultants = session.query(Consultant).filter(Consultant.type_contrat.isnot(None)).all()

        # Si c'est une question "combien de consultants en CDI/CDD"
        if any(word in question_lower for word in ["combien"]):
            return self._handle_contract_count_query(consultants, question_lower)
        else:
            # Répartition complète par type de contrat
            if consultants:
                return self._get_contract_detailed_breakdown(consultants)
            else:
                return "❓ Aucun consultant n'a de type de contrat renseigné."

    def _handle_company_statistics(self, session, question_lower: str) -> str:
        """Gère les statistiques par société"""
        consultants = self._get_consultants_with_company(session)

        if self._is_specific_company_search(question_lower):
            return self._handle_specific_company_search(consultants, question_lower)
        else:
            return self._handle_general_company_statistics(consultants)

    def _get_consultants_with_company(self, session) -> List:
        """Récupère tous les consultants ayant une société renseignée"""
        return session.query(Consultant).filter(Consultant.societe.isnot(None)).all()

    def _is_specific_company_search(self, question_lower: str) -> bool:
        """Vérifie si la question concerne une société spécifique"""
        return any(word in question_lower for word in ["quanteam", "asigma"])

    def _handle_specific_company_search(self, consultants: List, question_lower: str) -> str:
        """Gère la recherche pour une société spécifique"""
        societe_recherchee = self._extract_target_company(question_lower)
        consultants_societe = self._filter_consultants_by_company(consultants, societe_recherchee)

        if consultants_societe:
            return self._format_specific_company_response(consultants_societe, societe_recherchee)
        else:
            return f"❓ Aucun consultant trouvé chez {societe_recherchee}."

    def _extract_target_company(self, question_lower: str) -> str:
        """Extrait le nom de la société recherchée"""
        return "Quanteam" if "quanteam" in question_lower else "Asigma"

    def _filter_consultants_by_company(self, consultants: List, target_company: str) -> List:
        """Filtre les consultants par société"""
        return [c for c in consultants if c.societe and c.societe.lower() == target_company.lower()]

    def _format_specific_company_response(self, consultants_societe: List, societe_recherchee: str) -> str:
        """Formate la réponse pour une société spécifique"""
        response = f"🏢 **Consultants chez {societe_recherchee}** :\n\n"

        for i, consultant in enumerate(consultants_societe, 1):
            response += self._format_consultant_company_line(consultant, i)

        response += self.TOTAL_PREFIX + str(len(consultants_societe)) + self.CONSULTANT_FOUND_SUFFIX
        return response

    def _format_consultant_company_line(self, consultant, index: int) -> str:
        """Formate une ligne consultant pour l'affichage par société"""
        status_icon = "🟢" if consultant.disponibilite else "🔴"
        line = f"{index}. {status_icon} **{consultant.prenom} {consultant.nom}**"

        if consultant.grade:
            line += f" - {consultant.grade}"
        if consultant.type_contrat:
            line += f" ({consultant.type_contrat})"
        line += "\n"

        return line

    def _handle_general_company_statistics(self, consultants: List) -> str:
        """Gère les statistiques générales par société"""
        if not consultants:
            return "❓ Aucun consultant n'a de société renseignée."

        societes_count = self._group_consultants_by_company(consultants)
        return self._format_general_company_statistics(societes_count)

    def _group_consultants_by_company(self, consultants: List) -> Dict[str, List]:
        """Groupe les consultants par société"""
        societes_count: Dict[str, List[Consultant]] = {}
        for consultant in consultants:
            societe = consultant.societe
            if societe not in societes_count:
                societes_count[societe] = []
            societes_count[societe].append(consultant)
        return societes_count

    def _format_general_company_statistics(self, societes_count: Dict[str, List]) -> str:
        """Formate les statistiques générales par société"""
        response = "🏢 **Répartition par société :**\n\n"

        for societe, consultants_list in societes_count.items():
            response += f"• **{societe}** : {len(consultants_list)} consultant(s)\n"
            if len(consultants_list) <= 5:  # Afficher les noms si pas trop nombreux
                response += self._format_company_consultant_details(consultants_list)

        return response

    def _format_company_consultant_details(self, consultants_list: List) -> str:
        """Formate les détails des consultants pour une société"""
        details = ""
        for c in consultants_list:
            details += f"  - {c.prenom} {c.nom}\n"
        return details

    def _handle_professional_profile_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur le profil professionnel (grade, type contrat, société)"""
        question_lower: str = self.last_question.lower()

        # Si un nom est mentionné, chercher ce consultant spécifique
        if entities["noms"]:
            return self._handle_individual_profile_question(entities, question_lower)

        # Questions générales par critère
        else:
            try:
                with get_database_session() as session:
                    if any(
                        word in question_lower
                        for word in [
                            "grade",
                            "niveau",
                            "junior",
                            "confirmé",
                            "manager",
                            "directeur",
                        ]
                    ):
                        response = self._handle_grade_statistics(session)
                    elif any(word in question_lower for word in ["contrat", "cdi", "cdd", "stagiaire"]):
                        response = self._handle_contract_statistics(session, question_lower)
                    elif any(
                        word in question_lower
                        for word in [
                            "société",
                            "societe",
                            "quanteam",
                            "asigma",
                            "qui travaille",
                            "qui est",
                        ]
                    ):
                        response = self._handle_company_statistics(session, question_lower)
                    else:
                        response = "🤔 Précisez quel aspect du profil professionnel vous intéresse : grade, type de contrat, ou société ?"

            except (
                SQLAlchemyError,
                AttributeError,
                ValueError,
                TypeError,
                KeyError,
            ) as e:
                response = f"❌ Erreur lors de la récupération des données : {str(e)}"

            return {
                "response": response,
                "data": None,
                "intent": "profil_professionnel",
                "confidence": 0.8,
            }

    def _detect_skill_type(self, question_lower: str) -> Optional[str]:
        """Détecte le type de compétence demandé dans la question"""
        if any(
            word in question_lower
            for word in [
                "compétences techniques",
                "technique",
                "technologie",
                "programmation",
            ]
        ):
            return "technique"
        elif any(
            word in question_lower
            for word in [
                "compétences fonctionnelles",
                "fonctionnelle",
                "métier",
                "bancaire",
                "finance",
            ]
        ):
            return "fonctionnelle"
        return None

    def _extract_skill_from_question(self, question_lower: str) -> Optional[str]:
        """Extrait le nom de la compétence d'une question 'qui maîtrise'"""
        patterns = [
            r"qui\s+maîtrise\s+(.+?)(?:\?|$)",
            r"qui\s+sait\s+(.+?)(?:\?|$)",
            r"qui\s+connaît\s+(.+?)(?:\?|$)",
            r"qui\s+connait\s+(.+?)(?:\?|$)",
            r"qui\s+a\s+(.+?)(?:\?|$)",
            r"qui\s+possède\s+(.+?)(?:\?|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, question_lower)
            if match:
                competence_found = match.group(1).strip()
                # Nettoyer les articles et prépositions (protection ReDoS avec limites strictes)
                # Limite la longueur de la chaîne pour éviter le backtracking excessif
                if len(competence_found) <= 100:  # Protection ReDoS
                    competence_found = re.sub(r"^(?:le|la|les|du|de|des|en|une?)\s+", "", competence_found, count=1)
                    competence_found = re.sub(r"\s+(?:compétence|skill)s?\Z", "", competence_found, count=1)
                return competence_found
        return None

    def _handle_specific_skill_search(self, competence: str, type_competence: Optional[str]) -> Dict[str, Any]:
        """Gère la recherche de consultants ayant une compétence spécifique"""
        consultants = self._find_consultants_by_skill(competence, type_competence)

        if consultants:
            noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
            response = f"🎯 Consultants maîtrisant **{competence.title()}** :\n\n"
            response += "\n".join([f"• {nom}" for nom in noms])
            response += self.STATS_PREFIX + str(len(consultants)) + self.CONSULTANT_FOUND_SUFFIX
        else:
            response = f"❌ Aucun consultant ne maîtrise **{competence}** dans notre base."

        return {
            "response": response,
            "data": {"consultants": [{"nom": c.nom, "prenom": c.prenom} for c in consultants]},
            "intent": "competences",
            "confidence": 0.9,
        }

    def _handle_consultant_skills_inquiry(self, nom: str, type_competence: Optional[str]) -> Dict[str, Any]:
        """Gère les questions sur les compétences d'un consultant spécifique"""
        consultant = self._find_consultant_by_name(nom)

        if not consultant:
            return self._format_consultant_not_found_response(nom)

        skills = self._get_consultant_skills(consultant.id, type_competence)

        if not skills:
            return self._format_no_skills_response(consultant)

        response = self._format_consultant_skills_response(consultant, skills)

        return {
            "response": response,
            "data": {
                "consultant": consultant.nom,
                "skills_count": len(skills),
            },
            "intent": "competences",
            "confidence": 0.9,
        }

    def _format_consultant_not_found_response(self, nom: str) -> Dict[str, Any]:
        """Formate la réponse quand le consultant n'est pas trouvé"""
        return {
            "response": f"❌ Consultant **{nom}** introuvable.",
            "data": {
                "consultant": None,
                "skills_count": 0,
            },
            "intent": "competences",
            "confidence": 0.9,
        }

    def _format_no_skills_response(self, consultant) -> Dict[str, Any]:
        """Formate la réponse quand aucune compétence n'est trouvée"""
        return {
            "response": f"❌ Aucune compétence enregistrée pour **{consultant.prenom} {consultant.nom}**.",
            "data": {
                "consultant": consultant.nom,
                "skills_count": 0,
            },
            "intent": "competences",
            "confidence": 0.9,
        }

    def _format_consultant_skills_response(self, consultant, skills: List) -> str:
        """Formate la réponse complète des compétences d'un consultant"""
        response = f"🎯 **Compétences de {consultant.prenom} {consultant.nom} :**\n\n"

        categories = self._group_skills_by_category(skills)
        response += self._format_skills_by_category(categories)
        response += f"📊 **Total : {len(skills)} compétence(s)**"

        return response

    def _group_skills_by_category(self, skills: List) -> Dict[str, List[Dict[str, Any]]]:
        """Groupe les compétences par catégorie"""
        categories: Dict[str, List[Dict[str, Any]]] = {}
        for skill in skills:
            categorie = skill["categorie"] or "Autre"
            if categorie not in categories:
                categories[categorie] = []
            categories[categorie].append(skill)
        return categories

    def _format_skills_by_category(self, categories: Dict[str, List[Dict[str, Any]]]) -> str:
        """Formate l'affichage des compétences par catégorie"""
        response = ""
        for categorie, competences in categories.items():
            response += f"**🔹 {categorie.title()} :**\n"
            response += self._format_category_skills(competences)
            response += "\n"
        return response

    def _format_category_skills(self, competences: List[Dict[str, Any]]) -> str:
        """Formate les compétences d'une catégorie"""
        formatted = ""
        for comp in competences:
            niveau_emoji = self._get_skill_level_emoji(comp["niveau_maitrise"])
            experience_text = self._format_experience_text(comp["annees_experience"])
            formatted += f"  {niveau_emoji} **{comp['nom']}** - {comp['niveau_maitrise'].title()}{experience_text}\n"
        return formatted

    def _get_skill_level_emoji(self, niveau_maitrise: str) -> str:
        """Retourne l'emoji correspondant au niveau de maîtrise"""
        return {
            "debutant": "🟡",
            "intermediaire": "🟠",
            "expert": "🔴",
        }.get(niveau_maitrise, "⚪")

    def _format_experience_text(self, annees_experience: Optional[float]) -> str:
        """Formate le texte d'expérience en années"""
        if not annees_experience or annees_experience <= 0:
            return ""

        if annees_experience == 1:
            return f" ({annees_experience} an)"
        else:
            return f" ({annees_experience:.0f} ans)"

    def _handle_skills_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les compétences"""

        # Détecter le type de compétences demandé
        question_lower: str = self.last_question.lower()
        type_competence = self._detect_skill_type(question_lower)

        # Si une compétence spécifique est mentionnée
        if entities["competences"]:
            return self._handle_specific_skill_search(entities["competences"][0], type_competence)

        # Recherche dynamique de compétence dans la question
        elif any(word in question_lower for word in ["qui maîtrise", "qui sait", "qui connaît", "qui connait"]):
            competence_found = self._extract_skill_from_question(question_lower)

            if competence_found:
                return self._handle_specific_skill_search(competence_found, type_competence)

        # Question générale sur les compétences d'un consultant
        elif entities["noms"]:
            return self._handle_consultant_skills_inquiry(entities["noms"][0], type_competence)

        return {
            "response": "🤔 Pouvez-vous préciser quelle compétence ou quel consultant vous intéresse ?",
            "data": None,
            "intent": "competences",
            "confidence": 0.5,
        }

    def _extract_consultant_name_from_language_question(self, question_lower: str) -> Optional[str]:
        """Extrait le nom du consultant d'une question sur les langues"""
        patterns = [
            r"quelles?\s+langues?\s+parle\s+(\w+)",
            r"langues?\s+parle\s+(\w+)",
            r"langues?\s+de\s+(\w+)",
            r"(\w+)\s+parle\s+quelles?\s+langues?",
            r"quelles?\s+sont\s+les\s+langues?\s+de\s+(\w+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, question_lower)
            if match:
                return match.group(1)
        return None

    def _extract_language_from_question(self, question_lower: str) -> Optional[str]:
        """Extrait le nom de la langue d'une question 'qui parle'"""
        patterns = [
            r"qui\s+parle\s+(.+?)(?:\?|$)",
            r"parlent\s+(.+?)(?:\?|$)",
            r"qui\s+(?:\w+\s+)*parle\s+(?:\w+\s+)*(.+?)(?:\?|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, question_lower)
            if match:
                langue_found = match.group(1).strip()
                # Nettoyer les articles
                langue_found = re.sub(r"^(le|la|les|du|de|des|en|une?)\s+", "", langue_found)
                return langue_found
        return None

    def _format_consultant_languages_response(self, consultant) -> str:
        """Formate la réponse pour les langues d'un consultant"""
        if not consultant.langues:
            return f"❌ Aucune langue enregistrée pour **{consultant.prenom} {consultant.nom}**."

        response = "🌍 **Langues parlées par " + consultant.prenom + " " + consultant.nom + " :**\n\n"

        flag_emoji = {
            "FR": "🇫🇷",
            "EN": "🇬🇧",
            "ES": "🇪🇸",
            "DE": "🇩🇪",
            "IT": "🇮🇹",
            "PT": "🇵🇹",
            "NL": "🇳🇱",
            "RU": "🇷🇺",
            "ZH": "🇨🇳",
            "JA": "🇯🇵",
            "AR": "🇸🇦",
            "HI": "🇮�",
        }

        for cl in consultant.langues:
            emoji = flag_emoji.get(cl.langue.code_iso, "🌍")
            response += f"  {emoji} **{cl.langue.nom}** - {cl.niveau_label}"
            if cl.commentaire:
                response += f" - {cl.commentaire}"
            response += "\n"

        response += f"\n📊 **Total : {len(consultant.langues)} langue(s)**"
        return response

    def _handle_specific_language_search(self, langue_recherchee: str) -> Dict[str, Any]:
        """Gère la recherche de consultants parlant une langue spécifique"""
        consultants = self._find_consultants_by_language(langue_recherchee)

        if not consultants:
            return self._format_no_language_speakers_response(langue_recherchee)

        response = self._format_language_speakers_response(consultants, langue_recherchee)

        return {
            "response": response,
            "data": {"consultants": [{"nom": c.nom, "prenom": c.prenom} for c in consultants]},
            "intent": "langues",
            "confidence": 0.9,
        }

    def _format_no_language_speakers_response(self, langue_recherchee: str) -> Dict[str, Any]:
        """Formate la réponse quand aucun consultant ne parle la langue"""
        return {
            "response": f"❌ Aucun consultant ne parle **{langue_recherchee}** dans notre base.",
            "data": {"consultants": []},
            "intent": "langues",
            "confidence": 0.8,
        }

    def _format_language_speakers_response(self, consultants: List, langue_recherchee: str) -> str:
        """Formate la réponse complète des consultants parlant une langue"""
        response = self._format_language_speakers_list(consultants, langue_recherchee)

        if len(consultants) <= 5:
            response += self._format_language_levels_details(consultants, langue_recherchee)

        return response

    def _format_language_speakers_list(self, consultants: List, langue_recherchee: str) -> str:
        """Formate la liste de base des consultants parlant une langue"""
        noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
        response = f"🌍 Consultants parlant **{langue_recherchee.title()}** :\n\n"
        response += "\n".join([f"• {nom}" for nom in noms])
        response += f"\n\n📊 **{len(consultants)} consultant(s) trouvé(s)**"
        return response

    def _format_language_levels_details(self, consultants: List, langue_recherchee: str) -> str:
        """Formate les détails de niveaux pour une langue spécifique"""
        details = "\n\n🎯 **Niveaux détaillés :**"

        for consultant in consultants:
            level_info = self._get_consultant_language_level(consultant, langue_recherchee)
            if level_info:
                details += f"\n  • **{consultant.prenom} {consultant.nom}** : {level_info['niveau']}"
                if level_info["commentaire"]:
                    details += f" - {level_info['commentaire']}"

        return details

    def _get_consultant_language_level(self, consultant, langue_recherchee: str) -> Optional[Dict[str, str]]:
        """Récupère le niveau et commentaire d'un consultant pour une langue"""
        for cl in consultant.langues:
            if cl.langue.nom.lower() == langue_recherchee.lower():
                return {"niveau": cl.niveau_label, "commentaire": cl.commentaire}
        return None

    def _handle_consultant_languages_inquiry(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les langues d'un consultant spécifique"""
        question_lower = self.last_question.lower()

        # Si pas de nom détecté dans entities, essayer d'extraire manuellement
        nom = (
            entities["noms"][0]
            if entities["noms"]
            else self._extract_consultant_name_from_language_question(question_lower)
        )

        if nom:
            consultant = self._find_consultant_by_name(nom)

            if consultant:
                response = self._format_consultant_languages_response(consultant)
                return {
                    "response": response,
                    "data": {
                        "consultant": consultant.nom,
                        "languages_count": (len(consultant.langues) if consultant.langues else 0),
                    },
                    "intent": "langues",
                    "confidence": 0.8,
                }
            else:
                return {
                    "response": f"❌ Consultant **{nom}** introuvable.",
                    "data": {"consultant": None, "languages_count": 0},
                    "intent": "langues",
                    "confidence": 0.8,
                }
        else:
            # Question générale sur les langues sans nom spécifique
            return {
                "response": '🌍 Pour connaître les langues d\'un consultant, demandez : "Quelles langues parle [nom] ?"\n\nOu pour trouver qui parle une langue : "Qui parle anglais ?"',
                "data": {},
                "intent": "langues",
                "confidence": 0.6,
            }

    def _handle_languages_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les langues parlées par les consultants"""

        # Si une langue spécifique est mentionnée
        if entities["langues"]:
            return self._handle_specific_language_search(entities["langues"][0])

        # Question générale sur les langues d'un consultant
        elif entities["noms"] or any(
            word in self.last_question.lower() for word in ["quelles langues", "langues de", "langues parlées"]
        ):
            return self._handle_consultant_languages_inquiry(entities)

        # Recherche dynamique de langue dans la question
        elif any(word in self.last_question.lower() for word in ["qui parle", "parle", "parlent", "bilingue"]):
            question_lower = self.last_question.lower()
            langue_found = self._extract_language_from_question(question_lower)

            if langue_found:
                return self._handle_specific_language_search(langue_found)

        # Question générale sur les langues
        return {
            "response": '🌍 Pour connaître les langues d\'un consultant, demandez : "Quelles langues parle [nom] ?"\n\nOu pour trouver qui parle une langue : "Qui parle anglais ?"',
            "data": {},
            "intent": "langues",
            "confidence": 0.6,
        }

    def _handle_missions_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les missions"""
        question_lower: str = self.last_question.lower()
        is_count_question = self._is_count_question(question_lower)

        if entities["entreprises"]:
            return self._handle_company_missions_inquiry(entities["entreprises"][0], is_count_question)
        elif entities["noms"]:
            return self._handle_consultant_missions_inquiry(entities["noms"][0], is_count_question)
        else:
            return self._handle_generic_missions_question()

    def _is_count_question(self, question_lower: str) -> bool:
        """Détermine si c'est une question de comptage"""
        return any(word in question_lower for word in ["combien", "nombre"])

    def _handle_company_missions_inquiry(self, entreprise: str, is_count_question: bool) -> Dict[str, Any]:
        """Gère les questions sur les missions d'une entreprise"""
        missions = self._get_missions_by_company(entreprise)

        if is_count_question:
            response = self._format_company_missions_count(missions, entreprise)
        elif missions:
            response = self._format_company_missions_list(missions, entreprise)
        else:
            response = f"❌ Aucune mission trouvée chez **{entreprise}**."

        return {
            "response": response,
            "data": {"missions": len(missions), "entreprise": entreprise},
            "intent": "missions",
            "confidence": 0.9,
        }

    def _format_company_missions_count(self, missions: List, entreprise: str) -> str:
        """Formate le comptage des missions pour une entreprise"""
        return "📊 **" + str(len(missions)) + " mission(s)** trouvée(s) chez **" + entreprise.title() + "**"

    def _format_company_missions_list(self, missions: List, entreprise: str) -> str:
        """Formate la liste des missions pour une entreprise"""
        response = f"🏢 **Missions chez {entreprise.title()} :**\n\n"

        for mission in missions[:5]:  # Limiter à 5 résultats
            consultant_nom = f"{mission.consultant.prenom} {mission.consultant.nom}"
            response += f"• **{consultant_nom}** - {mission.nom_mission} ({mission.date_debut.strftime('%Y')})\n"

        if len(missions) > 5:
            response += f"\n... et {len(missions) - 5} autres missions"

        response += "\n\n📊 **Total : " + str(len(missions)) + " mission(s)**"
        return response

    def _handle_consultant_missions_inquiry(self, nom: str, is_count_question: bool) -> Dict[str, Any]:
        """Gère les questions sur les missions d'un consultant"""
        consultant = self._find_consultant_by_name(nom)

        if not consultant:
            return self._format_consultant_not_found_missions_response(nom)

        missions = self._get_missions_by_consultant(consultant.id)

        if is_count_question:
            response = self._format_consultant_missions_count(consultant, missions)
        elif missions:
            response = self._format_consultant_missions_list(consultant, missions)
        else:
            response = f"❌ Aucune mission trouvée pour **{consultant.prenom} {consultant.nom}**."

        return {
            "response": response,
            "data": {
                "consultant": nom,
                "missions_count": len(missions),
            },
            "intent": "missions",
            "confidence": 0.9,
        }

    def _format_consultant_not_found_missions_response(self, nom: str) -> Dict[str, Any]:
        """Formate la réponse quand le consultant n'est pas trouvé"""
        return {
            "response": f"❌ Consultant **{nom}** introuvable.",
            "data": {
                "consultant": nom,
                "missions_count": 0,
            },
            "intent": "missions",
            "confidence": 0.9,
        }

    def _format_consultant_missions_count(self, consultant, missions: List) -> str:
        """Formate le comptage des missions pour un consultant"""
        response = (
            "📊 **"
            + consultant.prenom
            + " "
            + consultant.nom
            + "** a **"
            + str(len(missions))
            + " mission(s)** dans la base"
        )

        if missions:
            missions_en_cours = [m for m in missions if m.statut == "en_cours"]
            if missions_en_cours:
                response += " (dont " + str(len(missions_en_cours)) + " en cours)"

        return response

    def _format_consultant_missions_list(self, consultant, missions: List) -> str:
        """Formate la liste détaillée des missions pour un consultant"""
        response = f"💼 **Missions de {consultant.prenom} {consultant.nom} :**\n\n"

        for mission in missions:
            response += self._format_mission_details(mission)

        response += "📊 **Total : " + str(len(missions)) + " mission(s)**"
        return response

    def _format_mission_details(self, mission) -> str:
        """Formate les détails d'une mission"""
        status_icon = "🟢" if mission.statut == "en_cours" else "✅"
        details = f"{status_icon} **{mission.client}** - {mission.nom_mission}\n"
        details += f"   📅 {mission.date_debut.strftime('%m/%Y')} → "

        if mission.date_fin:
            details += f"{mission.date_fin.strftime('%m/%Y')}"
        else:
            details += "En cours"

        if mission.taux_journalier:
            details += " | 💰 " + str(mission.taux_journalier) + "€/jour"

        details += "\n\n"
        return details

    def _handle_generic_missions_question(self) -> Dict[str, Any]:
        """Gère les questions génériques sur les missions"""
        return {
            "response": "🤔 Voulez-vous connaître les missions d'un consultant ou d'une entreprise spécifique ?",
            "data": None,
            "intent": "missions",
            "confidence": 0.5,
        }

    def _handle_stats_question(self) -> Dict[str, Any]:
        """Gère les questions statistiques"""

        stats = self._get_general_stats()

        # Si c'est une question spécifique sur le nombre de consultants
        if any(pattern in self.last_question for pattern in ["combien", "nombre"]):
            if "consultant" in self.last_question and "mission" not in self.last_question:
                response = f"👥 **Vous avez {stats['consultants_total']} consultants** dans votre base de données.\n\n"
                response += (
                    "📊 Détail : "
                    + str(stats["consultants_actifs"])
                    + " disponibles, "
                    + str(stats["consultants_inactifs"])
                    + " indisponibles"
                )

                return {
                    "response": response,
                    "data": {"consultants_count": stats["consultants_total"]},
                    "intent": "statistiques",
                    "confidence": 0.95,
                }

        # Statistiques complètes par défaut
        response = f"""📊 **Statistiques générales :**

👥 **Consultants :**
• Total : **{stats['consultants_total']}**
• Actifs : **{stats['consultants_actifs']}**
• Inactifs : **{stats['consultants_inactifs']}**

🏢 **Practices :**
• Total : **{stats['practices_total']}**

💼 **Missions :**
• Total : **{stats['missions_total']}**
• En cours : **{stats['missions_en_cours']}**
• Terminées : **{stats['missions_terminees']}**

� **Documents :**
• Total CVs : **{stats['cvs_total']}**
• Consultants avec CV : **{stats['consultants_avec_cv']}**

�💰 **Financier :**
• TJM moyen : **{stats['tjm_moyen']:,.0f} €**
• Salaire moyen : **{stats['salaire_moyen']:,.0f} €**
• CJM moyen : **{stats['cjm_moyen']:,.0f} €**"""

        return {
            "response": response,
            "data": {"stats": stats},
            "intent": "statistiques",
            "confidence": 0.9,
        }

    def _handle_contact_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les contacts (email, téléphone)"""

        if not entities["noms"]:
            return self._handle_generic_contact_question()

        nom: str = entities["noms"][0]
        consultant = self._find_consultant_by_name(nom)

        if not consultant:
            return self._handle_consultant_not_found_contact(nom)

        question_lower: str = self.last_question.lower()

        if self._is_email_question(question_lower):
            return self._handle_email_request(consultant)
        elif self._is_phone_question(question_lower):
            return self._handle_phone_request(consultant)
        else:
            return self._handle_complete_contact_request(consultant)

    def _handle_generic_contact_question(self) -> Dict[str, Any]:
        """Gère les questions de contact génériques sans nom spécifique"""
        return {
            "response": "🤔 De quel consultant souhaitez-vous connaître les coordonnées ?",
            "data": None,
            "intent": "contact",
            "confidence": 0.5,
        }

    def _handle_consultant_not_found_contact(self, nom: str) -> Dict[str, Any]:
        """Gère le cas où le consultant n'est pas trouvé pour une question de contact"""
        return {
            "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom}** dans la base de données.",
            "data": None,
            "intent": "contact",
            "confidence": 0.7,
        }

    def _is_email_question(self, question_lower: str) -> bool:
        """Détermine si la question concerne l'email"""
        return any(word in question_lower for word in ["mail", "email", "e-mail"])

    def _is_phone_question(self, question_lower: str) -> bool:
        """Détermine si la question concerne le téléphone"""
        return any(word in question_lower for word in ["téléphone", "tel", "numéro"])

    def _handle_email_request(self, consultant) -> Dict[str, Any]:
        """Gère les demandes spécifiques d'email"""
        if consultant.email:
            response = f"� L'email de **{consultant.prenom} {consultant.nom}** est : **{consultant.email}**"
        else:
            response = (
                f"❓ Désolé, l'email de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."
            )

        return {
            "response": response,
            "data": {
                "consultant": consultant.nom,
                "email": consultant.email,
                "telephone": consultant.telephone,
            },
            "intent": "contact",
            "confidence": 0.9,
        }

    def _handle_phone_request(self, consultant) -> Dict[str, Any]:
        """Gère les demandes spécifiques de téléphone"""
        if consultant.telephone:
            response = f"📞 Le téléphone de **{consultant.prenom} {consultant.nom}** est : **{consultant.telephone}**"
        else:
            response = (
                f"❓ Désolé, le téléphone de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."
            )

        return {
            "response": response,
            "data": {
                "consultant": consultant.nom,
                "email": consultant.email,
                "telephone": consultant.telephone,
            },
            "intent": "contact",
            "confidence": 0.9,
        }

    def _handle_complete_contact_request(self, consultant) -> Dict[str, Any]:
        """Gère les demandes de contact complet"""
        response = f"📞 **Contact de {consultant.prenom} {consultant.nom} :**\n\n"
        response += f"📧 Email : **{consultant.email or 'Non renseigné'}**\n"
        response += f"📞 Téléphone : **{consultant.telephone or 'Non renseigné'}**"

        return {
            "response": response,
            "data": {
                "consultant": consultant.nom,
                "email": consultant.email,
                "telephone": consultant.telephone,
            },
            "intent": "contact",
            "confidence": 0.9,
        }

    def _handle_list_consultants_question(self) -> Dict[str, Any]:
        """Gère les questions pour lister les consultants selon des critères"""
        question_lower: str = self.last_question.lower()

        consultants, titre = self._get_consultants_by_criteria(question_lower)

        if not consultants:
            return self._handle_no_consultants_found()

        response = self._format_consultants_list(consultants, titre)
        data = self._build_consultants_data(consultants)

        return {
            "response": response,
            "data": data,
            "intent": "liste_consultants",
            "confidence": 0.9,
        }

    def _get_consultants_by_criteria(self, question_lower: str) -> tuple:
        """Récupère les consultants selon les critères de la question"""
        with get_database_session() as session:
            if "disponibles" in question_lower or "disponible" in question_lower:
                consultants = session.query(Consultant).filter(Consultant.disponibilite).all()
                titre = "👥 **Consultants disponibles :**"
            elif "indisponibles" in question_lower or "indisponible" in question_lower:
                consultants = session.query(Consultant).filter(Consultant.disponibilite is False).all()
                titre = "👥 **Consultants indisponibles :**"
            elif "actifs" in question_lower or "actif" in question_lower:
                consultants = session.query(Consultant).filter(Consultant.disponibilite).all()
                titre = "👥 **Consultants actifs :**"
            else:
                consultants = session.query(Consultant).all()
                titre = "👥 **Tous les consultants :**"

        return consultants, titre

    def _handle_no_consultants_found(self) -> Dict[str, Any]:
        """Gère le cas où aucun consultant n'est trouvé"""
        return {
            "response": "❓ Aucun consultant ne correspond à ce critère.",
            "data": None,
            "intent": "liste_consultants",
            "confidence": 0.8,
        }

    def _format_consultants_list(self, consultants: List, titre: str) -> str:
        """Formate la liste des consultants pour l'affichage"""
        response = f"{titre}\n\n"

        for i, consultant in enumerate(consultants, 1):
            response += self._format_consultant_line(consultant, i)

        response += "\n📊 **Total : " + str(len(consultants)) + " consultant(s)**"
        return response

    def _format_consultant_line(self, consultant, index: int) -> str:
        """Formate une ligne de consultant dans la liste"""
        status_icon = "🟢" if consultant.disponibilite else "🔴"
        line = f"{index}. {status_icon} **{consultant.prenom} {consultant.nom}**"

        if consultant.email:
            line += f" - {consultant.email}"

        if consultant.salaire_actuel:
            cjm = self._calculate_cjm(consultant.salaire_actuel)
            line += f" - {consultant.salaire_actuel:,.0f} €/an - CJM: {cjm:,.0f} €"

        line += "\n"
        return line

    def _calculate_cjm(self, salaire_actuel: float) -> float:
        """Calcule le CJM à partir du salaire annuel"""
        return salaire_actuel * 1.8 / 216

    def _build_consultants_data(self, consultants: List) -> Dict:
        """Construit les données structurées des consultants"""
        return {
            "consultants": [
                {
                    "nom": c.nom,
                    "prenom": c.prenom,
                    "email": c.email,
                    "disponibilite": c.disponibilite,
                    "salaire": c.salaire_actuel,
                    "cjm": (self._calculate_cjm(c.salaire_actuel) if c.salaire_actuel else None),
                }
                for c in consultants
            ],
            "count": len(consultants),
        }

    def _handle_consultant_search(self, entities: Dict) -> Dict[str, Any]:
        """Gère la recherche d'informations sur un consultant"""

        if not entities["noms"]:
            return self._handle_generic_consultant_search()

        nom: str = entities["noms"][0]
        consultant = self._find_consultant_by_name(nom)

        if not consultant:
            return self._handle_consultant_not_found_search(nom)

        response = self._build_consultant_profile_response(consultant)

        return {
            "response": response,
            "data": {"consultant": consultant.nom},
            "intent": "recherche_consultant",
            "confidence": 0.9,
        }

    def _handle_generic_consultant_search(self) -> Dict[str, Any]:
        """Gère les recherches génériques sans nom spécifique"""
        return {
            "response": "🤔 De quel consultant souhaitez-vous connaître les informations ?",
            "data": None,
            "intent": "recherche_consultant",
            "confidence": 0.5,
        }

    def _handle_consultant_not_found_search(self, nom: str) -> Dict[str, Any]:
        """Gère le cas où le consultant n'est pas trouvé"""
        return {
            "response": f"❌ Consultant **{nom}** introuvable dans la base de données.",
            "data": {"consultant": None},
            "intent": "recherche_consultant",
            "confidence": 0.9,
        }

    def _build_consultant_profile_response(self, consultant) -> str:
        """Construit la réponse complète du profil consultant"""
        response = self._format_basic_consultant_info(consultant)
        response += self._format_consultant_salary_info(consultant)
        response += self._format_consultant_missions_info(consultant)
        return response

    def _format_basic_consultant_info(self, consultant) -> str:
        """Formate les informations de base du consultant"""
        date_creation = (
            consultant.date_creation.strftime(self.DATE_FORMAT) if consultant.date_creation else "Non renseignée"
        )

        return f"""👤 **{consultant.prenom} {consultant.nom}**

📧 Email : {consultant.email or 'Non renseigné'}
📞 Téléphone : {consultant.telephone or 'Non renseigné'}
📊 Disponibilité : **{'Disponible' if consultant.disponibilite else 'Indisponible'}**
📅 Date création : {date_creation}"""

    def _format_consultant_salary_info(self, consultant) -> str:
        """Formate les informations salariales du consultant"""
        if not consultant.salaire_actuel:
            return ""

        cjm = self._calculate_cjm(consultant.salaire_actuel)
        return f"\n💰 Salaire : **{consultant.salaire_actuel:,.0f} €**" + f"\n📈 CJM : **{cjm:,.0f} €**"

    def _format_consultant_missions_info(self, consultant) -> str:
        """Formate les informations sur les missions du consultant"""
        missions_count = len(consultant.missions)
        if missions_count > 0:
            return f"\n💼 Missions : **{missions_count}** mission(s)"
        return ""

    def _handle_general_question(self) -> Dict[str, Any]:
        """Gère les questions générales"""

        responses = [
            "🤖 Je suis là pour vous aider à interroger la base de données des consultants !",
            "",
            "💡 **Voici quelques exemples de questions :**",
            "",
            '💰 *Salaires :* "Quel est le salaire de Jean Dupont ?"',
            '� *Expérience :* "Quelle est l\'expérience de Jean Dupont ?"',
            '🎯 *Grade :* "Quel est le grade de Marie ?"',
            '📋 *Contrat :* "Quel est le type de contrat de Paul ?"',
            '🏢 *Société :* "Dans quelle société travaille Anne ?"',
            '�📧 *Contact :* "Quel est l\'email de Marie ?"',
            '👥 *Listes :* "Quels sont les consultants disponibles ?"',
            '🔍 *Compétences :* "Qui maîtrise Python ?"',
            '💼 *Missions :* "Quelles sont les missions chez BNP Paribas ?"',
            '� *Statistiques :* "Combien de consultants sont actifs ?"',
            '👤 *Profils :* "Qui est Marie Martin ?"',
            "",
            "Que souhaitez-vous savoir ? 😊",
        ]

        return {
            "response": "\n".join(responses),
            "data": None,
            "intent": "general",
            "confidence": 1.0,
        }

    def _handle_practices_question(self, entities: Dict) -> Dict[str, Any]:
        """
        Gère les questions sur les practices (équipes) des consultants.
        """
        from database.models import Practice

        if entities["practices"]:
            return self._handle_specific_practice_question(entities["practices"][0])
        else:
            return self._handle_general_practices_question()

    def _handle_specific_practice_question(self, practice_name: str) -> Dict[str, Any]:
        """Gère les questions sur une practice spécifique"""
        from database.models import Practice

        with get_database_session() as session:
            practice = (
                session.query(Practice)
                .options(joinedload(Practice.consultants))
                .filter(func.lower(Practice.nom) == practice_name.lower())
                .first()
            )

        if not practice:
            return self._handle_practice_not_found(practice_name)

        consultants = list(practice.consultants)

        if not consultants:
            return self._handle_empty_practice(practice)

        response = self._format_practice_consultants_response(practice, consultants)
        data = self._build_practice_consultants_data(practice, consultants)

        return {
            "response": response,
            "data": data,
            "intent": "practices",
            "confidence": 0.9,
        }

    def _handle_practice_not_found(self, practice_name: str) -> Dict[str, Any]:
        """Gère le cas où la practice n'est pas trouvée"""
        return {
            "response": f"❌ Practice **{practice_name}** introuvable dans la base.",
            "data": None,
            "intent": "practices",
            "confidence": 0.7,
        }

    def _handle_empty_practice(self, practice) -> Dict[str, Any]:
        """Gère le cas où la practice n'a aucun consultant"""
        return {
            "response": f"📋 **Practice {practice.nom}** : Aucun consultant assigné",
            "data": {
                "practice": practice.nom,
                "consultants": [],
            },
            "intent": "practices",
            "confidence": 0.9,
        }

    def _format_practice_consultants_response(self, practice, consultants: List) -> str:
        """Formate la réponse pour les consultants d'une practice"""
        response = f"👥 **Practice {practice.nom}** :\n\n"
        response += f"📋 **{len(consultants)} consultant(s)** :\n"

        for i, consultant in enumerate(consultants, 1):
            response += self._format_practice_consultant_line(consultant, i)

        if practice.responsable:
            response += f"\n👨‍💼 **Responsable** : {practice.responsable}"

        return response

    def _format_practice_consultant_line(self, consultant, index: int) -> str:
        """Formate une ligne de consultant dans une practice"""
        status_icon = "🟢" if consultant.disponibilite else "🔴"
        line = f"{index}. {status_icon} **{consultant.prenom} {consultant.nom}**"

        if consultant.salaire_actuel:
            cjm = self._calculate_cjm(consultant.salaire_actuel)
            line += f" - CJM: {cjm:,.0f} €"

        line += "\n"
        return line

    def _build_practice_consultants_data(self, practice, consultants: List) -> Dict:
        """Construit les données structurées d'une practice"""
        return {
            "practice": practice.nom,
            "consultants": [
                {
                    "nom": c.nom,
                    "prenom": c.prenom,
                    "disponibilite": c.disponibilite,
                    "cjm": (self._calculate_cjm(c.salaire_actuel) if c.salaire_actuel else None),
                }
                for c in consultants
            ],
        }

    def _handle_general_practices_question(self) -> Dict[str, Any]:
        """Gère les questions générales sur toutes les practices"""
        from database.models import Practice

        with get_database_session() as session:
            practices = session.query(Practice).filter(Practice.actif).all()

        if not practices:
            return self._handle_no_practices_found()

        response = self._format_all_practices_response(practices)
        data = self._build_all_practices_data(practices)

        return {
            "response": response,
            "data": data,
            "intent": "practices",
            "confidence": 0.8,
        }

    def _handle_no_practices_found(self) -> Dict[str, Any]:
        """Gère le cas où aucune practice active n'est trouvée"""
        return {
            "response": "❓ Aucune practice active trouvée dans la base.",
            "data": None,
            "intent": "practices",
            "confidence": 0.6,
        }

    def _format_all_practices_response(self, practices: List) -> str:
        """Formate la réponse pour toutes les practices"""
        response = "🏢 **Practices disponibles** :\n\n"

        for practice in practices:
            response += self._format_practice_summary_line(practice)

        return response

    def _format_practice_summary_line(self, practice) -> str:
        """Formate une ligne de résumé pour une practice"""
        nb_consultants = len(list(practice.consultants))
        nb_disponibles = len([c for c in practice.consultants if c.disponibilite])

        line = f"• **{practice.nom}** : {nb_consultants} consultant(s) ({nb_disponibles} disponible(s))\n"

        if practice.responsable:
            line += f"  👨‍💼 Responsable : {practice.responsable}\n"

        return line

    def _build_all_practices_data(self, practices: List) -> Dict:
        """Construit les données structurées de toutes les practices"""
        return {
            "practices": [
                {
                    "nom": p.nom,
                    "consultants_total": len(list(p.consultants)),
                    "consultants_disponibles": len([c for c in p.consultants if c.disponibilite]),
                    "responsable": p.responsable,
                }
                for p in practices
            ]
        }

    def _handle_cvs_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les CVs des consultants."""

        if entities["noms"]:
            return self._handle_specific_consultant_cvs(entities["noms"][0])
        else:
            return self._handle_general_cvs_question()

    def _handle_specific_consultant_cvs(self, nom_recherche: str) -> Dict[str, Any]:
        """Gère les questions sur les CVs d'un consultant spécifique"""
        consultant = self._find_consultant_by_name(nom_recherche)

        if not consultant:
            return self._handle_consultant_not_found_cvs(nom_recherche)

        cvs = consultant.cvs

        if not cvs:
            return self._handle_no_cvs_found(consultant)

        response = self._format_consultant_cvs_response(consultant, cvs)
        data = self._build_consultant_cvs_data(consultant, cvs)

        return {
            "response": response,
            "data": data,
            "intent": "cvs",
            "confidence": 0.9,
        }

    def _handle_consultant_not_found_cvs(self, nom_recherche: str) -> Dict[str, Any]:
        """Gère le cas où le consultant n'est pas trouvé pour les CVs"""
        return {
            "response": f"❌ Consultant **{nom_recherche}** introuvable.",
            "data": None,
            "intent": "cvs",
            "confidence": 0.7,
        }

    def _handle_no_cvs_found(self, consultant) -> Dict[str, Any]:
        """Gère le cas où le consultant n'a aucun CV"""
        response = f"📁 **{consultant.prenom} {consultant.nom}** : Aucun CV uploadé"

        return {
            "response": response,
            "data": {
                "consultant": f"{consultant.prenom} {consultant.nom}",
                "cvs": [],
            },
            "intent": "cvs",
            "confidence": 0.9,
        }

    def _format_consultant_cvs_response(self, consultant, cvs: List) -> str:
        """Formate la réponse des CVs d'un consultant"""
        response = f"📁 **CVs de {consultant.prenom} {consultant.nom}{self.SECTION_HEADER_SUFFIX}"

        for i, cv in enumerate(cvs, 1):
            response += self._format_cv_details(cv, i)

        response += f"📊 **Total : {len(cvs)} document(s)**"
        return response

    def _format_cv_details(self, cv, index: int) -> str:
        """Formate les détails d'un CV"""
        taille_mb = (cv.taille_fichier / 1024 / 1024) if cv.taille_fichier else 0
        date_upload = cv.date_upload.strftime(self.DATE_FORMAT) if cv.date_upload else "N/A"

        details = f"{index}. **{cv.fichier_nom}**\n"
        details += f"   📅 Uploadé le : {date_upload}\n"
        details += f"   📏 Taille : {taille_mb:.1f} MB\n"

        if cv.contenu_extrait:
            details += "   ✅ Contenu analysé\n"

        details += "\n"
        return details

    def _build_consultant_cvs_data(self, consultant, cvs: List) -> Dict:
        """Construit les données structurées des CVs d'un consultant"""
        return {
            "consultant": f"{consultant.prenom} {consultant.nom}",
            "cvs": [
                {
                    "nom": cv.fichier_nom,
                    "date_upload": (cv.date_upload.isoformat() if cv.date_upload else None),
                    "taille": cv.taille_fichier,
                    "contenu_analyse": bool(cv.contenu_extrait),
                }
                for cv in cvs
            ],
        }

    def _handle_general_cvs_question(self) -> Dict[str, Any]:
        """Gère les questions générales sur les CVs"""
        from database.models import CV

        stats = self._get_cvs_statistics()
        top_consultants = self._get_top_consultants_by_cvs()

        response = self._format_general_cvs_response(stats, top_consultants)
        data = self._build_general_cvs_data(stats, top_consultants)

        return {
            "response": response,
            "data": data,
            "intent": "cvs",
            "confidence": 0.8,
        }

    def _get_cvs_statistics(self) -> Dict:
        """Récupère les statistiques générales des CVs"""
        from database.models import CV

        with get_database_session() as session:
            cvs_total = session.query(CV).count()
            consultants_avec_cv = session.query(Consultant).join(CV).distinct().count()

        return {"cvs_total": cvs_total, "consultants_avec_cv": consultants_avec_cv}

    def _get_top_consultants_by_cvs(self) -> List:
        """Récupère le top 3 des consultants avec le plus de CVs"""
        from sqlalchemy import func

        from database.models import CV

        with get_database_session() as session:
            return (
                session.query(Consultant, func.count(CV.id).label("nb_cvs"))
                .join(CV)
                .group_by(Consultant.id)
                .order_by(func.count(CV.id).desc())
                .limit(3)
                .all()
            )

    def _format_general_cvs_response(self, stats: Dict, top_consultants: List) -> str:
        """Formate la réponse générale sur les CVs"""
        response = "📁 **Statistiques des CVs** :\n\n"
        response += f"• Total de documents : **{stats['cvs_total']}**\n"
        response += f"• Consultants avec CV : **{stats['consultants_avec_cv']}**\n"

        if top_consultants:
            response += "\n🏆 **Top consultants (nombre de CVs)** :\n"
            for consultant, nb_cvs in top_consultants:
                response += f"• **{consultant.prenom} {consultant.nom}** : {nb_cvs} CV(s)\n"

        return response

    def _build_general_cvs_data(self, stats: Dict, top_consultants: List) -> Dict:
        """Construit les données structurées générales des CVs"""
        return {
            "cvs_total": stats["cvs_total"],
            "consultants_avec_cv": stats["consultants_avec_cv"],
            "top_consultants": [{"nom": c.nom, "prenom": c.prenom, "nb_cvs": nb} for c, nb in top_consultants],
        }

    # Méthodes utilitaires pour les requêtes DB

    def _find_consultant_by_name(self, nom_recherche: str) -> Optional[Consultant]:
        """
        Recherche flexible d'un consultant par son nom.

        Effectue d'abord une recherche exacte sur prénom, nom ou nom complet,
        puis une recherche partielle si aucune correspondance exacte n'est trouvée.

        Args:
            nom_recherche: Nom ou prénom du consultant à rechercher (insensible à la casse)

        Returns:
            Objet Consultant si trouvé, None sinon

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> consultant = chatbot._find_consultant_by_name("Jean Dupont")
            >>> print(consultant.prenom, consultant.nom)
            Jean Dupont

            >>> consultant = chatbot._find_consultant_by_name("Dupont")
            >>> print(consultant.prenom, consultant.nom)
            Jean Dupont
        """

        # Essayer une correspondance exacte d'abord
        with get_database_session() as session:

            consultant = (
                session.query(Consultant)
                .options(joinedload(Consultant.langues).joinedload(ConsultantLangue.langue))
                .filter(
                    or_(
                        func.lower(Consultant.nom) == nom_recherche.lower(),
                        func.lower(Consultant.prenom) == nom_recherche.lower(),
                        func.lower(func.concat(Consultant.prenom, " ", Consultant.nom)) == nom_recherche.lower(),
                        func.lower(func.concat(Consultant.nom, " ", Consultant.prenom)) == nom_recherche.lower(),
                    )
                )
                .first()
            )

        if consultant:
            return consultant

        # Essayer une correspondance partielle
        with get_database_session() as session:

            consultant = (
                session.query(Consultant)
                .options(joinedload(Consultant.langues).joinedload(ConsultantLangue.langue))
                .filter(
                    or_(
                        func.lower(Consultant.nom).like(f"%{nom_recherche.lower()}%"),
                        func.lower(Consultant.prenom).like(f"%{nom_recherche.lower()}%"),
                    )
                )
                .first()
            )

        return consultant

    def _find_consultants_by_skill(self, competence: str, type_competence: Optional[str] = None) -> List[Any]:
        """
        Recherche les consultants maîtrisant une compétence spécifique.

        Args:
            competence: Nom de la compétence à rechercher (insensible à la casse)
            type_competence: Type de compétence (technique/fonctionnelle) pour filtrer (optionnel)

        Returns:
            Liste des objets Consultant maîtrisant la compétence

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> consultants = chatbot._find_consultants_by_skill("Python", "technique")
            >>> print(f"Trouvé {len(consultants)} consultants Python")

            >>> consultants = chatbot._find_consultants_by_skill("SQL")
            >>> print(f"Trouvé {len(consultants)} consultants SQL")
        """
        from database.models import Competence
        from database.models import ConsultantCompetence

        # Construction de la requête de base
        with get_database_session() as session:

            query = (
                session.query(Consultant)
                .join(
                    ConsultantCompetence,
                    Consultant.id == ConsultantCompetence.consultant_id,
                )
                .join(Competence, ConsultantCompetence.competence_id == Competence.id)
                .filter(func.lower(Competence.nom).like(f"%{competence.lower()}%"))
            )

        # Ajouter le filtre par type si spécifié
        if type_competence:
            query = query.filter(Competence.type_competence == type_competence)

        consultants = query.distinct().all()

        return consultants  # type: ignore[no-any-return]

    def _find_consultants_by_language(self, langue: str) -> List[Any]:
        """
        Recherche les consultants parlant une langue spécifique.

        Args:
            langue: Nom de la langue à rechercher (insensible à la casse)

        Returns:
            Liste des objets Consultant parlant la langue

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> consultants = chatbot._find_consultants_by_language("anglais")
            >>> print(f"Trouvé {len(consultants)} consultants anglophones")

            >>> consultants = chatbot._find_consultants_by_language("espagnol")
            >>> print(f"Trouvé {len(consultants)} consultants hispanophones")
        """

        # Construction de la requête de base
        with get_database_session() as session:

            consultants = (
                session.query(Consultant)
                .join(ConsultantLangue, Consultant.id == ConsultantLangue.consultant_id)
                .join(Langue, ConsultantLangue.langue_id == Langue.id)
                .filter(func.lower(Langue.nom).like(f"%{langue.lower()}%"))
                .distinct()
                .all()
            )

        return consultants  # type: ignore[no-any-return]

    def _get_missions_by_company(self, entreprise: str) -> List[Mission]:
        """
        Récupère toutes les missions associées à une entreprise.

        Args:
            entreprise: Nom de l'entreprise à rechercher (insensible à la casse)

        Returns:
            Liste des objets Mission pour cette entreprise

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> missions = chatbot._get_missions_by_company("BNP Paribas")
            >>> print(f"BNP Paribas a {len(missions)} missions")
        """
        with get_database_session() as session:
            return (
                session.query(Mission)
                .filter(func.lower(Mission.client).like(f"%{entreprise.lower()}%"))  # type: ignore[no-any-return]
                .all()
            )

    def _get_missions_by_consultant(self, consultant_id: int) -> List[Mission]:
        """
        Récupère toutes les missions d'un consultant spécifique.

        Args:
            consultant_id: Identifiant unique du consultant

        Returns:
            Liste des objets Mission du consultant, triés par date de début décroissante

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> missions = chatbot._get_missions_by_consultant(123)
            >>> print(f"Consultant 123 a {len(missions)} missions")
            >>> if missions:
            ...     print(f"Dernière mission: {missions[0].nom_mission}")
        """
        with get_database_session() as session:
            return (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant_id)  # type: ignore[no-any-return]
                .order_by(Mission.date_debut.desc())
                .all()
            )

    def _get_consultant_skills(self, consultant_id: int, type_competence: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les compétences détaillées d'un consultant.

        Args:
            consultant_id: Identifiant unique du consultant
            type_competence: Type de compétence à filtrer (technique/fonctionnelle) (optionnel)

        Returns:
            Liste de dictionnaires contenant les détails des compétences :
            - nom: Nom de la compétence
            - categorie: Catégorie de la compétence
            - type: Type de compétence (technique/fonctionnelle)
            - niveau_maitrise: Niveau de maîtrise (débutant/intermédiaire/expert)
            - annees_experience: Nombre d'années d'expérience
            - description: Description de la compétence

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> skills = chatbot._get_consultant_skills(123, "technique")
            >>> print(f"Consultant 123 a {len(skills)} compétences techniques")
            >>> for skill in skills:
            ...     print(f"- {skill['nom']}: {skill['niveau_maitrise']}")
        """
        with get_database_session() as session:

            query = (
                session.query(ConsultantCompetence)
                .join(Competence)
                .filter(ConsultantCompetence.consultant_id == consultant_id)
            )

        # Ajouter le filtre par type si spécifié
        if type_competence:
            query = query.filter(Competence.type_competence == type_competence)

        consultant_competences = query.all()

        skills = []
        for cc in consultant_competences:
            skills.append(
                {
                    "nom": cc.competence.nom,
                    "categorie": cc.competence.categorie,
                    "type": cc.competence.type_competence,
                    "niveau_maitrise": cc.niveau_maitrise,
                    "annees_experience": cc.annees_experience,
                    "description": cc.competence.description,
                }
            )

        return skills

    def _get_salary_stats(self) -> Dict[str, float]:
        """
        Calcule les statistiques des salaires des consultants.

        Returns:
            Dictionnaire contenant :
            - moyenne: Salaire moyen
            - mediane: Salaire médian
            - minimum: Salaire minimum
            - maximum: Salaire maximum
            - total: Nombre de consultants avec salaire renseigné

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> stats = chatbot._get_salary_stats()
            >>> print(f"Salaire moyen: {stats['moyenne']:,.0f} €")
            >>> print(f"Salaire médian: {stats['mediane']:,.0f} €")
        """
        with get_database_session() as session:

            consultants = (
                session.query(Consultant)
                .filter(
                    and_(
                        Consultant.salaire_actuel.isnot(None),
                        Consultant.salaire_actuel > 0,
                    )
                )
                .all()
            )

        if not consultants:
            return {"moyenne": 0, "mediane": 0, "minimum": 0, "maximum": 0, "total": 0}

        salaires = [c.salaire_actuel for c in consultants]
        salaires.sort()

        return {
            "moyenne": sum(salaires) / len(salaires),
            "mediane": salaires[len(salaires) // 2],
            "minimum": min(salaires),
            "maximum": max(salaires),
            "total": len(consultants),
        }

    def _get_general_stats(self) -> Dict[str, Any]:
        """
        Calcule les statistiques générales de la base de données.
        """
        with get_database_session() as session:
            consultant_stats = self._get_consultant_statistics(session)
            mission_stats = self._get_mission_statistics(session)
            practice_stats = self._get_practice_statistics(session)
            cv_stats = self._get_cv_statistics(session)
            financial_stats = self._get_financial_statistics(session)

        return {
            **consultant_stats,
            **mission_stats,
            **practice_stats,
            **cv_stats,
            **financial_stats,
        }

    def _get_consultant_statistics(self, session) -> Dict[str, int]:
        """Récupère les statistiques des consultants"""
        consultants_total = session.query(Consultant).count()
        consultants_actifs = session.query(Consultant).filter(Consultant.disponibilite).count()
        consultants_inactifs = consultants_total - consultants_actifs

        return {
            "consultants_total": consultants_total,
            "consultants_actifs": consultants_actifs,
            "consultants_inactifs": consultants_inactifs,
        }

    def _get_mission_statistics(self, session) -> Dict[str, int]:
        """Récupère les statistiques des missions"""
        missions_total = session.query(Mission).count()
        missions_en_cours = session.query(Mission).filter(Mission.statut == "en_cours").count()
        missions_terminees = missions_total - missions_en_cours

        return {
            "missions_total": missions_total,
            "missions_en_cours": missions_en_cours,
            "missions_terminees": missions_terminees,
        }

    def _get_practice_statistics(self, session) -> Dict[str, int]:
        """Récupère les statistiques des practices"""
        from database.models import Practice

        practices_total = session.query(Practice).filter(Practice.actif).count()

        return {
            "practices_total": practices_total,
        }

    def _get_cv_statistics(self, session) -> Dict[str, int]:
        """Récupère les statistiques des CVs"""
        from database.models import CV

        cvs_total = session.query(CV).count()
        consultants_avec_cv = session.query(Consultant).join(CV).distinct().count()

        return {
            "cvs_total": cvs_total,
            "consultants_avec_cv": consultants_avec_cv,
        }

    def _get_financial_statistics(self, session) -> Dict[str, float]:
        """Récupère les statistiques financières"""
        tjm_moyen = self._calculate_average_tjm(session)
        salaire_moyen = self._calculate_average_salary(session)
        cjm_moyen = self._calculate_average_cjm(salaire_moyen)

        return {
            "tjm_moyen": tjm_moyen,
            "salaire_moyen": salaire_moyen,
            "cjm_moyen": cjm_moyen,
        }

    def _calculate_average_tjm(self, session) -> float:
        """Calcule le TJM moyen"""
        return (
            session.query(func.avg(Mission.taux_journalier)).filter(Mission.taux_journalier.isnot(None)).scalar() or 0
        )

    def _calculate_average_salary(self, session) -> float:
        """Calcule le salaire moyen"""
        return (
            session.query(func.avg(Consultant.salaire_actuel)).filter(Consultant.salaire_actuel.isnot(None)).scalar()
            or 0
        )

    def _calculate_average_cjm(self, salaire_moyen: float) -> float:
        """Calcule le CJM moyen à partir du salaire moyen"""
        return (salaire_moyen * 1.8 / 216) if salaire_moyen > 0 else 0

    def _handle_availability_question(self, entities: Dict) -> Dict[str, Any]:
        """
        Gère les questions sur la disponibilité des consultants (V1.2.2).

        Args:
            entities: Dictionnaire contenant les entités extraites

        Returns:
            Dictionnaire avec la réponse formatée
        """
        consultant = self._get_consultant_from_entities(entities)

        if consultant:
            return self._handle_specific_consultant_availability(consultant)
        else:
            return self._handle_general_availability_question()

    def _get_consultant_from_entities(self, entities: Dict):
        """Extrait le consultant depuis les entités"""
        if entities["noms"]:
            nom_complet = " ".join(entities["noms"])
            return self._find_consultant_by_name(nom_complet)
        return None

    def _handle_specific_consultant_availability(self, consultant) -> Dict[str, Any]:
        """Gère la disponibilité d'un consultant spécifique"""
        try:
            consultant_db = self._get_consultant_db_data(consultant)

            if consultant_db:
                response = self._build_availability_response(consultant, consultant_db)
            else:
                response = self._format_availability_error(consultant)

            return self._build_availability_result(consultant, consultant_db, response)

        except (SQLAlchemyError, AttributeError, ValueError, TypeError) as e:
            return self._build_availability_error_result(e)

    def _get_consultant_db_data(self, consultant):
        """Récupère les données DB du consultant"""
        with get_database_session() as session:
            return session.query(Consultant).filter(Consultant.id == consultant.id).first()

    def _build_availability_response(self, consultant, consultant_db) -> str:
        """Construit la réponse de disponibilité"""
        response = self._format_availability_header(consultant)
        response += self._format_availability_status(consultant_db)
        response += self._format_consultant_details(consultant_db)
        return response

    def _format_availability_header(self, consultant) -> str:
        """Formate l'en-tête de disponibilité"""
        return "📅 **Disponibilité de " + consultant.prenom + " " + consultant.nom + self.SECTION_HEADER_SUFFIX

    def _format_availability_status(self, consultant_db) -> str:
        """Formate le statut de disponibilité basé sur les missions"""
        # Utiliser la nouvelle logique de calcul dynamique
        status = _calculate_availability_status(consultant_db)

        if "Disponible dans" in status:
            # Format pour disponibilité future avec délai
            return f"⏳ {status}\n\n"
        elif "Non disponible" in status:
            # Format pour indisponibilité avec alerte
            return f"🚫 {status}\n\n"
        else:
            # Format pour disponibilité immédiate
            return f"✅ {status}\n\n"

    def _format_asap_availability(self, consultant_db) -> str:
        """Formate la disponibilité ASAP"""
        response = "✅ **Disponible immédiatement (ASAP)**\n\n"
        missions_en_cours = self._get_missions_en_cours(consultant_db)

        if missions_en_cours:
            response += "⚠️ **Attention :** Le consultant a des missions en cours mais est marqué disponible\n"
            response += self._format_missions_list(missions_en_cours)

        return response

    def _format_planned_availability(self, consultant_db, date_dispo) -> str:
        """Formate la disponibilité planifiée"""
        response = "📅 **Disponible à partir du :** " + str(date_dispo) + "\n\n"

        missions_futures = self._get_missions_futures(consultant_db)
        if missions_futures:
            response += "🎯 **Missions en cours/planifiées :**\n"
            response += self._format_missions_futures_list(missions_futures)

        return response

    def _get_missions_en_cours(self, consultant_db):
        """Récupère les missions en cours"""
        return [m for m in consultant_db.missions if m.statut == "en_cours"]

    def _get_missions_futures(self, consultant_db):
        """Récupère les missions futures"""
        from datetime import date

        return [m for m in consultant_db.missions if m.date_fin and m.date_fin > date.today()]

    def _format_missions_list(self, missions):
        """Formate la liste des missions"""
        result = ""
        for mission in missions:
            result += self.BULLET_POINT_INDENT + mission.nom_mission + " chez " + mission.client + "\n"
        return result

    def _format_missions_futures_list(self, missions):
        """Formate la liste des missions futures"""
        result = ""
        for mission in missions:
            fin_mission = mission.date_fin.strftime(self.DATE_FORMAT)
            result += self.BULLET_POINT_INDENT + mission.nom_mission + " (fin: " + fin_mission + ")\n"
        return result

    def _format_consultant_details(self, consultant_db) -> str:
        """Formate les détails du consultant"""
        response = "\n📊 **Statut actuel :** "

        if consultant_db.disponibilite:
            response += "✅ Marqué disponible"
        else:
            response += "🔴 Marqué occupé"

        if consultant_db.grade:
            response += "\n🎯 **Grade :** " + str(consultant_db.grade)
        if consultant_db.type_contrat:
            response += "\n📝 **Contrat :** " + str(consultant_db.type_contrat)

        return response

    def _format_availability_error(self, consultant) -> str:
        """Formate l'erreur de disponibilité"""
        return (
            "❌ Impossible de récupérer les données de disponibilité pour **"
            + consultant.prenom
            + " "
            + consultant.nom
            + "**."
        )

    def _build_availability_result(self, consultant, consultant_db, response) -> Dict[str, Any]:
        """Construit le résultat de disponibilité"""
        return {
            "response": response,
            "data": {
                "consultant": {
                    "nom": consultant.nom,
                    "prenom": consultant.prenom,
                    "date_disponibilite": (
                        getattr(consultant_db, "date_disponibilite", None) if consultant_db else None
                    ),
                    "disponibilite_immediate": (
                        getattr(consultant_db, "disponibilite", None) if consultant_db else None
                    ),
                }
            },
            "intent": "disponibilite",
            "confidence": 0.9,
        }

    def _build_availability_error_result(self, error) -> Dict[str, Any]:
        """Construit le résultat d'erreur"""
        return {
            "response": ("❌ Erreur lors de la récupération des données de disponibilité : " + str(error)),
            "data": {},
            "intent": "disponibilite",
            "confidence": 0.3,
        }

    def _handle_general_availability_question(self) -> Dict[str, Any]:
        """Gère les questions générales sur les disponibilités"""
        try:
            consultants_dispos, consultants_occupes = self._get_availability_data()
            response = self._build_general_availability_response(consultants_dispos, consultants_occupes)

            return {
                "response": response,
                "data": {
                    "disponibles": len(consultants_dispos),
                    "occupes": len(consultants_occupes),
                    "total": len(consultants_dispos) + len(consultants_occupes),
                },
                "intent": "disponibilite",
                "confidence": 0.8,
            }

        except (SQLAlchemyError, AttributeError, ValueError, TypeError) as e:
            return {
                "response": "❌ Erreur lors de la récupération des disponibilités : " + str(e),
                "data": {},
                "intent": "disponibilite",
                "confidence": 0.3,
            }

    def _get_availability_data(self):
        """Récupère les données de disponibilité générale"""
        with get_database_session() as session:
            consultants_dispos = session.query(Consultant).filter(Consultant.disponibilite).all()

        with get_database_session() as session:
            consultants_occupes = session.query(Consultant).filter(Consultant.disponibilite is False).all()

        return consultants_dispos, consultants_occupes

    def _build_general_availability_response(self, consultants_dispos, consultants_occupes) -> str:
        """Construit la réponse générale de disponibilité"""
        response = "📅 **État des disponibilités** :\n\n"
        response += "✅ **Disponibles immédiatement :** " + str(len(consultants_dispos)) + " consultant(s)\n"

        response += self._format_available_consultants_list(consultants_dispos)
        response += self._format_busy_consultants_section(consultants_occupes)

        return response

    def _format_available_consultants_list(self, consultants_dispos) -> str:
        """Formate la liste des consultants disponibles"""
        response = ""

        if consultants_dispos:
            for consultant in consultants_dispos[:5]:  # Limiter à 5
                response += self.BULLET_POINT_INDENT + consultant.prenom + " " + consultant.nom + "\n"
            if len(consultants_dispos) > 5:
                response += self.BULLET_POINT_INDENT + "... et " + str(len(consultants_dispos) - 5) + " autre(s)\n"

        return response

    def _format_busy_consultants_section(self, consultants_occupes) -> str:
        """Formate la section des consultants occupés"""
        response = "\n🔴 **Occupés :** " + str(len(consultants_occupes)) + " consultant(s)\n"

        if consultants_occupes:
            for consultant in consultants_occupes[:5]:  # Limiter à 5
                date_dispo = consultant.date_disponibilite
                response += (
                    self.BULLET_POINT_INDENT
                    + consultant.prenom
                    + " "
                    + consultant.nom
                    + " (dispo: "
                    + str(date_dispo)
                    + ")\n"
                )
            if len(consultants_occupes) > 5:
                response += self.BULLET_POINT_INDENT + "... et " + str(len(consultants_occupes) - 5) + " autre(s)\n"

        return response

    def _get_consultant_missions_with_tjm(self, consultant_db) -> List:
        """Récupère les missions avec TJM d'un consultant"""
        if not consultant_db or not consultant_db.missions:
            return []
        return [m for m in consultant_db.missions if m.tjm or m.taux_journalier]

    def _format_mission_tjm_details(self, mission) -> str:
        """Formate les détails d'une mission avec son TJM"""
        tjm = mission.tjm or mission.taux_journalier
        tjm_type = "TJM" if mission.tjm else "TJM (ancien)"

        response = f"🎯 **{mission.nom_mission}**\n"
        response += f"{self.BULLET_POINT_INDENT}Client: {mission.client}\n"
        response += f"{self.BULLET_POINT_INDENT}{tjm_type}: {tjm}€\n"

        if mission.date_debut:
            debut = mission.date_debut.strftime(self.DATE_FORMAT)
            if mission.date_fin:
                fin = mission.date_fin.strftime(self.DATE_FORMAT)
                response += f"{self.BULLET_POINT_INDENT}Période: {debut} → {fin}\n"
            else:
                response += f"{self.BULLET_POINT_INDENT}Début: {debut} (en cours)\n"

        return response + "\n"

    def _calculate_tjm_average(self, missions_avec_tjm) -> tuple:
        """Calcule le TJM moyen à partir d'une liste de missions"""
        if not missions_avec_tjm:
            return 0, 0

        total_tjm = sum(mission.tjm or mission.taux_journalier for mission in missions_avec_tjm)
        count_tjm = len(missions_avec_tjm)
        return total_tjm / count_tjm if count_tjm > 0 else 0, count_tjm

    def _handle_consultant_tjm_inquiry(self, consultant) -> Dict[str, Any]:
        """Gère les questions TJM pour un consultant spécifique"""
        try:
            with get_database_session() as session:
                consultant_db = session.query(Consultant).filter(Consultant.id == consultant.id).first()

            missions_avec_tjm = self._get_consultant_missions_with_tjm(consultant_db)

            if missions_avec_tjm:
                response = f"💰 **TJM des missions de {consultant.prenom} {consultant.nom}** :\n\n"

                for mission in missions_avec_tjm:
                    response += self._format_mission_tjm_details(mission)

                tjm_moyen, count_tjm = self._calculate_tjm_average(missions_avec_tjm)
                if count_tjm > 1:
                    response += f"📊 **TJM moyen :** {tjm_moyen:.0f}€ (sur {count_tjm} missions)"

            else:
                response = f"💰 **{consultant.prenom} {consultant.nom}** : " "Aucun TJM renseigné dans les missions"

        except (
            SQLAlchemyError,
            AttributeError,
            ValueError,
            TypeError,
            ZeroDivisionError,
        ) as e:
            response = f"❌ Erreur lors de la récupération des TJM : {str(e)}"

        return {
            "response": response,
            "data": {"consultant": {"nom": consultant.nom, "prenom": consultant.prenom}},
            "intent": "tjm_mission",
            "confidence": 0.9,
        }

    def _get_global_tjm_statistics(self) -> Dict[str, Any]:
        """Calcule les statistiques globales de TJM"""
        try:
            with get_database_session() as session:
                # TJM moyen avec nouveau champ
                tjm_nouveau_moyen = session.query(func.avg(Mission.tjm)).filter(Mission.tjm.isnot(None)).scalar() or 0

                # TJM moyen avec ancien champ
                tjm_ancien_moyen = (
                    session.query(func.avg(Mission.taux_journalier))
                    .filter(Mission.taux_journalier.isnot(None))
                    .scalar()
                    or 0
                )

                # Compter les missions avec TJM
                missions_nouveau_tjm = session.query(Mission).filter(Mission.tjm.isnot(None)).count()

                missions_ancien_tjm = session.query(Mission).filter(Mission.taux_journalier.isnot(None)).count()

            response = "💰 **Statistiques TJM des missions** :\n\n"

            if missions_nouveau_tjm > 0:
                response += "🆕 **Nouveau format TJM :**\n"
                response += f"{self.BULLET_POINT_INDENT}Missions avec TJM: {missions_nouveau_tjm}\n"
                response += f"{self.BULLET_POINT_INDENT}TJM moyen: {tjm_nouveau_moyen:.0f}€\n\n"

            if missions_ancien_tjm > 0:
                response += "📊 **Ancien format TJM :**\n"
                response += f"{self.BULLET_POINT_INDENT}Missions avec TJM: {missions_ancien_tjm}\n"
                response += f"{self.BULLET_POINT_INDENT}TJM moyen: {tjm_ancien_moyen:.0f}€\n\n"

            # Calcul global
            if missions_nouveau_tjm > 0 or missions_ancien_tjm > 0:
                total_missions = missions_nouveau_tjm + missions_ancien_tjm
                tjm_global = (
                    (tjm_nouveau_moyen * missions_nouveau_tjm) + (tjm_ancien_moyen * missions_ancien_tjm)
                ) / total_missions
                response += f"🎯 **TJM global moyen :** {tjm_global:.0f}€ (sur {total_missions} missions)"
            else:
                response = "💰 **Aucun TJM renseigné** dans les missions"

            return {
                "response": response,
                "data": {
                    "tjm_nouveau_moyen": tjm_nouveau_moyen,
                    "tjm_ancien_moyen": tjm_ancien_moyen,
                    "missions_nouveau": missions_nouveau_tjm,
                    "missions_ancien": missions_ancien_tjm,
                },
                "intent": "tjm_mission",
                "confidence": 0.8,
            }

        except (SQLAlchemyError, ZeroDivisionError, TypeError, ValueError) as e:
            return {
                "response": f"❌ Erreur lors de la récupération des statistiques TJM : {str(e)}",
                "data": {},
                "intent": "tjm_mission",
                "confidence": 0.3,
            }

    def _handle_mission_tjm_question(self, entities: Dict) -> Dict[str, Any]:
        """
        Gère les questions sur les TJM (Taux Journalier Moyen) des missions (V1.2.2).

        Analyse les TJM des missions d'un consultant spécifique ou calcule
        les statistiques générales sur les TJM de toutes les missions.

        Args:
            entities: Dictionnaire contenant les entités extraites de la question
                     (noms, entreprises, compétences, langues, etc.)

        Returns:
            Dictionnaire contenant :
            - response: Réponse formatée sur les TJM
            - data: Données structurées sur les TJM
            - intent: Type d'intention détecté ("tjm_mission")
            - confidence: Niveau de confiance de la réponse (0.0 à 1.0)
        """
        # Chercher un consultant spécifique
        consultant = None
        if entities.get("noms"):
            nom_complet = " ".join(entities["noms"])
            consultant = self._find_consultant_by_name(nom_complet)

        if consultant:
            return self._handle_consultant_tjm_inquiry(consultant)
        else:
            return self._get_global_tjm_statistics()

    def get_response(self, question: str) -> str:
        """
        Interface simplifiée pour obtenir une réponse textuelle du chatbot.

        Méthode compatible avec les tests existants qui retourne uniquement
        la réponse textuelle sans les métadonnées structurées.

        Args:
            question: Question de l'utilisateur en langage naturel

        Returns:
            Réponse textuelle formatée du chatbot, ou message d'erreur
            si la question n'est pas comprise ou en cas d'exception

        Raises:
            Aucun: Les exceptions sont capturées et retournées comme messages d'erreur

        Example:
            >>> chatbot = ChatbotService()
            >>> response = chatbot.get_response("Quel est le salaire de Jean Dupont ?")
            >>> print(response)
            💰 Le salaire de **Jean Dupont** est de **45,000 €** par an.

            >>> response = chatbot.get_response("Question incompréhensible")
            >>> print(response)
            ❓ Je n'ai pas compris votre question.
        """
        try:
            result = self.process_question(question)
            response = result.get("response", "❓ Je n'ai pas compris votre question.")
            return str(response) if response is not None else "❓ Je n'ai pas compris votre question."
        except (AttributeError, KeyError, TypeError, ValueError) as e:
            return "❌ Erreur: " + str(e)

    def __del__(self):
        """
        Destructeur de la classe ChatbotService.

        Nettoie les ressources utilisées par le service.
        Note: La gestion des sessions de base de données est déléguée
        aux context managers pour éviter les fuites de mémoire.
        """
        # Nettoyage des ressources si nécessaire
        pass
