
def QM1(dataf):
    print('1. Qual a distância média percorrida por viagens com no máximo 2 passageiros')
    plt.figure(figsize=(10,6))
    sns.barplot(x=dataf[dataf['passenger_count'] <= 2] \
                .groupby(by=['passenger_count']) \
                .agg({'trip_distance':'mean'}) \
                .reset_index()['passenger_count'],
                
                y=dataf[dataf['passenger_count'] <= 2] \
                .groupby(by=['passenger_count']) \
                .agg({'trip_distance':'mean'}) \
                .reset_index()['trip_distance']);
    
    plt.ylabel('')

def QM2(dataf):
    print('2. Quais os 3 maiores vendors em quantidade total de dinheiro arrecadado;')
    plt.figure(figsize=(8, 6))
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
    
def QM3(dataf):  
    print('3. Faça um histograma da distribuição mensal, nos 4 anos, de corridas pagas em dinheiro;')
    plt.figure(figsize=(15,8))
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
    
def QM4(dataf):
    print('4. Faça um gráfico de série temporal contando a quantidade de gorjetas de cada dia, nos últimos 3 meses de 2012.')
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
    fig.show()
    
def bonus1(dataf):
    print('Qual o tempo médio das corridas nos dias de sábado e domingo;')
    fig = plt.figure(figsize=(14,10))
    sns.lineplot(data=dataf[(dataf['Dia_semana'] == 5) | (dataf['Dia_semana'] == 6)], 
             x="pickup_day", y="min_diff", hue="Dia_semana",palette='colorblind', style="Dia_semana", legend=False)
    plt.axhline(dataf['min_diff'][(dataf['Dia_semana'] == 5) | (dataf['Dia_semana'] == 6)].mean(), color='r',
            linestyle='--')
    plt.title('Tempo de corridas no Sábado e Domingo') 
    plt.ylabel('quantidade em minutos')
    plt.xlabel('')
    plt.legend(['Sábado','Domingo', 'Média'])
    fig.show()
