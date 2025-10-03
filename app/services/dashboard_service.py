"""
Service de gestion des dashboards personnalisés
Gère la création, modification, suppression et récupération des dashboards
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from app.database.database import get_database_session
from app.database.models import DashboardConfiguration, DashboardWidgetInstance, WidgetCatalog
from app.database.models import BusinessManager, Consultant, Mission, ConsultantBusinessManager


class DashboardService:
    """
    Service principal pour la gestion des dashboards
    """

    @staticmethod
    def get_all_dashboards() -> List[Dict]:
        """
        Récupère tous les dashboards disponibles

        Returns:
            List[Dict]: Liste des dashboards avec leurs informations
        """
        try:
            with get_database_session() as session:
                dashboards = (
                    session.query(DashboardConfiguration)
                    .order_by(DashboardConfiguration.is_template.desc(), DashboardConfiguration.nom)
                    .all()
                )

                return [
                    {
                        "id": dashboard.id,
                        "nom": dashboard.nom,
                        "description": dashboard.description,
                        "role_access": dashboard.role_access,
                        "is_template": dashboard.is_template,
                        "is_public": dashboard.is_public,
                        "created_by": dashboard.created_by,
                        "date_creation": dashboard.date_creation,
                        "widget_count": len(dashboard.widget_instances),
                    }
                    for dashboard in dashboards
                ]
        except Exception as e:
            print(f"Erreur lors de la récupération des dashboards: {e}")
            return []

    @staticmethod
    def get_dashboard_by_id(dashboard_id: int) -> Optional[Dict]:
        """
        Récupère un dashboard spécifique par son ID

        Args:
            dashboard_id: ID du dashboard

        Returns:
            Dict: Configuration complète du dashboard ou None
        """
        try:
            with get_database_session() as session:
                dashboard = (
                    session.query(DashboardConfiguration).filter(DashboardConfiguration.id == dashboard_id).first()
                )

                if not dashboard:
                    return None

                return {
                    "id": dashboard.id,
                    "nom": dashboard.nom,
                    "description": dashboard.description,
                    "layout_config": dashboard.layout_config or {},
                    "filters_config": dashboard.filters_config or {},
                    "role_access": dashboard.role_access,
                    "is_template": dashboard.is_template,
                    "is_public": dashboard.is_public,
                    "created_by": dashboard.created_by,
                    "date_creation": dashboard.date_creation,
                    "widgets": [
                        {
                            "id": widget.id,
                            "widget_type": widget.widget_type,
                            "position_x": widget.position_x,
                            "position_y": widget.position_y,
                            "width": widget.width,
                            "height": widget.height,
                            "config": widget.config or {},
                        }
                        for widget in dashboard.widget_instances
                    ],
                }
        except Exception as e:
            print(f"Erreur lors de la récupération du dashboard {dashboard_id}: {e}")
            return None

    @staticmethod
    def create_dashboard(
        nom: str, description: str = "", role_access: str = "all", created_by: str = "system", is_template: bool = False
    ) -> Optional[int]:
        """
        Crée un nouveau dashboard

        Args:
            nom: Nom du dashboard
            description: Description optionnelle
            role_access: Rôle d'accès (bm, direction, responsable_bm, all)
            created_by: Créateur du dashboard
            is_template: Si c'est un template

        Returns:
            int: ID du dashboard créé ou None en cas d'erreur
        """
        try:
            with get_database_session() as session:
                new_dashboard = DashboardConfiguration(
                    nom=nom,
                    description=description,
                    role_access=role_access,
                    created_by=created_by,
                    is_template=is_template,
                    layout_config={},
                    filters_config={},
                )

                session.add(new_dashboard)
                session.commit()
                return new_dashboard.id

        except Exception as e:
            print(f"Erreur lors de la création du dashboard: {e}")
            return None

    @staticmethod
    def add_widget_to_dashboard(
        dashboard_id: int,
        widget_type: str,
        position_x: int = 0,
        position_y: int = 0,
        width: int = 1,
        height: int = 1,
        config: Dict = None,
    ) -> bool:
        """
        Ajoute un widget à un dashboard

        Args:
            dashboard_id: ID du dashboard
            widget_type: Type du widget
            position_x: Position X dans la grille
            position_y: Position Y dans la grille
            width: Largeur en colonnes
            height: Hauteur en lignes
            config: Configuration spécifique du widget

        Returns:
            bool: True si ajouté avec succès
        """
        try:
            with get_database_session() as session:
                widget_instance = DashboardWidgetInstance(
                    dashboard_id=dashboard_id,
                    widget_type=widget_type,
                    position_x=position_x,
                    position_y=position_y,
                    width=width,
                    height=height,
                    config=config or {},
                )

                session.add(widget_instance)
                session.commit()
                return True

        except Exception as e:
            print(f"Erreur lors de l'ajout du widget: {e}")
            return False

    @staticmethod
    def remove_widget_from_dashboard(widget_instance_id: int) -> bool:
        """
        Supprime un widget d'un dashboard

        Args:
            widget_instance_id: ID de l'instance de widget à supprimer

        Returns:
            bool: True si suppression réussie
        """
        try:
            with get_database_session() as session:
                # Trouver l'instance de widget
                widget_instance = (
                    session.query(DashboardWidgetInstance)
                    .filter(DashboardWidgetInstance.id == widget_instance_id)
                    .first()
                )

                if widget_instance:
                    session.delete(widget_instance)
                    session.commit()
                    return True

                return False

        except Exception as e:
            print(f"Erreur lors de la suppression du widget: {e}")
            return False

    @staticmethod
    def get_available_widgets() -> List[Dict]:
        """
        Récupère la liste des widgets disponibles depuis le catalogue

        Returns:
            List[Dict]: Liste des widgets disponibles
        """
        try:
            with get_database_session() as session:
                widgets = (
                    session.query(WidgetCatalog)
                    .filter(WidgetCatalog.is_active == True)
                    .order_by(WidgetCatalog.category, WidgetCatalog.display_name)
                    .all()
                )

                return [
                    {
                        "id": widget.id,
                        "name": widget.name,
                        "display_name": widget.display_name,
                        "category": widget.category,
                        "description": widget.description,
                        "icon": widget.icon,
                        "config_schema": widget.config_schema or {},
                        "render_function": widget.render_function,
                    }
                    for widget in widgets
                ]
        except Exception as e:
            print(f"Erreur lors de la récupération des widgets: {e}")
            return []

    @staticmethod
    def delete_dashboard(dashboard_id: int) -> bool:
        """
        Supprime un dashboard et tous ses widgets

        Args:
            dashboard_id: ID du dashboard à supprimer

        Returns:
            bool: True si supprimé avec succès
        """
        try:
            with get_database_session() as session:
                dashboard = (
                    session.query(DashboardConfiguration).filter(DashboardConfiguration.id == dashboard_id).first()
                )

                if dashboard:
                    session.delete(dashboard)
                    session.commit()
                    return True
                return False

        except Exception as e:
            print(f"Erreur lors de la suppression du dashboard: {e}")
            return False

    @staticmethod
    def update_dashboard_layout(dashboard_id: int, layout_config: Dict) -> bool:
        """
        Met à jour la configuration de layout d'un dashboard

        Args:
            dashboard_id: ID du dashboard
            layout_config: Nouvelle configuration de layout

        Returns:
            bool: True si mis à jour avec succès
        """
        try:
            with get_database_session() as session:
                dashboard = (
                    session.query(DashboardConfiguration).filter(DashboardConfiguration.id == dashboard_id).first()
                )

                if dashboard:
                    dashboard.layout_config = layout_config
                    dashboard.derniere_maj = datetime.now()
                    session.commit()
                    return True
                return False

        except Exception as e:
            print(f"Erreur lors de la mise à jour du layout: {e}")
            return False


class DashboardDataService:
    """
    Service pour récupérer les données métier utilisées par les widgets
    """

    @staticmethod
    def get_intercontrat_data(bm_filter: Optional[int] = None) -> Dict:
        """
        Calcule les données d'intercontrat

        Args:
            bm_filter: ID du BM pour filtrer (optionnel)

        Returns:
            Dict: Données d'intercontrat
        """
        try:
            with get_database_session() as session:
                # Requête de base pour les consultants actifs
                query_consultants = session.query(Consultant).filter(Consultant.actif == True)

                # Filtre par BM si spécifié
                if bm_filter:
                    consultant_ids_bm = (
                        session.query(ConsultantBusinessManager.consultant_id)
                        .filter(
                            and_(
                                ConsultantBusinessManager.business_manager_id == bm_filter,
                                ConsultantBusinessManager.date_fin.is_(None),
                            )
                        )
                        .subquery()
                    )
                    query_consultants = query_consultants.filter(Consultant.id.in_(consultant_ids_bm))

                total_consultants = query_consultants.count()

                # Consultants avec mission en cours
                consultants_avec_mission = query_consultants.filter(
                    Consultant.id.in_(session.query(Mission.consultant_id).filter(Mission.statut == "en_cours"))
                ).count()

                # Consultants sans mission (intercontrat)
                consultants_intercontrat = total_consultants - consultants_avec_mission
                taux_intercontrat = (consultants_intercontrat / total_consultants * 100) if total_consultants > 0 else 0

                # Liste détaillée des consultants en intercontrat
                consultants_sans_mission = query_consultants.filter(
                    ~Consultant.id.in_(session.query(Mission.consultant_id).filter(Mission.statut == "en_cours"))
                ).all()

                return {
                    "total_consultants": total_consultants,
                    "consultants_avec_mission": consultants_avec_mission,
                    "consultants_intercontrat": consultants_intercontrat,
                    "taux_intercontrat": round(taux_intercontrat, 1),
                    "consultants_sans_mission": [
                        {
                            "id": c.id,
                            "nom": f"{c.prenom} {c.nom}",
                            "email": c.email,
                            "derniere_mission": DashboardDataService._get_last_mission_date(c.id, session),
                        }
                        for c in consultants_sans_mission
                    ],
                }

        except Exception as e:
            print(f"Erreur lors du calcul des données d'intercontrat: {e}")
            return {
                "total_consultants": 0,
                "consultants_avec_mission": 0,
                "consultants_intercontrat": 0,
                "taux_intercontrat": 0,
                "consultants_sans_mission": [],
            }

    @staticmethod
    def get_revenue_by_bm_data(period_months: int = 3) -> Dict:
        """
        Calcule les données de revenus par Business Manager

        Args:
            period_months: Nombre de mois à analyser

        Returns:
            Dict: Données de revenus par BM
        """
        try:
            with get_database_session() as session:
                # Calcul de la date de début de période
                from dateutil.relativedelta import relativedelta

                date_debut = date.today() - relativedelta(months=period_months)

                # Revenus par BM
                # Calcul SQL de la durée : julianday(date_fin) - julianday(date_debut)
                # Si date_fin est NULL, on utilise 30 jours par défaut
                duree_sql = func.coalesce(func.julianday(Mission.date_fin) - func.julianday(Mission.date_debut), 30)

                revenue_query = (
                    session.query(
                        BusinessManager.id,
                        BusinessManager.prenom,
                        BusinessManager.nom,
                        func.count(Mission.id).label("missions_count"),
                        func.avg(Mission.tjm).label("tjm_moyen"),
                        func.sum(Mission.tjm * duree_sql).label("ca_estime"),
                    )
                    .outerjoin(
                        ConsultantBusinessManager,
                        and_(
                            BusinessManager.id == ConsultantBusinessManager.business_manager_id,
                            ConsultantBusinessManager.date_fin.is_(None),
                        ),
                    )
                    .outerjoin(
                        Mission,
                        and_(
                            ConsultantBusinessManager.consultant_id == Mission.consultant_id,
                            Mission.date_debut >= date_debut,
                            Mission.statut.in_(["en_cours", "termine"]),
                        ),
                    )
                    .filter(BusinessManager.actif == True)
                    .group_by(BusinessManager.id, BusinessManager.prenom, BusinessManager.nom)
                    .all()
                )

                return {
                    "period_months": period_months,
                    "date_debut": date_debut,
                    "bm_revenues": [
                        {
                            "bm_id": row.id,
                            "bm_name": f"{row.prenom} {row.nom}",
                            "missions_count": row.missions_count or 0,
                            "tjm_moyen": float(row.tjm_moyen or 0),
                            "ca_estime": float(row.ca_estime or 0),
                        }
                        for row in revenue_query
                    ],
                }

        except Exception as e:
            print(f"Erreur lors du calcul des revenus par BM: {e}")
            return {"period_months": period_months, "date_debut": date.today(), "bm_revenues": []}

    @staticmethod
    def _get_last_mission_date(consultant_id: int, session: Session) -> Optional[str]:
        """
        Récupère la date de fin de la dernière mission d'un consultant

        Args:
            consultant_id: ID du consultant
            session: Session SQLAlchemy

        Returns:
            str: Date de fin de dernière mission ou None
        """
        try:
            last_mission = (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant_id, Mission.statut == "termine")
                .order_by(desc(Mission.date_fin))
                .first()
            )

            if last_mission and last_mission.date_fin:
                return last_mission.date_fin.strftime("%d/%m/%Y")
            return None

        except Exception:
            return None
