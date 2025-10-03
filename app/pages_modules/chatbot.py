"""
Page Chatbot pour Consultator
Interface conversationnelle pour interroger les données
"""

import os
import sys
from datetime import datetime

import streamlit as st

# Ajout du chemin pour les imports
sys.path.append(os.path.dirname(__file__))

# Imports des services
try:
    from services.chatbot_service import ChatbotService
except ImportError:
    # Import alternatif si le chemin ne fonctionne pas
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from services.chatbot_service import ChatbotService


def show():
    """Affiche la page du chatbot"""

    st.title("🤖 Assistant IA Consultator")
    st.markdown("### Interrogez vos données de consultant avec l'intelligence artificielle")

    # Initialiser le service chatbot dans la session
    if "chatbot_service" not in st.session_state:
        st.session_state.chatbot_service = ChatbotService()

    # Initialiser l'historique des conversations
    if "messages" not in st.session_state:
        st.session_state.messages = []

        # Message de bienvenue
        welcome_message = {
            "role": "assistant",
            "content": """👋 **Bonjour !** Je suis votre assistant IA pour Consultator.

Je peux vous aider à interroger vos données de consultants, missions et compétences.

💡 **Exemples de questions :**
- "Quel est le salaire de Jean Dupont ?"
- "Qui maîtrise Python ?"
- "Quelles sont les missions chez BNP Paribas ?"
- "Combien de consultants sont actifs ?"
- "Quel est le TJM moyen ?"

Que souhaitez-vous savoir ? 😊""",
            "timestamp": datetime.now(),
        }
        st.session_state.messages.append(welcome_message)

    # Afficher l'historique des conversations
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                # Afficher un timestamp pour les anciens messages
                if message["role"] == "assistant" and len(st.session_state.messages) > 1:
                    timestamp = message.get("timestamp", datetime.now())
                    st.caption(f"⏰ {timestamp.strftime('%H:%M')}")

    # Interface de saisie
    user_input = st.chat_input("Posez votre question...")

    if user_input:
        # Ajouter le message utilisateur
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now(),
        }
        st.session_state.messages.append(user_message)

        # Afficher le message utilisateur immédiatement
        with st.chat_message("user"):
            st.markdown(user_input)

        # Traiter la question avec le service chatbot
        with st.chat_message("assistant"):
            with st.spinner("🤔 Réflexion en cours..."):
                try:
                    # Traiter la question
                    response_data = st.session_state.chatbot_service.process_question(user_input)

                    # Extraire la réponse
                    response_content = response_data.get("response", "❌ Erreur lors du traitement")
                    confidence = response_data.get("confidence", 0.0)
                    intent = response_data.get("intent", "unknown")

                    # Afficher la réponse
                    st.markdown(response_content)

                    # Afficher des métadonnées en mode debug (optionnel)
                    if st.session_state.get("debug_mode", False):
                        st.caption(f"🎯 Intention: {intent} | 📊 Confiance: {confidence:.1%}")

                    # Si des données sont retournées, les afficher
                    if response_data.get("data"):
                        show_data_insights(response_data["data"], intent)

                    # Ajouter la réponse à l'historique
                    assistant_message = {
                        "role": "assistant",
                        "content": response_content,
                        "timestamp": datetime.now(),
                        "metadata": {
                            "intent": intent,
                            "confidence": confidence,
                            "data": response_data.get("data"),
                        },
                    }
                    st.session_state.messages.append(assistant_message)

                except Exception as e:
                    error_message = f"❌ **Erreur :** {str(e)}"
                    st.error(error_message)

                    # Ajouter l'erreur à l'historique
                    error_response = {
                        "role": "assistant",
                        "content": error_message,
                        "timestamp": datetime.now(),
                    }
                    st.session_state.messages.append(error_response)

        # Rerun pour mettre à jour l'affichage
        st.rerun()

    # Sidebar avec options et historique
    show_sidebar()


def show_data_insights(data: dict, intent: str):
    """Affiche des insights visuels basés sur les données retournées"""

    if intent == "salaire" and "stats" in data:
        stats = data["stats"]

        st.markdown("---")
        st.markdown("📊 **Détails des salaires :**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Minimum", f"{stats['minimum']:,.0f} €")
            st.metric("📊 Moyenne", f"{stats['moyenne']:,.0f} €")

        with col2:
            st.metric("🎯 Médiane", f"{stats['mediane']:,.0f} €")
            st.metric("👥 Total", f"{stats['total']} consultants")

        with col3:
            st.metric("🚀 Maximum", f"{stats['maximum']:,.0f} €")

    elif intent == "statistiques" and "stats" in data:
        stats = data["stats"]

        st.markdown("---")
        st.markdown("📈 **Tableau de bord :**")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**👥 Consultants**")
            st.metric("Total", stats["consultants_total"])
            st.metric(
                "Actifs",
                stats["consultants_actifs"],
                delta=stats["consultants_actifs"] - stats["consultants_inactifs"],
            )

        with col2:
            st.markdown("**💼 Missions**")
            st.metric("Total", stats["missions_total"])
            st.metric("En cours", stats["missions_en_cours"])

        # Graphique simple avec st.progress
        if stats["consultants_total"] > 0:
            actifs_ratio = stats["consultants_actifs"] / stats["consultants_total"]
            st.markdown(f"**Taux d'activité : {actifs_ratio:.1%}**")
            st.progress(actifs_ratio)


def show_sidebar():
    """Affiche la sidebar avec les options"""

    with st.sidebar:
        st.markdown("### 🤖 Assistant IA")

        # Bouton pour effacer l'historique
        if st.button("🗑️ Effacer l'historique", type="secondary"):
            st.session_state.messages = []
            if "chatbot_service" in st.session_state:
                del st.session_state.chatbot_service
            st.rerun()

        st.markdown("---")

        # Mode debug (optionnel)
        debug_mode = st.checkbox("🔧 Mode debug", value=st.session_state.get("debug_mode", False))
        st.session_state.debug_mode = debug_mode

        st.markdown("---")
        st.markdown("### 💡 Conseils d'utilisation")

        with st.expander("🎯 Types de questions", expanded=False):
            st.markdown(
                """
**💰 Salaires :**
- "Quel est le salaire de [nom] ?"
- "Salaire moyen des consultants"

**🎯 Compétences :**
- "Qui maîtrise [technologie] ?"
- "Compétences de [nom]"

**💼 Missions :**
- "Missions chez [entreprise]"
- "Projets de [consultant]"

**📊 Statistiques :**
- "Combien de consultants actifs ?"
- "TJM moyen"
"""
            )

        with st.expander("🚀 Fonctionnalités", expanded=False):
            st.markdown(
                """
✅ Recherche intelligente de consultants
✅ Analyse des salaires et TJM
✅ Historique des missions
✅ Statistiques en temps réel
✅ Interface conversationnelle
"""
            )

        st.markdown("---")
        st.markdown("### 📊 Statistiques rapides")

        # Afficher quelques stats rapides
        try:
            if "chatbot_service" in st.session_state:
                stats = st.session_state.chatbot_service._get_general_stats()

                st.metric("👥 Consultants", stats["consultants_total"])
                st.metric("💼 Missions", stats["missions_total"])

                if stats["tjm_moyen"] > 0:
                    st.metric("💰 TJM moyen", f"{stats['tjm_moyen']:.0f} €")

        except Exception:
            st.caption("⏳ Chargement des statistiques...")


if __name__ == "__main__":
    show()
