"""
Utilitaires pour les tests ultra-simples
Fournit des mocks réutilisables pour les composants Streamlit
"""

from unittest.mock import MagicMock


def create_mock_columns(*args, **kwargs):
    """
    Crée un mock ultra-simple pour st.columns()
    Prend les mêmes arguments que st.columns() mais retourne un tuple de mocks
    """
    # Par défaut, retourne 4 colonnes comme dans les fonctions testées
    num_columns = 4
    if args and isinstance(args[0], (list, tuple)):
        num_columns = len(args[0])
    elif args and isinstance(args[0], int):
        num_columns = args[0]

    mock_columns = []
    for _ in range(num_columns):
        mock_col = MagicMock()
        mock_col.text = MagicMock(return_value=mock_col)
        mock_col.number_input = MagicMock(return_value=mock_col)
        mock_col.selectbox = MagicMock(return_value=mock_col)
        mock_col.checkbox = MagicMock(return_value=mock_col)
        mock_col.text_area = MagicMock(return_value=mock_col)
        mock_col.button = MagicMock(return_value=mock_col)
        mock_col.metric = MagicMock(return_value=mock_col)
        mock_col.markdown = MagicMock(return_value=mock_col)
        mock_col.title = MagicMock(return_value=mock_col)
        mock_col.columns = MagicMock(return_value=mock_col)
        mock_col.tabs = MagicMock(return_value=mock_col)
        mock_col.form = MagicMock(return_value=mock_col)
        mock_col.form_submit_button = MagicMock(return_value=mock_col)
        mock_col.expander = MagicMock(return_value=mock_col)
        mock_col.date_input = MagicMock(return_value=mock_col)
        mock_col.radio = MagicMock(return_value=mock_col)
        mock_col.selectbox = MagicMock(return_value=mock_col)
        mock_col.container = MagicMock(return_value=mock_col)
        mock_col.empty = MagicMock(return_value=mock_col)
        mock_col.success = MagicMock(return_value=mock_col)
        mock_col.error = MagicMock(return_value=mock_col)
        mock_col.warning = MagicMock(return_value=mock_col)
        mock_col.info = MagicMock(return_value=mock_col)
        mock_col.rerun = MagicMock(return_value=mock_col)
        mock_col.subheader = MagicMock(return_value=mock_col)
        mock_col.dataframe = MagicMock(return_value=mock_col)
        mock_col.plotly_chart = MagicMock(return_value=mock_col)
        mock_columns.append(mock_col)

    return tuple(mock_columns)


def create_mock_session_state():
    """
    Crée un mock pour st.session_state
    """
    mock_session_state = MagicMock()
    return mock_session_state


def create_mock_database_session():
    """
    Crée un mock pour la session de base de données
    """
    mock_session = MagicMock()
    return mock_session
