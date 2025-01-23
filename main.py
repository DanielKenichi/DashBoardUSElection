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