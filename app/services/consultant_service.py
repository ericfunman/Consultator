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

from database.database import get_database_session
from database.models import Competence
from database.models import Consultant
from database.models import ConsultantCompetence
from database.models import Mission
from database.models import Practice


class ConsultantService:
    """Service pour la gestion des consultants optimisÃ© pour de gros volumes"""

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
    def search_consultants_optimized(
        search_term: str,
        page: int = 1,
        per_page: int = 50,
        practice_filter: Optional[str] = None,
        grade_filter: Optional[str] = None,
        availability_filter: Optional[bool] = None,
    ) -> List[Dict]:
        """Recherche optimisÃ©e avec cache pour de gros volumes - avec statistiques intÃ©grÃ©es"""
        try:
            with get_database_session() as session:
                # RequÃªte optimisÃ©e avec JOIN pour Ã©viter les requÃªtes N+1
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

                # Appliquer les filtres
                if practice_filter:
                    query = query.filter(Practice.nom == practice_filter)

                if grade_filter:
                    query = query.filter(Consultant.grade == grade_filter)

                if availability_filter is not None:
                    query = query.filter(
                        Consultant.disponibilite == availability_filter
                    )

                if search_term:
                    search_filter = f"%{search_term}%"
                    query = query.filter(
                        (Consultant.nom.ilike(search_filter))
                        | (Consultant.prenom.ilike(search_filter))
                        | (Consultant.email.ilike(search_filter))
                        | (Consultant.societe.ilike(search_filter))
                    )

                query = (
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

                results = query.all()

                # Convertir en dictionnaires avec calculs optimisÃ©s
                consultant_list = []
                for row in results:
                    salaire = row.salaire_actuel or 0
                    cjm = (salaire * 1.8 / 216) if salaire else 0

                    # Calcul de l'expÃ©rience
                    experience_annees = 0
                    if row.date_premiere_mission:
                        from datetime import date

                        today = date.today()
                        delta = today - row.date_premiere_mission
                        experience_annees = round(delta.days / 365.25, 1)

                    consultant_dict = {
                        "id": row.id,
                        "prenom": row.prenom,
                        "nom": row.nom,
                        "email": row.email,
                        "telephone": row.telephone,
                        "salaire_actuel": salaire,
                        "disponibilite": row.disponibilite,
                        "grade": row.grade or "Junior",
                        "type_contrat": row.type_contrat or "CDI",
                        "practice_name": row.practice_name or "Non affectÃ©",
                        "date_creation": row.date_creation,
                        "nb_missions": row.nb_missions,
                        "cjm": cjm,
                        "salaire_formatted": f"{salaire:,}â¬",
                        "cjm_formatted": f"{cjm:,.0f}â¬",
                        "statut": "â Disponible" if row.disponibilite else "ð´ OccupÃ©",
                        # Nouveaux champs V1.2
                        "societe": row.societe or "Quanteam",
                        "experience_annees": experience_annees,
                        "experience_formatted": (
                            f"{experience_annees} ans"
                            if experience_annees > 0
                            else "N/A"
                        ),
                    }
                    consultant_list.append(consultant_dict)

                return consultant_list
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la recherche optimisÃ©e: {e}")
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
    def get_all_consultants_with_stats(
        page: int = 1,
        per_page: int = 50,
        practice_filter: Optional[str] = None,
        grade_filter: Optional[str] = None,
        availability_filter: Optional[bool] = None,
    ) -> List[Dict]:
        """
        RÃ©cupÃ¨re tous les consultants avec leurs statistiques en une seule requÃªte optimisÃ©e
        RÃ©sout le problÃ¨me N+1 des requÃªtes pour compter les missions
        """
        try:
            with get_database_session() as session:
                # Une seule requÃªte avec LEFT JOIN pour rÃ©cupÃ©rer consultants + nombre
                # de missions
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

                # Appliquer les filtres
                if practice_filter:
                    query = query.filter(Practice.nom == practice_filter)

                if grade_filter:
                    query = query.filter(Consultant.grade == grade_filter)

                if availability_filter is not None:
                    query = query.filter(
                        Consultant.disponibilite == availability_filter
                    )

                query = (
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

                results = query.all()

                # Convertir en dictionnaires avec calculs optimisÃ©s
                consultant_list = []
                for row in results:
                    salaire = row.salaire_actuel or 0
                    cjm = (salaire * 1.8 / 216) if salaire else 0

                    # Calcul de l'expÃ©rience
                    experience_annees = 0
                    if row.date_premiere_mission:
                        from datetime import date

                        today = date.today()
                        delta = today - row.date_premiere_mission
                        experience_annees = round(delta.days / 365.25, 1)

                    consultant_dict = {
                        "id": row.id,
                        "prenom": row.prenom,
                        "nom": row.nom,
                        "email": row.email,
                        "telephone": row.telephone,
                        "salaire_actuel": salaire,
                        "disponibilite": row.disponibilite,
                        "practice_name": row.practice_name or "Non affectÃ©",
                        "date_creation": row.date_creation,
                        "derniere_maj": row.derniere_maj,
                        "nb_missions": row.nb_missions,
                        "cjm": cjm,
                        "salaire_formatted": f"{salaire:,}â¬",
                        "cjm_formatted": f"{cjm:,.0f}â¬",
                        "statut": "â Disponible" if row.disponibilite else "ð´ OccupÃ©",
                        # Nouveaux champs V1.2
                        "societe": row.societe or "Quanteam",
                        "experience_annees": experience_annees,
                        "experience_formatted": (
                            f"{experience_annees} ans"
                            if experience_annees > 0
                            else "N/A"
                        ),
                        # Nouveaux champs V1.2.1
                        "grade": row.grade or "Junior",
                        "type_contrat": row.type_contrat or "CDI",
                    }
                    consultant_list.append(consultant_dict)

                return consultant_list
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la rÃ©cupÃ©ration optimisÃ©e des consultants: {e}")
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
            print(f"Erreur lors de la rÃ©cupÃ©ration du consultant {consultant_id}: {e}")
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
            print(
                f"â Erreur lors de la suppression du consultant {consultant_id}: {e}"
            )
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
        Sauvegarde une mission extraite de l'analyse CV (mÃ©thode privÃ©e)

        Args:
            session: Session de base de donnÃ©es active
            consultant_id: ID du consultant propriÃ©taire de la mission
            mission_data: Dictionnaire contenant les donnÃ©es de la mission

        Returns:
            bool: True si la mission a Ã©tÃ© sauvegardÃ©e, False sinon

        Note:
            Cette mÃ©thode vÃ©rifie les doublons et gÃ¨re les conversions de dates
        """
        try:
            client = mission_data.get("client", "").strip()
            if not client:
                return False

            # VÃ©rifier si cette mission existe dÃ©jÃ  (mÃªme client + mÃªme annÃ©e)
            date_debut_str = mission_data.get("date_debut", "")
            if date_debut_str and date_debut_str != "En cours":
                try:
                    if len(date_debut_str) == 4:  # AnnÃ©e seulement
                        date_debut = date(int(date_debut_str), 1, 1)
                    else:
                        date_debut = datetime.strptime(
                            date_debut_str, "%Y-%m-%d"
                        ).date()
                except BaseException:
                    date_debut = None
            else:
                date_debut = None

            # VÃ©rifier doublons
            if date_debut:
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
                    print(f"Mission {client} {date_debut} dÃ©jÃ  existante, ignorÃ©e")
                    return False

            # Date de fin
            date_fin_str = mission_data.get("date_fin", "")
            date_fin = None
            if date_fin_str and date_fin_str != "En cours":
                try:
                    if len(date_fin_str) == 4:  # AnnÃ©e seulement
                        date_fin = date(int(date_fin_str), 12, 31)
                    else:
                        date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()
                except BaseException:
                    date_fin = None

            # CrÃ©er la mission
            mission = Mission(
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

            session.add(mission)
            return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur sauvegarde mission {mission_data.get('client', 'N/A')}: {e}")
            return False

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
        DÃ©termine automatiquement la catÃ©gorie d'une compÃ©tence (mÃ©thode privÃ©e)

        Args:
            skill_name: Nom de la compÃ©tence Ã  classifier
            type_competence: Type de compÃ©tence ("technique" ou "fonctionnelle")

        Returns:
            str: CatÃ©gorie de la compÃ©tence (ex: "Frontend", "Backend", "Management", etc.)

        Example:
            >>> category = ConsultantService._determine_skill_category("React", "technique")
            >>> print(category)  # Output: "Frontend"
        """
        skill_lower = skill_name.lower()

        if type_competence == "fonctionnelle":
            if any(
                word in skill_lower
                for word in ["management", "leadership", "gestion", "direction"]
            ):
                return "Management"
            elif any(
                word in skill_lower for word in ["scrum", "agile", "kanban", "projet"]
            ):
                return "Methodologie"
            elif any(
                word in skill_lower
                for word in ["formation", "conseil", "accompagnement"]
            ):
                return "Conseil"
            else:
                return "Fonctionnelle"

        # CompÃ©tences techniques
        frontend_keywords = [
            "react",
            "angular",
            "vue",
            "javascript",
            "typescript",
            "html",
            "css",
        ]
        backend_keywords = [
            "java",
            "python",
            "spring",
            "django",
            "flask",
            "node.js",
            "express",
        ]
        database_keywords = ["sql", "mysql", "postgresql", "mongodb", "oracle", "redis"]
        cloud_keywords = ["aws", "azure", "gcp", "docker", "kubernetes", "cloud"]
        devops_keywords = [
            "jenkins",
            "gitlab",
            "github",
            "ci/cd",
            "terraform",
            "ansible",
        ]

        if any(keyword in skill_lower for keyword in frontend_keywords):
            return "Frontend"
        elif any(keyword in skill_lower for keyword in backend_keywords):
            return "Backend"
        elif any(keyword in skill_lower for keyword in database_keywords):
            return "Database"
        elif any(keyword in skill_lower for keyword in cloud_keywords):
            return "Cloud"
        elif any(keyword in skill_lower for keyword in devops_keywords):
            return "DevOps"
        else:
            return "Technique"

    @staticmethod
    def save_cv_analysis(consultant_id: int, analysis_data: Dict[str, Any]) -> bool:
        """
        Sauvegarde les rÃ©sultats d'analyse de CV dans le profil du consultant

        Args:
            consultant_id: ID du consultant
            analysis_data: Dictionnaire contenant les donnÃ©es d'analyse (missions, compÃ©tences, etc.)

        Returns:
            bool: True si succÃ¨s, False sinon
        """
        try:
            with get_database_session() as session:
                # VÃ©rifier que le consultant existe
                consultant = (
                    session.query(Consultant)
                    .filter(Consultant.id == consultant_id)
                    .first()
                )
                if not consultant:
                    st.error(f"â Consultant avec ID {consultant_id} introuvable")
                    return False

                st.info(
                    f"ð¾ Sauvegarde de l'analyse CV pour {consultant.prenom} {consultant.nom}"
                )

                missions_count = 0
                skills_count = 0

                # 1. Sauvegarder les missions
                missions = analysis_data.get("missions", [])
                for mission_data in missions:
                    if not mission_data.get("client"):
                        continue

                    # Ignorer les missions sans dates valides
                    if (
                        not mission_data.get("date_debut")
                        or mission_data.get("date_debut") == ""
                    ):
                        st.warning(
                            f"â ï¸ Mission {mission_data['client']} ignorÃ©e - dates manquantes"
                        )
                        continue

                    # VÃ©rifier si la mission existe dÃ©jÃ  (Ã©viter les doublons)
                    existing_mission = (
                        session.query(Mission)
                        .filter(
                            Mission.consultant_id == consultant_id,
                            Mission.client == mission_data["client"],
                            Mission.date_debut == mission_data.get("date_debut", ""),
                        )
                        .first()
                    )

                    if not existing_mission:
                        # Convertir les dates si nÃ©cessaire
                        date_debut = mission_data.get("date_debut")
                        date_fin = mission_data.get("date_fin")

                        # Conversion des dates string vers date objects
                        try:
                            if date_debut and date_debut != "En cours":
                                if len(date_debut) >= 10:  # Format YYYY-MM-DD
                                    date_debut = datetime.strptime(
                                        date_debut[:10], "%Y-%m-%d"
                                    ).date()
                                else:
                                    continue  # Ignorer si format de date invalide
                            else:
                                continue  # Ignorer si pas de date de dÃ©but

                            if date_fin and date_fin != "En cours":
                                if len(date_fin) >= 10:  # Format YYYY-MM-DD
                                    date_fin = datetime.strptime(
                                        date_fin[:10], "%Y-%m-%d"
                                    ).date()
                                else:
                                    date_fin = None
                            else:
                                date_fin = None
                        except ValueError:
                            st.warning(
                                f"â ï¸ Mission {mission_data['client']} ignorÃ©e - format de date invalide"
                            )
                            continue

                        # CrÃ©er la nouvelle mission
                        new_mission = Mission(
                            consultant_id=consultant_id,
                            nom_mission=f"Mission chez {mission_data['client']}",
                            client=mission_data["client"],
                            role=mission_data.get("role", ""),  # Nouveau champ role
                            description=mission_data.get("resume", ""),
                            date_debut=date_debut,
                            date_fin=date_fin,
                            statut="en_cours" if date_fin is None else "terminee",
                            technologies_utilisees=", ".join(
                                mission_data.get("langages_techniques", [])
                            ),
                            revenus_generes=0,  # Ã complÃ©ter manuellement
                        )

                        session.add(new_mission)
                        missions_count += 1
                        st.success("â Mission ajoutÃ©e: " + mission_data["client"])

                # 2. Sauvegarder les compÃ©tences techniques
                technical_skills = analysis_data.get("langages_techniques", [])
                for skill_name in technical_skills:
                    if not skill_name or len(skill_name.strip()) < 2:
                        continue

                    skill_name = skill_name.strip()

                    # VÃ©rifier si la compÃ©tence existe dÃ©jÃ  dans le rÃ©fÃ©rentiel
                    competence = (
                        session.query(Competence)
                        .filter(Competence.nom.ilike(f"%{skill_name}%"))
                        .first()
                    )

                    if not competence:
                        # CrÃ©er la compÃ©tence dans le rÃ©fÃ©rentiel
                        competence = Competence(
                            nom=skill_name,
                            type_competence="technique",
                            categorie=ConsultantService._determine_skill_category(
                                skill_name, "technique"
                            ),
                            description="CompÃ©tence technique extraite automatiquement du CV",
                        )
                        session.add(competence)
                        session.flush()  # Pour obtenir l'ID

                    # VÃ©rifier si le consultant a dÃ©jÃ  cette compÃ©tence
                    existing_skill = (
                        session.query(ConsultantCompetence)
                        .filter(
                            ConsultantCompetence.consultant_id == consultant_id,
                            ConsultantCompetence.competence_id == competence.id,
                        )
                        .first()
                    )

                    if not existing_skill:
                        # Ajouter la compÃ©tence au consultant
                        consultant_skill = ConsultantCompetence(
                            consultant_id=consultant_id,
                            competence_id=competence.id,
                            niveau_maitrise="intermediaire",  # Par dÃ©faut
                            annees_experience=2.0,  # Estimation par dÃ©faut
                        )
                        session.add(consultant_skill)
                        skills_count += 1
                        st.success("â CompÃ©tence technique ajoutÃ©e: " + skill_name)

                # 3. Sauvegarder les compÃ©tences fonctionnelles
                functional_skills = analysis_data.get("competences_fonctionnelles", [])
                for skill_name in functional_skills:
                    if not skill_name or len(skill_name.strip()) < 2:
                        continue

                    skill_name = skill_name.strip()

                    # VÃ©rifier si la compÃ©tence existe dÃ©jÃ  dans le rÃ©fÃ©rentiel
                    competence = (
                        session.query(Competence)
                        .filter(Competence.nom.ilike(f"%{skill_name}%"))
                        .first()
                    )

                    if not competence:
                        # CrÃ©er la compÃ©tence dans le rÃ©fÃ©rentiel
                        competence = Competence(
                            nom=skill_name,
                            type_competence="fonctionnelle",
                            categorie=ConsultantService._determine_skill_category(
                                skill_name, "fonctionnelle"
                            ),
                            description="CompÃ©tence fonctionnelle extraite automatiquement du CV",
                        )
                        session.add(competence)
                        session.flush()  # Pour obtenir l'ID

                    # VÃ©rifier si le consultant a dÃ©jÃ  cette compÃ©tence
                    existing_skill = (
                        session.query(ConsultantCompetence)
                        .filter(
                            ConsultantCompetence.consultant_id == consultant_id,
                            ConsultantCompetence.competence_id == competence.id,
                        )
                        .first()
                    )

                    if not existing_skill:
                        # Ajouter la compÃ©tence au consultant
                        consultant_skill = ConsultantCompetence(
                            consultant_id=consultant_id,
                            competence_id=competence.id,
                            niveau_maitrise="intermediaire",  # Par dÃ©faut
                            annees_experience=2.0,  # Estimation par dÃ©faut
                        )
                        session.add(consultant_skill)
                        skills_count += 1
                        st.success("â CompÃ©tence fonctionnelle ajoutÃ©e: " + skill_name)

                # 4. Mettre Ã  jour la date de derniÃ¨re modification du consultant
                consultant.derniere_maj = datetime.now()

                # Committer toutes les modifications
                session.commit()

                st.success("ð Analyse CV sauvegardÃ©e avec succÃ¨s !")
                st.info(
                    f"ð **RÃ©sumÃ©**: {missions_count} missions ajoutÃ©es, {skills_count} compÃ©tences ajoutÃ©es"
                )

                return True

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            st.error("â Erreur lors de la sauvegarde de l'analyse CV: " + str(e))
            print(f"Erreur dÃ©taillÃ©e: {e}")
            import traceback

            traceback.print_exc()
            return False
