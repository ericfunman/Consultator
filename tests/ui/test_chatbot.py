import pytest
from unittest.mock import patch, MagicMock
from app.pages_modules.chatbot import show_data_insights, show_sidebar, show
from tests.fixtures.base_test import BaseUITest


class TestShowDataInsights(BaseUITest):
    @patch("app.pages_modules.chatbot.st")
    def test_show_data_insights_salaire(self, mock_st):
        """Test affichage insights pour données salaire"""
        # Setup
        data = {
            "stats": {
                "minimum": 45000,
                "moyenne": 65000,
                "mediane": 62000,
                "maximum": 85000,
                "total": 25,
            }
        }

        mock_st.markdown = MagicMock()
        mock_st.columns = MagicMock(
            return_value=[MagicMock(), MagicMock(), MagicMock()]
        )
        mock_st.metric = MagicMock()

        # Execute
        show_data_insights(data, "salaire")

        # Verify
        assert mock_st.markdown.call_count >= 2
        assert mock_st.columns.call_count == 1
        assert mock_st.metric.call_count == 5  # 5 metrics for salary stats

    @patch("app.pages_modules.chatbot.st")
    def test_show_data_insights_statistiques(self, mock_st):
        """Test affichage insights pour données statistiques"""
        # Setup
        data = {
            "stats": {
                "consultants_total": 42,
                "consultants_actifs": 35,
                "consultants_inactifs": 7,
                "missions_total": 28,
                "missions_en_cours": 15,
            }
        }

        mock_st.markdown = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        mock_st.metric = MagicMock()
        mock_st.progress = MagicMock()

        # Execute
        show_data_insights(data, "statistiques")

        # Verify
        assert mock_st.markdown.call_count >= 3
        assert mock_st.columns.call_count == 1
        assert mock_st.metric.call_count == 4  # 4 metrics for general stats
        mock_st.progress.assert_called_once()

    @patch("app.pages_modules.chatbot.st")
    def test_show_data_insights_unknown_intent(self, mock_st):
        """Test affichage insights pour intention inconnue"""
        # Setup
        data = {"test": "data"}

        mock_st.markdown = MagicMock()

        # Execute
        show_data_insights(data, "unknown_intent")

        # Verify
        # Should not display anything for unknown intent
        mock_st.markdown.assert_not_called()


class TestShowSidebar(BaseUITest):
    @patch("app.pages_modules.chatbot.st")
    def test_show_sidebar_basic_display(self, mock_st):
        """Test affichage de base de la sidebar"""
        # Setup
        mock_session_state = MagicMock()
        mock_st.session_state = mock_session_state
        mock_st.sidebar = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.checkbox = MagicMock(return_value=False)
        mock_st.expander = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.caption = MagicMock()

        # Execute
        show_sidebar()

        # Verify
        mock_st.sidebar.__enter__.assert_called_once()
        mock_st.sidebar.__exit__.assert_called_once()
        assert mock_st.markdown.call_count >= 5  # Multiple markdown calls
        mock_st.button.assert_called_once()

    @patch("app.pages_modules.chatbot.st")
    def test_show_sidebar_clear_history(self, mock_st):
        """Test effacement de l'historique"""
        # Setup
        mock_session_state = MagicMock()
        mock_st.session_state = mock_session_state
        mock_st.sidebar = MagicMock()
        mock_st.button = MagicMock(return_value=True)  # Clear button clicked
        mock_st.checkbox = MagicMock(return_value=False)
        mock_st.expander = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.rerun = MagicMock()

        # Execute
        show_sidebar()

        # Verify
        mock_st.rerun.assert_called_once()

    @patch("app.pages_modules.chatbot.st")
    def test_show_sidebar_with_stats(self, mock_st):
        """Test affichage des statistiques dans la sidebar"""
        # Setup
        mock_service = MagicMock()
        mock_service._get_general_stats.return_value = {
            "consultants_total": 42,
            "missions_total": 15,
            "tjm_moyen": 650,
        }

        # Create a mock session state that supports attribute assignment
        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.chatbot_service = mock_service

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state
        mock_st.sidebar = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.checkbox = MagicMock(return_value=False)
        mock_st.expander = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.metric = MagicMock()

        # Execute
        show_sidebar()

        # Verify
        mock_service._get_general_stats.assert_called_once()
        assert mock_st.metric.call_count == 3  # 3 metrics: consultants, missions, TJM

    @patch("app.pages_modules.chatbot.st")
    def test_show_sidebar_stats_error(self, mock_st):
        """Test gestion d'erreur lors de l'affichage des stats"""
        # Setup
        mock_service = MagicMock()
        mock_service._get_general_stats.side_effect = Exception("Stats error")

        # Create a mock session state that supports attribute assignment
        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.chatbot_service = mock_service

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state
        mock_st.sidebar = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.checkbox = MagicMock(return_value=False)
        mock_st.expander = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.caption = MagicMock()

        # Execute
        show_sidebar()

        # Verify
        mock_st.caption.assert_called_with("⏳ Chargement des statistiques...")


class TestIntegrationScenarios(BaseUITest):
    @patch("app.pages_modules.chatbot.st")
    def test_show_data_insights_edge_cases(self, mock_st):
        """Test cas limites pour show_data_insights"""
        # Setup proper column mocks
        mock_st.columns = MagicMock(
            return_value=[MagicMock(), MagicMock(), MagicMock()]
        )
        mock_st.metric = MagicMock()

        # Test with empty data
        show_data_insights({}, "salaire")

        # Test with complete stats
        complete_stats = {
            "stats": {
                "minimum": 45000,
                "moyenne": 65000,
                "mediane": 62000,
                "maximum": 85000,
                "total": 25,
            }
        }
        show_data_insights(complete_stats, "salaire")

        # Test with unknown intent
        show_data_insights({"stats": {"moyenne": 65000}}, "unknown")

        # Verify no errors occur
        # (This test mainly ensures no exceptions are raised)


class TestShowFunction(BaseUITest):
    @patch("app.pages_modules.chatbot.st")
    @patch("app.pages_modules.chatbot.ChatbotService")
    def test_show_initialization(self, mock_chatbot_service, mock_st):
        """Test initialisation de la fonction show"""
        # Setup
        mock_service_instance = MagicMock()
        mock_chatbot_service.return_value = mock_service_instance

        # Create a mock session state that supports attribute assignment
        class MockSessionState(dict):
            def __init__(self):
                super().__init__()

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __delattr__(self, name):
                try:
                    del self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.container = MagicMock()
        mock_st.chat_input = MagicMock(return_value=None)  # No user input
        mock_st.button = MagicMock(return_value=False)  # Don't clear history
        mock_st.checkbox = MagicMock(return_value=False)  # Debug mode off
        mock_st.expander = MagicMock()
        mock_st.caption = MagicMock()

        # Execute
        show()

        # Verify initialization
        mock_st.title.assert_called_once_with("🤖 Assistant IA Consultator")
        assert "chatbot_service" in mock_session_state
        assert "messages" in mock_session_state
        assert len(mock_session_state.messages) == 1  # Welcome message

    @patch("app.pages_modules.chatbot.st")
    @patch("app.pages_modules.chatbot.ChatbotService")
    def test_show_with_user_input(self, mock_chatbot_service, mock_st):
        """Test traitement d'une question utilisateur"""
        # Setup
        mock_service_instance = MagicMock()
        mock_service_instance.process_question.return_value = {
            "response": "Voici la réponse à votre question",
            "confidence": 0.85,
            "intent": "salaire",
            "data": {"stats": {"moyenne": 65000}},
        }
        mock_chatbot_service.return_value = mock_service_instance

        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.messages = []

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __delattr__(self, name):
                try:
                    del self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.container = MagicMock()
        mock_st.chat_input = MagicMock(return_value="Quel est le salaire moyen ?")
        mock_st.chat_message = MagicMock()
        mock_st.spinner = MagicMock()
        mock_st.rerun = MagicMock()
        mock_st.button = MagicMock(return_value=False)  # Don't clear history
        mock_st.checkbox = MagicMock(return_value=False)  # Debug mode off
        mock_st.expander = MagicMock()
        mock_st.caption = MagicMock()

        # Execute
        show()

        # Verify user input processing
        mock_service_instance.process_question.assert_called_once_with(
            "Quel est le salaire moyen ?"
        )
        mock_st.rerun.assert_called_once()  # Called once in main logic (no clear history button click)
        assert (
            len(mock_session_state.messages) == 2
        )  # User message + assistant response

    @patch("app.pages_modules.chatbot.st")
    @patch("app.pages_modules.chatbot.ChatbotService")
    def test_show_error_handling(self, mock_chatbot_service, mock_st):
        """Test gestion d'erreur lors du traitement"""
        # Setup
        mock_service_instance = MagicMock()
        mock_service_instance.process_question.side_effect = Exception("Service error")
        mock_chatbot_service.return_value = mock_service_instance

        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.messages = []

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __delattr__(self, name):
                try:
                    del self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.container = MagicMock()
        mock_st.chat_input = MagicMock(return_value="Test question")
        mock_st.chat_message = MagicMock()
        mock_st.spinner = MagicMock()
        mock_st.error = MagicMock()
        mock_st.rerun = MagicMock()
        mock_st.button = MagicMock(return_value=False)  # Don't clear history
        mock_st.checkbox = MagicMock(return_value=False)  # Debug mode off
        mock_st.expander = MagicMock()
        mock_st.caption = MagicMock()

        # Execute
        show()

        # Verify error handling
        mock_st.error.assert_called_once()
        # Note: messages may not be added due to mocking complexity, focus on error display

    @patch("app.pages_modules.chatbot.st")
    @patch("app.pages_modules.chatbot.ChatbotService")
    def test_show_debug_mode(self, mock_chatbot_service, mock_st):
        """Test mode debug activé"""
        # Setup
        mock_service_instance = MagicMock()
        mock_service_instance.process_question.return_value = {
            "response": "Debug response",
            "confidence": 0.9,
            "intent": "statistiques",
            "data": {},
        }
        mock_chatbot_service.return_value = mock_service_instance

        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.messages = []
                self.debug_mode = True

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __delattr__(self, name):
                try:
                    del self[name]
                except KeyError:
                    raise AttributeError(
                        f"'MockSessionState' object has no attribute '{name}'"
                    )

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.container = MagicMock()
        mock_st.chat_input = MagicMock(return_value="Test question")
        mock_st.chat_message = MagicMock()
        mock_st.spinner = MagicMock()
        mock_st.caption = MagicMock()
        mock_st.rerun = MagicMock()
        mock_st.button = MagicMock(return_value=False)  # Don't clear history
        mock_st.checkbox = MagicMock(return_value=True)  # Debug mode on
        mock_st.expander = MagicMock()

        # Execute
        show()

        # Verify debug information is displayed
        assert mock_st.caption.call_count >= 1  # At least one caption call
        # Check that debug info was displayed (may be mixed with other captions)
        debug_calls = [
            call
            for call in mock_st.caption.call_args_list
            if "🎯 Intention:" in str(call)
        ]
        assert len(debug_calls) == 1
