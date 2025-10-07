#!/usr/bin/env python3
"""
Tests complets pour app/services/dashboard_service.py
Phase 1: Dashboard Core - Amélioration couverture 62% → 64.5%
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, date
import pandas as pd

from app.services.dashboard_service import DashboardService, DashboardDataService


class TestDashboardService(unittest.TestCase):
    """Tests pour la classe DashboardService"""

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_all_dashboards_success(self, mock_get_session):
        """Test récupération de tous les dashboards"""
        # Mock session et dashboards
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_dashboard1 = Mock()
        mock_dashboard1.id = 1
        mock_dashboard1.nom = "Dashboard 1"
        mock_dashboard1.description = "Description 1"
        mock_dashboard1.role_access = "admin"
        mock_dashboard1.is_template = True
        mock_dashboard1.is_public = True
        mock_dashboard1.created_by = "user1"
        mock_dashboard1.date_creation = datetime.now()
        mock_dashboard1.widget_instances = [Mock(), Mock()]
        
        mock_dashboard2 = Mock()
        mock_dashboard2.id = 2
        mock_dashboard2.nom = "Dashboard 2"
        mock_dashboard2.description = "Description 2"
        mock_dashboard2.role_access = "user"
        mock_dashboard2.is_template = False
        mock_dashboard2.is_public = False
        mock_dashboard2.created_by = "user2"
        mock_dashboard2.date_creation = datetime.now()
        mock_dashboard2.widget_instances = [Mock()]
        
        mock_session.query.return_value.order_by.return_value.all.return_value = [
            mock_dashboard1, mock_dashboard2
        ]
        
        result = DashboardService.get_all_dashboards()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['nom'], "Dashboard 1")
        self.assertEqual(result[0]['widget_count'], 2)
        self.assertEqual(result[1]['widget_count'], 1)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_all_dashboards_empty(self, mock_get_session):
        """Test récupération dashboards - liste vide"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.order_by.return_value.all.return_value = []
        
        result = DashboardService.get_all_dashboards()
        
        self.assertEqual(result, [])

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_all_dashboards_exception(self, mock_get_session):
        """Test récupération dashboards avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.get_all_dashboards()
        
        self.assertEqual(result, [])

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_dashboard_by_id_success(self, mock_get_session):
        """Test récupération dashboard par ID - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_dashboard = Mock()
        mock_dashboard.id = 1
        mock_dashboard.nom = "Test Dashboard"
        mock_dashboard.description = "Test Description"
        mock_dashboard.layout_config = {"cols": 2}
        mock_dashboard.filters_config = {"date_range": "month"}
        mock_dashboard.role_access = "admin"
        mock_dashboard.is_template = False
        mock_dashboard.is_public = True
        mock_dashboard.created_by = "test_user"
        mock_dashboard.date_creation = datetime.now()
        
        # Mock widget instances
        mock_widget1 = Mock()
        mock_widget1.id = 1
        mock_widget1.widget_type = "intercontrat_rate"
        mock_widget1.position_x = 0
        mock_widget1.position_y = 0
        mock_widget1.width = 2
        mock_widget1.height = 1
        mock_widget1.config = {"threshold": 15}
        
        mock_dashboard.widget_instances = [mock_widget1]
        
        mock_session.query.return_value.filter.return_value.first.return_value = mock_dashboard
        
        result = DashboardService.get_dashboard_by_id(1)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['nom'], "Test Dashboard")
        self.assertEqual(result['layout_config'], {"cols": 2})
        self.assertEqual(len(result['widgets']), 1)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_dashboard_by_id_not_found(self, mock_get_session):
        """Test récupération dashboard par ID - non trouvé"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = DashboardService.get_dashboard_by_id(999)
        
        self.assertIsNone(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_dashboard_by_id_exception(self, mock_get_session):
        """Test récupération dashboard par ID avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.get_dashboard_by_id(1)
        
        self.assertIsNone(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_create_dashboard_success(self, mock_get_session):
        """Test création dashboard - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_dashboard = Mock()
        mock_dashboard.id = 42
        mock_session.add.return_value = None
        
        # Simuler l'ajout en DB qui met un ID
        def set_id(obj):
            obj.id = 42
        mock_session.add.side_effect = set_id
        
        result = DashboardService.create_dashboard(
            nom="Test Dashboard",
            description="Test Desc",
            role_access="admin",
            created_by="test_user"
        )
        
        # Vérifier que add et commit ont été appelés
        self.assertTrue(mock_session.add.called)
        self.assertTrue(mock_session.commit.called)

    @patch('app.services.dashboard_service.get_database_session')
    def test_create_dashboard_exception(self, mock_get_session):
        """Test création dashboard avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.create_dashboard("Test")
        
        self.assertIsNone(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_add_widget_to_dashboard_success(self, mock_get_session):
        """Test ajout widget au dashboard - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        result = DashboardService.add_widget_to_dashboard(
            dashboard_id=1,
            widget_type="intercontrat_rate",
            position_x=0,
            position_y=0,
            width=2,
            height=1,
            config={"threshold": 15}
        )
        
        self.assertTrue(result)
        self.assertTrue(mock_session.add.called)
        self.assertTrue(mock_session.commit.called)

    @patch('app.services.dashboard_service.get_database_session')
    def test_add_widget_to_dashboard_exception(self, mock_get_session):
        """Test ajout widget avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.add_widget_to_dashboard(1, "test_widget")
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_remove_widget_from_dashboard_success(self, mock_get_session):
        """Test suppression widget - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_widget = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_widget
        
        result = DashboardService.remove_widget_from_dashboard(123)
        
        self.assertTrue(result)
        self.assertTrue(mock_session.delete.called)
        self.assertTrue(mock_session.commit.called)

    @patch('app.services.dashboard_service.get_database_session')
    def test_remove_widget_from_dashboard_not_found(self, mock_get_session):
        """Test suppression widget - non trouvé"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = DashboardService.remove_widget_from_dashboard(999)
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_remove_widget_exception(self, mock_get_session):
        """Test suppression widget avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.remove_widget_from_dashboard(123)
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_available_widgets_success(self, mock_get_session):
        """Test récupération widgets disponibles"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_widget1 = Mock()
        mock_widget1.id = 1
        mock_widget1.name = "widget1"
        mock_widget1.display_name = "Widget 1"
        mock_widget1.category = "kpi"
        mock_widget1.description = "Desc 1"
        mock_widget1.icon = "📊"
        mock_widget1.config_schema = {}
        mock_widget1.render_function = "render_widget1"
        
        mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_widget1]
        
        result = DashboardService.get_available_widgets()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "widget1")

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_available_widgets_exception(self, mock_get_session):
        """Test récupération widgets avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.get_available_widgets()
        
        self.assertEqual(result, [])

    @patch('app.services.dashboard_service.get_database_session')
    def test_update_dashboard_success(self, mock_get_session):
        """Test mise à jour dashboard - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_dashboard = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_dashboard
        
        result = DashboardService.update_dashboard(
            dashboard_id=1,
            nom="Nouveau nom",
            description="Nouvelle desc",
            role_access="user",
            is_public=True
        )
        
        self.assertTrue(result)
        self.assertEqual(mock_dashboard.nom, "Nouveau nom")
        self.assertTrue(mock_session.commit.called)

    @patch('app.services.dashboard_service.get_database_session')
    def test_update_dashboard_not_found(self, mock_get_session):
        """Test mise à jour dashboard - non trouvé"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = DashboardService.update_dashboard(1, nom="Test")
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_update_dashboard_exception(self, mock_get_session):
        """Test mise à jour dashboard avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.update_dashboard(1, nom="Test")
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_delete_dashboard_success(self, mock_get_session):
        """Test suppression dashboard - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_dashboard = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_dashboard
        
        result = DashboardService.delete_dashboard(1)
        
        self.assertTrue(result)
        self.assertTrue(mock_session.delete.called)
        self.assertTrue(mock_session.commit.called)

    @patch('app.services.dashboard_service.get_database_session')
    def test_delete_dashboard_not_found(self, mock_get_session):
        """Test suppression dashboard - non trouvé"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = DashboardService.delete_dashboard(999)
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_delete_dashboard_exception(self, mock_get_session):
        """Test suppression dashboard avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.delete_dashboard(1)
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_update_dashboard_layout_success(self, mock_get_session):
        """Test mise à jour layout dashboard - succès"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_dashboard = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_dashboard
        
        new_layout = {"cols": 3, "rows": 4}
        result = DashboardService.update_dashboard_layout(1, new_layout)
        
        self.assertTrue(result)
        self.assertEqual(mock_dashboard.layout_config, new_layout)
        self.assertTrue(mock_session.commit.called)

    @patch('app.services.dashboard_service.get_database_session')
    def test_update_dashboard_layout_not_found(self, mock_get_session):
        """Test mise à jour layout - dashboard non trouvé"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = DashboardService.update_dashboard_layout(999, {})
        
        self.assertFalse(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_update_dashboard_layout_exception(self, mock_get_session):
        """Test mise à jour layout avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardService.update_dashboard_layout(1, {})
        
        self.assertFalse(result)


