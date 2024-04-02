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


st.set_page_config(page_title = 'Countries', page_icon = '🪩', layout = 'wide')
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
st.sidebar.markdown('## The world of flavors, in the palm of your hand')
st.sidebar.markdown("""---""")



#-----------------------------------------------------------------------------------------------------------------------------------------

########### Layout #############

with st.container():
    st.title('Business Information - Countries')
    dados = df1.loc[:, ['restaurant_id','country_name']]
    dados1 = dados.groupby('country_name').count().sort_values(by= 'restaurant_id', ascending = False).head(10).reset_index()
    fig = px.bar(y=dados1['country_name'],x=dados1['restaurant_id'],color = dados1['country_name'],
                 labels= {'x':'Number of restaurants', 'y':'Countries','color' : 'Countries'},
                 title = 'Top 10 Countries with the Most Registered Restaurants', text= dados1['restaurant_id'])
    fig.update_xaxes(range=[0, 4050])
    st.plotly_chart(fig, use_container_width = True)
    


with st.container():
    filtro = df1['price_type'] == 'expensive'
    dados = df1.loc[filtro, ['country_name','price_type']].reset_index()
    dados = dados.groupby('country_name').count().reset_index()
    dados['price_type'] = dados['price_type'].astype(float)
    fig= px.bar(x = dados['country_name'], y = dados['price_type'], color = dados['country_name'],
                labels = {'x':'Countries', 'y': 'Number of Expensive Orders'},
                title = 'Countries with the Most Expensive Dishes',text= dados['price_type'])
    fig.update_yaxes(range=[0, 1200])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width = True)


with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        

        dados = df1.loc[:,['city', 'country_name']]
        dados = dados.groupby('country_name').count().reset_index()
        fig = px.sunburst(dados, path = ['city','country_name'], values = 'city', color = 'country_name',
                  color_continuous_scale= 'RdBu', title = 'Number of Registered Cities per Country')
        st.plotly_chart(fig, use_container_width = True)

    with col2:
        dados = df1.loc[:,['country_name','average_cost_for_two']].groupby('country_name').mean().sort_values(by= 'average_cost_for_two',                                                                               ascending=False).reset_index()
        fig= px.bar(x = dados['country_name'], y = dados['average_cost_for_two'], title = 'Average Cost for two People',
                    labels = {'x':'Countries','y': 'Average Cost'})
        st.plotly_chart(fig, use_container_width= True)
        

    




