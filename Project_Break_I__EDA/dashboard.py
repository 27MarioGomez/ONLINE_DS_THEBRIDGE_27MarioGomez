import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Imprime el directorio de trabajo actual para depuración
st.write("Directorio de trabajo actual:", os.getcwd())

# Cargar datos
@st.cache_data
def load_data():
    # Ruta según el directorio actual en Streamlit
    filepath = os.path.join(os.getcwd(), "EDA_CHAMPIONS_LEAGUE/src/data/champions_league_complete_with_rounds.csv")
    return pd.read_csv(filepath)

df = load_data()

# Título del dashboard
st.title("Análisis Profundo de la Champions League")
st.write("Explora los equipos, métricas clave y tendencias en el torneo más prestigioso de Europa.")

# Análisis General
st.header("1. Análisis General del Torneo")

# Mostrar una vista del dataset embebido
st.subheader("1.1. Vista General del Dataset")
st.write("Una muestra de los datos utilizados en este análisis:")
st.dataframe(df.head())

# Análisis por Equipo
st.header("2. Análisis por Equipo")
team_selected = st.selectbox("Selecciona un equipo para analizar:", sorted(df['Team 1'].unique()))

# Filtrar datos por equipo seleccionado
team_data = df[(df['Team 1'] == team_selected) | (df['Team 2'] == team_selected)]

# Validar si hay datos del equipo seleccionado
if team_data.empty:
    st.subheader(f"2.1. Métricas Clave - {team_selected}")
    st.write("Este equipo no tiene datos suficientes para realizar un análisis detallado. Lo sentimos. 🙁")
else:
    # Métricas clave del equipo
    st.subheader(f"2.1. Métricas Clave - {team_selected}")
    total_matches = len(team_data)
    victories = len(team_data[(team_data['Team 1'] == team_selected) & (team_data['Team 1 Goals'] > team_data['Team 2 Goals'])]) + \
                len(team_data[(team_data['Team 2'] == team_selected) & (team_data['Team 2 Goals'] > team_data['Team 1 Goals'])])
    win_ratio = (victories / total_matches) * 100 if total_matches > 0 else 0
    total_goals = team_data['Team 1 Goals'].sum() + team_data['Team 2 Goals'].sum()

    st.write(f"- **Partidos Totales:** {total_matches}")
    st.write(f"- **Victorias Totales:** {victories}")
    st.write(f"- **Ratio de Victorias:** {win_ratio:.2f}%")
    st.write(f"- **Goles Totales:** {total_goals}")

    # Distribución de Goles por Temporada
    if not team_data.empty:
        st.subheader(f"2.2. Distribución de Goles por Temporada - {team_selected}")
        goals_by_season = team_data.groupby('Season').agg({'Team 1 Goals': 'sum', 'Team 2 Goals': 'sum'})
        goals_by_season.rename(columns={'Team 1 Goals': 'Goles como Local', 'Team 2 Goals': 'Goles como Visitante'}, inplace=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        goals_by_season.plot(kind='bar', stacked=True, ax=ax, color=['blue', 'orange'], alpha=0.8)
        plt.title(f"Distribución de Goles de {team_selected} por Temporada")
        plt.xlabel("Temporada")
        plt.ylabel("Goles Totales")
        st.pyplot(fig)

    # Relación entre Goles y Etapas Avanzadas
    advanced_rounds = team_data[team_data['Round'].isin(['Semifinal', 'Final'])]
    if not advanced_rounds.empty:
        st.subheader(f"2.3. Relación entre Goles y Etapas Avanzadas - {team_selected}")
        stage_goals = advanced_rounds.groupby('Round').agg({'Team 1 Goals': 'sum', 'Team 2 Goals': 'sum'}).sum(axis=1)

        fig, ax = plt.subplots(figsize=(10, 6))
        stage_goals.plot(kind='bar', ax=ax, color='green', alpha=0.8)
        plt.title(f"Goles de {team_selected} en Semifinales y Finales")
        plt.xlabel("Ronda")
        plt.ylabel("Goles Totales")
        st.pyplot(fig)
    else:
        st.subheader(f"2.3. Relación entre Goles y Etapas Avanzadas - {team_selected}")
        st.write("No hay datos suficientes para este equipo en Semifinales o Finales. 🙁")

# Insights Adicionales
st.header("3. Insights Adicionales")
if not team_data.empty:
    st.subheader("Comparativa: Goles Anotados vs Goles Encajados")
    fig, ax = plt.subplots(figsize=(8, 6))
    team_data.plot.scatter(x='Team 1 Goals', y='Team 2 Goals', ax=ax, color='purple', alpha=0.6)
    plt.title(f"Goles Anotados vs Goles Encajados - {team_selected}")
    plt.xlabel("Goles Anotados")
    plt.ylabel("Goles Encajados")
    st.pyplot(fig)
else:
    st.subheader("Comparativa: Goles Anotados vs Goles Encajados")
    st.write("No hay suficientes datos para generar esta visualización. 🙁")

# Conclusión
st.header("4. Conclusión")
st.write(f"El análisis interactivo del rendimiento de {team_selected} en la Champions League permite identificar patrones clave y métricas que han definido su desempeño. Los gráficos proporcionados ilustran una vista completa de su evolución en el torneo.")
