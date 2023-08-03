
import streamlit as st
import json
import pandas as pd
import geopandas as gpd
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import os
import leafmap.kepler
#------------------------------------------------------------------
#Maps
Geemap_Map = geemap.Map(basemaps='CartoDB.DarkMatter')
Kepler_Map= leafmap.kepler.Map()
#------------------------------------------------------------------

# st.set_page_config(layout="wide",page_title="This is NAIP IMAGERY page") must be always first for every other st.function to work properly

st.set_page_config(layout="wide",page_title="This is NAIP IMAGERY page")
# Loading Data
st.cache_data() 
# ------------------------------------------------------------------

Pirforos = Image.open("Data\Picture1.png")
Mean_Income_2011 = gpd.read_file("Data\Mean_Income_us_tracts_2011.geojson")
Mean_Income_2019 = gpd.read_file("Data\Mean_Income_us_tracts_2019.geojson")
Land_Use_Percentage = pd.read_csv("Data\Cross Classification.csv")
Urban_Green_2011 = gpd.read_file("Data\FIXUrban_Green_2011.geojson")
Urban_Green_2019 = gpd.read_file("Data\FIXUrban_Green_2019.geojson")

# ------------------------------------------------------------------

st.header("1. Luxury Effect vs Urban Green Spaces")
st.markdown("The variable which represents the Luxury Effect, is Mean Income.\
In this Page will be examined how UGS can be affected by Mean Income.")

st.subheader("1.1 A plot with Mean Income and Green [%]")
col_mean_1,col_mean_2 = st.columns(2)
with col_mean_1:
    fig_mean_1 = px.scatter(data_frame = Mean_Income_2011,  x = "Mean Income 2011 ($)", y = "Green [%]", hover_name="GEOID",title="Plot of Mean Income and Green [%] 2011 ")
    st.plotly_chart(fig_mean_1)
with col_mean_2:
    fig_mean_2 = px.scatter(data_frame = Mean_Income_2019,  x = "Mean Income 2019 ($)", y = "Green [%]", hover_name="GEOID", title="Plot of Mean Income and Green [%] 2019")
    st.plotly_chart(fig_mean_2)
Expander_1_1 = st.expander(label="My observatios and Yours ? (write them in the box bellow)")
with Expander_1_1:
    Text_1_1 = st.text_area(label="My observations ... yours ? :", 
    value=""" 
    As it seems, there is a positive correlation between Mean Income and Urban Green Spaces (Green [%]).\
    Although this positive correlation occurs, something weird is happening with the highest values of Mean Income.\
    The highest values of Mean Income correspond with the lowest values of the Green [%]. Respectively this is happening with the\
    highest values of the Green [%] and the lowest values of the Mean Income.\
    This shows up the necessity of map creation, to see what really is happening at a spatial level.\n
    What's your observations? :
    """,height=200)

st.write(Text_1_1)
config = {
'version': 'v1',
'config': {
'mapState': {
    'latitude': 40.71427,
    'longitude': -74.00597,
    'zoom': 9
    }}
}
with open(file="Data/Kepler_Map_Configuration.json") as Kepler_Datas_Configuration:
    Kepler_Datas_Configuration=json.load(Kepler_Datas_Configuration)

#Adding Datasets to Kepler Maps
st.subheader("1.2 The map with Mean Income tracts and 'Green tracts' ")
Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Mean_Income_2011),layer_name="Mean Income 2011",config=Kepler_Datas_Configuration)
Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Mean_Income_2019),layer_name="Mean Income 2019",config =Kepler_Datas_Configuration )
Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Urban_Green_2011),layer_name="Urban_Grenn_Use_2011",config=Kepler_Datas_Configuration)
Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Urban_Green_2019),layer_name="Urban_Grenn_Use_2019",config=Kepler_Datas_Configuration)

# Show me the Kepler Map
st.cache_resource()
Kepler_Map.to_streamlit()
st.write("Comments:")
st.write("Let's focus initially on the high values of green spaces, as we are examining the relationship between green spaces and median income. The majority of tracts with high values of green spaces are mainly \n\
         located in Staten Island and Queens. In both cases, there are high percentages of median income. On the contrary, in the Bronx and Brooklyn (in terms of low income values), the tracts have the lowest values \n\
         of green spaces and also lower median income values. In these three cases, a strong correlation is observed between green spaces and median income values. What is particularly striking is the very low percentage \n\
         values found in most tracts in Manhattan and the very high median income values. An attentive observer will notice that most tracts in Manhattan are adjacent to Central Park, the largest park in New York City.\n\
         As shown on the Green Spaces map, Central Park has a large percentage of green spaces. A similar phenomenon is also observed in the case of low percentage values of green spaces and very high median income values.")
st.write("What are the final conclusions ? ")
st.markdown("Coclusions:")
st.markdown("* :blue[1st: There is a positive correlation between UGS and Mean Income.]")
st.markdown("* :blue[2nd: There is a 'mandatory' need for more realistic indices than the plot (Mean Income and UGS) for more realistic results.]")
st.markdown("* :blue[3rd: This example shows the necessity of map creation.]")
st.markdown("* :blue[4th: This example reveals the complexity of the spatial characteristics, the real world.]")