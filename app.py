
# importar bibliotecas
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from pathlib import Path
import plotly.express as px

DATA_PATH = Path(st.text_input("Cole aqui o caminho para o arquivo dfconcat.csv"))
st.text('Esse processo pode demorar alguns minutos...')


def load_data(path):
    dataf = pd.read_csv(path / 'dfconcat.csv', index_col='Unnamed: 0')
    return dataf

def solving_columns(dataf):
    dataf['dropoff_day']= dataf['dropoff_day'].astype("datetime64")
    dataf['pickup_day']= dataf['pickup_day'].astype("datetime64")
    return dataf

# carregar os dados
df = solving_columns(load_data(DATA_PATH))

def QM1(dataf):
    fig = plt.figure(figsize=(10,6))
    sns.barplot(x=dataf[dataf['passenger_count'] <= 2] \
                .groupby(by=['passenger_count']) \
                .agg({'trip_distance':'mean'}) \
                .reset_index()['passenger_count'],
                
                y=dataf[dataf['passenger_count'] <= 2] \
                .groupby(by=['passenger_count']) \
                .agg({'trip_distance':'mean'}) \
                .reset_index()['trip_distance']);
    
    plt.ylabel('')
    return fig

def QM2(dataf):
    fig = plt.figure(figsize=(8,6))
    sns.barplot(x=dataf.groupby(by=['vendor_id']).agg({'total_amount':'sum'}) \
                .sort_values('total_amount', ascending = False) \
                .reset_index()[:3]['vendor_id'], 
                
                y=dataf.groupby(by=['vendor_id']) \
                .agg({'total_amount':'sum'}) \
                .sort_values('total_amount', ascending = False) \
                .reset_index()[:3]['total_amount']/100,
                
                hue=dataf.groupby(by=['vendor_id']) \
                .agg({'total_amount':'sum'}) \
                .sort_values('total_amount', ascending = False) \
                .reset_index()[:3]['vendor_id'], palette="deep", dodge=False)
    
    plt.title('Valor total agrupado por vendor') 
    plt.ylabel('')
    plt.xlabel('')
    return fig

def QM3(dataf):
    fig = plt.figure(figsize=(15,8))
    sns.barplot(data = dataf[dataf['payment_type'] == 'cash'] \
                    .groupby(dataf['dropoff_day'].dt.to_period('M')) \
                    .agg({'total_amount':'sum'}) \
                    .reset_index(), x='dropoff_day', y='total_amount')
    plt.xticks(rotation=90)
    plt.title('Soma de pagamentos em dinheiro agrupado por mês')
    plt.legend(['Total'], fontsize=13)
    plt.ylabel('')
    plt.xlabel('');
    plt.show()
    return fig

def QM4(dataf):
    fig = plt.figure(figsize=(12,8))
    fig = px.bar(x=dataf[(dataf['dropoff_day'].dt.year == 2012) & (dataf['dropoff_day'].dt.month >= 8)] \
                .groupby(by=dataf["dropoff_day"]) \
                .agg({'tip_amount':'sum'}) \
                .reset_index()['dropoff_day'],
                 
                 y=dataf[(dataf['dropoff_day'].dt.year == 2012) & (dataf['dropoff_day'].dt.month >= 8)] \
                .groupby(by=dataf["dropoff_day"]) \
                .agg({'tip_amount':'sum'}) \
                .reset_index()["tip_amount"], 
                 
                 color=dataf[(dataf['dropoff_day'].dt.year == 2012) & (dataf['dropoff_day'].dt.month >= 8)] \
                .groupby(by=dataf["dropoff_day"]) \
                .agg({'tip_amount':'sum'}) \
                .reset_index()["dropoff_day"].dt.month, 
                 
                title="Gorjeta por dia", 
                labels={'x':'day',
                        'y':'tip'}, 
                color_continuous_scale='portland', 
                opacity=0.7)
    return fig

def bonus1(dataf):
    fig = plt.figure(figsize=(18,14))
    sns.lineplot(data=dataf[(dataf['Dia_semana'] == 5) | (dataf['Dia_semana'] == 6)], 
             x="pickup_day", y="min_diff", hue="Dia_semana",palette='colorblind', style="Dia_semana", legend=False),
    plt.axhline(dataf['min_diff'][(dataf['Dia_semana'] == 5) | (dataf['Dia_semana'] == 6)].mean(), color='r',
            linestyle='--')
    plt.title('Tempo de corridas no Sábado e Domingo') 
    plt.ylabel('quantidade em minutos')
    plt.xlabel('')
    plt.legend(['Sábado','Domingo', 'Média'])
    return fig

#criando o app
st.image('DataSprint.png')
st.header('Resultado das questões')
st.markdown('AQUI VAI ENTRAR O GITHUB DO PROJETO')

opcao = st.selectbox( 'Selecione a opção desejada', ('Resposta 1', 'Resposta 2', 'Resposta 3', 'Resposta 4', 'Bônus 1'))

if opcao == 'Resposta 1':
    st.markdown('1. Qual a distância média percorrida por viagens com no máximo 2 passageiros')
    st.pyplot(QM1(df))
    
if opcao == 'Resposta 2':
    st.markdown('2. Quais os 3 maiores vendors em quantidade total de dinheiro arrecadado;')
    st.pyplot(QM2(df))
    
if opcao == 'Resposta 3':
    st.markdown('3. Faça um histograma da distribuição mensal, nos 4 anos, de corridas pagas em dinheiro;')
    st.write(QM3(df))

if opcao == 'Resposta 4':
    st.markdown('4. Faça um gráfico de série temporal contando a quantidade de gorjetas de cada dia, nos últimos 3 meses de 2012.')
    st.write(QM4(df))

if opcao == 'Bônus 1':
    st.markdown('Qual o tempo médio das corridas nos dias de sábado e domingo;')
    st.pyplot(bonus1(df))
