import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Charger les données depuis le fichier CSV
@st.cache_data
def load_data():
    data = pd.read_csv('france.csv', delimiter=';')
    # Filtrer les données pour ne garder que les catégories 'ABC'
    filtered_data = data[data['Catégorie'].isin(['ABC'])]
    return filtered_data

# Charger les données
data = load_data()

# Diviser la page en deux colonnes
left_column, right_column = st.columns(2)

# Sélectionner une région - colonne de gauche
with left_column:
    default_region_left = "Sélectionnez une région"
    region_options_left = sorted(data['Nom Officiel Région'].unique())
    region_left = st.selectbox('Sélectionnez une région (Gauche)', [default_region_left] + region_options_left)

# Sélectionner une région - colonne de droite
with right_column:
    default_region_right = "Sélectionnez une région"
    region_options_right = sorted(data['Nom Officiel Région'].unique())
    region_right = st.selectbox('Sélectionnez une région (Droite)', [default_region_right] + region_options_right)

# Filtrer les données en fonction de la région sélectionnée
if region_left != default_region_left:
    filtered_data_left = data[data['Nom Officiel Région'] == region_left]

    # Sélectionner un département dans la région sélectionnée - colonne de gauche
    with left_column:
        default_department_left = "Sélectionnez un département"
        department_options_left = sorted(filtered_data_left['Nom Officiel Département'].unique())
        department_left = st.selectbox('Sélectionnez un département (Gauche)', [default_department_left] + department_options_left)

    # Afficher les données filtrées et les graphiques - colonne de gauche
    with left_column:
        if department_left != default_department_left:
            filtered_data_left = filtered_data_left[filtered_data_left['Nom Officiel Département'] == department_left]

            # Afficher les données filtrées
            # st.subheader('Données filtrées (Gauche)')
            # st.write(filtered_data_left)

# Filtrer les données en fonction de la région sélectionnée - colonne de droite
if region_right != default_region_right:
    filtered_data_right = data[data['Nom Officiel Région'] == region_right]

    # Sélectionner un département dans la région sélectionnée - colonne de droite
    with right_column:
        default_department_right = "Sélectionnez un département"
        department_options_right = sorted(filtered_data_right['Nom Officiel Département'].unique())
        department_right = st.selectbox('Sélectionnez un département (Droite)', [default_department_right] + department_options_right)

    # Afficher les données filtrées et les graphiques - colonne de droite
    with right_column:
        if department_right != default_department_right:
            filtered_data_right = filtered_data_right[filtered_data_right['Nom Officiel Département'] == department_right]

            # Afficher les données filtrées
            # st.subheader('Données filtrées (Droite)')
            # st.write(filtered_data_right)

# Comparaison des deux départements sélectionnés
if region_left != default_region_left and region_right != default_region_right:
    if department_left != default_department_left and department_right != default_department_right:
        # Filtrer les données pour les deux régions sélectionnées
        filtered_data_left_region = data[data['Nom Officiel Région'] == region_left]
        filtered_data_right_region = data[data['Nom Officiel Région'] == region_right]

        # Filtrer les données pour les deux départements sélectionnés dans chaque région
        filtered_data_left = filtered_data_left_region[filtered_data_left_region['Nom Officiel Département'] == department_left]
        filtered_data_right = filtered_data_right_region[filtered_data_right_region['Nom Officiel Département'] == department_right]

        # Créer un DataFrame pour la comparaison
        comparison_data = pd.concat([filtered_data_left, filtered_data_right])

        # Réinitialiser l'index du DataFrame de comparaison
        comparison_data.reset_index(drop=True, inplace=True)

        # Ajouter une colonne pour indiquer la région et le département
        comparison_data['Région'] = [region_left] * len(filtered_data_left) + [region_right] * len(filtered_data_right)
        comparison_data['Département'] = [department_left] * len(filtered_data_left) + [department_right] * len(filtered_data_right)

        # Afficher les données filtrées
        st.subheader('Comparaison des départements sélectionnés')
        st.write(comparison_data)

        # Graphique pour la comparaison des deux départements
        fig_comparison = px.bar(comparison_data, x='Période (Trimestre)', y='Nb moyen demandeur emploi', 
                                title=f'Comparaison du chômage entre {department_left} ({region_left}) et {department_right} ({region_right})',
                                labels={'Période (Trimestre)': 'Trimestre', 'Nb moyen demandeur emploi': 'Nombre moyen de demandeurs d\'emploi'},
                                color='Département')
        st.plotly_chart(fig_comparison, use_container_width=True)

# Comparaison des deux départements sélectionnés
if region_left != default_region_left and region_right != default_region_right:
    if department_left != default_department_left and department_right != default_department_right:
        filtered_data_left = data[data['Nom Officiel Région'] == region_left]
        filtered_data_right = data[data['Nom Officiel Région'] == region_right]

        filtered_data_left = filtered_data_left[filtered_data_left['Nom Officiel Département'] == department_left]
        filtered_data_right = filtered_data_right[filtered_data_right['Nom Officiel Département'] == department_right]

        # Créer un DataFrame pour la comparaison
        comparison_data = pd.concat([filtered_data_left, filtered_data_right])

        # Réinitialiser l'index du DataFrame de comparaison
        comparison_data.reset_index(drop=True, inplace=True)

        # Ajouter une colonne pour indiquer le département
        comparison_data['Département'] = [department_left] * len(filtered_data_left) + [department_right] * len(filtered_data_right)

        # Créer la colonne "Mois" à partir de la colonne "Date"
        comparison_data['Mois'] = pd.to_datetime(comparison_data['Date']).dt.month

        # Graphique pour la comparaison du nombre moyen de demandeurs d'emploi par mois
        fig_monthly_comparison = px.bar(comparison_data, x='Mois', y='Nb moyen demandeur emploi', 
                                        title=f'Comparaison du nombre moyen de demandeurs d\'emploi par mois entre {department_left} et {department_right}',
                                        labels={'Mois': 'Mois', 'Nb moyen demandeur emploi': 'Nombre moyen de demandeurs d\'emploi'},
                                        color='Département',
                                        color_discrete_sequence=['#1f77b4', '#ff7f0e'])  # Changer la palette de couleurs
        st.plotly_chart(fig_monthly_comparison, use_container_width=True)

# Filtrer les données pour les catégories ABC et exclure la catégorie 'Indifférent' de la tranche d'âge
filtered_data_ABC = data[(data['Catégorie'] == 'ABC') & (data['Tranche d\'âge'] != 'Indifférent')]

# Créer un DataFrame pour la répartition par tranche d'âge
age_distribution = filtered_data_ABC.groupby('Tranche d\'âge')['Nb moyen demandeur emploi'].sum().reset_index()

# Créer le graphique Donut
fig_donut = px.pie(age_distribution, values='Nb moyen demandeur emploi', names='Tranche d\'âge', hole=0.4,
                   title="Répartition par tranche d'âge pour les catégories ABC")

# Modifier le type de graphique en Donut
fig_donut.update_traces(textposition='inside', textinfo='percent+label')

# Afficher le graphique Donut
st.plotly_chart(fig_donut, use_container_width=True)
