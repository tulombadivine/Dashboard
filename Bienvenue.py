import streamlit as st
from io import BytesIO
import requests



#FASTAPI_SERVER = 'https://dsoc-p7-api-019616fdcaac.herokuapp.com'
FASTAPI_SERVER= 'http://127.0.0.1:8000'

# Fonction pour récupérer l'image de l'API
def get_image_from_api(image_name):
    url = f"{FASTAPI_SERVER}/image/{image_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None
    
# Nom des images
images_names = ["intro",'pred', 'explo']

st.set_page_config(page_title="Bienvenue",layout="wide")


# Création des onglets
tab1, tab2, tab3 = st.tabs(["Introduction", "Page de Prédictions", "Page d'Exploration"])

with tab1:
    st.title("Dashboard de Scoring Crédit - Projet OpenClassrooms")
    col1, col2 = st.columns(2)
    # Titre de la page d'accueil
    with col1:
        # Sous-titre et introduction
        st.subheader("Mon Expérience en Data Science")
        st.write(
            "Ce Dashboard intervient dans le cadre de ma formation de Data Scientist avec OpenClassrooms. "
            "Le défi consiste à développer un outil de scoring crédit capable de prédire la probabilité de remboursement d'un crédit par un client. "
            "L'objectif est de créer un algorithme de classification utilisant une variété de sources de données, y compris des données comportementales et des informations issues d'autres institutions financières. "
            "Ce tableau de bord a deux objectifs principaux :"
        )
        st.write("1. **Présenter les Prédictions** : Il offre une vue d'ensemble des prédictions de remboursement de crédit, en aidant à classifier les demandes en crédit accordé ou refusé.")
        st.write("2. **Faciliter l'Exploration des Données** : Il permet aux clients de l'entreprise et à ses conseillers de naviguer aisément à travers les informations personnelles et les facteurs déterminants dans les décisions de crédit.")
        st.write(
            "Ce projet a été une étape cruciale dans mon apprentissage, me permettant de développer des compétences pratiques en science des données tout en apportant une solution concrète à un problème du monde réel."
        )
    with col2: 
        image1 = get_image_from_api(images_names[0])
        if image1:
            st.image(image1)
        else:
            st.error(f"L'image {images_names[0]} n'a pas pu être chargée")

    # Lien vers le cursus Data Scientist d'OpenClassrooms
    st.markdown("""
        <style>
        .centered-text {
            text-align: center;
        }
        </style>
        <p class="centered-text">Pour en savoir plus sur le cursus Data Scientist d'OpenClassrooms, cliquez <a href="https://openclassrooms.com/fr/paths/793-data-scientist" target="_blank">ici</a>.</p>
        """, unsafe_allow_html=True)

with tab2:
    # Description de la page de Prédictions
    col1, col2, col3 ,col4  = st.columns([1,2,3,1])
    with col2:
        st.markdown("## Page de Prédictions")
        st.write("""
        Sur cette page, l'utilisateur commence par sélectionner un Client ID à partir d'une liste déroulante. Une fois un client choisi, le dashboard lance une prédiction sur la probabilité que ce client rembourse son crédit. Cette prédiction est basée sur un modèle de machine learning entraîné sur des données historiques.

        Dans la barre latérale (sidebar), des variables clés associées au client sélectionné apparaissent. L'utilisateur peut cliquer sur ces variables pour obtenir des détails supplémentaires. Ces informations aident à comprendre les facteurs qui ont influencé la décision de prédiction du modèle.
        """)

    with col3:
        image2 = get_image_from_api(images_names[1])
        if image2:
            st.image(image2)
        else:
            st.error(f"L'image {images_names[1]} n'a pas pu être chargée")


with tab3:
    # Description de la page d'Exploration
    col1, col2, col3 , col4  = st.columns([1,2,3,1])
    with col2:
        st.markdown("## Page d'Exploration")
        st.write("""
        La page d'Exploration offre une vue plus approfondie des données. Ici, l'utilisateur peut sélectionner deux variables pour créer un scatter plot interactif. Ce graphique aide à visualiser les relations et les tendances entre différentes variables des données de crédit.

        De plus, cette page permet également de sélectionner un Client ID spécifique. En choisissant un client, l'utilisateur peut voir ou il se situe par rapport aux autres clients éligibles ou non.
        """)
    
    with col3:
        image3 = get_image_from_api(images_names[2])
        if image3:
            st.image(image3)
        else:
            st.error(f"L'image {images_names[2]} n'a pas pu être chargée")
    






