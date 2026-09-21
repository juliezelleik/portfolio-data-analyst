import streamlit as st

st.set_page_config(
    page_title="Portfolio Data Analyst",
    layout="wide"
)



@st.dialog("Aperçu agrandi", width="large")
def afficher_image_zoom(image, titre):
    st.subheader(titre)
    st.image(
        image,
        use_container_width=True
    )


def image_avec_zoom(image, titre, key):
    st.image(
        image,
        use_container_width=True
    )

    if st.button(
        "🔍 Agrandir l’image ci-dessus",
        key=key,
        use_container_width=True
    ):
        afficher_image_zoom(
            image,
            titre
        )



st.markdown("""
<h1 style="
    text-align:center;
    font-size:72px;
    font-weight:800;
    margin-bottom:10px;
    background: linear-gradient(90deg, #ff5fcf, #c03cff, #6f2dbd);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
">
Portfolio Data Analyst
</h1>
""", unsafe_allow_html=True)


st.markdown("""
<h3 style="
    text-align:center;
    color:#a978d8;
    font-size:28px;
    font-weight:500;
    margin-top:0px;
    margin-bottom:45px;
">
Analyse de données - Automatisation - Data Visualisation
</h3>
""", unsafe_allow_html=True)



# A PROPOS

st.subheader("A propos")

st.markdown("""
Je m'appelle Julie Planchon, Data Analyst en formation, spécialisée dans l’analyse,
l’automatisation et la création d’outils d’aide à la décision.

Après plusieurs années d’expérience professionnelle, j’oriente aujourd’hui mon parcours
vers la Data en combinant connaissance métier et compétences techniques, notamment en
Python, SQL, Power BI, Excel/VBA et Streamlit.
""")


st.divider()



# PROJET FIL ROUGE

st.markdown("""
<h2 style="
    text-align:center;
    font-size:46px;
    font-weight:750;
    margin-top:50px;
    margin-bottom:25px;
    background: linear-gradient(90deg, #ff9adf, #ff4fb8, #d63384);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
">
Projet fil rouge : CPAM du Val-de-Lys
</h2>
""", unsafe_allow_html=True)


st.write(
    "Analyse de données visant à identifier des comportements atypiques "
    "afin de prioriser les professionnels nécessitant un contrôle "
    "et ceux nécessitant un accompagnement."
)


st.caption(
    "Projet réalisé à partir de données entièrement fictives. - Guardia School"
)

st.caption(
    "Palette violette et rose choisie volontairement pour distinguer "
    "ce projet fictif d’une CPAM réelle."
)


st.divider()



# PROBLÉMATIQUE

st.header("Problématique")

st.image(
    "images/presentation.png",
    use_container_width=True
)


# GESTION DE PROJET

st.header("Gestion de projet")

st.image(
    "images/kanban.png",
    use_container_width=True
)



# PYTHON


st.header(
    "Préparation des données — Python / Pandas / Numpy"
)

st.image(
    "images/python.png",
    use_container_width=True
)



# DICTIONNAIRE


st.header("Dictionnaire de données")

st.image(
    "images/dictionnaire.png",
    use_container_width=True
)



# SQL


st.header("Modélisation & SQL")

st.image(
    "images/mcd_sql.png",
    use_container_width=True
)



# POWER BI


st.header("Dashboard Power BI")

col1, col2 = st.columns(2)


with col1:

    image_avec_zoom(
        "images/powerbi_1.png",
        "Dashboard Power BI - Vue 1",
        "zoom_powerbi_1"
    )

    image_avec_zoom(
        "images/powerbi_3.png",
        "Dashboard Power BI - Vue 3",
        "zoom_powerbi_3"
    )


with col2:

    image_avec_zoom(
        "images/powerbi_2.png",
        "Dashboard Power BI - Vue 2",
        "zoom_powerbi_2"
    )

    image_avec_zoom(
        "images/powerbi_4.png",
        "Dashboard Power BI - Vue 4",
        "zoom_powerbi_4"
    )



# RAPPORT


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


with open(
    "documents/rapport_final_atypies.pdf",
    "rb"
) as pdf_file:

    PDFbyte = pdf_file.read()


st.download_button(
    label="Télécharger le rapport d'analyse complet",
    data=PDFbyte,
    file_name="rapport_final_atypies.pdf",
    mime="application/pdf",
    use_container_width=True
)



# STREAMLIT


st.header("Dashboard Streamlit")

col1, col2 = st.columns(2)


with col1:

    image_avec_zoom(
        "images/dashboard_1.png",
        "Dashboard Streamlit - Vue 1",
        "zoom_dashboard_1"
    )

    image_avec_zoom(
        "images/dashboard_2.png",
        "Dashboard Streamlit - Vue 2",
        "zoom_dashboard_2"
    )


with col2:

    image_avec_zoom(
        "images/dashboard_3.png",
        "Dashboard Streamlit - Vue 3",
        "zoom_dashboard_3"
    )

    image_avec_zoom(
        "images/codage_python.png",
        "Codage Streamlit",
        "zoom_codage_python"
    )



# NOUVEAU DÉPARTEMENT


st.header(
    "Mise en situation : un nouveau département ajouté"
)

col1, col2 = st.columns(2)


with col1:

    image_avec_zoom(
        "images/mise_en_situation_1.png",
        "Mise en situation - Étape 1",
        "zoom_situation_1"
    )

    image_avec_zoom(
        "images/mise_en_situation_3.png",
        "Mise en situation - Étape 3",
        "zoom_situation_3"
    )


with col2:

    image_avec_zoom(
        "images/mise_en_situation_2.png",
        "Mise en situation - Étape 2",
        "zoom_situation_2"
    )

    image_avec_zoom(
        "images/mise_en_situation_4.png",
        "Mise en situation - Étape 4",
        "zoom_situation_4"
    )


st.image(
    "images/codage_api.png",
    use_container_width=True
)



# AUTOMATISATION


st.header(
    "Récapitulatif de l'automatisation"
)

st.image(
    "images/recap_automatisation.png",
    use_container_width=True
)



# MACHINE LEARNING


st.header(
    "Machine Learning : Isolation Forest"
)

col1, col2 = st.columns(2)


with col1:

    image_avec_zoom(
        "images/machine_learning.png",
        "Machine Learning - Isolation Forest",
        "zoom_ml_1"
    )

    image_avec_zoom(
        "images/machine_learning_1.png",
        "Machine Learning - Résultats",
        "zoom_ml_2"
    )


with col2:

    image_avec_zoom(
        "images/machine_learning_2.png",
        "Machine Learning - Intégration Streamlit",
        "zoom_ml_3"
    )

    image_avec_zoom(
        "images/machine_learning_3.png",
        "Machine Learning - Codage",
        "zoom_ml_4"
    )



# COMPÉTENCES


st.header("Compétences mobilisées")

st.image(
    "images/competences.png",
    use_container_width=True
)
