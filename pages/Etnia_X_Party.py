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

def calculate_state_correlation(df, ethnicity_type, party_type):
    if party_type == 'Democrats':
        party_column = '2020 Democrat vote raw'
    elif party_type == 'Republicans':
        party_column = '2020 Republican vote raw'
    else:
        party_column = '2020 other vote raw'
    
    state_correlations = []

    for state in df['state'].unique():
        state_df = df[df['state'] == state]
        correlation = state_df[ethnicity_type].corr(state_df[party_column])
        state_correlations.append({'state': state, 'correlation': correlation})

    return pd.DataFrame(state_correlations)

def create_choropleth_map(df, geojson_data, field_name, property_name, color_map):
    map_plot = px.choropleth_mapbox(
        data_frame=df,
        geojson=geojson_data,
        color="correlation",
        locations=field_name,
        featureidkey=property_name,
        color_continuous_scale=color_map,
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=3,
        range_color=(-1, 1),
        mapbox_style="carto-positron",
        height=600
    )
    
    map_plot.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        autosize=True
    )
    return map_plot

def create_scatter_plot(df, ethnicity_type):
    if ethnicity_type not in df.columns:
        st.error(f"A coluna '{ethnicity_type}' não existe no DataFrame.")
        return None
    
    scatter_plot = px.scatter(
        df,
        x="democrat_percentage",
        y="republican_percentage",
        color=ethnicity_type,
        hover_name="state",
        labels={
            "democrat_percentage": "Porcentagem de Votos Democratas",
            "republican_percentage": "Porcentagem de Votos Republicanos",
            ethnicity_type: f"Porcentagem de {ethnicity_type}"
        },
        title=f"Relação entre Votos Democratas e Republicanos por {ethnicity_type}",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    return scatter_plot

def create_ethnicity_vote_scatter(df, ethnicity_type, party_type):
    if party_type == 'Democrats':
        party_column = 'democrat_percentage'
        point_color = 'blue'  # Cor para Democratas
    elif party_type == 'Republicans':
        party_column = 'republican_percentage'
        point_color = 'red'  # Cor para Republicanos
    else:
        party_column = 'other_percentage'
        point_color = 'gray'  # Cor para outros (caso exista)
    
    if ethnicity_type not in df.columns:
        st.error(f"A coluna '{ethnicity_type}' não existe no DataFrame.")
        return None
    
    # Criar o gráfico de dispersão
    scatter_plot = px.scatter(
        df,
        x=ethnicity_type,
        y=party_column,
        hover_name="state",
        labels={
            ethnicity_type: f"Porcentagem de {ethnicity_type}",
            party_column: f"Porcentagem de Votos {party_type}"
        },
        title=f"Relação entre {ethnicity_type} e Votos {party_type}",
        trendline="ols"  # Adicionar uma linha de tendência linear
    )
    
    # Definir a cor dos pontos manualmente
    scatter_plot.update_traces(marker=dict(color=point_color))
    
    return scatter_plot

# Streamlit UI
st.set_page_config(page_title="Ethnicity and Vote Correlation", layout="wide")

st.markdown(
    """
    # Pergunta 5
    - Existe correlação entre etnia e o partido de voto por estado?
        - Hipótese1 : Existe uma correlação entre etnia e partido de voto
        - Hipótese2: Não Existe uma correlação entre etnia de voto
    """
)

st.write("# Correlation Between Ethnicity and Vote by State")

df = get_dataframe()
df_state = get_state_votes_df(df)

df_state['majority_party'] = df_state.apply(
    lambda row: 'Democrats' if row['democrat_percentage'] > row['republican_percentage'] else 'Republicans', axis=1)

ethnicity_type = st.selectbox(
    "Select ethnicity", 
    ["Hispanic or Latino percentage", "NH-White percentage", "NH-Black percentage", 
     "NH-American Indian and Alaska Native percentage", "NH-Asian percentage", 
     "NH-Native Hawaiian and Other Pacific Islander percentage", "NH-Some Other Race percentage"],
    key="ethnicity_selectbox"
)

party_filter = st.selectbox(
    "Select Party",
    ["Democrats", "Republicans"],
    key="party_selectbox"
)

df_state_filtered = df_state.copy()

if party_filter == "Democrats":
    df_state_filtered = df_state_filtered[df_state_filtered['majority_party'] == 'Democrats']
elif party_filter == "Republicans":
    df_state_filtered = df_state_filtered[df_state_filtered['majority_party'] == 'Republicans']

state_correlations = calculate_state_correlation(df, ethnicity_type, party_filter)
df_state_filtered = pd.merge(df_state_filtered, state_correlations, on="state")

# Adicionar as colunas de etnia ao DataFrame filtrado
df_ethnicity = df.groupby("state")[ethnicity_type].mean().reset_index()
df_state_filtered = pd.merge(df_state_filtered, df_ethnicity, on="state")

# Carregar o GeoJSON dos estados
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
response = requests.get(url)
geo_json_data = response.json()

# Criar o mapa interativo
map_plot = create_choropleth_map(df_state_filtered, geo_json_data, field_name="state", 
                                  property_name="properties.name", color_map="Viridis")

# Exibir o mapa no Streamlit
st.plotly_chart(map_plot, use_container_width=True)

# Texto de explicação
st.write("""
**Explicação do Mapa**         
Este mapa mostra a correlação entre a porcentagem de uma etnia específica e os votos recebidos por Democratas, Republicanos ou ambos os partidos nas eleições de 2020 nos Estados Unidos. 
A correlação varia de **-1 a 1**, onde:

- **Correlação próxima de 1**: Indica uma forte relação positiva entre a etnia e os votos para o partido selecionado. Isso significa que, em estados onde a porcentagem dessa etnia é alta, o partido tende a receber mais votos.
- **Correlação próxima de -1**: Indica uma forte relação negativa. Nesse caso, quanto maior a porcentagem da etnia, menor a proporção de votos para o partido.
- **Correlação próxima de 0**: Indica que não há uma relação clara entre a etnia e os votos para o partido.
""")

st.write("""
**Interpretação dos resultados:**
- Estados com cores mais **quentes** (correlação próxima de 1) mostram uma forte associação entre a etnia selecionada e os votos para o partido.
- Estados com cores mais **frias** (correlação próxima de -1) indicam uma relação inversa.
- Estados com cores **neutras** (correlação próxima de 0) sugerem que a etnia não é um fator determinante para os votos no partido.
""")

# Adicionar o selectbox para selecionar o partido para o novo scatter plot
party_scatter = st.selectbox(
    "Select Party for Ethnicity vs Vote Scatter Plot",
    ["Democrats", "Republicans"],
    key="party_scatter_selectbox"
)

# Criar e exibir o novo gráfico de dispersão
ethnicity_vote_scatter = create_ethnicity_vote_scatter(df_state_filtered, ethnicity_type, party_scatter)
if ethnicity_vote_scatter:
    st.plotly_chart(ethnicity_vote_scatter, use_container_width=True)

# Texto de interpretação do novo gráfico de dispersão
st.write("### Interpretação do Gráfico de Dispersão: Etnia vs Votos")
st.write(f"""
Este gráfico de dispersão mostra a relação entre a **{ethnicity_type}** (eixo X) e a **porcentagem de votos {party_scatter}** (eixo Y) em cada estado dos Estados Unidos. 
""")