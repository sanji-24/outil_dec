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

#######Comparaison des caractéristiques départementales

# Sélection des deux départements à comparer
departement1 = st.selectbox("Sélectionnez le premier département:", data['department (name)'].unique())
departement2 = st.selectbox("Sélectionnez le deuxième département:", data['department (name)'].unique())

# Filtrage des données pour les deux départements sélectionnés
data_departement1 = data[data['department (name)'] == departement1]
data_departement2 = data[data['department (name)'] == departement2]

# Calcul des moyennes pour chaque variable pour les deux départements
stats_departement1 = data_departement1[['Température (°C)', 'Humidité', 'Vitesse du vent moyen 10 mn', 'Nebulosité totale']].mean()
stats_departement2 = data_departement2[['Température (°C)', 'Humidité', 'Vitesse du vent moyen 10 mn', 'Nebulosité totale']].mean()

# Variables
labels = ['Température (°C)', 'Humidité', 'Vitesse du vent moyen 10 mn', 'Nebulosité totale']
stats1 = stats_departement1.values
stats2 = stats_departement2.values

# Nombre de variables
num_vars = len(labels)

# Création des angles pour chaque variable
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Rotation pour démarrer l'axe à 12h au lieu de 3h
angles += angles[:1]

# Création du graphique radar
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))  # Modification de la taille ici
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Dessiner une ligne pour chaque département
ax.plot(angles, stats1.tolist() + stats1[:1].tolist(), 'o-', linewidth=2, label=departement1)
ax.fill(angles, stats1.tolist() + stats1[:1].tolist(), alpha=0.25)

ax.plot(angles, stats2.tolist() + stats2[:1].tolist(), 'o-', linewidth=2, label=departement2)
ax.fill(angles, stats2.tolist() + stats2[:1].tolist(), alpha=0.25)

# Ajouter des étiquettes pour chaque variable
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Ajouter une légende
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# Titre
plt.title('Comparaison des caractéristiques départementales')

# Afficher le graphique
st.pyplot(fig)

##________________________________________________________________##

# Convertir la colonne 'Annee_Mois' en format datetime
data['Annee_Mois'] = pd.to_datetime(data['Annee_Mois'])

# Filtrer les données pour la température
df_temp = data[['Annee_Mois', 'Température (°C)']].dropna()

# Filtrer les données d'entraînement
train_data = df_temp[df_temp['Annee_Mois'] < '2022-01-01']
X_train = train_data['Annee_Mois'].apply(lambda x: x.toordinal()).values.reshape(-1, 1)
y_train = train_data['Température (°C)'].values

# Entraînement du modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Prédiction pour 2023/2024
future_dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M').to_series().apply(lambda x: x.toordinal()).values.reshape(-1, 1)
predictions = model.predict(future_dates)

# Affichage avec Streamlit
st.title('Prédiction de température pour 2023-2024')
st.write('Graphique nuage de points avec régression linéaire')

# Création du graphique
plt.figure(figsize=(12, 6))
plt.scatter(train_data['Annee_Mois'], train_data['Température (°C)'], color='blue', label='Données d\'entraînement')
plt.plot(pd.date_range(start='2022-01-01', end='2024-12-31', freq='M'), model.predict(np.arange(pd.to_datetime('2022-01-01').toordinal(), pd.to_datetime('2025-01-01').toordinal()).reshape(-1, 1)), color='red', label='Prédiction')
plt.xlabel('Date')
plt.ylabel('Température (°C)')
plt.title('Prédiction de température')
plt.legend()
plt.xticks(rotation=45)
st.pyplot(plt)

