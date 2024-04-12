import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Charger les données
data_tmp = pd.read_csv('valeursfoncieres.csv', sep =";")
data = data_tmp[~data_tmp['Ville'].str.startswith('0')]
# Définir la configuration de la page
st.set_page_config(
    page_title="Mon application Streamlit",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Titre de l'application
st.title("Comparaison des villes en France")

# Sidebar menu
with st.sidebar:
    st.markdown(
        """
        <style>
            .sidebar-content {
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 10px;
            }
            .tab-content > .stButton > button {
                background-color: #ffffff;
                border-radius: 10px 10px 0 0;
            }
            .tab-content > .stButton > button:hover {
                background-color: #f0f0ff;
            }
            .tab-content > .stButton > button:active {
                background-color: #a0a0ff;
            }
            .sidebar .sidebar-content {
            width: 300px;
            }
            .sidebar .sidebar-content .full-width-button {
            width: 100%;
            padding: 8px;
            font-size: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Les ventes immobilières")

tabs = st.empty()

st.subheader(" ")
        # Insérer le contenu de la feuille 1 ici
  # Filtre L_ATC1
col1, col2 = st.columns(2)
with col1:
    selected_ville1 = st.selectbox("Ville de départ :", data['Ville'].unique(), key="Ville1")

    # Filtre L_ATC2 (dépendant de L_ATC1)
    #filtered_ville2 = data[data['Ville'].isin(selected_ville1)]
with col2:
    selected_ville2 = st.selectbox("Ville souhaitée :", data['Ville'].unique(), key="Ville2")

# Vérifier si aucun filtre n'est sélectionné
if not selected_ville1 and not selected_ville2:
    filtered_data = data  # Utiliser toutes les données non filtrées
elif selected_ville1 and not selected_ville2:
# Filtrer les données en fonction des sélections des filtres
    filtered_data = data[data['Ville'].isin(selected_ville1)]
elif selected_ville1 and selected_ville2:
# Filtrer les données en fonction des sélections des filtres
    filtered_data_ville1 =data[
        (data['Ville'] == (selected_ville1))  
                              ]
    filtered_data_ville2 =data[
        (data['Ville']== (selected_ville2))]  
    
    filtered_data = data[(data['Ville'] == selected_ville1) | (data['Ville'] == selected_ville2)]
    

with col1:
    entete_html = """
    <div style="display: flex; align-items: center;">
        <img src="https://cdn-icons-png.flaticon.com/128/230/230550.png" alt="icone appartement" width="30" style="margin-right: 7px;">
        <p style="margin: 0;"><span style="font-size: 36px;"><b> Appartements - Ventes </b></span> </p>
    </div>
    """     
    with st.container():
            st.markdown(entete_html, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 5px;}</style>", unsafe_allow_html=True)

Data_ville1_appart = filtered_data_ville1[filtered_data_ville1["Type local"] == "Appartement"]
Data_ville1_maison = filtered_data_ville1[filtered_data_ville1["Type local"] == "Maison"]

Data_ville2_appart = filtered_data_ville2[filtered_data_ville2["Type local"] == "Appartement"]
Data_ville2_maison = filtered_data_ville2[filtered_data_ville2["Type local"] == "Maison"]

e_v1_appart_prix = round(Data_ville1_appart.loc[Data_ville1_appart["Annee"] == 2022, "PRIX_M2"].mean() / Data_ville1_appart.loc[Data_ville1_appart["Annee"] == 2021, "PRIX_M2"].mean() - 1, 1)
evol1 = "{:.1%}".format(abs(e_v1_appart_prix))
#Appartements
e_v1_appart_vente = round(Data_ville1_appart.loc[Data_ville1_appart["Annee"] == 2022, "NOMBRE_BIENS"].sum() / Data_ville1_appart.loc[Data_ville1_appart["Annee"] == 2021, "NOMBRE_BIENS"].sum() - 1, 1)
evol2 = "{:.1%}".format(abs(e_v1_appart_vente))

e_v2_appart_prix = round(Data_ville2_appart.loc[Data_ville2_appart["Annee"] == 2022, "PRIX_M2"].mean() / Data_ville2_appart.loc[Data_ville2_appart["Annee"] == 2021, "PRIX_M2"].mean() - 1, 1)
evol3 = "{:.1%}".format(abs(e_v2_appart_prix))

e_v2_appart_vente = round(Data_ville2_appart.loc[Data_ville2_appart["Annee"] == 2022, "NOMBRE_BIENS"].sum() / Data_ville2_appart.loc[Data_ville2_appart["Annee"] == 2021, "NOMBRE_BIENS"].sum() - 1, 1)
evol4 = "{:.1%}".format(abs(e_v2_appart_vente))

# Maison
e_v1_maison_prix = round(Data_ville1_maison.loc[Data_ville1_maison["Annee"] == 2022, "PRIX_M2"].mean() / Data_ville1_maison.loc[Data_ville1_maison["Annee"] == 2021, "PRIX_M2"].mean() - 1, 1)
evol5 = "{:.1%}".format(abs(e_v1_maison_prix))

e_v1_maison_vente = round(Data_ville1_maison.loc[Data_ville1_maison["Annee"] == 2022, "NOMBRE_BIENS"].sum() / Data_ville1_maison.loc[Data_ville1_maison["Annee"] == 2021, "NOMBRE_BIENS"].sum() - 1, 1)
evol6 = "{:.1%}".format(abs(e_v1_maison_vente))

e_v2_maison_prix = round(Data_ville2_maison.loc[Data_ville2_maison["Annee"] == 2022, "PRIX_M2"].mean() / Data_ville2_maison.loc[Data_ville2_maison["Annee"] == 2021, "PRIX_M2"].mean() - 1, 1)
evol7 = "{:.1%}".format(abs(e_v2_maison_prix))

e_v2_maison_vente = round(Data_ville2_maison.loc[Data_ville2_maison["Annee"] == 2022, "NOMBRE_BIENS"].sum() / Data_ville2_maison.loc[Data_ville2_maison["Annee"] == 2021, "NOMBRE_BIENS"].sum() - 1, 1)
evol8 = "{:.1%}".format(abs(e_v2_maison_vente))

valeurs = [e_v1_appart_prix, e_v1_appart_vente, e_v2_appart_prix, e_v2_appart_vente, e_v1_maison_prix, e_v1_maison_vente, e_v2_maison_prix, e_v2_maison_vente ]
# Détermination de la couleur et de la flèche en fonction de l'évolution
styles_evolution = []

for valeur in valeurs:
    if valeur > 0:
        couleur_fond = "lightgreen"
        couleur_texte = "darkgreen"
        fleche = "↑"
        signe = "+"
    else:
        couleur_fond = "lightcoral"
        couleur_texte = "darkred"
        fleche = "↓"
        signe = "-"

    style_evolution = f"background-color: {couleur_fond}; color: {couleur_texte}; padding: 3px; border-radius: 3px;"
    styles_evolution.append((style_evolution, fleche, signe))


col1, col2 = st.columns(2)
with col1:
    moy_ville1 = round(Data_ville1_appart['PRIX_M2'].mean(),1)
    sum_ville1 = round(Data_ville1_appart['NOMBRE_BIENS'].sum())
    # Définition de l'icône et du texte
    icon_html_appart_v1 = """
    <div style="display: flex; align-items: center;">
        <div>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} / m²</b></span> Prix au m² moyen</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} </b></span> Nombre d'appartements vendus depuis 2019</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        </div>
    </div>
    """.format( "{:,.2f} €".format(moy_ville1).replace(",", " "),styles_evolution[0][0],styles_evolution[0][1],styles_evolution[0][2],evol1, "{:,.0f}".format(sum_ville1).replace(",", " "), styles_evolution[1][0],styles_evolution[1][1],styles_evolution[1][2], evol2 )

    # Affichage de la carte avec l'icône et le texte
    with st.container():
            st.markdown(icon_html_appart_v1, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 5px;}</style>", unsafe_allow_html=True)
                 
with col2:
    moy_ville2 = round(Data_ville2_appart['PRIX_M2'].mean(),1)
    sum_ville2 = round(Data_ville2_appart['NOMBRE_BIENS'].sum())
    # Définition de l'icône et du texte
    icon_html_appart_v2 = """
   <div style="display: flex; align-items: center;">
        <div>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} / m²</b></span> Prix au m² moyen</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} </b></span> Nombre d'appartements vendus depuis 2019</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        </div>
    </div>
    """.format("{:,.2f} €".format(moy_ville2).replace(",", " "),styles_evolution[2][0],styles_evolution[2][1],styles_evolution[2][2],evol3, "{:,.0f}".format(sum_ville2).replace(",", " "), styles_evolution[3][0],styles_evolution[3][1],styles_evolution[3][2], evol4 )
    
    # Affichage de la carte avec l'icône et le texte
    #st.subheader("Ma Card")
    with st.container():
            st.markdown(icon_html_appart_v2, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 10px;}</style>", unsafe_allow_html=True)
    #st.write(icon_html_maison, unsafe_allow_html=True)           
# Afficher la répartition des variables BOITES et REM par ANNEE
# Si les données filtrées ne sont pas vides ou si le filtre par défaut est demandé
# Créer une figure pour les visualisations
fig1, ax1 = plt.subplots(figsize=(8, 6))
fig2, ax3 = plt.subplots(figsize=(8, 6))
# Répartition des BOITES par ANNEE (bar)
grouped_by_year_biens = Data_ville1_appart.groupby('Annee')['NOMBRE_BIENS'].sum()
ax1.bar(grouped_by_year_biens.index, grouped_by_year_biens.values, color='b', alpha=0.5, label='Ventes')
ax1.set_xlabel("Année")
ax1.set_ylabel("Vente", color='b')

# Créer un deuxième axe pour la REM par ANNEE (courbe)
ax2 = ax1.twinx()
grouped_by_year_prix = Data_ville1_appart.groupby('Annee')['PRIX_M2'].mean()
ax2.plot(grouped_by_year_prix.index, grouped_by_year_prix.values, color='r', label='Prix au m²')
ax2.set_ylabel("Prix m²", color='r')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Répartition des BOITES par ANNEE (bar)
grouped_by_year_biens = Data_ville2_appart.groupby('Annee')['NOMBRE_BIENS'].sum()
ax3.bar(grouped_by_year_biens.index, grouped_by_year_biens.values, color='b', alpha=0.5, label='Ventes')
ax3.set_xlabel("Année")
ax3.set_ylabel("Vente", color='b')

# Créer un deuxième axe pour la REM par ANNEE (courbe)
ax4 = ax3.twinx()
grouped_by_year_prix = Data_ville2_appart.groupby('Annee')['PRIX_M2'].mean()
ax4.plot(grouped_by_year_prix.index, grouped_by_year_prix.values, color='r', label='Prix au m²')
ax4.set_ylabel("Prix m²", color='r')
ax3.legend(loc='upper left')
ax4.legend(loc='upper right')
# Afficher le premier graphique dans la première colonne
with col1:
    st.pyplot(fig1)

# Afficher le deuxième graphique dans la deuxième colonne
with col2:
    st.pyplot(fig2)


with col1:
    entete_html_maison = """
    <div style="display: flex; align-items: center;">
        <img src="https://cdn-icons-png.flaticon.com/128/5502/5502417.png" alt="icone appartement" width="30" style="margin-right: 7px;">
        <p style="margin: 0;"><span style="font-size: 36px;"><b> Maisons - Ventes </b></span> </p>
    </div>
    """     
    with st.container():
            st.markdown(entete_html_maison, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 5px;}</style>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    moy_ville3 = round(Data_ville1_maison['PRIX_M2'].mean(),1)
    sum_ville3 = round(Data_ville1_maison['NOMBRE_BIENS'].sum())
    # Définition de l'icône et du texte
    icon_html_maison_v1 = """
    <div style="display: flex; align-items: center;">
        <div>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} / m²</b></span> Prix au m² moyen</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} </b></span> Nombre de maisons vendues depuis 2019</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        </div>
    </div>
    """.format("{:,.2f} €".format(moy_ville3).replace(",", " "),styles_evolution[4][0],styles_evolution[4][1],styles_evolution[4][2],evol5, "{:,.0f}".format(sum_ville3).replace(",", " "), styles_evolution[5][0],styles_evolution[5][1],styles_evolution[5][2], evol6 )

    # Affichage de la carte avec l'icône et le texte
    with st.container():
            st.markdown(icon_html_maison_v1, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 5px;}</style>", unsafe_allow_html=True)
                 
with col2:
    moy_ville4 = round(Data_ville2_maison['PRIX_M2'].mean(),1)
    sum_ville4 = round(Data_ville2_maison['NOMBRE_BIENS'].sum())
    # Définition de l'icône et du texte
    icon_html_maison_v2 = """
   <div style="display: flex; align-items: center;">
        <div>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} / m²</b></span> Prix au m² moyen</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        <p style="margin: 0;"><span style="font-size: 28px;"><b> {} </b></span> Nombre de maison vendues depuis 2019</p>
        <p style="margin: 0; font-size: 16px;{} ">{} {} {} - 2022 vs 2021</p>
        </div>
    </div>
    """.format("{:,.2f} €".format(moy_ville4).replace(",", " "),styles_evolution[6][0],styles_evolution[6][1],styles_evolution[6][2],evol7, "{:,.0f}".format(sum_ville4).replace(",", " "), styles_evolution[7][0],styles_evolution[7][1],styles_evolution[7][2], evol8 )
    
    # Affichage de la carte avec l'icône et le texte
    #st.subheader("Ma Card")
    with st.container():
            st.markdown(icon_html_maison_v2, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 10px;}</style>", unsafe_allow_html=True)
    #st.write(icon_html_maison, unsafe_allow_html=True)           
# Afficher la répartition des variables BOITES et REM par ANNEE
# Si les données filtrées ne sont pas vides ou si le filtre par défaut est demandé
# Créer une figure pour les visualisations
fig1, ax1 = plt.subplots(figsize=(8, 6))
fig2, ax3 = plt.subplots(figsize=(8, 6))
# Répartition des BOITES par ANNEE (bar)
grouped_by_year_biens = Data_ville1_maison.groupby('Annee')['NOMBRE_BIENS'].sum()
ax1.bar(grouped_by_year_biens.index, grouped_by_year_biens.values, color='b', alpha=0.5, label='Ventes')
ax1.set_xlabel("Année")
ax1.set_ylabel("Vente", color='b')

# Créer un deuxième axe pour la REM par ANNEE (courbe)
ax2 = ax1.twinx()
grouped_by_year_prix = Data_ville1_maison.groupby('Annee')['PRIX_M2'].mean()
ax2.plot(grouped_by_year_prix.index, grouped_by_year_prix.values, color='r', label='Prix au m²')
ax2.set_ylabel("Prix m²", color='r')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Répartition des BOITES par ANNEE (bar)
grouped_by_year_biens = Data_ville2_maison.groupby('Annee')['NOMBRE_BIENS'].sum()
ax3.bar(grouped_by_year_biens.index, grouped_by_year_biens.values, color='b', alpha=0.5,  label='Ventes')
ax3.set_xlabel("Année")
ax3.set_ylabel("Vente", color='b')

# Créer un deuxième axe pour la REM par ANNEE (courbe)
ax4 = ax3.twinx()
grouped_by_year_prix = Data_ville2_maison.groupby('Annee')['PRIX_M2'].mean()
ax4.plot(grouped_by_year_prix.index, grouped_by_year_prix.values, color='r', label='Prix au m²')
ax4.set_ylabel("Prix m²", color='r')

ax3.legend(loc='upper left')
ax4.legend(loc='upper right')

# Afficher le premier graphique dans la première colonne
with col1:
    st.pyplot(fig1)

# Afficher le deuxième graphique dans la deuxième colonne
with col2:
    st.pyplot(fig2)

with col1:
    entete_html_data = """
    <div style="display: flex; align-items: center;">
        <img src="https://cdn-icons-png.flaticon.com/128/5126/5126025.png" alt="icone appartement" width="30" style="margin-right: 7px;">
        <p style="margin: 0;"><span style="font-size: 36px;"><b> Tableau de données </b></span> </p>
    </div>
    """     
    with st.container():
            st.markdown(entete_html_data, unsafe_allow_html=True)
            st.markdown("---")  # Ajout d'une ligne horizontale pour un meilleur séparateur
            st.markdown("<style>div.st-bb{border: 1px solid #ccc; padding: 5px;}</style>", unsafe_allow_html=True)

    # Afficher le tableau de valeurs
    #st.subheader("Tableau des valeurs filtrées")
    #st.dataframe(filtered_data.groupby('ANNEE')['BOITES', 'REM'].sum())
dt1 = filtered_data.groupby(['Annee','Ville','Type local'])['NOMBRE_BIENS'].sum().reset_index()
dt2 = filtered_data.groupby(['Annee','Ville','Type local'])[['PRIX_M2', 'Surface reelle bati','Surface terrain']].mean().reset_index()
dt = pd.merge(dt1, dt2, on=['Annee', 'Ville', 'Type local'])

if not dt.empty:
    # Définir les labels de colonnes personnalisés
    custom_column_labels = {"Annee": "Année", "Ville": "Commune", "Type local": "Type de bien","NOMBRE_BIENS": "Ventes ( en € )", "PRIX_M2": "Prix m²", "Surface reelle bati" : "Surface réelle ( en m² )","Surface terrain":"Surface terrain ( en m² )" }
    
    # Afficher le tableau avec des labels de colonnes personnalisés
    st.dataframe(dt.rename(columns=custom_column_labels).style.set_table_styles([{'selector': 'th', 'props': [('font-weight', 'bold')]}]))
    
    # Bouton d'export vers Excel
    if st.button("Exporter vers Excel", key="export_button", help="Exportez les données vers Excel"):
        csv = dt.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="donnees_filtrees.csv">Télécharger CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.info("Le fichier a été téléchargé.")
else:
    st.write("Aucune donnée correspondante pour les filtres sélectionnés.")