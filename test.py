from parser import AFMParser
from numpy import *
import Image

parser = AFMParser("data/POPC.001")

scan =  parser.get_scans()[0]
for key, val in scan.iteritems():
    print key,"::" , val

for i in range(0, 3):

    scale = parser.get_scale(i)
    print "layer %s" %i
    print "name:", parser.get_layer_name(i)
    print "scale:", scale

    data = parser.read_layer(i)
    print amin(data), amax(data)
    print data


    rot_and_scaled = rot90(data * scale)
    #img = Image.fromarray(rot_and_scaled, mode='L')
    #img.show()
