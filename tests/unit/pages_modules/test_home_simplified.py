"""
Test home simplifié pour améliorer la couverture
"""
import unittest
from unittest.mock import patch, MagicMock

class TestHomeSimplified(unittest.TestCase):
    """Tests simplifiés pour le module home"""
    
    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_no_data(self, mock_get_db_info, mock_st):
        """Test show() sans données"""
        mock_get_db_info.return_value = {
            'exists': True,
            'consultants': 0,
            'missions': 0, 
            'practices': 0
        }
        mock_st.title.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_st.metric.return_value = None
        
        from app.pages_modules.home import show
        show()
        
        mock_st.title.assert_called_once_with("🏠 Accueil - Consultator")
        self.assertGreater(mock_st.columns.call_count, 0)
    
    @patch('app.pages_modules.home.st')
    def test_get_database_info_basic(self, mock_st):
        """Test get_database_info() fonction de base"""
        with patch('app.pages_modules.home.get_database_session') as mock_session:
            mock_session_obj = mock_session.return_value.__enter__.return_value
            mock_session_obj.query.return_value.count.return_value = 5
            
            from app.pages_modules.home import get_database_info
            result = get_database_info()
            
            self.assertIsInstance(result, dict)
            self.assertIn('exists', result)
    
    @patch('app.pages_modules.home.st')
    def test_show_getting_started_basic_structure(self, mock_st):
        """Test show_getting_started() structure de base"""
        mock_st.subheader.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.container.return_value.__enter__ = MagicMock()
        mock_st.container.return_value.__exit__ = MagicMock()
        mock_st.markdown.return_value = None
        mock_st.button.return_value = False
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock()
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifier que la fonction s'exécute sans erreur
        self.assertGreater(mock_st.subheader.call_count, 0)

if __name__ == '__main__':
    unittest.main()
