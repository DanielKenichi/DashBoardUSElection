import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from dataset.get_dataset import get_dataframe

def get_state_votes_df(df):
    state_votes_df = df.groupby("state")[["2020 Democrat vote raw", "2020 Republican vote raw", "2020 other vote raw"]].sum()

    state_votes_df["total_votes"] = state_votes_df.sum(axis=1)

    state_votes_df["democrat_percentage"] = (state_votes_df["2020 Democrat vote raw"] / state_votes_df["total_votes"])
    state_votes_df["republican_percentage"] = (state_votes_df["2020 Republican vote raw"] / state_votes_df["total_votes"])
    state_votes_df["other_percentage"] = (state_votes_df["2020 other vote raw"] / state_votes_df["total_votes"])

    state_votes_df.reset_index(inplace=True)

    return state_votes_df

# Calcular a correlação para cada estado individualmente
def calculate_state_correlation(df, ethnicity_type, party_type):
    # Determinar a coluna do partido
    if party_type == 'Democrats':
        party_column = '2020 Democrat vote raw'
    elif party_type == 'Republicans':
        party_column = '2020 Republican vote raw'
    else:
        party_column = '2020 other vote raw'
    
    # Lista para armazenar as correlações por estado
    state_correlations = []

    # Iterar sobre cada estado
    for state in df['state'].unique():
        # Filtrar os dados para o estado atual
        state_df = df[df['state'] == state]
        
        # Calcular a correlação entre a etnia e o partido no estado
        correlation = state_df[ethnicity_type].corr(state_df[party_column])
        
        # Adicionar a correlação à lista
        state_correlations.append({'state': state, 'correlation': correlation})

    # Criar um DataFrame com as correlações por estado
    return pd.DataFrame(state_correlations)

def create_choropleth_map(df, geojson_data, field_name, property_name, color_map):
    map_plot = px.choropleth_mapbox(
        data_frame=df,
        geojson=geojson_data,
        color="correlation",  # Usar a correlação de etnia e votos
        locations=field_name,  # Coluna que contém o nome do estado
        featureidkey=property_name,  # Nome da chave no GeoJSON
        color_continuous_scale=color_map,
        center={"lat": 37.0902, "lon": -95.7129},  # Ajustar para o centro dos EUA
        zoom=3,  # Ajuste o zoom para visualizar os estados
        range_color=(-1, 1),  # Definir o intervalo da correlação (-1 a 1)
        mapbox_style="carto-positron",
        height=600  # Aumentar a altura do mapa
    )
    
    # Ajustar o layout para ocupar mais espaço
    map_plot.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Reduzir margens
        autosize=True  # Ajustar automaticamente o tamanho
    )
    return map_plot

# Streamlit UI
st.set_page_config(page_title="Ethnicity and Vote Correlation", layout="wide")  # Layout amplo

st.write("# Correlation Between Ethnicity and Vote by State")

df = get_dataframe()
df_state = get_state_votes_df(df)

# Adicionar a coluna 'majority_party' com base nos votos democratas e republicanos
df_state['majority_party'] = df_state.apply(
    lambda row: 'Democrats' if row['democrat_percentage'] > row['republican_percentage'] else 'Republicans', axis=1)

# Adicionar o selectbox para escolher a etnia a ser visualizada
ethnicity_type = st.selectbox(
    "Select ethnicity", 
    ["Hispanic or Latino percentage", "NH-White percentage", "NH-Black percentage", 
     "NH-American Indian and Alaska Native percentage", "NH-Asian percentage", 
     "NH-Native Hawaiian and Other Pacific Islander percentage", "NH-Some Other Race percentage"]
)

# Adicionar o selectbox para selecionar a exibição de estados democratas, republicanos ou ambos
party_filter = st.selectbox(
    "Select Party",
    ["Both", "Democrats", "Republicans"]
)

# Filtrando os estados com base no partido selecionado
df_state_filtered = df_state.copy()

if party_filter == "Democrats":
    df_state_filtered = df_state_filtered[df_state_filtered['majority_party'] == 'Democrats']
elif party_filter == "Republicans":
    df_state_filtered = df_state_filtered[df_state_filtered['majority_party'] == 'Republicans']
# Caso "Both", não aplicamos filtro

# Calculando a correlação para a etnia selecionada e o partido em cada estado
if party_filter == "Both":
    # Calcular correlações para Democratas e Republicanos separadamente
    dem_correlations = calculate_state_correlation(df, ethnicity_type, 'Democrats')
    rep_correlations = calculate_state_correlation(df, ethnicity_type, 'Republicans')
    
    # Renomear as colunas de correlação para evitar conflitos
    dem_correlations = dem_correlations.rename(columns={'correlation': 'correlation_dem'})
    rep_correlations = rep_correlations.rename(columns={'correlation': 'correlation_rep'})
    
    # Juntar as correlações ao DataFrame filtrado
    df_state_filtered = pd.merge(df_state_filtered, dem_correlations, on="state")
    df_state_filtered = pd.merge(df_state_filtered, rep_correlations, on="state")
    
    # Criar uma coluna combinada para a correlação
    df_state_filtered['correlation'] = (df_state_filtered['correlation_dem'] + df_state_filtered['correlation_rep']) / 2
