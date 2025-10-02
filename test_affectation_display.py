#!/usr/bin/env python3
"""
Test direct de la fonction _display_affectation_info
"""

import os
import sys

sys.path.append(".")

from unittest.mock import MagicMock

# Simuler l'environnement Streamlit
import streamlit as st


def mock_streamlit():
    """Mock des fonctions Streamlit pour test"""
    # Mock st.columns
    col1_mock = MagicMock()
    col2_mock = MagicMock()
    col3_mock = MagicMock()

    def columns_mock(spec):
        if isinstance(spec, list):
            num_cols = len(spec)
        else:
            num_cols = spec
            
        if num_cols == 2:
            return col1_mock, col2_mock
        elif num_cols == 3:
            return col1_mock, col2_mock, col3_mock
        else:
            return [MagicMock() for _ in range(num_cols)]

    st.columns = columns_mock
    st.markdown = MagicMock()
    st.write = MagicMock()
    st.success = MagicMock()
    st.warning = MagicMock()
    st.error = MagicMock()
    st.info = MagicMock()

    # Mock des méthodes des colonnes
    for col in [col1_mock, col2_mock, col3_mock]:
        col.__enter__ = MagicMock(return_value=col)
        col.__exit__ = MagicMock(return_value=None)
        col.markdown = MagicMock()
        col.write = MagicMock()


def test_affectation_display():
    """Test de la fonction _display_affectation_info"""

    try:
        # Mock Streamlit
        mock_streamlit()

        # Import après mock
        from app.database.database import get_session
        from app.database.models import Consultant
        from app.pages_modules.consultant_info import _display_affectation_info

        # Récupérer Eric
        with get_session() as session:
            eric = (
                session.query(Consultant)
                .filter(Consultant.email == "eric.lapina@quanteam.fr")
                .first()
            )

            if not eric:
                print("❌ Eric non trouvé")
                return False

            print(f"✅ Eric trouvé: {eric.prenom} {eric.nom}")
            print(f"   - Statut période d'essai: {eric.etat_periode_essai}")
            print(f"   - Fin période d'essai: {eric.fin_periode_essai}")
            print(f"   - Actif: {eric.actif}")
            print(f"   - Société: {eric.societe}")

            print("\n🧪 Test de _display_affectation_info...")

            try:
                # Appeler la fonction
                _display_affectation_info(eric)
                print("✅ Fonction exécutée sans erreur")

                # Vérifier les appels mockés
                print("\n📝 Appels Streamlit capturés:")
                if st.markdown.call_count > 0:
                    print(f"   - st.markdown appelé {st.markdown.call_count} fois")
                    for i, call in enumerate(st.markdown.call_args_list):
                        args, kwargs = call
                        if args:
                            print(f"     Call {i+1}: {args[0][:100]}...")

                if st.columns.call_count > 0:
                    print(f"   - st.columns appelé {st.columns.call_count} fois")

                return True

            except Exception as func_error:
                print(f"❌ Erreur dans _display_affectation_info: {func_error}")
                print(f"   Type: {type(func_error).__name__}")
                import traceback

                print(f"   Trace: {traceback.format_exc()}")
                return False

    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback

        print(f"   Trace: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    print("🔧 Test de la fonction _display_affectation_info...")
    success = test_affectation_display()
    if success:
        print("\n✅ Test réussi!")
    else:
        print("\n❌ Test échoué")
