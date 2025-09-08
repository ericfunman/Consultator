"""
Service pour la gestion des practices
"""

from typing import Dict
from typing import List
from typing import Optional

import streamlit as st
from sqlalchemy.orm import sessionmaker

from database.database import get_database_session
from database.models import Consultant
from database.models import Practice

get_session = get_database_session


class PracticeService:
    """Service pour gérer les practices"""

    @staticmethod
    def get_all_practices() -> List[Practice]:
        """Récupère toutes les practices actives"""
        session = get_session()
        try:
            return (
                session.query(Practice)
                .filter(Practice.actif)
                .order_by(Practice.nom)
                .all()
            )
        except Exception as e:
            st.error(f"Erreur lors de la récupération des practices: {e}")
            return []
        finally:
            session.close()

    @staticmethod
    def get_practice_by_id(practice_id: int) -> Optional[Practice]:
        """Récupère une practice par son ID"""
        session = get_session()
        try:
            return session.query(Practice).filter(Practice.id == practice_id).first()
        except Exception as e:
            st.error(f"Erreur lors de la récupération de la practice: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_practice_by_name(nom: str) -> Optional[Practice]:
        """Récupère une practice par son nom"""
        session = get_session()
        try:
            return session.query(Practice).filter(Practice.nom == nom).first()
        except Exception as e:
            st.error(f"Erreur lors de la récupération de la practice: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def create_practice(
        nom: str, description: str = "", responsable: str = ""
    ) -> Optional[Practice]:
        """Crée une nouvelle practice"""
        session = get_session()
        try:
            # Vérifier si la practice existe déjà
            existing = session.query(Practice).filter(Practice.nom == nom).first()
            if existing:
                st.error(f"La practice '{nom}' existe déjà")
                return None

            practice = Practice(
                nom=nom, description=description, responsable=responsable, actif=True
            )

            session.add(practice)
            session.commit()
            session.refresh(practice)

            st.success(f"Practice '{nom}' créée avec succès")
            return practice

        except Exception as e:
            st.error(f"Erreur lors de la création de la practice: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_practice(practice_id: int, **kwargs) -> bool:
        """Met à jour une practice"""
        session = get_session()
        try:
            practice = (
                session.query(Practice).filter(Practice.id == practice_id).first()
            )
            if not practice:
                st.error("Practice non trouvée")
                return False

            for key, value in kwargs.items():
                if hasattr(practice, key):
                    setattr(practice, key, value)

            session.commit()
            st.success("Practice mise à jour avec succès")
            return True

        except Exception as e:
            st.error(f"Erreur lors de la mise à jour de la practice: {e}")
            return False
        finally:
            session.close()

    @staticmethod
    def get_consultants_by_practice(
        practice_id: Optional[int] = None,
    ) -> Dict[str, List[Consultant]]:
        """Récupère les consultants groupés par practice"""
        from sqlalchemy.orm import joinedload

        session = get_session()
        try:
            if practice_id:
                # Consultants d'une practice spécifique
                consultants = (
                    session.query(Consultant)
                    .options(
                        joinedload(Consultant.missions),
                        joinedload(Consultant.competences),
                    )
                    .filter(Consultant.practice_id == practice_id)
                    .order_by(Consultant.nom, Consultant.prenom)
                    .all()
                )

                practice = (
                    session.query(Practice).filter(Practice.id == practice_id).first()
                )
                practice_name = practice.nom if practice else "Practice inconnue"

                # Détacher les objets de la session pour éviter les erreurs
                # DetachedInstance
                for consultant in consultants:
                    session.expunge(consultant)

                return {practice_name: consultants}
            else:
                # Tous les consultants groupés par practice
                practices = session.query(Practice).filter(Practice.actif).all()
                result = {}

                for practice in practices:
                    consultants = (
                        session.query(Consultant)
                        .options(
                            joinedload(Consultant.missions),
                            joinedload(Consultant.competences),
                        )
                        .filter(Consultant.practice_id == practice.id)
                        .order_by(Consultant.nom, Consultant.prenom)
                        .all()
                    )

                    # Détacher les objets de la session
                    for consultant in consultants:
                        session.expunge(consultant)

                    result[practice.nom] = consultants

                # Consultants sans practice
                consultants_sans_practice = (
                    session.query(Consultant)
                    .options(
                        joinedload(Consultant.missions),
                        joinedload(Consultant.competences),
                    )
                    .filter(Consultant.practice_id.is_(None))
                    .order_by(Consultant.nom, Consultant.prenom)
                    .all()
                )

                # Détacher les objets de la session
                for consultant in consultants_sans_practice:
                    session.expunge(consultant)

                if consultants_sans_practice:
                    result["Sans Practice"] = consultants_sans_practice

                return result
        except Exception as e:
            st.error(
                f"Erreur lors de la récupération des consultants par practice: {e}"
            )
            return {}
        finally:
            session.close()

    @staticmethod
    def assign_consultant_to_practice(
        consultant_id: int, practice_id: Optional[int]
    ) -> bool:
        """Assigne un consultant à une practice"""
        session = get_session()
        try:
            consultant = (
                session.query(Consultant).filter(Consultant.id == consultant_id).first()
            )
            if not consultant:
                st.error("Consultant non trouvé")
                return False

            if practice_id:
                practice = (
                    session.query(Practice).filter(Practice.id == practice_id).first()
                )
                if not practice:
                    st.error("Practice non trouvée")
                    return False

            consultant.practice_id = practice_id
            session.commit()

            if practice_id:
                st.success(f"Consultant assigné à la practice {practice.nom}")
            else:
                st.success("Consultant retiré de sa practice")

            return True
        except Exception as e:
            st.error(f"Erreur lors de l'assignation: {e}")
            return False
        finally:
            session.close()

    @staticmethod
    def get_practice_statistics() -> Dict:
        """Récupère les statistiques des practices"""
        session = get_session()
        try:
            practices = session.query(Practice).filter(Practice.actif).all()

            stats = {
                "total_practices": len(practices),
                "total_consultants": 0,
                "practices_detail": [],
            }

            for practice in practices:
                consultants_count = (
                    session.query(Consultant)
                    .filter(Consultant.practice_id == practice.id)
                    .count()
                )

                consultants_actifs = (
                    session.query(Consultant)
                    .filter(
                        Consultant.practice_id == practice.id, Consultant.disponibilite
                    )
                    .count()
                )

                stats["practices_detail"].append(
                    {
                        "nom": practice.nom,
                        "total_consultants": consultants_count,
                        "consultants_actifs": consultants_actifs,
                        "responsable": practice.responsable or "Non défini",
                    }
                )

                stats["total_consultants"] += consultants_count

            # Consultants sans practice
            sans_practice = (
                session.query(Consultant)
                .filter(Consultant.practice_id.is_(None))
                .count()
            )

            if sans_practice > 0:
                stats["practices_detail"].append(
                    {
                        "nom": "Sans Practice",
                        "total_consultants": sans_practice,
                        "consultants_actifs": session.query(Consultant)
                        .filter(
                            Consultant.practice_id.is_(None), Consultant.disponibilite
                        )
                        .count(),
                        "responsable": "-",
                    }
                )

                stats["total_consultants"] += sans_practice

            return stats
        except Exception as e:
            st.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {
                "total_practices": 0,
                "total_consultants": 0,
                "practices_detail": [],
            }
        finally:
            session.close()

    @staticmethod
    def init_default_practices():
        """Initialise les practices par défaut (Data et Quant)"""
        session = get_session()
        try:
            # Vérifier si les practices existent déjà
            existing_practices = session.query(Practice).all()

            if not existing_practices:
                # Créer les practices par défaut
                practices_default = [
                    {
                        "nom": "Data",
                        "description": "Practice spécialisée dans les données, analytics, BI et data science",
                        "responsable": "",
                    },
                    {
                        "nom": "Quant",
                        "description": "Practice spécialisée dans l'analyse quantitative et le risk management",
                        "responsable": "",
                    },
                ]

                for practice_data in practices_default:
                    practice = Practice(**practice_data)
                    session.add(practice)

                session.commit()
                st.success("Practices par défaut initialisées : Data et Quant")
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation des practices: {e}")
        finally:
            session.close()
