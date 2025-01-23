import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from dataset.get_dataset import get_dataframe


def get_state_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and returns a new DataFrame with state-level data.

    Args:
        df: The input DataFrame with county-level data.

    Returns:
        A new DataFrame with the following columns:
        - state: The name of the state.
        - mean_income: The average mean income for the state.
        - median_income: The average median income for the state.
        - most_voted_party: The party with the most votes in the state.
    """

    # Calculate the most voted party for each county
    df['most_voted_party'] = df.apply(
        lambda row: 'Democrat' if row['2020 Democrat vote raw'] > row['2020 Republican vote raw'] and row['2020 Democrat vote raw'] > row['2020 other vote raw']
        else 'Republican' if row['2020 Republican vote raw'] > row['2020 Democrat vote raw'] and row['2020 Republican vote raw'] > row['2020 other vote raw']
        else 'Other', axis=1
    )

    # Aggregate data by state
    state_data = df.groupby('state').agg(
        mean_income=('Mean income (dollars)', 'mean'),
        median_income=('Median income (dollars)', 'mean'),
        total_democrat_votes=('2020 Democrat vote raw', 'sum'),
        total_republican_votes=('2020 Republican vote raw', 'sum'),
        total_other_votes=('2020 other vote raw', 'sum')
    )

    # Determine the most voted party for each state based on total votes
    state_data['most_voted_party'] = state_data.apply(
        lambda row: 'Democrat' if row['total_democrat_votes'] > row['total_republican_votes'] and row['total_democrat_votes'] > row['total_other_votes']
        else 'Republican' if row['total_republican_votes'] > row['total_democrat_votes'] and row['total_republican_votes'] > row['total_other_votes']
        else 'Other', axis=1
    )

    # Reset index to make 'state' a column
    state_data = state_data.reset_index()

    # Select and rename the desired columns
    state_data = state_data[['state', 'mean_income',
                             'median_income', 'most_voted_party']]
    state_data = state_data.rename(columns={'state': 'state_name'})

    return state_data


st.title("Pergunta 2")

st.markdown(
    """
    - Existe correlação entre concentração de renda e o partido de voto por estado?
        - Hipótese1 : Existe uma correlação entre concentração de renda e partido de voto
        - Hipótese2: Não Existe uma correlação entre concentração de renda e partido de voto
    """
)
df = get_dataframe()
state_df = get_state_data(df)  # Use o dataframe agregado por estado!

# Violin plot para Mean Income
fig_mean = px.violin(state_df,
                     y="mean_income",
                     x="state_name",
                     color="most_voted_party",
                     box=True,  # Mostra a caixa
                     points="all",  # Mostra todos os pontos
                     color_discrete_map={'Democrat': 'blue',
                                         'Republican': 'red', 'Other': 'gray'},
                     )
fig_mean.update_traces(
    jitter=0.7,  # Adiciona jitter horizontal aos pontos
    pointpos=0,  # Posiciona os pontos no centro
    marker=dict(size=7, opacity=0.7),  # Melhora a visualização dos pontos
)
fig_mean.update_layout(
    title_text="Mean Income by State",
    yaxis_title="Mean Income (dollars)",
    xaxis_title="State"
)

fig_mean.update_traces(
    jitter=0.7,
    pointpos=0,
    marker=dict(size=7, opacity=0.7),
    line_width=2.5  # Adicione esta linha para aumentar a espessura da linha da caixa
)

st.plotly_chart(fig_mean)

# Violin plot para Median Income (similar ao anterior)
fig_median = px.violin(state_df,
                       y="median_income",
                       x="state_name",
                       color="most_voted_party",
                       box=True,  # Mostra a caixa
                       points="all",  # Mostra todos os pontos
                       color_discrete_map={'Democrat': 'blue',
                                           'Republican': 'red', 'Other': 'gray'},
                       )

fig_median.update_traces(
    jitter=0.7,  # Adiciona jitter horizontal aos pontos
    pointpos=0,  # Posiciona os pontos no centro
    marker=dict(size=7, opacity=0.7),  # Melhora a visualização dos pontos
)

fig_median.update_layout(
    title_text="Median Income by State",
    yaxis_title="Median Income (dollars)",
    xaxis_title="State",
)

fig_median.update_traces(
    jitter=0.7,
    pointpos=0,
    marker=dict(size=7, opacity=0.7),
    line_width=2.5  # Adicione esta linha para aumentar a espessura da linha da caixa
)

st.plotly_chart(fig_median)
