import streamlit as st

# Definir um titulo
st.title('Evento | Dashboard com Python')

# Cabeçalho de uma seção
st.header('Conhecendo os elementos do Streamlit')

# subtítulo
st.subheader('Aula 2 [2/4]')

# texto simples
st.text('Nesta aula vamos entender os elementos do Streamlit')

# texto formatado usando Markdown
st.markdown('# Stremlit')

st.write('Stream é uma framework de alto nível do Python!')

if st.button('Botão'):
    st.write('Botão selecionado!')

if st.checkbox('Checkbox para opções.'):
    st.write('Usuário selecionou')

escolha = st.radio('Qual linguagem mais utiliza:', ('Python', 'R', 'Java', 'JavaScript', 'Outra'))

Lista_Frameworks = ['Matplotlib', 'Seaborn', 'Plotly']
opcao = st.selectbox('Escolha seu framework favorito de Data Visualization:', Lista_Frameworks)

Lista_Estudo = ['Pandas', 'Numpy', 'Matplotlib', 'Seaborn', 'Plotly', 'Scipy', 'TensorFlow']
selecoes = st.multiselect('Escolha múltiplas opções:', Lista_Estudo )

valor = st.slider('Quantos anos trabalha com Data Science:', 0, 30, 1)

arquivo = st.file_uploader('Escolha um arquivo', type=['csv', 'txt'])

#st.image('logo_python.png', caption='Descritivo da imagem', use_column_width=True)

import pandas as pd
import numpy as np

# Criando um DataFrame base
df = pd.DataFrame(
    { 
        'Dias': [loop for loop in range(31)]
    }
)

# Adicionando novas colunas com dados fictícios
df['Valor de Venda'] = np.random.randint(100, 1000, size=31)
df['Custo'] = df['Valor de Venda'] * 0.8  
df['Lucro'] = df['Valor de Venda'] - df['Custo']
df['Quantidade Vendida'] = np.random.randint(10, 50, size=31)
df['Cliente'] = ['Cliente ' + str(i) for i in range(1, 32)]

# Incluindo a tabela no front
st.dataframe(df)

import altair as alt

# Criando um gráfico de linha com Altair
chart = alt.Chart(df).mark_line().encode(
    x='Dias',
    y='Valor de Venda'
)

# Exibindo o gráfico no Streamlit
st.altair_chart(chart)