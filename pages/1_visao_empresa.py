### --- bibliotecas --- ###
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go


### --- bibliotecas necessárias --- ###
from datetime import date
import datetime
from datetime import time
from datetime import datetime
from numpy import inner
from pandas.core.internals import concat
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title = 'Visão empresa', page_icon = '🏢', layout = 'wide')


####### --- import dataset --- #######

# lendo o dataset importado e criando a variável 'trains.
df = pd.read_csv('train.csv')


####### --- limpeza dos dados --- #######
df1 = df.copy()


## 1. convertendo a coluna 'Delivery_person_Age' de 'string' para 'int':
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy() # explicação - falta....


linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy() # explicação - falta....


linhas_selecionadas = (df1['City'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy() # explicação - falta....


linhas_selecionadas = (df1['Festival'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy() # explicação - falta....


## convertendo de string para 'int':
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )


## 2. convertendo a coluna 'Delivery_person_Ratings' de 'string' para 'float':
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype ( float )      


## 3. convertendo a coluna 'Order_Date' de 'string' para 'data':
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')


## 4. convertendo a coluna 'multiple_deliveries' de 'string' para 'int':
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )


## 5. removendo os espaços dentro de strins/texto/object
#df1 = df1.reset_index( drop=True)
#for i in range(len(df1)):
#  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

## 6. removendo os espaços dentro de strins/texto/object:
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()


## limpando a coluna de time taken:
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1] )
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )


####### --- Visão empresa --- ########

## 1.0 - quantidade de pedidos por dia
#df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
#px.bar(df_aux, x = 'Order_Date', y= 'ID')


### =================================================== ###
#                   Barra lateral                         #
### =================================================== ###


st.markdown('#### Marketplace - Visão Cliente')

## colocando a imagem: 
image_path = 'IMG.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)


## informações da barra lateral. 
st.sidebar.markdown('## Cury Company')
st.sidebar.markdown('### Rapidez em delivery in town')
st.sidebar.markdown(""" --- """)


# filtro para seleção de data limite.
st.sidebar.markdown('#### Selecione uma data limite:') 

date_slider = st.sidebar.slider(
    'Até qual data deseja analisar?',
    value = pd.datetime(2022, 4, 13),
    min_value = pd.datetime(2022, 2, 11),
    max_value = pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY')

#st.header(date_slider)
st.sidebar.markdown(""" --- """)

#st.dataframe(df1)

## multipla seleção das condições de trânsito:
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown(""" --- """)

st.sidebar.markdown('#### Powered by Geraldo Pedro Dambros')


# filtro de data:
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


# filtro de trânsito:
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###

tab1, tab2, tab3 = st.tabs ((['Visão Gerencial', 
                              'Visão Tática', 
                              'Visão Geográfica']))

####### Construção da tabela 1 #######

with tab1: # visão gerencial
    
    with st.container():
        st.markdown('#### Orders by day') # gráico de barra -
        df_aux = (df1.loc[:, ['ID', 'Order_Date']]
                    .groupby(['Order_Date'])
                    .count()
                    .reset_index())
        fig = px.bar(df_aux, x = 'Order_Date', y= 'ID')
        st.plotly_chart(fig, use_container_width=True)
            
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('#### Ordem por tráfego')
            df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
            df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() * 100
            fig = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density')
            st.plotly_chart(fig, use_container_width=True)
            
            
        with col2:
            st.markdown('#### Tráfego por cidade')
            df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
            st.plotly_chart(fig, use_container_width=True)
            
    
with tab2: # visão tática - gráficos semanais -
    with st.container():
        st.markdown('#### Orde by Week')
        df1['Week_of_year'] = df1['Order_Date'].dt.strftime( '%U' ) 
        df_aux = df1.loc[:, ['ID', 'Week_of_year']].groupby(['Week_of_year']).count().reset_index()
        fig = px.line( df_aux, x= 'Week_of_year', y= 'ID')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('#### Orde Share by Week')   
        df_aux1 = df1.loc[:, ['ID', 'Week_of_year']].groupby(['Week_of_year']).count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby(['Week_of_year']).nunique().reset_index()
        df_aux = pd.merge(df_aux1, df_aux2, how='inner') # juntar dois dataframes.
        df_aux['order_by_deliver'] = df_aux['ID'] / df_aux ['Delivery_person_ID'].round(2)
        fig = px.line(df_aux, x='Week_of_year', y='order_by_deliver')
        st.plotly_chart(fig, use_container_width=True)
        
    
with tab3: # visão geográfica - mapa -
    st.markdown('#### Mapa da cidade')
    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index())

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], 
                      location_info['Delivery_location_longitude']],
                      popup = location_info[['City','Road_traffic_density']]).add_to(map)
    
    folium_static(map, width=1024, height=600) 
    
#st.header('FTC')
#print(df1.head(100))
#print(f'Estou aqui, Geraldo')