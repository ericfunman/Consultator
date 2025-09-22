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

# Imports des services existants
from database.database import get_database_session
from database.models import Competence
from database.models import Consultant
from database.models import ConsultantCompetence
from database.models import ConsultantLangue
from database.models import Langue
from database.models import Mission


class ChatbotService:
    """Service principal du chatbot pour Consultator"""

    # Constantes pour les chaînes de format répétées
    SECTION_HEADER_SUFFIX = "** :\n\n"
    YEARS_SUFFIX = " années\n"
    TOTAL_PREFIX = "\n📊 **Total : "
    CONSULTANT_FOUND_SUFFIX = " consultant(s) trouvé(s)**"
    STATS_PREFIX = "\n\n📊 **"
    BULLET_POINT = " • "
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
            with get_database_session() as session:
                return query_func(session)

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

    def _analyze_intent(self, question: str) -> str:
        """Analyse l'intention de la question"""

        # D'abord, vérifier s'il y a un nom de consultant mentionné
        with get_database_session() as session:
            all_consultants = session.query(Consultant).all()
            has_consultant_name: bool = False
            for consultant in all_consultants:
                if re.search(
                    rf"\b{re.escape(consultant.prenom.lower())}\b", question
                ) or re.search(rf"\b{re.escape(consultant.nom.lower())}\b", question):
                    has_consultant_name = True
                    break

        # Patterns pour identifier les intentions
        intent_patterns = {
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
                r"quelles.+compétences",
                r"quelles.+competences",
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
                r"niveau.+langue",
                r"parle.+anglais",
                r"qui.+parle",
                r"quelles.+langues",
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
                r"combien.+missions?",
                r"nombre.+missions?",
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
                r"combien.+consultants",
                r"nombre.+consultants",
                r"combien.+dans.+base",
                r"nombre",
                r"moyenne",
                r"total",
                r"statistiques",
                r"combien.+missions",
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
                r"quand.+libre",
                r"quand.+disponible",
                r"date.+disponibilité",
                r"fin.+mission",
                r"libéré",
                r"fini",
                r"termine",
                r"asap",
                r"immédiatement",
                r"tout de suite",
                r"prochaine disponibilité",
            ],
            "tjm_mission": [  # Nouvelle intention V1.2.2
                r"tjm.+mission",
                r"taux.+mission",
                r"prix.+mission",
                r"coût.+mission",
                r"tarif.+mission",
                r"facturation.+mission",
                r"journalier.+mission",
                r"combien.+coûte.+mission",
                r"prix.+journée.+mission",
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

        # Scorer chaque intention
        intent_scores: Dict[str, int] = {}
        for intent, patterns in intent_patterns.items():
            score: int = 0
            for pattern in patterns:
                if re.search(pattern, question):
                    score += 1
            intent_scores[intent] = score

        # Si un nom de consultant est mentionné et qu'on parle de salaire,
        # c'est forcément une question de salaire spécifique
        if has_consultant_name and intent_scores.get("salaire", 0) > 0:
            return "salaire"

        # Si un nom de consultant est mentionné et qu'on demande des coordonnées,
        # c'est forcément une question de contact
        if has_consultant_name and intent_scores.get("contact", 0) > 0:
            return "contact"

        # NOUVELLE RÈGLE V1.2.2 : Prioriser tjm_mission sur missions si TJM est
        # mentionné
        if intent_scores.get("tjm_mission", 0) > 0 and re.search(
            r"tjm|taux|prix|coût|tarif", question
        ):
            return "tjm_mission"

        # Si un nom de consultant est mentionné et qu'on parle de missions,
        # c'est forcément une question de missions spécifique
        if has_consultant_name and intent_scores.get("missions", 0) > 0:
            return "missions"

        # Si c'est une question de type "combien de consultants en CDI/CDD", c'est
        # du profil professionnel
        if re.search(
            r"combien.+(consultants?).+(cdi|cdd|stagiaire|alternant|indépendant)",
            question,
        ):
            return "profil_professionnel"

        # Si c'est une question de type "qui travaille chez", c'est du profil
        # professionnel
        if re.search(r"qui.+(travaille|est).+(chez|dans).+(quanteam|asigma)", question):
            return "profil_professionnel"

        # Si c'est une question de type "combien de missions", c'est des missions
        if re.search(r"combien.+missions?", question):
            return "missions"

        # Si le mot "combien" est utilisé avec un nom de consultant, c'est probablement un salaire
        # MAIS seulement si ce n'est pas déjà traité par les règles ci-dessus
        if has_consultant_name and re.search(r"combien", question):
            return "salaire"

        # Si c'est une question de type "combien de consultants", c'est des statistiques
        if re.search(r"combien.+(consultants?|dans.+base)", question):
            return "statistiques"

        # Retourner l'intention avec le meilleur score
        if max(intent_scores.values()) > 0:
            best_intent = max(intent_scores, key=lambda k: intent_scores[k])
            return best_intent
        else:
            return "general"

    def _extract_entities(self, question: str) -> Dict[str, List[str]]:
        """Extrait les entités nommées de la question"""
        entities: Dict[str, List[str]] = {
            "noms": [],
            "entreprises": [],
            "competences": [],
            "langues": [],
            "montants": [],
            "practices": [],
        }

        # Patterns pour extraire les entités

        # Noms - chercher dans la base de données
        with get_database_session() as session:

            all_consultants = session.query(Consultant).all()
        for consultant in all_consultants:
            # Chercher le prénom dans la question (insensible à la casse)
            if re.search(rf"\b{re.escape(consultant.prenom.lower())}\b", question):
                entities["noms"].append(consultant.prenom)
            # Chercher le nom de famille dans la question
            if re.search(rf"\b{re.escape(consultant.nom.lower())}\b", question):
                entities["noms"].append(consultant.nom)
            # Chercher le nom complet
            nom_complet: str = f"{consultant.prenom} {consultant.nom}".lower()
            if nom_complet in question:
                entities["noms"].append(f"{consultant.prenom} {consultant.nom}")

        # Supprimer les doublons en gardant l'ordre
        entities["noms"] = list(dict.fromkeys(entities["noms"]))

        # Entreprises connues
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
                entities["entreprises"].append(entreprise)

        # Compétences techniques - chercher dans la liste prédéfinie ET dans la base
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
                entities["competences"].append(competence)

        # Chercher aussi dans la base de données des compétences
        from database.models import Competence

        with get_database_session() as session:

            all_competences = session.query(Competence).all()
        for competence in all_competences:
            if re.search(rf"\b{re.escape(competence.nom.lower())}\b", question):
                entities["competences"].append(competence.nom)

        # Supprimer les doublons
        entities["competences"] = list(dict.fromkeys(entities["competences"]))

        # Langues - chercher dans la base de données des langues
        with get_database_session() as session:

            all_langues = session.query(Langue).all()
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
                entities["langues"].append(langue)

        # Chercher dans la base de données
        for langue in all_langues:
            if re.search(rf"\b{re.escape(langue.nom.lower())}\b", question):
                entities["langues"].append(langue.nom)

        # Supprimer les doublons
        entities["langues"] = list(dict.fromkeys(entities["langues"]))

        # Montants
        montants_pattern: str = r"(\d+(?:\s*\d{3})*)\s*(?:euros?|€)"
        montants_matches: List[str] = re.findall(montants_pattern, question)
        entities["montants"] = [
            montant.replace(" ", "") for montant in montants_matches
        ]

        # Practices - chercher dans la base de données
        from database.models import Practice

        with get_database_session() as session:

            all_practices = session.query(Practice).filter(Practice.actif).all()
        for practice in all_practices:
            if re.search(rf"\b{re.escape(practice.nom.lower())}\b", question):
                entities["practices"].append(practice.nom)

        return entities

    def _handle_salary_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les salaires et le CJM"""

        # Détecter si c'est une question sur le CJM
        is_cjm_question = (
            "cjm" in self.last_question.lower()
            or "coût journalier" in self.last_question.lower()
        )

        # Si un nom est mentionné, chercher ce consultant spécifique
        if entities["noms"]:
            nom_recherche: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom_recherche)

            if consultant:
                if consultant.salaire_actuel and consultant.salaire_actuel > 0:
                    if is_cjm_question:
                        # Calculer le CJM
                        cjm = consultant.salaire_actuel * 1.8 / 216
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

                return {
                    "response": response,
                    "data": {
                        "consultant": {
                            "nom": consultant.nom,
                            "prenom": consultant.prenom,
                            "salaire": consultant.salaire_actuel,
                            "cjm": (
                                (consultant.salaire_actuel * 1.8 / 216)
                                if consultant.salaire_actuel
                                else None
                            ),
                            "disponibilite": consultant.disponibilite,
                        }
                    },
                    "intent": "salaire",
                    "confidence": 0.9,
                }
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom_recherche}** dans la base de données.",
                    "data": None,
                    "intent": "salaire",
                    "confidence": 0.7,
                }

        # Sinon, donner des statistiques générales
        else:
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

    def _handle_experience_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur l'expérience des consultants"""

        # Si un nom est mentionné, chercher ce consultant spécifique
        if entities["noms"]:
            nom_recherche: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom_recherche)

            if consultant:
                # Récupérer les informations d'expérience depuis la base de données
                try:
                    with get_database_session() as session:
                        consultant_db = (
                            session.query(Consultant)
                            .filter(Consultant.id == consultant.id)
                            .first()
                        )

                        if consultant_db:
                            if consultant_db.date_premiere_mission:
                                # Utiliser la propriété calculée du modèle
                                experience_annees = consultant_db.experience_annees

                                response = (
                                    "📊 **Expérience de "
                                    + consultant.prenom
                                    + " "
                                    + consultant.nom
                                    + self.SECTION_HEADER_SUFFIX
                                )
                                response += f"🚀 **Première mission :** {consultant_db.date_premiere_mission.strftime(self.DATE_FORMAT)}\n"
                                response += f"⏱️ **Expérience totale :** **{experience_annees} années**\n"

                                # Ajouter des informations contextuelles
                                if consultant_db.grade:
                                    response += (
                                        f"🎯 **Grade actuel :** {consultant_db.grade}\n"
                                    )

                                if consultant_db.societe:
                                    response += (
                                        f"🏢 **Société :** {consultant_db.societe}\n"
                                    )

                                if consultant_db.date_entree_societe:
                                    response += f"📅 **Date d'entrée société :** {consultant_db.date_entree_societe.strftime(self.DATE_FORMAT)}\n"

                                # Calculer l'ancienneté dans la société
                                if consultant_db.date_entree_societe:
                                    from datetime import date

                                    today = date.today()
                                    if consultant_db.date_sortie_societe:
                                        fin_periode = consultant_db.date_sortie_societe
                                    else:
                                        fin_periode = today
                                    delta_societe = (
                                        fin_periode - consultant_db.date_entree_societe
                                    )
                                    anciennete_societe = round(
                                        delta_societe.days / 365.25, 1
                                    )
                                    response += f"🏢 **Ancienneté société :** {anciennete_societe} années\n"

                                # Statut société
                                statut = consultant_db.statut_societe
                                if statut == "En poste":
                                    response += f"✅ **Statut :** {statut}"
                                elif statut == "Départ prévu":
                                    response += f"⚠️ **Statut :** {statut}"
                                else:
                                    response += f"❌ **Statut :** {statut}"

                            else:
                                response = f"❓ L'expérience de **{consultant.prenom} {consultant.nom}** ne peut pas être calculée car la date de première mission n'est pas renseignée."
                        else:
                            response = f"❌ Impossible de récupérer les données de **{consultant.prenom} {consultant.nom}**."

                except (ValueError, TypeError, AttributeError, KeyError) as e:
                    response = f"❌ Erreur lors de la récupération des données d'expérience : {str(e)}"

                return {
                    "response": response,
                    "data": {
                        "consultant": {
                            "nom": consultant.nom,
                            "prenom": consultant.prenom,
                            "experience_annees": (
                                getattr(consultant_db, "experience_annees", None)
                                if "consultant_db" in locals()
                                else None
                            ),
                            "date_premiere_mission": (
                                consultant_db.date_premiere_mission.isoformat()
                                if "consultant_db" in locals()
                                and consultant_db.date_premiere_mission
                                else None
                            ),
                            "grade": (
                                getattr(consultant_db, "grade", None)
                                if "consultant_db" in locals()
                                else None
                            ),
                            "societe": (
                                getattr(consultant_db, "societe", None)
                                if "consultant_db" in locals()
                                else None
                            ),
                        }
                    },
                    "intent": "experience",
                    "confidence": 0.9,
                }
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom_recherche}** dans la base de données.",
                    "data": None,
                    "intent": "experience",
                    "confidence": 0.7,
                }

        # Statistiques générales sur l'expérience
        else:
            try:
                with get_database_session() as session:
                    consultants_avec_experience = (
                        session.query(Consultant)
                        .filter(Consultant.date_premiere_mission.isnot(None))
                        .all()
                    )

                    if consultants_avec_experience:
                        experiences = [
                            c.experience_annees for c in consultants_avec_experience
                        ]

                        response = "📊 **Statistiques d'expérience :**\n\n"
                        response += f"• **Consultants avec expérience renseignée :** {len(consultants_avec_experience)}\n"
                        response += (
                            "• **Expérience moyenne :** "
                            + str(sum(experiences) / len(experiences))
                            + self.YEARS_SUFFIX
                        )
                        response += (
                            "• **Expérience minimum :** "
                            + str(min(experiences))
                            + self.YEARS_SUFFIX
                        )
                        response += (
                            "• **Expérience maximum :** "
                            + str(max(experiences))
                            + self.YEARS_SUFFIX
                        )

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

            return {
                "response": response,
                "data": {
                    "consultants_count": (
                        len(consultants_avec_experience)
                        if "consultants_avec_experience" in locals()
                        else 0
                    )
                },
                "intent": "experience",
                "confidence": 0.8,
            }

    def _get_profile_response_for_grade(self, consultant, consultant_db):
        """Retourne la réponse pour une question sur le grade"""
        return f"🎯 **Grade de {consultant.prenom} {consultant.nom}** : **{consultant_db.grade or 'Non renseigné'}**"

    def _get_profile_response_for_contract(self, consultant, consultant_db):
        """Retourne la réponse pour une question sur le type de contrat"""
        return f"📋 **Type de contrat de {consultant.prenom} {consultant.nom}** : **{consultant_db.type_contrat or 'Non renseigné'}**"

    def _get_profile_response_for_company(self, consultant, consultant_db):
        """Retourne la réponse pour une question sur la société"""
        response = f"🏢 **Société de {consultant.prenom} {consultant.nom}** : **{consultant_db.societe or 'Non renseigné'}**"
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
            response += f"📅 **Date d'entrée société :** {consultant_db.date_entree_societe.strftime(self.DATE_FORMAT)}\n"

        if consultant_db.date_sortie_societe:
            response += f"📅 **Date de sortie société :** {consultant_db.date_sortie_societe.strftime(self.DATE_FORMAT)}\n"
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

    def _handle_individual_profile_question(
        self, entities: Dict, question_lower: str
    ) -> Dict[str, Any]:
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
                consultant_db = (
                    session.query(Consultant)
                    .filter(Consultant.id == consultant.id)
                    .first()
                )

                if not consultant_db:
                    response = f"❌ Impossible de récupérer les données de **{consultant.prenom} {consultant.nom}**."
                else:
                    # Déterminer le type d'information demandée
                    if any(
                        word in question_lower
                        for word in ["grade", "niveau", "poste", "fonction"]
                    ):
                        response = self._get_profile_response_for_grade(
                            consultant, consultant_db
                        )
                    elif any(
                        word in question_lower
                        for word in ["contrat", "type contrat", "cdi", "cdd"]
                    ):
                        response = self._get_profile_response_for_contract(
                            consultant, consultant_db
                        )
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
                        response = self._get_profile_response_for_company(
                            consultant, consultant_db
                        )
                    else:
                        response = self._get_complete_profile_response(
                            consultant, consultant_db
                        )

        except (SQLAlchemyError, AttributeError, ValueError, TypeError) as e:
            response = f"❌ Erreur lors de la récupération du profil : {str(e)}"
            consultant_db = None

        return {
            "response": response,
            "data": {
                "consultant": {
                    "nom": consultant.nom,
                    "prenom": consultant.prenom,
                    "grade": (
                        getattr(consultant_db, "grade", None) if consultant_db else None
                    ),
                    "type_contrat": (
                        getattr(consultant_db, "type_contrat", None)
                        if consultant_db
                        else None
                    ),
                    "societe": (
                        getattr(consultant_db, "societe", None)
                        if consultant_db
                        else None
                    ),
                }
            },
            "intent": "profil_professionnel",
            "confidence": 0.9,
        }

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
                        # Statistiques par grade
                        consultants = (
                            session.query(Consultant)
                            .filter(Consultant.grade.isnot(None))
                            .all()
                        )

                        if consultants:
                            grades_count: Dict[str, List[Consultant]] = {}
                            for consultant in consultants:
                                grade = consultant.grade
                                if grade not in grades_count:
                                    grades_count[grade] = []
                                grades_count[grade].append(consultant)

                            response = "🎯 **Répartition par grade :**\n\n"
                            for grade, consultants_list in grades_count.items():
                                response += f"• **{grade}** : {len(consultants_list)} consultant(s)\n"
                                if (
                                    len(consultants_list) <= 5
                                ):  # Afficher les noms si pas trop nombreux
                                    for c in consultants_list:
                                        response += f"  - {c.prenom} {c.nom}\n"
                        else:
                            response = "❓ Aucun consultant n'a de grade renseigné."

                    elif any(
                        word in question_lower
                        for word in ["contrat", "cdi", "cdd", "stagiaire"]
                    ):
                        # Statistiques par type de contrat ou recherche spécifique
                        consultants = (
                            session.query(Consultant)
                            .filter(Consultant.type_contrat.isnot(None))
                            .all()
                        )

                        # Si c'est une question "combien de consultants en CDI/CDD"
                        if any(word in question_lower for word in ["combien"]):
                            if "cdi" in question_lower:
                                consultants_cdi = [
                                    c
                                    for c in consultants
                                    if c.type_contrat
                                    and c.type_contrat.upper() == "CDI"
                                ]
                                response = f"📋 **{len(consultants_cdi)} consultant(s) en CDI**"
                            elif "cdd" in question_lower:
                                consultants_cdd = [
                                    c
                                    for c in consultants
                                    if c.type_contrat
                                    and c.type_contrat.upper() == "CDD"
                                ]
                                response = f"📋 **{len(consultants_cdd)} consultant(s) en CDD**"
                            elif "stagiaire" in question_lower:
                                consultants_stagiaire = [
                                    c
                                    for c in consultants
                                    if c.type_contrat
                                    and c.type_contrat.lower() == "stagiaire"
                                ]
                                response = f"📋 **{len(consultants_stagiaire)} consultant(s) stagiaire(s)**"
                            else:
                                # Statistiques complètes
                                contrats_count: Dict[str, int] = {}
                                for consultant in consultants:
                                    contrat = consultant.type_contrat
                                    if contrat not in contrats_count:
                                        contrats_count[contrat] = 0
                                    contrats_count[contrat] += 1

                                response = "📋 **Nombre de consultants par type de contrat :**\n\n"
                                for contrat, count in contrats_count.items():
                                    response += (
                                        f"• **{contrat}** : {count} consultant(s)\n"
                                    )
                        else:
                            # Répartition complète par type de contrat
                            if consultants:
                                contrats_list: Dict[str, List[Consultant]] = {}
                                for consultant in consultants:
                                    contrat = consultant.type_contrat
                                    if contrat not in contrats_list:
                                        contrats_list[contrat] = []
                                    contrats_list[contrat].append(consultant)

                                response = (
                                    "📋 **Répartition par type de contrat :**\n\n"
                                )
                                for contrat, consultants_list in contrats_list.items():
                                    response += f"• **{contrat}** : {len(consultants_list)} consultant(s)\n"
                                    if (
                                        len(consultants_list) <= 5
                                    ):  # Afficher les noms si pas trop nombreux
                                        for c in consultants_list:
                                            response += f"  - {c.prenom} {c.nom}\n"
                            else:
                                response = "❓ Aucun consultant n'a de type de contrat renseigné."

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
                        # Statistiques par société ou recherche de consultants par
                        # société
                        consultants = (
                            session.query(Consultant)
                            .filter(Consultant.societe.isnot(None))
                            .all()
                        )

                        # Si c'est une recherche spécifique pour une société
                        if any(
                            word in question_lower for word in ["quanteam", "asigma"]
                        ):
                            societe_recherchee = (
                                "Quanteam" if "quanteam" in question_lower else "Asigma"
                            )
                            consultants_societe = [
                                c
                                for c in consultants
                                if c.societe
                                and c.societe.lower() == societe_recherchee.lower()
                            ]

                            if consultants_societe:
                                response = f"🏢 **Consultants chez {societe_recherchee}** :\n\n"
                                for i, consultant in enumerate(consultants_societe, 1):
                                    status_icon = (
                                        "🟢" if consultant.disponibilite else "🔴"
                                    )
                                    response += f"{i}. {status_icon} **{consultant.prenom} {consultant.nom}**"
                                    if consultant.grade:
                                        response += f" - {consultant.grade}"
                                    if consultant.type_contrat:
                                        response += f" ({consultant.type_contrat})"
                                    response += "\n"

                                response += (
                                    self.TOTAL_PREFIX
                                    + str(len(consultants_societe))
                                    + self.CONSULTANT_FOUND_SUFFIX
                                )
                            else:
                                response = f"❓ Aucun consultant trouvé chez {societe_recherchee}."
                        else:
                            # Statistiques générales par société
                            if consultants:
                                societes_count: Dict[str, List[Consultant]] = {}
                                for consultant in consultants:
                                    societe = consultant.societe
                                    if societe not in societes_count:
                                        societes_count[societe] = []
                                    societes_count[societe].append(consultant)

                                response = "🏢 **Répartition par société :**\n\n"
                                for societe, consultants_list in societes_count.items():
                                    response += f"• **{societe}** : {len(consultants_list)} consultant(s)\n"
                                    if (
                                        len(consultants_list) <= 5
                                    ):  # Afficher les noms si pas trop nombreux
                                        for c in consultants_list:
                                            response += f"  - {c.prenom} {c.nom}\n"
                            else:
                                response = (
                                    "❓ Aucun consultant n'a de société renseignée."
                                )

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

    def _handle_skills_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les compétences"""

        # Détecter le type de compétences demandé
        question_lower: str = self.last_question.lower()
        type_competence = None

        if any(
            word in question_lower
            for word in [
                "compétences techniques",
                "technique",
                "technologie",
                "programmation",
            ]
        ):
            type_competence = "technique"
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
            type_competence = "fonctionnelle"

        # Si une compétence spécifique est mentionnée
        if entities["competences"]:
            competence: str = entities["competences"][0]
            consultants = self._find_consultants_by_skill(competence, type_competence)

            if consultants:
                noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
                response = f"🎯 Consultants maîtrisant **{competence.title()}** :\n\n"
                response += "\n".join([f"• {nom}" for nom in noms])

                # Ajouter les détails des compétences
                response += (
                    self.STATS_PREFIX
                    + str(len(consultants))
                    + self.CONSULTANT_FOUND_SUFFIX
                )
            else:
                response = (
                    f"❌ Aucun consultant ne maîtrise **{competence}** dans notre base."
                )

            return {
                "response": response,
                "data": {
                    "consultants": [
                        {"nom": c.nom, "prenom": c.prenom} for c in consultants
                    ]
                },
                "intent": "competences",
                "confidence": 0.9,
            }

        # Recherche dynamique de compétence dans la question
        elif any(
            word in question_lower
            for word in ["qui maîtrise", "qui sait", "qui connaît", "qui connait"]
        ):
            # Extraire le nom de la compétence après le verbe

            # Chercher tous les mots après "maîtrise", "sait", "connaît"
            patterns = [
                r"qui\s+maîtrise\s+(.+?)(?:\?|$)",
                r"qui\s+sait\s+(.+?)(?:\?|$)",
                r"qui\s+connaît\s+(.+?)(?:\?|$)",
                r"qui\s+connait\s+(.+?)(?:\?|$)",
                r"qui\s+a\s+(.+?)(?:\?|$)",
                r"qui\s+possède\s+(.+?)(?:\?|$)",
            ]

            competence_found = None
            for pattern in patterns:
                match = re.search(pattern, question_lower)
                if match:
                    competence_found = match.group(1).strip()
                    # Nettoyer les articles et prépositions
                    competence_found = re.sub(
                        r"^(le|la|les|du|de|des|en|une?)\s+", "", competence_found
                    )
                    competence_found = re.sub(
                        r"\s+(compétence|skill)s?$", "", competence_found
                    )
                    break

            if competence_found:
                consultants = self._find_consultants_by_skill(
                    competence_found, type_competence
                )

                if consultants:
                    noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
                    response = f"🎯 Consultants maîtrisant **{competence_found.title()}** :\n\n"
                    response += "\n".join([f"• {nom}" for nom in noms])
                    response += (
                        "\n\n📊 **"
                        + str(len(consultants))
                        + " consultant(s) trouvé(s)**"
                    )
                else:
                    response = f"❌ Aucun consultant ne maîtrise **{competence_found}** dans notre base."

                return {
                    "response": response,
                    "data": {
                        "consultants": [
                            {"nom": c.nom, "prenom": c.prenom} for c in consultants
                        ]
                    },
                    "intent": "competences",
                    "confidence": 0.8,
                }

        # Question générale sur les compétences d'un consultant
        elif entities["noms"]:
            nom: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)

            if consultant:
                skills = self._get_consultant_skills(consultant.id, type_competence)

                if skills:
                    response = f"🎯 **Compétences de {consultant.prenom} {consultant.nom} :**\n\n"

                    # Grouper par catégorie
                    categories: Dict[str, List[Dict[str, Any]]] = {}
                    for skill in skills:
                        categorie = skill["categorie"] or "Autre"
                        if categorie not in categories:
                            categories[categorie] = []
                        categories[categorie].append(skill)

                    # Afficher par catégorie
                    for categorie, competences in categories.items():
                        response += f"**🔹 {categorie.title()} :**\n"
                        for comp in competences:
                            niveau_emoji = {
                                "debutant": "🟡",
                                "intermediaire": "🟠",
                                "expert": "🔴",
                            }.get(comp["niveau_maitrise"], "⚪")

                            experience_text = ""
                            if (
                                comp["annees_experience"]
                                and comp["annees_experience"] > 0
                            ):
                                if comp["annees_experience"] == 1:
                                    experience_text = (
                                        f" ({comp['annees_experience']} an)"
                                    )
                                else:
                                    experience_text = (
                                        f" ({comp['annees_experience']:.0f} ans)"
                                    )

                            response += f"  {niveau_emoji} **{comp['nom']}** - {comp['niveau_maitrise'].title()}{experience_text}\n"
                        response += "\n"

                    response += f"📊 **Total : {len(skills)} compétence(s)**"
                else:
                    response = f"❌ Aucune compétence enregistrée pour **{consultant.prenom} {consultant.nom}**."
            else:
                response = f"❌ Consultant **{nom}** introuvable."

            return {
                "response": response,
                "data": {
                    "consultant": consultant.nom if consultant else None,
                    "skills_count": len(skills) if consultant else 0,
                },
                "intent": "competences",
                "confidence": 0.9,
            }

        return {
            "response": "🤔 Pouvez-vous préciser quelle compétence ou quel consultant vous intéresse ?",
            "data": None,
            "intent": "competences",
            "confidence": 0.5,
        }

    def _handle_languages_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les langues parlées par les consultants"""

        # Si une langue spécifique est mentionnée
        if entities["langues"]:
            langue_recherchee: str = entities["langues"][0]
            consultants = self._find_consultants_by_language(langue_recherchee)

            if consultants:
                noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
                response = (
                    f"🌍 Consultants parlant **{langue_recherchee.title()}** :\n\n"
                )
                response += "\n".join([f"• {nom}" for nom in noms])

                # Ajouter les détails des niveaux
                response += (
                    "\n\n📊 **" + str(len(consultants)) + " consultant(s) trouvé(s)**"
                )

                # Détails des niveaux si moins de 5 consultants
                if len(consultants) <= 5:
                    response += "\n\n🎯 **Niveaux détaillés :**"
                    for consultant in consultants:
                        for cl in consultant.langues:
                            if cl.langue.nom.lower() == langue_recherchee.lower():
                                response += f"\n  • **{consultant.prenom} {consultant.nom}** : {cl.niveau_label}"
                                if cl.commentaire:
                                    response += f" - {cl.commentaire}"
                                break

                return {
                    "response": response,
                    "data": {
                        "consultants": [
                            {"nom": c.nom, "prenom": c.prenom} for c in consultants
                        ]
                    },
                    "intent": "langues",
                    "confidence": 0.9,
                }
            else:
                response = f"❌ Aucun consultant ne parle **{langue_recherchee}** dans notre base."
                return {
                    "response": response,
                    "data": {"consultants": []},
                    "intent": "langues",
                    "confidence": 0.8,
                }

        # Question générale sur les langues d'un consultant (vérifier en premier)
        elif entities["noms"] or any(
            word in self.last_question.lower()
            for word in ["quelles langues", "langues de", "langues parlées"]
        ):
            # Si pas de nom détecté dans entities, essayer d'extraire manuellement
            nom: Optional[str] = None
            if entities["noms"]:
                nom = entities["noms"][0]
            else:
                # Extraire le nom après "langues parle" ou "langues de"
                patterns = [
                    r"quelles?\s+langues?\s+parle\s+(\w+)",
                    r"langues?\s+parle\s+(\w+)",
                    r"langues?\s+de\s+(\w+)",
                    r"(\w+)\s+parle\s+quelles?\s+langues?",
                    r"quelles?\s+sont\s+les\s+langues?\s+de\s+(\w+)",
                ]

                for pattern in patterns:
                    match = re.search(pattern, self.last_question.lower())
                    if match:
                        nom = match.group(1)
                        break

            if nom:
                consultant = self._find_consultant_by_name(nom)

                if consultant:
                    if consultant.langues:
                        response = (
                            "🌍 **Langues parlées par "
                            + consultant.prenom
                            + " "
                            + consultant.nom
                            + " :**\n\n"
                        )

                        for cl in consultant.langues:
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
                                "HI": "🇮🇳",
                            }
                            emoji = flag_emoji.get(cl.langue.code_iso, "🌍")
                            response += (
                                f"  {emoji} **{cl.langue.nom}** - {cl.niveau_label}"
                            )
                            if cl.commentaire:
                                response += f" - {cl.commentaire}"
                            response += "\n"

                        response += (
                            "\n📊 **Total : "
                            + str(len(consultant.langues))
                            + " langue(s)**"
                        )
                    else:
                        response = f"❌ Aucune langue enregistrée pour **{consultant.prenom} {consultant.nom}**."
                else:
                    response = f"❌ Consultant **{nom}** introuvable."

                return {
                    "response": response,
                    "data": {
                        "consultant": consultant.nom if consultant else None,
                        "languages_count": len(consultant.langues) if consultant else 0,
                    },
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

        # Recherche dynamique de langue dans la question
        elif any(
            word in self.last_question.lower()
            for word in ["qui parle", "parle", "parlent", "bilingue"]
        ):
            # Extraire le nom de la langue après "parle"
            question_lower: str = self.last_question.lower()

            patterns = [
                r"qui\s+parle\s+(.+?)(?:\?|$)",
                r"parlent\s+(.+?)(?:\?|$)",
                r"qui.+parle.+(.+?)(?:\?|$)",
            ]

            langue_found = None
            for pattern in patterns:
                match = re.search(pattern, question_lower)
                if match:
                    langue_found = match.group(1).strip()
                    # Nettoyer les articles
                    langue_found = re.sub(
                        r"^(le|la|les|du|de|des|en|une?)\s+", "", langue_found
                    )
                    break

            if langue_found:
                consultants = self._find_consultants_by_language(langue_found)

                if consultants:
                    noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
                    response = (
                        f"🌍 Consultants parlant **{langue_found.title()}** :\n\n"
                    )
                    response += "\n".join([f"• {nom}" for nom in noms])
                    response += (
                        "\n\n📊 **"
                        + str(len(consultants))
                        + " consultant(s) trouvé(s)**"
                    )
                else:
                    response = f"❌ Aucun consultant ne parle **{langue_found}** dans notre base."

                return {
                    "response": response,
                    "data": {
                        "consultants": (
                            [{"nom": c.nom, "prenom": c.prenom} for c in consultants]
                            if consultants
                            else []
                        )
                    },
                    "intent": "langues",
                    "confidence": 0.8,
                }

        # Question générale sur les langues
        return {
            "response": '🌍 Pour connaître les langues d\'un consultant, demandez : "Quelles langues parle [nom] ?"\n\nOu pour trouver qui parle une langue : "Qui parle anglais ?"',
            "data": {},
            "intent": "langues",
            "confidence": 0.6,
        }

    def _handle_missions_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les missions"""

        # Détecter si c'est une question sur le nombre de missions
        question_lower: str = self.last_question.lower()
        is_count_question = any(
            word in question_lower for word in ["combien", "nombre"]
        )

        if entities["entreprises"]:
            entreprise: str = entities["entreprises"][0]
            missions = self._get_missions_by_company(entreprise)

            if is_count_question:
                response = (
                    "📊 **"
                    + str(len(missions))
                    + " mission(s)** trouvée(s) chez **"
                    + entreprise.title()
                    + "**"
                )
            elif missions:
                response = f"🏢 **Missions chez {entreprise.title()} :**\n\n"
                for mission in missions[:5]:  # Limiter à 5 résultats
                    consultant_nom = (
                        f"{mission.consultant.prenom} {mission.consultant.nom}"
                    )
                    response += f"• **{consultant_nom}** - {mission.nom_mission} ({mission.date_debut.strftime('%Y')})\n"

                if len(missions) > 5:
                    response += f"\n... et {len(missions) - 5} autres missions"

                response += "\n\n📊 **Total : " + str(len(missions)) + " mission(s)**"
            else:
                response = f"❌ Aucune mission trouvée chez **{entreprise}**."

            return {
                "response": response,
                "data": {"missions": len(missions), "entreprise": entreprise},
                "intent": "missions",
                "confidence": 0.9,
            }

        elif entities["noms"]:
            nom: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)

            if consultant:
                missions = self._get_missions_by_consultant(consultant.id)

                if is_count_question:
                    # Question spécifique sur le nombre
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
                        missions_en_cours = [
                            m for m in missions if m.statut == "en_cours"
                        ]
                        if missions_en_cours:
                            response += (
                                " (dont " + str(len(missions_en_cours)) + " en cours)"
                            )
                elif missions:
                    response = (
                        f"💼 **Missions de {consultant.prenom} {consultant.nom} :**\n\n"
                    )
                    for mission in missions:
                        status_icon = "🟢" if mission.statut == "en_cours" else "✅"
                        response += f"{status_icon} **{mission.client}** - {mission.nom_mission}\n"
                        response += f"   📅 {mission.date_debut.strftime('%m/%Y')} → "
                        if mission.date_fin:
                            response += f"{mission.date_fin.strftime('%m/%Y')}"
                        else:
                            response += "En cours"
                        if mission.taux_journalier:
                            response += (
                                " | 💰 " + str(mission.taux_journalier) + "€/jour"
                            )
                        response += "\n\n"

                    response += "📊 **Total : " + str(len(missions)) + " mission(s)**"
                else:
                    response = f"❌ Aucune mission trouvée pour **{consultant.prenom} {consultant.nom}**."
            else:
                response = f"❌ Consultant **{nom}** introuvable."

            return {
                "response": response,
                "data": {
                    "consultant": nom,
                    "missions_count": len(missions) if consultant else 0,
                },
                "intent": "missions",
                "confidence": 0.9,
            }

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
            if (
                "consultant" in self.last_question
                and "mission" not in self.last_question
            ):
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

        if entities["noms"]:
            nom: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)

            if consultant:
                # Déterminer le type d'information demandée
                question_lower: str = self.last_question.lower()

                if any(word in question_lower for word in ["mail", "email", "e-mail"]):
                    if consultant.email:
                        response = f"📧 L'email de **{consultant.prenom} {consultant.nom}** est : **{consultant.email}**"
                    else:
                        response = f"❓ Désolé, l'email de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."

                elif any(
                    word in question_lower for word in ["téléphone", "tel", "numéro"]
                ):
                    if consultant.telephone:
                        response = f"📞 Le téléphone de **{consultant.prenom} {consultant.nom}** est : **{consultant.telephone}**"
                    else:
                        response = f"❓ Désolé, le téléphone de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."

                else:
                    # Information de contact complète
                    response = (
                        f"📞 **Contact de {consultant.prenom} {consultant.nom} :**\n\n"
                    )
                    response += (
                        f"📧 Email : **{consultant.email or 'Non renseigné'}**\n"
                    )
                    response += (
                        f"📞 Téléphone : **{consultant.telephone or 'Non renseigné'}**"
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
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom}** dans la base de données.",
                    "data": None,
                    "intent": "contact",
                    "confidence": 0.7,
                }

        return {
            "response": "🤔 De quel consultant souhaitez-vous connaître les coordonnées ?",
            "data": None,
            "intent": "contact",
            "confidence": 0.5,
        }

    def _handle_list_consultants_question(self) -> Dict[str, Any]:
        """Gère les questions pour lister les consultants selon des critères"""

        question_lower: str = self.last_question.lower()

        # Déterminer le filtre à appliquer
        if "disponibles" in question_lower or "disponible" in question_lower:
            with get_database_session() as session:
                consultants = (
                    session.query(Consultant).filter(Consultant.disponibilite).all()
                )
            titre = "👥 **Consultants disponibles :**"
        elif "indisponibles" in question_lower or "indisponible" in question_lower:
            with get_database_session() as session:
                consultants = (
                    session.query(Consultant)
                    .filter(Consultant.disponibilite is False)
                    .all()
                )
            titre = "👥 **Consultants indisponibles :**"
        elif "actifs" in question_lower or "actif" in question_lower:
            with get_database_session() as session:
                consultants = (
                    session.query(Consultant).filter(Consultant.disponibilite).all()
                )
            _ = "👥 **Consultants actifs :**"
        else:
            # Tous les consultants
            with get_database_session() as session:

                consultants = session.query(Consultant).all()
            titre = "👥 **Tous les consultants :**"

        if not consultants:
            return {
                "response": "❓ Aucun consultant ne correspond à ce critère.",
                "data": None,
                "intent": "liste_consultants",
                "confidence": 0.8,
            }

        # Construire la réponse
        response = f"{titre}\n\n"

        for i, consultant in enumerate(consultants, 1):
            status_icon = "🟢" if consultant.disponibilite else "🔴"
            response += f"{i}. {status_icon} **{consultant.prenom} {consultant.nom}**"

            if consultant.email:
                response += f" - {consultant.email}"

            if consultant.salaire_actuel:
                cjm = consultant.salaire_actuel * 1.8 / 216
                response += (
                    f" - {consultant.salaire_actuel:,.0f} €/an - CJM: {cjm:,.0f} €"
                )

            response += "\n"

        response += "\n📊 **Total : " + str(len(consultants)) + " consultant(s)**"

        return {
            "response": response,
            "data": {
                "consultants": [
                    {
                        "nom": c.nom,
                        "prenom": c.prenom,
                        "email": c.email,
                        "disponibilite": c.disponibilite,
                        "salaire": c.salaire_actuel,
                        "cjm": (
                            (c.salaire_actuel * 1.8 / 216) if c.salaire_actuel else None
                        ),
                    }
                    for c in consultants
                ],
                "count": len(consultants),
            },
            "intent": "liste_consultants",
            "confidence": 0.9,
        }

    def _handle_consultant_search(self, entities: Dict) -> Dict[str, Any]:
        """Gère la recherche d'informations sur un consultant"""

        if entities["noms"]:
            nom: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)

            if consultant:
                response = f"""👤 **{consultant.prenom} {consultant.nom}**

📧 Email : {consultant.email or 'Non renseigné'}
📞 Téléphone : {consultant.telephone or 'Non renseigné'}
📊 Disponibilité : **{'Disponible' if consultant.disponibilite else 'Indisponible'}**
📅 Date création : {consultant.date_creation.strftime('%d/%m/%Y') if consultant.date_creation else 'Non renseignée'}"""

                if consultant.salaire_actuel:
                    cjm = consultant.salaire_actuel * 1.8 / 216
                    response += (
                        "\n💰 Salaire : **"
                        + f"{consultant.salaire_actuel:,.0f}"
                        + " €**"
                    )
                    response += "\n📈 CJM : **" + f"{cjm:,.0f}" + " €**"

                # Ajouter info sur les missions
                missions_count = len(consultant.missions)
                if missions_count > 0:
                    response += f"\n💼 Missions : **{missions_count}** mission(s)"
            else:
                response = (
                    f"❌ Consultant **{nom}** introuvable dans la base de données."
                )

            return {
                "response": response,
                "data": {"consultant": consultant.nom if consultant else None},
                "intent": "recherche_consultant",
                "confidence": 0.9,
            }

        return {
            "response": "🤔 De quel consultant souhaitez-vous connaître les informations ?",
            "data": None,
            "intent": "recherche_consultant",
            "confidence": 0.5,
        }

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

        Args:
            entities: Dictionnaire contenant les entités extraites de la question
                     (noms, entreprises, compétences, langues, etc.)

        Returns:
            Dictionnaire contenant :
            - response: Réponse formatée pour l'utilisateur
            - data: Données structurées sur les practices
            - intent: Type d'intention détecté ("practices")
            - confidence: Niveau de confiance de la réponse (0.0 à 1.0)

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données
            AttributeError: Si les données de practice sont malformées

        Example:
            >>> entities = {"practices": ["Data"]}
            >>> result = chatbot._handle_practices_question(entities)
            >>> print(result["response"])
            👥 **Practice Data** :
            📋 **5 consultant(s)** :
            1. 🟢 **Jean Dupont** - CJM: 450 €
            ...
        """
        from database.models import Practice

        # Si une practice spécifique est mentionnée
        if entities["practices"]:
            practice_name: str = entities["practices"][0]
            with get_database_session() as session:
                practice = (
                    session.query(Practice)
                    .filter(func.lower(Practice.nom) == practice_name.lower())
                    .first()
                )

            if practice:
                # Récupérer les consultants de cette practice
                consultants = list(practice.consultants)

                if consultants:
                    response = f"👥 **Practice {practice.nom}** :\n\n"
                    response += f"📋 **{len(consultants)} consultant(s)** :\n"

                    for i, consultant in enumerate(consultants, 1):
                        status_icon = "🟢" if consultant.disponibilite else "🔴"
                        cjm = (
                            (consultant.salaire_actuel * 1.8 / 216)
                            if consultant.salaire_actuel
                            else 0
                        )
                        response += f"{i}. {status_icon} **{consultant.prenom} {consultant.nom}**"
                        if consultant.salaire_actuel:
                            response += f" - CJM: {cjm:,.0f} €"
                        response += "\n"

                    if practice.responsable:
                        response += f"\n👨‍💼 **Responsable** : {practice.responsable}"
                else:
                    response = (
                        f"📋 **Practice {practice.nom}** : Aucun consultant assigné"
                    )

                return {
                    "response": response,
                    "data": {
                        "practice": practice.nom,
                        "consultants": [
                            {
                                "nom": c.nom,
                                "prenom": c.prenom,
                                "disponibilite": c.disponibilite,
                                "cjm": (
                                    (c.salaire_actuel * 1.8 / 216)
                                    if c.salaire_actuel
                                    else None
                                ),
                            }
                            for c in consultants
                        ],
                    },
                    "intent": "practices",
                    "confidence": 0.9,
                }
            else:
                return {
                    "response": f"❌ Practice **{practice_name}** introuvable dans la base.",
                    "data": None,
                    "intent": "practices",
                    "confidence": 0.7,
                }

        # Question générale sur les practices
        else:
            with get_database_session() as session:

                practices = session.query(Practice).filter(Practice.actif).all()

            if practices:
                response = "🏢 **Practices disponibles** :\n\n"

                for practice in practices:
                    nb_consultants = len(list(practice.consultants))
                    nb_disponibles = len(
                        [c for c in practice.consultants if c.disponibilite]
                    )

                    response += f"• **{practice.nom}** : {nb_consultants} consultant(s) ({nb_disponibles} disponible(s))\n"
                    if practice.responsable:
                        response += f"  👨‍💼 Responsable : {practice.responsable}\n"

                return {
                    "response": response,
                    "data": {
                        "practices": [
                            {
                                "nom": p.nom,
                                "consultants_total": len(list(p.consultants)),
                                "consultants_disponibles": len(
                                    [c for c in p.consultants if c.disponibilite]
                                ),
                                "responsable": p.responsable,
                            }
                            for p in practices
                        ]
                    },
                    "intent": "practices",
                    "confidence": 0.8,
                }
            else:
                return {
                    "response": "❓ Aucune practice active trouvée dans la base.",
                    "data": None,
                    "intent": "practices",
                    "confidence": 0.6,
                }

    def _handle_cvs_question(self, entities: Dict) -> Dict[str, Any]:
        """
        Gère les questions sur les CVs des consultants.

        Args:
            entities: Dictionnaire contenant les entités extraites de la question
                     (noms, entreprises, compétences, langues, etc.)

        Returns:
            Dictionnaire contenant :
            - response: Réponse formatée sur les CVs
            - data: Données structurées sur les CVs
            - intent: Type d'intention détecté ("cvs")
            - confidence: Niveau de confiance de la réponse (0.0 à 1.0)

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données
            AttributeError: Si les données de CV sont malformées

        Example:
            >>> entities = {"noms": ["Jean Dupont"]}
            >>> result = chatbot._handle_cvs_question(entities)
            >>> print(result["response"])
            📁 **CVs de Jean Dupont** :
            1. **CV_Jean_Dupont.pdf**
               📅 Uploadé le : 15/01/2024
               📏 Taille : 2.5 MB
               ✅ Contenu analysé
            📊 **Total : 1 document(s)**
        """
        from database.models import CV

        # Si un consultant spécifique est mentionné
        if entities["noms"]:
            nom_recherche: str = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom_recherche)

            if consultant:
                cvs = consultant.cvs

                if cvs:
                    response = (
                        "📁 **CVs de "
                        + consultant.prenom
                        + " "
                        + consultant.nom
                        + "** :\n\n"
                    )

                    for i, cv in enumerate(cvs, 1):
                        taille_mb = (
                            (cv.taille_fichier / 1024 / 1024)
                            if cv.taille_fichier
                            else 0
                        )
                        date_upload = (
                            cv.date_upload.strftime("%d/%m/%Y")
                            if cv.date_upload
                            else "N/A"
                        )

                        response += str(i) + ". **" + cv.fichier_nom + "**\n"
                        response += "   📅 Uploadé le : " + date_upload + "\n"
                        response += "   📏 Taille : " + str(taille_mb) + " MB\n"
                        if cv.contenu_extrait:
                            response += "   ✅ Contenu analysé\n"
                        response += "\n"

                    response += "📊 **Total : " + str(len(cvs)) + " document(s)**"
                else:
                    response = (
                        "📁 **"
                        + consultant.prenom
                        + " "
                        + consultant.nom
                        + "** : Aucun CV uploadé"
                    )

                return {
                    "response": response,
                    "data": {
                        "consultant": f"{consultant.prenom} {consultant.nom}",
                        "cvs": [
                            {
                                "nom": cv.fichier_nom,
                                "date_upload": (
                                    cv.date_upload.isoformat()
                                    if cv.date_upload
                                    else None
                                ),
                                "taille": cv.taille_fichier,
                                "contenu_analyse": bool(cv.contenu_extrait),
                            }
                            for cv in cvs
                        ],
                    },
                    "intent": "cvs",
                    "confidence": 0.9,
                }
            else:
                return {
                    "response": f"❌ Consultant **{nom_recherche}** introuvable.",
                    "data": None,
                    "intent": "cvs",
                    "confidence": 0.7,
                }

        # Question générale sur les CVs
        else:
            with get_database_session() as session:

                cvs_total = session.query(CV).count()
            with get_database_session() as session:

                consultants_avec_cv = (
                    session.query(Consultant).join(CV).distinct().count()
                )

            response = "📁 **Statistiques des CVs** :\n\n"
            response += "• Total de documents : **" + str(cvs_total) + "**\n"
            response += "• Consultants avec CV : **" + str(consultants_avec_cv) + "**\n"

            # Top 3 consultants avec le plus de CVs
            from sqlalchemy import func

            with get_database_session() as session:

                top_consultants = session.query(
                    Consultant,
                    func.count(CV.id)
                    .label("nb_cvs")
                    .join(CV)
                    .group_by(Consultant.id)
                    .order_by(func.count(CV.id).desc())
                    .limit(3)
                    .all(),
                )

            if top_consultants:
                response += "\n🏆 **Top consultants (nombre de CVs)** :\n"
                for consultant, nb_cvs in top_consultants:
                    response += (
                        "• **"
                        + consultant.prenom
                        + " "
                        + consultant.nom
                        + "** : "
                        + str(nb_cvs)
                        + " CV(s)\n"
                    )

            return {
                "response": response,
                "data": {
                    "cvs_total": cvs_total,
                    "consultants_avec_cv": consultants_avec_cv,
                    "top_consultants": [
                        {"nom": c.nom, "prenom": c.prenom, "nb_cvs": nb}
                        for c, nb in top_consultants
                    ],
                },
                "intent": "cvs",
                "confidence": 0.8,
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
                .filter(
                    or_(
                        func.lower(Consultant.nom) == nom_recherche.lower(),
                        func.lower(Consultant.prenom) == nom_recherche.lower(),
                        func.lower(func.concat(Consultant.prenom, " ", Consultant.nom))
                        == nom_recherche.lower(),
                        func.lower(func.concat(Consultant.nom, " ", Consultant.prenom))
                        == nom_recherche.lower(),
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
                .filter(
                    or_(
                        func.lower(Consultant.nom).like(f"%{nom_recherche.lower()}%"),
                        func.lower(Consultant.prenom).like(
                            f"%{nom_recherche.lower()}%"
                        ),
                    )
                )
                .first()
            )

        return consultant

    def _find_consultants_by_skill(
        self, competence: str, type_competence: Optional[str] = None
    ) -> List[Any]:
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
                .filter(  # type: ignore[no-any-return]
                    func.lower(Mission.client).like(f"%{entreprise.lower()}%")
                )
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
                .filter(  # type: ignore[no-any-return]
                    Mission.consultant_id == consultant_id
                )
                .order_by(Mission.date_debut.desc())
                .all()
            )

    def _get_consultant_skills(
        self, consultant_id: int, type_competence: Optional[str] = None
    ) -> List[Dict[str, Any]]:
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

        Récupère des métriques complètes sur consultants, missions, practices,
        CVs et données financières.

        Returns:
            Dictionnaire contenant toutes les statistiques :
            - consultants_total: Nombre total de consultants
            - consultants_actifs: Nombre de consultants disponibles
            - consultants_inactifs: Nombre de consultants indisponibles
            - missions_total: Nombre total de missions
            - missions_en_cours: Nombre de missions en cours
            - missions_terminees: Nombre de missions terminées
            - practices_total: Nombre de practices actives
            - cvs_total: Nombre total de CVs
            - consultants_avec_cv: Nombre de consultants avec au moins un CV
            - tjm_moyen: TJM moyen des missions
            - salaire_moyen: Salaire moyen des consultants
            - cjm_moyen: CJM moyen calculé

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données

        Example:
            >>> stats = chatbot._get_general_stats()
            >>> print(f"Base: {stats['consultants_total']} consultants")
            >>> print(f"Missions: {stats['missions_total']} total")
            >>> print(f"TJM moyen: {stats['tjm_moyen']:.0f} €")
        """
        from database.models import CV
        from database.models import Practice

        # Consultants
        with get_database_session() as session:

            consultants_total = session.query(Consultant).count()
        with get_database_session() as session:

            consultants_actifs = (
                session.query(Consultant).filter(Consultant.disponibilite).count()
            )
        consultants_inactifs = consultants_total - consultants_actifs

        # Missions
        with get_database_session() as session:

            missions_total = session.query(Mission).count()
        with get_database_session() as session:

            missions_en_cours = (
                session.query(Mission).filter(Mission.statut == "en_cours").count()
            )
        missions_terminees = missions_total - missions_en_cours

        # Practices
        with get_database_session() as session:

            practices_total = session.query(Practice).filter(Practice.actif).count()

        # CVs
        with get_database_session() as session:

            cvs_total = session.query(CV).count()
        with get_database_session() as session:

            consultants_avec_cv = session.query(Consultant).join(CV).distinct().count()

        # TJM moyen
        with get_database_session() as session:

            tjm_moyen = (
                session.query(func.avg(Mission.taux_journalier))
                .filter(Mission.taux_journalier.isnot(None))
                .scalar()
                or 0
            )

        # Salaire moyen et CJM moyen
        with get_database_session() as session:

            salaire_moyen = (
                session.query(func.avg(Consultant.salaire_actuel))
                .filter(Consultant.salaire_actuel.isnot(None))
                .scalar()
                or 0
            )
        cjm_moyen = (salaire_moyen * 1.8 / 216) if salaire_moyen > 0 else 0

        return {
            "consultants_total": consultants_total,
            "consultants_actifs": consultants_actifs,
            "consultants_inactifs": consultants_inactifs,
            "missions_total": missions_total,
            "missions_en_cours": missions_en_cours,
            "missions_terminees": missions_terminees,
            "practices_total": practices_total,
            "cvs_total": cvs_total,
            "consultants_avec_cv": consultants_avec_cv,
            "tjm_moyen": tjm_moyen,
            "salaire_moyen": salaire_moyen,
            "cjm_moyen": cjm_moyen,
        }

    def _handle_availability_question(self, entities: Dict) -> Dict[str, Any]:
        """
        Gère les questions sur la disponibilité des consultants (V1.2.2).

        Analyse la disponibilité immédiate (ASAP) ou planifiée des consultants,
        en tenant compte des missions en cours qui peuvent retarder la disponibilité.

        Args:
            entities: Dictionnaire contenant les entités extraites de la question
                     (noms, entreprises, compétences, langues, etc.)

        Returns:
            Dictionnaire contenant :
            - response: Réponse formatée sur la disponibilité
            - data: Données structurées sur la disponibilité
            - intent: Type d'intention détecté ("disponibilite")
            - confidence: Niveau de confiance de la réponse (0.0 à 1.0)

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données
            AttributeError: Si les données de disponibilité sont malformées

        Example:
            >>> entities = {"noms": ["Jean Dupont"]}
            >>> result = chatbot._handle_availability_question(entities)
            >>> print(result["response"])
            📅 **Disponibilité de Jean Dupont** :
            ✅ **Disponible immédiatement (ASAP)**
            📊 **Statut actuel :** ✅ Marqué disponible
        """
        # Chercher un consultant spécifique

        # Chercher un consultant spécifique
        consultant = None
        if entities["noms"]:
            nom_complet = " ".join(entities["noms"])
            consultant = self._find_consultant_by_name(nom_complet)

        if consultant:
            try:
                # Récupérer les données de disponibilité
                with get_database_session() as session:

                    consultant_db = (
                        session.query(Consultant)
                        .filter(Consultant.id == consultant.id)
                        .first()
                    )

                if consultant_db:
                    response = (
                        "📅 **Disponibilité de "
                        + consultant.prenom
                        + " "
                        + consultant.nom
                        + "** :\n\n"
                    )

                    # Date de disponibilité calculée
                    date_dispo = consultant_db.date_disponibilite
                    if date_dispo == "ASAP":
                        response += "✅ **Disponible immédiatement (ASAP)**\n\n"

                        # Vérifier s'il y a des missions en cours
                        missions_en_cours = [
                            m for m in consultant_db.missions if m.statut == "en_cours"
                        ]
                        if missions_en_cours:
                            response += "⚠️ **Attention :** Le consultant a des missions en cours mais est marqué disponible\n"
                            for mission in missions_en_cours:
                                response += (
                                    "   • "
                                    + mission.nom_mission
                                    + " chez "
                                    + mission.client
                                    + "\n"
                                )
                    else:
                        response += (
                            "📅 **Disponible à partir du :** "
                            + str(date_dispo)
                            + "\n\n"
                        )

                        # Afficher les missions qui retardent la disponibilité
                        from datetime import date

                        missions_futures = [
                            m
                            for m in consultant_db.missions
                            if m.date_fin and m.date_fin > date.today()
                        ]
                        if missions_futures:
                            response += "🎯 **Missions en cours/planifiées :**\n"
                            for mission in missions_futures:
                                fin_mission = mission.date_fin.strftime("%d/%m/%Y")
                                response += (
                                    "   • "
                                    + mission.nom_mission
                                    + " (fin: "
                                    + fin_mission
                                    + ")\n"
                                )

                    # Statut général
                    response += "\n📊 **Statut actuel :** "
                    if consultant_db.disponibilite:
                        response += "✅ Marqué disponible"
                    else:
                        response += "🔴 Marqué occupé"

                    # Informations complémentaires
                    if consultant_db.grade:
                        response += "\n🎯 **Grade :** " + str(consultant_db.grade)
                    if consultant_db.type_contrat:
                        response += "\n📝 **Contrat :** " + str(
                            consultant_db.type_contrat
                        )

                else:
                    response = (
                        "❌ Impossible de récupérer les données de disponibilité pour **"
                        + consultant.prenom
                        + " "
                        + consultant.nom
                        + "**."
                    )

            except (SQLAlchemyError, AttributeError, ValueError, TypeError) as e:
                response = (
                    "❌ Erreur lors de la récupération des données de disponibilité : "
                    + str(e)
                )

            return {
                "response": response,
                "data": {
                    "consultant": {
                        "nom": consultant.nom,
                        "prenom": consultant.prenom,
                        "date_disponibilite": (
                            getattr(consultant_db, "date_disponibilite", None)
                            if "consultant_db" in locals()
                            else None
                        ),
                        "disponibilite_immediate": (
                            getattr(consultant_db, "disponibilite", None)
                            if "consultant_db" in locals()
                            else None
                        ),
                    }
                },
                "intent": "disponibilite",
                "confidence": 0.9,
            }
        else:
            # Question générale sur les disponibilités
            try:
                with get_database_session() as session:

                    consultants_dispos = (
                        session.query(Consultant).filter(Consultant.disponibilite).all()
                    )
                with get_database_session() as session:

                    consultants_occupes = (
                        session.query(Consultant)
                        .filter(Consultant.disponibilite is False)
                        .all()
                    )

                response = "📅 **État des disponibilités** :\n\n"
                response += (
                    "✅ **Disponibles immédiatement :** "
                    + str(len(consultants_dispos))
                    + " consultant(s)\n"
                )

                if consultants_dispos:
                    for consultant in consultants_dispos[:5]:  # Limiter à 5
                        response += (
                            "   • " + consultant.prenom + " " + consultant.nom + "\n"
                        )
                    if len(consultants_dispos) > 5:
                        response += (
                            "   • ... et "
                            + str(len(consultants_dispos) - 5)
                            + " autre(s)\n"
                        )

                response += (
                    "\n🔴 **Occupés :** "
                    + str(len(consultants_occupes))
                    + " consultant(s)\n"
                )

                if consultants_occupes:
                    for consultant in consultants_occupes[:5]:  # Limiter à 5
                        date_dispo = consultant.date_disponibilite
                        response += (
                            "   • "
                            + consultant.prenom
                            + " "
                            + consultant.nom
                            + " (dispo: "
                            + str(date_dispo)
                            + ")\n"
                        )
                    if len(consultants_occupes) > 5:
                        response += (
                            "   • ... et "
                            + str(len(consultants_occupes) - 5)
                            + " autre(s)\n"
                        )

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
                    "response": "❌ Erreur lors de la récupération des disponibilités : "
                    + str(e),
                    "data": {},
                    "intent": "disponibilite",
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

        Raises:
            SQLAlchemyError: En cas d'erreur de base de données
            ZeroDivisionError: En cas de division par zéro lors des calculs
            AttributeError: Si les données de TJM sont malformées

        Example:
            >>> entities = {"noms": ["Jean Dupont"]}
            >>> result = chatbot._handle_mission_tjm_question(entities)
            >>> print(result["response"])
            💰 **TJM des missions de Jean Dupont** :
            🎯 **Mission Data Analyst**
               • Client: BNP Paribas
               • TJM: 450€
               • Période: 01/01/2024 → 31/03/2024
            📊 **TJM moyen :** 450€ (sur 1 missions)
        """
        # Chercher un consultant spécifique

        # Chercher un consultant spécifique
        consultant = None
        if entities["noms"]:
            nom_complet = " ".join(entities["noms"])
            consultant = self._find_consultant_by_name(nom_complet)

        if consultant:
            try:
                # Récupérer les missions avec TJM
                with get_database_session() as session:

                    consultant_db = (
                        session.query(Consultant)
                        .filter(Consultant.id == consultant.id)
                        .first()
                    )

                if consultant_db and consultant_db.missions:
                    missions_avec_tjm = [
                        m for m in consultant_db.missions if m.tjm or m.taux_journalier
                    ]

                    if missions_avec_tjm:
                        response = (
                            "💰 **TJM des missions de "
                            + consultant.prenom
                            + " "
                            + consultant.nom
                            + "** :\n\n"
                        )

                        total_tjm = 0
                        count_tjm = 0

                        for mission in missions_avec_tjm:
                            tjm = mission.tjm or mission.taux_journalier
                            tjm_type = "TJM" if mission.tjm else "TJM (ancien)"

                            response += "🎯 **" + mission.nom_mission + "**\n"
                            response += "   • Client: " + mission.client + "\n"
                            response += "   • " + tjm_type + ": " + str(tjm) + "€\n"

                            if mission.date_debut:
                                debut = mission.date_debut.strftime("%d/%m/%Y")
                                if mission.date_fin:
                                    fin = mission.date_fin.strftime("%d/%m/%Y")
                                    response += (
                                        "   • Période: " + debut + " → " + fin + "\n"
                                    )
                                else:
                                    response += "   • Début: " + debut + " (en cours)\n"

                            response += "\n"

                            total_tjm += tjm
                            count_tjm += 1

                        if count_tjm > 1:
                            tjm_moyen = total_tjm / count_tjm
                            response += (
                                "📊 **TJM moyen :** "
                                + str(tjm_moyen)
                                + "€ (sur "
                                + str(count_tjm)
                                + " missions)"
                            )

                    else:
                        response = (
                            "💰 **"
                            + consultant.prenom
                            + " "
                            + consultant.nom
                            + "** : Aucun TJM renseigné dans les missions"
                        )
                else:
                    response = (
                        "💰 **"
                        + consultant.prenom
                        + " "
                        + consultant.nom
                        + "** : Aucune mission trouvée"
                    )

            except (
                SQLAlchemyError,
                AttributeError,
                ValueError,
                TypeError,
                ZeroDivisionError,
            ) as e:
                response = "❌ Erreur lors de la récupération des TJM : " + str(e)

            return {
                "response": response,
                "data": {
                    "consultant": {"nom": consultant.nom, "prenom": consultant.prenom}
                },
                "intent": "tjm_mission",
                "confidence": 0.9,
            }
        else:
            # Question générale sur les TJM
            try:
                # TJM moyen avec nouveau champ
                tjm_nouveau_moyen = (
                    session.query(func.avg(Mission.tjm))
                    .filter(Mission.tjm.isnot(None))
                    .scalar()
                    or 0
                )

                # TJM moyen avec ancien champ
                with get_database_session() as session:

                    tjm_ancien_moyen = (
                        session.query(func.avg(Mission.taux_journalier))
                        .filter(Mission.taux_journalier.isnot(None))
                        .scalar()
                        or 0
                    )

                # Compter les missions avec TJM
                with get_database_session() as session:
                    missions_nouveau_tjm = (
                        session.query(Mission).filter(Mission.tjm.isnot(None)).count()
                    )

                with get_database_session() as session:
                    missions_ancien_tjm = (
                        session.query(Mission)
                        .filter(Mission.taux_journalier.isnot(None))
                        .count()
                    )

                response = "💰 **Statistiques TJM des missions** :\n\n"

                if missions_nouveau_tjm > 0:
                    response += "🆕 **Nouveau format TJM :**\n"
                    response += (
                        "   • Missions avec TJM: " + str(missions_nouveau_tjm) + "\n"
                    )
                    response += "   • TJM moyen: " + str(tjm_nouveau_moyen) + "€\n\n"

                if missions_ancien_tjm > 0:
                    response += "📊 **Ancien format TJM :**\n"
                    response += (
                        "   • Missions avec TJM: " + str(missions_ancien_tjm) + "\n"
                    )
                    response += "   • TJM moyen: " + str(tjm_ancien_moyen) + "€\n\n"

                # Calcul global
                if missions_nouveau_tjm > 0 or missions_ancien_tjm > 0:
                    total_missions = missions_nouveau_tjm + missions_ancien_tjm
                    tjm_global = (
                        (tjm_nouveau_moyen * missions_nouveau_tjm)
                        + (tjm_ancien_moyen * missions_ancien_tjm)
                    ) / total_missions
                    response += (
                        "🎯 **TJM global moyen :** "
                        + str(tjm_global)
                        + "€ (sur "
                        + str(total_missions)
                        + " missions)"
                    )
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
                    "response": "❌ Erreur lors de la récupération des statistiques TJM : "
                    + str(e),
                    "data": {},
                    "intent": "tjm_mission",
                    "confidence": 0.3,
                }

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
            return (
                str(response)
                if response is not None
                else "❓ Je n'ai pas compris votre question."
            )
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
