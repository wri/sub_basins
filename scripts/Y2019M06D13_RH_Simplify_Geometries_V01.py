
# coding: utf-8

# In[52]:

""" Simplify geometry
-------------------------------------------------------------------------------

Simplify hydrobasin level 6 and 7 geometries. 

This script is not used since geopandas creates gaps between polygons after 
simplification. MapShaper can use a more advanced simplification algorithm.

We use https://mapshaper.org/ with the following settings:

- input_files = See S3 input path
- detect line intersections = True
- snap vertices = True

Simplify
- prevent shape removal = False
- use planar geometry = False
- method: Visvalingam's Algorithm / weighted area

percentage: 50% (Selected based on visual inspection)
44 line errors (level7)
12 line errors (level6):
- repair = True


Author: Rutger Hofste
Date: 20190613
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

SCRIPT_NAME = "Y2019M06D13_RH_Simplify_Geometries_V01"
OUTPUT_VERSION  = 1
 
# Tolerance in degrees (appr. 1 km at equator)
TOLERANCE = 360/43200 

S3_INPUT_PATH= "s3://wri-projects/Aqueduct30/rawData/WWF/HydroSheds30sComplete/00_consolidated"

ec2_input_path = "/volumes/data/{}/input_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)
ec2_output_path = "/volumes/data/{}/output_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)

s3_output_path = "s3://wri-projects/Aqueduct30/processData/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)


# In[32]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version
get_ipython().magic('matplotlib inline')


# In[7]:

levels = [6]


# In[17]:

level = levels[0]


# In[9]:

get_ipython().system('rm -r {ec2_input_path} ')
get_ipython().system('rm -r {ec2_output_path} ')
get_ipython().system('mkdir -p {ec2_input_path} ')
get_ipython().system('mkdir -p {ec2_output_path} ')


# In[18]:

s3_input_path = "{}/level{}".format(S3_INPUT_PATH,level)


# In[19]:

s3_input_path


# In[20]:

get_ipython().system('aws s3 cp {s3_input_path} {ec2_input_path} --recursive')


# In[21]:

input_filename = "hybas_merged_standard_level{}_V01.shp".format(level)


# In[23]:

input_path = "{}/{}".format(ec2_input_path,input_filename)


# In[24]:

import geopandas as gpd


# In[25]:

gdf = gpd.read_file(filename=input_path)


# In[28]:

gdf =gdf[1:10]


# In[40]:

gdf_simplified = gdf.copy()


# In[41]:

gdf_simplified["geometry"] = gdf.geometry.simplify(tolerance=TOLERANCE,preserve_topology=True)


# In[45]:

output_filename = "hydrobasin_level_{:02d}_simplified.shp".format(level)


# In[47]:

output_path = "{}/{}".format(ec2_output_path,output_filename)


# In[54]:

gdf.crs


# In[51]:

gdf_simplified.to_file(filename=output_path,
                       driver="ESRI Shapefile")


# In[53]:

get_ipython().system('aws s3 cp {ec2_output_path} {s3_output_path} --recursive ')


# In[ ]:



