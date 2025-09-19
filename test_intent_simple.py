import sys
sys.path.append('.')
sys.path.append('app')
from unittest.mock import Mock, patch
from contextlib import contextmanager

@contextmanager
def setup_mock():
    mock_session = Mock()
    mock_session.__enter__ = Mock(return_value=mock_session)
    mock_session.__exit__ = Mock(return_value=None)
    mock_session.query.return_value.all.return_value = []
    yield mock_session

with patch('app.services.chatbot_service.get_database_session') as mock_func:
    with setup_mock() as session:
        mock_func.return_value = session
        from app.services.chatbot_service import ChatbotService
        chatbot = ChatbotService()
        
        tests = [
            'combien de consultants',
            'qui est jean dupont', 
            'competences python',
            'missions chez google',
            'salaire moyen',
            'languages anglais',
            'experience java',
            'statistiques generales',
            'bonjour'
        ]
        
        print("# Assertions correctes pour les intentions:")
        for test in tests:
            result = chatbot._analyze_intent(test)
            print(f'assert chatbot._analyze_intent("{test}") == "{result}"')