### --- bibliotecas --- ###

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go


### --- bibliotecas necessárias --- ###
import numpy as np
import datetime
from numpy import inner
from pandas.core.internals import concat
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title = 'Visão entregadores', page_icon = '🏍', layout = 'wide')


### --- import dataset --- ###
# lendo o dataset importado e criando a variável 'trains.

df = pd.read_csv('train.csv')


### --- limpeza dos dados --- ###

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


### =================================================== ###
#                   Barra lateral                         #
### =================================================== ###

## criando a barra lateral:

st.markdown('### Marketplace - Visão Entregadores')


## importando a imagem: 
image_path = 'IMG.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)


## informações da barra lateral. 
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Rapidez em delivery in town')
st.sidebar.markdown(""" --- """)


# filtro para seleção de data limite.
st.sidebar.markdown('#### Selecione uma data limite') 

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime(2022, 4, 13),
    min_value = pd.datetime(2022, 2, 11),
    max_value = pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY')


st.sidebar.markdown(""" --- """)
    

## multipla seleção das condições de trânsito:
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown(""" --- """)

st.sidebar.markdown('### Powered by Geraldo Pedro Dambros')


# filtro de data:
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


# filtro de trânsito:
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]


### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])


with tab1:
    with st.container(): # primeiro container - 
        st.markdown('#### Overall Metrics:')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
             maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
             col1.metric('Maior idade', maior_idade)            

        with col2:
             menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
             col2.metric('Menor idade', menor_idade)           
        
        with col3:
             melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
             col3.metric('Melhor veículo', melhor_condicao)                                
                                            
        with col4:
             pior_condicao = df1.loc[:,'Vehicle_condition'].min()
             col4.metric('Pior veículo', pior_condicao)                               
             
                
    with st.container(): # segundo container - 
        st.markdown( """ --- """ )
        st.markdown('### Avaliações:')
        
        col1, col2 = st.columns(2)
        
        with col1:
             st.markdown('#### Média por entregador:')
             df_avg_ratings_delivery = (df1.loc[:, ['Delivery_person_Ratings','Delivery_person_ID']]
                                          .groupby('Delivery_person_ID')
                                          .mean().reset_index())            
             st.dataframe(df_avg_ratings_delivery)
            
            
        with col2:
             st.markdown('#### Média por trânsito:') # média por trânsito -
            
             df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                                 .groupby('Road_traffic_density')
                                                 .agg({'Delivery_person_Ratings': ('mean', 'std')})).round(2)

             df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

             df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
             st.dataframe(df_avg_std_rating_by_traffic)
            
             st.markdown('#### Média por clima:') # média por clima -

             df_rating_by_Weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                         .groupby('Weatherconditions')
                                         .agg({'Delivery_person_Ratings': ('mean', 'std', 'median')})
                                         .round(2))

             df_rating_by_Weather.columns = ['média', 'desvio_padrão','mediana']

             df_rating_by_Weather = df_rating_by_Weather.reset_index()
             st.dataframe(df_rating_by_Weather)
            
    
    with st.container(): # terceiro container - 
        st.markdown ( """ --- """ )
        st.markdown('### Velocidade de entrega:')
        col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Top entregadores rápidos:')
        
        df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                  .groupby(['City', 'Delivery_person_ID'])
                  .mean()
                  .sort_values(['City', 'Time_taken(min)'], ascending=True).reset_index())

        df_aux_01 = df2.loc[df2['City'] == 'Metropolitian', :].head(5)
        df_aux_02 = df2.loc[df2['City'] == 'Urban', :].head(5)
        df_aux_03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(5)

        df3 = pd.concat([df_aux_01, df_aux_02, df_aux_03]).reset_index(drop=True)

        st.dataframe(df3)
                                      
    with col2:        
        st.markdown('#### Top entregadores lentos:')
        
        df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                  .groupby(['City', 'Delivery_person_ID'])
                  .mean()
                  .sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index())

        df_aux_01 = df2.loc[df2['City'] == 'Metropolitian', :].head(5) 
        df_aux_02 = df2.loc[df2['City'] == 'Urban', :].head(5)
        df_aux_03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(5)

        df3 = pd.concat([df_aux_01, df_aux_02, df_aux_03]).reset_index(drop=True)
        
        st.dataframe(df3.round(0))