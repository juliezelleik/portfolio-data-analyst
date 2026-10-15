from scipy import stats

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

try:
    st.set_page_config(
        page_title="Zeloria - Bilan du pré-lancement",
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
    background: #FFF9F5;
}

h1, h2, h3, p, li, label, span, div[data-testid="stMetricValue"],
div[data-testid="stMetricLabel"], div[data-testid="stHeading"] *,
div[data-testid="stSlider"] *, div[data-testid="stToggle"] * {
    color: #4A3B52;
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
    color: #4A3B52;
}

.carte-histoire {
    background: #FDE4EE;
    border: 2px solid #F8C8DC;
}

.carte-question {
    background: #EADFFB;
    border: 2px solid #D9C8F0;
}

.carte-verdict {
    background: #DDF4EA;
    border: 2px solid #BFE8D8;
}

.pastille {
    display: inline-block;
    background: #EADFFB;
    color: #4A3B52;
    font-size: 13px;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 999px;
}

.etiquette {
    font-weight: 800;
    font-size: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 2px solid #F8C8DC;
    padding: 16px;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)


#  DONNEES

def charger():
    ventes = pd.read_csv(
        "ventes.csv", sep=";",
        parse_dates=["date"]
    )
    budget = pd.read_csv(
        "budget.csv", sep=";"
    )
    return ventes, budget


ventes, budget = charger()


def espaces(nombre):
    return f"{nombre:,.0f}".replace(",", " ")


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


#  HISTOIRE ET PROBLEMATIQUE

st.markdown('<div class="titre-zeloria">Zeloria</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sous-titre">Studio Zelleik - bilan du pré-lancement</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="carte carte-histoire">
<div class="etiquette">L'histoire</div>
Zeloria est un jeu mobile gratuit de type gacha, créé par le studio Zelleik.
On y collectionne, on élève et on soigne des petites créatures obtenues par
tirage au sort. C'est un jeu « pay to progress » : on peut payer pour progresser plus
vite ou personnaliser ses créatures, mais pas pour gagner plus facilement qu'un autre joueur
(pas de « pay to win »). Depuis le 1er juillet 2026, un groupe de joueurs teste le jeu en
pré-lancement. Trois mois plus tard, il est temps de faire le point avant le lancement
officiel, prévu le 1er novembre 2026.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="carte carte-question">
<div class="etiquette">La problématique</div>
Que faut-il améliorer avant le lancement officiel de Zeloria pour augmenter ses revenus
et/ou le rendre rentable le plus rapidement possible ?
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<span class="pastille">Données fictives</span>',
    unsafe_allow_html=True
)

st.divider()


#  1. RENTABILITE

st.header("1. Bilan financier du pré-lancement")

cout_initial = budget[budget["type"] == "Initial"]["montant_euros"].sum()
cout_mensuel = budget[budget["type"] == "Mensuel"]["montant_euros"].sum()
cout_jour = cout_mensuel / 30

ventes = ventes.sort_values("date").reset_index(drop=True)
ventes["revenus_cumules"] = ventes["revenus_euros"].cumsum()
ventes["couts_cumules"] = cout_initial + cout_jour * (ventes.index + 1)

revenus_total = ventes["revenus_euros"].sum()
couts_total = ventes["couts_cumules"].iloc[-1]

k1, k2, k3, k4 = st.columns(4)

k1.metric("Téléchargements", espaces(ventes["telechargements"].sum()))
k2.metric(
    "Joueurs actifs (moyenne 7 jours)",
    espaces(ventes["joueurs_actifs"].tail(7).mean())
)
k3.metric("Revenus des achats", f"{espaces(revenus_total)} €")
k4.metric("Budget récupéré", f"{revenus_total / couts_total:.0%}")


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

MOIS_COURT = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
              "août", "sept.", "oct.", "nov.", "déc."]


def date_fr(d):
    return f"{d.day} {MOIS_COURT[d.month - 1]} {d.year}"


def style_graphique(graphique):
    return (
        graphique
        .configure(background="#FFFFFF")
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor="#4A3B52", titleColor="#4A3B52", gridColor="#F1E6EC")
        .configure_legend(labelColor="#4A3B52", titleColor="#4A3B52")
    )



