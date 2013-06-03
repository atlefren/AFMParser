from parser import AFMParser
from numpy import *
import gdal
import osr

def get_coordsys():
    #load our custom crs
    prj_text = open("coordsys.wkt", 'r').read()
    srs = osr.SpatialReference()
    if srs.ImportFromWkt(prj_text):
        raise ValueError("Error importing PRJ information" )

    return srs

def get_transform(parser, data):
    #calculate dims
    scan_size, x_offset, y_offset = parser.get_size()
    x_size = data.shape[0]
    y_size = data.shape[1]
    x_res = scan_size / x_size
    y_res = scan_size / y_size

    #set the transform (offsets doesn't seem to work the way I think)
    #top left x, w-e pixel resolution, rotation, 0 if image is "north up", top left y, rotation, 0 if image is "north up", n-s pixel resolution
    return [0, x_res, 0, 0, 0, y_res]


def create_dem(afmfile, outfile):

    #parse the afm data
    parser = AFMParser(afmfile)

    #flip to account for the fact that the matrix is top-left, but gdal is bottom-left
    data = flipud(parser.read_layer(0))

    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(
        outfile,
        data.shape[1],
        data.shape[0],
        1 ,
        gdal.GDT_Int16 ,
    )

    dst_ds.SetGeoTransform(get_transform(parser, data))
    dst_ds.SetProjection(get_coordsys().ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds = None


create_dem("data/POPC.013", "test2.tiff")