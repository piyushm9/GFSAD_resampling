## Mosaic Rasters
# https://pro.arcgis.com/en/pro-app/tool-reference/data-management/mosaic-to-new-raster.htm

import arcpy
from arcpy import env
import os, glob

path = "D:\\Delaware\\Work\\resampling arcgis\\batch\\mosaic"
os.chdir(path)
arcpy.env.workspace = path
p = arcpy.mp.ArcGISProject('current')
m = p.listMaps()[0]
files = glob.glob("*.tif")
layers = m.listLayers()
   
#MosaicToNewRaster(input_rasters, output_location, raster_dataset_name_with_extension, {coordinate_system_for_the_raster}, {pixel_type}, {cellsize}, number_of_bands, {mosaic_method}, {mosaic_colormap_mode})

f=""
for file in files:
    f = f+';'+file
arcpy.MosaicToNewRaster_management(f, path, "cropland_extent_5arcmin.tif", "", "64 bit", "0.0833333333333334", "1", "MAXIMUM","FIRST")

# using MAXIMUM here because there are many overlapping tiles and we want the cropland extent


arcpy.MosaicToNewRaster_management('sa_afg.tif;se_ne.tif', path, "test.tif", "", "64 bit", "0.0833333333333334", "1", "MAXIMUM","FIRST")