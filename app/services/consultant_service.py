"""
Service de gestion des consultants
CRUD operations pour les consultants avec la base de données
Optimisé pour gérer 1000+ consultants avec cache et pagination efficace
"""

from datetime import date
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import streamlit as st
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from database.database import get_database_session
from database.models import Competence
from database.models import Consultant
from database.models import ConsultantCompetence
from database.models import Mission
from database.models import Practice


class ConsultantService:
    """Service pour la gestion des consultants optimisé pour de gros volumes"""

    @staticmethod
    def get_all_consultants_objects(
            page: int = 1,
            per_page: int = 50) -> List[Consultant]:
        """Récupère tous les consultants comme objets (ancienne interface)"""
        try:
            with get_database_session() as session:
                consultants = session.query(Consultant)\
                    .options(joinedload(Consultant.practice))\
                    .offset((page - 1) * per_page)\
                    .limit(per_page)\
                    .all()

                # Détacher les instances de la session pour éviter les erreurs
                # DetachedInstance
                for consultant in consultants:
                    session.expunge(consultant)

                return consultants
        except Exception as e:
            print(f"Erreur lors de la récupération des consultants: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=300)  # Cache pendant 5 minutes
    def get_all_consultants(page: int = 1, per_page: int = 50) -> List[Dict]:
        """Récupère tous les consultants avec pagination optimisée"""
        try:
            with get_database_session() as session:
                consultants = session.query(Consultant)\
                    .options(joinedload(Consultant.practice))\
                    .offset((page - 1) * per_page)\
                    .limit(per_page)\
                    .all()

                # Convertir en dictionnaires pour éviter les erreurs de session
                consultant_list = []
                for consultant in consultants:
                    consultant_dict = {
                        'id': consultant.id,
                        'prenom': consultant.prenom,
                        'nom': consultant.nom,
                        'email': consultant.email,
                        'telephone': consultant.telephone,
                        'salaire_actuel': consultant.salaire_actuel,
                        'disponibilite': consultant.disponibilite,
                        'practice_name': consultant.practice.nom if consultant.practice else 'N/A',
                        'date_creation': consultant.date_creation,
                        'derniere_maj': consultant.derniere_maj,
                        # Nouveaux champs V1.2.2
                        'date_disponibilite': consultant.date_disponibilite,
                        'experience_annees': consultant.experience_annees,
                        'grade': consultant.grade,
                        'type_contrat': consultant.type_contrat,
                        'societe': consultant.societe
                    }
                    consultant_list.append(consultant_dict)

                return consultant_list
        except Exception as e:
            print(f"Erreur lors de la récupération des consultants: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=300)  # Cache pendant 5 minutes
    def search_consultants_optimized(
            search_term: str,
            page: int = 1,
            per_page: int = 50) -> List[Dict]:
        """Recherche optimisée avec cache pour de gros volumes - avec statistiques intégrées"""
        try:
            with get_database_session() as session:
                # Requête optimisée avec JOIN pour éviter les requêtes N+1
                query = session.query(
                    Consultant.id,
                    Consultant.prenom,
                    Consultant.nom,
                    Consultant.email,
                    Consultant.telephone,
                    Consultant.salaire_actuel,
                    Consultant.disponibilite,
                    Consultant.date_creation,
                    Consultant.societe,
                    Consultant.date_entree_societe,
                    Consultant.date_sortie_societe,
                    Consultant.date_premiere_mission,
                    Consultant.grade,
                    Consultant.type_contrat,
                    Practice.nom.label('practice_name'),
                    func.count(Mission.id).label('nb_missions')
                ).outerjoin(Practice, Consultant.practice_id == Practice.id)\
                 .outerjoin(Mission, Consultant.id == Mission.consultant_id)

                if search_term:
                    search_filter = f"%{search_term}%"
                    query = query.filter(
                        (Consultant.nom.ilike(search_filter)) |
                        (Consultant.prenom.ilike(search_filter)) |
                        (Consultant.email.ilike(search_filter))
                    )

                query = query.group_by(
                    Consultant.id,
                    Consultant.prenom,
                    Consultant.nom,
                    Consultant.email,
                    Consultant.telephone,
                    Consultant.salaire_actuel,
                    Consultant.disponibilite,
                    Consultant.date_creation,
                    Consultant.societe,
                    Consultant.date_entree_societe,
                    Consultant.date_sortie_societe,
                    Consultant.date_premiere_mission,
                    Consultant.grade,
                    Consultant.type_contrat,
                    Practice.nom
                ).offset((page - 1) * per_page).limit(per_page)

                results = query.all()

                # Convertir en dictionnaires avec calculs optimisés
                consultant_list = []
                for row in results:
                    salaire = row.salaire_actuel or 0
                    cjm = (salaire * 1.8 / 216) if salaire else 0

                    # Calcul de l'expérience
                    experience_annees = 0
                    if row.date_premiere_mission:
                        from datetime import date
                        today = date.today()
                        delta = today - row.date_premiere_mission
                        experience_annees = round(delta.days / 365.25, 1)

                    consultant_dict = {
                        'id': row.id,
                        'prenom': row.prenom,
                        'nom': row.nom,
                        'email': row.email,
                        'telephone': row.telephone,
                        'salaire_actuel': salaire,
                        'disponibilite': row.disponibilite,
                        'grade': row.grade or 'Junior',
                        'type_contrat': row.type_contrat or 'CDI',
                        'practice_name': row.practice_name or 'Non affecté',
                        'date_creation': row.date_creation,
                        'nb_missions': row.nb_missions,
                        'cjm': cjm,
                        'salaire_formatted': f"{salaire:,}€",
                        'cjm_formatted': f"{cjm:,.0f}€",
                        'statut': "✅ Disponible" if row.disponibilite else "🔴 Occupé",
                        # Nouveaux champs V1.2
                        'societe': row.societe or 'Quanteam',
                        'experience_annees': experience_annees,
                        'experience_formatted': f"{experience_annees} ans" if experience_annees > 0 else "N/A"
                    }
                    consultant_list.append(consultant_dict)

                return consultant_list
        except Exception as e:
            print(f"Erreur lors de la recherche optimisée: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=600)  # Cache pendant 10 minutes
    def get_consultants_count() -> int:
        """Retourne le nombre total de consultants avec cache"""
        try:
            with get_database_session() as session:
                return session.query(Consultant).count()
        except Exception as e:
            print(f"Erreur lors du comptage des consultants: {e}")
            return 0

    @staticmethod
    @st.cache_data(ttl=300)  # Cache pendant 5 minutes
    def get_all_consultants_with_stats(page: int = 1, per_page: int = 50) -> List[Dict]:
        """
        Récupère tous les consultants avec leurs statistiques en une seule requête optimisée
        Résout le problème N+1 des requêtes pour compter les missions
        """
        try:
            with get_database_session() as session:
                # Une seule requête avec LEFT JOIN pour récupérer consultants + nombre
                # de missions
                query = session.query(
                    Consultant.id,
                    Consultant.prenom,
                    Consultant.nom,
                    Consultant.email,
                    Consultant.telephone,
                    Consultant.salaire_actuel,
                    Consultant.disponibilite,
                    Consultant.date_creation,
                    Consultant.derniere_maj,
                    Consultant.societe,
                    Consultant.date_entree_societe,
                    Consultant.date_sortie_societe,
                    Consultant.date_premiere_mission,
                    Consultant.grade,
                    Consultant.type_contrat,
                    Practice.nom.label('practice_name'),
                    func.count(Mission.id).label('nb_missions')
                ).outerjoin(Practice, Consultant.practice_id == Practice.id)\
                 .outerjoin(Mission, Consultant.id == Mission.consultant_id)\
                 .group_by(
                     Consultant.id,
                     Consultant.prenom,
                     Consultant.nom,
                     Consultant.email,
                     Consultant.telephone,
                     Consultant.salaire_actuel,
                     Consultant.disponibilite,
                     Consultant.date_creation,
                     Consultant.derniere_maj,
                     Consultant.societe,
                     Consultant.date_entree_societe,
                     Consultant.date_sortie_societe,
                     Consultant.date_premiere_mission,
                     Consultant.grade,
                     Consultant.type_contrat,
                     Practice.nom
                )\
                    .offset((page - 1) * per_page)\
                    .limit(per_page)

                results = query.all()

                # Convertir en dictionnaires avec calculs optimisés
                consultant_list = []
                for row in results:
                    salaire = row.salaire_actuel or 0
                    cjm = (salaire * 1.8 / 216) if salaire else 0

                    # Calcul de l'expérience
                    experience_annees = 0
                    if row.date_premiere_mission:
                        from datetime import date
                        today = date.today()
                        delta = today - row.date_premiere_mission
                        experience_annees = round(delta.days / 365.25, 1)

                    consultant_dict = {
                        'id': row.id,
                        'prenom': row.prenom,
                        'nom': row.nom,
                        'email': row.email,
                        'telephone': row.telephone,
                        'salaire_actuel': salaire,
                        'disponibilite': row.disponibilite,
                        'practice_name': row.practice_name or 'Non affecté',
                        'date_creation': row.date_creation,
                        'derniere_maj': row.derniere_maj,
                        'nb_missions': row.nb_missions,
                        'cjm': cjm,
                        'salaire_formatted': f"{salaire:,}€",
                        'cjm_formatted': f"{cjm:,.0f}€",
                        'statut': "✅ Disponible" if row.disponibilite else "🔴 Occupé",
                        # Nouveaux champs V1.2
                        'societe': row.societe or 'Quanteam',
                        'experience_annees': experience_annees,
                        'experience_formatted': f"{experience_annees} ans" if experience_annees > 0 else "N/A",
                        # Nouveaux champs V1.2.1
                        'grade': row.grade or 'Junior',
                        'type_contrat': row.type_contrat or 'CDI'
                    }
                    consultant_list.append(consultant_dict)

                return consultant_list
        except Exception as e:
            print(f"Erreur lors de la récupération optimisée des consultants: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=300)  # Cache pendant 5 minutes
    def get_consultant_summary_stats() -> Dict[str, int]:
        """Récupère les statistiques générales avec cache pour tableau de bord"""
        try:
            with get_database_session() as session:
                total_consultants = session.query(Consultant).count()
                available_consultants = session.query(Consultant)\
                    .filter(Consultant.disponibilite).count()
                total_missions = session.query(Mission).count()
                active_missions = session.query(Mission)\
                    .filter(Mission.statut == 'en_cours').count()

                return {
                    'total_consultants': total_consultants,
                    'available_consultants': available_consultants,
                    'total_missions': total_missions,
                    'active_missions': active_missions,
                    'busy_consultants': total_consultants - available_consultants
                }
        except Exception as e:
            print(f"Erreur lors de la récupération des stats: {e}")
            return {
                'total_consultants': 0,
                'available_consultants': 0,
                'total_missions': 0,
                'active_missions': 0,
                'busy_consultants': 0
            }

    @staticmethod
    def get_consultants_by_availability(available: bool = True) -> List[Dict]:
        """Récupère les consultants selon leur disponibilité"""
        try:
            with get_database_session() as session:
                consultants = session.query(Consultant)\
                    .filter(Consultant.disponibilite == available)\
                    .all()

                # Convertir en dictionnaires
                result = []
                for consultant in consultants:
                    result.append({
                        'id': consultant.id,
                        'prenom': consultant.prenom,
                        'nom': consultant.nom,
                        'email': consultant.email,
                        'telephone': consultant.telephone,
                        'salaire_actuel': consultant.salaire_actuel,
                        'disponibilite': consultant.disponibilite,
                        'grade': consultant.grade,
                        'type_contrat': consultant.type_contrat,
                        'statut': "✅ Disponible" if consultant.disponibilite else "🔴 Occupé"
                    })

                return result
        except Exception as e:
            print(
                f"Erreur lors de la récupération des consultants par disponibilité: {e}")
            return []

    @staticmethod
    def get_consultant_by_id(consultant_id: int) -> Optional[Consultant]:
        """Récupère un consultant par son ID avec toutes ses relations"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant)\
                    .options(
                        joinedload(Consultant.competences),
                        joinedload(Consultant.missions)
                )\
                    .filter(Consultant.id == consultant_id)\
                    .first()

                # Détacher l'objet de la session pour éviter les erreurs de session
                # fermée
                if consultant:
                    session.expunge(consultant)

                return consultant
        except Exception as e:
            print(f"Erreur lors de la récupération du consultant {consultant_id}: {e}")
            return None

    @staticmethod
    def get_consultant_with_stats(consultant_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un consultant avec ses statistiques pour éviter les problèmes de session"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant) .options(
                    joinedload(
                        Consultant.competences).joinedload(
                        ConsultantCompetence.competence), joinedload(
                        Consultant.missions)) .filter(
                    Consultant.id == consultant_id) .first()

                if not consultant:
                    return None

                # Calculer les statistiques avant de fermer la session
                competences_count = len(
                    consultant.competences) if consultant.competences else 0
                missions_count = len(consultant.missions) if consultant.missions else 0

                # Convertir en dictionnaire avec toutes les données nécessaires
                consultant_data = {
                    'id': consultant.id,
                    'prenom': consultant.prenom,
                    'nom': consultant.nom,
                    'email': consultant.email,
                    'telephone': consultant.telephone,
                    'salaire_actuel': consultant.salaire_actuel,
                    'disponibilite': consultant.disponibilite,
                    'notes': consultant.notes,
                    'date_creation': consultant.date_creation,
                    'derniere_maj': consultant.derniere_maj,
                    'competences_count': competences_count,
                    'missions_count': missions_count,
                    'competences': [
                        {
                            'id': comp.competence.id if comp.competence else comp.id,
                            'nom': comp.competence.nom if comp.competence else 'N/A',
                            'niveau': comp.niveau_maitrise,
                            'annees_experience': comp.annees_experience
                        } for comp in (consultant.competences or [])
                    ],
                    'missions': [
                        {
                            'id': mission.id,
                            'nom_mission': mission.nom_mission,
                            'client': mission.client,
                            'description': mission.description,
                            'date_debut': mission.date_debut,
                            'date_fin': mission.date_fin,
                            'statut': mission.statut,
                            'revenus_generes': mission.revenus_generes
                        } for mission in (consultant.missions or [])
                    ]
                }

                return consultant_data

        except Exception as e:
            print(
                f"Erreur lors de la récupération du consultant avec stats {consultant_id}: {e}")
            return None

    @staticmethod
    def get_consultant_by_email(email: str) -> Optional[Consultant]:
        """Récupère un consultant par son email"""
        try:
            with get_database_session() as session:
                return session.query(Consultant)\
                    .filter(Consultant.email == email.lower())\
                    .first()
        except Exception as e:
            print(
                f"Erreur lors de la récupération du consultant par email {email}: {e}")
            return None

    @staticmethod
    def create_consultant(data: dict) -> bool:
        """Crée un nouveau consultant"""
        try:
            with get_database_session() as session:
                consultant = Consultant(
                    prenom=data.get('prenom'),
                    nom=data.get('nom'),
                    email=data.get('email'),
                    telephone=data.get('telephone'),
                    salaire_actuel=data.get('salaire'),
                    practice_id=data.get('practice_id'),
                    disponibilite=data.get('disponible', True),
                    notes=data.get('notes'),
                    date_creation=datetime.now(),
                    derniere_maj=datetime.now(),
                    # Nouveaux champs V1.2
                    societe=data.get('societe', 'Quanteam'),
                    date_entree_societe=data.get('date_entree_societe'),
                    date_sortie_societe=data.get('date_sortie_societe'),
                    date_premiere_mission=data.get('date_premiere_mission'),
                    # Nouveaux champs V1.2.1
                    grade=data.get('grade', 'Junior'),
                    type_contrat=data.get('type_contrat', 'CDI')
                )

                session.add(consultant)
                session.commit()
                print(
                    f"✅ Consultant {
                        data.get('prenom')} {
                        data.get('nom')} créé avec succès")
                return True

        except Exception as e:
            print(f"❌ Erreur lors de la création du consultant: {e}")
            return False

    @staticmethod
    def update_consultant(consultant_id: int, data: dict) -> bool:
        """Met à jour un consultant existant"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant).filter(
                    Consultant.id == consultant_id).first()

                if not consultant:
                    print(f"❌ Consultant avec l'ID {consultant_id} non trouvé")
                    return False

                # Mapping des attributs pour éviter les erreurs
                attribute_mapping = {
                    'salaire': 'salaire_actuel',
                    'disponible': 'disponibilite',
                    'date_mise_a_jour': 'derniere_maj'
                }

                # Mise à jour des champs
                for key, value in data.items():
                    # Utiliser le mapping si nécessaire
                    attr_name = attribute_mapping.get(key, key)

                    if hasattr(consultant, attr_name):
                        setattr(consultant, attr_name, value)
                    else:
                        print(
                            f"⚠️ Attribut {attr_name} non trouvé sur le modèle Consultant")

                consultant.derniere_maj = datetime.now()
                session.commit()
                print(f"✅ Consultant {consultant_id} mis à jour avec succès")
                return True

        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du consultant: {e}")
            return False

    @staticmethod
    def delete_consultant(consultant_id: int) -> bool:
        """Supprime un consultant"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant).filter(
                    Consultant.id == consultant_id).first()

                if not consultant:
                    print(f"❌ Consultant avec l'ID {consultant_id} non trouvé")
                    return False

                print(
                    f"🔄 Suppression en cours du consultant {
                        consultant.prenom} {
                        consultant.nom} (ID: {consultant_id})")
                session.delete(consultant)
                session.commit()
                print(f"✅ Consultant {consultant_id} supprimé avec succès")
                return True

        except Exception as e:
            print(f"❌ Erreur lors de la suppression du consultant {consultant_id}: {e}")
            print(f"Type d'erreur: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False

    @staticmethod
    def search_consultants(search_term: str) -> List[Consultant]:
        """Recherche des consultants par nom, prénom ou email"""
        try:
            with get_database_session() as session:
                return session.query(Consultant)\
                    .filter(
                        (Consultant.nom.ilike(f"%{search_term}%")) |
                        (Consultant.prenom.ilike(f"%{search_term}%")) |
                        (Consultant.email.ilike(f"%{search_term}%"))
                )\
                    .all()
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return []

    @staticmethod
    def get_consultants_count() -> int:
        """Retourne le nombre total de consultants"""
        try:
            with get_database_session() as session:
                return session.query(Consultant).count()
        except Exception as e:
            print(f"Erreur lors du comptage des consultants: {e}")
            return 0

    @staticmethod
    def get_available_consultants() -> List[Consultant]:
        """Retourne les consultants disponibles"""
        try:
            with get_database_session() as session:
                return session.query(Consultant)\
                    .filter(Consultant.disponibilite)\
                    .all()
        except Exception as e:
            print(f"Erreur lors de la récupération des consultants disponibles: {e}")
            return []

    @staticmethod
    def save_cv_analysis(consultant_id: int, analysis_data: Dict[str, Any]) -> bool:
        """Sauvegarde une analyse de CV complète pour un consultant"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant).filter(
                    Consultant.id == consultant_id).first()
                if not consultant:
                    print(f"Consultant {consultant_id} non trouvé")
                    return False

                # Sauvegarder les missions
                missions_saved = 0
                for mission_data in analysis_data.get('missions', []):
                    if ConsultantService._save_mission_from_analysis(
                            session, consultant_id, mission_data):
                        missions_saved += 1

                # Sauvegarder les compétences
                skills_saved = 0

                # Compétences techniques
                for tech in analysis_data.get('langages_techniques', []):
                    if ConsultantService._save_competence_from_analysis(
                            session, consultant_id, tech, 'technique'):
                        skills_saved += 1

                # Compétences fonctionnelles
                for func_skill in analysis_data.get('competences_fonctionnelles', []):
                    if ConsultantService._save_competence_from_analysis(
                            session, consultant_id, func_skill, 'fonctionnelle'):
                        skills_saved += 1

                # Mettre à jour la date de modification du consultant
                consultant.derniere_maj = datetime.now()

                session.commit()
                print(
                    f"✅ Analyse sauvegardée: {missions_saved} missions, {skills_saved} compétences")
                return True

        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de l'analyse CV: {e}")
            return False

    @staticmethod
    def _save_mission_from_analysis(
            session: Session,
            consultant_id: int,
            mission_data: Dict) -> bool:
        """Sauvegarde une mission extraite de l'analyse CV"""
        try:
            client = mission_data.get('client', '').strip()
            if not client:
                return False

            # Vérifier si cette mission existe déjà (même client + même année)
            date_debut_str = mission_data.get('date_debut', '')
            if date_debut_str and date_debut_str != 'En cours':
                try:
                    if len(date_debut_str) == 4:  # Année seulement
                        date_debut = date(int(date_debut_str), 1, 1)
                    else:
                        date_debut = datetime.strptime(
                            date_debut_str, '%Y-%m-%d').date()
                except BaseException:
                    date_debut = None
            else:
                date_debut = None

            # Vérifier doublons
            if date_debut:
                existing = session.query(Mission).filter(
                    Mission.consultant_id == consultant_id,
                    Mission.client == client,
                    Mission.date_debut == date_debut
                ).first()

                if existing:
                    print(f"Mission {client} {date_debut} déjà existante, ignorée")
                    return False

            # Date de fin
            date_fin_str = mission_data.get('date_fin', '')
            date_fin = None
            if date_fin_str and date_fin_str != 'En cours':
                try:
                    if len(date_fin_str) == 4:  # Année seulement
                        date_fin = date(int(date_fin_str), 12, 31)
                    else:
                        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
                except BaseException:
                    date_fin = None

            # Créer la mission
            mission = Mission(
                consultant_id=consultant_id,
                nom_mission=mission_data.get(
                    'resume',
                    f"Mission chez {client}")[
                    :200],
                client=client,
                date_debut=date_debut or date.today(),
                date_fin=date_fin,
                statut='terminee' if date_fin else 'en_cours',
                technologies_utilisees=', '.join(
                    mission_data.get(
                        'langages_techniques',
                        [])),
                description=mission_data.get(
                    'resume',
                    ''))

            session.add(mission)
            return True

        except Exception as e:
            print(f"Erreur sauvegarde mission {mission_data.get('client', 'N/A')}: {e}")
            return False

    @staticmethod
    def _save_competence_from_analysis(
            session: Session,
            consultant_id: int,
            competence_name: str,
            type_competence: str) -> bool:
        """Sauvegarde une compétence extraite de l'analyse CV"""
        try:
            competence_name = competence_name.strip()
            if not competence_name:
                return False

            # Chercher ou créer la compétence
            competence = session.query(Competence).filter(
                Competence.nom == competence_name).first()

            if not competence:
                # Déterminer la catégorie automatiquement
                categorie = ConsultantService._determine_skill_category(
                    competence_name, type_competence)

                competence = Competence(
                    nom=competence_name,
                    categorie=categorie,
                    type_competence=type_competence
                )
                session.add(competence)
                session.flush()  # Pour obtenir l'ID

            # Vérifier si le consultant a déjà cette compétence
            existing_consultant_competence = session.query(ConsultantCompetence).filter(
                ConsultantCompetence.consultant_id == consultant_id,
                ConsultantCompetence.competence_id == competence.id
            ).first()

            if not existing_consultant_competence:
                # Ajouter la relation consultant-compétence
                consultant_competence = ConsultantCompetence(
                    consultant_id=consultant_id,
                    competence_id=competence.id,
                    annees_experience=1.0,  # Valeur par défaut
                    niveau_maitrise='intermediaire'  # Valeur par défaut
                )
                session.add(consultant_competence)
                return True
            else:
                # Compétence déjà existante
                return False

        except Exception as e:
            print(f"Erreur sauvegarde compétence {competence_name}: {e}")
            return False

    @staticmethod
    def _determine_skill_category(skill_name: str, type_competence: str) -> str:
        """Détermine automatiquement la catégorie d'une compétence"""
        skill_lower = skill_name.lower()

        if type_competence == 'fonctionnelle':
            if any(
                word in skill_lower for word in [
                    'management',
                    'leadership',
                    'gestion',
                    'direction']):
                return 'Management'
            elif any(word in skill_lower for word in ['scrum', 'agile', 'kanban', 'projet']):
                return 'Methodologie'
            elif any(word in skill_lower for word in ['formation', 'conseil', 'accompagnement']):
                return 'Conseil'
            else:
                return 'Fonctionnelle'

        # Compétences techniques
        frontend_keywords = [
            'react',
            'angular',
            'vue',
            'javascript',
            'typescript',
            'html',
            'css']
        backend_keywords = [
            'java',
            'python',
            'spring',
            'django',
            'flask',
            'node.js',
            'express']
        database_keywords = ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis']
        cloud_keywords = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'cloud']
        devops_keywords = [
            'jenkins',
            'gitlab',
            'github',
            'ci/cd',
            'terraform',
            'ansible']

        if any(keyword in skill_lower for keyword in frontend_keywords):
            return 'Frontend'
        elif any(keyword in skill_lower for keyword in backend_keywords):
            return 'Backend'
        elif any(keyword in skill_lower for keyword in database_keywords):
            return 'Database'
        elif any(keyword in skill_lower for keyword in cloud_keywords):
            return 'Cloud'
        elif any(keyword in skill_lower for keyword in devops_keywords):
            return 'DevOps'
        else:
            return 'Technique'

    @staticmethod
    def save_cv_analysis(consultant_id: int, analysis_data: Dict[str, Any]) -> bool:
        """
        Sauvegarde les résultats d'analyse de CV dans le profil du consultant

        Args:
            consultant_id: ID du consultant
            analysis_data: Dictionnaire contenant les données d'analyse (missions, compétences, etc.)

        Returns:
            bool: True si succès, False sinon
        """
        try:
            with get_database_session() as session:
                # Vérifier que le consultant existe
                consultant = session.query(Consultant).filter(
                    Consultant.id == consultant_id).first()
                if not consultant:
                    st.error(f"❌ Consultant avec ID {consultant_id} introuvable")
                    return False

                st.info(
                    f"💾 Sauvegarde de l'analyse CV pour {
                        consultant.prenom} {
                        consultant.nom}")

                missions_count = 0
                skills_count = 0

                # 1. Sauvegarder les missions
                missions = analysis_data.get('missions', [])
                for mission_data in missions:
                    if not mission_data.get('client'):
                        continue

                    # Ignorer les missions sans dates valides
                    if not mission_data.get(
                            'date_debut') or mission_data.get('date_debut') == '':
                        st.warning(
                            f"⚠️ Mission {
                                mission_data['client']} ignorée - dates manquantes")
                        continue

                    # Vérifier si la mission existe déjà (éviter les doublons)
                    existing_mission = session.query(Mission).filter(
                        Mission.consultant_id == consultant_id,
                        Mission.client == mission_data['client'],
                        Mission.date_debut == mission_data.get('date_debut', '')
                    ).first()

                    if not existing_mission:
                        # Convertir les dates si nécessaire
                        date_debut = mission_data.get('date_debut')
                        date_fin = mission_data.get('date_fin')

                        # Conversion des dates string vers date objects
                        try:
                            if date_debut and date_debut != 'En cours':
                                if len(date_debut) >= 10:  # Format YYYY-MM-DD
                                    date_debut = datetime.strptime(
                                        date_debut[:10], '%Y-%m-%d').date()
                                else:
                                    continue  # Ignorer si format de date invalide
                            else:
                                continue  # Ignorer si pas de date de début

                            if date_fin and date_fin != 'En cours':
                                if len(date_fin) >= 10:  # Format YYYY-MM-DD
                                    date_fin = datetime.strptime(
                                        date_fin[:10], '%Y-%m-%d').date()
                                else:
                                    date_fin = None
                            else:
                                date_fin = None
                        except ValueError:
                            st.warning(
                                f"⚠️ Mission {
                                    mission_data['client']} ignorée - format de date invalide")
                            continue

                        # Créer la nouvelle mission
                        new_mission = Mission(
                            consultant_id=consultant_id,
                            nom_mission=f"Mission chez {mission_data['client']}",
                            client=mission_data['client'],
                            role=mission_data.get('role', ''),  # Nouveau champ role
                            description=mission_data.get('resume', ''),
                            date_debut=date_debut,
                            date_fin=date_fin,
                            statut='en_cours' if date_fin is None else 'terminee',
                            technologies_utilisees=', '.join(
                                mission_data.get('langages_techniques', [])),
                            revenus_generes=0  # À compléter manuellement
                        )

                        session.add(new_mission)
                        missions_count += 1
                        st.success(f"✅ Mission ajoutée: {mission_data['client']}")

                # 2. Sauvegarder les compétences techniques
                technical_skills = analysis_data.get('langages_techniques', [])
                for skill_name in technical_skills:
                    if not skill_name or len(skill_name.strip()) < 2:
                        continue

                    skill_name = skill_name.strip()

                    # Vérifier si la compétence existe déjà dans le référentiel
                    competence = session.query(Competence).filter(
                        Competence.nom.ilike(f'%{skill_name}%')
                    ).first()

                    if not competence:
                        # Créer la compétence dans le référentiel
                        competence = Competence(
                            nom=skill_name,
                            type_competence='technique',
                            categorie=ConsultantService._determine_skill_category(
                                skill_name,
                                'technique'),
                            description=f'Compétence technique extraite automatiquement du CV')
                        session.add(competence)
                        session.flush()  # Pour obtenir l'ID

                    # Vérifier si le consultant a déjà cette compétence
                    existing_skill = session.query(ConsultantCompetence).filter(
                        ConsultantCompetence.consultant_id == consultant_id,
                        ConsultantCompetence.competence_id == competence.id
                    ).first()

                    if not existing_skill:
                        # Ajouter la compétence au consultant
                        consultant_skill = ConsultantCompetence(
                            consultant_id=consultant_id,
                            competence_id=competence.id,
                            niveau_maitrise='intermediaire',  # Par défaut
                            annees_experience=2.0  # Estimation par défaut
                        )
                        session.add(consultant_skill)
                        skills_count += 1
                        st.success(f"✅ Compétence technique ajoutée: {skill_name}")

                # 3. Sauvegarder les compétences fonctionnelles
                functional_skills = analysis_data.get('competences_fonctionnelles', [])
                for skill_name in functional_skills:
                    if not skill_name or len(skill_name.strip()) < 2:
                        continue

                    skill_name = skill_name.strip()

                    # Vérifier si la compétence existe déjà dans le référentiel
                    competence = session.query(Competence).filter(
                        Competence.nom.ilike(f'%{skill_name}%')
                    ).first()

                    if not competence:
                        # Créer la compétence dans le référentiel
                        competence = Competence(
                            nom=skill_name,
                            type_competence='fonctionnelle',
                            categorie=ConsultantService._determine_skill_category(
                                skill_name,
                                'fonctionnelle'),
                            description=f'Compétence fonctionnelle extraite automatiquement du CV')
                        session.add(competence)
                        session.flush()  # Pour obtenir l'ID

                    # Vérifier si le consultant a déjà cette compétence
                    existing_skill = session.query(ConsultantCompetence).filter(
                        ConsultantCompetence.consultant_id == consultant_id,
                        ConsultantCompetence.competence_id == competence.id
                    ).first()

                    if not existing_skill:
                        # Ajouter la compétence au consultant
                        consultant_skill = ConsultantCompetence(
                            consultant_id=consultant_id,
                            competence_id=competence.id,
                            niveau_maitrise='intermediaire',  # Par défaut
                            annees_experience=2.0  # Estimation par défaut
                        )
                        session.add(consultant_skill)
                        skills_count += 1
                        st.success(f"✅ Compétence fonctionnelle ajoutée: {skill_name}")

                # 4. Mettre à jour la date de dernière modification du consultant
                consultant.derniere_maj = datetime.now()

                # Committer toutes les modifications
                session.commit()

                st.success(f"🎉 Analyse CV sauvegardée avec succès !")
                st.info(
                    f"📊 **Résumé**: {missions_count} missions ajoutées, {skills_count} compétences ajoutées")

                return True

        except Exception as e:
            st.error(f"❌ Erreur lors de la sauvegarde de l'analyse CV: {e}")
            print(f"Erreur détaillée: {e}")
            import traceback
            traceback.print_exc()
            return False
