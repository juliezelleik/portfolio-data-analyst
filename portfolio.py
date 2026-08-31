import streamlit as st

st.set_page_config(
    page_title="Portfolio Data Analyst",
    layout="wide"
)

st.title("Portfolio Data Analyst")

st.subheader("Projet fil rouge — CPAM du Val-de-Lys")

st.write(
    "Analyse de données visant à identifier des comportements atypiques "
    "afin de prioriser les professionnels nécessitant un contrôle "
    "et ceux nécessitant un accompagnement."
)

st.caption("Projet réalisé à partir de données entièrement fictives. - Guardia School")
st.caption("Palette violette et rose choisie volontairement pour distinguer ce projet fictif d’une CPAM réelle.")

st.divider()

st.header("Problématique")
st.image("images/presentation.png", use_container_width=True)

st.header("Gestion de projet")
st.image("images/kanban.png", use_container_width=True)

st.header("Préparation des données — Python / Pandas / Numpy")
st.image("images/python.png", use_container_width=True)

st.header("Dictionnaire de données")
st.image("images/dictionnaire.png", use_container_width=True)

st.header("Modélisation & SQL")
st.image("images/mcd_sql.png", use_container_width=True)

st.header("Dashboard Power BI")
col1, col2 = st.columns(2)

with col1:
    st.image("images/powerbi_1.png", use_container_width=True)
    st.image("images/powerbi_3.png", use_container_width=True)

with col2:
    st.image("images/powerbi_2.png", use_container_width=True)
    st.image("images/powerbi_4.png", use_container_width=True)

st.markdown("""
<style>
div.stDownloadButton > button {
    width: 100%;
    height: 70px;
    font-size: 24px;
    font-weight: 800;
    color: #ff4fd8;
    border: 2px solid #ff4fd8;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

with open("documents/rapport_final_atypies.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(
    label="Télécharger le rapport d'analyse complet",
    data=PDFbyte,
    file_name="rapport_final_atypies.pdf",
    mime="application/pdf",
    use_container_width=True
)

st.header("Compétences mobilisées")
st.image("images/competences.png", use_container_width=True)
