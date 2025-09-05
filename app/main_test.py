import streamlit as st

st.title("🏢 Consultator - Test")
st.write("Si vous voyez ce message, l'application fonctionne !")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Consultants", "1000+")

with col2:
    st.metric("💼 Missions", "500+")

with col3:
    st.metric("📈 Taux", "85%")

st.success("✅ Application fonctionnelle !")
