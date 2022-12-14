import streamlit as st
from PIL import Image
import emoji

st.set_page_config(
#    page_title = 'Home',
    page_icon =  '🌏'
)  

#image_path = '\Users\Geraldo\desktop\ComunidadeDS\FTC\Record\Dataset'
image_path = 'IMG.png'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)


## informações da barra lateral. 
st.sidebar.markdown('## Cury Company')
st.sidebar.markdown('### Rapidez em delivery in town')
st.sidebar.markdown( """ --- """ )

st.write('### Cury Company - Dashboard - Análise de crescimento') 

st.markdown(
    """
    Este Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    
    ### Como utilizar esse Growth Dashboad?
 
    - #### Visão empresa:
        - Visão gerencial: métricas gerais de comportamento;
        - visão tática: indicadores semanais de crescimento;
        - visão geográfica: insights de geolocalização.
    
    - #### Visão entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
        
    - #### Visão restaurante:
        - indicadores semanais de crescimento dos restaurantes.
    
    ### Ask for Help
    - Time de Data Science:
        - email: geraldodambrostrader@gmail.com
""")