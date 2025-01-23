import streamlit as st

from dataset.get_dataset import get_dataframe

st.set_page_config(
    page_title="Etapa 2 PVD",
)

st.write("# Etapa 2 - PVD")

st.sidebar.success("Selecione a hipótese a ser exibida")

st.markdown(
    """
    ### Alunos
    - Daniel Kenichi Tiago Tateishi - RA: 790837 
    - Natália Bachiega Magalhães - RA: 769846 
    - Vinícius Quaresma da Luz - RA: 769836
    - Matheus Henrique Cassatti - RA: 771050
    """
)

df = get_dataframe()
st.title("Dataset utilizado")

'''
O dataset utilizado foi o "Ultimate US Election Dataset" disponível no Kaggle por meio [deste link](https://www.kaggle.com/datasets/essarabi/ultimate-us-election-dataset?resource=download).

Nós realizamos algumas operações de limpeza nos dados, afim de remover símbolos inválidos, converter alguns dados binarizados para uma codificação válida, dentre outras medidas. O resultado é exibido na tabela interativa abaixo.
'''

st.dataframe(df)

'''
# Sobre este trabalho

Nós utilizamos a biblioteca `streamlit` para montar esta dashboard interativa. O Streamlit permite parametrizar páginas interativas, transformando-as em dashboards, mas sem *entrar no caminho* da análise dos dados.

Ainda utilizamos as bibliotecas usuais, como a Pandas, para manipular os dados, mas o Streamlit permite adicionar uma camada de interação nesse processo.

Nós também fizemos uso do Plotly, associado ao streamlit, para exibir gráficos interativos.

A documentação oficial do Streamlit pode ser acessada por meio do link https://docs.streamlit.io/develop/api-reference/. Já a documentação oficial do Plotly pode ser acessada por meio do link https://plotly.com/python/.

## Sobre a interatividade

Utilizamos o streamlit para permitir interação, não apenas para controlar os filtros que atuam sobre os dados, mas também para permitir interagir com os gráficos que são exibidos. Isso melhora a exibição, sem distanciar a maneira como o código da análise dos dados em si é executada.

Além da documentação oficial, consideramos o vídeo abaixo como uma boa introdução ao streamlit.
'''

st.video('https://youtu.be/D0D4Pa22iG0')