from parser import AFMParser
from numpy import *
import gdal

parser = AFMParser("data/POPC.001")

data = parser.read_layer(0)

driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create(
    '193.tiff',
    data.shape[1],
    data.shape[0],
    1 ,
    gdal.GDT_Int16 ,
)

dst_ds.GetRasterBand(1).WriteArray(data)
