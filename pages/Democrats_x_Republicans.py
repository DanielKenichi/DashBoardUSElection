import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import os
from dataset.get_dataset import get_dataframe

processed_dfs = dict()

def get_state_votes_df(df):
    state_votes_df = df.groupby("state")[["2020 Democrat vote raw", "2020 Republican vote raw", "2020 other vote raw"]].sum()

    state_votes_df["total_votes"] = state_votes_df.sum(axis=1)

    state_votes_df["democrat_percentage"] = (state_votes_df["2020 Democrat vote raw"] / state_votes_df["total_votes"])
    state_votes_df["republican_percentage"] = (state_votes_df["2020 Republican vote raw"] / state_votes_df["total_votes"])
    state_votes_df["other_percentage"] = (state_votes_df["2020 other vote raw"] / state_votes_df["total_votes"])

    state_votes_df.reset_index(inplace=True)

    return state_votes_df

def get_county_votes_df(df):
    map_df = df.copy()
    map_df = map_df.rename(columns={
        "2020 Republican vote %": "republican_percentage", 
        "2020 Democrat vote %": "democrat_percentage",
        "2020 other vote %": "other_percentage",
    })

    response = requests.get(
        "https://github.com/kjhealy/fips-codes/blob/master/state_and_county_fips_master.csv"
    )

    with open("./data/fips.csv", "r") as file: 
        fips_df = pd.read_csv(file)

    map_df["state_ac"] = ""

    for state in map_df["state"].unique().tolist():
        state_row = fips_df[fips_df["name"] == state.upper()]
        row_with_ac = fips_df.iloc[state_row.index[0] + 1]

        state_acron = row_with_ac["state"]

        map_df.loc[map_df["state"] == state, "state_ac"] = state_acron

    result_df = map_df.merge(
        fips_df[["fips", "name", "state"]], 
        left_on=["county", "state_ac"], 
        right_on=["name", "state"], 
        how="left",
    )

    result_df = result_df.drop(columns=["name"])

    map_df["fips"] = result_df["fips"]

    map_df["fips"] = map_df["fips"].apply(lambda x: str(x).zfill(5))

    return map_df

def determine_color(map_df):
    def assign_color(row):
        if row["republican_percentage"] > row["democrat_percentage"] and row["republican_percentage"] > row["other_percentage"]:
            return "Republicans"
        elif row["democrat_percentage"] > row["republican_percentage"] and row["democrat_percentage"] > row["other_percentage"]:
            return "Democrats"
        else:
            return "Others"
    
    map_df["winner party"] = map_df.apply(assign_color, axis=1)
    return map_df

st.set_page_config(
    page_title="Democrats x Republicans",
    layout="wide"
)

st.markdown(
    """
    # Pergunta 1
    - Quais estados tiveram maioria republicana e Quais democrata?
        - Hipótese1 : A maioria dos estados teve maioria republicana
        - Hipótese2:  A maioria dos estados teve maioria democrata
    """
)

st.write("# Democrats x Republicans")

party_selector, state_or_county = st.columns(2)

df = get_dataframe()

with party_selector:
    party_to_show = st.selectbox("",["Both", "Democrats", "Republicans"])
with state_or_county:
    city_or_state = st.selectbox("", ["by state", "by county"])

republican_color = "#F2545B"
democrat_color = "#216681"
not_selected_color = "#D3D3D3"

if party_to_show == "Both":
   color_map = {"Republicans": republican_color,"Democrats": democrat_color}
elif party_to_show == "Democrats":
   color_map = {"Republicans": not_selected_color,"Democrats": democrat_color}
else:
   color_map = {"Republicans": republican_color,"Democrats": not_selected_color}

#preparing df for the map plot
if city_or_state == "by state":
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    file_name = "us-states.json"
    field_name = "state"
    property_name = "properties.name"
    map_df = get_state_votes_df(df)
    hist_df = get_state_votes_df(df)
else: #by county
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    file_name = "us-counties.json"
    field_name = "fips"
    property_name = "id"
    map_df = get_county_votes_df(df)
    hist_df = get_county_votes_df(df)

map_df = determine_color(map_df)

response = requests.get(url)
with open(file_name, "w", encoding="utf-8") as file:
    file.write(response.text)
with open(file_name, "r") as file:
    geo_json_data = json.load(file)

row1 = st.columns(1)
map_plot = px.choropleth_map(
    data_frame=map_df, 
    geojson=geo_json_data, 
    color="winner party",
    locations=field_name, featureidkey=property_name,
    center = {"lat": 37.0902, "lon": -95.7129},
    zoom=2.5,
    color_discrete_map=color_map
)
row1[0].plotly_chart(map_plot, use_container_width=True)

'''
    **Imagem:** Mapa dos estados unidos onde cada estado ou cidade é colorida por uma cor
    representante do partido vencedor na eleição de 2020. Azul para democrata e vermelho para republicano
'''

#preparing df for the barplot
counts = map_df["winner party"].value_counts()
counts_df = pd.DataFrame(counts).transpose()
counts_df = counts_df.melt(var_name="Party", value_name="Count")

if party_to_show != "Both":
    counts_df = counts_df[counts_df["Party"] == party_to_show]
row2 = st.columns(1)

bar_plot = px.bar(
    counts_df,
    x="Party",
    y="Count",
    color="Party",
    color_discrete_map=color_map,
    text="Count"
)

location = city_or_state.split(" ")[1]

bar_plot.update_layout(
    title=f"Count of {location}",
    xaxis_title="Party",
    yaxis_title="Count",
    yaxis_range=[0, len(map_df)],
    showlegend=False
)
bar_plot.update_traces(textposition='outside', textfont=dict(size=16))

row2[0].plotly_chart(bar_plot, use_container_width=True)

'''
    **Imagem:** gráfico de barras comparando número de cidade ou estados vencedores de cada partido
'''

row3 = st.columns(1)

opacity = 0.75
bar_size = 0.05

hist1 = go.Histogram(
    x=hist_df["democrat_percentage"],
    opacity=opacity,
    marker=dict(color=democrat_color),
    name='Democrats',
    xbins=dict(size=bar_size),
    autobinx=False
)

hist2 = go.Histogram(
    x=hist_df["republican_percentage"],
    opacity=opacity,
    marker=dict(color=republican_color),
    name='Republicans',
    xbins=dict(size=bar_size),
    autobinx=False
)


if party_to_show == "Both":
    hist2.update(yaxis='y2')
    layout = go.Layout(
        title='Democrats x Republicans',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Count', showgrid=True),
        yaxis2=dict(title='Count', overlaying='y', side='right', showgrid=False),
        barmode='overlay',
        bargap=0.2,
        showlegend=True
    )

    fig = go.Figure(data=[hist1, hist2], layout=layout)

elif party_to_show == "Democrats":
    layout = go.Layout(
        title='Democrats',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Count', showgrid=True),
        barmode='overlay',
        bargap=0.2,
        showlegend=True
    )

    fig = go.Figure(data=[hist1], layout=layout)

else:
    layout = go.Layout(
        title='Republicans',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Count', showgrid=True),
        barmode='overlay',
        bargap=0.2,
        showlegend=True
    )

    fig = go.Figure(data=[hist2], layout=layout)

row3[0].plotly_chart(fig, use_container_width=True)

'''
    **Imagem:** histograma demonstrando a distribuição da porcentagem de votos democratas e republicanos
    por cidade ou estado
'''