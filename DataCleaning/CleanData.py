import sys

import ParseHTM
import MatchingRoadBridge
import CoordinateFixing

#First and optionally, parse the HTM data into CSV files ready for processing
#This is optional and triggered by a flag on calling because it takes some time
shouldConvertData = '--parse-data'
if len(sys.argv)>1 and sys.argv[1] == shouldConvertData:
    ParseHTM.parseRoadInfo()
    ParseHTM.parseBridgeInfo()

#Fix potential swaps of latitude and longitude in data
CoordinateFixing.fixRoads()
CoordianteFixing.fixBridges()

#Smooth road data to reduce effects of outlying points in a road due to bad data


#Address data sets where one of two sets of latitude/longitude are missing


#Finally, remove all roads and bridges that are outside the Bangladesh boundary
CoordinateFixing.boundCheckRoads()
CoordinateFixing.boundCheckBridges()

print('Done with data cleaning.')
