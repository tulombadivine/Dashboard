import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Exploration",layout="wide")

# Serveur fastAPI
FASTAPI_SERVER = 'https://app-opc-01e0e62f2bf5.herokuapp.com'
#FASTAPI_SERVER= 'http://127.0.0.1:8000'

st.markdown("<h1 style='text-align: center;'>Exploration</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Récupère les out de l'API
# liste des variables et les données pour la visualisation
@st.cache_data
def get_data():
    response = requests.get(f'{FASTAPI_SERVER}/prediction_for_all')
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to retrieve data')
        return {}
    
# liste des clients
@st.cache_data
def get_client_list():
    response = requests.get(f'{FASTAPI_SERVER}/list_client')
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to retrieve client list')
        return []
    
with st.spinner('Loading...'):
    # Récupère les données
    data = get_data()
    df = pd.DataFrame(data['data_viz'])
    df['Prediction'] = df['Prediction'].map({"0": 'Eligible', "1": 'Not eligible'})
    variables = data['list_var']

    # Sélection des variables pour les axes x et y
    with col2:
        x_var = st.selectbox('Select variable for X axis:', variables)
    with col3:
        y_var = st.selectbox('Select variable for Y axis:', variables)

    # Choix de l'ID du client
    with col1:
        client_id = st.selectbox('Select a Client ID:', get_client_list())

if st.button('Visualization'):
    # Crée le scatter plot avec Plotly
    client_id = str(client_id)
    if x_var and y_var:
        # Création du scatter plot
        fig = px.scatter(df, x=x_var, y=y_var, color='Prediction',
                 color_discrete_map={'Not Eligible': 'yellow', 'Eligible': 'red'})

        # Mise en évidence de le client
        ID_mask = df['SK_ID_CURR'] == client_id
        fig.add_scatter(x=df[ID_mask][x_var], y=df[ID_mask][y_var], 
                        mode='markers', marker=dict(color='green', size=15),
                        name='You')

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
