
import streamlit as st
import ee
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
import os
import leafmap.kepler
#------------------------------------------------------------------
#Maps
Geemap_Map = geemap.Map(basemaps='CartoDB.DarkMatter')
Kepler_Map= leafmap.kepler.Map()
#------------------------------------------------------------------

# st_page_config must be always first to work properly !!!

st.set_page_config(layout="wide",page_title="This is NAIP IMAGERY page")

#------------------------------------------------------------------
os.environ['LOCALTILESERVER_CLIENT_PREFIX'] = 'proxy/{port}'

#-------------------------------------------------------------------
# Function for NA
def main():
    st.sidebar.title("Datasets")
    pages = st.sidebar.radio("Select a page: ",("Land Use Dataset: NAIP Imagery","Other Datasets"))

    if pages == "Land Use Dataset: NAIP Imagery":
         
        @st.cache_resource()
        def image_for_classification(start_date,finish_date):
                # - Polar Coordinates
                start = ee.Date(start_date)
                finish = ee.Date(finish_date)

                # A feature collection of point geometries for mountain peaks.

                filterBounds = ee.Geometry.BBox(-74.2559,40.4961,-73.7000,40.9155)

                #print('Images intersecting feature collection', filteredCollection.filterBounds(fc));

                filteredCollection = ee.ImageCollection('USDA/NAIP/DOQQ')\
                    .filterBounds(filterBounds)\
                    .filterDate(start, finish)\
                    .sort('CLOUD_COVER', True)


                image = filteredCollection.mosaic().clip(filterBounds)
                return image

        st.cache_resource()
        def geemap_appearrance():
            vis = {
                'bands': ['R','G','B'],
                'min': 0,
                'max': 255,
                'gamma':1
            }

            start_date_1 = '2019-08-09'
            finish_date_1 = '2020-09-07'
            start_date_2 = '2011-01-01'
            finish_date_2 = '2013-12-31'

            Geemap_Map.addLayer(image_for_classification(start_date = start_date_1,finish_date = finish_date_1),vis,f'ROI {start_date_1}-{finish_date_1}')
            Geemap_Map.addLayer(image_for_classification(start_date = start_date_2,finish_date = finish_date_2),vis,f'ROI {start_date_2}-{finish_date_2}')
            Geemap_Map.zoom_to_bounds(bounds=[-74.2559,40.4961,-73.7000,40.9155])
            Geemap_Map.to_streamlit()
            st.write(f"1st: Image -> Start date: {start_date_1} and Finsh Date: {finish_date_1}")
            st.write(f"2nd: Image -> Start date: {start_date_2} and Finsh Date: {finish_date_2}")
            return
        st.header("NAIP Imagery Dataset")
        st.write("The National Agriculture Imagery Program (NAIP) is a program that acquires aerial imagery during the agricultural growing seasons in the United States. \n\
                  The primary goal of the NAIP program is to make digital ortho photography available to governmental agencies and the public within a year of acquisition. \n\
                  The program collects (1-meter imagery for the entire conterminous United States. The imagery is acquired during peak growing season, 'leaf on' and delivered to USDA County Service Centers\n\
                  to maintain the common land unit (CLU) boundaries and assist with farm programs.")
        col1, col2 = st.columns(2)
        with col1:
             
            st.subheader("2019-2020")
            st.write("NAIP Imagery 2019 - 2020 resolutions are the following:")
            st.write("Spatial Resolution: 0.6m")
            st.write("Radiometric Resolution: 8-bit")
            st.write("Spectral Resolution: Red, Green, Blue, Near Infrared")
            st.write("True Orthorectified: No")
        with col2:
            st.subheader("2011-2013")
            st.write("NAIP Imagery 2011 - 2013 resolutions are the following:")
            st.write("Spatial Resolution: 1m")
            st.write("Radiometric Resolution: 8-bit")
            st.write("Spectral Resolution: Red, Green, Blue, Near Infrared")
            st.write("True Orthorectified: No")
        geemap_appearrance()
        
        # ---------------------------------------------------------------
        # Resolution definitions

        st.subheader("Resolution Definitions")

        selectbox = st.selectbox(label="Choose Resolution Definition (Spatial, Radiometric, Spectral or True Orthorectifies)",options=["Spatial Resolution","Radiometric Resolution","Spectral Resolution", "True Orthorectified"])
    
        if selectbox == "Spatial Resolution":
            st.write("Satellite/Aerial imagery spatial resolution refers to the level of detail captured by a satellite/aerial \n\
                      sensor. It is defined by the size of each pixel within a digital image and the area on Earths surface \n\
                      by that pixel. The most commonly used metric for classifying optical satellite imagery \n\
                      spatial resolution refers to the distance represented by a pixel in an image. For example,\n\
                      NASAs Landsat collects imagery at 15-meter resolution—so every pixel in one of its images represents a 15 m \n\
                      by 15 m square on the ground.")
            
        if selectbox == "Spectral Resolution":
            st.write("Spectral resolution is related to the granularity of the breadth of coverage of the electromagnetic spectrum captured by the satellite/aerial sensors.\n\
                  A finer spectral resolution can discriminate between narrower bands of wavelength, differentiating, for example, between red, green,\n\
                  and blue bands and allowing for colored image.")
            
        if selectbox == "Radiometric Resolution":    
            st.write("Radiometric resolution relates to how much information is perceived by a satellite's sensor.\n\
                  It is the amount of information in each pixel, that is, the number of bits representing the energy recorded. Each bit records an exponent of power 2.\n\
                  For example, an 8 bit resolution is 2^8, which indicates that the sensor has 256 potential digital values (0-255) to store information.")
        
        if selectbox == "True Orthorectified":
            st.write("True orthorectified imagery is a type of orthorectified imagery that has been processed to remove terrain displacement and camera tilt.")

        
        
