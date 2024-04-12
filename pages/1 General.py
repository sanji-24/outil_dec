import streamlit as st
import pandas as pd

# Titre de la page
st.title('Portrait du territoire')

# Charger les données (remplacez cela par vos propres données)
data = pd.read_csv("nouvelle_base.csv")

# Diviser la page en deux colonnes
left_column, right_column = st.columns(2)

# Filtrer les villes pour la colonne de gauche
with left_column:
    selected_city_left = st.selectbox("Choisissez une ville départ", [""] + list(data["city_code"].unique()))

    if selected_city_left:  # Vérifie si une ville est sélectionnée
        city_data_left = data[data["city_code"] == selected_city_left]

        # Afficher la carte avec la latitude et la longitude
        st.map(city_data_left[["latitude", "longitude"]].drop_duplicates())

        # Afficher les informations sur la ville
        st.write("Nombre d'habitants :", city_data_left["Nombre.d.habitants"].iloc[0])
        st.write("Type d'agglomération :", city_data_left["Type.d.agglomeration"].iloc[0])
        st.write("Nom de la région :", city_data_left["region_name"].iloc[0])

# Filtrer les villes pour la colonne de droite
with right_column:
    selected_city_right = st.selectbox("Choisissez une ville souhaitée", [""] + list(data["city_code"].unique()))

    if selected_city_right:  # Vérifie si une ville est sélectionnée
        city_data_right = data[data["city_code"] == selected_city_right]

        # Afficher la carte avec la latitude et la longitude
        st.map(city_data_right[["latitude", "longitude"]].drop_duplicates())

        # Afficher les informations sur la ville
        st.write("Nombre d'habitants :", city_data_right["Nombre.d.habitants"].iloc[0])
        st.write("Type d'agglomération :", city_data_right["Type.d.agglomeration"].iloc[0])
        st.write("Nom de la région :", city_data_right["region_name"].iloc[0])

