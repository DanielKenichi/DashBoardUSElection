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

st.set_page_config(
    page_title="Income x Party",
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

row1 = st.columns(1)

if party != "Both":
    scatter_plot = px.scatter(
        plot_df, 
        x='Gini Index', 
        y=y_axis_field, 
        title='Gini Index x Party Votes'
    )
    scatter_plot.update_traces(marker=dict(color=plot_color))

scatter_plot.update_layout(
    xaxis_title='Gini Index',
    yaxis_title='Party Votes (percentage)',
)

row1[0].plotly_chart(scatter_plot, use_container_width=True)

row2 = st.columns(1)

correlation_matrix = plot_df[['Gini Index', y_axis_field]].corr()

matrix_plot = go.Figure(
    data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis',
        showscale=True
    )
)

# Add annotations to the heatmap
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
    title='Gini Index x Party votes',
    xaxis_title='Gini Index',
    yaxis_title='Party Votes (percentage)'
)

row2[0].plotly_chart(matrix_plot, use_container_width=True)
