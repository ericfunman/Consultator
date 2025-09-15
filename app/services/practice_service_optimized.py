"""
Service optimisé pour la gestion des practices
Version haute performance avec cache et requêtes optimisées
"""

import time
from functools import lru_cache
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import streamlit as st
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import sessionmaker

from database.database import get_database_session
from database.models import Competence
from database.models import Consultant
from database.models import Mission
from database.models import Practice


class PracticeServiceOptimized:
    """Service optimisé pour gérer les practices avec cache et requêtes optimisées"""

    @staticmethod
    @st.cache_data(ttl=300)  # Cache 5 minutes
    def get_all_practices_cached() -> List[Dict]:
        """Récupère toutes les practices actives avec cache"""
        session = get_database_session()
        try:
            practices = (
                session.query(Practice)
                .filter(Practice.actif)
                .order_by(Practice.nom)
                .all()
            )

            # Convertir en dict pour le cache
            return [
                {
                    "id": p.id,
                    "nom": p.nom,
                    "description": p.description,
                    "responsable": p.responsable,
                    "actif": p.actif,
                }
                for p in practices
            ]
        except (SQLAlchemyError, OSError, ValueError, TypeError, AttributeError) as e:
            st.error(f"Erreur lors de la récupération des practices: {e}")
            return []
        finally:
            session.close()

    @staticmethod
    @st.cache_data(ttl=300)  # Cache 5 minutes
    def get_practice_statistics_optimized() -> Dict:
        """Récupère les statistiques des practices avec une seule requête optimisée"""
        session = get_database_session()
        try:
            # Requête SQL optimisée avec GROUP BY au lieu de N requêtes
            query = text(
                """
                SELECT
                    COALESCE(p.nom, 'Sans Practice') as practice_nom,
                    COALESCE(p.responsable, 'Non défini') as responsable,
                    COUNT(c.id) as total_consultants,
                    SUM(CASE WHEN c.disponibilite = 1 THEN 1 ELSE 0 END) as consultants_actifs
                FROM consultants c
                LEFT JOIN practices p ON c.practice_id = p.id
                WHERE p.actif = 1 OR p.actif IS NULL
                GROUP BY p.id, p.nom, p.responsable
                ORDER BY practice_nom
            """
            )

            result = session.execute(query).fetchall()

            stats = {
                "total_practices": 0,
                "total_consultants": 0,
                "practices_detail": [],
            }

            for row in result:
                practice_detail = {
                    "nom": row.practice_nom,
                    "total_consultants": row.total_consultants,
                    "consultants_actifs": row.consultants_actifs,
                    "responsable": row.responsable,
                }
                stats["practices_detail"].append(practice_detail)
                stats["total_consultants"] += row.total_consultants

                if row.practice_nom != "Sans Practice":
                    stats["total_practices"] += 1

            return stats
        except (SQLAlchemyError, OSError, ValueError, TypeError, AttributeError) as e:
            st.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {
                "total_practices": 0,
                "total_consultants": 0,
                "practices_detail": [],
            }
        finally:
            session.close()

    @staticmethod
    @st.cache_data(ttl=180)  # Cache 3 minutes
    def get_consultants_by_practice_optimized() -> Dict[str, List[Dict]]:
        """Récupère les consultants groupés par practice avec requête optimisée"""
        session = get_database_session()
        try:
            # Requête unique optimisée avec sous-requêtes pour les comptes
            query = text(
                """
                SELECT
                    c.id,
                    c.nom,
                    c.prenom,
                    c.email,
                    c.telephone,
                    c.salaire_actuel,
                    c.disponibilite,
                    COALESCE(p.nom, 'Sans Practice') as practice_nom,
                    COALESCE(mission_count.count, 0) as nb_missions,
                    COALESCE(comp_count.count, 0) as nb_competences
                FROM consultants c
                LEFT JOIN practices p ON c.practice_id = p.id
                LEFT JOIN (
                    SELECT consultant_id, COUNT(*) as count
                    FROM missions
                    GROUP BY consultant_id
                ) mission_count ON c.id = mission_count.consultant_id
                LEFT JOIN (
                    SELECT consultant_id, COUNT(*) as count
                    FROM consultant_competences
                    GROUP BY consultant_id
                ) comp_count ON c.id = comp_count.consultant_id
                WHERE p.actif = 1 OR p.actif IS NULL
                ORDER BY practice_nom, c.nom, c.prenom
            """
            )

            result = session.execute(query).fetchall()

            consultants_by_practice = {}

            for row in result:
                practice_nom = row.practice_nom

                consultant_data = {
                    "id": row.id,
                    "nom_complet": f"{row.prenom} {row.nom}",
                    "email": row.email,
                    "telephone": row.telephone or "Non renseigné",
                    "salaire_actuel": row.salaire_actuel,
                    "disponibilite": bool(row.disponibilite),
                    "nb_missions": row.nb_missions,
                    "nb_competences": row.nb_competences,
                }

                if practice_nom not in consultants_by_practice:
                    consultants_by_practice[practice_nom] = []

                consultants_by_practice[practice_nom].append(consultant_data)

            return consultants_by_practice
        except (SQLAlchemyError, OSError, ValueError, TypeError, AttributeError) as e:
            st.error(f"Erreur lors de la récupération des consultants: {e}")
            return {}
        finally:
            session.close()

    @staticmethod
    def get_consultants_by_practice_paginated(
        practice_name: str = None, page: int = 1, per_page: int = 50
    ) -> Tuple[List[Dict], int]:
        """Récupère les consultants avec pagination pour éviter de charger tous d'un coup"""
        session = get_database_session()
        try:
            offset = (page - 1) * per_page

            # Requête de base
            base_query = """
                SELECT
                    c.id,
                    c.nom,
                    c.prenom,
                    c.email,
                    c.telephone,
                    c.salaire_actuel,
                    c.disponibilite,
                    COALESCE(p.nom, 'Sans Practice') as practice_nom,
                    COALESCE(mission_count.count, 0) as nb_missions,
                    COALESCE(comp_count.count, 0) as nb_competences
                FROM consultants c
                LEFT JOIN practices p ON c.practice_id = p.id
                LEFT JOIN (
                    SELECT consultant_id, COUNT(*) as count
                    FROM missions
                    GROUP BY consultant_id
                ) mission_count ON c.id = mission_count.consultant_id
                LEFT JOIN (
                    SELECT consultant_id, COUNT(*) as count
                    FROM consultant_competences
                    GROUP BY consultant_id
                ) comp_count ON c.id = comp_count.consultant_id
                WHERE (p.actif = 1 OR p.actif IS NULL)
            """

            # Ajouter filtre si practice spécifique
            if practice_name and practice_name != "Toutes":
                if practice_name == "Sans Practice":
                    base_query += " AND p.nom IS NULL"
                else:
                    base_query += f" AND p.nom = '{practice_name}'"

            # Pagination
            query = text(
                base_query
                + f" ORDER BY practice_nom, c.nom, c.prenom LIMIT {per_page} OFFSET {offset}"
            )

            # Compter le total
            count_query = text(
                base_query.replace(
                    "SELECT c.id,c.nom,c.prenom,c.email,c.telephone,c.salaire_actuel,c.disponibilite,COALESCE(p.nom, 'Sans Practice') as practice_nom,COALESCE(mission_count.count, 0) as nb_missions,COALESCE(comp_count.count, 0) as nb_competences",
                    "SELECT COUNT(DISTINCT c.id)",
                )
            )

            result = session.execute(query).fetchall()
            total = session.execute(count_query).scalar()

            consultants = []
            for row in result:
                consultant_data = {
                    "id": row.id,
                    "nom_complet": f"{row.prenom} {row.nom}",
                    "email": row.email,
                    "telephone": row.telephone or "Non renseigné",
                    "salaire_actuel": row.salaire_actuel,
                    "disponibilite": bool(row.disponibilite),
                    "nb_missions": row.nb_missions,
                    "nb_competences": row.nb_competences,
                    "practice_nom": row.practice_nom,
                }
                consultants.append(consultant_data)

            return consultants, total
        except (SQLAlchemyError, OSError, ValueError, TypeError, AttributeError) as e:
            st.error(f"Erreur lors de la récupération paginée: {e}")
            return [], 0
        finally:
            session.close()

    @staticmethod
    @st.cache_data(ttl=600)  # Cache 10 minutes
    def get_practice_detailed_stats_cached(practice_name: str) -> Dict:
        """Statistiques détaillées d'une practice avec cache"""
        session = get_database_session()
        try:
            # Requête optimisée pour les stats détaillées
            query = text(
                """
                SELECT
                    COUNT(*) as total_consultants,
                    SUM(CASE WHEN c.disponibilite = 1 THEN 1 ELSE 0 END) as disponibles,
                    COALESCE(AVG(CASE WHEN c.salaire_actuel > 0 THEN c.salaire_actuel END), 0) as salaire_moyen,
                    COALESCE(SUM(mission_count.count), 0) as total_missions,
                    COALESCE(SUM(comp_count.count), 0) as total_competences
                FROM consultants c
                LEFT JOIN practices p ON c.practice_id = p.id
                LEFT JOIN (
                    SELECT consultant_id, COUNT(*) as count
                    FROM missions
                    GROUP BY consultant_id
                ) mission_count ON c.id = mission_count.consultant_id
                LEFT JOIN (
                    SELECT consultant_id, COUNT(*) as count
                    FROM consultant_competences
                    GROUP BY consultant_id
                ) comp_count ON c.id = comp_count.consultant_id
                WHERE COALESCE(p.nom, 'Sans Practice') = :practice_name
            """
            )

            result = session.execute(query, {"practice_name": practice_name}).fetchone()

            return {
                "total_consultants": result.total_consultants or 0,
                "disponibles": result.disponibles or 0,
                "salaire_moyen": float(result.salaire_moyen or 0),
                "total_missions": result.total_missions or 0,
                "total_competences": result.total_competences or 0,
            }
        except (SQLAlchemyError, OSError, ValueError, TypeError, AttributeError) as e:
            st.error(f"Erreur lors du calcul des stats détaillées: {e}")
            return {}
        finally:
            session.close()

    @staticmethod
    def clear_practices_cache():
        """Efface le cache des practices (à appeler après modifications)"""
        try:
            # Effacer les caches Streamlit
            st.cache_data.clear()
            st.success("🔄 Cache effacé - données mises à jour")
        except (OSError, ValueError, TypeError, AttributeError) as e:
            st.warning(f"Impossible d'effacer le cache: {e}")
