import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos con la ruta corregida
@st.cache_data
def load_data():
    data_path = r"C:\Users\mario\Documents\GitHub\ONLINE_DS_THEBRIDGE_27MarioGomez\Project_Break_I__EDA\EDA - CHAMPIONS LEAGUE\src\data\champions_league_complete_with_rounds.csv"
    df = pd.read_csv(data_path)
    return df

# Configuración del dashboard
st.set_page_config(page_title="Champions League Dashboard", layout="wide")
st.title("Análisis de la Champions League")
st.markdown("Este dashboard interactivo analiza el rendimiento del Real Madrid en la Champions League.")

# Cargar datos
df = load_data()

# Sección 1: Descripción general
st.header("1. Descripción General")
st.dataframe(df.head())

# Métricas clave
st.subheader("Métricas Clave del Dataset")
st.write(f"Total de partidos: {df.shape[0]}")
st.write(f"Columnas disponibles: {', '.join(df.columns)}")

# Sección 2: Visualización de Goles
st.header("2. Visualización de Goles")
team = st.selectbox("Selecciona un equipo para analizar:", options=df['Team 1'].unique())
team_data = df[(df['Team 1'] == team) | (df['Team 2'] == team)]

# Visualización de distribución de goles
st.subheader(f"Distribución de Goles - {team}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(team_data['Team 1 Goals'], kde=True, label='Goles como local', color="blue", ax=ax)
sns.histplot(team_data['Team 2 Goals'], kde=True, label='Goles como visitante', color="orange", ax=ax)
ax.set_title(f"Distribución de Goles de {team}")
ax.set_xlabel("Goles")
ax.set_ylabel("Frecuencia")
ax.legend()
st.pyplot(fig)

# Sección 3: Análisis de etapas avanzadas
st.header("3. Apariciones en Etapas Avanzadas")
advanced_rounds = df[df['Round'].str.contains('Semifinal|Final', case=False, na=False)]
team_appearances = advanced_rounds.groupby(['Team 1'])['Round'].count().sort_values(ascending=False).head(10)

# Visualización de apariciones en etapas avanzadas
st.subheader("Equipos con más apariciones en etapas avanzadas")
fig, ax = plt.subplots(figsize=(10, 6))
team_appearances.plot(kind='bar', color='green', ax=ax)
ax.set_title("Apariciones en Semifinales y Finales")
ax.set_xlabel("Equipo")
ax.set_ylabel("Número de apariciones")
st.pyplot(fig)

# Conclusión
st.header("4. Conclusión")
st.markdown("""
Este dashboard proporciona un análisis detallado sobre el rendimiento de equipos en la Champions League, con foco en el Real Madrid.
Puedes explorar métricas clave y entender las tendencias que definen el éxito en este torneo.
""")