revenus_28j = ventes["revenus_euros"].tail(28).sum()
couts_28j = cout_jour * 28
marge_28j = revenus_28j - couts_28j
net_jour = marge_28j / 28
reste = couts_total - revenus_total


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
    st.subheader("Évolution des revenus par rapport aux coûts")
    zone_revenus = st.container()

    montrer_suite = st.toggle(
        "Montrer la suite estimée à ce rythme",
        value=True
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

    st.altair_chart(
        style_graphique(graphique_telechargements),
        theme=None,
        use_container_width=True
    )

with zone_revenus:

    reel = ventes[["date", "revenus_cumules", "couts_cumules"]].rename(columns={
        "revenus_cumules": "Revenus cumulés",
        "couts_cumules": "Coûts cumulés"
    })
    reel = reel.melt(id_vars="date", var_name="serie", value_name="euros")
    reel["type"] = "Réel"

    tables = [reel]
    date_amorti = None

    if reste > 0:

        revenu_jour = revenus_28j / 28

        if marge_28j > 0:
            jours_restants = int(reste / net_jour) + 1
            date_amorti = ventes["date"].iloc[-1] + pd.Timedelta(days=jours_restants)
            fin_suite = date_amorti
        else:
            fin_suite = ventes["date"].iloc[-1] + pd.Timedelta(days=365)

        if montrer_suite:

            suite = pd.DataFrame({
                "date": pd.date_range(ventes["date"].iloc[-1], fin_suite)
            })
            k = (suite["date"] - ventes["date"].iloc[-1]).dt.days
            suite["Revenus cumulés"] = revenus_total + revenu_jour * k
            suite["Coûts cumulés"] = couts_total + cout_jour * k
            suite = suite.melt(id_vars="date", var_name="serie", value_name="euros")
            suite["type"] = "Suite estimée"
            tables.append(suite)

    courbes = pd.concat(tables)
    courbes["libelle"] = courbes["date"].apply(date_fr)

    lignes_courbes = (
        alt.Chart(courbes)
        .mark_line(strokeWidth=3)
        .encode(
            x=alt.X(
                "date:T", title="Date",
                axis=alt.Axis(
                    labelExpr=LABEL_MOIS_ANNEE,
                    tickCount={"interval": "month", "step": 1},
                                  labelAngle=-45, labelOverlap=True
                )
            ),
            y=alt.Y("euros:Q", title="Montant cumulé (en euros)",
                    axis=alt.Axis(labelExpr=LABEL_EUROS)),
            color=alt.Color(
                "serie:N", title=None,
                scale=alt.Scale(
                    domain=["Revenus cumulés", "Coûts cumulés"],
                    range=[MENTHE, ROSE]
                ),
                legend=alt.Legend(orient="bottom")
            ),
            strokeDash=alt.StrokeDash(
                "type:N", title=None,
                scale=alt.Scale(domain=["Réel", "Suite estimée"], range=[[1, 0], [6, 5]]),
                legend=alt.Legend(orient="bottom")
            ),
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

        croisement = (
            alt.Chart(point).mark_point(size=160, filled=True, color="#4A3B52")
            .encode(x="date:T", y="euros:Q")
        )
        etiquette = (
            alt.Chart(point)
            .mark_text(align="right", dx=-12, dy=-14, fontWeight="bold",
                       fontSize=14, color="#4A3B52")
            .encode(x="date:T", y="euros:Q", text="texte:N")
        )

        graphique_final = lignes_courbes + croisement + etiquette

    st.altair_chart(
        style_graphique(graphique_final.properties(height=340, padding={"left": 5, "right": 40, "top": 25, "bottom": 5})),
        theme=None,
        use_container_width=True
    )

st.caption(
    f"Budget : {espaces(cout_initial)} € investis avant le pré-lancement, "
    f"puis {espaces(cout_mensuel)} € par mois (serveurs, équipe, marketing)."
)


if marge_28j > 0 and reste > 0:
    nb_mois = round(reste / (net_jour * 30))
    date_amorti = ventes["date"].iloc[-1] + pd.Timedelta(days=int(reste / net_jour) + 1)
    nb_jours_restants = int(reste / net_jour) + 1
    conclusion = (
        "Comment on calcule la date d'amortissement"
        "<ul>"
        f"<li>Sur les 28 derniers jours, Zeloria a rapporté {espaces(revenus_28j)} € "
        f"et coûté {espaces(couts_28j)} €, soit {espaces(marge_28j)} € de gagnés "
        "en plus des coûts.</li>"
        f"<li>Il reste {espaces(reste)} € à récupérer. Chaque période de 28 jours rapporte "
        f"{espaces(marge_28j)} € de plus que les coûts, donc il faut environ "
        f"{espaces(reste)} ÷ {espaces(marge_28j)} = {reste / marge_28j:.0f} périodes de 28 jours.</li>"
        f"<li>{reste / marge_28j:.0f} périodes de 28 jours, c'est environ {nb_jours_restants} jours, "
        f"soit à peu près {nb_mois} mois.</li>"
        "</ul>"
        f"Zeloria sera donc amorti vers {MOIS[date_amorti.month - 1]} {date_amorti.year}."
    )
    titre_verdict = "Zeloria couvre ses frais, mais il n'est pas encore amorti."
elif reste <= 0:
    conclusion = "Zeloria est amorti."
    titre_verdict = "Zeloria a récupéré tout son budget."
else:
    perte_mois = -marge_28j / 28 * 30
    conclusion = (
        "Comment on le constate"
        "<ul>"
        f"<li>Sur les 28 derniers jours, Zeloria a rapporté {espaces(revenus_28j)} € "
        f"et coûté {espaces(couts_28j)} €.</li>"
        f"<li>Il perd donc environ {espaces(perte_mois)} € par mois : plus le temps passe, "
        "plus l'écart entre les coûts et les revenus se creuse.</li>"
        "</ul>"
        "Pendant un test fermé, ne pas couvrir ses frais est normal : le jeu n'est pas encore "
        "ouvert à tout le monde. Mais à ce rythme, Zeloria ne serait jamais amorti, "
        "d'où les améliorations à préparer avant le lancement officiel."
    )
    titre_verdict = "Pendant le pré-lancement, Zeloria ne couvre pas ses frais."

if marge_28j >= 0:
    phrase_marge = f"il gagne {espaces(marge_28j)} € de plus que ses coûts"
else:
    phrase_marge = f"il perd {espaces(-marge_28j)} €"

st.markdown(
    f"""
<div class="carte carte-verdict">
<div class="etiquette">Ce qu'il faut retenir</div>
{titre_verdict}
<ul>
<li>Coûts depuis le début du pré-lancement : {espaces(couts_total)} €
({espaces(cout_initial)} € au départ, plus {espaces(cout_mensuel)} € par mois)</li>
<li>Revenus depuis le début du pré-lancement : {espaces(revenus_total)} €</li>
<li>Reste à récupérer : {espaces(max(reste, 0))} €</li>
<li>Ces 28 derniers jours, le jeu a rapporté {espaces(revenus_28j)} € pour
{espaces(couts_28j)} € de coûts : {phrase_marge}.</li>
</ul>
{conclusion}
</div>
""",
    unsafe_allow_html=True
)


#  2. SATISFACTION DES JOUEURS

st.divider()

st.header("2. Satisfaction des joueurs testeurs")

enquetes = pd.read_csv("enquetes.csv", sep=";")
bugs = pd.read_csv("bugs.csv", sep=";")

NOM_ENQUETE = {
    "ENQ-1": "Enquête 1 (juillet)",
    "ENQ-2": "Enquête 2 (août)",
    "ENQ-3": "Enquête 3 (septembre)",
}
enquetes["enquete"] = enquetes["id_enquete"].map(NOM_ENQUETE)

moyennes = enquetes.groupby("enquete")["note_satisfaction"].mean()

s1, s2, s3 = st.columns(3)
for colonne, nom in zip((s1, s2, s3), NOM_ENQUETE.values()):
    colonne.metric(f"Satisfaction - {nom}", f"{moyennes[nom]:.2f} / 5".replace(".", ","))

plaintes = enquetes[enquetes["theme"] != "Rien à changer"]

gauche, droite = st.columns(2)

with gauche:

    st.subheader("Remontées des joueurs par sujet")

    par_theme = plaintes.groupby(["theme", "enquete"]).size().reset_index(name="plaintes")

    graphique_plaintes = (
        alt.Chart(par_theme)
        .mark_bar()
        .encode(
            y=alt.Y("theme:N", title=None,
                    sort=alt.EncodingSortField("plaintes", op="sum", order="descending")),
            yOffset=alt.YOffset("enquete:N", sort=list(NOM_ENQUETE.values())),
            x=alt.X("plaintes:Q", title="Nombre de joueurs qui s'en plaignent"),
            color=alt.Color(
                "enquete:N", title=None,
                scale=alt.Scale(domain=list(NOM_ENQUETE.values()),
                                range=["#D9CCF5", "#B9A0EC", "#8A63D2"]),
                legend=alt.Legend(orient="bottom")
            ),
            tooltip=[
                alt.Tooltip("theme:N", title="Sujet"),
                alt.Tooltip("enquete:N", title="Enquête"),
                alt.Tooltip("plaintes:Q", title="Joueurs"),
            ],
        )
        .properties(height=420)
    )

    st.altair_chart(style_graphique(graphique_plaintes), theme=None, use_container_width=True)

with droite:

    st.subheader("Bugs par sujet et état des corrections")

    etat_bugs = bugs.groupby(["categorie", "statut"]).size().reset_index(name="bugs")

    graphique_bugs = (
        alt.Chart(etat_bugs)
        .mark_bar()
        .encode(
            y=alt.Y("categorie:N", title=None,
                    sort=alt.EncodingSortField("bugs", op="sum", order="descending")),
            x=alt.X("bugs:Q", title="Nombre de bugs signalés"),
            color=alt.Color(
                "statut:N", title=None,
                scale=alt.Scale(domain=["Corrigé", "En cours", "Ouvert"],
                                range=[MENTHE, LAVANDE, ROSE]),
                legend=alt.Legend(orient="bottom")
            ),
            order=alt.Order("statut:N", sort="ascending"),
            tooltip=[
                alt.Tooltip("categorie:N", title="Sujet"),
                alt.Tooltip("statut:N", title="État"),
                alt.Tooltip("bugs:Q", title="Bugs"),
            ],
        )
        .properties(height=420)
    )

    st.altair_chart(style_graphique(graphique_bugs), theme=None, use_container_width=True)

st.caption(
    "Corrigé : le correctif est publié. En cours : un correctif est en préparation. "
    "Ouvert : le bug est signalé mais personne ne l'a encore pris en charge."
)


tableau = par_theme.pivot(index="theme", columns="enquete", values="plaintes").fillna(0)
tableau = tableau[list(NOM_ENQUETE.values())]
tableau["evolution"] = tableau[NOM_ENQUETE["ENQ-3"]] - tableau[NOM_ENQUETE["ENQ-1"]]

restants = bugs[bugs["statut"] != "Corrigé"]
tableau["bugs_restants"] = restants.groupby("categorie").size()
tableau["bugs_restants"] = tableau["bugs_restants"].fillna(0).astype(int)

a_corriger = tableau[
    (tableau["evolution"] >= 0) & (tableau["bugs_restants"] > 0)
].sort_values("evolution", ascending=False)

note_debut = f"{moyennes.iloc[0]:.2f}".replace(".", ",")
note_fin = f"{moyennes.iloc[-1]:.2f}".replace(".", ",")

lignes = ""
for theme, ligne in a_corriger.iterrows():
    lignes += (
        f"<li>{theme} : {int(ligne[NOM_ENQUETE['ENQ-1']])} plaintes en juillet "
        f"puis {int(ligne[NOM_ENQUETE['ENQ-3']])} en septembre. "
        f"Il reste {ligne['bugs_restants']} bug{'s' if ligne['bugs_restants'] > 1 else ''} à corriger.</li>"
    )

ont_baisse = tableau[tableau["evolution"] < 0].index.tolist()

st.markdown(
    f"""
<div class="carte carte-verdict">
<div class="etiquette">Ce qu'il faut retenir</div>
La satisfaction monte de {note_debut} à {note_fin}, mais deux sujets ne s'améliorent pas.
<ul>
<li>Les plaintes ont baissé sur : {", ".join(t.lower() for t in ont_baisse)}.
Les correctifs publiés ont donc marché.</li>
</ul>
Il reste des plaintes qui ne baissent pas, avec des bugs encore non corrigés.
Ces sujets sont à corriger avant le lancement officiel :
<ul>{lignes}</ul>
</div>
""",
    unsafe_allow_html=True
)


#  3. ACTIONS A METTRE EN PLACE

st.divider()

st.header("3. Actions à mettre en place")

st.markdown("""
<div class="carte carte-question">
<div class="etiquette">Les actions proposées</div>
Les plaintes montrent qu'il faut améliorer la boutique et les menus.
D'autres idées servent à faire acheter davantage et à garder les joueurs : un événement
chaque semaine, une tenue payante chaque mois, un pass mensuel avec des cadeaux bonus,
un Zeloria légendaire par saison de 3 mois (gratuit à attraper, mais ses couleurs et
son évolution sont payantes), un pass de combat par saison avec des récompenses à
débloquer, un cadeau pour le joueur qui invite un ami et une campagne de publicité pour
faire venir de nouveaux joueurs. Ces actions sont préparées en octobre et produisent leur effet
à partir du lancement officiel, le 1er novembre 2026 (plus tard si leur mise en place est plus longue).
</div>
""", unsafe_allow_html=True)

actions = pd.DataFrame({
    "Action": [
        "Boutique plus claire et prix revus",
        "Menus simplifiés et bugs corrigés",
        "Un événement chaque semaine",
        "Une tenue payante chaque mois",
        "Pass mensuel avec cadeaux bonus",
        "Un Zeloria légendaire par saison",
        "Un cadeau pour inviter un ami",
        "Un pass de combat par saison",
        "Une campagne de publicité de lancement",
    ],
    "Pourquoi": [
        "21 plaintes en septembre",
        "26 plaintes, 4 bugs à corriger",
        "Faire revenir les joueurs",
        "Acheter chaque mois",
        "Revenu régulier chaque mois",
        "Gratuit à attraper, payant à améliorer",
        "Faire venir de nouveaux joueurs",
        "Des récompenses à débloquer pendant 3 mois",
        "Faire venir de nouveaux joueurs",
    ],
    "Durée de mise en place (jours)": [7, 30, 30, 7, 7, 30, 14, 30, 14],
    "Mise en place (€)": [5000, 12000, 4000, 3000, 5000, 10000, 4000, 8000, 15000],
    "Coût par mois (€)": [0, 0, 3000, 1500, 500, 500, 1000, 1000, 40000],
})

st.subheader("Coût et durée de chaque action")

actions = st.data_editor(
    actions,
    hide_index=True,
    use_container_width=True,
    disabled=["Action", "Pourquoi"],
    column_config={
        "Durée de mise en place (jours)": st.column_config.NumberColumn(
            min_value=0, step=1,
            help="Temps de préparation avant que l'action ne produise son effet."),
        "Mise en place (€)": st.column_config.NumberColumn(min_value=0, step=500),
        "Coût par mois (€)": st.column_config.NumberColumn(min_value=0, step=500),
    },
)


choix, graphique_col = st.columns([1, 2.4])

with choix:

    st.subheader("Choix des actions")

    SCENARIOS = {
        "Réaliste": {"part_acheteurs": 4.0, "invitent": 10, "depart_moins": 20,
                     "part_pass": 12, "prix_pass": 5,
                     "part_battle": 10, "prix_battle": 9.99, "cpi": 1.0, "bouche": 3},
        "Ambitieux": {"part_acheteurs": 5.0, "invitent": 12, "depart_moins": 30,
                      "part_pass": 20, "prix_pass": 5,
                      "part_battle": 15, "prix_battle": 9.99, "cpi": 0.8, "bouche": 4},
    }

    scenario = st.radio("Scénario", list(SCENARIOS), index=0, horizontal=True)

    hypotheses = SCENARIOS[scenario]
    part_acheteurs = hypotheses["part_acheteurs"]
    invitent = hypotheses["invitent"]
    departs_moins = hypotheses["depart_moins"]
    part_pass = hypotheses["part_pass"]
    prix_pass = hypotheses["prix_pass"]
    part_battle = hypotheses["part_battle"]
    prix_battle = hypotheses["prix_battle"]
    cpi = hypotheses["cpi"]
    bouche = hypotheses["bouche"]

    st.caption(
        f"Part des joueurs qui achètent : {str(part_acheteurs).replace('.', ',')} % (3 % aujourd'hui)  \n"
        f"Invitations d'amis : {invitent} pour 100 joueurs par mois  \n"
        f"Départs en moins : {departs_moins} %  \n"
        f"Pass mensuel : {part_pass} % des joueurs, {prix_pass} € par mois  \n"
        f"Pass de combat : {part_battle} % des joueurs, {str(prix_battle).replace('.', ',')} € la saison  \n"
        f"Publicité : {str(cpi).replace('.', ',')} € par téléchargement  \n"
        f"Bouche-à-oreille : {bouche} % de téléchargements en plus par nouveauté"
    )

    retenue = [
        st.checkbox(nom, value=True, key=f"action_{i}")
        for i, nom in enumerate(actions["Action"])
    ]
    comparer = st.checkbox("Comparer avec le jeu sans aucune action", value=True)

retenues = actions[retenue]

revenu_jour_base = revenus_28j / 28
dernier_jour = ventes["date"].iloc[-1]
nb_jours = 900
JOURS_AVANT_LANCEMENT = 31
TELECHARGEMENTS_LANCEMENT = 300_000
PIC_PAR_SAISON = 20_000
PART_QUI_RESTE_LANCEMENT = 0.05
jours = pd.date_range(dernier_jour, periods=nb_jours + 1)
k = np.arange(nb_jours + 1)


p_actuel = ventes["acheteurs"].tail(28).sum() / ventes["joueurs_actifs"].tail(28).sum()
joueurs_actifs_moy = ventes["joueurs_actifs"].tail(28).mean()
panier_moyen = revenus_28j / ventes["acheteurs"].tail(28).sum()
gain_points = part_acheteurs / 100 - p_actuel

part_en_place = np.zeros(nb_jours + 1)
pass_en_place = np.zeros(nb_jours + 1)
battle_en_place = np.zeros(nb_jours + 1)
pub_budget_jour = np.zeros(nb_jours + 1)
bouche_en_place = np.zeros(nb_jours + 1)
saison_en_place = np.zeros(nb_jours + 1)
amis_en_place = np.zeros(nb_jours + 1)
cout_actions_jour = np.zeros(nb_jours + 1)
for numero, a in retenues.iterrows():
    en_place = k > max(a["Durée de mise en place (jours)"], JOURS_AVANT_LANCEMENT)
    cout_actions_jour += en_place * a["Coût par mois (€)"] / 30
    if numero in (5, 7):
        saison_en_place += en_place
    if numero not in (6, 8):
        bouche_en_place += en_place
    if numero == 4:
        pass_en_place += en_place
    elif numero == 6:
        amis_en_place += en_place
    elif numero == 7:
        battle_en_place += en_place
    elif numero == 8:
        pub_budget_jour += en_place * a["Coût par mois (€)"]
    else:
        part_en_place += en_place / 5


telechargements_jour = ventes["telechargements"].tail(28).mean()
depart_jour = 1 / 30
part_qui_reste_joueur = depart_jour * joueurs_actifs_moy / telechargements_jour

def evolution_joueurs(amis_actifs=True, pub_active=True, departs_reduits=True, avec_actions=True):
    joueurs = np.zeros(nb_jours + 1)
    telechargements = np.zeros(nb_jours + 1)
    joueurs[0] = joueurs_actifs_moy
    for j in range(1, nb_jours + 1):
        arrivees = telechargements_jour
        if not avec_actions:
            amis_actifs = pub_active = departs_reduits = False
        if amis_actifs:
            arrivees += amis_en_place[j] * joueurs[j - 1] * (invitent / 100) / 30
        if pub_active:
            arrivees += pub_budget_jour[j] / cpi / 30
        if avec_actions:
            montee = 1 + min(max(j - JOURS_AVANT_LANCEMENT, 0), 180) / 90
            arrivees *= 1 + bouche / 100 * bouche_en_place[j] * montee
        vague = 0.0
        if j > JOURS_AVANT_LANCEMENT:
            vague = (TELECHARGEMENTS_LANCEMENT * (1 - np.exp(-1 / 6))
                     * np.exp(-(j - JOURS_AVANT_LANCEMENT - 1) / 6))
        if avec_actions and j > JOURS_AVANT_LANCEMENT + 90:
            depuis_saison = (j - JOURS_AVANT_LANCEMENT - 1) % 90
            if j - JOURS_AVANT_LANCEMENT - 1 >= 90:
                vague += (saison_en_place[j] * PIC_PAR_SAISON * (1 - np.exp(-1 / 6))
                          * np.exp(-depuis_saison / 6))
        nouveaux_joueurs = part_qui_reste_joueur * arrivees + PART_QUI_RESTE_LANCEMENT * vague
        arrivees += vague
        reduction = departs_moins / 100 * part_en_place[j] if departs_reduits else 0
        departs = depart_jour * (1 - reduction)
        joueurs[j] = joueurs[j - 1] * (1 - departs) + nouveaux_joueurs
        telechargements[j] = arrivees
    return joueurs, telechargements


joueurs_avec, telechargements_avec = evolution_joueurs()
joueurs_sans, telechargements_sans = evolution_joueurs(avec_actions=False)

total_depuis_le_debut = ventes["telechargements"].sum()
joueurs_un_an_avec = total_depuis_le_debut + telechargements_avec[1:366].sum()
joueurs_un_an_sans = total_depuis_le_debut + telechargements_sans[1:366].sum()

p_jour = p_actuel + gain_points * part_en_place
revenus_pass_jour = joueurs_avec * pass_en_place * (part_pass / 100) * prix_pass / 30
revenus_battle_jour = joueurs_avec * battle_en_place * (part_battle / 100) * prix_battle / 90
revenus_jour_avec = joueurs_avec * p_jour * panier_moyen + revenus_pass_jour + revenus_battle_jour
couts_jour_avec = cout_jour + cout_actions_jour

revenus_avec = revenus_total + np.cumsum(np.r_[0, revenus_jour_avec[1:]])
couts_avec = (
    couts_total + retenues["Mise en place (€)"].sum()
    * (k > 0) + np.cumsum(np.r_[0, couts_jour_avec[1:]])
)
revenus_jour_sans = joueurs_sans * p_actuel * panier_moyen
revenus_sans = revenus_total + np.cumsum(np.r_[0, revenus_jour_sans[1:]])
couts_sans = couts_total + cout_jour * k


def jour_amortissement(revenus, couts):
    atteint = np.where(revenus >= couts)[0]
    return jours[atteint[0]] if len(atteint) else None


amorti_sans = jour_amortissement(revenus_sans, couts_sans)
amorti_avec = jour_amortissement(revenus_avec, couts_avec)


def en_toutes_lettres(d):
    return "jamais" if d is None else f"{MOIS[d.month - 1]} {d.year}"


with graphique_col:

    st.subheader("Revenus et coûts avec les actions")

    fin_graphique = (amorti_avec if amorti_avec is not None else jours[400]) + pd.Timedelta(days=120)
    fin_graphique = min(fin_graphique, jours[-1])
    pas_mois = 1 if (fin_graphique - jours[0]).days <= 600 else 2

    reel_a = ventes[["date", "revenus_cumules", "couts_cumules"]].rename(columns={
        "revenus_cumules": "Revenus", "couts_cumules": "Coûts"
    }).melt(id_vars="date", var_name="serie", value_name="euros")

    projection = pd.concat([
        pd.DataFrame({"date": jours, "serie": "Revenus", "euros": revenus_avec}),
        pd.DataFrame({"date": jours, "serie": "Coûts", "euros": couts_avec}),
    ])
    parties = [reel_a, projection]

    if comparer:
        parties.append(pd.DataFrame({
            "date": jours, "serie": "Revenus sans action", "euros": revenus_sans
        }))

    courbes_a = pd.concat(parties)
    courbes_a = courbes_a[courbes_a["date"] <= fin_graphique]
    courbes_a["libelle"] = courbes_a["date"].apply(date_fr)

    domaine = ["Revenus", "Coûts"] + (["Revenus sans action"] if comparer else [])
    couleurs = [MENTHE, ROSE] + (["#9A8CA6"] if comparer else [])
    traits = [[1, 0], [1, 0]] + ([[6, 4]] if comparer else [])

    lignes_a = (
        alt.Chart(courbes_a)
        .mark_line(strokeWidth=3)
        .encode(
            x=alt.X("date:T", title="Date",
                    axis=alt.Axis(labelExpr=LABEL_MOIS_ANNEE,
                                  tickCount={"interval": "month", "step": pas_mois},
                                  labelAngle=-45, labelOverlap=True)),
            y=alt.Y("euros:Q", title="Montant cumulé depuis le début (en euros)",
                    axis=alt.Axis(labelExpr=LABEL_EUROS)),
            color=alt.Color("serie:N", title=None,
                            scale=alt.Scale(domain=domaine, range=couleurs),
                            legend=alt.Legend(orient="bottom")),
            strokeDash=alt.StrokeDash("serie:N", legend=None,
                                      scale=alt.Scale(domain=domaine, range=traits)),
            tooltip=[
                alt.Tooltip("libelle:N", title="Date"),
                alt.Tooltip("serie:N", title="Courbe"),
                alt.Tooltip("euros:Q", title="Euros", format=",.0f"),
            ],
        )
    )

    calques = lignes_a

    if amorti_avec is not None:
        i_avec = int(np.where(jours == amorti_avec)[0][0])
        point_a = pd.DataFrame({
            "date": [amorti_avec],
            "euros": [couts_avec[i_avec]],
            "texte": [f"Amorti en {MOIS[amorti_avec.month - 1]} {amorti_avec.year}"],
        })
        calques = (
            calques
            + alt.Chart(point_a).mark_point(size=180, filled=True, color="#4A3B52")
            .encode(x="date:T", y="euros:Q")
            + alt.Chart(point_a).mark_text(align="right", dx=-12, dy=-16,
                                           fontWeight="bold", fontSize=14, color="#4A3B52")
            .encode(x="date:T", y="euros:Q", text="texte:N")
        )

    st.altair_chart(
        style_graphique(calques.properties(
            height=420, padding={"left": 5, "right": 40, "top": 25, "bottom": 5})),
        theme=None, use_container_width=True
    )

    st.subheader("Évolution du nombre de joueurs qui téléchargent le jeu")

    reel = ventes[["date", "telechargements"]].rename(columns={"telechargements": "nb"})
    reel["courbe"] = "Pré-lancement (réel)"
    suite = pd.DataFrame({"date": jours[1:366], "nb": telechargements_avec[1:366],
                          "courbe": "Avec les actions cochées"})
    suite_sans = pd.DataFrame({"date": jours[1:366], "nb": telechargements_sans[1:366],
                               "courbe": "Sans action"})
    domaine_dl = ["Pré-lancement (réel)", "Avec les actions cochées"] + (["Sans action"] if comparer else [])
    tout = pd.concat([reel, suite] + ([suite_sans] if comparer else []), ignore_index=True)
    tout["mois"] = tout["date"].dt.to_period("M").dt.to_timestamp()
    par_mois = tout.groupby(["mois", "courbe"], as_index=False)["nb"].sum()
    par_mois["nb"] = par_mois["nb"].round()
    sept = par_mois[(par_mois["courbe"] == "Pré-lancement (réel)")
                    & (par_mois["mois"] == pd.Timestamp("2026-09-01"))]
    raccords = [sept.assign(courbe=nom) for nom in domaine_dl[1:]]
    par_mois = pd.concat([par_mois] + raccords, ignore_index=True)

    couleurs_dl = [LAVANDE, MENTHE] + (["#9A8CA6"] if comparer else [])
    traits_dl = [[1, 0], [1, 0]] + ([[6, 4]] if comparer else [])

    courbes_dl = alt.Chart(par_mois).encode(
        x=alt.X("mois:T", title="",
                axis=alt.Axis(labelExpr=LABEL_MOIS_ANNEE, labelAngle=-45,
                              tickCount={"interval": "month", "step": 1})),
        y=alt.Y("nb:Q", title="Téléchargements dans le mois",
                axis=alt.Axis(labelExpr=LABEL_EUROS)),
        color=alt.Color("courbe:N", title="",
                        scale=alt.Scale(domain=domaine_dl, range=couleurs_dl),
                        legend=alt.Legend(orient="bottom")),
        strokeDash=alt.StrokeDash("courbe:N", scale=alt.Scale(domain=domaine_dl, range=traits_dl), legend=None),
        tooltip=[
            alt.Tooltip("mois:T", title="Mois", format="%m/%Y"),
            alt.Tooltip("courbe:N", title="Courbe"),
            alt.Tooltip("nb:Q", title="Téléchargements", format=",.0f"),
        ],
    )
    graphique_dl = (
        courbes_dl.mark_line(strokeWidth=3) + courbes_dl.mark_point(filled=True, size=70)
    ).properties(height=320, padding={"left": 5, "right": 20, "top": 10, "bottom": 5})

    st.altair_chart(style_graphique(graphique_dl), theme=None, use_container_width=True)

    st.caption(
        f"Le lancement officiel du 1er novembre 2026 provoque un pic de {espaces(TELECHARGEMENTS_LANCEMENT)} "
        f"téléchargements, qui retombe en quelques jours. Avec les actions cochées, le nombre de "
        f"téléchargements remonte ensuite peu à peu, avec un petit pic à chaque nouvelle saison. "
        f"{espaces(joueurs_un_an_avec)} joueurs auront téléchargé le jeu dans un an, "
        f"contre {espaces(joueurs_un_an_sans)} sans action."
    )

st.caption(
    "Les coûts de mise en place sont payés dès octobre 2026. L'effet sur les revenus et sur "
    "les joueurs commence au lancement officiel, le 1er novembre 2026, ou après la durée de "
    "mise en place de l'action si elle est plus longue."
)


cout_mise_en_place = retenues["Mise en place (€)"].sum()
cout_actions_mois = retenues["Coût par mois (€)"].sum()
gain_mois = (revenus_jour_avec[365] - revenus_jour_sans[365]) * 30
benefice_mois = gain_mois - cout_actions_mois

if len(retenues) == 0:
    verdict_actions = "Aucune action retenue : le jeu garde le rythme du pré-lancement."
    if amorti_sans is None:
        verdict_actions += " À ce rythme, Zeloria ne sera jamais amorti."
elif amorti_avec is None:
    verdict_actions = (
        "Avec ces actions, Zeloria ne serait pas encore amorti dans les deux ans et demi "
        "qui suivent : il faut retenir d'autres actions ou augmenter leur effet."
    )
else:
    if amorti_sans is None:
        comparaison = "Sans action, Zeloria ne serait jamais amorti."
    else:
        mois_gagnes = round((amorti_sans - amorti_avec).days / 30)
        comparaison = (
            f"Sans action, il serait amorti en {en_toutes_lettres(amorti_sans)}, soit "
            f"{mois_gagnes} mois de plus."
        )
    verdict_actions = (
        f"Avec ces actions, Zeloria est amorti en {en_toutes_lettres(amorti_avec)}. "
        f"{comparaison}"
        f"<br>Les actions retenues coûtent {espaces(cout_mise_en_place)} € au départ et "
        f"{espaces(cout_actions_mois)} € par mois. Un an après, elles rapportent environ "
        f"{espaces(gain_mois)} € de plus par mois."
    )

st.markdown(
    f"""
<div class="carte carte-verdict">
<div class="etiquette">Ce qu'il faut retenir</div>
{verdict_actions}
<br>Il s'agit d'une pré-décision, prise avec les données du pré-lancement. Après le lancement
officiel, il faudra suivre l'évolution réelle des joueurs et des revenus, puis prendre d'autres
décisions en conséquence.
</div>
""",
    unsafe_allow_html=True
)


#  4. FIABILITE DU GAIN ATTENDU

st.divider()

st.header("4. Fiabilité du gain attendu")

st.markdown("""
<div class="carte carte-question">
<div class="etiquette">Comment lire cette partie</div>
Chaque jour, un joueur actif a deux possibilités : acheter ou ne pas acheter.
Aujourd'hui, 3 joueurs sur 100 achètent. Mais ce n'est jamais exactement 3 sur 100 : un jour
il y en a un peu plus, le lendemain un peu moins, simplement à cause du hasard,
comme quand on lance une pièce 100 fois et qu'on n'obtient pas toujours 50 piles.<br><br>
La loi binomiale (vue en cours) calcule cette zone de variation normale. Le graphique
de gauche la dessine deux fois, pour le nombre de joueurs actifs attendu dans un an : en gris,
le nombre d'acheteurs par jour avec la part d'acheteurs d'aujourd'hui ; en vert, celui que l'on
aurait avec la part d'acheteurs du scénario choisi plus haut.
Plus la courbe est haute à un endroit, plus ce nombre d'acheteurs est probable.<br><br>
Si les deux courbes se chevauchent beaucoup, une hausse pourrait n'être que du hasard.
Si elles sont bien séparées, la hausse est réelle. Le graphique de droite vérifie que le
montant dépensé à chaque achat ne bouge pas, avec le test t de Student du cours.
</div>
""", unsafe_allow_html=True)

p_apres = part_acheteurs / 100
n_joueurs = int(round(joueurs_actifs_moy))
n_joueurs_apres = int(round(joueurs_avec[365]))

bas_avant, haut_avant = stats.binom.interval(0.95, n_joueurs_apres, p_actuel)
bas_apres, haut_apres = stats.binom.interval(0.95, n_joueurs_apres, p_apres)

x_min = int(min(stats.binom.ppf(0.0005, n_joueurs_apres, p_actuel), stats.binom.ppf(0.0005, n_joueurs_apres, p_apres)))
x_max = int(max(stats.binom.ppf(0.9995, n_joueurs_apres, p_actuel), stats.binom.ppf(0.9995, n_joueurs_apres, p_apres)))
valeurs = np.arange(x_min, x_max + 1)

loi = pd.concat([
    pd.DataFrame({"acheteurs": valeurs, "probabilite": stats.binom.pmf(valeurs, n_joueurs_apres, p_actuel),
                  "situation": f"Part d'acheteurs d'aujourd'hui ({p_actuel:.1%})".replace(".", ",")}),
    pd.DataFrame({"acheteurs": valeurs, "probabilite": stats.binom.pmf(valeurs, n_joueurs_apres, p_apres),
                  "situation": f"Part d'acheteurs avec les actions ({part_acheteurs:.1f} %)".replace(".", ",")}),
])

gauche, droite = st.columns(2)

with gauche:

    st.subheader("Nombre d'acheteurs par jour")

    domaine_loi = list(loi["situation"].unique())

    graphique_loi = (
        alt.Chart(loi)
        .mark_area(opacity=0.55, line=True)
        .encode(
            x=alt.X("acheteurs:Q", title="Nombre d'acheteurs en une journée"),
            y=alt.Y("probabilite:Q", title="Probabilité", axis=alt.Axis(format="%")),
            color=alt.Color("situation:N", title=None,
                            scale=alt.Scale(domain=domaine_loi, range=["#9A8CA6", MENTHE]),
                            legend=alt.Legend(orient="bottom")),
            tooltip=[
                alt.Tooltip("situation:N", title="Situation"),
                alt.Tooltip("acheteurs:Q", title="Acheteurs"),
                alt.Tooltip("probabilite:Q", title="Probabilité", format=".2%"),
            ],
        )
        .properties(height=340)
    )

    st.altair_chart(style_graphique(graphique_loi), theme=None, use_container_width=True)

with droite:

    st.subheader("Panier moyen par mois")

    ventes["panier"] = ventes["revenus_euros"] / ventes["acheteurs"]
    ventes["mois"] = ventes["date"].dt.month

    paniers_mois = []
    for mois in sorted(ventes["mois"].unique()):
        valeurs_mois = ventes[ventes["mois"] == mois]["panier"]
        bas, haut = stats.t.interval(0.95, len(valeurs_mois) - 1,
                                     valeurs_mois.mean(), stats.sem(valeurs_mois))
        paniers_mois.append({"mois": MOIS[mois - 1].capitalize(), "panier": valeurs_mois.mean(),
                             "bas": bas, "haut": haut})
    paniers_mois = pd.DataFrame(paniers_mois)

    base_p = alt.Chart(paniers_mois).encode(
        x=alt.X("mois:N", title="Mois", sort=list(paniers_mois["mois"]),
                axis=alt.Axis(labelAngle=0))
    )
    barres_p = base_p.mark_errorbar(color="#4A3B52", thickness=2).encode(
        y=alt.Y("bas:Q", title="Panier moyen d'un acheteur (en euros)",
                scale=alt.Scale(domain=[6, 7.2]),
                axis=alt.Axis(labelExpr="replace(format(datum.value, '.1f'), '.', ',')")),
        y2="haut:Q"
    )
    points_p = base_p.mark_point(size=160, filled=True, color=LAVANDE).encode(
        y="panier:Q",
        tooltip=[alt.Tooltip("mois:N", title="Mois"),
                 alt.Tooltip("panier:Q", title="Panier moyen (€)", format=".2f")]
    )

    st.altair_chart(style_graphique((barres_p + points_p).properties(height=340)),
                    theme=None, use_container_width=True)

t_test = stats.ttest_ind(
    ventes[ventes["mois"] == 7]["panier"], ventes[ventes["mois"] == 9]["panier"]
)
abonnes_pass = n_joueurs_apres * part_pass / 100 * (pass_en_place[365] > 0)
revenu_pass_mois = abonnes_pass * prix_pass
acheteurs_battle = n_joueurs_apres * part_battle / 100 * (battle_en_place[365] > 0)
revenu_battle_mois = acheteurs_battle * prix_battle / 3

acheteurs_avant = n_joueurs * p_actuel
acheteurs_meme_part = n_joueurs_apres * p_actuel
acheteurs_apres = n_joueurs_apres * p_apres
en_plus_part = acheteurs_apres - acheteurs_meme_part
facteur = acheteurs_apres / acheteurs_avant

part_avant_txt = f"{p_actuel * 100:.1f}".replace(".", ",")
part_apres_txt = f"{part_acheteurs:.1f}".replace(".", ",")
facteur_txt = f"{facteur:.0f}"

se_voit = bas_apres > haut_avant

if se_voit:
    phrase_hasard = (
        "Pour le même nombre de joueurs, les deux courbes du graphique ne se touchent pas : "
        "passer de la part d'acheteurs d'aujourd'hui à celle du scénario se verrait tout de suite "
        "dans les ventes, ce n'est pas un effet du hasard."
    )
else:
    phrase_hasard = (
        "Les deux courbes du graphique se chevauchent : une bonne journée pourrait être "
        "due au hasard, il faudrait observer plusieurs jours avant de conclure que les "
        "actions fonctionnent."
    )

note_panier = str(round(ventes["panier"].mean(), 2)).replace(".", ",")

if len(retenues) == 0:
    phrase_amorti = "Sans action, Zeloria garde le rythme du pré-lancement."
elif amorti_avec is None:
    phrase_amorti = "Avec ces actions, Zeloria ne serait pas encore amorti dans les deux ans et demi."
elif amorti_sans is None:
    phrase_amorti = (
        f"Zeloria serait amorti en {en_toutes_lettres(amorti_avec)}, alors que sans action "
        "il ne le serait jamais."
    )
else:
    phrase_amorti = (
        f"Zeloria serait amorti en {en_toutes_lettres(amorti_avec)}, "
        f"au lieu de {en_toutes_lettres(amorti_sans)} sans action."
    )

paragraphe_pass = ""
if pass_en_place[365] > 0:
    paragraphe_pass = (
        f"<p>Le pass mensuel à {prix_pass} € attirerait {part_pass} % des joueurs actifs, soit "
        f"environ {espaces(abonnes_pass)} joueurs et environ {espaces(revenu_pass_mois)} € par mois.</p>"
    )

paragraphe_battle = ""
if battle_en_place[365] > 0:
    paragraphe_battle = (
        f"<p>Le pass de combat se vend une fois par saison de 3 mois, à "
        f"{str(prix_battle).replace('.', ',')} €. {part_battle} % des joueurs actifs l'achèteraient, "
        f"soit environ {espaces(acheteurs_battle)} joueurs par saison, ce qui représente environ "
        f"{espaces(revenu_battle_mois)} € par mois.</p>"
    )

st.markdown(
    f"""
<div class="carte carte-verdict">
<div class="etiquette">Ce qu'il faut retenir</div>
<p>Aujourd'hui, {part_avant_txt} % des joueurs actifs achètent chaque jour, soit environ
{espaces(acheteurs_avant)} acheteurs sur {espaces(n_joueurs)} joueurs. Avec les actions du scénario
{scenario.lower()}, Zeloria compterait dans un an environ {espaces(n_joueurs_apres)} joueurs actifs.
Avec la même part d'acheteurs qu'aujourd'hui, cela ferait déjà {espaces(acheteurs_meme_part)}
acheteurs par jour. Grâce aux actions, {part_apres_txt} % de ces joueurs achèteraient, soit environ
{espaces(acheteurs_apres)} acheteurs par jour, {espaces(en_plus_part)} de plus. Au total, il y aurait
environ {facteur_txt} fois plus d'acheteurs qu'aujourd'hui.</p>

<p>{phrase_hasard}</p>

<p>Le montant dépensé à chaque achat ne change pas : {note_panier} € en moyenne, d'un mois à
l'autre. Pour gagner plus, il faut donc plus d'acheteurs, et non des achats plus chers.</p>

{paragraphe_pass}{paragraphe_battle}<p>{phrase_amorti}</p>
</div>
""",
    unsafe_allow_html=True
)