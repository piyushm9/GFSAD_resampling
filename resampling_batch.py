"""

RESAMPLING GFSAD 30M DATA TO 5ARC-MINUTE RESOLUTION """
#%%
import os, glob
import arcpy
from arcpy.sa import *
from arcpy import env

path = "D:\\Delaware\\Work\\resampling arcgis\\test2\\"
#path = "C:\\Work\\resampling\\gfsad\\eu_ca_ru_me\\"
#path1 = "C:\\Work\\resampling\\batch\\eur\\intermediate\\"
#path2 = "C:\\Work\\resampling\\batch\\eur\\output\\"
os.chdir(path)
arcpy.env.workspace = path
p = arcpy.mp.ArcGISProject('current')
m = p.listMaps()[0]

#%%

for f in glob.glob("*.tif"):    
#%%
    ## Build Pyramids
    #https://pro.arcgis.com/en/pro-app/tool-reference/data-management/build-pyramids.htm
    arcpy.BatchBuildPyramids_management(path+f, "", "","NEAREST", "DEFAULT", "", "SKIP_EXISTING")
    print('Built pyramids')

    ## Set Null
    #https://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/set-null.htm
    #generates the tiff file with 1s and 2s
    a = SetNull(path+f, path+f, "Value=0")
    print('SetNull complete')

    ## Get Extent
    # https://pro.arcgis.com/en/pro-app/arcpy/classes/extent.htm
    # https://community.esri.com/thread/10029
    x = Raster(path+f).extent
    
    ## Process: Clip Raster
    # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/clip.htm
    # '-10.0 30.0 0.0 40.0'
    x.XMin # 10.001213552687869     #left
    x.XMax # 0.0013474729261808704  #right
    x.YMin # 29.9990592501146       #bottom
    x.YMax # 40.108609626067285     #top
    # order for clip raster: left bottom right top
    l = round(x.XMin,0)
    r = round(x.XMax,0)
    b = round(x.YMin,0)
    t = round(x.YMax,0)
    extent1 = str(l)+' '+str(b)+' '+str(r)+' '+str(t) #left bottom right top
    #getting file name
    if len(f)==52:
        c = f.lower()[24:30]
    else:
        c = f.lower()[24:31]

    clip_raster = path1+c+'_clip.tif'
    arcpy.Clip_management(a, extent1, clip_raster, "", "NoData", "NONE", "MAINTAIN_EXTENT")
    print('Clip complete')

    ## Process: Create Fishnet
    #https://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-fishnet.htm
    grid = path1+c+"_grid.shp"
    origin_coord= str(l)+' '+str(b) # left bottom
    y_axis_coord= str(l)+' '+str(t) # left top 
    cell_width=""  #these values will be calcualted by the tool
    cell_height="" 
    # number of rows and columns together with origin and opposite corner determine the size of each cell
    number_rows="120" 
    number_columns="120"
    corner_coord= str(r)+' '+str(t) # right top
    labels="NO_LABELS"
    template= extent1 #left bottom right top
    geometry_type="POLYGON"
    arcpy.CreateFishnet_management(grid, origin_coord, y_axis_coord, cell_width, cell_height, number_rows, number_columns, corner_coord, labels, template, geometry_type)
    print('Fishnet complete')

    ## Process: Zonal Statistics as Table
    #https://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/zonal-statistics-as-table.htm
    mean_table = path1+c+"_mean.dbf"
    arcpy.gp.ZonalStatisticsAsTable_sa(grid, "FID", clip_raster, mean_table, "DATA", "MEAN")
    print('Zonal Statistics complete')

    ## Process: Add Join
    # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-join.htm
    grid1 = path1+c+"_grid1.shp"
    #join grid file with table
    joined = arcpy.AddJoin_management(grid, "FID", mean_table, "FID_", "KEEP_COMMON")
    #save as a new grid file
    print('Join complete')

    ## Process: Feature to Raster
    # https://pro.arcgis.com/en/pro-app/tool-reference/conversion/feature-to-raster.htm
    mean_raster = path1+c+"_mean.tif"
    arcpy.FeatureToRaster_conversion(joined, "MEAN", mean_raster, "0.08333333333333333333333333333333333333334")
    print('Feature to Raster complete')

    ## Process: Minus 1
    mean1_raster = path2+c+"_mean1.tif"
    arcpy.gp.Minus_sa(mean_raster, "1", mean1_raster)
    print('Minus complete')

    ## Remove all layers from the map
    layers = m.listLayers()
    tables = m.listTables()

    for layer in layers:
        len1 = len(m.listLayers())
        print(len1)
        if len1>0:
            m.removeLayer(layer)

    for table in tables:
        len2 = len(m.listTables())
        if len2>0:
            m.removeTable(table)
    print('All layers removed')
    print(f+'done')


## Mosaic Rasters
# https://pro.arcgis.com/en/pro-app/tool-reference/data-management/mosaic-to-new-raster.htm

import arcpy
from arcpy import env
import os, glob

path = "D:\\Delaware\\Work\\resampling arcgis\\5arcmin\\"
os.chdir(path)
arcpy.env.workspace = path
p = arcpy.mp.ArcGISProject('current')
m = p.listMaps()[0]
files = glob.glob("*.tif")

#a = files[0]
#b = files[1]
#c = a+';'+b


    
#arcpy.MosaicToNewRaster_management(files[0]+';'+files[1], path,"test.tif", "", "64 bit","0.0833333333333334", "1", "MEAN","FIRST")
    
#MosaicToNewRaster(input_rasters, output_location, raster_dataset_name_with_extension, {coordinate_system_for_the_raster}, {pixel_type}, {cellsize}, number_of_bands, {mosaic_method}, {mosaic_colormap_mode})

f=""
for file in files:
    f = f+';'+file

arcpy.MosaicToNewRaster_management(f, path, "europe.tif", "", "64 bit", "0.0833333333333334", "1", "MEAN","FIRST")





