import streamlit as st
from streamlit_option_menu import option_menu ## menu para o sidebar

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

##Carregar os arquivos##

dados_bignumbrs = pd.read_parquet('./dados_bignumber.parquet')
dados_serietemporal = pd.read_parquet('./dados_serietemporal.parquet')
dados_boxplot= pd.read_parquet('./dados_boxplot.parquet')
dados_estudo= pd.read_parquet('./dados_estudo.parquet')

## Grupo de Funções##

def gerar_grafico_serie( dados_serie ):
    '''
    Função renderizar o gráfico de série temporal
    Parametro: uma base de dados no formato especifico
    '''

    # Criar figura
    Figura = go.Figure()

    # Adicionar série temporal diária
    Figura.add_trace(
        go.Scatter(
            x=dados_serie.index,
            y=dados_serie['media_preco'],
            mode='lines',
            name='Diário',
            line=dict(color='#157806')
        )
    )

    # Adicionar média móvel de 7 dias
    Figura.add_trace(
        go.Scatter(
            x=dados_serie.index,
            y=dados_serie['mm7d'],
            mode='lines',
            name='mm7d',
            line=dict(color='#1af0ac', width=2)
        )
    )

    # Adicionar média móvel de 30 dias com janela rolante de 20 dias
    Figura.add_trace(
        go.Scatter(
            x=dados_serie.index,
            y=dados_serie['mm30d'].rolling(window=20).mean(),
            mode='lines',
            name='mm30d',
            line=dict(color='#adf03a', width=2)
        )
    )

    # Títulos e labels
    Figura.update_layout(
        title='Série Temporal | Preço megawatt-hora (MWh) €',
        xaxis_title='Data',
        yaxis_title='Preço em EURO €',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
        ),
        height=500,
        width=1200
    )

    return Figura

def gerar_grafico_outliers( dados_serie ):
    
    # Filtrar dados para remover outliers
    dados_filtrados = dados_serie.loc[dados_serie['euros_per_mwh'] < 4000]

    # Criar figura
    Figura2 = go.Figure()

    # Adicionar um boxplot para cada mês (assumindo que 'data_boxplot' contém a categoria mensal)
    for categoria in dados_filtrados['data_boxplot'].unique():

        Figura2.add_trace(go.Box(
            y=dados_filtrados[dados_filtrados['data_boxplot'] == categoria]['euros_per_mwh'],
            name=categoria,
            boxmean='sd',  # Para mostrar a média e desvio padrão no boxplot
            width=0.5,
            marker_color='#db4061'
        ))

    # Títulos e labels
    Figura2.update_layout(
        title='Distribuição de Preço megawatt-hora (MWh) € | Mensal',
        xaxis_title='Mês',
        yaxis_title='Preço em EURO €',
        xaxis={'type': 'category'},  # Para garantir que os meses sejam categóricos
        height=500,
        width=1200,
        showlegend=False
    )

    # Rotacionar os rótulos do eixo x
    Figura2.update_xaxes(tickangle=90)

    return Figura2

def gerar_grafico_estudo( dados, ano, mes ):

    # ANO , MES -> Interação do usuário no Front-end

    # Filtrar o ano e mes que o usuário está setando no FRONT-END
    Filtro = dados.loc[ (dados.ano == ano) & (dados.mes == mes) ]
    
    # Analise
    anl_estudo = Filtro.groupby( by=['dia', 'hora'] ).agg(
        media_preco = ('euros_per_mwh', 'mean')
    ).reset_index()

    # Pivotar a tabela
    anl_estudo = anl_estudo.pivot_table( index='hora', columns='dia', values='media_preco')

    # Ordenacao
    anl_estudo = anl_estudo.sort_index()

    # Ajuste no index
    anl_estudo.index = anl_estudo.index.astype(str)

    # Criar heatmap
    Figura3 = go.Figure(
        data=go.Heatmap(
            z=anl_estudo.values,
            x=anl_estudo.columns,
            y=anl_estudo.index,
            colorscale='Reds',
            showscale=True,
            colorbar=dict(thickness=10, len=0.5)
        )
    )

    # Títulos e labels
    Figura3.update_layout(
        title=f'Comportamento entre horário e dia',
        xaxis_title='Dias',
        yaxis_title='Horário',
        height=700,
        width=1200
    )

    return Figura3



