#!/usr/bin/env python3
"""
Script pour tester et corriger les assertions d'intention du chatbot
"""

from app.services.chatbot_service import ChatbotService
from unittest.mock import Mock, patch, MagicMock
from contextlib import contextmanager


@contextmanager
def setup_database_mock():
    """Context manager pour setup des mocks de base de données"""
    mock_session = Mock()
    mock_session.__enter__ = Mock(return_value=mock_session)
    mock_session.__exit__ = Mock(return_value=None)

    # Configuration des mocks de base - liste vide de consultants pour les tests d'intention
    mock_session.query.return_value.all.return_value = []  # Pas de consultants nommés
    mock_session.query.return_value.first.return_value = None
    mock_session.query.return_value.count.return_value = 0
    mock_session.query.return_value.filter.return_value = (
        mock_session.query.return_value
    )
    mock_session.query.return_value.order_by.return_value = (
        mock_session.query.return_value
    )
    mock_session.query.return_value.limit.return_value = mock_session.query.return_value
    mock_session.query.return_value.offset.return_value = (
        mock_session.query.return_value
    )
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.rollback = Mock()
    mock_session.close = Mock()

    try:
        yield mock_session
    finally:
        pass


def test_all_intentions():
    """Teste toutes les intentions et affiche les résultats"""

    print("🧪 Test de toutes les intentions...")

    with patch(
        "app.services.chatbot_service.get_database_session"
    ) as mock_session_func:
        with setup_database_mock() as session:
            mock_session_func.return_value = session
            chatbot = ChatbotService()

            # Tests d'intentions
            test_cases = [
                ("combien de consultants", "???"),
                ("qui est jean dupont", "???"),
                ("competences python", "???"),
                ("missions chez google", "???"),
                ("salaire moyen", "???"),
                ("languages anglais", "???"),
                ("experience java", "???"),
                ("statistiques generales", "???"),
                ("bonjour", "???"),
            ]

            results = []
            for question, expected in test_cases:
                actual = chatbot._analyze_intent(question)
                results.append((question, expected, actual))
                print(f"  '{question}' -> '{actual}'")

            print("\n📝 Résultats pour correction:")
            for question, expected, actual in results:
                print(
                    f'        assert chatbot._analyze_intent("{question}") == "{actual}"'
                )


if __name__ == "__main__":
    test_all_intentions()
