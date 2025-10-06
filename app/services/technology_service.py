"""
Service de gestion des technologies personnalisées
"""

import os
import sys
from typing import List
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from database.database import get_database_session
from database.models import CustomTechnology
from utils.technologies_referentiel import TECHNOLOGIES_REFERENTIEL
from utils.technologies_referentiel import get_all_technologies

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TechnologyService:
    @staticmethod
    def get_all_available_technologies() -> List[str]:
        """Retourne toutes les technologies disponibles (référentiel + personnalisées)"""
        # Technologies du référentiel
        ref_technologies = get_all_technologies()

        # Technologies personnalisées en base
        try:
            with get_database_session() as session:
                custom_techs = session.query(CustomTechnology).all()
                custom_tech_names = [tech.nom for tech in custom_techs]

            # Fusion et tri
            all_technologies = set(ref_technologies + custom_tech_names)
            return sorted(all_technologies)

        except SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des technologies personnalisées: {e}")
            return ref_technologies

    @staticmethod
    def get_all_technologies() -> List[str]:
        """Alias de get_all_available_technologies pour compatibilité avec les tests"""
        return TechnologyService.get_all_available_technologies()

    @staticmethod
    def add_custom_technology(name: str, category: str = "Personnalisées") -> bool:
        """Ajoute une technologie personnalisée en base de données"""
        try:
            with get_database_session() as session:
                # Vérifier si elle existe déj?
                existing = session.query(CustomTechnology).filter(CustomTechnology.nom == name).first()

                if existing:
                    return False

                # Ajouter la nouvelle technologie
                new_tech = CustomTechnology(
                    nom=name,
                    categorie=category,
                    description=f"Technologie personnalisée: {name}",
                )

                session.add(new_tech)
                session.commit()
                return True

        except SQLAlchemyError as e:
            print(f"Erreur lors de l'ajout de la technologie: {e}")
            return False

    @staticmethod
    def get_custom_technologies() -> List[dict]:
        """Retourne la liste des technologies personnalisées"""
        try:
            with get_database_session() as session:
                custom_techs = session.query(CustomTechnology).all()

                return [
                    {
                        "id": tech.id,
                        "nom": tech.nom,
                        "categorie": tech.categorie,
                        "description": tech.description,
                    }
                    for tech in custom_techs
                ]

        except SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des technologies personnalisées: {e}")
            return []

    @staticmethod
    def delete_custom_technology(tech_id: int) -> bool:
        """Supprime une technologie personnalisée"""
        try:
            with get_database_session() as session:
                tech = session.query(CustomTechnology).filter(CustomTechnology.id == tech_id).first()

                if tech:
                    session.delete(tech)
                    session.commit()
                    return True
                return False

        except SQLAlchemyError as e:
            print(f"Erreur lors de la suppression de la technologie: {e}")
            return False

    @staticmethod
    def search_technologies(query: str) -> List[str]:
        """Recherche des technologies par nom"""
        all_techs = TechnologyService.get_all_available_technologies()
        query_lower = query.lower()
        return [tech for tech in all_techs if query_lower in tech.lower()]

    @staticmethod
    def get_technologies_by_category() -> dict:
        """Retourne les technologies organisées par catégorie"""
        # Référentiel de base
        technologies = TECHNOLOGIES_REFERENTIEL.copy()

        # Ajouter les technologies personnalisées
        custom_techs = TechnologyService.get_custom_technologies()
        for tech in custom_techs:
            category = tech["categorie"]
            if category not in technologies:
                technologies[category] = []
            technologies[category].append(tech["nom"])

        # Trier chaque catégorie
        for category in technologies:
            technologies[category] = sorted(technologies[category])

        return technologies
