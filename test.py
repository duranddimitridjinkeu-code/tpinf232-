import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page pour un affichage large
st.set_page_config(page_title="Global Salary Analytics INF232", layout="wide")

st.title("🌍 Observatoire Mondial des Salaires par Continent")
st.markdown("""
*Projet TP INF 232 EC2 - Collecte et Analyse Descriptive* **Auteur :** Dimitri  
**Enseignant :** Pr. Rollin Francis
""")

# --- FONCTION DE COLLECTE EN LIGNE (Simulation de flux API) ---
@st.cache_data
def fetch_salary_data_online():
    # Simulation d'une collecte de données sur un serveur international
    continents_dict = {
        'Afrique': ['Cameroun', 'Sénégal', 'Côte d\'Ivoire', 'Nigéria', 'Afrique du Sud'],
        'Europe': ['France', 'Allemagne', 'Belgique', 'Espagne', 'Italie'],
        'Asie': ['Chine', 'Japon', 'Inde', 'Corée du Sud', 'Vietnam'],
        'Amérique': ['USA', 'Canada', 'Brésil', 'Mexique', 'Argentine']
    }
    
    records = []
    for continent, pays_list in continents_dict.items():
        for pays in pays_list:
            # On simule 20 relevés par pays pour avoir une base statistique robuste
            for _ in range(20):
                # Paramètres de salaires réalistes par zone (en USD)
                if continent == 'Europe':
                    salaire = np.random.normal(3500, 800)
                elif continent == 'Afrique':
                    salaire = np.random.normal(600, 300)
                elif continent == 'Amérique':
                    salaire = np.random.normal(4500, 1500)
                else: # Asie
                    salaire = np.random.normal(2500, 1000)
                
                records.append({
                    'Continent': continent,
                    'Pays': pays,
                    'Salaire_USD': abs(round(salaire, 2))
                })
    return pd.DataFrame(records)

# --- LOGIQUE DE L'APPLICATION ---
st.sidebar.header("🕹️ Contrôle de l'Application")
if st.sidebar.button("🌐 Lancer la collecte en direct"):
    # 1. Collecte
    df = fetch_salary_data_online()
    st.success(f"✅ Collecte terminée : {len(df)} points de données récupérés en ligne.")

    # 2. Indicateurs Clés (Métriques)
    st.header("📊 Indicateurs de Tendance Centrale")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Moyenne Mondiale", f"{int(df['Salaire_USD'].mean()):,} $".replace(',', ' '))
    m2.metric("Médiane", f"{int(df['Salaire_USD'].median()):,} $".replace(',', ' '))
    m3.metric("Salaire Max", f"{int(df['Salaire_USD'].max()):,} $".replace(',', ' '))
    m4.metric("Écart-Type", f"{int(df['Salaire_USD'].std()):,} $".replace(',', ' '))

    # 3. Analyse Moderne (Plotly)
    st.header("📈 Visualisation Interactive")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_box = px.box(df, x="Continent", y="Salaire_USD", color="Continent",
                         title="Dispersion des salaires (Boxplot par Continent)")
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col2:
        fig_bar = px.histogram(df, x="Continent", y="Salaire_USD", histfunc="avg",
                               color="Continent", title="Salaire Moyen par Continent")
        st.plotly_chart(fig_bar, use_container_width=True)

    # 4. Analyse "À l'ancienne" par Continent (Matplotlib)
    st.header("📉 Distribution Détaillée (Modèle Fréquentiste)")
    st.write("Voici la densité de probabilité pour chaque continent (un graphe par zone) :")
    
    continents = df['Continent'].unique()
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    axes = axes.flatten()

    for i, cont in enumerate(continents):
        subset = df[df['Continent'] == cont]['Salaire_USD']
        # Histogramme
        subset.plot(kind='hist', bins=15, density=True, alpha=0.4, color='teal', ax=axes[i], edgecolor='black')
        # Courbe de densité
        subset.plot(kind='kde', color='red', ax=axes[i], linewidth=2)
        
        axes[i].set_title(f"Distribution : {cont}")
        axes[i].set_xlabel("Salaire Mensuel (USD)")
        axes[i].grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    st.pyplot(fig)

    # 5. Synthèse des données
    st.header("📋 Tableau Récapitulatif")
    st.dataframe(df.groupby(['Continent', 'Pays'])['Salaire_USD'].describe(), use_container_width=True)

else:
    st.info("👋 Bienvenue Dimitri ! Cliquez sur le bouton dans la barre latérale pour lancer l'analyse.")