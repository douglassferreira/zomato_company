# Labraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
import folium
import inflection
from PIL import Image


# Import dataset
df = pd.read_csv('zomato.csv')
df1 = df.copy()

st.set_page_config(page_title = 'General Information', page_icon = '📝', layout = 'wide')

######################## Funções ######################

# Renomear as colunas do DataFrame
def rename_columns(dataframe):
  df = dataframe.copy()
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new
  return df


# Criação do Tipo de Categoria de Comida
def create_price_type(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

#Preenchimento do nome dos países
COUNTRIES = {
  1: "India",
  14: "Australia",
  30: "Brazil",
  37: "Canada",
  94: "Indonesia",
  148: "New Zeland",
  162: "Philippines",
  166: "Qatar",
  184: "Singapure",
  189: "South Africa",
  191: "Sri Lanka",
  208: "Turkey",
  214: "United Arab Emirates",
  215: "England",
  216: "United States of America",
}
def country_name(country_id):
  return COUNTRIES[country_id]

# Remover valores ausentes (NAs)
def remove_na(dataframe):
  df = dataframe.copy()
  num_col = df.shape[1]
  for i in range(num_col):
    # Verifica se os valores na coluna i são diferentes de NaN
    column_not_nan = df.iloc[:, i].notna()
    # Valores sem NaN:
    df = df.loc[column_not_nan]
  return df
#------------------------------------------ Limpeza do Datafreme --------------------------------------------------

# Renomear Colunas
df1 = rename_columns(df1)

# Remover NAs
df1 = remove_na(df1)

# Criando Colunas
df1["country_name"] = df1.loc[:, "country_code"].apply(lambda x: country_name(x))
df1["price_type"] = df1.loc[:, "price_range"].apply(lambda x: create_price_type(x))


#Categorizar todos os restaurantes somente por um tipo de culinária
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])



#----------------------------------------------------------------------------------------

#######   Barra lateral #########

# Colocar uma imagem de logo

image_path = 'Zomato_logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width = 300)
st.sidebar.markdown('## The world of flavors, in the palm of your hand.')
st.sidebar.markdown("""---""")


st.sidebar.markdown('## Choose the Countries You Want to View Restaurants')
nomes_paises = list(COUNTRIES.values())

countries_options =st.sidebar.multiselect('Countries:',
    nomes_paises,
    default= ['Brazil','England','Qatar','South Africa','Canada','Australia']
)
st.sidebar.markdown("""---""")

# Filtro Countries

linhas_selecionadas = df1['country_name'].isin(countries_options)
df1 = df1.loc[linhas_selecionadas,:]
#-----------------------------------------------------------------------------------------------------------------------------------------

##### Layout #######

with st.container():
    st.title('Zomato Restaurants Dashboard')
    st.markdown("""---""")
    st.markdown('### General information')
    
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.markdown('Registered Restaurants')
        st.subheader(len(df1['restaurant_name']))
    with col2:
        st.markdown('Registered Countries')
        st.subheader(df1.loc[:,'country_code'].nunique())
    with col3:
        st.markdown('Cities Officially Listed')
        st.subheader(df1.loc[:,'city'].nunique())
    with col4: 
        st.markdown('Number of Reviews')
        st.subheader(df1.loc[:,'votes'].sum())
        
    with col5:
        st.markdown('Types of Cuisines ')
        st.subheader(df1.loc[:,'cuisines'].nunique())

#---------------------------------------------------------------------------------------------------------------------------------------
########### Layout #############
with st.container():
# Mapa

  dados = df1.loc[:, ['restaurant_id','country_name','latitude','longitude']]
  dados1 = dados.groupby('country_name').agg({'restaurant_id': 'count', 'latitude': 'first', 'longitude': 'first'}).reset_index()

  map = folium.Map()

  # Loop para adicionar marcadores ao mapa
  for index, location_info in dados1.iterrows():
      popup_info = f"Number of Restaurants: {location_info['restaurant_id']}"  # Construindo a informação do popup
      folium.Marker([location_info['latitude'], location_info['longitude']], popup=popup_info).add_to(map) # Adiciona marcador ao mapa

  folium_static(map, width=1024, height=600)

 
        




