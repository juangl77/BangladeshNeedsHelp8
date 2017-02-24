import sys

import ParseHTM
import MatchingRoadBridge
import CoordinateFixing
import ReadWriteCSV

def prepareFinalData():
    ReadWriteCSV.writeRoadsFinal('../RMMS/CSV/_allRoads_final.csv','../_roads2.csv')
    ReadWriteCSV.writeBridgesFinal('../BMMS/CSV/_allBridges_final.csv','../BMMS_overview.xlsx')

#First and optionally, parse the HTM data into CSV files ready for processing
#This is optional and triggered by a flag on calling because it takes some time
shouldConvertData = '--parse-data'
if len(sys.argv)>1 and sys.argv[1] == shouldConvertData:
    #ParseHTM.parseRoadInfo()
    ParseHTM.parseBridgeInfo()

#Fix potential swaps of latitude and longitude in data
print('Performing coordinate swap...')
CoordinateFixing.fixRoads()
CoordinateFixing.fixBridges()

#Smooth road data to reduce effects of outlying points in a road due to bad data
print('Performing road smoothing...')
MatchingRoadBridge.smoothRoads()

#Address data sets where one of two sets of latitude/longitude are missing
print('Performing coordinate matching...')


#Finally, remove all roads and bridges that are outside the Bangladesh boundary
print('Perform boundary check...')
CoordinateFixing.boundCheckRoads()
CoordinateFixing.boundCheckBridges()

#Output the final results to the WBSIM folder for use
print('Writing final data...')
prepareFinalData()

print('Done with data cleaning')
