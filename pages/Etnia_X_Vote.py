from dataset import get_dataset
from pandas import pd
import plotly.express as px

# Calculando a porcentagem dos votos de cada estado
state_votes = get_dataset().groupby('state')[['2020 Democrat vote raw', '2020 Republican vote raw', '2020 other vote raw']].sum()

# Calculando o total de votos por estado
state_votes['total_votes'] = state_votes.sum(axis=1)

# Calculando a porcentagem de cada tipo de voto
state_votes['democrat_percentage'] = (state_votes['2020 Democrat vote raw'] / state_votes['total_votes'])
state_votes['republican_percentage'] = (state_votes['2020 Republican vote raw'] / state_votes['total_votes'])
state_votes['other_percentage'] = (state_votes['2020 other vote raw'] / state_votes['total_votes'])

# Incluindo a coluna do estado no DataFrame final
state_votes.reset_index(inplace=True)

# Concatenando os dois DataFrames (dados do Kaggle e state_votes)
df_Hip5 = pd.merge(get_dataset(), state_votes, on='state', how='left')

# Agrupando os estados e calculando a média das porcentagens
df_Hip5_group = df_Hip5.groupby('state')[[
    'democrat_percentage', 'republican_percentage', 'other_percentage',
    'Hispanic or Latino percentage', 'NH-White percentage', 'NH-Black percentage',
    'NH-American Indian and Alaska Native percentage', 'NH-Asian percentage',
    'NH-Native Hawaiian and Other Pacific Islander percentage', 'NH-Some Other Race percentage'
]].mean()

group_df_reset = df_Hip5_group.reset_index()

# Criando o mapa coroplético para visualizar a relação por estado
fig = px.choropleth(
    group_df_reset,
    geojson="https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json",
    locations='state',  # Coluna que contém os estados
    featureidkey="properties.name",  # Nome das propriedades dos estados no arquivo GeoJSON
    color='Hispanic or Latino percentage',  # Métrica para a coloração (exemplo: porcentagem de latinos)
    hover_name='state',  # Nome do estado no hover
    hover_data={
        'democrat_percentage': ':.2%',
        'republican_percentage': ':.2%',
        'other_percentage': ':.2%',
        'Hispanic or Latino percentage': ':.2%'
    },
    color_continuous_scale='Viridis',  # Escala de cores
    title="Relação entre etnia e votos por estado"
)

# Ajustando o layout do mapa
fig.update_geos(
    visible=False,  # Esconde os limites externos
    fitbounds="locations"  # Ajusta o zoom para se adequar aos estados
)

# Exibindo o mapa
fig.show()
