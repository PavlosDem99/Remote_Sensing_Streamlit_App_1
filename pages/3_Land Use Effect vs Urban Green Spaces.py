
import streamlit as st
import pandas as pd
import geopandas as gpd
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
from PIL import Image
import plotly.express as px
import ee
from geemap import geojson_to_ee, ee_to_geojson, shp_to_ee
from ipyleaflet import GeoJSON
Map = geemap.Map()

#------------------------------------------------------------------
st.cache_data()
# Loading Data
Pirforos = Image.open("Data\Picture1.png")
Land_Use_Percentage = pd.read_csv("Data\Cross Classification.csv")
Urban_Green_2011 = gpd.read_file("Data\FIXUrban_Green_2011.geojson")
Urban_Green_2019 = gpd.read_file("Data\FIXUrban_Green_2019.geojson")


st.set_page_config(layout="wide",page_title="This is NAIP IMAGERY page")

st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to",options = ("Land Use","SVM Algorithm"))

if pages == "Land Use":

    st.header("1. Land Use Effect vs Urban Green Spaces")
    st.markdown("The variable which represents the Land Uses Effect is Land uses.\
    In this Page will be examined how UGS can be affected by Land Uses")

    st.subheader("1.1 Classification of Land Uses and Accuracy Assessment")
    #st.write("In this section, the change detection between 2011 and 2019 will be examined.\")
    # ---------------------------------------------
    # From over here classification method is starting
    
    st.cache_resource()
    class classification:
       
       def __init__(self,start,finish):
            # A feature collection of point geometries for mountain peaks.
            self.start = start
            self.finish = finish

            filterBounds = ee.Geometry.BBox(-74.2559,40.4961,-73.7000,40.9155)

            #print('Images intersecting feature collection', filteredCollection.filterBounds(fc));

            filteredCollection = ee.ImageCollection('USDA/NAIP/DOQQ')\
            .filterBounds(filterBounds)\
            .filterDate(start, finish)\
            .sort('CLOUD_COVER', True)

            # Find the first Aerial photograph for the location of interest 
            image = filteredCollection

            vis = {
                'bands': ['R','G','B'],
                'min': 0,
                'max': 255,
                'gamma':1
            }
            
            Map.centerObject(image, 12)
            Map.addLayer(image, vis, 'ROI ')
        

            # Creation of a mosaic to stick all images together 
            # Mosaic's crs = WGS 84

            image_mosaic= ee.ImageCollection.mosaic(image)

            # saving the bands to variables

            Nir_Band = image_mosaic.select('N')
            Red_Band = image_mosaic.select('R')
            Green_Band = image_mosaic.select('G')
            Blue_Band = image_mosaic.select('B')

            # NDVI Calculation

            ndvi = Nir_Band.subtract(Red_Band).divide(Nir_Band.add(Red_Band)).rename('NDVI')

            vis_params_ndvi_clips = {
                'min': -1,
                'max': 1,
                'palette': ['red', 'white', 'green'],
            }
            # EVI Calculation

            G = 2.5
            C_1 = 6 
            C_2 = 7.5
            L = 1

            vis_params_evi_clip = {
                'min': -1,
                'max': 2,
                'palette': ['green', 'white', 'red'],
            }

            # With rename, you can reanme the name of a band as it will appears in properties  
            evi = (Nir_Band.subtract(Red_Band)).multiply(G).divide(Nir_Band.add(Red_Band.multiply(C_1)).subtract(Blue_Band.multiply(C_2)).add(L)).rename('EVI')

            # PSSR Calculation

            PSSR = Nir_Band.divide(Red_Band).rename('PSSR').rename('PSSR')
            vis_params_pssr_clip = {
                'min': -2,
                'max': 2,
                'palette': ['black', 'grey', 'white'],
            }

            # GNDVI Calculation

            gndvi = Nir_Band.subtract(Green_Band).divide(Nir_Band.add(Green_Band)).rename('GNDVI')

            vis_params_gndvi_clips = {
                'min': -1,
                'max': 1,
                'palette': ['red', 'white', 'green'],
            }

            #  NDWI Calculation

            ndwi= Green_Band.subtract(Nir_Band).divide(Nir_Band.add(Green_Band)).rename('NDWI')

            vis_params_ndwi_clips = {
                'min': -1,
                'max': 1,
                'palette': ['green', 'white', 'blue'],
            }

            Map.addLayer(evi, vis_params_evi_clip, name ='EVI',shown=False)
            Map.addLayer(PSSR, vis_params_pssr_clip, name = 'PSSR',shown=False)
            Map.addLayer(gndvi, vis_params_gndvi_clips,name='GNVDI',shown=False)
            Map.addLayer(ndwi, vis_params_ndwi_clips,name='NDWI',shown=False)
            
            #Creaation of a new image with all the bands
            New_Bands = ee.Image([ndvi,evi,PSSR,gndvi,ndwi])
            image_mosaic = image_mosaic.addBands(New_Bands)
            Map.addLayer(image_mosaic,name="image_mosaic",shown=False)
            

            # We must clip the image (image_mosaic) to make the classification this is happening because Google Earth Engine is working with this way

            Clip_Geometry = ee.Geometry.BBox(-74.3086, 40.5676,-73.7013, 40.9302)

            clip_image_mosaic = ee.Image.clip(image_mosaic,Clip_Geometry)
            Map.addLayer(clip_image_mosaic,name="Clip_Image")
        
            # Training Data 

            training_sample = geemap.geojson_to_ee("Data\Training_Points_4800_with_Shadows.geojson")
            bands = ["R","G","B","N","NDVI","EVI","PSSR","GNDVI","NDWI"]
            #bands_select = clip_image_mosaic.select(bands)
            label = 'landcover'

            # Overlay the points on the imagery to get training.
            training =clip_image_mosaic.select(bands).sampleRegions(
                **{'collection': training_sample, 'properties': [label], "scale":1})

            # Train the classification algorithm

            self.trained = ee.Classifier.libsvm(decisionProcedure = "Margin",kernelType = 'RBF').train(training,label,bands)
            result = clip_image_mosaic.select(bands).classify(self.trained)

            # Validation Data 2019 - 2020 *** Validation Data between 2019 - 2020 & 2011 - 2013 must be always be different 
            validation_1 = geemap.geojson_to_ee("Data/Training_Points_4800_with_Shadows_2012.geojson")
            validated_1 =clip_image_mosaic.select(bands).sampleRegions(
            **{'collection': validation_1 , 'properties': [label], "scale":1})
            sample_1 = validated_1.randomColumn()
            split_1 = 0.7 
            validation_test_1 = sample_1.filter(ee.Filter.gte('random', split_1))
            final_validated_1 = validation_test_1.classify(self.trained)
            self.test_accuracy_test_1 = final_validated_1.errorMatrix('landcover', 'classification')

            # Validation Data 2011 - 2013 *** Validation Data between 2019 - 2020 & 2011 - 2013 must be always be different 
            validation_2 = geemap.geojson_to_ee("Data/Training_Points_4800_with_Shadows_2012.geojson")
            validated_2 =clip_image_mosaic.select(bands).sampleRegions(
            **{'collection': validation_2 , 'properties': [label], "scale":1})
            sample_2 = validated_1.randomColumn()
            split_2 = 0.7 
            validation_test_2 = sample_2.filter(ee.Filter.gte('random', split_2))
            final_validated_2 = validation_test_2.classify(self.trained)
            self.test_accuracy_test_2 = final_validated_2.errorMatrix('landcover', 'classification')
            # Visualization of the classification imagery
            vis_class = {
                'min': 11,
                'max': 17,
                'palette': ["#008000","#5cff25","#FC46AA","#000000","#FFA500","blue","white"]
                }
            Map.addLayer(result,vis_class,name=f"Classified {start} - {finish}")
            legend_dict = {
                "vegetation": "#008000",
                "Grass": "#5cff25",
                "buildings": "#FC46AA",
                "roads": "#000000",
                "Bare Land": "#FFA500",
                "Water": "blue",
                "Shadows": "white"
                    }
            Map.add_legend(title="Land Cover Classification",legend_dict=legend_dict)

    # Confusion Matrix
   
                      
    st.cache_resource()
    def classifications_calling():
        classification_1 = classification(start = '2019-08-09', finish='2020-09-07')
        classification_2 = classification(start = '2011-01-01', finish='2013-12-31')  
        st.write("For the change detection, a classification has been made for the two images of the NAIP Imagery program. One for 2019 and one for 2011, respectively.\
                So, the results that follow, refer to these classifications.")
        
        st.write("Classification accuracy for both classidied images")

        st.cache_resource()
        def accuracy_result_1(classification):
            selectBox = st.selectbox(label="Select the kind of accuracy",options=("Overall Accuracy","Kappa Accuracy","Producer Accuracy","User/Consumer Accuracy"),key="1")
            if selectBox=="Overall Accuracy":
                st.write("The overall accuracy is : ", classification.trained.confusionMatrix().accuracy().getInfo())
            elif selectBox=="Kappa Accuracy":
                st.write("The kappa accuracy is : ", classification.trained.confusionMatrix().kappa().getInfo())
            elif selectBox=="Producer Accuracy":
                st.write("The producer accuracy is : ", classification.trained.confusionMatrix().producersAccuracy().getInfo())
            elif selectBox=="User/Consumer Accuracy":
                st.write("The user/consumer accuracy is : ", classification.trained.confusionMatrix().consumersAccuracy().getInfo())
            return
        
        st.cache_resource()
        def accuracy_result_2(classification):
            selectBox = st.selectbox(label="Select the kind of accuracy",options=("Overall Accuracy","Kappa Accuracy","Producer Accuracy","User/Consumer Accuracy"),key="2")
            if selectBox=="Overall Accuracy":
                st.write("The overall accuracy is : ", classification.trained.confusionMatrix().accuracy().getInfo())
            elif selectBox=="Kappa Accuracy":
                st.write("The kappa accuracy is : ", classification.trained.confusionMatrix().kappa().getInfo())
            elif selectBox=="Producer Accuracy":
                st.write("The producer accuracy is : ", classification.trained.confusionMatrix().producersAccuracy().getInfo())
            elif selectBox=="User/Consumer Accuracy":
                st.write("The user/consumer accuracy is : ", classification.trained.confusionMatrix().consumersAccuracy().getInfo())
            return
        
        st.cache_resource()
        def accuracy_result_VALIDATION_1(classification):
          
            #test_accuracy = classification_1.validated.errorMatrix('landcover', 'classification')
            selectBox = st.selectbox(label="Select the kind of accuracy",options=("Overall Accuracy","Kappa Accuracy","Producer Accuracy","User/Consumer Accuracy"),key="3")
            if selectBox=="Overall Accuracy":
                st.write("The overall accuracy is : ", classification.test_accuracy_test_1.accuracy().getInfo())
            elif selectBox=="Kappa Accuracy":
                st.write("The kappa accuracy is : ", classification.test_accuracy_test_1.kappa().getInfo())
            elif selectBox=="Producer Accuracy":
                st.write("The producer accuracy is : ", classification.test_accuracy_test_1.producersAccuracy().getInfo())
            elif selectBox=="User/Consumer Accuracy":
                st.write("The user/consumer accuracy is : ", classification.test_accuracy_test_1.consumersAccuracy().getInfo())
            return
        
        st.cache_resource()
        def accuracy_result_VALIDATION_2(classification):
          
            #test_accuracy = classification_1.validated.errorMatrix('landcover', 'classification')
            selectBox = st.selectbox(label="Select the kind of accuracy",options=("Overall Accuracy","Kappa Accuracy","Producer Accuracy","User/Consumer Accuracy"),key="4")
            if selectBox=="Overall Accuracy":
                st.write("The overall accuracy is : ", classification.test_accuracy_test_2.accuracy().getInfo())
            elif selectBox=="Kappa Accuracy":
                st.write("The kappa accuracy is : ", classification.test_accuracy_test_2.kappa().getInfo())
            elif selectBox=="Producer Accuracy":
                st.write("The producer accuracy is : ", classification.test_accuracy_test_2.producersAccuracy().getInfo())
            elif selectBox=="User/Consumer Accuracy":
                st.write("The user/consumer accuracy is : ", classification.test_accuracy_test_2.consumersAccuracy().getInfo())
            return

        col1,col2 = st.columns(2)
        with col1:

            st.markdown("### Classification Accuracy Results for the year 2019-2020")
            st.write("Training Data")
            accuracy_result_1(classification=classification_1)
            st.write("Validation Data")
            accuracy_result_VALIDATION_1(classification=classification_1)

        with col2:
            st.markdown("### Classification Accuracy Results for the year 2011-2013")
            st.write("Training Data")
            accuracy_result_2(classification=classification_2)
            st.write("Validation Data")
            accuracy_result_VALIDATION_2(classification=classification_2)
        
        Map.to_streamlit()
        return
    with st.spinner('Please wait while is loading... 😎'):
        classifications_calling()
   
   # ---------------------- Change Detection Part 2 ------------------------------

    st.subheader("1.2. Change Detection")
    tab_2_1,tab_2_2,tab_2_3 = st.tabs(["From Trees to Buildings","From Buildings to Trees","From Buildings to Grass"])
    with tab_2_1:
        Trees_to_Buildings = Image.open("Data\Trees_to_Buildings.JPG")
        st.markdown(":green[Yellow circles show the correct change detections] and :red[Red Circles the false change detections]")
        st.image(Trees_to_Buildings)
        st.markdown("Observations: The main change detection in this picture, is the appearance of the big building in 2019")

    with tab_2_2:
        Buildings_to_Trees = Image.open("Data\Buildings_to_trees.JPG")
        st.image(Buildings_to_Trees)
        st.markdown("Observations: In this case, most detections which appear in blue are false. This may be due to the Image 2011 which has not been preprocessed. In respect to this, this case shows the necessity of the preprocess method to be made for an image especially for an image that will be used for a change detection. Also, another thing that pops up is the necessity of the two images to have the same resolutions.")

    with tab_2_3:
        Buildings_to_Grass = Image.open("Data\Buildings_to_Grass.JPG")
        st.image(Buildings_to_Grass)
        st.markdown("Observations: In this case this change detection shows the change between Buildings and Grass.")

    st.empty()
    st.markdown("Principles of making a map of Change Detection:\n\
           1. The change detection is based on the difference of the two epochs.\n\
           2.Similar spatial resolution between the two epochs.\n\
           3. Same radiometric resolution (also the images must be preprocessed radiometric corrected from envirnomental effects) between the two epochs and same .\n\
            Be carefull about the NAIP Imagery Dataset.\n The things that you have to pay attention, are the resolution of this Dataset.\
            The radiometric and spatial resolution are not perfect for the Change Detection. This is due to the 2011 dataset, which has not been preprocessed.\
            Also both of th 'Images' are not true orthorectified.")

    st.success("But for the purposes of this project, the 2011 dataset has been theorized to be suitable for change detection.")

    st.subheader("1.3 Quantification of Land Uses of the two epochs")
    st.dataframe(data=Land_Use_Percentage)
    #st.text("\n What's do you observe ?")
    Expander_2_1 = st.expander("My Observation and yours ? (Write them in the box bellow)")
    with Expander_2_1:
        Text_2_2_1 = st.text_area(label="My observations ... yours ? : ",\
        value=" The percentage of the change that UGS had was approximately +4%. The positive symbol means the positive percentage change in the overall percentage of all tracts.\
            The biggest change is located on the Artifacts, with a percentage of 7.4%. This may be due to the large percentage change in the shadow category (~7.3% Epoch 2019). \
            A pleasant phenomenon that appears is that there is a huge percentage of Green in New York in both periods.")
    st.write(Text_2_2_1)
    dimensions = ['Green [%]',"Artifacts [%]"]
    st.markdown("##### 1.3.1 Plots: Artifacts vs Urban Green Spaces and Make your own Charts (Make your charts)")
    fig_1 = px.scatter(data_frame = pd.DataFrame(Urban_Green_2011),  x = "Artifacts [%]", y = "Green [%]",hover_name=Urban_Green_2011.index, title = "Artifacts vs Urban Green 2011")
    fig_2 = px.scatter(data_frame = pd.DataFrame(Urban_Green_2019),  x = "Artifacts [%]", y = "Green [%]",hover_name=Urban_Green_2019.index, title = "Artifacts vs Urban Green 2019")
    df_fig_1_1 = pd.DataFrame(Urban_Green_2011)
    df_fig_1_2 = pd.DataFrame(Urban_Green_2019)
            
    tab_1_1,tab_1_2 = st.tabs(tabs=["Artifacts vs UGS", "Make your own charts"])

    with tab_1_1:
        col_1,col_2 = st.columns(2)

        with col_1:
            #st.text("Epoch 2011")
            st.plotly_chart(fig_1, theme = "streamlit",use_container_width=True)
        
        with col_2:
            #st.text("Epoxh 2019")
            st.plotly_chart(fig_2, theme = "streamlit",use_container_width=True)
    st.write("Observations about the above plots. There is an obvious negative correlation between Artifacts and UGS.Also, the majority of the tracts have a higher percentage of Artifacts [%] than Green [%].")
    with tab_1_2:
        
        #fig_2 = px.scatter(data_frame = pd.DataFrame(Urban_Green_2019),  x = "Artifacts [%]", y = "Green [%]",hover_name=Urban_Green_2019.index, title = "Artifacts vs Urban Green 2019")
        col_1,col_2 = st.columns(2)


        with col_1:
            #st.text("Epoch 2011")
            Select_box_x = st.selectbox(label = "Choose x column ",options=list(Urban_Green_2011.columns),index=9)
            Select_box_y = st.selectbox(label = "Choose y column ",options=list(Urban_Green_2011.columns),index=9)
            fig_1 = px.scatter(data_frame = df_fig_1_1,  x = Select_box_x, y = Select_box_y, hover_name=Urban_Green_2011.index, title = f"{Select_box_x} vs {Select_box_y} 2011")
            st.plotly_chart(fig_1, theme = "streamlit",use_container_width=True)
        
        with col_2:
            #st.text("Epoxh 2019")
            Select_box_x = st.selectbox(label = "Choose x column ",options=list(Urban_Green_2019.columns),index=9)
            Select_box_y = st.selectbox(label = "Choose y column ",options=list(Urban_Green_2019.columns),index=9)
            fig_2 = px.scatter(data_frame = df_fig_1_2,  x = Select_box_x, y = Select_box_y, hover_name=Urban_Green_2019.index, title = f"{Select_box_x} vs {Select_box_y} 2019")
            st.plotly_chart(fig_2, theme = "streamlit",use_container_width=True)

    st.markdown("##### 1.3.2 Quantification of **change detection of land uses** for the epochs 2019 & 2011")
    st.dataframe(data=pd.DataFrame(pd.read_csv('Data\Cross_Classification_Change_Detection.csv')),height=500)
    st.text("CrossClassCode column's number corresponds to the numbers of the Change Detection Image.\nBut as it mentioned before the change detection image cannot shows up in this application")
    st.write("What are the final Coclusions?")
    st.markdown("**Coclusions:**")
    st.markdown("* :blue[1st: For a change detection, it is mandatory, the two image will have the same resolutions and be preprocessed]")
    st.markdown("* :blue[2nd: UGS are depended on a huge level from Land Uses, specifically there is a negative dependance with the Artifacts (Buildings and Roads)\
                and there is a positive dependance with bare land.]")
    st.markdown("* :blue[3rd: New York city has a big percentage of Green in US tracts in both periods]")

# -------------------------------------------------------------------------------------------------
# SVM Algorithm page is following 

elif pages == "SVM Algorithm":
    st.title("1. SVM Algorithm")
    st.subheader("1.1 What is SVM ?")
    st.write("Support Vector Machine (SVM) is a supervised machine learning algorithm that can be used for both classification and regression analysis. The objective of the SVM\
             algorithm is to find a hyperplane in an N-dimensional space that distinctly classifies the data points. SVMs are effective in high dimensional spaces (hence, it choosed for the image classification) and can\
             efficiently perform non-linear classification using what is called the kernel trick, implicitly mapping their inputs into high-dimensional feature spaces.\
             Several machine-learning algorithms have been proposed for remote sensing image classification during the past two decades. Among these machine learning algorithms, Random Forest (RF) and Support Vector Machines (SVM)\
             have drawn attention to image classification in several remote sensing applications. SVMs are particularly appealing in the remote sensing field due to their ability to successfully handle small training data sets,\
             often producing higher classification accuracy than traditional methods. ")
    st.write("Bibliography: https://link.springer.com/chapter/10.1007/978-3-642-30062-2_8#Sec30 and https://www.sciencedirect.com/science/article/abs/pii/S0924271610001140 ")
   