# Databricks notebook source
import json
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn import metrics
import seaborn as sns
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# Header
st.title('Análise de Ativos Digitais')

# Conecta ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['your_db']
collection = db['your_collection']

# Carrega dados para um DataFrame
records = list(collection.find())
data = pd.json_normalize(records, sep='_')

# Remove a coluna ObjectId
data = data.drop(columns=['_id'])

# Converte last_updated para datetime
data['last_updated'] = pd.to_datetime(data['last_updated'])

# Verifica se a coluna 'name' está presente no DataFrame
if 'name' in data.columns:
    ativos = data['name'].unique().tolist()
else:
    st.error("A coluna 'name' não está disponível nos dados.")
    st.stop()

# Presumindo que você tenha um DataFrame chamado data_ativo
data_ativo = pd.DataFrame(data)

# Adicionando oscilações
def get_oscillation_data(data):
    np.random.seed(0)  
    t = np.linspace(0, data.shape[0], data.shape[0])
    noise = np.random.normal(0, 0.05, data.shape[0])  
    data['open'] = data['circulating_supply'] + np.sin(t) * data['circulating_supply'] * 0.1 + noise
    data['close'] = data['circulating_supply'] + np.cos(t) * data['circulating_supply'] * 0.1 + noise
    data['high'] = data[['open', 'close']].max(axis=1) + data['circulating_supply'] * 0.05
    data['low'] = data[['open', 'close']].min(axis=1) - data['circulating_supply'] * 0.05
    return data

# Presumindo que 'data' seja um DataFrame pandas
data_ativo = get_oscillation_data(data_ativo)

# Sidebar Esquerda
st.sidebar.header('Configurações')

# Dropdown para selecionar ativo
ativos = data['name'].unique().tolist()
ativo_selecionado = st.sidebar.selectbox('Selecione o ativo', ativos)

# Filtrar dados pelo ativo selecionado
data_ativo = data[data['name'] == ativo_selecionado]

# Radio button para selecionar o intervalo de tempo
intervalo = st.sidebar.radio('Selecione o intervalo de tempo', ['1 hora', '6 horas', '12 horas', '24 horas'])

# Opções de Compra e Venda
st.sidebar.header('Compra e Venda')
if st.sidebar.button('Comprar'):
    st.sidebar.success('Compra realizada com sucesso!')
if st.sidebar.button('Vender'):
    st.sidebar.success('Venda realizada com sucesso!')
    
# Suponho que você tenha um DataFrame chamado data_ativo
# Vou criar um exemplo de DataFrame aqui para simular
data = {'last_updated': pd.date_range(start='2023-10-01', periods=10, freq='H'),
        'total_supply': range(10, 20),
        'circulating_supply': range(1, 11)}
data_ativo = pd.DataFrame(data)


# Content Central
st.header(f'Análise Detalhada do Ativo: {ativo_selecionado}')

# Criando colunas 'open', 'high', 'low', e 'close' usando 'total_supply' e 'circulating_supply'
data_ativo['open'] = data_ativo['total_supply'] - data_ativo.get('circulating_supply', 0)  
data_ativo['close'] = data_ativo['total_supply']
data_ativo['high'] = data_ativo['total_supply'] + (data_ativo['total_supply'] - data_ativo.get('circulating_supply', 0))  
data_ativo['low'] = data_ativo['total_supply'] - (data_ativo['total_supply'] - data_ativo.get('circulating_supply', 0))  

# Verifica se as colunas necessárias existem
if all(col in data_ativo.columns for col in ['open', 'high', 'low', 'close', 'last_updated']):
    # Cria subplots
    fig_candlestick = make_subplots(rows=1, cols=1, subplot_titles=('Candlestick',),
                                    shared_xaxes=True)

    # Adiciona gráfico de Candlestick
    fig_candlestick.add_trace(go.Candlestick(x=data_ativo['last_updated'],
                                             open=data_ativo['open'],
                                             high=data_ativo['high'],
                                             low=data_ativo['low'],
                                             close=data_ativo['close'],
                                             name='Candlesticks'))

    # Adiciona indicadores técnicos (exemplo: médias móveis)
    data_ativo['MA5'] = data_ativo['close'].rolling(window=5).mean()
    data_ativo['MA20'] = data_ativo['close'].rolling(window=20).mean()

    fig_candlestick.add_trace(go.Scatter(x=data_ativo['last_updated'], y=data_ativo['MA5'], name='MA5',
                                         line=dict(color='blue', width=1)))
    fig_candlestick.add_trace(go.Scatter(x=data_ativo['last_updated'], y=data_ativo['MA20'], name='MA20',
                                         line=dict(color='orange', width=1)))

    # Atualiza layout
    fig_candlestick.update_layout(xaxis_title='Data', yaxis_title='Preço', template="plotly_dark",
                                  xaxis_rangeslider_visible=False)

    # Exibi o gráfico
    st.plotly_chart(fig_candlestick, use_container_width=True)
else:
    st.error("As colunas necessárias para criar o gráfico de Candlestick não estão disponíveis nos dados.")


# Carrega dados para um DataFrame
data = pd.json_normalize(list(collection.find()), sep='_')

# Remove a coluna ObjectId
data = data.drop(columns=['_id'])

# Converte last_updated para datetime
data['last_updated'] = pd.to_datetime(data['last_updated'])

