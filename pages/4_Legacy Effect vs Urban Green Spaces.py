import streamlit as st
import geopandas as gpd
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
import plotly.graph_objects as go
import leafmap.kepler
#------------------------------------------------------------------
#Maps
Geemap_Map = geemap.Map(basemaps='CartoDB.DarkMatter')
#------------------------------------------------------------------
st.cache_data()
# Loading Data
Urban_Green_2011 = gpd.read_file("Data\FIXUrban_Green_2011.geojson")
Urban_Green_2019 = gpd.read_file("Data\FIXUrban_Green_2019.geojson")
Historic_Districts_2011 = gpd.read_file("Data\Historic Districts_2011.geojson")
Historic_Districts_2019 = gpd.read_file("Data\Historic Districts_2019.geojson")
Historic_Districts_2011 = gpd.GeoDataFrame(Historic_Districts_2011)
Historic_Districts_2019 = gpd.GeoDataFrame(Historic_Districts_2019)

# st.set_page_config(layout="wide",page_title="This is NAIP IMAGERY page") must be always first for every other st.function to work properly

st.set_page_config(layout="wide",page_title="This is NAIP IMAGERY page")


st.header("3. Legacy Effect vs Urban Green Spaces")
st.markdown("The variable which represents the Legacy Effect is Historic Districts.\
In this Page will be examined how UGS can be affected by Historic Districts")
st.subheader("3.1 Map of Historic Districts with Percentage of the Urban Green Spaces")
style = {
    "stroke": False,
    "color": "#ff0000",
    "weight": 1,
    "opacity": 1,
    "fill": True,
    "fillColor": "#ffffff",
    "fillOpacity": 1.0,
    "dashArray": "9",
    "clickable": True
}
Hover_List = ["Green [%]","Grass [%]","ID","Vegetation [%]","category","desdate","area_name"]
Geemap_Map.add_data(data=gpd.GeoDataFrame(Historic_Districts_2011),column = "Green [%]",cmap="Greens",k=7, layer_name=" Historic Districts 2011")
Geemap_Map.add_data(data=gpd.GeoDataFrame(Historic_Districts_2019),column = "Green [%]",cmap="Greens",k=7, layer_name=" Historic Districts 2019")
Geemap_Map.add_basemap(basemap="CartoDB.DarkMatter")
#Map.set_center(lat=40.71427,lon=-74.00597)
Geemap_Map.to_streamlit()


Expander_3_1 = st.expander(label="My Observations and Yours (Write them down, inside the box) ?")
with Expander_3_1:
        Text_3_1 = st.text_area(label="Observations",
        value= """ My obsevartions: Someone can notice that most Historic Districts have more than 20% of the UGS.\
        This is a great index, which shows that someone can find a wide area of UGS in such places. Another thing that pops up is the\
        positive spatial relation between UGS and Historic Districts.\
        Yours? :""", height=200)
st.write(Text_3_1)

# Creation of the plot with Historic Districts and the Percentage of the Urban Green Spaces in them
st.subheader("3.2 A plot with Green Percentages of the two Epochs into Historic Districts ")
fig_3_1 = go.Figure()
fig_3_1.add_trace(go.Scatter(
    x=Historic_Districts_2011["ID"],
    y=Historic_Districts_2011["Green [%]"],
    mode='markers',
    marker=dict(
        size=5,
        color='mediumpurple',
        #symbol='triangle-up'
    ),
    name=' 2011 Green Distribution'            
))

fig_3_1.add_trace(go.Scatter(
    x=Historic_Districts_2019["ID"],
    y=Historic_Districts_2019["Green [%]"],
    mode='markers',
    marker=dict(
        size=5,
        color='mediumblue'
        #symbol='triangle-up'
    ),
    name=' 2019 Green Distribution'
))
fig_3_1.update_layout(
    xaxis_title="ID",
    yaxis_title="Green [%]",
)
#fig_3_1.add_bar(xaxis="grgr")
st.plotly_chart(fig_3_1,use_container_width=True)

Expander_3_2 = st.expander(label="My Observations and yours? (Write them in the box bellow)")
with Expander_3_2:
    Text_3_2 = st.text_area(label="Observations",
    value= """ This chart is plotting the Percentage of the Urban Green Spaces and the Historic Districts.\
    On the X axis, are the IDs and on the Y axis the percentage, in the two epochs respectively.\
    When the two dots (blue and purple) intersect each other, it means that the percentage of the UGS on a specific Historic District didn't change.\
    Therefore, if the blue dot is higher than purple dot, that means the UGS in a Historic Districts saw a rise on the urban green.\
    What's your observations? (Write them down):""", height=200)

st.write(Text_3_2)
st.write("What are the final Conclusions?")
st.markdown("**Conclusions**")
st.markdown("* :blue[1st: There is a positive strength correlation of the UGS and Historic Districts]")
st.markdown("* :blue[2nd: Over the years UGS are getting bigger into Historic Districts]")