# ------------------------------------------------------------------
# Other Datasets Page is following

    elif pages == "Other Datasets":
        st.header("Other Datasets")
        st.markdown("In this page you can find other datasets that are used in this project. The datasets are the following:")
        #------------------------------------------------------------------
        # container for the dataset of Mean Income

        st.subheader("1. Dataset for Mean Income (2011 & 2019)")
        st.write("The Mean Income is the mean income of the US households per tract. The dataset is from the US Census Bureau. A tract is the smallest area that is used for the US Census.")
        st.write("US Census Bureau: https://www.census.gov/programs-surveys/acs \
                  Population Estimates Program that produces and disseminates the official estimates of the population for the nation, states, counties, cities, and towns and estimates of housing units for states and counties.\n\
                 Data are based on a sample and are subject to sampling variability. The degree of uncertainty for an estimate arising from sampling variability is represented through the use of a margin of error.\n\
                 The value shown here is the 90 percent margin of error. The margin of error can be interpreted roughly as providing a 90 percent probability that the interval defined by the estimate minus the margin of error \n\
                 and the estimate plus the margin of error (the lower and upper confidence bounds) contains the true value. \n\
                 In addition to sampling variability, the ACS estimates are subject to nonsampling error (for a discussion of nonsampling variability, see ACS Technical Documentation). \n\
                 The effect of nonsampling error is not represented in these tables.") 

        #------------------------------------------------------------------
        # container for the dataset of Historic Districts
        st.subheader("2. Dataset for Historic Districts")
        st.write("The Historic Districts Dataset is a dataset that contains the Historic Districts of the US states.This dataset contains boundaries and associated attribute information for all designated historic districts\n\
                 or areas under consideration for historic district designation (i.e. calendared) by the New York City Landmarks Preservation Commission (LPC), including items that may have been denied designation or overturned.\n\
                  Please note that some areas may have multiple records in the database if different actions were taken over time. \n\
                  Please pay close attention to the 'CURRENT' and 'LAST_ACTION_ON_BOUNDARY' fields to determine the status of a particular area. \n\
                  The geographic locations of the polygons in this dataset are derived primarily from the Department of City Planning's PLUTO dataset, \n\
                  and therefore discrepancies may arise where the LPC dataset has not been updated with information from the most recent PLUTO releases. Please pay close attention to the field descriptions present \n\
                  in the file's metadata to understand how to use this dataset. And please contact LPC if there are questions or concerns")
        
        st.write("This dataset was taken by NYC Open Data Program\n\
                 NYC Open Data Program: https://opendata.cityofnewyork.us/ is managed by the Open Data Team at the NYC Office of Technology and Innovation (OTI). \n\
                 The team works with City agencies to identify and make data available, coordinate platform operations and improvements, and promote the use of Open Data both within government and throughout NYC. \n\
                 Each City agency also has an Open Data Coordinator, who serves as the main point of contact for the Open Data team and the public, and works to identify, document, structure, and manage the agency’s public datasets")


    return

if __name__ == '__main__':
    main()
    




































