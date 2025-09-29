"""
Service de gestion des consultants
CRUD operations pour les consultants avec la base de donnÃ©es
OptimisÃ© pour gÃ©rer 1000+ consultants avec cache et pagination efficace
"""

from datetime import date
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import streamlit as st
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.database.database import get_database_session
from app.database.models import Competence
from app.database.models import Consultant
from app.database.models import ConsultantCompetence
from app.database.models import Mission
from app.database.models import Practice


class ConsultantService:
    """Service pour la gestion des consultants optimisÃ© pour de gros volumes"""

    # Constantes pour éviter la duplication de chaînes (SonarQube)
    STATUS_AVAILABLE = "✅ Disponible"
    STATUS_BUSY = "🔴 Occupé"
    STATUS_IN_PROGRESS = "En cours"

    @staticmethod
    def get_all_consultants_objects(
        page: int = 1, per_page: int = 50
    ) -> List[Consultant]:
        """
        RÃ©cupÃ¨re tous les consultants comme objets (ancienne interface)

        Args:
            page: NumÃ©ro de la page (commence Ã  1)
            per_page: Nombre de consultants par page

        Returns:
            Liste d'objets Consultant dÃ©tachÃ©s de la session

        Raises:
            SQLAlchemyError: En cas d'erreur de base de donnÃ©es
        """
        try:
            with get_database_session() as session:
                consultants = (
                    session.query(Consultant)
                    .options(joinedload(Consultant.practice))
                    .offset((page - 1) * per_page)
                    .limit(per_page)
                    .all()
                )

                # DÃ©tacher les instances de la session pour Ã©viter les erreurs
                # DetachedInstance
                for consultant in consultants:
                    session.expunge(consultant)

                return consultants
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la rÃ©cupÃ©ration des consultants: {e}")
            return []

    @staticmethod
    def get_all_consultants(page: int = 1, per_page: int = 50) -> List[Dict]:
        """RÃ©cupÃ¨re tous les consultants avec pagination optimisÃ©e"""
        try:
            with get_database_session() as session:
                consultants = (
                    session.query(Consultant)
                    .options(joinedload(Consultant.practice))
                    .offset((page - 1) * per_page)
                    .limit(per_page)
                    .all()
                )

                # Convertir en dictionnaires pour Ã©viter les erreurs de session
                consultant_list = []
                for consultant in consultants:
                    consultant_dict = {
                        "id": consultant.id,
                        "prenom": consultant.prenom,
                        "nom": consultant.nom,
                        "email": consultant.email,
                        "telephone": consultant.telephone,
                        "salaire_actuel": consultant.salaire_actuel,
                        "disponibilite": consultant.disponibilite,
                        "practice_name": (
                            consultant.practice.nom if consultant.practice else "N/A"
                        ),
                        "date_creation": consultant.date_creation,
                        "derniere_maj": consultant.derniere_maj,
                        # Nouveaux champs V1.2.2
                        "date_disponibilite": consultant.date_disponibilite,
                        "experience_annees": consultant.experience_annees,
                        "grade": consultant.grade,
                        "type_contrat": consultant.type_contrat,
                        "societe": consultant.societe,
                    }
                    consultant_list.append(consultant_dict)

                return consultant_list
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la rÃ©cupÃ©ration des consultants: {e}")
            return []

    @staticmethod
    def _build_search_query(
        session, practice_filter, grade_filter, availability_filter, search_term
    ):
        """Helper: Construit la requête de base avec les filtres"""
        # Requête optimisée avec JOIN pour éviter les requêtes N+1
        query = (
            session.query(
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
                Practice.nom.label("practice_name"),
                func.count(Mission.id).label("nb_missions"),
            )
            .outerjoin(Practice, Consultant.practice_id == Practice.id)
            .outerjoin(Mission, Consultant.id == Mission.consultant_id)
        )

        return ConsultantService._apply_search_filters(
            query, practice_filter, grade_filter, availability_filter, search_term
        )

    @staticmethod
    def _apply_search_filters(
        query, practice_filter, grade_filter, availability_filter, search_term
    ):
        """Helper: Applique tous les filtres de recherche"""
        # Appliquer les filtres
        if practice_filter:
            query = query.filter(Practice.nom == practice_filter)

        if grade_filter:
            query = query.filter(Consultant.grade == grade_filter)

        if availability_filter is not None:
            query = query.filter(Consultant.disponibilite == availability_filter)

        if search_term:
            search_filter = f"%{search_term}%"
            query = query.filter(
                (Consultant.nom.ilike(search_filter))
                | (Consultant.prenom.ilike(search_filter))
                | (Consultant.email.ilike(search_filter))
                | (Consultant.societe.ilike(search_filter))
            )

        return query

    @staticmethod
    def _finalize_search_query(query, page, per_page):
        """Helper: Finalise la requête avec grouping et pagination"""
        return (
            query.group_by(
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
                Practice.nom,
            )
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

    @staticmethod
    def _convert_consultant_row_to_dict(row):
        """Helper: Convertit une ligne de résultat en dictionnaire"""
        salaire = row.salaire_actuel or 0
        cjm = (salaire * 1.8 / 216) if salaire else 0

        # Calcul de l'expérience
        experience_annees = ConsultantService._calculate_experience_years(
            row.date_premiere_mission
        )

        return {
            "id": row.id,
            "prenom": row.prenom,
            "nom": row.nom,
            "email": row.email,
            "telephone": row.telephone,
            "salaire_actuel": salaire,
            "disponibilite": row.disponibilite,
            "grade": row.grade or "Junior",
            "type_contrat": row.type_contrat or "CDI",
            "practice_name": row.practice_name or "Non affecté",
            "date_creation": row.date_creation,
            "nb_missions": row.nb_missions,
            "cjm": cjm,
            "salaire_formatted": f"{salaire:,}€",
            "cjm_formatted": f"{cjm:,.0f}€",
            "statut": (
                ConsultantService.STATUS_AVAILABLE
                if row.disponibilite
                else ConsultantService.STATUS_BUSY
            ),
            # Nouveaux champs V1.2
            "societe": row.societe or "Quanteam",
            "experience_annees": experience_annees,
            "experience_formatted": (
                f"{experience_annees} ans" if experience_annees > 0 else "N/A"
            ),
        }

    @staticmethod
    def _calculate_experience_years(date_premiere_mission):
        """Helper: Calcule l'expérience en années"""
        if not date_premiere_mission:
            return 0

        from datetime import date

        today = date.today()
        delta = today - date_premiere_mission
        return round(delta.days / 365.25, 1)

    @staticmethod
    def search_consultants_optimized(
        search_term: str,
        page: int = 1,
        per_page: int = 50,
        practice_filter: Optional[str] = None,
        grade_filter: Optional[str] = None,
        availability_filter: Optional[bool] = None,
    ) -> List[Dict]:
        """Recherche optimisée avec cache pour de gros volumes - avec statistiques intégrées"""
        try:
            with get_database_session() as session:
                # Construire et exécuter la requête
                query = ConsultantService._build_search_query(
                    session,
                    practice_filter,
                    grade_filter,
                    availability_filter,
                    search_term,
                )
                query = ConsultantService._finalize_search_query(query, page, per_page)
                results = query.all()

                # Convertir en dictionnaires avec calculs optimisés
                consultant_list = []
                for row in results:
                    consultant_dict = ConsultantService._convert_consultant_row_to_dict(
                        row
                    )
                    consultant_list.append(consultant_dict)

                return consultant_list
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la recherche optimisée: {e}")
            return []

    @staticmethod
    def get_consultants_count() -> int:
        """Retourne le nombre total de consultants avec cache"""
        try:
            with get_database_session() as session:
                return session.query(Consultant).count()
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors du comptage des consultants: {e}")
            return 0

    @staticmethod
    def _build_stats_query(session, practice_filter, grade_filter, availability_filter):
        """Helper: Construit la requête optimisée pour les stats des consultants"""
        # Une seule requête avec LEFT JOIN pour récupérer consultants + nombre de missions
        query = (
            session.query(
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
                Practice.nom.label("practice_name"),
                func.count(Mission.id).label("nb_missions"),
            )
            .outerjoin(Practice, Consultant.practice_id == Practice.id)
            .outerjoin(Mission, Consultant.id == Mission.consultant_id)
        )

        return ConsultantService._apply_stats_filters(
            query, practice_filter, grade_filter, availability_filter
        )

    @staticmethod
    def _apply_stats_filters(query, practice_filter, grade_filter, availability_filter):
        """Helper: Applique les filtres pour les statistiques"""
        # Appliquer les filtres
        if practice_filter:
            query = query.filter(Practice.nom == practice_filter)

        if grade_filter:
            query = query.filter(Consultant.grade == grade_filter)

        if availability_filter is not None:
            query = query.filter(Consultant.disponibilite == availability_filter)

        return query

    @staticmethod
    def _finalize_stats_query(query, page, per_page):
        """Helper: Finalise la requête stats avec grouping et pagination"""
        return (
            query.group_by(
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
                Practice.nom,
            )
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

    @staticmethod
    def _convert_stats_row_to_dict(row):
        """Helper: Convertit une ligne de résultat stats en dictionnaire"""
        salaire = row.salaire_actuel or 0
        cjm = (salaire * 1.8 / 216) if salaire else 0

        # Calcul de l'expérience
        experience_annees = ConsultantService._calculate_experience_years(
            row.date_premiere_mission
        )

        return {
            "id": row.id,
            "prenom": row.prenom,
            "nom": row.nom,
            "email": row.email,
            "telephone": row.telephone,
            "salaire_actuel": salaire,
            "disponibilite": row.disponibilite,
            "practice_name": row.practice_name or "Non affecté",
            "date_creation": row.date_creation,
            "derniere_maj": row.derniere_maj,
            "nb_missions": row.nb_missions,
            "cjm": cjm,
            "salaire_formatted": f"{salaire:,}€",
            "cjm_formatted": f"{cjm:,.0f}€",
            "statut": (
                ConsultantService.STATUS_AVAILABLE
                if row.disponibilite
                else ConsultantService.STATUS_BUSY
            ),
            # Nouveaux champs V1.2
            "societe": row.societe or "Quanteam",
            "experience_annees": experience_annees,
            "experience_formatted": (
                f"{experience_annees} ans" if experience_annees > 0 else "N/A"
            ),
            # Nouveaux champs V1.2.1
            "grade": row.grade or "Junior",
            "type_contrat": row.type_contrat or "CDI",
        }

    @staticmethod
    def get_all_consultants_with_stats(
        page: int = 1,
        per_page: int = 50,
        practice_filter: Optional[str] = None,
        grade_filter: Optional[str] = None,
        availability_filter: Optional[bool] = None,
    ) -> List[Dict]:
        """
        Récupère tous les consultants avec leurs statistiques en une seule requête optimisée
        Résout le problème N+1 des requêtes pour compter les missions
        """
        try:
            with get_database_session() as session:
                # Construire et exécuter la requête
                query = ConsultantService._build_stats_query(
                    session, practice_filter, grade_filter, availability_filter
                )
                query = ConsultantService._finalize_stats_query(query, page, per_page)
                results = query.all()

                # Convertir en dictionnaires avec calculs optimisés
                consultant_list = []
                for row in results:
                    consultant_dict = ConsultantService._convert_stats_row_to_dict(row)
                    consultant_list.append(consultant_dict)

                return consultant_list
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la récupération optimisée des consultants: {e}")
            return []

    @staticmethod
    def get_consultant_summary_stats() -> Dict[str, int]:
        """RÃ©cupÃ¨re les statistiques gÃ©nÃ©rales avec cache pour tableau de bord"""
        try:
            with get_database_session() as session:
                total_consultants = session.query(Consultant).count()
                available_consultants = (
                    session.query(Consultant).filter(Consultant.disponibilite).count()
                )
                total_missions = session.query(Mission).count()
                active_missions = (
                    session.query(Mission).filter(Mission.statut == "en_cours").count()
                )

                return {
                    "total_consultants": total_consultants,
                    "available_consultants": available_consultants,
                    "total_missions": total_missions,
                    "active_missions": active_missions,
                    "busy_consultants": total_consultants - available_consultants,
                }
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la rÃ©cupÃ©ration des stats: {e}")
            return {
                "total_consultants": 0,
                "available_consultants": 0,
                "total_missions": 0,
                "active_missions": 0,
                "busy_consultants": 0,
            }

    @staticmethod
    def get_consultants_by_availability(available: bool = True) -> List[Dict]:
        """
        RÃ©cupÃ¨re les consultants selon leur disponibilitÃ©

        Args:
            available: True pour les consultants disponibles, False pour les occupÃ©s

        Returns:
            Liste de dictionnaires contenant les informations des consultants

        Example:
            >>> disponibles = ConsultantService.get_consultants_by_availability(True)
            >>> print(f"Nombre de consultants disponibles: {len(disponibles)}")
        """
        try:
            with get_database_session() as session:
                consultants = (
                    session.query(Consultant)
                    .filter(Consultant.disponibilite == available)
                    .all()
                )

                # Convertir en dictionnaires
                result = []
                for consultant in consultants:
                    result.append(
                        {
                            "id": consultant.id,
                            "prenom": consultant.prenom,
                            "nom": consultant.nom,
                            "email": consultant.email,
                            "telephone": consultant.telephone,
                            "salaire_actuel": consultant.salaire_actuel,
                            "disponibilite": consultant.disponibilite,
                            "grade": consultant.grade,
                            "type_contrat": consultant.type_contrat,
                            "statut": (
                                "â Disponible"
                                if consultant.disponibilite
                                else "ð´ OccupÃ©"
                            ),
                        }
                    )

                return result
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(
                f"Erreur lors de la rÃ©cupÃ©ration des consultants par disponibilitÃ©: {e}"
            )
            return []

    @staticmethod
    def get_consultant_by_id(consultant_id: int) -> Optional[Consultant]:
        """RÃ©cupÃ¨re un consultant par son ID avec toutes ses relations"""
        try:
            with get_database_session() as session:
                consultant = (
                    session.query(Consultant)
                    .options(
                        joinedload(Consultant.competences),
                        joinedload(Consultant.missions),
                    )
                    .filter(Consultant.id == consultant_id)
                    .first()
                )

                # DÃ©tacher l'objet de la session pour Ã©viter les erreurs de session
                # fermÃ©e
                if consultant:
                    session.expunge(consultant)

                return consultant
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(
                f"Erreur lors de la rÃ©cupÃ©ration du consultant {consultant_id}: {e}"
            )
            return None

    @staticmethod
    def get_consultant_with_stats(consultant_id: int) -> Optional[Dict[str, Any]]:
        """RÃ©cupÃ¨re un consultant avec ses statistiques pour Ã©viter les problÃ¨mes de session"""
        try:
            with get_database_session() as session:
                consultant = (
                    session.query(Consultant)
                    .options(
                        joinedload(Consultant.competences).joinedload(
                            ConsultantCompetence.competence
                        ),
                        joinedload(Consultant.missions),
                    )
                    .filter(Consultant.id == consultant_id)
                    .first()
                )

                if not consultant:
                    return None

                # Calculer les statistiques avant de fermer la session
                competences_count = (
                    len(consultant.competences) if consultant.competences else 0
                )
                missions_count = len(consultant.missions) if consultant.missions else 0

                # Convertir en dictionnaire avec toutes les donnÃ©es nÃ©cessaires
                consultant_data = {
                    "id": consultant.id,
                    "prenom": consultant.prenom,
                    "nom": consultant.nom,
                    "email": consultant.email,
                    "telephone": consultant.telephone,
                    "salaire_actuel": consultant.salaire_actuel,
                    "disponibilite": consultant.disponibilite,
                    "notes": consultant.notes,
                    "date_creation": consultant.date_creation,
                    "derniere_maj": consultant.derniere_maj,
                    "competences_count": competences_count,
                    "missions_count": missions_count,
                    "competences": [
                        {
                            "id": comp.competence.id if comp.competence else comp.id,
                            "nom": comp.competence.nom if comp.competence else "N/A",
                            "niveau": comp.niveau_maitrise,
                            "annees_experience": comp.annees_experience,
                        }
                        for comp in (consultant.competences or [])
                    ],
                    "missions": [
                        {
                            "id": mission.id,
                            "nom_mission": mission.nom_mission,
                            "client": mission.client,
                            "description": mission.description,
                            "date_debut": mission.date_debut,
                            "date_fin": mission.date_fin,
                            "statut": mission.statut,
                            "revenus_generes": mission.revenus_generes,
                        }
                        for mission in (consultant.missions or [])
                    ],
                }

                return consultant_data

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(
                f"Erreur lors de la rÃ©cupÃ©ration du consultant avec stats {consultant_id}: {e}"
            )
            return None

    @staticmethod
    def get_consultant_by_email(email: str) -> Optional[Consultant]:
        """
        RÃ©cupÃ¨re un consultant par son email

        Args:
            email: Adresse email du consultant (insensible Ã  la casse)

        Returns:
            Objet Consultant si trouvÃ©, None sinon

        Example:
            >>> consultant = ConsultantService.get_consultant_by_email("jean.dupont@email.com")
            >>> if consultant:
            ...     print(f"Consultant trouvÃ©: {consultant.prenom} {consultant.nom}")
        """
        try:
            with get_database_session() as session:
                return (
                    session.query(Consultant)
                    .filter(Consultant.email == email.lower())
                    .first()
                )
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(
                f"Erreur lors de la rÃ©cupÃ©ration du consultant par email {email}: {e}"
            )
            return None

    @staticmethod
    def create_consultant(data: dict) -> bool:
        """
        CrÃ©e un nouveau consultant dans la base de donnÃ©es

        Args:
            data: Dictionnaire contenant les donnÃ©es du consultant avec les clÃ©s:
                - prenom (str): PrÃ©nom du consultant (requis)
                - nom (str): Nom du consultant (requis)
                - email (str): Email du consultant (requis)
                - telephone (str, optional): NumÃ©ro de tÃ©lÃ©phone
                - salaire (float, optional): Salaire actuel
                - practice_id (int, optional): ID de la practice
                - disponible (bool, optional): DisponibilitÃ© (dÃ©faut: True)
                - notes (str, optional): Notes complÃ©mentaires
                - societe (str, optional): SociÃ©tÃ© (dÃ©faut: "Quanteam")
                - grade (str, optional): Grade du consultant (dÃ©faut: "Junior")
                - type_contrat (str, optional): Type de contrat (dÃ©faut: "CDI")

        Returns:
            bool: True si la crÃ©ation a rÃ©ussi, False sinon

        Example:
            >>> data = {
            ...     "prenom": "Jean",
            ...     "nom": "Dupont",
            ...     "email": "jean.dupont@email.com",
            ...     "salaire": 45000.0,
            ...     "grade": "Senior"
            ... }
            >>> success = ConsultantService.create_consultant(data)
            >>> print("CrÃ©ation rÃ©ussie" if success else "Ãchec de crÃ©ation")
        """
        try:
            # Validation des champs requis
            required_fields = ["prenom", "nom", "email"]
            for field in required_fields:
                if not data.get(field) or str(data.get(field, "")).strip() == "":
                    print(f"â Champ requis manquant ou vide: {field}")
                    return False

            # Validation de l'email
            email = data.get("email", "").strip()
            if "@" not in email or "." not in email:
                print(f"â Format d'email invalide: {email}")
                return False

            # VÃ©rifier l'unicitÃ© de l'email
            with get_database_session() as session:
                existing_consultant = (
                    session.query(Consultant)
                    .filter(Consultant.email == email.lower())
                    .first()
                )
                if existing_consultant:
                    print(f"â Email dÃ©jÃ  utilisÃ©: {email}")
                    return False

            with get_database_session() as session:
                consultant = Consultant(
                    prenom=data.get("prenom").strip(),
                    nom=data.get("nom").strip(),
                    email=email.lower(),
                    telephone=(
                        data.get("telephone", "").strip()
                        if data.get("telephone")
                        else None
                    ),
                    salaire_actuel=data.get("salaire_actuel") or data.get("salaire"),
                    practice_id=data.get("practice_id"),
                    disponibilite=data.get("disponibilite", True),
                    notes=data.get("notes", "").strip() if data.get("notes") else None,
                    date_creation=datetime.now(),
                    derniere_maj=datetime.now(),
                    # Nouveaux champs V1.2
                    societe=data.get("societe", "Quanteam").strip(),
                    date_entree_societe=data.get("date_entree_societe"),
                    date_sortie_societe=data.get("date_sortie_societe"),
                    date_premiere_mission=data.get("date_premiere_mission"),
                    # Nouveaux champs V1.2.1
                    grade=data.get("grade", "Junior").strip(),
                    type_contrat=data.get("type_contrat", "CDI").strip(),
                )

                session.add(consultant)
                session.commit()
                print(
                    f"â Consultant {data.get('prenom')} {data.get('nom')} crÃ©Ã© avec succÃ¨s"
                )
                return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"â Erreur lors de la crÃ©ation du consultant: {e}")
            return False

    @staticmethod
    def update_consultant(consultant_id: int, data: dict) -> bool:
        """
        Met Ã  jour un consultant existant dans la base de donnÃ©es

        Args:
            consultant_id: ID du consultant Ã  mettre Ã  jour
            data: Dictionnaire contenant les champs Ã  mettre Ã  jour

        Returns:
            bool: True si la mise Ã  jour a rÃ©ussi, False sinon

        Example:
            >>> data = {"salaire": 50000.0, "disponible": False}
            >>> success = ConsultantService.update_consultant(123, data)
            >>> print("Mise Ã  jour rÃ©ussie" if success else "Ãchec de mise Ã  jour")
        """
        try:
            with get_database_session() as session:
                consultant = (
                    session.query(Consultant)
                    .filter(Consultant.id == consultant_id)
                    .first()
                )

                if not consultant:
                    print(f"â Consultant avec l'ID {consultant_id} non trouvÃ©")
                    return False

                # Mapping des attributs pour Ã©viter les erreurs
                attribute_mapping = {
                    "salaire": "salaire_actuel",
                    "disponibilite": "disponibilite",
                    "date_mise_a_jour": "derniere_maj",
                }

                # Mise Ã  jour des champs
                for key, value in data.items():
                    # Utiliser le mapping si nÃ©cessaire
                    attr_name = attribute_mapping.get(key, key)

                    if hasattr(consultant, attr_name):
                        setattr(consultant, attr_name, value)
                    else:
                        print(
                            f"â ï¸ Attribut {attr_name} non trouvÃ© sur le modÃ¨le Consultant"
                        )

                consultant.derniere_maj = datetime.now()
                session.commit()
                print(f"â Consultant {consultant_id} mis Ã  jour avec succÃ¨s")
                return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"â Erreur lors de la mise Ã  jour du consultant: {e}")
            return False

    @staticmethod
    def delete_consultant(consultant_id: int) -> bool:
        """
        Supprime un consultant de la base de donnÃ©es

        Args:
            consultant_id: ID du consultant Ã  supprimer

        Returns:
            bool: True si la suppression a rÃ©ussi, False sinon

        Note:
            Cette opÃ©ration est irrÃ©versible et supprime Ã©galement toutes les
            relations associÃ©es (missions, compÃ©tences, etc.)

        Example:
            >>> success = ConsultantService.delete_consultant(123)
            >>> print("Suppression rÃ©ussie" if success else "Ãchec de suppression")
        """
        try:
            with get_database_session() as session:
                consultant = (
                    session.query(Consultant)
                    .filter(Consultant.id == consultant_id)
                    .first()
                )

                if not consultant:
                    print(f"â Consultant avec l'ID {consultant_id} non trouvÃ©")
                    return False

                print(
                    f"ð Suppression en cours du consultant {consultant.prenom} {consultant.nom} (ID: {consultant_id})"
                )
                session.delete(consultant)
                session.commit()
                print(f"â Consultant {consultant_id} supprimÃ© avec succÃ¨s")
                return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"â Erreur lors de la suppression du consultant {consultant_id}: {e}")
            print(f"Type d'erreur: {type(e).__name__}")
            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def search_consultants(search_term: str) -> List[Consultant]:
        """
        Recherche des consultants par nom, prÃ©nom ou email

        Args:
            search_term: Terme de recherche (insensible Ã  la casse)

        Returns:
            Liste d'objets Consultant correspondant Ã  la recherche

        Example:
            >>> consultants = ConsultantService.search_consultants("dupont")
            >>> print(f"TrouvÃ© {len(consultants)} consultant(s)")
        """
        try:
            with get_database_session() as session:
                return (
                    session.query(Consultant)
                    .filter(
                        (Consultant.nom.ilike(f"%{search_term}%"))
                        | (Consultant.prenom.ilike(f"%{search_term}%"))
                        | (Consultant.email.ilike(f"%{search_term}%"))
                        | (Consultant.societe.ilike(f"%{search_term}%"))
                    )
                    .all()
                )
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la recherche: {e}")
            return []

    @staticmethod
    def get_available_consultants() -> List[Consultant]:
        """
        Retourne la liste des consultants actuellement disponibles

        Returns:
            Liste d'objets Consultant avec disponibilite=True

        Example:
            >>> disponibles = ConsultantService.get_available_consultants()
            >>> print(f"{len(disponibles)} consultants disponibles pour de nouvelles missions")
        """
        try:
            with get_database_session() as session:
                return session.query(Consultant).filter(Consultant.disponibilite).all()
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la rÃ©cupÃ©ration des consultants disponibles: {e}")
            return []

    @staticmethod
    def _save_mission_from_analysis(
        session: Session, consultant_id: int, mission_data: Dict
    ) -> bool:
        """
        Sauvegarde une mission extraite de l'analyse CV (méthode privée)

        Args:
            session: Session de base de données active
            consultant_id: ID du consultant propriétaire de la mission
            mission_data: Dictionnaire contenant les données de la mission

        Returns:
            bool: True si la mission a été sauvegardée, False sinon
        """
        try:
            client = mission_data.get("client", "").strip()
            if not client:
                return False

            # Vérifier les doublons avec date de début
            date_debut = ConsultantService._parse_mission_start_date(mission_data)
            if ConsultantService._mission_already_exists(
                session, consultant_id, client, date_debut
            ):
                return False

            # Traiter la date de fin
            date_fin = ConsultantService._parse_mission_end_date(mission_data)

            # Créer et sauvegarder la mission
            mission = ConsultantService._create_mission_object(
                consultant_id, mission_data, client, date_debut, date_fin
            )
            session.add(mission)
            return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur sauvegarde mission {mission_data.get('client', 'N/A')}: {e}")
            return False

    @staticmethod
    def _parse_mission_start_date(mission_data: Dict) -> Optional[date]:
        """Parse la date de début d'une mission depuis les données"""
        date_debut_str = mission_data.get("date_debut", "")
        if not date_debut_str or date_debut_str == ConsultantService.STATUS_IN_PROGRESS:
            return None

        try:
            if len(date_debut_str) == 4:  # Année seulement
                return date(int(date_debut_str), 1, 1)
            else:
                return datetime.strptime(date_debut_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_mission_end_date(mission_data: Dict) -> Optional[date]:
        """Parse la date de fin d'une mission depuis les données"""
        date_fin_str = mission_data.get("date_fin", "")
        if not date_fin_str or date_fin_str == ConsultantService.STATUS_IN_PROGRESS:
            return None

        try:
            if len(date_fin_str) == 4:  # Année seulement
                return date(int(date_fin_str), 12, 31)
            else:
                return datetime.strptime(date_fin_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _mission_already_exists(
        session: Session, consultant_id: int, client: str, date_debut: Optional[date]
    ) -> bool:
        """Vérifie si une mission similaire existe déjà"""
        if not date_debut:
            return False

        existing = (
            session.query(Mission)
            .filter(
                Mission.consultant_id == consultant_id,
                Mission.client == client,
                Mission.date_debut == date_debut,
            )
            .first()
        )

        if existing:
            print(f"Mission {client} {date_debut} déjà existante, ignorée")
            return True
        return False

    @staticmethod
    def _create_mission_object(
        consultant_id: int,
        mission_data: Dict,
        client: str,
        date_debut: Optional[date],
        date_fin: Optional[date],
    ) -> Mission:
        """Crée un objet Mission à partir des données parsées"""
        return Mission(
            consultant_id=consultant_id,
            nom_mission=mission_data.get("resume", f"Mission chez {client}")[:200],
            client=client,
            date_debut=date_debut or date.today(),
            date_fin=date_fin,
            statut="terminee" if date_fin else "en_cours",
            technologies_utilisees=", ".join(
                mission_data.get("langages_techniques", [])
            ),
            description=mission_data.get("resume", ""),
        )

    @staticmethod
    def _save_competence_from_analysis(
        session: Session, consultant_id: int, competence_name: str, type_competence: str
    ) -> bool:
        """
        Sauvegarde une compÃ©tence extraite de l'analyse CV (mÃ©thode privÃ©e)

        Args:
            session: Session de base de donnÃ©es active
            consultant_id: ID du consultant
            competence_name: Nom de la compÃ©tence Ã  sauvegarder
            type_competence: Type de compÃ©tence ("technique" ou "fonctionnelle")

        Returns:
            bool: True si la compÃ©tence a Ã©tÃ© sauvegardÃ©e, False sinon

        Note:
            Cette mÃ©thode crÃ©e automatiquement la compÃ©tence dans le rÃ©fÃ©rentiel
            si elle n'existe pas dÃ©jÃ
        """
        try:
            competence_name = competence_name.strip()
            if not competence_name:
                return False

            # Chercher ou crÃ©er la compÃ©tence
            competence = (
                session.query(Competence)
                .filter(Competence.nom == competence_name)
                .first()
            )

            if not competence:
                # DÃ©terminer la catÃ©gorie automatiquement
                categorie = ConsultantService._determine_skill_category(
                    competence_name, type_competence
                )

                competence = Competence(
                    nom=competence_name,
                    categorie=categorie,
                    type_competence=type_competence,
                )
                session.add(competence)
                session.flush()  # Pour obtenir l'ID

            # VÃ©rifier si le consultant a dÃ©jÃ  cette compÃ©tence
            existing_consultant_competence = (
                session.query(ConsultantCompetence)
                .filter(
                    ConsultantCompetence.consultant_id == consultant_id,
                    ConsultantCompetence.competence_id == competence.id,
                )
                .first()
            )

            if not existing_consultant_competence:
                # Ajouter la relation consultant-compÃ©tence
                consultant_competence = ConsultantCompetence(
                    consultant_id=consultant_id,
                    competence_id=competence.id,
                    annees_experience=1.0,  # Valeur par dÃ©faut
                    niveau_maitrise="intermediaire",  # Valeur par dÃ©faut
                )
                session.add(consultant_competence)
                return True
            else:
                # CompÃ©tence dÃ©jÃ  existante
                return False

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur sauvegarde compÃ©tence {competence_name}: {e}")
            return False

    @staticmethod
    def _determine_skill_category(skill_name: str, type_competence: str) -> str:
        """
        Détermine automatiquement la catégorie d'une compétence (méthode privée)

        Args:
            skill_name: Nom de la compétence à classifier
            type_competence: Type de compétence ("technique" ou "fonctionnelle")

        Returns:
            str: Catégorie de la compétence (ex: "Frontend", "Backend", "Management", etc.)
        """
        skill_lower = skill_name.lower()

        if type_competence == "fonctionnelle":
            return ConsultantService._categorize_functional_skill(skill_lower)
        else:
            return ConsultantService._categorize_technical_skill(skill_lower)

    @staticmethod
    def _categorize_functional_skill(skill_lower: str) -> str:
        """Catégorise une compétence fonctionnelle"""
        if ConsultantService._is_management_skill(skill_lower):
            return "Management"
        elif ConsultantService._is_methodology_skill(skill_lower):
            return "Methodologie"
        elif ConsultantService._is_consulting_skill(skill_lower):
            return "Conseil"
        else:
            return "Fonctionnelle"

    @staticmethod
    def _is_management_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence de management"""
        management_keywords = ["management", "leadership", "gestion", "direction"]
        return any(word in skill_lower for word in management_keywords)

    @staticmethod
    def _is_methodology_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence méthodologique"""
        methodology_keywords = ["scrum", "agile", "kanban", "projet"]
        return any(word in skill_lower for word in methodology_keywords)

    @staticmethod
    def _is_consulting_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence de conseil"""
        consulting_keywords = ["formation", "conseil", "accompagnement"]
        return any(word in skill_lower for word in consulting_keywords)

    @staticmethod
    def _categorize_technical_skill(skill_lower: str) -> str:
        """Catégorise une compétence technique"""
        if ConsultantService._is_frontend_skill(skill_lower):
            return "Frontend"
        elif ConsultantService._is_backend_skill(skill_lower):
            return "Backend"
        elif ConsultantService._is_database_skill(skill_lower):
            return "Database"
        elif ConsultantService._is_cloud_skill(skill_lower):
            return "Cloud"
        elif ConsultantService._is_devops_skill(skill_lower):
            return "DevOps"
        else:
            return "Technique"

    @staticmethod
    def _is_frontend_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence frontend"""
        frontend_keywords = [
            "react",
            "angular",
            "vue",
            "javascript",
            "typescript",
            "html",
            "css",
        ]
        return any(keyword in skill_lower for keyword in frontend_keywords)

    @staticmethod
    def _is_backend_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence backend"""
        backend_keywords = [
            "java",
            "python",
            "spring",
            "django",
            "flask",
            "node.js",
            "express",
        ]
        return any(keyword in skill_lower for keyword in backend_keywords)

    @staticmethod
    def _is_database_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence base de données"""
        database_keywords = ["sql", "mysql", "postgresql", "mongodb", "oracle", "redis"]
        return any(keyword in skill_lower for keyword in database_keywords)

    @staticmethod
    def _is_cloud_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence cloud"""
        cloud_keywords = ["aws", "azure", "gcp", "docker", "kubernetes", "cloud"]
        return any(keyword in skill_lower for keyword in cloud_keywords)

    @staticmethod
    def _is_devops_skill(skill_lower: str) -> bool:
        """Vérifie si c'est une compétence DevOps"""
        devops_keywords = [
            "jenkins",
            "gitlab",
            "github",
            "ci/cd",
            "terraform",
            "ansible",
        ]
        return any(keyword in skill_lower for keyword in devops_keywords)

    @staticmethod
    def save_cv_analysis(consultant_id: int, analysis_data: Dict[str, Any]) -> bool:
        """
        Sauvegarde les résultats d'analyse de CV dans le profil du consultant

        Args:
            consultant_id: ID du consultant
            analysis_data: Dictionnaire contenant les données d'analyse

        Returns:
            bool: True si succès, False sinon
        """
        try:
            with get_database_session() as session:
                consultant = ConsultantService._get_consultant_for_cv_analysis(
                    session, consultant_id
                )
                if not consultant:
                    return False

                st.info(
                    f"💾 Sauvegarde de l'analyse CV pour {consultant.prenom} {consultant.nom}"
                )

                # Sauvegarder les différentes parties de l'analyse
                missions_count = ConsultantService._save_cv_missions(
                    session, consultant_id, analysis_data
                )
                skills_count = ConsultantService._save_cv_skills(
                    session, consultant_id, analysis_data
                )

                # Finaliser la sauvegarde
                ConsultantService._finalize_cv_analysis_save(
                    session, consultant, missions_count, skills_count
                )

                return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            st.error("❌ Erreur lors de la sauvegarde de l'analyse CV: " + str(e))
            print(f"Erreur détaillée: {e}")
            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def _get_consultant_for_cv_analysis(session: Session, consultant_id: int):
        """Récupère le consultant pour l'analyse CV"""
        consultant = (
            session.query(Consultant).filter(Consultant.id == consultant_id).first()
        )
        if not consultant:
            st.error(f"❌ Consultant avec ID {consultant_id} introuvable")
        return consultant

    @staticmethod
    def _save_cv_missions(
        session: Session, consultant_id: int, analysis_data: Dict
    ) -> int:
        """Sauvegarde les missions extraites du CV"""
        missions = analysis_data.get("missions", [])
        missions_count = 0

        for mission_data in missions:
            if ConsultantService._should_save_mission(
                mission_data
            ) and ConsultantService._save_single_cv_mission(
                session, consultant_id, mission_data
            ):
                missions_count += 1

        return missions_count

    @staticmethod
    def _should_save_mission(mission_data: Dict) -> bool:
        """Vérifie si une mission doit être sauvegardée"""
        if not mission_data.get("client"):
            return False

        if not mission_data.get("date_debut") or mission_data.get("date_debut") == "":
            st.warning(f"⚠️ Mission {mission_data['client']} ignorée - dates manquantes")
            return False

        return True

    @staticmethod
    def _save_single_cv_mission(
        session: Session, consultant_id: int, mission_data: Dict
    ) -> bool:
        """Sauvegarde une mission individuelle du CV"""
        # Vérifier les doublons
        if ConsultantService._mission_exists_for_cv(
            session, consultant_id, mission_data
        ):
            return False

        # Convertir et valider les dates
        date_debut, date_fin = ConsultantService._parse_cv_mission_dates(mission_data)
        if not date_debut:
            return False

        # Créer et sauvegarder la mission
        new_mission = ConsultantService._create_cv_mission_object(
            consultant_id, mission_data, date_debut, date_fin
        )
        session.add(new_mission)
        st.success("✅ Mission ajoutée: " + mission_data["client"])
        return True

    @staticmethod
    def _mission_exists_for_cv(
        session: Session, consultant_id: int, mission_data: Dict
    ) -> bool:
        """Vérifie si une mission CV existe déjà"""
        existing_mission = (
            session.query(Mission)
            .filter(
                Mission.consultant_id == consultant_id,
                Mission.client == mission_data["client"],
                Mission.date_debut == mission_data.get("date_debut", ""),
            )
            .first()
        )
        return existing_mission is not None

    @staticmethod
    def _parse_cv_mission_dates(mission_data: Dict):
        """Parse les dates d'une mission CV"""
        date_debut = mission_data.get("date_debut")
        date_fin = mission_data.get("date_fin")

        try:
            if date_debut and date_debut != ConsultantService.STATUS_IN_PROGRESS:
                if len(date_debut) >= 10:  # Format YYYY-MM-DD
                    date_debut = datetime.strptime(date_debut[:10], "%Y-%m-%d").date()
                else:
                    return None, None  # Format invalide
            else:
                return None, None  # Pas de date de début

            if date_fin and date_fin != ConsultantService.STATUS_IN_PROGRESS:
                if len(date_fin) >= 10:  # Format YYYY-MM-DD
                    date_fin = datetime.strptime(date_fin[:10], "%Y-%m-%d").date()
                else:
                    date_fin = None
            else:
                date_fin = None

        except ValueError:
            st.warning(
                f"⚠️ Mission {mission_data['client']} ignorée - format de date invalide"
            )
            return None, None

        return date_debut, date_fin

    @staticmethod
    def _create_cv_mission_object(
        consultant_id: int, mission_data: Dict, date_debut, date_fin
    ) -> Mission:
        """Crée un objet Mission depuis les données CV"""
        return Mission(
            consultant_id=consultant_id,
            nom_mission=f"Mission chez {mission_data['client']}",
            client=mission_data["client"],
            role=mission_data.get("role", ""),
            description=mission_data.get("resume", ""),
            date_debut=date_debut,
            date_fin=date_fin,
            statut="en_cours" if date_fin is None else "terminee",
            technologies_utilisees=", ".join(
                mission_data.get("langages_techniques", [])
            ),
            revenus_generes=0,  # À compléter manuellement
        )

    @staticmethod
    def _save_cv_skills(
        session: Session, consultant_id: int, analysis_data: Dict
    ) -> int:
        """Sauvegarde les compétences extraites du CV"""
        skills_count = 0

        # Compétences techniques
        technical_skills = analysis_data.get("langages_techniques", [])
        skills_count += ConsultantService._save_skills_by_type(
            session, consultant_id, technical_skills, "technique"
        )

        # Compétences fonctionnelles
        functional_skills = analysis_data.get("competences_fonctionnelles", [])
        skills_count += ConsultantService._save_skills_by_type(
            session, consultant_id, functional_skills, "fonctionnelle"
        )

        return skills_count

    @staticmethod
    def _save_skills_by_type(
        session: Session, consultant_id: int, skills: list, skill_type: str
    ) -> int:
        """Sauvegarde un ensemble de compétences d'un type donné"""
        count = 0

        for skill_name in skills:
            if ConsultantService._should_save_skill(
                skill_name
            ) and ConsultantService._save_single_cv_skill(
                session, consultant_id, skill_name.strip(), skill_type
            ):
                count += 1

        return count

    @staticmethod
    def _should_save_skill(skill_name: str) -> bool:
        """Vérifie si une compétence doit être sauvegardée"""
        return skill_name and len(skill_name.strip()) >= 2

    @staticmethod
    def _save_single_cv_skill(
        session: Session, consultant_id: int, skill_name: str, skill_type: str
    ) -> bool:
        """Sauvegarde une compétence individuelle du CV"""
        # Récupérer ou créer la compétence dans le référentiel
        competence = ConsultantService._get_or_create_competence(
            session, skill_name, skill_type
        )

        # Vérifier si le consultant a déjà cette compétence
        if ConsultantService._consultant_has_skill(
            session, consultant_id, competence.id
        ):
            return False

        # Ajouter la compétence au consultant
        ConsultantService._add_skill_to_consultant(
            session, consultant_id, competence.id
        )
        st.success(f"✅ Compétence {skill_type} ajoutée: {skill_name}")
        return True

    @staticmethod
    def _get_or_create_competence(session: Session, skill_name: str, skill_type: str):
        """Récupère ou crée une compétence dans le référentiel"""
        competence = (
            session.query(Competence)
            .filter(Competence.nom.ilike(f"%{skill_name}%"))
            .first()
        )

        if not competence:
            competence = Competence(
                nom=skill_name,
                type_competence=skill_type,
                categorie=ConsultantService._determine_skill_category(
                    skill_name, skill_type
                ),
                description=f"Compétence {skill_type} extraite automatiquement du CV",
            )
            session.add(competence)
            session.flush()  # Pour obtenir l'ID

        return competence

    @staticmethod
    def _consultant_has_skill(
        session: Session, consultant_id: int, competence_id: int
    ) -> bool:
        """Vérifie si le consultant a déjà cette compétence"""
        existing_skill = (
            session.query(ConsultantCompetence)
            .filter(
                ConsultantCompetence.consultant_id == consultant_id,
                ConsultantCompetence.competence_id == competence_id,
            )
            .first()
        )
        return existing_skill is not None

    @staticmethod
    def _add_skill_to_consultant(
        session: Session, consultant_id: int, competence_id: int
    ):
        """Ajoute une compétence au consultant"""
        consultant_skill = ConsultantCompetence(
            consultant_id=consultant_id,
            competence_id=competence_id,
            niveau_maitrise="intermediaire",  # Par défaut
            annees_experience=2.0,  # Estimation par défaut
        )
        session.add(consultant_skill)

    @staticmethod
    def _finalize_cv_analysis_save(
        session: Session, consultant, missions_count: int, skills_count: int
    ):
        """Finalise la sauvegarde de l'analyse CV"""
        # Mettre à jour la date de dernière modification
        consultant.derniere_maj = datetime.now()

        # Committer toutes les modifications
        session.commit()

        st.success("🎉 Analyse CV sauvegardée avec succès !")
        st.info(
            f"📊 **Résumé**: {missions_count} missions ajoutées, {skills_count} compétences ajoutées"
        )
