"""
Service Chatbot pour interroger les données des consultants
Utilise l'IA pour répondre aux questions sur la base de données
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st

# Imports des services existants
from database.database import get_database_session
from database.models import Consultant, Mission, Competence, ConsultantCompetence
from sqlalchemy import func, and_, or_


class ChatbotService:
    """Service principal du chatbot pour Consultator"""
    
    def __init__(self):
        self.session = get_database_session()
        self.conversation_history = []
        self.last_question = ""
    
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
            
            # Générer la réponse selon l'intention
            if intent == "salaire":
                return self._handle_salary_question(entities)
            elif intent == "competences":
                return self._handle_skills_question(entities)
            elif intent == "missions":
                return self._handle_missions_question(entities)
            elif intent == "contact":
                return self._handle_contact_question(entities)
            elif intent == "liste_consultants":
                return self._handle_list_consultants_question(entities)
            elif intent == "statistiques":
                return self._handle_stats_question(entities)
            elif intent == "recherche_consultant":
                return self._handle_consultant_search(entities)
            else:
                return self._handle_general_question(clean_question)
                
        except Exception as e:
            return {
                "response": f"❌ Désolé, j'ai rencontré une erreur : {str(e)}",
                "data": None,
                "intent": "error",
                "confidence": 0.0
            }
    
    def _clean_question(self, question: str) -> str:
        """Nettoie et normalise la question"""
        # Supprimer la ponctuation excessive
        question = re.sub(r'[!]{2,}', '!', question)
        question = re.sub(r'[?]{2,}', '?', question)
        
        # Normaliser les espaces
        question = re.sub(r'\s+', ' ', question.strip())
        
        return question.lower()
    
    def _analyze_intent(self, question: str) -> str:
        """Analyse l'intention de la question"""
        
        # D'abord, vérifier s'il y a un nom de consultant mentionné
        all_consultants = self.session.query(Consultant).all()
        has_consultant_name = False
        for consultant in all_consultants:
            if (re.search(rf'\b{re.escape(consultant.prenom.lower())}\b', question) or
                re.search(rf'\b{re.escape(consultant.nom.lower())}\b', question)):
                has_consultant_name = True
                break
        
        # Patterns pour identifier les intentions
        intent_patterns = {
            "salaire": [
                r"salaire", r"rémunération", r"paie", r"combien gagne", 
                r"revenus", r"euros", r"€", r"salaire de", r"gagne"
            ],
            "competences": [
                r"compétences", r"competences", r"maîtrise", r"maitrise", r"sait faire", r"technologies",
                r"langages", r"outils", r"expertise", r"python", r"sql", r"java",
                r"quelles.+compétences", r"quelles.+competences", r"skills", r"techno", r"connaît", r"connait"
            ],
            "missions": [
                r"missions", r"mission", r"travaille", r"chez", r"entreprise", r"client",
                r"projet", r"bnp", r"paribas", r"société générale", r"combien.+missions?",
                r"nombre.+missions?", r"projets"
            ],
            "contact": [
                r"mail", r"email", r"e-mail", r"téléphone", r"tel", r"numéro",
                r"contact", r"joindre", r"coordonnées"
            ],
            "liste_consultants": [
                r"quels sont les consultants", r"liste des consultants", r"consultants disponibles",
                r"consultants actifs", r"tous les consultants", r"lister les consultants",
                r"qui sont les consultants", r"montrer les consultants"
            ],
            "statistiques": [
                r"combien.+consultants", r"nombre.+consultants", r"combien.+dans.+base", 
                r"nombre", r"moyenne", r"total", r"statistiques", r"combien.+missions",
                r"actifs", r"inactifs", r"tjm moyen", r"combien y a", r"il y a combien"
            ],
            "recherche_consultant": [
                r"qui est", r"consultant", r"profil", r"information sur",
                r"details"
            ]
        }
        
        # Scorer chaque intention
        intent_scores = {}
        for intent, patterns in intent_patterns.items():
            score = 0
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
        
        # Si un nom de consultant est mentionné et qu'on parle de missions,
        # c'est forcément une question de missions spécifique
        if has_consultant_name and intent_scores.get("missions", 0) > 0:
            return "missions"
        
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
            return max(intent_scores, key=intent_scores.get)
        else:
            return "general"
    
    def _extract_entities(self, question: str) -> Dict[str, List[str]]:
        """Extrait les entités nommées de la question"""
        entities = {
            "noms": [],
            "entreprises": [],
            "competences": [],
            "montants": []
        }
        
        # Patterns pour extraire les entités
        
        # Noms - chercher dans la base de données
        all_consultants = self.session.query(Consultant).all()
        for consultant in all_consultants:
            # Chercher le prénom dans la question (insensible à la casse)
            if re.search(rf'\b{re.escape(consultant.prenom.lower())}\b', question):
                entities["noms"].append(consultant.prenom)
            # Chercher le nom de famille dans la question
            if re.search(rf'\b{re.escape(consultant.nom.lower())}\b', question):
                entities["noms"].append(consultant.nom)
            # Chercher le nom complet
            nom_complet = f"{consultant.prenom} {consultant.nom}".lower()
            if nom_complet in question:
                entities["noms"].append(f"{consultant.prenom} {consultant.nom}")
        
        # Supprimer les doublons en gardant l'ordre
        entities["noms"] = list(dict.fromkeys(entities["noms"]))
        
        # Entreprises connues
        entreprises_connues = [
            "bnp paribas", "société générale", "axa", "orange", "airbus", 
            "renault", "peugeot", "total", "carrefour", "crédit agricole"
        ]
        for entreprise in entreprises_connues:
            if entreprise in question:
                entities["entreprises"].append(entreprise)
        
        # Compétences techniques
        competences_connues = [
            "python", "java", "javascript", "sql", "react", "angular",
            "node.js", "docker", "kubernetes", "aws", "azure", "power bi"
        ]
        for competence in competences_connues:
            if competence in question:
                entities["competences"].append(competence)
        
        # Montants
        montants_pattern = r'(\d+(?:\s*\d{3})*)\s*(?:euros?|€)'
        montants_matches = re.findall(montants_pattern, question)
        entities["montants"] = [montant.replace(' ', '') for montant in montants_matches]
        
        return entities
    
    def _handle_salary_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les salaires"""
        
        # Si un nom est mentionné, chercher ce consultant spécifique
        if entities["noms"]:
            nom_recherche = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom_recherche)
            
            if consultant:
                if consultant.salaire_actuel and consultant.salaire_actuel > 0:
                    response = f"💰 Le salaire de **{consultant.prenom} {consultant.nom}** est de **{consultant.salaire_actuel:,.0f} €** par an."
                    if not consultant.disponibilite:
                        response += "\n⚠️ Attention : ce consultant est actuellement indisponible."
                else:
                    response = f"❓ Désolé, le salaire de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."
                
                return {
                    "response": response,
                    "data": {
                        "consultant": {
                            "nom": consultant.nom,
                            "prenom": consultant.prenom,
                            "salaire": consultant.salaire_actuel,
                            "disponibilite": consultant.disponibilite
                        }
                    },
                    "intent": "salaire",
                    "confidence": 0.9
                }
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom_recherche}** dans la base de données.",
                    "data": None,
                    "intent": "salaire",
                    "confidence": 0.7
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
                "confidence": 0.8
            }
    
    def _handle_skills_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les compétences"""
        
        if entities["competences"]:
            competence = entities["competences"][0]
            consultants = self._find_consultants_by_skill(competence)
            
            if consultants:
                noms = [f"**{c.prenom} {c.nom}**" for c in consultants]
                response = f"🎯 Consultants maîtrisant **{competence.title()}** :\n\n"
                response += "\n".join([f"• {nom}" for nom in noms])
            else:
                response = f"❌ Aucun consultant ne maîtrise **{competence}** dans notre base."
            
            return {
                "response": response,
                "data": {"consultants": [{"nom": c.nom, "prenom": c.prenom} for c in consultants]},
                "intent": "competences",
                "confidence": 0.9
            }
        
        # Question générale sur les compétences
        elif entities["noms"]:
            nom = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)
            
            if consultant:
                skills = self._get_consultant_skills(consultant.id)
                
                if skills:
                    response = f"🎯 **Compétences de {consultant.prenom} {consultant.nom} :**\n\n"
                    
                    # Grouper par catégorie
                    categories = {}
                    for skill in skills:
                        categorie = skill["categorie"] or "Autre"
                        if categorie not in categories:
                            categories[categorie] = []
                        categories[categorie].append(skill)
                    
                    # Afficher par catégorie
                    for categorie, competences in categories.items():
                        response += f"**� {categorie.title()} :**\n"
                        for comp in competences:
                            niveau_emoji = {
                                "debutant": "🟡",
                                "intermediaire": "🟠", 
                                "expert": "🔴"
                            }.get(comp["niveau_maitrise"], "⚪")
                            
                            experience_text = ""
                            if comp["annees_experience"] and comp["annees_experience"] > 0:
                                if comp["annees_experience"] == 1:
                                    experience_text = f" ({comp['annees_experience']} an)"
                                else:
                                    experience_text = f" ({comp['annees_experience']:.0f} ans)"
                            
                            response += f"  {niveau_emoji} **{comp['nom']}** - {comp['niveau_maitrise'].title()}{experience_text}\n"
                        response += "\n"
                    
                    response += f"� **Total : {len(skills)} compétence(s)**"
                else:
                    response = f"❌ Aucune compétence enregistrée pour **{consultant.prenom} {consultant.nom}**."
            else:
                response = f"❌ Consultant **{nom}** introuvable."
            
            return {
                "response": response,
                "data": {"consultant": consultant.nom if consultant else None, "skills_count": len(skills) if consultant else 0},
                "intent": "competences",
                "confidence": 0.9
            }
        
        return {
            "response": "🤔 Pouvez-vous préciser quelle compétence ou quel consultant vous intéresse ?",
            "data": None,
            "intent": "competences",
            "confidence": 0.5
        }
    
    def _handle_missions_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les missions"""
        
        # Détecter si c'est une question sur le nombre de missions
        question_lower = self.last_question.lower()
        is_count_question = any(word in question_lower for word in ["combien", "nombre"])
        
        if entities["entreprises"]:
            entreprise = entities["entreprises"][0]
            missions = self._get_missions_by_company(entreprise)
            
            if is_count_question:
                response = f"📊 **{len(missions)} mission(s)** trouvée(s) chez **{entreprise.title()}**"
            elif missions:
                response = f"🏢 **Missions chez {entreprise.title()} :**\n\n"
                for mission in missions[:5]:  # Limiter à 5 résultats
                    consultant_nom = f"{mission.consultant.prenom} {mission.consultant.nom}"
                    response += f"• **{consultant_nom}** - {mission.nom_mission} ({mission.date_debut.strftime('%Y')})\n"
                
                if len(missions) > 5:
                    response += f"\n... et {len(missions) - 5} autres missions"
                
                response += f"\n\n📊 **Total : {len(missions)} mission(s)**"
            else:
                response = f"❌ Aucune mission trouvée chez **{entreprise}**."
            
            return {
                "response": response,
                "data": {"missions": len(missions), "entreprise": entreprise},
                "intent": "missions",
                "confidence": 0.9
            }
        
        elif entities["noms"]:
            nom = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)
            
            if consultant:
                missions = self._get_missions_by_consultant(consultant.id)
                
                if is_count_question:
                    # Question spécifique sur le nombre
                    response = f"📊 **{consultant.prenom} {consultant.nom}** a **{len(missions)} mission(s)** dans la base"
                    if missions:
                        missions_en_cours = [m for m in missions if m.statut == "en_cours"]
                        if missions_en_cours:
                            response += f" (dont {len(missions_en_cours)} en cours)"
                elif missions:
                    response = f"💼 **Missions de {consultant.prenom} {consultant.nom} :**\n\n"
                    for mission in missions:
                        status_icon = "🟢" if mission.statut == "en_cours" else "✅"
                        response += f"{status_icon} **{mission.client}** - {mission.nom_mission}\n"
                        response += f"   📅 {mission.date_debut.strftime('%m/%Y')} → "
                        if mission.date_fin:
                            response += f"{mission.date_fin.strftime('%m/%Y')}"
                        else:
                            response += "En cours"
                        if mission.taux_journalier:
                            response += f" | 💰 {mission.taux_journalier}€/jour"
                        response += "\n\n"
                    
                    response += f"📊 **Total : {len(missions)} mission(s)**"
                else:
                    response = f"❌ Aucune mission trouvée pour **{consultant.prenom} {consultant.nom}**."
            else:
                response = f"❌ Consultant **{nom}** introuvable."
            
            return {
                "response": response,
                "data": {"consultant": nom, "missions_count": len(missions) if consultant else 0},
                "intent": "missions",
                "confidence": 0.9
            }
        
        return {
            "response": "🤔 Voulez-vous connaître les missions d'un consultant ou d'une entreprise spécifique ?",
            "data": None,
            "intent": "missions",
            "confidence": 0.5
        }
    
    def _handle_stats_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions statistiques"""
        
        stats = self._get_general_stats()
        
        # Si c'est une question spécifique sur le nombre de consultants
        if any(pattern in self.last_question for pattern in ["combien", "nombre"]):
            if "consultant" in self.last_question and "mission" not in self.last_question:
                response = f"👥 **Vous avez {stats['consultants_total']} consultants** dans votre base de données.\n\n"
                response += f"📊 Détail : {stats['consultants_actifs']} disponibles, {stats['consultants_inactifs']} indisponibles"
                
                return {
                    "response": response,
                    "data": {"consultants_count": stats['consultants_total']},
                    "intent": "statistiques",
                    "confidence": 0.95
                }
        
        # Statistiques complètes par défaut
        response = f"""📊 **Statistiques générales :**

👥 **Consultants :**
• Total : **{stats['consultants_total']}**
• Actifs : **{stats['consultants_actifs']}** 
• Inactifs : **{stats['consultants_inactifs']}**

💼 **Missions :**
• Total : **{stats['missions_total']}**
• En cours : **{stats['missions_en_cours']}**
• Terminées : **{stats['missions_terminees']}**

💰 **Financier :**
• TJM moyen : **{stats['tjm_moyen']:,.0f} €**
• Salaire moyen : **{stats['salaire_moyen']:,.0f} €**"""
        
        return {
            "response": response,
            "data": {"stats": stats},
            "intent": "statistiques",
            "confidence": 0.9
        }
    
    def _handle_contact_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions sur les contacts (email, téléphone)"""
        
        if entities["noms"]:
            nom = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)
            
            if consultant:
                # Déterminer le type d'information demandée
                question_lower = self.last_question.lower()
                
                if any(word in question_lower for word in ["mail", "email", "e-mail"]):
                    if consultant.email:
                        response = f"📧 L'email de **{consultant.prenom} {consultant.nom}** est : **{consultant.email}**"
                    else:
                        response = f"❓ Désolé, l'email de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."
                
                elif any(word in question_lower for word in ["téléphone", "tel", "numéro"]):
                    if consultant.telephone:
                        response = f"📞 Le téléphone de **{consultant.prenom} {consultant.nom}** est : **{consultant.telephone}**"
                    else:
                        response = f"❓ Désolé, le téléphone de **{consultant.prenom} {consultant.nom}** n'est pas renseigné dans la base."
                
                else:
                    # Information de contact complète
                    response = f"📞 **Contact de {consultant.prenom} {consultant.nom} :**\n\n"
                    response += f"📧 Email : **{consultant.email or 'Non renseigné'}**\n"
                    response += f"📞 Téléphone : **{consultant.telephone or 'Non renseigné'}**"
                
                return {
                    "response": response,
                    "data": {
                        "consultant": consultant.nom,
                        "email": consultant.email,
                        "telephone": consultant.telephone
                    },
                    "intent": "contact",
                    "confidence": 0.9
                }
            else:
                return {
                    "response": f"❌ Je n'ai pas trouvé de consultant nommé **{nom}** dans la base de données.",
                    "data": None,
                    "intent": "contact",
                    "confidence": 0.7
                }
        
        return {
            "response": "🤔 De quel consultant souhaitez-vous connaître les coordonnées ?",
            "data": None,
            "intent": "contact",
            "confidence": 0.5
        }
    
    def _handle_list_consultants_question(self, entities: Dict) -> Dict[str, Any]:
        """Gère les questions pour lister les consultants selon des critères"""
        
        question_lower = self.last_question.lower()
        
        # Déterminer le filtre à appliquer
        if "disponibles" in question_lower or "disponible" in question_lower:
            consultants = self.session.query(Consultant).filter(Consultant.disponibilite == True).all()
            titre = "👥 **Consultants disponibles :**"
        elif "indisponibles" in question_lower or "indisponible" in question_lower:
            consultants = self.session.query(Consultant).filter(Consultant.disponibilite == False).all()
            titre = "👥 **Consultants indisponibles :**"
        elif "actifs" in question_lower or "actif" in question_lower:
            consultants = self.session.query(Consultant).filter(Consultant.disponibilite == True).all()
            titre = "👥 **Consultants actifs :**"
        else:
            # Tous les consultants
            consultants = self.session.query(Consultant).all()
            titre = "👥 **Tous les consultants :**"
        
        if not consultants:
            return {
                "response": "❓ Aucun consultant ne correspond à ce critère.",
                "data": None,
                "intent": "liste_consultants",
                "confidence": 0.8
            }
        
        # Construire la réponse
        response = f"{titre}\n\n"
        
        for i, consultant in enumerate(consultants, 1):
            status_icon = "🟢" if consultant.disponibilite else "🔴"
            response += f"{i}. {status_icon} **{consultant.prenom} {consultant.nom}**"
            
            if consultant.email:
                response += f" - {consultant.email}"
            
            if consultant.salaire_actuel:
                response += f" - {consultant.salaire_actuel:,.0f} €/an"
            
            response += "\n"
        
        response += f"\n📊 **Total : {len(consultants)} consultant(s)**"
        
        return {
            "response": response,
            "data": {
                "consultants": [
                    {
                        "nom": c.nom,
                        "prenom": c.prenom,
                        "email": c.email,
                        "disponibilite": c.disponibilite,
                        "salaire": c.salaire_actuel
                    } for c in consultants
                ],
                "count": len(consultants)
            },
            "intent": "liste_consultants",
            "confidence": 0.9
        }
    
    def _handle_consultant_search(self, entities: Dict) -> Dict[str, Any]:
        """Gère la recherche d'informations sur un consultant"""
        
        if entities["noms"]:
            nom = entities["noms"][0]
            consultant = self._find_consultant_by_name(nom)
            
            if consultant:
                response = f"""👤 **{consultant.prenom} {consultant.nom}**

📧 Email : {consultant.email or 'Non renseigné'}
📞 Téléphone : {consultant.telephone or 'Non renseigné'}
📊 Disponibilité : **{'Disponible' if consultant.disponibilite else 'Indisponible'}**
📅 Date création : {consultant.date_creation.strftime('%d/%m/%Y') if consultant.date_creation else 'Non renseignée'}"""

                if consultant.salaire_actuel:
                    response += f"\n💰 Salaire : **{consultant.salaire_actuel:,.0f} €**"
                
                # Ajouter info sur les missions
                missions_count = len(consultant.missions)
                if missions_count > 0:
                    response += f"\n💼 Missions : **{missions_count}** mission(s)"
            else:
                response = f"❌ Consultant **{nom}** introuvable dans la base de données."
            
            return {
                "response": response,
                "data": {"consultant": consultant.nom if consultant else None},
                "intent": "recherche_consultant", 
                "confidence": 0.9
            }
        
        return {
            "response": "🤔 De quel consultant souhaitez-vous connaître les informations ?",
            "data": None,
            "intent": "recherche_consultant",
            "confidence": 0.5
        }
    
    def _handle_general_question(self, question: str) -> Dict[str, Any]:
        """Gère les questions générales"""
        
        responses = [
            "🤖 Je suis là pour vous aider à interroger la base de données des consultants !",
            "",
            "💡 **Voici quelques exemples de questions :**",
            "",
            "💰 *Salaires :* \"Quel est le salaire de Jean Dupont ?\"",
            "📧 *Contact :* \"Quel est l'email de Marie ?\"",
            "👥 *Listes :* \"Quels sont les consultants disponibles ?\"",
            "🎯 *Compétences :* \"Qui maîtrise Python ?\"", 
            "💼 *Missions :* \"Quelles sont les missions chez BNP Paribas ?\"",
            "📊 *Statistiques :* \"Combien de consultants sont actifs ?\"",
            "👤 *Profils :* \"Qui est Marie Martin ?\"",
            "",
            "Que souhaitez-vous savoir ? 😊"
        ]
        
        return {
            "response": "\n".join(responses),
            "data": None,
            "intent": "general",
            "confidence": 1.0
        }
    
    # Méthodes utilitaires pour les requêtes DB
    
    def _find_consultant_by_name(self, nom_recherche: str) -> Optional[Consultant]:
        """Trouve un consultant par son nom (flexible)"""
        
        # Essayer une correspondance exacte d'abord
        consultant = self.session.query(Consultant).filter(
            or_(
                func.lower(Consultant.nom) == nom_recherche.lower(),
                func.lower(Consultant.prenom) == nom_recherche.lower(),
                func.lower(func.concat(Consultant.prenom, ' ', Consultant.nom)) == nom_recherche.lower(),
                func.lower(func.concat(Consultant.nom, ' ', Consultant.prenom)) == nom_recherche.lower()
            )
        ).first()
        
        if consultant:
            return consultant
        
        # Essayer une correspondance partielle
        consultant = self.session.query(Consultant).filter(
            or_(
                func.lower(Consultant.nom).like(f'%{nom_recherche.lower()}%'),
                func.lower(Consultant.prenom).like(f'%{nom_recherche.lower()}%')
            )
        ).first()
        
        return consultant
    
    def _find_consultants_by_skill(self, competence: str) -> List[Consultant]:
        """Trouve les consultants ayant une compétence (simulation)"""
        # Pour l'instant, retourner une liste vide
        # TODO: Implémenter la recherche par compétences quand la relation sera créée
        return []
    
    def _get_missions_by_company(self, entreprise: str) -> List[Mission]:
        """Récupère les missions pour une entreprise"""
        return self.session.query(Mission).filter(
            func.lower(Mission.entreprise).like(f'%{entreprise.lower()}%')
        ).all()
    
    def _get_missions_by_consultant(self, consultant_id: int) -> List[Mission]:
        """Récupère les missions d'un consultant"""
        return self.session.query(Mission).filter(
            Mission.consultant_id == consultant_id
        ).order_by(Mission.date_debut.desc()).all()
    
    def _get_consultant_skills(self, consultant_id: int) -> List[Dict[str, Any]]:
        """Récupère les compétences d'un consultant avec leurs détails"""
        consultant_competences = self.session.query(ConsultantCompetence).join(
            Competence
        ).filter(
            ConsultantCompetence.consultant_id == consultant_id
        ).all()
        
        skills = []
        for cc in consultant_competences:
            skills.append({
                "nom": cc.competence.nom,
                "categorie": cc.competence.categorie,
                "type": cc.competence.type_competence,
                "niveau_maitrise": cc.niveau_maitrise,
                "annees_experience": cc.annees_experience,
                "description": cc.competence.description
            })
        
        return skills
    
    def _get_salary_stats(self) -> Dict[str, float]:
        """Calcule les statistiques des salaires"""
        consultants = self.session.query(Consultant).filter(
            and_(Consultant.salaire_actuel.isnot(None), Consultant.salaire_actuel > 0)
        ).all()
        
        if not consultants:
            return {"moyenne": 0, "mediane": 0, "minimum": 0, "maximum": 0, "total": 0}
        
        salaires = [c.salaire_actuel for c in consultants]
        salaires.sort()
        
        return {
            "moyenne": sum(salaires) / len(salaires),
            "mediane": salaires[len(salaires) // 2],
            "minimum": min(salaires),
            "maximum": max(salaires),
            "total": len(consultants)
        }
    
    def _get_general_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques générales"""
        
        # Consultants
        consultants_total = self.session.query(Consultant).count()
        consultants_actifs = self.session.query(Consultant).filter(Consultant.disponibilite == True).count()
        consultants_inactifs = consultants_total - consultants_actifs
        
        # Missions
        missions_total = self.session.query(Mission).count()
        missions_en_cours = self.session.query(Mission).filter(Mission.statut == "en_cours").count()
        missions_terminees = missions_total - missions_en_cours
        
        # TJM moyen
        tjm_moyen = self.session.query(func.avg(Mission.taux_journalier)).filter(Mission.taux_journalier.isnot(None)).scalar() or 0
        
        # Salaire moyen
        salaire_moyen = self.session.query(func.avg(Consultant.salaire_actuel)).filter(
            Consultant.salaire_actuel.isnot(None)
        ).scalar() or 0
        
        return {
            "consultants_total": consultants_total,
            "consultants_actifs": consultants_actifs,
            "consultants_inactifs": consultants_inactifs,
            "missions_total": missions_total,
            "missions_en_cours": missions_en_cours,
            "missions_terminees": missions_terminees,
            "tjm_moyen": tjm_moyen,
            "salaire_moyen": salaire_moyen
        }
    
    def __del__(self):
        """Ferme la session DB"""
        if hasattr(self, 'session'):
            self.session.close()
