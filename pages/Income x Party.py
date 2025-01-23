import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dataset.get_dataset import get_dataframe

def get_state_df(df, state):
    state_df = df[df["state"] == state]

    state_df.rename(columns={
        "2020 Republican vote %": "republican_percentage", 
        "2020 Democrat vote %": "democrat_percentage",
        "2020 other vote %": "other_percentage",
    })

    return state_df

def get_corr_matrix_plot(x_field, y_field):

    correlation_matrix = plot_df[[x_field, y_field]].corr()

    matrix_plot = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Viridis',
            showscale=True
        )
    )
    for i in range(len(correlation_matrix)):
        for j in range(len(correlation_matrix)):
            matrix_plot.add_annotation(
                go.layout.Annotation(
                    text=str(round(correlation_matrix.iloc[i, j], 2)),
                    x=correlation_matrix.columns[j],
                    y=correlation_matrix.index[i],
                    showarrow=False,
                    font=dict(color='white' if correlation_matrix.iloc[i, j] < 0.5 else 'black')
                )
            )
    matrix_plot.update_layout(
        title=f"{x_field} x Party votes",
        xaxis_title=x_field,
        yaxis_title='Party Votes (percentage)'
    )

    return matrix_plot

def get_scatter_plot(x_field, y_field, x_title, y_title, title):

    plot = px.scatter(
        plot_df, 
        x=x_field, 
        y=y_field, 
        title=title
    )

    plot.update_traces(marker=dict(color=plot_color))

    plot.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
    )

    return plot


st.set_page_config(
    page_title="Income x Party",
    layout="wide"
)

st.markdown(
    """
    # Pergunta 3
    - Existe correlação entre concentração de renda e o partido de voto por estado?
        - Hipótese1 : Existe uma correlação entre concentração de renda e partido de voto
        - Hipótese2:  Não Existe uma correlação entre concentração de renda e partido de voto
    """
)

st.write("# Income x Party")

df = get_dataframe()

view_selector, party_selector = st.columns(2)
views = df["state"].unique().tolist()
views.insert(0, "All")

with view_selector:
    view = st.selectbox("", views)
with party_selector:
    party = st.selectbox("", ["Democrats", "Republicans"])

if view != "All":
    plot_df = get_state_df(df, view)
else:
    plot_df = df.copy()

republican_color = "#F2545B"
democrat_color = "#216681"

if party == "Democrats":
    y_axis_field = "2020 Democrat vote %"
    plot_color = democrat_color
else:
    y_axis_field = "2020 Republican vote %"
    plot_color = republican_color

medianCol1, meanCol1 = st.columns(2)
giniCol1 = st.columns(1)[0]

gini_scatter_plot = get_scatter_plot(
    "Gini Index", 
    y_axis_field, 
    "Gini Index", 
    "Party Votes (percentage)", 
    "Gini Index"
)

giniCol1.plotly_chart(gini_scatter_plot, use_container_width=True)

mean_scatter_plot = get_scatter_plot(
    "Mean income (dollars)",
    y_axis_field,
    "Mean income (dollars)",
    "Party Votes (percentage)",
    "Mean income (dollars)"
)

meanCol1.plotly_chart(mean_scatter_plot, use_container_width=True)

median_scatter_plot = get_scatter_plot(
    "Median income (dollars)",
    y_axis_field,
    "Median income (dollars)",
    "Party Votes (percentage)",
    "Median income (dollars)"
)

medianCol1.plotly_chart(median_scatter_plot, use_container_width=True)

medianCol2, meanCol2 = st.columns(2)
giniCol2 = st.columns(1)[0]

gini_matrix_plot = get_corr_matrix_plot("Gini Index", y_axis_field)

giniCol2.plotly_chart(gini_matrix_plot, use_container_width=True)

mean_matrix_plot = get_corr_matrix_plot("Mean income (dollars)", y_axis_field)

meanCol2.plotly_chart(mean_matrix_plot, use_container_width=True)

median_matrix_plot = get_corr_matrix_plot("Median income (dollars)", y_axis_field)

medianCol2.plotly_chart(median_matrix_plot, use_container_width=True)