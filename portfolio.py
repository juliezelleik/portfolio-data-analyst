import os
import runpy

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portfolio Data Analyst",
    layout="wide"
)


#  STYLE

st.markdown("""
<style>

hr {
    height: 2px !important;
    background: #E89495 !important;
    border: none !important;
    opacity: 0.85 !important;
}

div.stButton > button {
    border-radius: 14px;
    border: none;
    background: linear-gradient(
        135deg,
        #F9D3AC,
        #FBB1AE,
        #B7E2E9
    );
    font-weight: 700;
}

div.stButton > button p {
    color: #3B2A45;
    font-weight: 800;
}

div.stButton > button:hover {
    box-shadow: 0 5px 18px rgba(251, 177, 174, 0.45);
}

div[class*="st-key-carte_"] {
    border: 2px solid #E89495 !important;
    border-radius: 18px;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(232, 148, 149, 0.28);
    padding: 14px;
    border-radius: 16px;
    background: rgba(160, 144, 159, 0.07);
}

details {
    border-color: rgba(232, 148, 149, 0.45) !important;
    border-radius: 14px !important;
}

.carte-titre {
    font-size: 30px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #E89495, #B57FD0, #8E4DB0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.carte-texte {
    min-height: 4.2em;
    line-height: 1.6;
    margin-bottom: 8px;
}

.pastille {
    display: inline-block;
    padding: 4px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 15px;
    color: white;
    margin-bottom: 14px;
    margin-right: 8px;
}

.pastille-fictif {
    border: 1px solid #E89495;
    background: transparent;
    color: #F7B1B2;
}

.pastille-encours { background: linear-gradient(135deg, #E89495, #8E4DB0); }
.pastille-termine { background: linear-gradient(135deg, #8E4DB0, #692782); }

</style>
""", unsafe_allow_html=True)


#  NAVIGATION 

if "page" not in st.session_state:
    st.session_state.page = "accueil"


def aller(page):
    st.session_state.page = page
    st.session_state.remonter = True


#  FENÊTRES (pop-up) 

@st.dialog("Projet Data et jeux vidéo")
def projet_jeux_video():

    st.write(
        "Ce projet est en cours de construction. "
        "Il sera présenté ici dès qu'il sera prêt."
    )


#  PAGE D'ACCUEIL 

def page_accueil():

    st.markdown("""
    <h1 style="
        text-align:center;
        font-size:72px;
        font-weight:800;
        margin-bottom:10px;
        background: linear-gradient(90deg, #E89495, #B57FD0, #8E4DB0);
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
        color:#AFDBD6;
        font-size:28px;
        font-weight:500;
        margin-top:0px;
        margin-bottom:45px;
    ">
    Analyse de données - Automatisation - Data Visualisation
    </h3>
    """, unsafe_allow_html=True)

    st.subheader("A propos")

    st.markdown("""
Je m'appelle Julie Planchon, Data Analyst en formation, spécialisée dans l’analyse,
l’automatisation et la création d’outils d’aide à la décision.

Après plusieurs années d’expérience professionnelle, j’oriente aujourd’hui mon parcours
vers la Data en combinant connaissance métier et compétences techniques, notamment en
Python, SQL, Power BI, Excel/VBA et Streamlit.
""")

    st.divider()

    st.subheader("Mes projets")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True, height=300, key="carte_jeux"):

            st.markdown(
                '<div class="carte-titre">Projet Data et jeux vidéo</div>'
                '<span class="pastille pastille-termine">Terminé</span>'
                '<span class="pastille pastille-fictif">Projet fictif</span>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="carte-texte">'
                'Évaluer la rentabilité d\'un jeu free-to-play après son lancement '
                'et fiabiliser les chiffres pour décider des priorités.'
                '</div>',
                unsafe_allow_html=True
            )

            st.button(
                "Ouvrir le projet",
                key="btn_jeux_video",
                use_container_width=True,
                on_click=aller,
                args=("zeloria",)
            )

    with col2:

        with st.container(border=True, height=300, key="carte_cpam"):

            st.markdown(
                '<div class="carte-titre">Projet fil rouge : '
                'CPAM du Val-de-Lys</div>'
                '<span class="pastille pastille-termine">Terminé</span>'
                '<span class="pastille pastille-fictif">Projet fictif</span>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="carte-texte">'
                'Identifier les atypies de facturation des professionnels '
                'de santé pour prioriser les contrôles et l\'accompagnement.'
                '</div>',
                unsafe_allow_html=True
            )

            st.button(
                "Ouvrir le projet",
                key="btn_cpam",
                use_container_width=True,
                on_click=aller,
                args=("cpam",)
            )


#  PAGE PROJET FIL ROUGE 

def page_cpam():

    st.button(
        "Retour à l'accueil",
        key="btn_retour",
        on_click=aller,
        args=("accueil",)
    )

    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PORTFOCPAM")
    ancien_dossier = os.getcwd()
    os.chdir(dossier)
    try:
        runpy.run_path("cpamportfofo_app.py")
    finally:
        os.chdir(ancien_dossier)


#  AFFICHAGE 

def page_zeloria():

    st.button(
        "Retour à l'accueil",
        key="btn_retour_zeloria",
        on_click=aller,
        args=("accueil",)
    )

    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zeloria")
    ancien_dossier = os.getcwd()
    os.chdir(dossier)
    try:
        runpy.run_path("zeloria_app.py")
    finally:
        os.chdir(ancien_dossier)


if st.session_state.page == "cpam":
    page_cpam()
elif st.session_state.page == "zeloria":
    page_zeloria()
else:
    page_accueil()


# quand on change de page, on remonte tout en haut
if st.session_state.get("remonter"):
    components.html("""
    <script>
    var haut = window.parent.document.querySelector('[data-testid="stMain"]')
            || window.parent.document.querySelector('section.main');
    haut.scrollTo(0, 0);
    </script>
    """, height=0)
    st.session_state.remonter = False
