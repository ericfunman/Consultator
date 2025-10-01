"""
Tests de couverture mega pour home.py
Target: Passer de 37% à 85%+ de couverture
Module: 82 statements total, 52 manquants à couvrir
"""

import unittest
from datetime import datetime, date, timedelta
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import sys
import os


class MockSessionState(dict):
    """Mock pour st.session_state qui supporte à la fois dict et attributs"""
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            self[key] = None
            return None
    
    def __setattr__(self, key, value):
        self[key] = value


class TestHomeMegaCoverage(unittest.TestCase):
    """Tests mega pour home.py - Coverage ciblé"""
    
    def setUp(self):
        """Setup pour chaque test"""
        self.mock_col = MagicMock()
        self.mock_col.__enter__ = Mock(return_value=self.mock_col)
        self.mock_col.__exit__ = Mock(return_value=None)
        
        # Mock pour database info
        self.db_info_exists = {
            "exists": True,
            "consultants": 25,
            "missions": 45,
            "practices": 5
        }
        
        self.db_info_not_exists = {
            "exists": False,
            "consultants": 0,
            "missions": 0
        }
        
        self.db_info_empty = {
            "exists": True,
            "consultants": 0,
            "missions": 0
        }
    
    # ===================== MODULE STRUCTURE TESTS =====================
    
    def test_module_imports_and_constants(self):
        """Test des imports et constantes du module"""
        from app.pages_modules.home import DETAIL_COLUMN
        
        # Vérifications
        self.assertEqual(DETAIL_COLUMN, "Détail")
    
    def test_path_setup_logic(self):
        """Test de la logique d'ajout de path"""
        # Tester l'import du module pour déclencher la logique path
        import app.pages_modules.home
        
        # Le module doit s'importer sans erreur
        self.assertTrue(hasattr(app.pages_modules.home, 'show'))
        self.assertTrue(hasattr(app.pages_modules.home, 'show_dashboard_charts'))
        self.assertTrue(hasattr(app.pages_modules.home, 'show_getting_started'))
    
    # ===================== MAIN SHOW FUNCTION TESTS =====================
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('streamlit.title')
    @patch('streamlit.error')
    @patch('streamlit.button')
    def test_show_database_not_exists(self, mock_button, mock_error, mock_title, mock_get_db_info):
        """Test show() avec base de données non existante"""
        # Setup
        mock_get_db_info.return_value = self.db_info_not_exists
        mock_button.return_value = False
        
        from app.pages_modules.home import show
        show()
        
        # Vérifications
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_get_db_info.assert_called_once()
        mock_error.assert_called_once_with("❌ Base de données non initialisée")
        mock_button.assert_called_once_with("Initialiser la base de données")
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('streamlit.title')
    @patch('streamlit.error')
    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_show_database_initialization_button_clicked(self, mock_rerun, mock_success, 
                                                        mock_button, mock_error, mock_title, mock_get_db_info):
        """Test show() avec clic sur bouton d'initialisation"""
        # Setup
        mock_get_db_info.return_value = self.db_info_not_exists
        mock_button.return_value = True
        
        with patch('database.database.init_database', return_value=True) as mock_init_db:
            from app.pages_modules.home import show
            show()
        
        # Vérifications
        mock_init_db.assert_called_once()
        mock_success.assert_called_once_with("✅ Base de données initialisée avec succès !")
        mock_rerun.assert_called_once()
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('streamlit.title')
    @patch('streamlit.error')
    @patch('streamlit.button')
    def test_show_database_initialization_failed(self, mock_button, mock_error, mock_title, mock_get_db_info):
        """Test show() avec échec d'initialisation de DB"""
        # Setup
        mock_get_db_info.return_value = self.db_info_not_exists
        mock_button.return_value = True
        
        with patch('database.database.init_database', return_value=False) as mock_init_db:
            from app.pages_modules.home import show
            show()
        
        # Vérifications
        mock_init_db.assert_called_once()
        # Pas de success ou rerun si init_database retourne False
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('app.pages_modules.home.show_getting_started')
    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.markdown')
    def test_show_with_empty_database(self, mock_markdown, mock_metric, mock_columns, 
                                     mock_title, mock_getting_started, mock_get_db_info):
        """Test show() avec base de données vide"""
        # Setup
        mock_get_db_info.return_value = self.db_info_empty
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifications
        mock_get_db_info.assert_called_once()
        mock_columns.assert_called_once_with(3)
        mock_getting_started.assert_called_once()
        # Verify metrics calls
        self.assertEqual(mock_metric.call_count, 3)
        mock_markdown.assert_called_once_with("---")
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('app.pages_modules.home.show_dashboard_charts')
    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.markdown')
    def test_show_with_data(self, mock_markdown, mock_metric, mock_columns, 
                           mock_title, mock_dashboard_charts, mock_get_db_info):
        """Test show() avec des données existantes"""
        # Setup
        mock_get_db_info.return_value = self.db_info_exists
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifications
        mock_get_db_info.assert_called_once()
        mock_columns.assert_called_once_with(3)
        mock_dashboard_charts.assert_called_once()
        # Verify metrics with actual data
        self.assertEqual(mock_metric.call_count, 3)
    
    # ===================== METRICS DISPLAY TESTS =====================
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_metrics_values_display(self, mock_metric, mock_columns, mock_title, mock_get_db_info):
        """Test des valeurs affichées dans les métriques"""
        # Setup
        mock_get_db_info.return_value = self.db_info_exists
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        # Mock show_dashboard_charts pour éviter le problème de columns dans cette fonction
        with patch('app.pages_modules.home.show_dashboard_charts'):
            from app.pages_modules.home import show
            show()
        
        # Vérifier les appels de métriques avec les bonnes valeurs
        expected_calls = [
            unittest.mock.call(
                label="👥 Consultants",
                value=25,
                delta="Actifs dans la practice"
            ),
            unittest.mock.call(
                label="💼 Missions", 
                value=45,
                delta="En cours et terminées"
            ),
            unittest.mock.call(
                label="📊 Taux d'occupation",
                value="85%",
                delta="2%"
            )
        ]
        
        mock_metric.assert_has_calls(expected_calls, any_order=False)
    
    # ===================== DASHBOARD CHARTS TESTS =====================
    
    @patch('streamlit.columns')
    @patch('streamlit.subheader') 
    @patch('streamlit.plotly_chart')
    @patch('streamlit.dataframe')
    def test_show_dashboard_charts_basic(self, mock_dataframe, mock_plotly_chart, 
                                        mock_subheader, mock_columns):
        """Test de show_dashboard_charts - structure de base"""
        # Setup
        mock_columns.return_value = [self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show_dashboard_charts
        show_dashboard_charts()
        
        # Vérifications
        mock_columns.assert_called_once_with(2)
        self.assertEqual(mock_subheader.call_count, 2)
        mock_plotly_chart.assert_called_once()
        mock_dataframe.assert_called_once()
    
    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    @patch('streamlit.plotly_chart')
    @patch('streamlit.dataframe')
    def test_show_dashboard_charts_data_generation(self, mock_dataframe, mock_plotly_chart,
                                                  mock_subheader, mock_columns):
        """Test de la génération de données dans show_dashboard_charts"""
        # Setup
        mock_columns.return_value = [self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show_dashboard_charts
        show_dashboard_charts()
        
        # Vérifier que dataframe a été appelé avec les bonnes données
        self.assertEqual(mock_dataframe.call_count, 1)
        call_args = mock_dataframe.call_args
        
        # Vérifier que c'est un DataFrame pandas
        df_arg = call_args[0][0]
        self.assertIsInstance(df_arg, pd.DataFrame)
        
        # Vérifier les colonnes du DataFrame d'activités
        expected_columns = ["Date", "Action", "Détail"]
        self.assertEqual(list(df_arg.columns), expected_columns)
        
        # Vérifier le nombre de lignes d'activités
        self.assertEqual(len(df_arg), 4)
    
    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    @patch('streamlit.plotly_chart')
    @patch('plotly.express.line')
    @patch('streamlit.dataframe')
    def test_show_dashboard_charts_revenue_generation(self, mock_dataframe, mock_px_line,
                                                     mock_plotly_chart, mock_subheader, mock_columns):
        """Test de la génération du graphique de revenus"""
        # Setup
        mock_columns.return_value = [self.mock_col, self.mock_col]
        mock_fig = MagicMock()
        mock_px_line.return_value = mock_fig
        
        from app.pages_modules.home import show_dashboard_charts
        show_dashboard_charts()
        
        # Vérifications du graphique
        mock_px_line.assert_called_once()
        call_args = mock_px_line.call_args
        
        # Vérifier les paramètres du graphique
        self.assertEqual(call_args[1]['x'], "Mois")
        self.assertEqual(call_args[1]['y'], "Revenus")
        self.assertEqual(call_args[1]['title'], "Évolution mensuelle des revenus")
        
        # Vérifier que le DataFrame de revenus est correct
        df_revenus = call_args[0][0]
        self.assertIsInstance(df_revenus, pd.DataFrame)
        self.assertEqual(list(df_revenus.columns), ["Mois", "Revenus"])
        self.assertEqual(len(df_revenus), 12)  # 12 mois
        
        # Vérifier que plotly_chart a été appelé avec le bon figure
        mock_plotly_chart.assert_called_once_with(mock_fig, width="stretch")
    
    # ===================== GETTING STARTED TESTS =====================
    
    @patch('streamlit.subheader')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    @patch('streamlit.markdown')
    @patch('streamlit.button')
    @patch('streamlit.expander')
    def test_show_getting_started_structure(self, mock_expander, mock_button, mock_markdown,
                                          mock_container, mock_columns, mock_subheader):
        """Test de la structure de show_getting_started"""
        # Setup
        mock_columns.side_effect = [
            [self.mock_col, self.mock_col, self.mock_col],  # Premier appel (3 colonnes)
            [self.mock_col]  # Second appel (1 colonne)
        ]
        mock_container.return_value = self.mock_col
        mock_button.return_value = False
        mock_expander.return_value = self.mock_col
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifications
        self.assertEqual(mock_subheader.call_count, 2)
        self.assertEqual(mock_columns.call_count, 2)  # 3 colonnes puis 1 colonne
        self.assertEqual(mock_container.call_count, 3)  # 3 containers pour les étapes
        self.assertEqual(mock_markdown.call_count, 6)  # 3 étapes + 3 séparateurs + contenu expander
        mock_button.assert_called_once()
        mock_expander.assert_called_once()
    
    @patch('streamlit.subheader')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    @patch('streamlit.markdown')
    @patch('streamlit.button')
    @patch('streamlit.switch_page')
    @patch('streamlit.expander')
    def test_show_getting_started_button_click(self, mock_expander, mock_switch_page, mock_button,
                                              mock_markdown, mock_container, mock_columns, mock_subheader):
        """Test du clic sur le bouton d'ajout de consultant"""
        # Setup
        mock_columns.side_effect = [
            [self.mock_col, self.mock_col, self.mock_col],
            [self.mock_col]
        ]
        mock_container.return_value = self.mock_col
        mock_button.return_value = True  # Bouton cliqué
        mock_expander.return_value = self.mock_col
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifications
        mock_button.assert_called_once_with("➕ Ajouter un consultant", type="primary")
        mock_switch_page.assert_called_once_with("pages/consultants.py")
    
    @patch('streamlit.subheader')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    @patch('streamlit.markdown')
    @patch('streamlit.button')
    @patch('streamlit.expander')
    def test_show_getting_started_content_verification(self, mock_expander, mock_button, mock_markdown,
                                                      mock_container, mock_columns, mock_subheader):
        """Test du contenu des étapes dans show_getting_started"""
        # Setup
        mock_columns.side_effect = [
            [self.mock_col, self.mock_col, self.mock_col],
            [self.mock_col]
        ]
        mock_container.return_value = self.mock_col
        mock_button.return_value = False
        mock_expander.return_value = self.mock_col
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifier les subheaders
        expected_subheaders = [
            "🚀 Commencez avec Consultator",
            "⚡ Actions rapides"
        ]
        
        for i, expected in enumerate(expected_subheaders):
            self.assertEqual(mock_subheader.call_args_list[i][0][0], expected)
        
        # Vérifier que markdown a été appelé pour les étapes
        self.assertTrue(mock_markdown.called)
        
        # Vérifier le contenu de l'expander
        mock_expander.assert_called_once_with("💡 Conseils pour bien commencer")
    
    # ===================== EDGE CASES AND ERROR HANDLING =====================
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('streamlit.title')
    def test_show_with_none_db_info(self, mock_title, mock_get_db_info):
        """Test show() avec get_database_info retournant None"""
        # Setup
        mock_get_db_info.return_value = None
        
        from app.pages_modules.home import show
        
        # Doit gérer le cas None sans erreur
        try:
            show()
            # Si aucune exception, le test passe
        except Exception as e:
            self.fail(f"show() a levé une exception avec db_info=None: {e}")
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_show_with_missing_db_keys(self, mock_metric, mock_columns, mock_title, mock_get_db_info):
        """Test show() avec des clés manquantes dans db_info"""
        # Setup - db_info incomplet
        incomplete_db_info = {"exists": True}  # Manque consultants, missions
        mock_get_db_info.return_value = incomplete_db_info
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifier que les métriques utilisent des valeurs par défaut (0)
        self.assertEqual(mock_metric.call_count, 3)
    
    # ===================== INTEGRATION TESTS =====================
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('app.pages_modules.home.show_dashboard_charts')
    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.markdown')
    def test_integration_flow_with_data(self, mock_markdown, mock_metric, mock_columns,
                                       mock_title, mock_dashboard_charts, mock_get_db_info):
        """Test d'intégration complet avec données"""
        # Setup
        mock_get_db_info.return_value = self.db_info_exists
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifier le flow complet
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_get_db_info.assert_called_once()
        mock_columns.assert_called_once_with(3)
        self.assertEqual(mock_metric.call_count, 3)
        mock_markdown.assert_called_once_with("---")
        mock_dashboard_charts.assert_called_once()
    
    @patch('app.pages_modules.home.get_database_info')
    @patch('app.pages_modules.home.show_getting_started')
    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.markdown')
    def test_integration_flow_without_data(self, mock_markdown, mock_metric, mock_columns,
                                          mock_title, mock_getting_started, mock_get_db_info):
        """Test d'intégration complet sans données"""
        # Setup
        mock_get_db_info.return_value = self.db_info_empty
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifier le flow complet
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_get_db_info.assert_called_once()
        mock_columns.assert_called_once_with(3)
        self.assertEqual(mock_metric.call_count, 3)
        mock_markdown.assert_called_once_with("---")
        mock_getting_started.assert_called_once()


if __name__ == '__main__':
    unittest.main()