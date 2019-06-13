# WRI version of HydroBASINS
Create hydrological sub-basins for water risk calculation using various levels of HydroBASINS.

## Rationale 

Water related stress metrics are often calculated by aggregating pixel data to a hydrological sub-basin unit. The [HydroBASIN](https://hydrosheds.org/images/inpages/HydroBASINS_TechDoc_v1c.pdf) dataset can be used for this but has limitation. For many of the water related stress metrics, it is assumed that water resources are pooled (shared) within each sub-basin. Using the default HydroBASIN, this assumption will not hold in the following cases:

### Delta regions
Streams cannot bifurcate in the HydroBASIN and HydroSHEDS datasets leading to inaccurate representation of deltas.

### Coastal and island regions 
Coastal regions and islands are often grouped into a single multipolygon. The hydrology however, is often not connected leading to erroneous results. 

## Approach 

In this repo, we develop an approach to address some of these issues by combining several levels of HydroBASIN data, apply a few GIS processing steps and by grouping delta regions. 

The result is a database that addresses some of the major limitations of the default HydroBASINS data. 

## Limitations

TBD