# Verifica se a coluna 'name' está presente no DataFrame
if 'name' in data.columns:
    # Obter a lista de ativos dos dados
    ativos = data['name'].unique().tolist()
else:
    st.error("A coluna 'name' não está disponível nos dados.")
    st.stop()

# Certifique-se de que a variável ativos_selecionados é definida antes de ser usada
ativos_selecionados = st.sidebar.multiselect('Selecione os ativos para comparação', ativos, default=ativos[:3])


# Content Central
st.header('Gráficos 3D Visualizações de Dados Multidimensionais')

# Verifica se as colunas 'volume' e 'volatility' 
if 'volume' not in data_ativo.columns:
    data_ativo['volume'] = np.random.rand(len(data_ativo)) 
if 'volatility' not in data_ativo.columns:
    data_ativo['volatility'] = np.random.rand(len(data_ativo))  



# Adicionando um gráfico 3D para visualizar preço, volume e volatilidade
fig_3d = go.Figure(data=[go.Surface(z=data_ativo[['close', 'volume', 'volatility']].values)])

fig_3d.update_layout(title='3D Gráfico de superfície de preço, volume e volatilidade',
                     scene=dict(
                         xaxis_title='Preço',
                         yaxis_title='Volume',
                         zaxis_title='Volatilidade'
                     ),
                     margin=dict(l=0, r=0, t=30, b=0),
                     template="plotly_dark")

# Exibir o gráfico 3D
st.plotly_chart(fig_3d, use_container_width=True)



# Verifica se algum ativo foi selecionado
if not ativos_selecionados:
    st.warning('Por favor, selecione pelo menos um ativo para análise.')
    st.stop()

# Filtra dados pelos ativos selecionados
data_ativos = data[data['name'].isin(ativos_selecionados)]

# Content Central
st.header('Análise Comparativa de Ativos Digitais')

# Cria gráfico de radar para comparação de ativos
fig = go.Figure()

for ativo in ativos_selecionados:
    ativo_data = data_ativos[data_ativos['name'] == ativo].mean(numeric_only=True) 
    metrics = ['total_supply', 'market_cap', 'volume_24h'] 
    
    # Verificar se as métricas existem no DataFrame
    metrics = [metric for metric in metrics if metric in ativo_data.index]

    fig.add_trace(go.Scatterpolar(
        r=[ativo_data[metric] for metric in metrics],
        theta=metrics,
        fill='toself',
        name=ativo
    ))

# Atualiza layout
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, data_ativos[metrics].max().max()]  
        )),
    showlegend=True,
    title="Comparação de Ativos Digitais"
)

# Exibir o gráfico de radar
st.plotly_chart(fig, use_container_width=True)


# Carrega dados para um DataFrame
data = pd.json_normalize(list(collection.find()), sep='_')

# Filtra o DataFrame para conter apenas as colunas 'name' e 'total_supply'
data = data[['name', 'total_supply']]

# Remove linhas com valores NaN em 'total_supply'
data = data.dropna(subset=['total_supply'])

# Converte 'total_supply' para numérico
data['total_supply'] = pd.to_numeric(data['total_supply'], errors='coerce')

# Remove linhas com valores NaN após a conversão
data = data.dropna(subset=['total_supply'])

# Pivotar o DataFrame para ter ativos como colunas e total_supply como valores
data_pivot = data.pivot(columns='name', values='total_supply')

# Calcula a matriz de correlação
correlation_matrix = data_pivot.corr()

# Content Central
st.header('Correlação de Ativos com base em Total Supply')

# Cria um heatmap da matriz de correlação
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1)
st.pyplot(plt.gcf())



# Histograma
st.subheader('Histograma de Preços de Fechamento')
hist = go.Figure(data=[go.Histogram(x=data_ativo['close'], nbinsx=50)])
hist.update_layout(
    title_text='Distribuição de Preços de Fechamento',
    xaxis_title_text='Preço',
    yaxis_title_text='Frequência',
)

st.plotly_chart(hist)


# Carrega dados para um DataFrame
records = list(collection.find())
data = pd.json_normalize(records, sep='_')

data = data[['name', 'last_updated', 'total_supply']]
data['last_updated'] = pd.to_datetime(data['last_updated'])

# Cria um DataFrame pivot para transformar os nomes dos ativos em colunas
data_pivot = data.pivot(index='last_updated', columns='name', values='total_supply').fillna(0)

# Cria um gráfico de área empilhada interativo usando Plotly
fig = px.area(data_pivot.reset_index(), 
              x='last_updated', 
              y=data_pivot.columns, 
              title='Distribuição do Portfólio ao Longo do Tempo')

# Ajusta o layout
fig.update_layout(xaxis_title='Data',
                  yaxis_title='Total Supply',
                  legend_title='Ativos')

# Mostra o gráfico no aplicativo Streamlit
st.plotly_chart(fig)



# Verifica se as colunas 'volume' e 'volatility' existem
if 'volume' not in data_ativo.columns:
    data_ativo['volume'] = np.random.rand(len(data_ativo))  
if 'volatility' not in data_ativo.columns:
    data_ativo['volatility'] = np.random.rand(len(data_ativo)) 



# Footer
st.markdown('Emerson Amorim')
st.markdown('Copyright © 2023')