import os
import random
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st

try:
    st.set_page_config(page_title="CPAM du Val-de-Lys - Portfolio Data Analyst", layout="wide")
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
div[data-testid="stColumn"]:first-child div[data-testid="stImage"] img { background:#FFFFFF; border:none; padding:6px; }
.stDownloadButton > button { width:100%; background:#15152B; border:1px solid #7437B8; border-radius:20px; padding:22px 24px; }
.stDownloadButton > button:hover { background:#2A1745; border-color:#E72DE5; }
.stDownloadButton > button p { color:#E75BFF !important; font-size:20px; font-weight:800; }

.carte { background:#15152B; border:1px solid #7437B8; border-radius:20px; padding:18px 24px; margin:8px 0; }
.carte h3 { color:#E75BFF !important; margin-top:0; }
.carte li { margin:4px 0; }
.kpi { background:#15152B; border:1px solid #7437B8; border-radius:20px; padding:18px 10px; text-align:center; height:100%; }
.kpi .val { font-size:36px; font-weight:800; color:#E75BFF; line-height:1.1; }
.kpi .lib { font-size:15px; color:#EAE6F3; margin-top:6px; }
.probleme { background:#2A1745; border-left:6px solid #E72DE5; border-radius:14px; padding:22px 26px; margin:14px 0;
            font-size:24px; font-weight:700; color:#FFFFFF; line-height:1.4; }
.badge { display:inline-block; background:#2A1745; border:1px solid #7437B8; border-radius:999px;
         padding:5px 13px; margin:4px 6px 4px 0; font-size:14px; }
.couche { border-radius:20px; padding:18px 20px; height:100%; background:#15152B; }
.couche .nom { font-size:26px; font-weight:800; }
.couche .sous { font-size:15px; color:#BFB6D6; margin-bottom:10px; }
.fleche { font-size:40px; text-align:center; color:#E75BFF; padding-top:70px; }
.gros { font-size:44px; font-weight:800; color:#FFFFFF; line-height:1.1; }
.ind { display:flex; justify-content:space-between; border-bottom:1px solid #2A1745; padding:7px 0; font-size:15px; }
.ind .haut { color:#E75BFF; font-weight:700; }

/* boutons de choix (étapes, cas) */
div[data-testid="stButtonGroup"] button { background:#15152B !important; border:1px solid #7437B8 !important; }
div[data-testid="stButtonGroup"] button p { color:#EAE6F3 !important; }
div[data-testid="stButtonGroup"] button:hover { background:#2A1745 !important; }
div[data-testid="stButtonGroup"] button[kind$="Active"], div[data-testid="stButtonGroup"] button[aria-checked="true"] {
        background:#C03CFF !important; border-color:#C03CFF !important; }
div[data-testid="stButtonGroup"] button[kind$="Active"] p, div[data-testid="stButtonGroup"] button[aria-checked="true"] p {
        color:#FFFFFF !important; }
/* bouton "Voir un autre exemple" */
.stButton > button { background:#15152B; border:1px solid #7437B8; color:#EAE6F3; }
.stButton > button:hover { background:#2A1745; border-color:#E72DE5; color:#FFFFFF; }
/* volets dépliables */
div[data-testid="stExpander"] details { background:#15152B; border:1px solid #7437B8; border-radius:14px; }
div[data-testid="stExpander"] summary, div[data-testid="stExpander"] details[open] summary { background:#15152B !important; }
div[data-testid="stExpander"] summary:hover { background:#2A1745 !important; }
div[data-testid="stExpander"] summary * { color:#EAE6F3 !important; }
/* listes déroulantes */
div[data-testid="stSelectbox"] div[role="group"] { background:#15152B !important; border:1px solid #7437B8 !important; }
div[data-testid="stSelectbox"] input, div[data-testid="stSelectbox"] svg { color:#EAE6F3 !important; fill:#EAE6F3 !important; }
[role="listbox"] { background:#15152B !important; border:1px solid #7437B8 !important; }
[role="option"] { background:#15152B !important; color:#EAE6F3 !important; }
[role="option"]:hover, [role="option"][data-focused="true"] { background:#2A1745 !important; }
div[data-baseweb="select"] > div { background:#15152B !important; border-color:#7437B8 !important; }
div[data-baseweb="select"] * { color:#EAE6F3 !important; }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li { background:#15152B !important; color:#EAE6F3 !important; }
div[data-baseweb="popover"] li:hover { background:#2A1745 !important; }
/* blocs de code */
div[data-testid="stCode"] pre, div[data-testid="stCode"] code { background:#0F0F1F !important; }
/* puces de choix (tables) */
button[data-testid^="stBaseButton-pills"] { background:#15152B !important; border:1px solid #7437B8 !important; }
button[data-testid^="stBaseButton-pills"] p { color:#EAE6F3 !important; }
button[data-testid="stBaseButton-pillsActive"] { background:#C03CFF !important; border-color:#C03CFF !important; }
button[data-testid="stBaseButton-pillsActive"] p { color:#FFFFFF !important; }
.stButton > button:disabled { opacity:.45; }
div[class*="st-key-etape_"] button { height:110px; border-radius:20px; border:2px solid #7437B8; background:#15152B; }
div[class*="st-key-etape_"] button p { font-size:26px !important; font-weight:800; color:#FFFFFF !important; }
div[class*="st-key-etape_"] button:hover { background:#2A1745; border-color:#E72DE5; }
code { background:#2A1745 !important; color:#EAE6F3 !important; }
.message { border-radius:14px; padding:14px 18px; margin:10px 0; border:1px solid; }
</style>
""", unsafe_allow_html=True)


# chemins relatifs au fichier : fonctionne en local et sur GitHub / Streamlit Cloud
BASE_DIR = Path(__file__).resolve().parent
FICHIER_DONNEES = BASE_DIR / "scores_anonymes.csv"
LOGO = BASE_DIR / "logo_cpam_valdulys.png"
RAPPORT = BASE_DIR / "rapport_final_atypies.pdf"
MODELE = BASE_DIR / "modele_etoile_powerbi.png"
DASHBOARD = BASE_DIR / "dashboard_powerbi.png"


def style_graphe(graphe):
    return graphe.configure(background="#15152B").configure_axis(
        labelColor="#EAE6F3", titleColor="#EAE6F3", gridColor="#2A1745", domainColor="#5B367D"
    ).configure_view(stroke=None)


def message(texte, coul):
    st.markdown(f'<div class="message" style="border-color:{coul};background:{coul}1F">{texte}</div>',
                unsafe_allow_html=True)


def carte(html):
    st.markdown(f'<div class="carte">{html}</div>', unsafe_allow_html=True)


def kpis(liste):
    colonnes = st.columns(len(liste))
    for col, (valeur, libelle) in zip(colonnes, liste):
        col.markdown(f'<div class="kpi"><div class="val">{valeur}</div><div class="lib">{libelle}</div></div>',
                     unsafe_allow_html=True)


def choix_bouton(libelle, options, cle):
    if hasattr(st, "segmented_control"):
        choix = st.segmented_control(libelle, options, default=options[0], key=cle, label_visibility="collapsed")
    else:
        choix = st.radio(libelle, options, horizontal=True, key=cle, label_visibility="collapsed")
    return choix or options[0]


def fr(x, n=1):
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


# en-tête : logo et titre
col_logo, col_titre = st.columns([1, 3], vertical_alignment="center")
with col_logo:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
with col_titre:
    st.markdown('<div style="font-size:40px;font-weight:800;color:#FFFFFF;line-height:1.15">'
                'Projet fil rouge : CPAM du Val-de-Lys</div>'
                '<div style="color:#BFB6D6;margin-top:6px">Formation Data Analyst - Guardia School - '
                'caisse primaire et données fictives</div>', unsafe_allow_html=True)
st.write("")

onglets = st.tabs(["Le projet", "Les données", "Le parcours", "Est-ce le hasard ?", "Compétences mobilisées"])

# ======================================================================== 1. LE PROJET
with onglets[0]:
    kpis([("620", "collaborateurs"), ("1,12 million", "d’assurés"), ("18 600", "professionnels de santé")])
    st.write("")
    gauche, droite = st.columns(2)
    with gauche:
        carte("<h3>Le contexte</h3>"
              "<p>Chaque année, des contrôles nationaux visent certaines catégories de professionnels de santé.</p>"
              "<p>La direction veut s’y préparer :</p>"
              "<ul><li><b>contrôler</b> les professionnels les plus atypiques,</li>"
              "<li><b>accompagner</b> les autres,</li>"
              "<li>et ainsi limiter les dérives de facturation avant l’arrivée des contrôles.</li></ul>")
    with droite:
        carte("<h3>Mon rôle : Data Analyst</h3>"
              "<p>Cadrer le projet en méthode Agile, analyser les données, construire un dashboard Power BI "
              "et rédiger un rapport pour la direction.</p>"
              "<p>Au fil des demandes, le projet s’est enrichi : une application Streamlit, une API, "
              "puis une brique de Machine Learning.</p>")

    st.markdown('<div class="probleme">Comment identifier les atypies de facturation des professionnels de santé '
                'afin de prioriser ceux à contrôler ou à accompagner ?</div>', unsafe_allow_html=True)

    st.markdown("### 5 livrables en 14 semaines")
    kpis([("1", "Socle de données"), ("2", "Power BI et rapport"), ("3", "Streamlit"),
          ("4", "API locale"), ("5", "Machine Learning")])
    st.write("")
    carte("<p style='font-size:20px;text-align:center;margin:0'><b>Un outil au service de l’accompagnement "
          "et d’aide à la facturation.</b></p>")

# ======================================================================== 2. LES DONNÉES
with onglets[1]:
    st.markdown("## L’architecture médaillon")
    st.write("Les données passent par trois niveaux, du fichier brut à la table prête à l’analyse.")
    c1, f1, c2, f2, c3 = st.columns([5, 1, 5, 1, 5])
    for col, nom, coul, sous, lignes in [
        (c1, "Bronze", "#CD7F32", "Données brutes",
         ["20 fichiers reçus", "Formats différents : CSV, TXT, JSON", "Valeurs manquantes, doublons"]),
        (c2, "Silver", "#C9CCD6", "Données nettoyées",
         ["Nettoyage avec Pandas", "Dictionnaire de données", "Tables reliées dans MySQL"]),
        (c3, "Gold", "#D4AF37", "Données prêtes à l’analyse",
         ["1 ligne = 1 professionnel", "Indicateurs et score pédagogique", "Exportée de Power BI, utilisée par "
                                                                            "Streamlit et le Machine Learning"]),
    ]:
        items = "".join(f"<li>{x}</li>" for x in lignes)
        col.markdown(f'<div class="couche" style="border:2px solid {coul}">'
                     f'<div class="nom" style="color:{coul}">{nom}</div><div class="sous">{sous}</div>'
                     f'<ul>{items}</ul></div>', unsafe_allow_html=True)
    f1.markdown('<div class="fleche">→</div>', unsafe_allow_html=True)
    f2.markdown('<div class="fleche">→</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### La granularité : ce que représente une ligne")
    g1, g2, g3 = st.columns([5, 2, 5])
    g1.markdown('<div class="carte" style="text-align:center"><div style="color:#BFB6D6">Ce que j’avais</div>'
                '<div class="gros">15 805</div><div>lignes</div>'
                '<div style="margin-top:8px"><b>1 ligne = 1 remboursement</b>, le niveau le plus fin</div></div>',
                unsafe_allow_html=True)
    g2.markdown('<div class="fleche" style="padding-top:40px">→<div style="font-size:15px;color:#EAE6F3">'
                'agrégation par professionnel</div></div>', unsafe_allow_html=True)
    g3.markdown('<div class="carte" style="text-align:center;border-color:#D4AF37">'
                '<div style="color:#BFB6D6">Ce dont j’avais besoin</div>'
                '<div class="gros">750</div><div>lignes</div>'
                '<div style="margin-top:8px"><b>1 ligne = 1 professionnel</b> : la table gold</div></div>',
                unsafe_allow_html=True)

    st.markdown("### 20 tables reçues → 9 retenues")
# ---------------------------------------------------------------- données anonymes (communes aux onglets)
@st.cache_data
def charger():
    df = pd.read_csv(FICHIER_DONNEES, sep=";")
    return df


# ======================================================================== 3. LE PARCOURS


def etape_powerbi():
    st.markdown("#### Le modèle de données")
    if MODELE.exists():
        st.image(str(MODELE), use_container_width=True)
    st.markdown("#### Le dashboard Power BI")
    if DASHBOARD.exists():
        st.image(str(DASHBOARD), use_container_width=True)


def etape_streamlit(df):
    st.markdown("#### Une fiche par professionnel, comparée à sa catégorie")
    cibles = df[df["orientation"] != "Non ciblé"].sort_values("score_pedagogique", ascending=False).reset_index(drop=True)
    onglet = choix_bouton("Onglet", ["À contrôler", "À accompagner"], "onglet_demo")
    liste = cibles[cibles["orientation"] == onglet].reset_index(drop=True)
    libelles = [f"Professionnel {i + 1} - {r.categorie}" for i, r in liste.iterrows()]
    pick = st.selectbox("Sélectionner un professionnel", libelles, key=f"sel_{onglet}")
    ex = liste.iloc[libelles.index(pick)]
    kpis([(fr(ex["score_pedagogique"]) + " / 20", "score pédagogique"), (ex["orientation"], "orientation"),
          (ex["categorie"], "catégorie"), (str(int((df["categorie"] == ex["categorie"]).sum())), "professionnels comparables")])
    st.write("")
    meme = df[df["categorie"] == ex["categorie"]]
    lignes = []
    for c, lib in [("taux_degrade_moyen", "Taux dégradé (%)"), ("taux_rejet_moyen", "Taux de rejet (%)"),
                   ("nb_actes_jour_moyen", "Actes par jour")]:
        k = 100 if "taux" in c else 1
        lignes += [{"Indicateur": lib, "Qui": "Ce professionnel", "Valeur": ex[c] * k},
                   {"Indicateur": lib, "Qui": f"Médiane des {ex['categorie'].lower()}s", "Valeur": meme[c].median() * k}]
    comp = pd.DataFrame(lignes)
    graphe = alt.Chart(comp).mark_bar(cornerRadiusEnd=4).encode(
        y=alt.Y("Qui:N", title=None, axis=alt.Axis(labels=False, ticks=False)),
        x=alt.X("Valeur:Q", title=None),
        color=alt.Color("Qui:N", scale=alt.Scale(range=["#E72DE5", "#6B6F7A"]),
                        legend=alt.Legend(orient="top", title=None, labelColor="#EAE6F3")),
        row=alt.Row("Indicateur:N", title=None, header=alt.Header(labelColor="#EAE6F3", labelAngle=0, labelAlign="left")),
        tooltip=["Qui:N", alt.Tooltip("Valeur:Q", format=".2f")]
    ).resolve_scale(x="independent").properties(height=55, width=700)
    st.altair_chart(style_graphe(graphe), use_container_width=False)


def etape_api():
    st.markdown("#### La direction souhaite intégrer un nouveau département sans modifier le code : "
                "c’est le rôle de l’API")
    st.caption("Une API, c’est un guichet entre deux programmes : on pose une question, elle répond. "
               "GET sert à lire, POST sert à agir.")
    st.markdown("#### Essayez : un nouveau département arrive")
    etat = st.session_state.setdefault("api_etape", 0)

    def aller(n):
        st.session_state["api_etape"] = n

    a, b, c = st.columns(3)
    a.button("1. Déposer les fichiers du 98", use_container_width=True, on_click=aller, args=(1,), disabled=etat >= 1)
    b.button("2. GET /nouvelles-donnees", use_container_width=True, on_click=aller, args=(2,), disabled=etat != 1)
    c.button("3. POST /mise-a-jour/98", use_container_width=True, on_click=aller, args=(3,), disabled=etat != 2)
    if etat == 1:
        message("Les 4 fichiers du département 98 sont dans le dossier surveillé. L’API ne les a pas encore lus.", "#5BC0EB")
    if etat == 2:
        st.code('{"departement": "98", "nouveaux_professionnels": 30}', language="json")
        message("Dans le Streamlit : nouvelles données disponibles pour le département 98, "
                "avec 30 nouveaux professionnels. Bouton « Mettre à jour les données ».", "#F2B84B")
    if etat >= 3:
        message("Mise à jour effectuée - 780 professionnels disponibles", "#49CC90")
    pro, ctrl = ("780", "16") if etat >= 3 else ("750", "12")
    kpis([(pro, "professionnels dans le Streamlit"), (ctrl, "à contrôler"), ("0", "ligne de code modifiée")])
    if etat:
        st.button("Recommencer", key="api_reset", on_click=aller, args=(0,))


def isoler(points, cible, rng):
    # coupes au hasard jusqu'à isoler le point cible, comme un arbre d'Isolation Forest
    x0, x1, y0, y1 = 0.0, 10.0, 0.0, 10.0
    reste = list(range(len(points)))
    coupes = []
    while len(reste) > 1 and len(coupes) < 30:
        axe = rng.choice(["x", "y"])
        vals = [points[i][0 if axe == "x" else 1] for i in reste]
        v = rng.uniform(min(vals), max(vals))
        if axe == "x":
            coupes.append(dict(x=v, x2=v, y=y0, y2=y1))
            if points[cible][0] < v:
                x1 = v
            else:
                x0 = v
        else:
            coupes.append(dict(x=x0, x2=x1, y=v, y2=v))
            if points[cible][1] < v:
                y1 = v
            else:
                y0 = v
        reste = [i for i in reste if x0 <= points[i][0] <= x1 and y0 <= points[i][1] <= y1]
    return coupes, (x0, x1, y0, y1)


def etape_ml():
    st.markdown("#### Comment l’Isolation Forest repère un profil atypique")
    st.write("Le modèle coupe les données au hasard, encore et encore. Un profil atypique se retrouve seul "
             "en quelques coupes. Un profil habituel, noyé dans la foule, en demande beaucoup plus.")
    rng0 = random.Random(3)
    points = [(min(9.7, max(0.3, rng0.gauss(5, 1.1))), min(9.7, max(0.3, rng0.gauss(5.5, 1.1)))) for _ in range(70)]
    points.append((9.2, 1.0))
    atyp = len(points) - 1
    habituel = min(range(len(points) - 1), key=lambda i: (points[i][0] - 5) ** 2 + (points[i][1] - 5.5) ** 2)

    choix = choix_bouton("Profil", ["Profil atypique", "Profil habituel"], "profil_if")
    graine = st.session_state.setdefault("graine_if", 1)
    cible = atyp if choix == "Profil atypique" else habituel
    coupes, boite = isoler(points, cible, random.Random(graine + (0 if cible == atyp else 100)))

    cle_n = f"n_{choix}_{graine}"
    st.session_state.setdefault(cle_n, 0)
    b1, b2, _ = st.columns([1, 1, 3])
    b1.button("Faire une coupe", use_container_width=True, disabled=st.session_state[cle_n] >= len(coupes),
              on_click=lambda: st.session_state.update({cle_n: st.session_state[cle_n] + 1}))
    b2.button("Tout couper", use_container_width=True,
              on_click=lambda: st.session_state.update({cle_n: len(coupes)}))
    n = st.session_state[cle_n]
    pts = pd.DataFrame([{"x": p[0], "y": p[1], "role": "Profil suivi" if i == cible else "Autres"}
                        for i, p in enumerate(points)])
    nuage = alt.Chart(pts).mark_circle(size=90).encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, 10]), title="Indicateur 1", axis=alt.Axis(labels=False)),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 10]), title="Indicateur 2", axis=alt.Axis(labels=False)),
        color=alt.Color("role:N", scale=alt.Scale(domain=["Profil suivi", "Autres"], range=["#E72DE5", "#8A8FA0"]),
                        legend=alt.Legend(orient="top", title=None, labelColor="#EAE6F3")),
        size=alt.condition(alt.datum.role == "Profil suivi", alt.value(220), alt.value(70)))
    couches = [nuage]
    if n:
        traits = pd.DataFrame(coupes[:n])
        couches.append(alt.Chart(traits).mark_rule(color="#5BC0EB", strokeWidth=2).encode(
            x="x:Q", x2="x2:Q", y="y:Q", y2="y2:Q"))
        if n >= len(coupes):
            x0, x1, y0, y1 = boite
            couches.append(alt.Chart(pd.DataFrame([dict(x=x0, x2=x1, y=y0, y2=y1)])).mark_rect(
                color="#E72DE5", opacity=0.18).encode(x="x:Q", x2="x2:Q", y="y:Q", y2="y2:Q"))
    g, d = st.columns([3, 2])
    with g:
        st.altair_chart(style_graphe(alt.layer(*couches).properties(height=380)), use_container_width=True)
    with d:
        fini = n >= len(coupes)
        st.markdown(f'<div class="kpi" style="margin-top:30px"><div class="val">{n}</div>'
                    f'<div class="lib">{"coupes : profil isolé !" if fini else "coupes pour l’instant"}</div></div>',
                    unsafe_allow_html=True)
        st.write("")
        if not fini:
            carte("<p>Cliquez sur « Faire une coupe » jusqu’à ce que le profil rose soit seul dans sa case.</p>")
        elif choix == "Profil atypique":
            carte("<p>Isolé en <b>très peu de coupes</b> : il ne ressemble à aucun autre. "
                  "Son score d’anomalie sera élevé.</p>")
        else:
            carte("<p>Il faut <b>beaucoup de coupes</b> pour le séparer de ses voisins : "
                  "c’est un profil habituel. Son score d’anomalie sera bas.</p>")
        st.button("Refaire les coupes au hasard", use_container_width=True,
                  on_click=lambda: st.session_state.update(graine_if=graine + 1))
    st.caption("Le vrai modèle répète l’opération sur 100 arbres et 9 indicateurs, puis fait la moyenne : "
               "c’est le score d’anomalie. Pas besoin de données étiquetées : on parle de modèle non supervisé.")


with onglets[2]:
    st.markdown("## Le parcours, étape par étape")
    st.caption("Cliquez sur une étape.")
    ETAPES = ["Power BI", "Streamlit", "API", "Machine Learning"]
    etape = st.session_state.get("etape_choisie")
    cols = st.columns(4)
    for col, nom in zip(cols, ETAPES):
        col.button(nom, key=f"etape_{ETAPES.index(nom)}", use_container_width=True,
                   on_click=lambda n=nom: st.session_state.update(etape_choisie=n))
    if etape:
        st.markdown(f"<style>.st-key-etape_{ETAPES.index(etape)} button {{ background:#C03CFF !important; "
                    f"border-color:#C03CFF !important; }}</style>", unsafe_allow_html=True)
    st.write("")
    if etape is None:
        pass
    elif etape == "Power BI":
        etape_powerbi()
    elif etape == "Streamlit" and not FICHIER_DONNEES.exists():
        st.warning(f"Fichier introuvable : {FICHIER_DONNEES.name} doit être à côté de cpamportfofo_app.py.")
    elif etape == "Streamlit":
        etape_streamlit(charger())
    elif etape == "API":
        etape_api()
    else:
        etape_ml()

# ======================================================================== 4. EST-CE LE HASARD ?
with onglets[3]:
    st.markdown("## Est-ce le hasard ?")
    st.write("Le score pédagogique cible 34 professionnels. Le Machine Learning, qui ne connaît pas les règles "
             "de la direction, en signale 51. Et 18 sont repérés par les deux. Est-ce une coïncidence ?")
    kpis([("34", "ciblés par le score pédagogique"), ("51", "signalés par le Machine Learning"),
          ("18", "repérés par les deux")])
    st.write("")
    st.markdown("#### Essayez : tirez 34 professionnels au hasard, dans l’ordre 1, 2, 3")
    tirages = st.session_state.setdefault("tirages", [])
    etape_h = st.session_state.setdefault("etape_hasard", 0)

    def tirer(n, etape):
        for _ in range(n):
            # 750 professionnels, dont 51 signalés par le ML : combien parmi 34 tirés au hasard ?
            tirages.append(sum(1 for i in random.sample(range(750), 34) if i < 51))
        st.session_state["etape_hasard"] = etape

    def effacer():
        st.session_state["tirages"] = []
        st.session_state["etape_hasard"] = 0

    b1, b2, b3 = st.columns(3)
    b1.button("1. Tirer une fois", use_container_width=True, on_click=tirer, args=(1, 1), disabled=etape_h != 0)
    b2.button("2. Tirer 1 000 fois", use_container_width=True, on_click=tirer, args=(1000, 2), disabled=etape_h != 1)
    b3.button("3. Effacer", use_container_width=True, on_click=effacer, disabled=etape_h != 2)

    if etape_h == 1:
        _, d = st.columns([3, 2])
        with d:
            st.markdown(f'<div class="kpi"><div class="val">{tirages[-1]}</div>'
                        f'<div class="lib">en commun avec le Machine Learning, pour ce tirage au hasard</div></div>',
                        unsafe_allow_html=True)
            st.caption("Un seul tirage ne suffit pas : passez à l’étape 2.")
    elif etape_h == 2:
        g, d = st.columns([3, 2])
        with g:
            compte = pd.Series(tirages).value_counts().reindex(range(0, 21), fill_value=0)
            hist = pd.DataFrame({"en_commun": compte.index, "tirages": compte.values})
            barres = alt.Chart(hist).mark_bar(color="#7437B8", cornerRadiusEnd=3).encode(
                x=alt.X("en_commun:O", title="Professionnels en commun avec le Machine Learning",
                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("tirages:Q", title="Nombre de tirages"),
                tooltip=[alt.Tooltip("en_commun:O", title="En commun"), alt.Tooltip("tirages:Q", title="Tirages")])
            reel = alt.Chart(pd.DataFrame({"en_commun": [18], "texte": ["Résultat réel : 18"]}))
            trait = reel.mark_rule(color="#E72DE5", strokeWidth=3).encode(x="en_commun:O")
            etiquette = reel.mark_text(color="#E72DE5", dy=-8, fontSize=14, fontWeight="bold", align="right",
                                       dx=-6).encode(x="en_commun:O", y=alt.value(12), text="texte:N")
            st.altair_chart(style_graphe((barres + trait + etiquette).properties(height=340)),
                            use_container_width=True)
        with d:
            st.markdown(f'<div class="kpi"><div class="val">{fr(sum(tirages) / len(tirages))}</div>'
                        f'<div class="lib">en commun en moyenne au hasard, sur {len(tirages)} tirages '
                        f'(maximum : {max(tirages)})</div></div>', unsafe_allow_html=True)
            st.write("")
            st.markdown('<div class="kpi" style="border:2px solid #E72DE5"><div class="val">18 sur 34</div>'
                        '<div class="lib">retrouvés par le Machine Learning : bien plus que le hasard. '
                        '<b>Ce n’est pas une coïncidence.</b></div></div>', unsafe_allow_html=True)

# ======================================================================== 5. COMPÉTENCES
COMPETENCES = [
    ("Données", "Python, Pandas, NumPy, analyse, qualité des données"),
    ("Modélisation", "Dictionnaire de données, MCD, SQL, MySQL"),
    ("Datavisualisation", "Power BI, DAX, KPI, analyse d’atypies"),
    ("Projet", "Kanban, Agile, organisation, restitution"),
    ("Automatisation", "Streamlit, API, Machine Learning : Isolation Forest"),
]

with onglets[4]:
    st.markdown("## Compétences mobilisées")
    colonnes = st.columns(len(COMPETENCES))
    for col, (titre, detail) in zip(colonnes, COMPETENCES):
        col.markdown(f'<div class="kpi" style="text-align:left;padding:18px">'
                     f'<div style="font-size:19px;font-weight:800;color:#E75BFF">{titre}</div>'
                     f'<div style="margin-top:8px">{detail}</div></div>', unsafe_allow_html=True)
    st.write("")
    if RAPPORT.exists():
        with open(RAPPORT, "rb") as rapport:
            st.download_button("Télécharger le rapport d'analyse", rapport.read(),
                               file_name="rapport_final_atypies.pdf", mime="application/pdf",
                               use_container_width=True)

st.caption("Formation Data Analyst - Guardia School - CPAM fictive")