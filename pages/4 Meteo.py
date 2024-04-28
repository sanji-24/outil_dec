import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime


def load_data():
    df = pd.read_csv("donnees_selectionnees.csv")
    return df

data = load_data()
# Suppression des lignes avec des données manquantes pour toutes les variables
data = data.dropna()

# Création du menu de sélection des départements
departements = sorted(data['department (name)'].dropna().unique())
departement1 = st.selectbox('Sélectionnez le premier département:', departements)
departement2 = st.selectbox('Sélectionnez le deuxième département:', departements)

# Sélection de la saison
saison = st.radio("Sélectionnez une saison:", ['Été', 'Automne', 'Hiver', 'Printemps'])

# Filtrage des données en fonction de la saison sélectionnée
saison_mapping = {'Été': [6, 7, 8], 'Automne': [9, 10, 11], 'Hiver': [12, 1, 2], 'Printemps': [3, 4, 5]}
mois_saison = saison_mapping[saison]
filtered_data = data[data['Annee_Mois'].astype(str).str[-2:].astype(int).isin(mois_saison)]

# Filtrage des données en fonction des départements sélectionnés
filtered_data = filtered_data[(filtered_data['department (name)'] == departement1) | (filtered_data['department (name)'] == departement2)]

# Calcul des moyennes d'humidité pour chaque département
humidite_departement1 = filtered_data[filtered_data['department (name)'] == departement1]['Humidité'].mean()
humidite_departement2 = filtered_data[filtered_data['department (name)'] == departement2]['Humidité'].mean()

# Création des données pour le diagramme circulaire
labels = [departement1, departement2]
humidites = [humidite_departement1, humidite_departement2]

# Création du diagramme circulaire avec Plotly
fig = px.pie(names=labels, values=humidites, title="Pourcentage moyen d'humidité par département")
st.plotly_chart(fig)
#________________________________________________________________#

####évolution moyenne de la température

# Création du menu de sélection des départements
departements = sorted(data['department (name)'].dropna().unique())
departement1 = st.selectbox('Sélectionnez le premier département:', departements, key="departement1")
departement2 = st.selectbox('Sélectionnez le deuxième département:', departements, key="departement2")

# Filtrage des données en fonction des départements sélectionnés
filtered_data_departement1 = data[data['department (name)'] == departement1]
filtered_data_departement2 = data[data['department (name)'] == departement2]

# Calcul des moyennes de température par mois pour chaque département
mean_temp_departement1 = filtered_data_departement1.groupby('Annee_Mois')['Température (°C)'].mean().reset_index()
mean_temp_departement2 = filtered_data_departement2.groupby('Annee_Mois')['Température (°C)'].mean().reset_index()

# Création du diagramme de comparaison de l'évolution moyenne de la température
fig = px.line(mean_temp_departement1, x='Annee_Mois', y='Température (°C)', title=f'Évolution moyenne de la température - {departement1} vs {departement2}')
fig.add_scatter(x=mean_temp_departement2['Annee_Mois'], y=mean_temp_departement2['Température (°C)'], mode='lines', name=departement2)
st.plotly_chart(fig)

    #________________________________________________________________#

###### Analyse de la température

# Choix de l'option d'analyse (région ou département)
analyse_option = st.radio("Choisissez l'option d'analyse:", ['Région', 'Département'])

if analyse_option == 'Région':
    # Calcul des statistiques pour chaque région
    stats_temp_region = data.groupby('region (name)')['Température (°C)'].mean().reset_index()
    stats_temp_region = stats_temp_region.sort_values(by='Température (°C)', ascending=False)
    stats_temp_region = stats_temp_region.rename(columns={'region (name)': 'Nom de la région'})

    # Affichage du diagramme en barres pour les cinq régions les plus chaudes et les cinq régions les plus froides
    fig = px.bar(stats_temp_region.head(5), x='Nom de la région', y='Température (°C)', title='Cinq régions les plus chaudes')
    st.plotly_chart(fig)

    fig = px.bar(stats_temp_region.tail(5), x='Nom de la région', y='Température (°C)', title='Cinq régions les plus froides')
    st.plotly_chart(fig)

else:  # Analyse par département
    # Calcul des statistiques pour chaque département
    stats_temp_departement = data.groupby('department (name)')['Température (°C)'].mean().reset_index()
    stats_temp_departement = stats_temp_departement.sort_values(by='Température (°C)', ascending=False)
    stats_temp_departement = stats_temp_departement.rename(columns={'department (name)': 'Nom du département'})

    # Affichage du diagramme en barres pour les dix départements les plus chauds et les dix départements les plus froids
    fig = px.bar(stats_temp_departement.head(10), x='Nom du département', y='Température (°C)', title='Dix départements les plus chauds')
    st.plotly_chart(fig)

    fig = px.bar(stats_temp_departement.tail(10), x='Nom du département', y='Température (°C)', title='Dix départements les plus froids')
    st.plotly_chart(fig)

#________________________________________________________________##________________________________________________________________#
