from scipy import stats

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

try:
    st.set_page_config(
        page_title="Zeloria - État des lieux",
        layout="wide"
    )
except st.errors.StreamlitAPIException:
    pass

# Palette
ROSE = "#E67AA3"
MENTHE = "#4DBF98"
LAVANDE = "#A98BE0"


#  STYLE

st.markdown("""
<style>

.stApp {
    background: #0E1117;
}

h1, h2, h3, p, li, label, span, div[data-testid="stMetricValue"],
div[data-testid="stMetricLabel"], div[data-testid="stHeading"] *,
div[data-testid="stSlider"] *, div[data-testid="stToggle"] * {
    color: #EAE6F3;
}

.stButton > button {
    background: #E67AA3;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 8px 18px;
}

.stButton > button:hover {
    background: #D4608D;
    color: #FFFFFF;
}

.stButton > button p {
    color: #FFFFFF;
}

.titre-zeloria {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    margin-bottom: 0;
    color: #E67AA3;
}

.sous-titre {
    text-align: center;
    font-size: 22px;
    color: #A98BE0;
    margin-bottom: 30px;
}

.carte {
    padding: 20px 26px;
    border-radius: 22px;
    margin-bottom: 18px;
    font-size: 18px;
    line-height: 1.6;
    color: #EAE6F3;
}

.carte-histoire {
    background: #3A2030;
    border: 2px solid #E67AA3;
}

.carte-question {
    background: #2A2145;
    border: 2px solid #A98BE0;
}

.carte-verdict {
    background: #163529;
    border: 2px solid #4DBF98;
}

.pastille {
    display: inline-block;
    background: #2A2145;
    color: #EAE6F3;
    font-size: 13px;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 999px;
}

.ticket {
    background: #1A1F2B;
    border: 2px solid #E67AA3;
    border-radius: 14px;
    padding: 10px 14px;
    margin-bottom: 10px;
    font-size: 15px;
    line-height: 1.4;
    color: #EAE6F3;
}

.ticket small {
    color: #A98BE0;
    font-weight: 700;
}

.etiquette {
    font-weight: 800;
    font-size: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

div[data-testid="stMetric"] {
    background: #1A1F2B;
    border: 2px solid #E67AA3;
    padding: 16px;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)


#  DONNEES

donnees = pd.read_csv("zeloria.csv", sep=";", parse_dates=["date"])
ventes = donnees[donnees["type"] == "vente"].sort_values("date").reset_index(drop=True)
bugs = donnees[donnees["type"] == "bug"].copy()
enquetes = donnees[donnees["type"] == "enquete"].copy()
budget = donnees[donnees["type"] == "budget"]

DEBUT_TEST = pd.Timestamp("2026-06-01")
LANCEMENT = pd.Timestamp("2026-09-01")


def espaces(nombre):
    return f"{nombre:,.0f}".replace(",", " ")


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

MOIS_COURT = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
              "août", "sept.", "oct.", "nov.", "déc."]

LABEL_JOUR = (
    "timeFormat(datum.value, '%d') + ' ' + "
    "['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.']"
    "[month(datum.value)]"
)

LABEL_MOIS_ANNEE = (
    "['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.']"
    "[month(datum.value)] + ' ' + timeFormat(datum.value, '%Y')"
)

LABEL_EUROS = "replace(format(datum.value, ',d'), /,/g, ' ')"


def date_fr(d):
    return f"{d.day} {MOIS_COURT[d.month - 1]} {d.year}"


def style_graphique(graphique):
    return (
        graphique
        .configure(background="#151922")
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor="#EAE6F3", titleColor="#EAE6F3", gridColor="#2C3340")
        .configure_legend(labelColor="#EAE6F3", titleColor="#EAE6F3")
    )


def virgule(nombre, decimales=1):
    return f"{nombre:.{decimales}f}".replace(".", ",")


# le sujet avec son déterminant : "la connexion", "le son", "les menus"
AVEC_ARTICLE = {
    "performance": "la performance",
    "son": "le son",
    "récompenses": "les récompenses",
    "connexion": "la connexion",
    "menus": "les menus",
    "boutique": "la boutique",
    "affichage": "l'affichage",
}


def liste(sujets):
    mots = [AVEC_ARTICLE[sujet] for sujet in sujets]
    if len(mots) <= 1:
        return "".join(mots)
    return ", ".join(mots[:-1]) + " et " + mots[-1]


#  HISTOIRE ET PROBLEMATIQUE

st.markdown('<div class="titre-zeloria">Zeloria</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sous-titre">Studio Zelleik</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="carte carte-histoire">
<div class="etiquette">L'histoire</div>
Zeloria est un jeu free-to-play de type gacha, créé par le studio Zelleik.
On y collectionne, on élève et on soigne des petites créatures. C'est un jeu « pay to progress » : on peut payer pour progresser plus
vite ou personnaliser ses créatures, mais pas pour gagner plus facilement. De juin à août 2026, un groupe de joueurs sélectionnés a testé le jeu.
Leurs remarques ont servi à corriger les bugs. Le lancement officiel a eu
lieu le 1er septembre 2026 : les joueurs pré-inscrits recevaient un cadeau s'ils lançaient le
jeu le jour de sa sortie.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="carte carte-question">
<div class="etiquette">La problématique</div>
Six semaines après le lancement, Zeloria est-il rentable ? Et que reste-t-il à améliorer pour
qu'il soit amorti le plus rapidement possible ?
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<span class="pastille">Données fictives</span>',
    unsafe_allow_html=True
)

st.divider()


#  1. LE TEST

st.header("1. Le test de juin à août 2026")

TEST = ["Test - juin", "Test - juillet", "Test - août"]
LANCE = ["Lancement - septembre", "Lancement - octobre"]

moyennes = enquetes.groupby("enquete")["note"].mean()

colonnes = st.columns(3)
for colonne, nom in zip(colonnes, TEST):
    colonne.metric(f"Satisfaction - {nom.lower()}", f"{virgule(moyennes[nom], 2)} / 5")

plaintes = enquetes[enquetes["categorie"] != "Rien à changer"]
repondants = enquetes.groupby("enquete").size()


def graphique_plaintes(vagues, couleurs, hauteur=420):
    par_theme = (plaintes[plaintes["enquete"].isin(vagues)]
                 .groupby(["categorie", "enquete"]).size().reset_index(name="plaintes"))
    par_theme["part"] = par_theme["plaintes"] / par_theme["enquete"].map(repondants)
    return (
        alt.Chart(par_theme)
        .mark_bar()
        .encode(
            y=alt.Y("categorie:N", title=None,
                    sort=alt.EncodingSortField("plaintes", op="sum", order="descending")),
            yOffset=alt.YOffset("enquete:N", sort=vagues),
            x=alt.X("part:Q", title="Part des joueurs qui s'en plaignent",
                    axis=alt.Axis(format="%")),
            color=alt.Color("enquete:N", title=None,
                            scale=alt.Scale(domain=vagues, range=couleurs),
                            legend=alt.Legend(orient="bottom")),
            tooltip=[
                alt.Tooltip("categorie:N", title="Sujet"),
                alt.Tooltip("enquete:N", title="Enquête"),
                alt.Tooltip("plaintes:Q", title="Joueurs"),
                alt.Tooltip("part:Q", title="Part des répondants", format=".0%"),
            ],
        )
        .properties(height=hauteur)
    )


st.subheader("Ce que reprochent les testeurs")
st.altair_chart(style_graphique(graphique_plaintes(TEST, ["#D9CCF5", "#B9A0EC", "#8A63D2"], 380)),
                theme=None, use_container_width=True)

par_vague = plaintes.groupby(["categorie", "enquete"]).size().unstack(fill_value=0)
premiers = par_vague[TEST[0]].sort_values(ascending=False).index[:3].str.lower().tolist()
persistent = par_vague[par_vague[TEST[2]] >= par_vague[TEST[0]]].index.str.lower().tolist()

st.markdown(
    f"""
<div class="carte carte-verdict">
La satisfaction des testeurs passe de {virgule(moyennes[TEST[0]], 2)} à {virgule(moyennes[TEST[2]], 2)} sur 5.
En juin, les plaintes portaient surtout sur {liste(premiers)}.
Les plaintes sur {liste(persistent)} ne baissent pas.
</div>
""",
    unsafe_allow_html=True
)


#  2. LE TABLEAU KANBAN

st.divider()

st.header("2. Correction des bugs avec la méthode Kanban")

ORDRE_STATUT = ["Terminé", "En cours", "À faire"]


def libelle_sprint(numero):
    debut = DEBUT_TEST + pd.Timedelta(days=15 * (numero - 1))
    fin = debut + pd.Timedelta(days=14)
    return f"Période {numero} ({debut.day} {MOIS_COURT[debut.month - 1]} - {fin.day} {MOIS_COURT[fin.month - 1]})"


bugs["sprint"] = bugs["sprint"].astype(int)
par_sprint = bugs.groupby(["sprint", "statut"]).size().reset_index(name="tickets")
par_sprint["libelle"] = par_sprint["sprint"].apply(libelle_sprint)

gauche, droite = st.columns([1.2, 1])

with gauche:

    st.subheader("Tickets par période de 15 jours")

    graphique_sprints = (
        alt.Chart(par_sprint)
        .mark_bar()
        .encode(
            x=alt.X("sprint:O", title="Période de 15 jours", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("tickets:Q", title="Nombre de tickets"),
            color=alt.Color("statut:N", title=None,
                            scale=alt.Scale(domain=ORDRE_STATUT, range=[MENTHE, LAVANDE, ROSE]),
                            legend=alt.Legend(orient="bottom")),
            order=alt.Order("statut:N", sort="ascending"),
            tooltip=[
                alt.Tooltip("libelle:N", title="Période"),
                alt.Tooltip("statut:N", title="Colonne"),
                alt.Tooltip("tickets:Q", title="Tickets"),
            ],
        )
        .properties(height=360)
    )
    st.altair_chart(style_graphique(graphique_sprints), theme=None, use_container_width=True)

with droite:

    st.subheader("Tableau Kanban d'une période")

    numeros = sorted(bugs["sprint"].unique())
    choix = st.selectbox("Période", numeros, index=len(numeros) - 1,
                         format_func=libelle_sprint)
    tickets = bugs[bugs["sprint"] == choix]

    colonnes_kanban = st.columns(3)
    for colonne, statut in zip(colonnes_kanban, ["À faire", "En cours", "Terminé"]):
        cartes = tickets[tickets["statut"] == statut]
        html = f'<div class="etiquette">{statut} ({len(cartes)})</div>'
        for _, t in cartes.iterrows():
            html += (f'<div class="ticket"><small>{t["id"]} - {t["gravite"]}</small><br>'
                     f'{t["titre"]}</div>')
        colonne.markdown(html, unsafe_allow_html=True)

termines = int((bugs["statut"] == "Terminé").sum())
restants = bugs[bugs["statut"] != "Terminé"]
sujets_restants = restants["categorie"].value_counts()

st.markdown(
    f"""
<div class="carte carte-verdict">
{termines} tickets sur {len(bugs)} sont terminés.
</div>
""",
    unsafe_allow_html=True
)


#  3. LE LANCEMENT OFFICIEL

st.divider()

st.header("3. Le lancement officiel du 1er septembre")

k1, k2, k3 = st.columns(3)
k1.metric("Téléchargements depuis le lancement", espaces(ventes["telechargements"].sum()))
k2.metric("Pic en une journée", espaces(ventes["telechargements"].max()))
k3.metric("Joueurs actifs (moyenne 30 jours)", espaces(ventes["joueurs_actifs"].tail(30).mean()))

gauche, droite = st.columns(2)

with gauche:
    st.subheader("Nombre de joueurs qui téléchargent le jeu")
    zone_telechargements = st.container()

    pas = st.radio(
        "Regrouper les téléchargements par",
        ["Jour", "Semaine", "Mois"],
        horizontal=True
    )

    debut_periode, fin_periode = st.slider(
        "Période affichée",
        min_value=ventes["date"].min().date(),
        max_value=ventes["date"].max().date(),
        value=(ventes["date"].min().date(), ventes["date"].max().date()),
        format="DD/MM/YYYY"
    )

with droite:
    st.subheader("Ce que reprochent les joueurs après le lancement")
    st.altair_chart(
        style_graphique(graphique_plaintes([TEST[2]] + LANCE, ["#D9CCF5", "#B9A0EC", "#8A63D2"], 340)),
        theme=None, use_container_width=True
    )

with zone_telechargements:

    affiche = ventes[
        (ventes["date"].dt.date >= debut_periode) & (ventes["date"].dt.date <= fin_periode)
    ][["date", "telechargements"]].copy()

    if pas == "Semaine":
        affiche = affiche.resample("W-MON", on="date", label="left", closed="left").sum().reset_index()
        titre_x = "Semaine (date du lundi)"
        label_x = LABEL_JOUR
    elif pas == "Mois":
        affiche = affiche.resample("MS", on="date").sum().reset_index()
        titre_x = "Mois"
        label_x = LABEL_MOIS_ANNEE
    else:
        titre_x = "Jour"
        label_x = LABEL_JOUR

    affiche["libelle"] = affiche["date"].apply(date_fr)
    largeur = max(3, int(480 / max(len(affiche), 1) * 0.8))

    graphique_telechargements = (
        alt.Chart(affiche)
        .mark_bar(color=LAVANDE, size=largeur)
        .encode(
            x=alt.X("date:T", title=titre_x, axis=alt.Axis(labelExpr=label_x, tickCount=7, labelOverlap=True)),
            y=alt.Y("telechargements:Q", title="Nombre de téléchargements",
                    axis=alt.Axis(labelExpr=LABEL_EUROS)),
            tooltip=[
                alt.Tooltip("libelle:N", title=titre_x),
                alt.Tooltip("telechargements:Q", title="Téléchargements"),
            ],
        )
        .properties(height=340)
    )
    st.altair_chart(style_graphique(graphique_telechargements), theme=None, use_container_width=True)

part_aout = par_vague[TEST[2]] / repondants[TEST[2]]
part_oct = par_vague[LANCE[1]] / repondants[LANCE[1]]
evolution = part_oct - part_aout
plus_cites = part_oct.sort_values(ascending=False).index[:2].str.lower().tolist()
ont_baisse = [t.lower() for t in evolution[evolution < -0.015].index if t.lower() not in plus_cites]
ont_monte = [t.lower() for t in evolution[evolution > 0.015].index if t.lower() not in plus_cites]

st.markdown(
    f"""
<div class="carte carte-verdict">
Le lancement attire {espaces(ventes["telechargements"].sum())} joueurs en six semaines, avec un pic de
{espaces(ventes["telechargements"].max())} téléchargements le jour de la sortie. Après les corrections, les plaintes
baissent sur {liste(ont_baisse)}. Elles augmentent sur {liste(ont_monte)}. Les sujets les plus cités
restent {liste(plus_cites)} : ce sont les points à améliorer en priorité.
</div>
""",
    unsafe_allow_html=True
)


#  4. LA RENTABILITE

st.divider()

st.header("4. Rentabilité depuis le lancement")

cout_initial = budget[budget["categorie"] == "Initial"]["montant_euros"].sum()
cout_mensuel = budget[budget["categorie"] == "Mensuel"]["montant_euros"].sum()
cout_jour = cout_mensuel / 30

calendrier = pd.DataFrame({"date": pd.date_range(DEBUT_TEST, ventes["date"].max())})
calendrier = calendrier.merge(ventes[["date", "revenus_euros"]], on="date", how="left").fillna(0)
calendrier["revenus_cumules"] = calendrier["revenus_euros"].cumsum()
calendrier["couts_cumules"] = cout_initial + cout_jour * (calendrier.index + 1)

revenus_total = calendrier["revenus_cumules"].iloc[-1]
couts_total = calendrier["couts_cumules"].iloc[-1]
revenus_30j = ventes["revenus_euros"].tail(30).sum()
couts_30j = cout_jour * 30
marge_30j = revenus_30j - couts_30j
reste = couts_total - revenus_total

m1, m2, m3, m4 = st.columns(4)
m1.metric("Dépenses depuis juin", f"{espaces(couts_total)} €")
m2.metric("Revenus des achats", f"{espaces(revenus_total)} €")
m3.metric("Budget récupéré", f"{revenus_total / couts_total:.0%}")
m4.metric("Gain des 30 derniers jours", f"{espaces(marge_30j)} €")

montrer_suite = st.toggle("Montrer la suite estimée à ce rythme", value=True)

tables = [calendrier[["date", "revenus_cumules", "couts_cumules"]].rename(columns={
    "revenus_cumules": "Revenus cumulés", "couts_cumules": "Coûts cumulés"
}).melt(id_vars="date", var_name="serie", value_name="euros").assign(type="Réel")]

date_amorti = None
if reste > 0 and marge_30j > 0:
    net_jour = marge_30j / 30
    jours_restants = int(reste / net_jour) + 1
    date_amorti = ventes["date"].iloc[-1] + pd.Timedelta(days=jours_restants)
    if montrer_suite:
        suite = pd.DataFrame({"date": pd.date_range(ventes["date"].iloc[-1], date_amorti)})
        k = (suite["date"] - ventes["date"].iloc[-1]).dt.days
        suite["Revenus cumulés"] = revenus_total + (revenus_30j / 30) * k
        suite["Coûts cumulés"] = couts_total + cout_jour * k
        tables.append(suite.melt(id_vars="date", var_name="serie", value_name="euros").assign(type="Suite estimée"))

courbes = pd.concat(tables)
courbes["libelle"] = courbes["date"].apply(date_fr)

lignes_courbes = (
    alt.Chart(courbes)
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("date:T", title="Date",
                axis=alt.Axis(labelExpr=LABEL_MOIS_ANNEE,
                              tickCount={"interval": "month", "step": 1},
                              labelAngle=-45, labelOverlap=True)),
        y=alt.Y("euros:Q", title="Montant cumulé (en euros)", axis=alt.Axis(labelExpr=LABEL_EUROS)),
        color=alt.Color("serie:N", title=None,
                        scale=alt.Scale(domain=["Revenus cumulés", "Coûts cumulés"], range=[MENTHE, ROSE]),
                        legend=alt.Legend(orient="bottom")),
        strokeDash=alt.StrokeDash("type:N", title=None,
                                  scale=alt.Scale(domain=["Réel", "Suite estimée"], range=[[1, 0], [6, 5]]),
                                  legend=alt.Legend(orient="bottom")),
        tooltip=[
            alt.Tooltip("libelle:N", title="Date"),
            alt.Tooltip("serie:N", title="Courbe"),
            alt.Tooltip("euros:Q", title="Euros", format=",.0f"),
        ],
    )
)

graphique_final = lignes_courbes
if date_amorti is not None and montrer_suite:
    point = pd.DataFrame({
        "date": [date_amorti],
        "euros": [couts_total + cout_jour * jours_restants],
        "texte": [f"Amorti en {MOIS[date_amorti.month - 1]} {date_amorti.year}"],
    })
    graphique_final = (
        lignes_courbes
        + alt.Chart(point).mark_point(size=160, filled=True, color="#EAE6F3").encode(x="date:T", y="euros:Q")
        + alt.Chart(point).mark_text(align="right", dx=-12, dy=-14, fontWeight="bold", fontSize=14,
                                     color="#EAE6F3").encode(x="date:T", y="euros:Q", text="texte:N")
    )

st.altair_chart(
    style_graphique(graphique_final.properties(height=360, padding={"left": 5, "right": 40, "top": 25, "bottom": 5})),
    theme=None, use_container_width=True
)

st.caption(
    f"Budget : {espaces(cout_initial)} € investis avant le test, puis {espaces(cout_mensuel)} € par mois "
    "(serveurs, équipe, marketing). Pendant le test, il n'y a pas eu d'achats."
)

if marge_30j > 0 and reste > 0:
    st.markdown(
        f"""
<div class="carte carte-verdict">
Sur {espaces(couts_total)} € dépensés depuis juin, {espaces(revenus_total)} € sont déjà récupérés. Ces 30 derniers
jours, le jeu a rapporté {espaces(revenus_30j)} € pour {espaces(couts_30j)} € de coûts : il est rentable chaque
mois. À ce rythme, il serait amorti vers {MOIS[date_amorti.month - 1]} {date_amorti.year}.
</div>
""",
        unsafe_allow_html=True
    )
    with st.expander("Comment est calculée la date d'amortissement"):
        st.markdown(
            f"- Sur les 30 derniers jours, Zeloria a rapporté {espaces(revenus_30j)} € et coûté "
            f"{espaces(couts_30j)} €, soit {espaces(marge_30j)} € de gagnés en plus des coûts.\n"
            f"- Il reste {espaces(reste)} € à récupérer : {espaces(reste)} ÷ {espaces(marge_30j)} = "
            f"{reste / marge_30j:.1f} périodes de 30 jours, soit environ {jours_restants} jours.\n"
            "- Après le pic de lancement, les téléchargements baissent : la date est donc une estimation, "
            "à revoir chaque mois."
        )
elif reste <= 0:
    st.markdown('<div class="carte carte-verdict">Zeloria a récupéré tout son budget.</div>',
                unsafe_allow_html=True)
else:
    st.markdown(
        f"""
<div class="carte carte-verdict">
Sur {espaces(couts_total)} € dépensés depuis juin, {espaces(revenus_total)} € sont récupérés. Ces 30 derniers
jours, le jeu a rapporté {espaces(revenus_30j)} € pour {espaces(couts_30j)} € de coûts : il perd
{espaces(-marge_30j)} € par mois.
</div>
""",
        unsafe_allow_html=True
    )


#  5. FIABILITE

st.divider()

st.header("5. Fiabilité des chiffres")

st.markdown("""
<div class="carte carte-question">
Le nombre d'acheteurs varie d'un jour à l'autre. On vérifie ici que la hausse d'octobre n'est pas
due au hasard, et que le montant dépensé à chaque achat reste stable.
</div>
""", unsafe_allow_html=True)

ventes["panier"] = ventes["revenus_euros"] / ventes["acheteurs"]
ventes["mois"] = ventes["date"].dt.month
sept = ventes[ventes["mois"] == 9]
octo = ventes[ventes["mois"] == 10]

p_sept = sept["acheteurs"].sum() / sept["joueurs_actifs"].sum()
p_oct = octo["acheteurs"].sum() / octo["joueurs_actifs"].sum()
test_binomial = stats.binomtest(int(octo["acheteurs"].sum()), int(octo["joueurs_actifs"].sum()),
                                p_sept, alternative="greater")

gauche, droite = st.columns(2)

with gauche:

    st.subheader("Part de joueurs qui achètent chaque jour")

    ventes["part"] = ventes["acheteurs"] / ventes["joueurs_actifs"]
    ventes["bas"] = stats.binom.ppf(0.025, ventes["joueurs_actifs"], p_sept) / ventes["joueurs_actifs"]
    ventes["haut"] = stats.binom.ppf(0.975, ventes["joueurs_actifs"], p_sept) / ventes["joueurs_actifs"]
    ventes["libelle"] = ventes["date"].apply(date_fr)

    axe_x = alt.X("date:T", title="Date", axis=alt.Axis(labelExpr=LABEL_JOUR, tickCount=7, labelOverlap=True))
    format_pct = alt.Axis(format=".1%", labelExpr="replace(format(datum.value, '.1%'), '.', ',')")

    bande = alt.Chart(ventes).mark_area(opacity=0.35, color="#9A8CA6").encode(
        x=axe_x, y=alt.Y("bas:Q", title="Part d'acheteurs", axis=format_pct,
                         scale=alt.Scale(zero=False)), y2="haut:Q")
    points = alt.Chart(ventes).mark_point(filled=True, size=55, color=LAVANDE).encode(
        x="date:T", y="part:Q",
        tooltip=[alt.Tooltip("libelle:N", title="Jour"),
                 alt.Tooltip("part:Q", title="Part d'acheteurs", format=".2%")])

    st.altair_chart(style_graphique((bande + points).properties(height=340)),
                    theme=None, use_container_width=True)
    st.caption("La zone grise est la variation normale d'un jour à l'autre si la part d'acheteurs "
               "restait celle de septembre (loi binomiale, intervalle à 95 %).")

with droite:

    st.subheader("Panier moyen par mois")

    paniers = []
    for mois, groupe in ((9, sept), (10, octo)):
        valeurs = groupe["panier"]
        bas, haut = stats.t.interval(0.95, len(valeurs) - 1, valeurs.mean(), stats.sem(valeurs))
        paniers.append({"mois": MOIS[mois - 1].capitalize(), "panier": valeurs.mean(), "bas": bas, "haut": haut})
    paniers = pd.DataFrame(paniers)

    base_p = alt.Chart(paniers).encode(
        x=alt.X("mois:N", title="Mois", sort=list(paniers["mois"]), axis=alt.Axis(labelAngle=0)))
    barres_p = base_p.mark_errorbar(color="#EAE6F3", thickness=2).encode(
        y=alt.Y("bas:Q", title="Panier moyen d'un acheteur (en euros)", scale=alt.Scale(domain=[6, 7]),
                axis=alt.Axis(labelExpr="replace(format(datum.value, '.1f'), '.', ',')")),
        y2="haut:Q")
    points_p = base_p.mark_point(size=160, filled=True, color=LAVANDE).encode(
        y="panier:Q",
        tooltip=[alt.Tooltip("mois:N", title="Mois"),
                 alt.Tooltip("panier:Q", title="Panier moyen (€)", format=".2f")])

    st.altair_chart(style_graphique((barres_p + points_p).properties(height=340)),
                    theme=None, use_container_width=True)
    st.caption("Les traits montrent l'intervalle de confiance à 95 % de chaque moyenne (test t de Student).")

t_test = stats.ttest_ind(sept["panier"], octo["panier"])

if test_binomial.pvalue < 0.05:
    phrase_part = (f"La part d'acheteurs passe de {virgule(p_sept * 100)} % en septembre à "
                   f"{virgule(p_oct * 100)} % en octobre : la hausse est trop forte pour être due au hasard.")
else:
    phrase_part = (f"La part d'acheteurs passe de {virgule(p_sept * 100)} % en septembre à "
                   f"{virgule(p_oct * 100)} % en octobre : la hausse pourrait être due au hasard.")

if t_test.pvalue >= 0.05:
    phrase_panier = (f"Le panier moyen reste stable, autour de {virgule(ventes['panier'].mean(), 2)} € : "
                     "la hausse vient du nombre d'acheteurs.")
else:
    phrase_panier = (f"Le panier moyen passe de {virgule(sept['panier'].mean(), 2)} € à "
                     f"{virgule(octo['panier'].mean(), 2)} € entre septembre et octobre.")

if date_amorti is not None:
    phrase_fin = (f"Zeloria est rentable chaque mois et serait amorti vers {MOIS[date_amorti.month - 1]} "
                  f"{date_amorti.year}. Il reste à améliorer : {liste(plus_cites)}.")
else:
    phrase_fin = "Zeloria n'est pas encore rentable chaque mois."

st.markdown(
    f"""
<div class="carte carte-verdict">
<p>{phrase_part}</p>
<p>{phrase_panier}</p>
<p>{phrase_fin}</p>
</div>
""",
    unsafe_allow_html=True
)