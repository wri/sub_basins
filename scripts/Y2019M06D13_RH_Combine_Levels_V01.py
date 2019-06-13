
# coding: utf-8

# In[1]:

""" Combine level 7 for coastal and level 6 inland.
-------------------------------------------------------------------------------

TODO: 

- add area per polygon
- remove small polygons


Author: Rutger Hofste
Date: 20190613
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

SCRIPT_NAME = "Y2019M06D13_RH_Combine_Levels_V01"
OUTPUT_VERSION  = 1

S3_INPUT_PATH= "s3://wri-projects/Aqueduct30/processData/Y2019M06D13_RH_Simplify_Geometries_V01"

ec2_input_path = "/volumes/data/{}/input_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)
ec2_output_path = "/volumes/data/{}/output_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)

s3_output_path = "s3://wri-projects/Aqueduct30/processData/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)


# In[2]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version
get_ipython().magic('matplotlib inline')


# In[3]:

get_ipython().system('rm -r {ec2_input_path} ')
get_ipython().system('rm -r {ec2_output_path} ')
get_ipython().system('mkdir -p {ec2_input_path} ')
get_ipython().system('mkdir -p {ec2_output_path} ')


# In[4]:

get_ipython().system('aws s3 cp {S3_INPUT_PATH} {ec2_input_path} --recursive')


# In[5]:

import pandas as pd
import geopandas as gpd


# In[6]:

input_path_level6 = "{}/hybas_merged_standard_level6_V01_simplified/hybas_merged_standard_level6_V01.shp".format(ec2_input_path)
input_path_level7 = "{}/hybas_merged_standard_level7_V01_simplified/hybas_merged_standard_level7_V01.shp".format(ec2_input_path)


# In[7]:

gdf_level6_og = gpd.read_file(filename=input_path_level6)
gdf_level7_og = gpd.read_file(filename=input_path_level7)


# In[8]:

gdf_level6_og.shape


# In[9]:

gdf_level7_og.shape


# In[10]:

gdf_level7 = gdf_level7_og.loc[gdf_level7_og["geometry"].notnull()]
gdf_level6 = gdf_level6_og.loc[gdf_level6_og["geometry"].notnull()]


# In[11]:

# Select all inland level 6 basins
gdf_level6_inland = gdf_level6.loc[gdf_level6["COAST"] == 0]
gdf_level6_coast = gdf_level6.loc[gdf_level6["COAST"] == 1]


# In[12]:

def find_corresponding_basins(pfaf_id_level6,gdf_level7):
    """
    Using a pfaf_id from level 6, find all hydrobasins in level 7 that 
    make up the hydrobasin level 6 polygon.
    
    """
    pfaf_id_level7_min = pfaf_id_level6*10
    pfaf_id_level7_max = pfaf_id_level7_min + 9
    
    gdf_level7_selection = gdf_level7.loc[(gdf_level7["PFAF_ID"] >= pfaf_id_level7_min)&(gdf_level7["PFAF_ID"] <= pfaf_id_level7_max)]    
    return gdf_level7_selection


# In[13]:

list_level7_coast = []
for index, row in gdf_level6_coast.iterrows():
    pfaf_id_level6 = row["PFAF_ID"]
    gdf_level7_coast_selection = find_corresponding_basins(pfaf_id_level6,gdf_level7)
    list_level7_coast.append(gdf_level7_coast_selection)


# In[14]:

df = pd.concat(list_level7_coast)


# In[15]:

gdf_level7_coast = gpd.GeoDataFrame(df)


# In[16]:

# Combine level 6 inland with level 7 equivalent for coastal.


# In[17]:

gdf_combined = gdf_level6_inland.append(gdf_level7_coast)


# In[18]:

def explode(gdf):
    """ 
    Explodes a geodataframe 
    
    Will explode muti-part geometries into single geometries. Original index is
    stored in column level_0 and zero-based count of geometries per multi-
    geometry is stored in level_1
    
    Args:
        gdf (gpd.GeoDataFrame) : input geodataframe with multi-geometries
        
    Returns:
        gdf (gpd.GeoDataFrame) : exploded geodataframe with a new index 
                                 and two new columns: level_0 and level_1
        
    """
    gs = gdf.explode()
    gdf2 = gs.reset_index().rename(columns={0: 'geometry'})
    gdf_out = gdf2.merge(gdf.drop('geometry', axis=1), left_on='level_0', right_index=True)
    gdf_out = gdf_out.set_index(['level_0', 'level_1']).set_geometry('geometry')
    gdf_out.crs = gdf.crs
    return gdf_out


# In[19]:

gdf_exploded = explode(gdf_combined)


# In[20]:

gdf_exploded.head()


# In[21]:

gdf_exploded_noindex = gdf_exploded.reset_index()
gdf_exploded_noindex.drop(columns=["level_0","level_1"],inplace=True)


# In[22]:

output_filename = "test.shp"


# In[23]:

output_path = "{}/{}".format(ec2_output_path,output_filename)


# In[24]:

gdf_exploded_noindex['index'] = gdf_exploded_noindex.index


# In[25]:

gdf_exploded_noindex.to_file(filename=output_path,driver="ESRI Shapefile")


# In[26]:

get_ipython().system('aws s3 cp {ec2_output_path} {s3_output_path} --recursive ')


# In[ ]:



