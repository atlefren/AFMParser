from parser import AFMParser
from numpy import *
import gdal
import osr

#load our custom crs
prj_text = open("coordsys.wkt", 'r').read()
srs = osr.SpatialReference()
if srs.ImportFromWkt(prj_text):
    raise ValueError("Error importing PRJ information" )

#parse the afm data
parser = AFMParser("data/POPC.001")

#flip to account for the fact that the matrix is top-left, but gdal is bottom-left
data = flipud(parser.read_layer(0))

driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create(
    'test1.tiff',
    data.shape[1],
    data.shape[0],
    1 ,
    gdal.GDT_Int16 ,
)

#calculate dims
scan_size, x_offset, y_offset = parser.get_size()
x_size = data.shape[0]
y_size = data.shape[1]
x_res = scan_size / x_size
y_res = scan_size / y_size

#set the transform (offsets doesn't seem to work the way I think)

#w-e pixel resolution, rotation, 0 if image is "north up", top left y, rotation, 0 if image is "north up", n-s pixel resolution
dst_ds.SetGeoTransform([0, x_res, 0, 0, 0, y_res])
dst_ds.SetProjection(srs.ExportToWkt())
dst_ds.GetRasterBand(1).WriteArray(data)
dst_ds = None