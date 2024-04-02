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


st.set_page_config(page_title = 'Cuisines', page_icon = '🍦', layout = 'wide')
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


########### Layout #############

with st.container():
  st.title('Business Information - Cuisines')
  st.markdown('## Top Restaurants by Cuisine Types')

  dados = df1.loc[:, ['restaurant_name', 'city', 'country_name', 'cuisines', 'aggregate_rating']]
  dados1 = dados.groupby(['cuisines']).max().sort_values(by='aggregate_rating', ascending=False).reset_index()
  dados1.columns = ['Cuisines', 'Restaurant Name', 'City', 'Country', 'Aggregate Rating']

  st.dataframe(dados1)



with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('### Top 10 Best Cuisine Types')
        dados = df1.loc[:,['cuisines','aggregate_rating','country_name']].groupby(['cuisines','country_name']).max().sort_values(by='aggregate_rating',
                                                                                          ascending=False).reset_index().head(10)
        fig= px.bar(x = dados['cuisines'], y= dados['aggregate_rating'], color = dados['country_name'],
                    labels= {'x':'Cuisines','y':'Aggregate Rating','color':'Countries'})
        fig.update_traces(text = dados['aggregate_rating'], textposition = 'outside')
        fig.update_yaxes(range=[0,5.3])
        st.plotly_chart(fig, use_container_width= True)

    with col2:
        st.markdown('### Top 10 Worst Cuisine Types')
        dados = df1.loc[:,['cuisines','aggregate_rating','country_name']].groupby(['cuisines','country_name']).min().sort_values(by='aggregate_rating',
                                                                                          ascending=True).reset_index().head(10)
        fig= px.bar(x = dados['cuisines'], y= dados['aggregate_rating'], color = dados['country_name'],
                    labels = {'x':'Cuisines','y':'Aggregate Rating', 'color':'Countries'})
        fig.update_traces(text = dados['aggregate_rating'], textposition = 'outside')
        fig.update_yaxes(range=[0,5.3])
        st.plotly_chart(fig, use_container_width= True)   










