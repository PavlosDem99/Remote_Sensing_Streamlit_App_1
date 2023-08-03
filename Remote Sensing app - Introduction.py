#%%
import streamlit as st
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
import ee
from PIL import Image
import os
import leafmap.kepler
#------------------------------------------------------------------
#Maps
Geemap_Map = geemap.Map(basemaps='CartoDB.DarkMatter')
Kepler_Map= leafmap.kepler.Map()
#Loading the data
#------------------------------------------------------------------
Map_Background_NY= Image.open('Maps/New York SRTM.png')
Pirforos = Image.open('Data\Picture1.png')

#------------------------------------------------------------------
os.environ['LOCALTILESERVER_CLIENT_PREFIX'] = 'proxy/{port}'
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]
#------------------------------------------------------------------
# Main Function

def main():
    # Create a sidebar with a selection widget
    
    st.set_page_config(layout="wide")
   
    # Use an if statement to display different content on different pages:

    backgroundColor="#FFFFFH"
    col1,col2 = st.columns([1,9])
    with col2:
        st.title("National Tecnhical University of Athens\t - School of Rural, Surveying and Geoinformatics Engineer")
    
    with col1:
        st.image(Pirforos,width=90, use_column_width=200)
    st.header("Title: How Urban Green Spaces can be affected by Socioeconomic Factors and Land Uses ")
    
    
    st.markdown("""##### **:blue[A brief introduction about this Project]** \n
    Green spaces are an integral part of urban fabric, and their relationship should be characterized as inseparable. Green spaces refer to areas where vegetation is present, including parks and squares, 
    generally providing spaces for residents to freely walk and connect with nature. According to Angelo Siolas (2015), green spaces, also known as "Urban Green Spaces", 
    are the points where the city meets nature. Green spaces should be an integral part of every neighborhood, and their distribution should be uniform, with sizes sufficient to meet the needs of all residents.

    Numerous studies have shown that green spaces are influenced by various socio-economic factors. Hai-Li Zhang et al. (2021) studied how green spaces depend on property values, 
    the history of the area, land uses, and other factors in two different periods. Mendel Giezen (2018) used satellite images to detect a reduction in green spaces over time due to increased construction.
    Therefore,the purpose of this study is to identify the correlation between certain socio-economic factors and green spaces in two time periods at the level of USA Tract.

    It is important to note that in this study, green spaces refer specifically to areas with vegetation. Green spaces in cities offer various benefits that make the relationship between nature and the urban environment 
    inseparable. They can act as natural carbon sinks, absorbing carbon dioxide emissions from vehicles. They also reduce the likelihood of flooding by absorbing atmospheric precipitation and help control soil erosion. 
    Additionally, green spaces function as noise reduction tools in cities, creating a more pleasant and sustainable living environment for residents. Furthermore, green spaces can be considered as temperature regulators, 
    mitigating the heat island effect predominantly found in urban areas. Lastly, they undoubtedly enhance the aesthetics of the city, providing a more visually appealing environment.
    
    The aim of this project is, how green spaces are affected by socio-economic factors and land uses, with a focus on the case of New York City. For better and more accuracy results, two epochs have been investigated, 2011 and 2019. 
    The application includes a study implementation section with subsections on Luxury Effect, Land Use Effect, and Legacy Effect, and a bibliography. 
    The study implementation section includes graphs, charts, and maps to support the analysis. The application concludes that there is a strong correlation between green spaces and median income, 
    and suggests further analysis with additional indicators and dynamic maps for more representative results.
    The project is made of four Pages. The 1st is about the Datasets that being used in this project. The 2nd examines how Luxury Effect can affect Urban Green Spaces (UGS) and 
    the 3rd and 4th Pages examine how Land Use Effect and Legacy Effect can be affect UGS, respectivly.  
    The Socioeconomic Factors which will be examined are : \n
    - Mean Income (Luxury Effect) \n 
    - Historic Districts (Legacy Effect) \n
    and also - Land Use (Lan Use Effect).\n\
    """)
    st.write(" \n ")
    col1, col2, col3 = st.columns([0.25,0.5, 0.25])
    with col2:
        st.image(Map_Background_NY,output_format='PNG',width=1080,caption="Figure 1: New York City Map",clamp=True)

    st.markdown("##### **:blue[Bibliography]** \n\
    Hai-Li Zhang a, J. P.-L.-F. (2021). Wealth and land use drive the distribution of urban green space in the tropical coastal city of Haikou, China. ELSEVIER. \n\
    Mendel Giezen, S. B. (2018). Using Remote Sensing to Analyse Net Land-Use Change from Conflicting Sustainability Policies:. ISPRS  \n\
    Άγγελος Σιόλας, Α. Β. (2015). Μέθοδοι, Εφαρμογές και Εργαλεία Πολεοδομικό Μετασχηματισμού: Εργαλεία και Τεχνικές. ΑΘΗΝΑ: Kallipos  \n\
    Richards, J. A. (2012). Remote Sensing Digital Image Analysis - An introduction. Canbera, Australia: Springe\n\
    Sofia F. Francoa, J. L. (2018). Measurement and valuation of urban greenness: Remote sensing and hedonic applications to Lisbon, Portugal. ELSEVIER\n\
    Wei Lia, J.-D. M. (2014). A comparison of the economic benefits of urban green spaces estimated with NDVI and with high-resolution land cover data. ELSEVIER\n\
    Wu, Q. (2020). geemap: A Python package for interactive mapping with. Geograpgy. The Journal of Open Source Software.\n\
    Yingdan Mei, X. Z. (2018). apitalization of Urban Green Vegetation in a Housing Market with Poor Environmental Quality:. Journal of Urban Planning and Development.\n\
    Zhonglin Ji, Y. P. (2022). Prediction of Corn Yield in the USA Corn Belt Using Satellite Data and Machine Learning: From an Evapotranspiration Perspective . Basel, Switzerland.: MDPI.\n\
    Γεωργούλη, Κ. (2015). Τεχνητή Νοημοσύνη - Μια Εισαγωγική Προσέγγιση. Αθήνα: Kallipos.\n\
    Δημήτρης, Α. (1998). Ψηφιακή Τηλεπισκόπηση. Αθήνα.\n\
    Ιωάννης, Ψ. (2021). Χαρτογράφηση καμένων εκτάσεων απο διαχρονικά δορυφορικά δεδομένα Sentinel-2 στο περιβάλλον του Google Earth Engine. Αθήνα: ΕΜΠ.\n\
    Κωνσταντίνος Γ. Περάκης, Ι. Ν. (2015). Η Τηλεπισκόπηση σε 13 ενότητες. Kallipos.\n\
    Σπύρος Φουντάς, Θ. Γ. (2015). Γεωργία Ακριβείας. Kallipos.\n\
")
    st.markdown("#### Anknowledgments \n\
                This project was developed as part of the course 'Remote Sensing Applications' of the Department of Rural, Surveying Engineering and Geoinformatics Enginnereing of the National Technical University of Athens\n\
                under the supervision of Professor Konstantinos Karantzalos. Also a huge thanks to my advisor-friend Alekos Falaggas for his valuable advices")   
    return

# code that should only be executed when this module is run directly

if __name__ == '__main__':
   
    main()
    
# %%
