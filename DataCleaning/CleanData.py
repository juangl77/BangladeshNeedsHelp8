import sys

import ParseHTM
import MatchingRoadBridge
import CoordinateFixing
import ReadWriteCSV

def deleteRowsWithBadData(rows):
    badCount = 0
    for row in rows:
        rowIsBad = False
        for (i,key) in enumerate(row):
            try:
                rowIsBad = True if float(row[key]) < 0 else False
            except ValueError:
                continue

        if rowIsBad:
            print(row)
            badCount += 1
            del row

    return (rows, badCount)

def prepareFinalData(roadFile, bridgeFile):
    roads = ReadWriteCSV.readRoads(roadFile)
    bridges = ReadWriteCSV.readBridges(bridgeFile)

    (roads, badRoadCount) = deleteRowsWithBadData(roads)
    (bridges, badBridgeCount) = deleteRowsWithBadData(bridges)
    print('{} roads and {} bridges were removed due to lingering bad data (should be 0)'.format(badRoadCount, badBridgeCount))

    ReadWriteCSV.writeRoads([ReadWriteCSV.Row(row) for row in roads],'../RMMS/CSV/_allRoads_cleaned.csv')
    ReadWriteCSV.writeBridges([ReadWriteCSV.Row(row) for row in bridges],'../BMMS/CSV/_allBridges_cleaned.csv')

    ReadWriteCSV.writeRoadsFinal('../RMMS/CSV/_allRoads_cleaned.csv','../WBSIM/infrastructure/_roads2.csv')
    ReadWriteCSV.writeBridgesFinal('../BMMS/CSV/_allBridges_cleaned.csv','../WBSIM/infrastructure/BMMS_overview.xlsx')

roadFileName = '../RMMS/CSV/_allRoads.csv'
bridgeFileName = '../BMMS/CSV/_allBridges.csv'

#First and optionally, parse the HTM data into CSV files ready for processing
#This is optional and triggered by a flag on calling because it takes some time
shouldConvertData = '--parse-data'
if len(sys.argv)>1 and sys.argv[1] == shouldConvertData:
    ParseHTM.parseRoadInfo()
    ParseHTM.parseBridgeInfo()

#Fix potential swaps of latitude and longitude in data
print('Performing coordinate swap...')
roadFileName = CoordinateFixing.fixRoads(roadFileName)
bridgeFileName = CoordinateFixing.fixBridges(bridgeFileName)

#Smooth road data to reduce effects of outlying points in a road due to bad data
print('Performing road smoothing...')
roadFileName = MatchingRoadBridge.smoothRoads(roadFileName)

#Address data sets where one of two sets of latitude/longitude are missing
print('Performing coordinate matching...')
(roadFileName,bridgeFileName) = MatchingRoadBridge.matchRoadToBridge(roadFileName,bridgeFileName)

#Finally, remove all roads and bridges that are outside the Bangladesh boundary
print('Perform boundary check...')
roadFileName = CoordinateFixing.boundCheckRoads(roadFileName)
bridgeFileName = CoordinateFixing.boundCheckBridges(bridgeFileName)

#Output the final results to the WBSIM folder for use
print('Writing final data...')
prepareFinalData(roadFileName,bridgeFileName)

print('Done with data cleaning')
