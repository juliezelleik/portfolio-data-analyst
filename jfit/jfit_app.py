import os

import streamlit as st

try:
    st.set_page_config(
        page_title="JFIT - Site vitrine",
        layout="wide"
    )
except st.errors.StreamlitAPIException:
    pass

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# Palette du site JFIT
BLEU = "#7FB8CC"
VIOLET = "#8B5CF6"
CORAIL = "#F0605A"


#  STYLE

st.markdown("""
<style>

.stApp {
    background: #0E1117;
}

h1, h2, h3, p, li, label, span, div[data-testid="stMetricValue"],
div[data-testid="stMetricLabel"], div[data-testid="stHeading"] * {
    color: #EAE6F3;
}

.stButton > button {
    background: #8B5CF6;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 8px 18px;
}

.stButton > button:hover {
    background: #7442E8;
    color: #FFFFFF;
}

.stButton > button p {
    color: #FFFFFF;
}

.titre-jfit {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    margin-bottom: 0;
    color: #EAE6F3;
}

.titre-jfit span {
    color: #8B5CF6;
}

.sous-titre {
    text-align: center;
    font-size: 22px;
    color: #7FB8CC;
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
    background: #17303A;
    border: 2px solid #7FB8CC;
}

.carte-question {
    background: #2A2145;
    border: 2px solid #8B5CF6;
}

.carte-verdict {
    background: #3A1F22;
    border: 2px solid #F0605A;
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

.etiquette {
    font-weight: 800;
    font-size: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.bouton-site {
    display: block;
    padding: 20px 26px;
    border-radius: 22px;
    margin-bottom: 18px;
    background: #8B5CF6;
    color: #FFFFFF !important;
    font-size: 22px;
    font-weight: 800;
    text-align: center;
    text-decoration: none !important;
}

.bouton-site:hover {
    background: #7442E8;
}

div[data-testid="stMetric"] {
    background: #1A1F2B;
    border: 2px solid #7FB8CC;
    padding: 16px;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)


#  LE PROJET

st.markdown('<div class="titre-jfit">JFIT<span>.</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sous-titre">Site vitrine d\'un club de sport</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="carte carte-histoire">
<div class="etiquette">Le projet</div>
JFIT est un club de sport fictif qui propose 7 cours collectifs du lundi au samedi : yoga,
vélo, boxe, danse, step et circuit training. J'ai créé son site vitrine en PHP et MySQL,
avec 3 pages : l'accueil, le planning de la semaine et la présentation des cours.
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<a class="bouton-site" href="https://jfit.infinityfreeapp.com" target="_blank">Voir le site</a>',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="pastille">Données fictives</span>',
    unsafe_allow_html=True
)

st.divider()


#  1. LA BASE DE DONNEES

st.header("1. La base de données")

k1, k2, k3 = st.columns(3)
k1.metric("Cours collectifs", "7")
k2.metric("Salles", "3")
k3.metric("Séances par semaine", "32")

st.markdown("""
La base contient 3 tables :
- **salle** : les espaces du club (salle co, salle vélo, plateau muscu)
- **cours** : les activités, avec leur description, leur intensité et leur durée
- **seance** : le planning, chaque ligne est un créneau (un cours, un jour, une heure)
""")

st.code("""CREATE TABLE seance (
  id_seance INT AUTO_INCREMENT PRIMARY KEY,
  id_cours INT NOT NULL,
  jour INT NOT NULL,
  debut TIME NOT NULL,
  fin TIME NOT NULL,
  FOREIGN KEY (id_cours) REFERENCES cours(id_cours)
);""", language="sql")


#  2. LE PLANNING

st.divider()

st.header("2. Le planning")

gauche, droite = st.columns([1, 1.2])

with gauche:

    st.subheader("La requête")

    st.code("""SELECT s.jour,
       TIME_FORMAT(s.debut, '%Hh%i') AS debut,
       TIME_FORMAT(s.fin, '%Hh%i') AS fin,
       c.nom AS cours, sa.nom AS salle
FROM seance s
JOIN cours c ON c.id_cours = s.id_cours
JOIN salle sa ON sa.id_salle = c.id_salle
ORDER BY s.debut, s.jour, c.nom""", language="sql")

with droite:

    st.subheader("Le résultat")
    st.image(os.path.join(DOSSIER, "apercu_planning.png"), use_container_width=True)

st.markdown("""
<div class="carte carte-verdict">
Le planning se construit tout seul à partir de la base : si une séance change dans la table seance,
la grille se met à jour sans modifier le reste du code.
</div>
""", unsafe_allow_html=True)


#  3. LES CHOIX TECHNIQUES

st.divider()

st.header("3. Les choix techniques")

st.markdown("""
- **Un header et un footer communs** à toutes les pages : le menu n'est écrit qu'une fois
- **Le mot de passe de la base est isolé** dans un fichier à part, pour garantir la sécurité des données
- **Une couleur par cours**, reprise dans le planning et sur les fiches des cours
""")

gauche, droite = st.columns(2)

with gauche:
    st.subheader("L'accueil")
    st.image(os.path.join(DOSSIER, "apercu_accueil.png"), use_container_width=True)

with droite:
    st.subheader("Les cours")
    st.image(os.path.join(DOSSIER, "apercu_cours.png"), use_container_width=True)