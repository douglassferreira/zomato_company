import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon = '📊')

#image_path = 'Zomato_logo.png'
image = Image.open('Zomato_logo.png')
st.sidebar.image(image, width = 300)
st.sidebar.markdown('## The world of flavors, in the palm of your hand.')
st.sidebar.markdown("""---""")

st.write('# Zomato Company Growth Dashboard')

st.markdown(
    """ The Growth Dashboard was built to track the growth metrics of the restaurants registered on Zomato.
    ## How to use this Growth Dashboard?

    - #### General information:
        - Analysis on the number of reviews, variety of cuisines, countries, cities, and registered restaurants.
        - Map showing the location of restaurants by country.

    - #### Business Information - Countries:
        - The 10 countries with the highest number of registered restaurants.
        - Number of dishes considered expensive per country.
        - Number of registered cities per country.
        - Average cost for two people per country.

    - #### Business Information - Cities:
        - The 10 cities with the highest number of restaurants.
        - Number of restaurants with an average rating above 4 per city.
        - Number of restaurants with an average rating below 2.5 per city.
        - Number of cuisines per city.

    - #### Business Information - Cuisines:
        - Top restaurants by cuisine.
        - The top 10 best cuisines.
        - The top 10 worst cuisines.

    - #### Contact:
        - Linkedin: www.linkedin.com/in/douglas-ferreira-ds
        - GitHub: https://github.com/douglassferreira


"""
)