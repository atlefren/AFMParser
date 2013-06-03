AFMParser
========

AFMParser is a parser for AFM (Atomic Force Microscpoy) scan files from Bruker NanoScale Analyzer.
The general idea is to generate a georeferenced DEM (Digital Elevation Model) that can be opened and analyzed
in off-the-shelf or open-source GIS-tools.

My understanding of AFM is rather non-existant, so I've based the parsing of the files on the Matlab-libraries provided
by Prof. Robert Carpick found on (http://nanoprobenetwork.org/software-library/welcome-to-the-carpick-labs-software-toolbox).

How to use
----------

The file test.py shows general usage. In short

    from parser import AFMParser

    #this parsed the header
    parser = AFMParser("path/to/file.001")
    #this reads the layer at index i and returns it as a 2-dim numpy array
    data = parser.read_layer(i)

Todo
----
This is by all means a work in progress. Several things remain to be done. See (http://gis.stackexchange.com/questions/62427/creating-nanoscale-dem-with-gdal)
for additional details.

Install
-------
Make sure to have the python-gdal bindings and numpy installed (can't get gdal to work with a virtualenv)