class TestDashboardDataService(unittest.TestCase):
    """Tests pour la classe DashboardDataService"""

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_intercontrat_data_no_filter(self, mock_get_session):
        """Test récupération données intercontrat sans filtre"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock count pour total et avec mission
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        # Premier count() = total_consultants = 10
        # Deuxième count() = consultants_avec_mission = 8
        mock_query.count.side_effect = [10, 8]
        
        # Mock consultants sans mission
        mock_consultant1 = Mock()
        mock_consultant1.id = 1
        mock_consultant1.prenom = "Jean"
        mock_consultant1.nom = "Dupont"
        mock_consultant1.email = "jean.dupont@test.fr"
        
        mock_consultant2 = Mock()
        mock_consultant2.id = 2
        mock_consultant2.prenom = "Marie"
        mock_consultant2.nom = "Martin"
        mock_consultant2.email = "marie.martin@test.fr"
        
        mock_query.all.return_value = [mock_consultant1, mock_consultant2]
        
        # Mock _get_last_mission_date
        with patch.object(DashboardDataService, '_get_last_mission_date', return_value="01/01/2024"):
            result = DashboardDataService.get_intercontrat_data(None)
        
        self.assertEqual(result['total_consultants'], 10)
        self.assertEqual(result['consultants_avec_mission'], 8)
        self.assertEqual(result['consultants_intercontrat'], 2)
        self.assertEqual(result['taux_intercontrat'], 20)
        self.assertEqual(len(result['consultants_sans_mission']), 2)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_intercontrat_data_with_filter(self, mock_get_session):
        """Test récupération données intercontrat avec filtre BM"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        # 5 consultants total, 4 avec mission
        mock_query.count.side_effect = [5, 4]
        mock_query.all.return_value = [Mock(id=1, prenom="Test", nom="User", email="test@test.fr")]
        
        with patch.object(DashboardDataService, '_get_last_mission_date', return_value=None):
            result = DashboardDataService.get_intercontrat_data(123)
        
        self.assertEqual(result['total_consultants'], 5)
        self.assertEqual(result['consultants_intercontrat'], 1)
        self.assertEqual(result['taux_intercontrat'], 20)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_intercontrat_data_all_in_mission(self, mock_get_session):
        """Test récupération données intercontrat - tous en mission"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        # 10 consultants total, 10 avec mission
        mock_query.count.side_effect = [10, 10]
        mock_query.all.return_value = []
        
        result = DashboardDataService.get_intercontrat_data(None)
        
        self.assertEqual(result['taux_intercontrat'], 0)
        self.assertEqual(result['consultants_intercontrat'], 0)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_intercontrat_data_exception(self, mock_get_session):
        """Test récupération données intercontrat avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardDataService.get_intercontrat_data(None)
        
        self.assertEqual(result['total_consultants'], 0)
        self.assertEqual(result['taux_intercontrat'], 0)
        self.assertEqual(result['consultants_sans_mission'], [])

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_revenue_by_bm_data_with_data(self, mock_get_session):
        """Test récupération revenus par BM avec données"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        # Mock résultats query avec named attributes
        mock_row1 = Mock()
        mock_row1.id = 1
        mock_row1.prenom = "Jean"
        mock_row1.nom = "Manager"
        mock_row1.missions_count = 5
        mock_row1.tjm_moyen = 500
        mock_row1.ca_estime = 75000
        
        mock_row2 = Mock()
        mock_row2.id = 2
        mock_row2.prenom = "Marie"
        mock_row2.nom = "Lead"
        mock_row2.missions_count = 3
        mock_row2.tjm_moyen = 450
        mock_row2.ca_estime = 40000
        
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.all.return_value = [mock_row1, mock_row2]
        
        result = DashboardDataService.get_revenue_by_bm_data(period_months=3)
        
        self.assertIn('bm_revenues', result)
        self.assertEqual(len(result['bm_revenues']), 2)
        self.assertEqual(result['bm_revenues'][0]['bm_name'], "Jean Manager")
        self.assertEqual(result['bm_revenues'][0]['missions_count'], 5)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_revenue_by_bm_data_empty(self, mock_get_session):
        """Test récupération revenus par BM - pas de données"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.all.return_value = []
        
        result = DashboardDataService.get_revenue_by_bm_data()
        
        self.assertEqual(len(result['bm_revenues']), 0)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_revenue_by_bm_data_exception(self, mock_get_session):
        """Test récupération revenus par BM avec exception"""
        mock_get_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        result = DashboardDataService.get_revenue_by_bm_data()
        
        self.assertEqual(result['bm_revenues'], [])

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_last_mission_date_with_mission(self, mock_get_session):
        """Test récupération date dernière mission - avec mission"""
        mock_session = MagicMock()
        
        mock_mission = Mock()
        mock_mission.date_fin = date(2024, 10, 6)
        
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = mock_mission
        
        result = DashboardDataService._get_last_mission_date(123, mock_session)
        
        self.assertEqual(result, "06/10/2024")

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_last_mission_date_no_mission(self, mock_get_session):
        """Test récupération date dernière mission - sans mission"""
        mock_session = MagicMock()
        
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = None
        
        result = DashboardDataService._get_last_mission_date(123, mock_session)
        
        self.assertIsNone(result)

    @patch('app.services.dashboard_service.get_database_session')
    def test_get_last_mission_date_exception(self, mock_get_session):
        """Test récupération date dernière mission avec exception"""
        mock_session = MagicMock()
        mock_session.query.side_effect = Exception("DB Error")
        
        result = DashboardDataService._get_last_mission_date(123, mock_session)
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
