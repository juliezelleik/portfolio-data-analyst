import os
import runpy

import streamlit as st

st.set_page_config(
    page_title="Portfolio Data Analyst",
    layout="wide"
)


#  STYLE

st.markdown("""
<style>

div.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(192, 60, 255, 0.80);
    background: linear-gradient(
        135deg,
        rgba(255, 95, 207, 0.08),
        rgba(111, 45, 189, 0.15)
    );
    font-weight: 700;
}

div.stButton > button:hover {
    border-color: #ff5fcf;
    box-shadow: 0 5px 18px rgba(192, 60, 255, 0.22);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(192, 60, 255, 0.45);
    border-radius: 18px;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(192, 60, 255, 0.28);
    padding: 14px;
    border-radius: 16px;
    background: rgba(120, 50, 160, 0.07);
}

details {
    border-color: rgba(192, 60, 255, 0.45) !important;
    border-radius: 14px !important;
}

.etape {
    display: flex;
    align-items: center;
    gap: 22px;
    min-height: 96px;
    padding: 18px 24px;
    border-radius: 18px;
    border: 1px solid rgba(192, 60, 255, 0.60);
    background: linear-gradient(
        135deg,
        rgba(255, 95, 207, 0.14),
        rgba(111, 45, 189, 0.24)
    );
    margin-bottom: 10px;
}

.etape-num {
    flex: 0 0 56px;
    height: 56px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: 800;
    color: white;
    background: linear-gradient(135deg, #ff5fcf, #6f2dbd);
}

.etape-titre {
    font-size: 26px;
    font-weight: 800;
    line-height: 1.2;
    background: linear-gradient(90deg, #ff5fcf, #c03cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.etape-resume {
    font-size: 18px;
    margin-top: 4px;
    opacity: 0.9;
}

.carte-titre {
    font-size: 30px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #ff5fcf, #c03cff, #6f2dbd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

div[data-testid="stDownloadButton"] > button {
    border: none;
    border-radius: 14px;
    padding: 14px;
    font-weight: 800;
    color: white;
    background: linear-gradient(135deg, #ff5fcf, #c03cff);
}

div[data-testid="stDownloadButton"] > button:hover {
    color: white;
    box-shadow: 0 5px 22px rgba(255, 95, 207, 0.45);
}

div[class*="st-key-etape_"] {
    border: 1px solid rgba(192, 60, 255, 0.60);
    border-radius: 18px;
    padding: 18px 24px;
    background: linear-gradient(
        135deg,
        rgba(255, 95, 207, 0.14),
        rgba(111, 45, 189, 0.24)
    );
    margin-bottom: 10px;
}

div[class*="st-key-etape_"] details {
    background: rgba(255, 95, 207, 0.10);
    border: 1px solid rgba(255, 95, 207, 0.70) !important;
}

div[class*="st-key-etape_"] details summary {
    padding: 16px 20px;
}

div[class*="st-key-etape_"] details summary p {
    font-size: 21px;
    font-weight: 800;
    color: #ff7fd8;
}

div[class*="st-key-etape_"] details summary:hover {
    background: rgba(255, 95, 207, 0.18);
}

div[class*="st-key-etape_"] .etape {
    border: none;
    background: none;
    padding: 0;
    margin: 0;
    min-height: 0;
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
    border: 1px solid #ff5fcf;
    background: transparent;
    color: #ff9adf;
}

.pastille-encours { background: linear-gradient(135deg, #ff5fcf, #c03cff); }
.pastille-termine { background: linear-gradient(135deg, #c03cff, #6f2dbd); }

</style>
""", unsafe_allow_html=True)


#  NAVIGATION 

if "page" not in st.session_state:
    st.session_state.page = "accueil"


def aller(page):
    st.session_state.page = page


#  OUTILS D'AFFICHAGE 

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
        "Agrandir l’image ci-dessus",
        key=key,
        use_container_width=True
    ):
        afficher_image_zoom(
            image,
            titre
        )


def grille_images(images, prefixe):
    """Affiche les images 2 par ligne, chacune avec son bouton d'agrandissement."""

    for i in range(0, len(images), 2):

        colonnes = st.columns(2)

        for j, (chemin, titre) in enumerate(images[i:i + 2]):

            with colonnes[j]:

                image_avec_zoom(
                    chemin,
                    titre,
                    f"{prefixe}_{i + j}"
                )


def section(
    numero,
    titre,
    resume,
    enjeu,
    defi,
    appris,
    images=(),
    prefixe="",
    extra=None,
    bouton_bandeau=None
):
    """Une étape : un bandeau coloré à lire en une seconde,
    et le détail (texte + images) dans un volet à ouvrir."""

    bandeau = f"""
        <div class="etape">
            <div class="etape-num">{numero}</div>
            <div>
                <div class="etape-titre">{titre}</div>
                <div class="etape-resume">{resume}</div>
            </div>
        </div>
        """

    with st.container(key=f"etape_{numero}"):

        if bouton_bandeau is not None:

            col_texte, col_bouton = st.columns(
                [4, 1],
                vertical_alignment="center"
            )

            col_texte.markdown(bandeau, unsafe_allow_html=True)

            with col_bouton:
                bouton_bandeau()

        else:

            st.markdown(bandeau, unsafe_allow_html=True)

        if extra is not None:
            extra()

        with st.expander("Voir les détails et les images"):

            c1, c2, c3 = st.columns(3)

            c1.markdown(f"**Enjeu**\n\n{enjeu}")
            c2.markdown(f"**Défi**\n\n{defi}")
            c3.markdown(f"**Ce que j'ai appris**\n\n{appris}")

            if images:

                st.divider()

                grille_images(images, prefixe)

    st.write("")


#  FENÊTRES (pop-up) 

@st.dialog("La méthode Agile dans mon projet", width="large")
def expliquer_agile():

    st.markdown("""
**Qu'est-ce que la méthode Agile ?**

C'est une façon de gérer un projet par petites étapes. Au lieu de tout
préparer au départ puis de livrer à la fin, on découpe le travail en
petites tâches, on avance étape par étape et on ajuste en route.

**Le Kanban**

C'est un tableau visuel avec des colonnes (par exemple *à faire*,
*en cours*, *terminé*). Chaque tâche est une carte qui avance de gauche à
droite. On voit en un coup d'œil ce qui est fait, ce qui est en cours et ce
qu'il reste à faire.

**Dans ce projet**

J'ai organisé le projet avec un tableau Kanban : de la préparation des
données jusqu'au Machine Learning, chaque grande étape a été découpée en
tâches plus petites, ce qui m'a permis de suivre l'avancement et de
prioriser.
""")


@st.dialog("Projet Data et jeux vidéo")
def projet_jeux_video():

    st.write(
        "Ce projet est en cours de construction. "
        "Il sera présenté ici dès qu'il sera prêt."
    )


#  BLOCS SUPPLÉMENTAIRES 

def bouton_agile():

    if st.button(
        "En savoir plus sur la méthode Agile",
        key="btn_agile",
        use_container_width=True
    ):
        expliquer_agile()


def bouton_rapport():

    with open(
        "documents/rapport_final_atypies.pdf",
        "rb"
    ) as pdf_file:

        pdf = pdf_file.read()

    st.download_button(
        label="Télécharger le rapport d'analyse complet",
        data=pdf,
        file_name="rapport_final_atypies.pdf",
        mime="application/pdf",
        use_container_width=True
    )


def chiffres_ml():

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Professionnels analysés", "750")
    c2.metric("Détectés atypiques", "51")
    c3.metric("À contrôler retrouvés", "8 / 8")
    c4.metric("Non ciblés signalés", "33")


#  PAGE D'ACCUEIL 

def page_accueil():

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

        with st.container(border=True, height=300):

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

        with st.container(border=True, height=300):

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

    st.markdown("""
    <h2 style="
        text-align:center;
        font-size:46px;
        font-weight:750;
        margin-top:30px;
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

    st.header("Problématique")

    st.image(
        "images/presentation.png",
        use_container_width=True
    )

    st.header("Le projet étape par étape")

    section(
        1,
        "Gestion de projet en méthode Agile",
        "Un tableau Kanban pour suivre l'avancement",
        "Mener un projet de bout en bout, des données au Machine Learning, "
        "avec un calendrier réaliste.",
        "Garder une vision claire de l'avancement et savoir quoi traiter "
        "en priorité.",
        "Découper le travail en petites tâches visibles dans un tableau Kanban.",
        images=[("images/kanban.png", "Tableau Kanban du projet")],
        prefixe="agile",
        bouton_bandeau=bouton_agile
    )

    section(
        2,
        "Préparation et fiabilisation des données",
        "20 jeux de données contrôlés et nettoyés",
        "Des analyses fiables demandent des données fiables : 20 jeux de "
        "données (csv, txt, json) à contrôler.",
        "Repérer les valeurs manquantes, les doublons et les types ou "
        "formats incohérents avant toute analyse.",
        "Contrôler et nettoyer avec Pandas et NumPy, puis appliquer des "
        "règles de cohérence métier.",
        images=[("images/python.png", "Préparation des données")],
        prefixe="python"
    )

    section(
        3,
        "Dictionnaire de données",
        "20 tables documentées",
        "Que toute l'équipe parle des mêmes données.",
        "Documenter 20 tables : nom, type, format SQL, clé, valeur NULL "
        "autorisée ou non.",
        "Un référentiel partagé évite les erreurs de lecture entre SQL "
        "et Power BI.",
        images=[("images/dictionnaire.png", "Dictionnaire de données")],
        prefixe="dico"
    )

    section(
        4,
        "Modélisation et base de données SQL",
        "Une base MySQL de 20 tables reliées",
        "Structurer les données pour pouvoir les interroger.",
        "Relier 20 tables par des clés primaires et étrangères, puis "
        "importer les données dans MySQL.",
        "Modéliser les relations, puis écrire des requêtes d'analyse, par "
        "exemple les professionnels avec le plus d'anomalies.",
        images=[("images/mcd_sql.png", "Modélisation et SQL")],
        prefixe="sql"
    )

    section(
        5,
        "Dashboard Power BI",
        "Un dashboard de 4 pages et un score pédagogique pour prioriser",
        "Repérer les professionnels qui se distinguent de leur groupe de "
        "comparaison, en croisant plusieurs indicateurs : facturation, "
        "rejets, indus, télétransmission, activité.",
        "Aller vers une analyse approfondie : définir des critères "
        "d'atypie (hausse mensuelle, taux dégradé, actes par jour...) et "
        "les regrouper dans un score pédagogique sur 20.",
        "Le score pédagogique classe les professionnels : 8 à contrôler "
        "(score ≥ 12) et 28 à accompagner (score de 5 à 11). C'est une "
        "aide à la décision, pas une preuve de fraude : la décision reste "
        "humaine.",
        images=[
            ("images/powerbi_1.png", "Dashboard Power BI - Vue 1"),
            ("images/powerbi_2.png", "Dashboard Power BI - Vue 2"),
            ("images/powerbi_3.png", "Dashboard Power BI - Vue 3"),
            ("images/powerbi_4.png", "Dashboard Power BI - Vue 4"),
        ],
        prefixe="powerbi",
        extra=bouton_rapport
    )

    section(
        6,
        "Dashboard Streamlit",
        "Un outil interactif d'aide à la décision",
        "Donner aux équipes un outil interactif d'aide à la décision.",
        "Choisir un groupe puis un professionnel, le comparer à sa "
        "catégorie et étudier les alertes.",
        "Streamlit sert de couche de restitution : il lit les données et "
        "réagit aux choix de l'utilisateur.",
        images=[
            ("images/dashboard_1.png", "Dashboard Streamlit"),
            ("images/dashboard_3.png", "Analyse approfondie de l'activité du professionnel choisi"),
            ("images/dashboard_2.png", "Étude approfondie des alertes"),
            ("images/codage_python.png", "Explication du codage : Streamlit"),
        ],
        prefixe="dashboard"
    )

    section(
        7,
        "Automatisation : un nouveau département ajouté",
        "Un nouveau département ajouté automatiquement au dashboard",
        "Intégrer un nouveau département avec le minimum d'actions manuelles.",
        "Faire dialoguer SQL, fichiers CSV, API locale et Streamlit sans "
        "modifier le code du tableau de bord. Traitement local uniquement "
        "(RGPD).",
        "Enchaîner requête SQL, fichiers CSV, API FastAPI et Streamlit, "
        "avec un pop-up de mise à jour (exemple : département 98).",
        images=[
            ("images/mise_en_situation_1.png", "Mise en situation : un nouveau département ajouté"),
            ("images/mise_en_situation_2.png", "Mise à jour automatique de l'API"),
            ("images/mise_en_situation_3.png", "Mise à jour automatique du Streamlit avec un pop-up"),
            ("images/mise_en_situation_4.png", "Résultat : le département 98 est intégré à l'analyse"),
            ("images/codage_api.png", "Explication du codage : API"),
            ("images/recap_automatisation.png", "Récapitulatif de l'automatisation"),
        ],
        prefixe="auto"
    )

    section(
        8,
        "Machine Learning : Isolation Forest",
        "Des profils atypiques que le score métier n'a pas ciblés",
        "Faire ressortir des professionnels atypiques que le score métier "
        "n'a pas ciblés.",
        "Choisir la contamination : j'ai comparé « auto » et 0,05, et "
        "retenu « auto » pour sa stabilité (92 % contre 88 %).",
        "Un modèle non supervisé n'a pas de bonne réponse : on vérifie la "
        "distribution des scores et la stabilité. Le ML complète la revue "
        "humaine sans la remplacer.",
        images=[
            ("images/machine_learning1.png", "Machine Learning - Isolation Forest"),
            ("images/machine_learning2.png", "Machine Learning - Distribution des scores"),
            ("images/machine_learning2bis.png", "Machine Learning - Vérification"),
            ("images/machine_learning3.png", "Machine Learning - Intégration Streamlit"),
            ("images/machine_learning4.png", "Machine Learning - Codage"),
            ("images/machine_learning5.png", "Machine Learning - Fonctionnement Isolation Forest"),
            ("images/machine_learning6.png", "Machine Learning - Explication du codage"),
        ],
        prefixe="ml",
        extra=chiffres_ml
    )

    st.header("Compétences mobilisées")

    st.image(
        "images/competences.png",
        use_container_width=True
    )


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
