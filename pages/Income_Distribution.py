import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from dataset.get_dataset import get_dataframe
from helpers.pdf_plot import PDFPlot

## Visualization of this graph still needs to be fixed##


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

    return df


st.set_page_config(page_title="Income Distribution", layout="wide")

st.title("Pergunta 2")

st.markdown(
    """
    - Existe correlação entre concentração de renda e o partido de voto por estado?
        - Hipótese1 : Existe uma correlação entre concentração de renda e partido de voto
        - Hipótese2: Não Existe uma correlação entre concentração de renda e partido de voto
    """
)
df = get_dataframe()
mod_df = get_state_data(df)  # Use o dataframe agregado por estado!

col1, col2 = st.columns([1, 1])

with col1:
    selected_state_pdf = st.selectbox(
        "Selecione o estado",
        sorted(df["state"].unique())
    )

df_state_violin = mod_df[mod_df["state"] == selected_state_pdf]

# Violin plot para Mean Income
fig_mean = px.violin(df_state_violin,
                     y="Mean income (dollars)",
                     x="state",
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

'''
    **Imagem:** O gráfico de Velas (ou Candlestick) apresenta a média de 
renda por estado, levando em consideração o partido ganhador
 (Democrata ou Republicano) de cada condado.
'''

# Violin plot para Median Income (similar ao anterior)
fig_median = px.violin(df_state_violin,
                       y="Median income (dollars)",
                       x="state",
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

'''
**Imagem:** O gráfico de Velas (ou Candlestick em inglês)
apresenta a mediana de renda por estado, levando
 em consideração o partido ganhador (Democrata ou Republicano)
   de cada condado.

'''


'''
# Concentração de renda.
'''

# Plota um histograma da renda média
fig, ax = plt.subplots(figsize=(14, 8))
ax.hist(mod_df['Mean income (dollars)'], bins=50,
        color='blue', alpha=0.7, density=True)
ax.set_title('Histograma da Renda Média', fontsize=16)
ax.set_xlabel('Renda Média (dólares)', fontsize=14)
ax.set_ylabel('Densidade', fontsize=14)
st.pyplot(fig)

'''
**Imagem:** Histograma de renda média dos EUA.
'''

concetration_percentage = st.slider("Digite o valor da porcentagem desejada.",
                                    min_value=0.0, max_value=1.0, value=0.05, step=0.01, format="%.2f")

[pdf, x] = PDFPlot().plot(
    desired_percentile=concetration_percentage,
    real_data=mod_df['Mean income (dollars)'].values,
)

st.pyplot(pdf)


st.markdown(
    f'> **Imagem**: Gráfico de área que indica a probabilidade de {(concetration_percentage * 100):.0f}% da população ganhar até US$ {x:.2f}.')

col3, col4 = st.columns([1, 1])

with col3:
    selected_state_pdf = st.selectbox(
        "Selecione o estado para o PDF de renda",
        sorted(df["state"].unique())
    )

with col4:
    df_state_pdf = mod_df[mod_df["state"] == selected_state_pdf]

    concetration_percentage = st.slider(
        "Digite o valor da porcentagem desejada (por estado).",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.01,
        format="%.2f"
    )

[pdf, x] = PDFPlot().plot(
    desired_percentile=concetration_percentage,
    real_data=np.sort(df_state_pdf['Mean income (dollars)'].values),
)

st.pyplot(pdf)

st.markdown(
    f'> **Imagem**: Gráfico de área que indica a probabilidade de {(concetration_percentage * 100):.0f}% da população de {selected_state_pdf} ganhar até US$ {x:.2f}.'
)


'''
## Conclusão

- Em alguns estados há uma disparidade muito elevada na quantidade de condados que votaram nos republicanos e democratas.  Isso causa um desbalanceamento na comparação de renda por partido. Ex: Hawaii (só tem condados que votaram nos democratas) e Kentucky (que 120 condados são Republicanos e apenas 2 são Democratas).
Essa característica dificulta a análise de relação entre renda e partido no estado, já que a quantidade de dados é desbalanceada.

- Alguns estados como Califórnia, Colorado, Maryland,
New Mexico, New York, seus condados com média e mediana mais altas para renda votam nos democratas.


- Em outros estados como Alabama e Mississipi, a maioria dos condados com média e mediana mais altas para renda votam nos republicanos.

- No geral, em 20 estados a renda mais alta é a dos republicanos, contra 26 estados onde a renda mais alta é a dos democratas.
4 estados todos os condados votaram nos democratas e 1 estado todos os condados votaram nos republicanos.
Porém, não dá para se concluir com clareza se no geral, os estados com mais concentração de renda tendem a votar majoritariamente no partido republicano ou democrata, já que a comparação muitos estados é afetada pela diferença na quantidade de dados. 
'''
