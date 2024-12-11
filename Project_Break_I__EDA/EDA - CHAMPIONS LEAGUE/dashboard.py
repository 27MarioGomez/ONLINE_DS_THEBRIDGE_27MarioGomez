# dashboard.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
@st.cache_data
def load_data():
    filepath = "src/data/champions_league_complete_with_rounds.csv"
    return pd.read_csv(filepath)

df = load_data()

# Configuración del dashboard
st.title("Análisis Profundo de la Champions League")
st.markdown("Explora los equipos, métricas clave y tendencias en el torneo más prestigioso de Europa.")

# --- Análisis General ---
st.header("1. Análisis General del Torneo")

# Gráfico: Distribución de Rondas
st.subheader("1.1. Distribución de Rondas en el Dataset")
round_distribution = df['Round'].value_counts().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=round_distribution.values, y=round_distribution.index, palette="Purples_r", ax=ax)
ax.set_title("Distribución de Partidos por Ronda")
ax.set_xlabel("Cantidad de Partidos")
ax.set_ylabel("Ronda")
st.pyplot(fig)

# --- Análisis por Equipo ---
st.header("2. Análisis por Equipo")
selected_team = st.selectbox("Selecciona un equipo para analizar:", sorted(df['Team 1'].unique()))

# Filtrar datos por equipo seleccionado
team_data = df[(df['Team 1'] == selected_team) | (df['Team 2'] == selected_team)]

# Métricas clave por equipo
st.subheader(f"2.1. Métricas Clave - {selected_team}")
total_matches = len(team_data)
total_victories = len(team_data[
    ((team_data['Team 1'] == selected_team) & (team_data['Team 1 Goals'] > team_data['Team 2 Goals'])) |
    ((team_data['Team 2'] == selected_team) & (team_data['Team 2 Goals'] > team_data['Team 1 Goals']))
])
win_ratio = (total_victories / total_matches) * 100
total_goals = team_data['Team 1 Goals'].where(team_data['Team 1'] == selected_team, 0).sum() + \
              team_data['Team 2 Goals'].where(team_data['Team 2'] == selected_team, 0).sum()

st.write(f"- **Partidos Totales:** {total_matches}")
st.write(f"- **Victorias Totales:** {total_victories}")
st.write(f"- **Ratio de Victorias:** {win_ratio:.2f}%")
st.write(f"- **Goles Totales:** {total_goals}")

# Gráfico: Distribución de Goles por Temporada
st.subheader(f"2.2. Distribución de Goles por Temporada - {selected_team}")
goals_by_season = team_data.groupby('Season')[['Team 1 Goals', 'Team 2 Goals']].sum()
goals_by_season = goals_by_season.rename(columns={
    'Team 1 Goals': 'Goles como Local',
    'Team 2 Goals': 'Goles como Visitante'
})
fig, ax = plt.subplots(figsize=(12, 6))
goals_by_season.plot(kind='bar', stacked=True, ax=ax, color=['blue', 'orange'], alpha=0.8)
ax.set_title(f"Distribución de Goles de {selected_team} por Temporada")
ax.set_xlabel("Temporada")
ax.set_ylabel("Goles Totales")
st.pyplot(fig)

# Gráfico: Relación entre Goles y Rondas Avanzadas
st.subheader(f"2.3. Relación entre Goles y Etapas Avanzadas - {selected_team}")
advanced_stages = team_data[team_data['Round'].isin(['Semifinal', 'Final'])]
stage_goals = advanced_stages.groupby('Round')[['Team 1 Goals', 'Team 2 Goals']].sum().sum(axis=1)
fig, ax = plt.subplots(figsize=(10, 5))
stage_goals.plot(kind='bar', ax=ax, color='green', alpha=0.8)
ax.set_title(f"Goles de {selected_team} en Semifinales y Finales")
ax.set_xlabel("Ronda")
ax.set_ylabel("Goles Totales")
st.pyplot(fig)

# --- Insights adicionales ---
st.header("3. Insights Adicionales")
st.subheader("Comparativa: Goles Anotados vs Goles Encajados")
team_performance = team_data.copy()
team_performance['Goles Anotados'] = team_performance['Team 1 Goals'].where(
    team_performance['Team 1'] == selected_team, team_performance['Team 2 Goals'])
team_performance['Goles Encajados'] = team_performance['Team 2 Goals'].where(
    team_performance['Team 1'] == selected_team, team_performance['Team 1 Goals'])

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=team_performance, x='Goles Anotados', y='Goles Encajados', ax=ax, color='purple')
ax.set_title(f"Goles Anotados vs Encajados - {selected_team}")
ax.set_xlabel("Goles Anotados")
ax.set_ylabel("Goles Encajados")
st.pyplot(fig)

# --- Conclusión ---
st.header("4. Conclusión")
st.markdown(
    f"El análisis interactivo del rendimiento de {selected_team} en la Champions League permite "
    "identificar patrones clave y métricas que han definido su desempeño. Los gráficos proporcionados "
    "ilustran una vista completa de su evolución en el torneo."
)
