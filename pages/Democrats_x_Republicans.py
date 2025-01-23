import streamlit as st
import plotly.express as px
import json
import os
import kagglehub
import re
from dataset.get_dataset import get_dataframe

def get_state_votes_df(df):
    state_votes_df = df.groupby("state")[["2020 Democrat vote raw", "2020 Republican vote raw", "2020 other vote raw"]].sum()

    state_votes_df["total_votes"] = state_votes_df.sum(axis=1)

    state_votes_df["democrat_percentage"] = (state_votes_df["2020 Democrat vote raw"] / state_votes_df["total_votes"])
    state_votes_df["republican_percentage"] = (state_votes_df["2020 Republican vote raw"] / state_votes_df["total_votes"])
    state_votes_df["other_percentage"] = (state_votes_df["2020 other vote raw"] / state_votes_df["total_votes"])

    state_votes_df.reset_index(inplace=True)

    return state_votes_df

def determine_color(states_df):
    def assign_color(row):
        if row["republican_percentage"] > row["democrat_percentage"] and row["republican_percentage"] > row["other_percentage"]:
            return "Republican"
        elif row["democrat_percentage"] > row["republican_percentage"] and row["democrat_percentage"] > row["other_percentage"]:
            return "Democrat"
        else:
            return "Other"
    
    states_df["winner party"] = states_df.apply(assign_color, axis=1)
    return states_df

def format_state_name(state_name):
    if state_name == "DistrictofColumbia":
        return "District of Columbia"

    return re.sub(r'([a-z])([A-Z])', r'\1 \2', state_name)

st.set_page_config(
    page_title="Democrats x Republicans",
)

df = get_dataframe()

#preparing df for the plot
states_df = get_state_votes_df(df)
states_df = determine_color(states_df)
states_df["state"] = states_df["state"].apply(format_state_name)


path = kagglehub.dataset_download("pompelmo/usa-states-geojson")
path = os.path.join(path, "us-states.json")
with open(path, "r") as file:
    geo_json_data = json.load(file)

st.write("# Democrats x Republicans")
party_to_show = st.selectbox("",("Both", "Democrats", "Republicans"))

col1 = st.columns(1)

republican_color = "#F2545B"
democrat_color = "#216681"
not_selected_color = "#D3D3D3"

if party_to_show == "Both":
   color_map = {"Republican": republican_color,"Democrat": democrat_color}
elif party_to_show == "Democrats":
   color_map = {"Republican": not_selected_color,"Democrat": democrat_color}
else:
   color_map = {"Republican": republican_color,"Democrat": not_selected_color}

fig = px.choropleth_map(data_frame=states_df, geojson=geo_json_data, color="winner party",
                        locations="state", featureidkey="properties.name",
                        center = {"lat": 37.0902, "lon": -95.7129},zoom=3,
                        color_discrete_map=color_map)
col1[0].plotly_chart(fig)