else:
    # Calcular correlação apenas para o partido selecionado
    state_correlations = calculate_state_correlation(df, ethnicity_type, party_filter)
    df_state_filtered = pd.merge(df_state_filtered, state_correlations, on="state")

# Carregar o GeoJSON dos estados
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
response = requests.get(url)
geo_json_data = response.json()

# Criar o mapa interativo
map_plot = create_choropleth_map(df_state_filtered, geo_json_data, field_name="state", 
                                  property_name="properties.name", color_map="Viridis")

# Exibir o mapa no Streamlit
st.plotly_chart(map_plot, use_container_width=True)  # Usar a largura total do contêiner

# Texto de conclusão
st.write("## Conclusão")
st.write("""
Este mapa mostra a correlação entre a porcentagem de uma etnia específica e os votos recebidos por Democratas, Republicanos ou ambos os partidos nas eleições de 2020 nos Estados Unidos. 
A correlação varia de **-1 a 1**, onde:

- **Correlação próxima de 1**: Indica uma forte relação positiva entre a etnia e os votos para o partido selecionado. Isso significa que, em estados onde a porcentagem dessa etnia é alta, o partido tende a receber mais votos.
- **Correlação próxima de -1**: Indica uma forte relação negativa. Nesse caso, quanto maior a porcentagem da etnia, menor a proporção de votos para o partido.
- **Correlação próxima de 0**: Indica que não há uma relação clara entre a etnia e os votos para o partido.

Ao selecionar **'Both'**, o mapa exibe a correlação média entre a etnia e os votos de ambos os partidos, permitindo uma visão geral da influência da etnia no cenário político.
""")

st.write("""
**Interpretação dos resultados:**
- Estados com cores mais **quentes** (correlação próxima de 1) mostram uma forte associação entre a etnia selecionada e os votos para o partido.
- Estados com cores mais **frias** (correlação próxima de -1) indicam uma relação inversa.
- Estados com cores **neutras** (correlação próxima de 0) sugerem que a etnia não é um fator determinante para os votos no partido.

Utilize os filtros acima para explorar como diferentes etnias se correlacionam com os votos de Democratas, Republicanos ou ambos.
""")

# Scatter plot para visualizar a relação entre etnia e votos
st.write("## Scatter Plot: Relação entre Etnia e Votos")
st.write("""
O gráfico de dispersão abaixo mostra a relação direta entre a porcentagem da etnia selecionada e a porcentagem de votos para o partido escolhido (ou a média de ambos, se 'Both' for selecionado). 
Cada ponto representa um estado, e a linha de tendência ajuda a visualizar a correlação.
""")

# Adicionar as colunas de porcentagem étnica ao df_state_filtered
# Para isso, precisamos juntar as colunas de etnia do DataFrame original (df) ao df_state_filtered
df_state_filtered = pd.merge(df_state_filtered, df[['state', ethnicity_type]], on="state", how="left")

# Criar o scatter plot
if party_filter == "Both":
    # Para "Both", usamos a média das porcentagens de votos de Democratas e Republicanos
    df_state_filtered['party_votes_percentage'] = (df_state_filtered['democrat_percentage'] + df_state_filtered['republican_percentage']) / 2
else:
    # Para partidos individuais, usamos a porcentagem de votos correspondente
    if party_filter == "Democrats":
        df_state_filtered['party_votes_percentage'] = df_state_filtered['democrat_percentage']
    elif party_filter == "Republicans":
        df_state_filtered['party_votes_percentage'] = df_state_filtered['republican_percentage']

# Criar o gráfico de dispersão
scatter_plot = px.scatter(
    df_state_filtered,
    x=ethnicity_type,
    y="party_votes_percentage",
    color="majority_party",  # Colorir os pontos pelo partido majoritário
    trendline="ols",  # Adicionar uma linha de tendência
    title=f"Relação entre {ethnicity_type} e Porcentagem de Votos para {party_filter}",
    labels={
        ethnicity_type: f"{ethnicity_type} (%)",
        "party_votes_percentage": f"Porcentagem de Votos para {party_filter} (%)",
        "majority_party": "Partido Majoritário"
    },
    size_max=10,  # Ajustar o tamanho máximo dos pontos
    opacity=0.7  # Ajustar a transparência dos pontos
)

# Ajustar o layout do scatter plot
scatter_plot.update_layout(
    xaxis_title=f"{ethnicity_type} (%)",
    yaxis_title=f"Porcentagem de Votos para {party_filter} (%)",
    legend_title="Partido Majoritário",
    showlegend=True
)

# Ajustar a linha de tendência para melhorar a visualização
scatter_plot.update_traces(
    line=dict(color="red", width=2, dash="dash")  # Linha de tendência vermelha tracejada
)

# Exibir o scatter plot
st.plotly_chart(scatter_plot, use_container_width=True)