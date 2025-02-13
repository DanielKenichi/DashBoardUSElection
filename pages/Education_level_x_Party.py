import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

from dataset.get_dataset import get_dataframe

# Configuração da UI
st.set_page_config(
    page_title="Educação x partido de voto",
    page_icon="🎓",
    layout="wide"
)

df = get_dataframe()

# Título
st.title("Existe correlação entre níveis de educação e o partido de voto por estado?")

# Descrição
'''
Os gráficos abaixo buscam responder a esta pergunta. Para isso, vamos utilizar alguns métodos distintos de renderização, começando pelo gráfico de dispersão.
'''

education_level_options = {
    'Population with less than 9th grade education': 'Até a 9ª série',
    'Population with 9th to 12th grade education, no diploma': '9ª a 12ª série, sem diploma',
    'High School graduate and equivalent': 'Ensino Médio completo',
    'Some College,No Degree': 'Ensino Superior incompleto',
    'Associates Degree': 'Associates Degree',
    'Bachelors Degree': 'Bacharelado',
    'Graduate or professional degree': 'Pós-graduação',
}

education_level = st.selectbox(
    'Nível de educação',
    education_level_options.keys(),
    index=list(education_level_options.keys()).index('Bachelors Degree'),
    format_func=lambda x: education_level_options[x],
)

plot_size = st.selectbox(
    'Tamanho do ponto',
    ['Total Population', 'Hispanic or Latino percentage', 'Mean income (dollars)']
)

col1, col2 = st.columns([1, 1])

df['republican_votes'] = df['2020 Republican vote %'] * df['Total Population']
df['democrat_votes'] = df['2020 Democrat vote %'] * df['Total Population']

# Gráfico de dispersão para votos republicanos
fig1 = px.scatter(
    df,
    x=education_level,
    y='2020 Republican vote %',
    color='state',
    size=plot_size,
    hover_name='county',
    size_max=60,
    title=f'Porcentagem de votos republicanos pela porcentagem da população no nível {education_level_options[education_level]}',
    labels={
        education_level: f'Porcentagem da população com nível de educação {education_level_options[education_level]}',
        '2020 Republican vote %': 'Porcentagem de votos republicanos',
    },
)

# Gráfico de dispersão para votos democratas
fig2 = px.scatter(
    df,
    x=education_level,
    y='2020 Democrat vote %',
    color='state',
    size=plot_size,
    hover_name='county',
    size_max=60,
    title=f'Porcentagem de votos democratas pela porcentagem da população no nível {education_level_options[education_level]}',
    labels={
        education_level: f'Porcentagem da população com nível de educação {education_level_options[education_level]}',
        '2020 Democrat vote %': 'Porcentagem de votos democratas',
    },
)

# Encontrando o valor máximo do eixo y em ambos os gráficos
max_y_value = 0
for fig in [fig1, fig2]:
    for trace in fig.data:
        max_y_value = max(max_y_value, trace.y.max())

fig1.update_yaxes(range=[0, max_y_value * 1.1])
fig2.update_yaxes(range=[0, max_y_value * 1.1])

with col1:
    st.plotly_chart(fig1)

with col2:
    st.plotly_chart(fig2)


st.write("## Matriz de Correlação")
'''
Esta matriz de correlação mostra a correlação entre cada nível de educação e a porcentagem de votos para os partidos Republicano e Democrata.

- **Valores mais altos** indicam uma **correlação positiva**.
- **Valores mais baixos** indicam uma **correlação negativa**.
- **Valores mais próximos de 0** indicam uma **correlação fraca**.
'''

correlation_data = df[list(education_level_options.keys()) + ['2020 Republican vote %', '2020 Democrat vote %']]
correlation_matrix = correlation_data.corr()
education_party_correlations = correlation_matrix.loc[list(education_level_options.keys()), ['2020 Republican vote %', '2020 Democrat vote %']]

# Define o intervalo da escala de cores como -1 a 1
fig3 = ff.create_annotated_heatmap(
    z=education_party_correlations.values,
    x=['Votos Republicanos', 'Votos Democratas'],
    y=list(education_level_options.values()),
    colorscale='inferno',
    showscale=True,
    xgap=3,
    ygap=3,
    zmin=-1,  # Define o valor mínimo da escala de cores
    zmax=1   # Define o valor máximo da escala de cores
)

fig3.update_layout(
    title_text='Correlação entre Nível de Educação e Partido do Voto',
    title_x=0.5,
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    xaxis_zeroline=False,
    yaxis_zeroline=False,
    yaxis_autorange='reversed',
    template='plotly_dark'
)

# Exibindo o mapa de calor
st.plotly_chart(fig3)