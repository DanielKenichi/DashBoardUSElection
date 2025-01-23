import streamlit as st
import plotly.express as px
import pandas as pd

from dataset.get_dataset import get_dataframe

# Configuração da UI
st.set_page_config(
    page_title="Educação x partido de voto",
    page_icon="🎓",
)

df = get_dataframe()

st.title("Existe correlação entre níveis de educação e o partido de voto por estado?")

st.write(
    "Um gráfico de dispersão mostrando a relação entre o nível de educação e a porcentagem de votos por partido em cada estado."
)

education_level_options = {
    'Population with less than 9th grade education': 'Até a 9ª série',
    'Population with 9th to 12th grade education, no diploma': '9 à 12ª série (sem diploma)',
    'High School graduate and equivalent': 'Ensino Médio completo',
    'Some College,No Degree': 'Ensino Superior incompleto',
    'Associates Degree': 'Diploma de Associado',
    'Bachelors Degree': 'Bacharelado',
    'Graduate or professional degree': 'Pós-graduação',
}

education_level = st.selectbox(
    'Nível de educação',
    education_level_options.keys(),
    format_func=lambda x: education_level_options[x],
)

df['republican_votes'] = df['2020 Republican vote %'] * df['Total Population']
df['democrat_votes'] = df['2020 Democrat vote %'] * df['Total Population']

fig1 = px.scatter(
    df,
    x=education_level,
    y='republican_votes',
    color='state',
    size='Total Population',
    hover_name='county',
    size_max=60,
    title=f'Relação entre a porcentagem de votos republicanos e o nível de educação ({education_level_options[education_level]})',
    labels={
        education_level: 'Nível de educação',
        'republican_votes': 'Número de votos republicanos',
    },
)

fig2 = px.scatter(
    df,
    x=education_level,
    y='democrat_votes',
    color='state',
    size='Total Population',
    hover_name='county',
    size_max=60,
    title=f'Relação entre a porcentagem de votos democratas e o nível de educação ({education_level_options[education_level]})',
    labels={
        education_level: 'Nível de educação',
        'democrat_votes': 'Número de votos democratas',
    },
)

max_y_value = 0
for fig in [fig1, fig2]:
    for trace in fig.data:
        max_y_value = max(max_y_value, trace.y.max())

# Ajustando os limites do eixo y de ambos os gráficos
fig1.update_yaxes(range=[0, max_y_value * 1.1])
fig2.update_yaxes(range=[0, max_y_value * 1.1])

# Exibindo os gráficos
st.plotly_chart(fig1)
st.plotly_chart(fig2)