##Front-end##

#Título - Subtitulo da página

st.set_page_config(
    page_title='Análise de Dados',
    page_icon='logo_python.png',
    layout='wide'

)

#Siderbar Superior

st.sidebar.image('logo_enefit.png')
st.sidebar.title('Analytics')

##customizando a sidebar##

with st.sidebar:

    #menu de seleção

    selected = option_menu(
        #titulo
        'Menu',
        #Opções de navegação

        ['Dashboard', 'Tático','Operacional'],

        #Icones para o menu de opções

        icons=['bar-chart-fill','bar-chart-fill','bar-chart-fill'],

        #icone para o menu pricipal

        menu_icon='cast',

        #seleção padrão
        default_index=0,

        #estilos

        styles={
            'menu-title': {'font-size': '18px'}, #diminuiu o tamanho da fonte do título
            'menu-icon': {'display': 'none'}, # remove o icone do título
            'icon': {'font-size': '12px'}, #estilo dos icones
            'nav-link':{'font-size': '15px', '--hover-color': '#6052d9'}, #cor de fundo ao passar o mouse
            'nav-link-selected': {'background-color': '#157806'}, #cor de funfo do item selecionado.
        }



    )

    # navegação das páginas

if selected ==  'Dashboard':
        #título da página
        st.title('Análise Indicadores de Energia')

        #big Numbers | superiores

        st.subheader('Estatísticas dos preços')

        #Futuramente tem que conectar na base de dados

        big_2021 = dados_bignumbrs[dados_bignumbrs.ano==2021]['media'].round(1)
        big_2022= dados_bignumbrs[dados_bignumbrs.ano==2022]['media'].round(1)
        big_2023 = dados_bignumbrs[dados_bignumbrs.ano==2023]['media'].round(1)
        big_media = dados_bignumbrs[dados_bignumbrs.ano==2024]['media'].round(1)

        #frame para incluir os big numbers
        #4colunas

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.metric('Preço médio 2021 ', big_2021)
        
        with col2:
            st.metric('Preço médio 2021 é: ', big_2022)
        with col3:
            st.metric('Preço médio 2021 é: ', big_2023)
        with col4:
            st.metric('Preço médio 2021 é: ', big_media)

        #Gráfico de série temporal
        chamar_grafico =  gerar_grafico_serie(dados_serietemporal)
        st.plotly_chart(chamar_grafico)

        #Gráfico de boxplot
    
        chamar_grafico2= gerar_grafico_outliers(dados_boxplot)
        st.plotly_chart(chamar_grafico2)

        # Indicador Dinâmico 
        st.subheader('Estudo do preço comparando Dia vs Horário do consumo')

        #filtros

        lista_ano = [2023,2022,2021]
        lista_meses = [mes for mes in range(1,13)]

        #tabelas
        col1,col2,col3 = st.columns(3)

        with col1:
            selecione_ano= st.selectbox('Selecione o ano', lista_ano)
        with col2:
            selecione_mes= st.selectbox('Selecione o mês', lista_meses)

        #Gráfico de calor
        
        chamar_grafico3 = gerar_grafico_estudo(dados_estudo,selecione_ano,selecione_mes)
        st.plotly_chart(chamar_grafico3)

        #rodapé
        st.markdown(
            '''
                <hr styles ='border': 1px solid #d3d3d3;'/>
                <p styles = 'text-align: center; color: gray;'>
                    Dashboard de custo de Energia | Dados Fornecidos por Enefit | Desenvolvido por Odemir Depieri Jr e aplicado em aula por Gabriela Santana | 2024
                </p>


            ''',
            unsafe_allow_html=True

        )



elif selected == 'Tático':
        pass
elif selected =='Operacional':
        pass
else:
        pass

