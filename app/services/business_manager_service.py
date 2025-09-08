"""
Service de gestion des Business Managers
CRUD operations pour les Business Managers avec la base de données
"""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from database.database import get_database_session
from database.models import BusinessManager
from database.models import ConsultantBusinessManager


class BusinessManagerService:
    """Service pour la gestion des Business Managers"""

    @staticmethod
    @st.cache_data(ttl=300)  # Cache pendant 5 minutes
    def get_all_business_managers() -> List[Dict]:
        """Récupère tous les Business Managers"""
        try:
            with get_database_session() as session:
                business_managers = session.query(BusinessManager).all()

                # Convertir en dictionnaires pour éviter les erreurs de session
                bm_list = []
                for bm in business_managers:
                    # Compter les consultants assignés (actifs)
                    consultants_count = (
                        session.query(ConsultantBusinessManager)
                        .filter(
                            ConsultantBusinessManager.business_manager_id == bm.id,
                            ConsultantBusinessManager.date_fin.is_(None),
                        )
                        .count()
                    )

                    bm_list.append(
                        {
                            "id": bm.id,
                            "prenom": bm.prenom,
                            "nom": bm.nom,
                            "email": bm.email,
                            "telephone": bm.telephone,
                            "actif": bm.actif,
                            "consultants_count": consultants_count,
                            "date_creation": bm.date_creation,
                            "notes": bm.notes,
                        }
                    )

                return bm_list
        except Exception as e:
            print(f"Erreur lors de la récupération des Business Managers: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=120)  # Cache pendant 2 minutes pour la recherche
    def search_business_managers(search_term: str) -> List[Dict]:
        """Recherche des Business Managers par prénom, nom ou email"""
        try:
            with get_database_session() as session:
                query = session.query(BusinessManager)

                if search_term:
                    search_filter = f"%{search_term}%"
                    query = query.filter(
                        (BusinessManager.nom.ilike(search_filter))
                        | (BusinessManager.prenom.ilike(search_filter))
                        | (BusinessManager.email.ilike(search_filter))
                    )

                business_managers = query.all()

                # Convertir en dictionnaires
                bm_list = []
                for bm in business_managers:
                    # Compter les consultants assignés (actifs)
                    consultants_count = (
                        session.query(ConsultantBusinessManager)
                        .filter(
                            ConsultantBusinessManager.business_manager_id == bm.id,
                            ConsultantBusinessManager.date_fin.is_(None),
                        )
                        .count()
                    )

                    bm_list.append(
                        {
                            "id": bm.id,
                            "prenom": bm.prenom,
                            "nom": bm.nom,
                            "email": bm.email,
                            "telephone": bm.telephone,
                            "actif": bm.actif,
                            "consultants_count": consultants_count,
                            "date_creation": bm.date_creation,
                            "notes": bm.notes,
                        }
                    )

                return bm_list
        except Exception as e:
            print(f"Erreur lors de la recherche des Business Managers: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=600)  # Cache pendant 10 minutes
    def get_business_managers_count() -> int:
        """Retourne le nombre total de Business Managers avec cache"""
        try:
            with get_database_session() as session:
                return session.query(BusinessManager).count()
        except Exception as e:
            print(f"Erreur lors du comptage des Business Managers: {e}")
            return 0

    @staticmethod
    def get_business_manager_by_id(bm_id: int) -> Optional[BusinessManager]:
        """Récupère un Business Manager par son ID"""
        try:
            with get_database_session() as session:
                return (
                    session.query(BusinessManager)
                    .filter(BusinessManager.id == bm_id)
                    .first()
                )
        except Exception as e:
            print(f"Erreur lors de la récupération du Business Manager {bm_id}: {e}")
            return None
