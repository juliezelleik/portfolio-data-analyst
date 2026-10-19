import streamlit as st

try:
    st.set_page_config(page_title="CPAM du Val-de-Lys", layout="wide")
except st.errors.StreamlitAPIException:
    pass

st.markdown("""
<style>
.stApp { background: #23272D; }
.block-container { padding-top: 3rem; max-width: 1250px; }
header[data-testid="stHeader"] { background: #23272D; }
header[data-testid="stHeader"] * { color: #EAE6F3 !important; }
h1, h2, h3, h4, p, li, label, span, div, small { color: #EAE6F3; }
h2, h3 { color: #E75BFF !important; }
div[data-testid="stHeading"] * { color: #E75BFF !important; }
hr { border-color: #5B367D !important; }

div[role="tablist"] { gap: 6px; border-bottom: 3px solid #C03CFF; }
[data-testid="stTab"], button[data-baseweb="tab"] { background: #15152B; border: 1px solid #7437B8; border-bottom: none;
        border-radius: 14px 14px 0 0; padding: 12px 15px; height: auto; cursor: pointer; }
[data-testid="stTab"]:hover, button[data-baseweb="tab"]:hover { background: #2A1745; }
[data-testid="stTab"] p, button[data-baseweb="tab"] p { color: #EAE6F3 !important; font-size: 16px; font-weight: 600; margin: 0; white-space: nowrap; }
[data-testid="stTab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"] {
        background: #C03CFF; border-color: #C03CFF; }
[data-testid="stTab"][aria-selected="true"] p, button[data-baseweb="tab"][aria-selected="true"] p { color: #FFFFFF !important; }
[data-testid="stTab"] > div:not([data-testid]) { display: none; }
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none; }

div[data-testid="stImage"] img { border-radius: 14px; border: 1px solid #5B367D; }
.stDownloadButton > button { width:100%; background:#15152B; border:1px solid #7437B8; border-radius:20px;
                             padding:38px 24px; margin:8px 0; }
.stDownloadButton > button:hover { background:#2A1745; border-color:#E72DE5; }
.stDownloadButton > button p { color:#E75BFF !important; font-size:28px; font-weight:800; }
.carte { background:#15152B; border:1px solid #7437B8; border-radius:20px; padding:18px 24px; margin:8px 0; }
.titre-cpam { text-align:center; font-size:46px; font-weight:800; color:#FFFFFF; margin:0 0 6px 0; }
</style>
""", unsafe_allow_html=True)


# images du PowerPoint, rangées dans le dossier slides
def montrer(*noms):
    for nom in noms:
        st.image("slides/" + nom, use_container_width=True)


onglets = st.tabs(["Présentation", "Gestion de projet", "Données", "Power BI", "Streamlit",
                   "API", "Machine Learning", "Compétences mobilisées"])

with onglets[0]:
    montrer("01_bienvenue.png", "02_contexte.png", "03_problematique.png", "04_données.png", "05_stack.png")

with onglets[1]:
    montrer("06_retroplanning.png", "07_budget.png", "kanban.png")

with onglets[2]:
    montrer("08_preparation.png", "python.png", "09_SQL.png")

with onglets[3]:
    montrer("10_powerbi_1.png", "11_powerbi_2.png", "12_powerbi_3.png", "13_powerbi_4.png")
    with open("rapport_final_atypies.pdf", "rb") as rapport:
        st.download_button("Télécharger le rapport d'analyse", rapport.read(),
                           file_name="rapport_final_atypies.pdf", mime="application/pdf",
                           use_container_width=True)

with onglets[4]:
    montrer("dashboard_1.png", "dashboard_2.png", "dashboard_3.png", "codage_python.png")

with onglets[5]:
    montrer("mise_en_situation_1.png", "mise_en_situation_2.png", "codage_api.png",
            "mise_en_situation_3.png", "mise_en_situation_4.png", "recap_automatisation.png")

with onglets[6]:
    montrer("machine_learning1.png", "machine_learning2.png", "machine_learning3.png", "machine_learning4.png",
            "machine_learning5.png", "machine_learning6.png", "machine_learning7.png")

with onglets[7]:
    montrer("competences.png")

st.caption("Formation Data Analyst - Guardia School - CPAM fictive")