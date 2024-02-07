import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="Prediction",layout="wide")

# Localisation du serveur fastAPI
FASTAPI_SERVER = 'https://app-opc-01e0e62f2bf5.herokuapp.com'
#FASTAPI_SERVER= 'http://127.0.0.1:8000'
st.markdown("<h1 style='text-align: center;'>Loan eligibilty</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,0.5,2])

# Récupération des différents out des fonctions API
## liste des clients
@st.cache_data
def get_client_list():
    response = requests.get(f'{FASTAPI_SERVER}/list_client')
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to retrieve client list')
        return []

## adresses clients
def get_client_address(client_id):
    response = requests.post(f'{FASTAPI_SERVER}/client_adress', json={"client_id": client_id})
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to retrieve client address')
        return None

## prédiction 
def predict_for_client(client_id):
    response = requests.post(f'{FASTAPI_SERVER}/predict_for_client', json={"client_id": client_id})
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to retrieve prediction')
        return None

## rechercher une image 
def get_image(image_name):
    response = requests.get(f'{FASTAPI_SERVER}/image/{image_name}')
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error('Failed to retrieve image')
        return None

# Initialise le session state pour permettre la permanence ou non d'affichage
if 'selected_feature' not in st.session_state:
    st.session_state['selected_feature'] = None
if 'prediction_result' not in st.session_state:
    st.session_state['prediction_result'] = None
if 'eligibility_message' not in st.session_state:
    st.session_state['eligibility_message'] = ''
if 'right_score' not in st.session_state:
    st.session_state['right_score'] = None
if 'lime_image' not in st.session_state:
    st.session_state['lime_image'] = None
if 'global_image' not in st.session_state:
    st.session_state['global_image'] = None
if 'lime_importance_plot' not in st.session_state:
    st.session_state['lime_importance_plot'] = None


with st.sidebar:
    st.header("Features")

# Sélection de l'ID du client
with col1:
    client_list = get_client_list()
    client_id = st.selectbox('Select ID:', client_list)

# Affichage de l'adresse du client et exécution de la prédiction
if client_id:
    with col1:
        # Affichage des données clients à la selection de l'ID
        client_address = get_client_address(client_id)
        if client_address:
            st.write(f"Client ID: {client_id}")
            st.write(f"First Name: {client_address['first_name']}")
            st.write(f"Last Name: {client_address['last_name']}")
            st.write(f"Address: {client_address['adress']}")

        # A l'activation de la prédiction
        if st.button('Launch Prediction'):
            # reset des session_state
            st.session_state.eligibility_message = ''
            st.session_state.prediction_result = None
            st.session_state.selected_feature = None
            st.session_state.global_image = None
            
            with st.spinner('Loading...'):
                st.session_state.prediction_result = predict_for_client(client_id)
                if st.session_state.prediction_result['prediction'][0] == 1:
                    st.session_state.eligibility_message = "Loan not available"
                else:
                    st.session_state.eligibility_message = "You can purchase a loan"


                # Vérifie si right_score est dans la réponse et l'afficher dans une jauge
                if 'right_score' in st.session_state.prediction_result:
                    right_score = st.session_state.prediction_result['right_score']
                    score_percentage = right_score * 100
                    # Utilisation de HTML/CSS pour créer la barre de progression personnalisée
                    score_position = score_percentage - 2.5  # Centrer le marqueur de score

                    # Calcule les positions relatives pour le texte
                    not_allowed_position = 25 - (len("Loan Available") / 2)  # ajuster en fonction de la longueur du texte
                    loan_available_position = 75 - (len("Not Allowed") / 2)  # ajuster en fonction de la longueur du texte

                    # Définir la couleur en fonction de score_percentage
                    fill_color = "#76b900" if score_percentage <= 50 else "#ff0000"  # Vert si 50% ou moins, Rouge sinon

                    # Utilisation de HTML/CSS pour créer la barre de progression personnalisée
                    progress_bar_html = f"""
                    <style>
                    .progress-bar-container {{
                    width: 100%;
                    background-color: #eee;
                    border-radius: 10px;
                    position: relative;
                    height: 20px;
                    margin-bottom: 5px; /* Espace entre la barre et les labels */
                    }}

                    .progress-bar-fill {{
                    width: {score_percentage}%;
                    background-color: {fill_color};
                    height: 20px;
                    position: absolute;
                    z-index: 1;
                    }}

                    .progress-bar-grey-zone {{
                    position: absolute;
                    left: 49%;
                    width: 2%; /* Largeur de la zone grise */
                    background-color: grey;
                    height: 20px;
                    z-index: 2; /* Assurez-vous que la zone grise soit au-dessus du remplissage */
                    }}

                    .progress-bar-labels {{
                    display: flex;
                    justify-content: space-between;
                    position: relative;
                    width: 100%;
                    padding-top: 25px; /* Ajustez la valeur pour la position verticale des labels */
                    }}

                    .progress-bar-labels span {{
                    font-size: 0.8em;
                    }}
                    </style>

                    <div class="progress-bar-container">
                    <div class="progress-bar-fill"></div>
                    <div class="progress-bar-grey-zone"></div>
                    </div>
                    <div class="progress-bar-labels">
                    <span style="position: absolute; left: 0%;">Loan Available</span>
                    <span style="position: absolute; right: 0%;">Not Allowed</span>
                    </div>
                    """

                    st.session_state.right_score = progress_bar_html
                    

                    # statement du graph LIME
                    if 'lime_importance_plot' in st.session_state.prediction_result:
                        lime_image_encoded = st.session_state.prediction_result['lime_importance_plot']
                        st.session_state.lime_importance_plot = lime_image_encoded

                    # statement du graphique SHAP
                    st.session_state.global_image = get_image('shap_bee')

with col1: 
    # Affiche le message d'éligibilité
    if st.session_state.eligibility_message:
        if "not" in st.session_state.eligibility_message:
            st.error(st.session_state.eligibility_message)
        else:
            st.success(st.session_state.eligibility_message) 
    # Affiche la barre de progression       
    if st.session_state.right_score:
        st.markdown(st.session_state.right_score, unsafe_allow_html=True)
        spacer1 = st.empty()
        spacer1.markdown(" ")
        spacer2 = st.empty()
        spacer2.markdown(" ")

with col3:        
    # Récupère et afficher l'image de prédiction globale  (SHAP)
    if  st.session_state.global_image:
        st.image(st.session_state.global_image, caption='Global Importance')
        spacer = st.empty()
        spacer.markdown(" ")
        spacer1 = st.empty()
        spacer1.markdown(" ")
        spacer2 = st.empty()
        spacer2.markdown(" ")

    # Récupère et afficher l'image de prédiction locale (LIME)    
    if st.session_state.lime_importance_plot:
         lime_image = base64.b64decode(st.session_state.lime_importance_plot)
         lime_image = Image.open(BytesIO(lime_image))
         st.image(lime_image, caption="Local Prediction Importance")             

# Création de boutons dans la sidebar pour chaque caractéristique
if st.session_state.prediction_result:
    features = st.session_state.prediction_result['local_importance']['Feature']
    importances = st.session_state.prediction_result['local_importance']['Importance']
    for index in features.keys():
        feature_name = features[index]
        importance = importances[index]
        unique_key = f"feature_{client_id}_{index}"
        if st.sidebar.button(f"{feature_name}", key=unique_key):
            st.session_state.selected_feature = feature_name

# Affichage des détails de la caractéristique sélectionnée
if st.session_state.selected_feature and st.session_state.prediction_result:
    with col1:
        feature_name = st.session_state.selected_feature
        # Trouve l'index de la caractéristique sélectionnée
        index_of_feature = None
        for index, name in st.session_state.prediction_result['local_importance']['Feature'].items():
            if name == feature_name:
                index_of_feature = index
                break

        if index_of_feature is not None and index_of_feature in st.session_state.prediction_result['local_importance']['Importance']:
            importance = st.session_state.prediction_result['local_importance']['Importance'][index_of_feature]
            #client_value = st.session_state.prediction_result['client_data'][feature_name]
            if importance>0:
                st.error(f"Selected Feature: {feature_name}")
                st.error(f"Local Importance: {importance}")
            elif importance<0:
                st.success(f"Selected Feature: {feature_name}")
                st.success(f"Local Importance: {importance}")

            #st.write(f"Client Value: {client_value}")
            kde_image = get_image(f"{feature_name}_kde")
            if kde_image:
                st.image(kde_image, caption=f"{feature_name} KDE")

# Run le script en utilisant (local):
# streamlit run streamlit_dashboard.py
