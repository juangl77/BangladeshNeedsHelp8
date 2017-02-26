import Constants

import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt

RoadIDCheckAbove = 'RoadIDCheckAbove'
RoadIDCheckBelow = 'RoadIDCheckBelow'
UpperErrorLat = 'UpperErrorLat'
BelowErrorLat = 'BelowErrorLat'
UpperErrorLon = 'UpperErrorLon'
BelowErrorLon = 'BelowErrorLon'
Error = 'Error'

LatitudeNotMatching = 'LatitudeNotMatching'
LongitudeNotMatching = 'LongitudeNotMatching'
NoDataInRoadFile = 'NoDataInRoadFile'
NoDataInBridgeFile = 'NoDataInBridgeFile'

def smoothRoads(roadFile):
    RoadData = pd.read_csv(roadFile)

    #Deleting inconsistent coordinates
    #Finding quantities out of tolerance. This tolerance may be improved by checking average differences!!
    Tolerance = 0.02
    RoadData[UpperErrorLat]=abs(RoadData[Constants.lat].shift(-1)-RoadData[Constants.lat])>Tolerance
    RoadData[BelowErrorLat]=abs(RoadData[Constants.lat].shift()-RoadData[Constants.lat])>Tolerance
    RoadData[UpperErrorLon]=abs(RoadData[Constants.lon].shift(-1)-RoadData[Constants.lon])>Tolerance
    RoadData[BelowErrorLon]=abs(RoadData[Constants.lon].shift()-RoadData[Constants.lon])>Tolerance
    #Checking Road ID
    RoadData[RoadIDCheckAbove]=RoadData[Constants.road]==RoadData[Constants.road].shift(-1)
    RoadData[RoadIDCheckBelow]=RoadData[Constants.road]==RoadData[Constants.road].shift()
    #Labeling Errors
    RoadData[Error]=((RoadData[RoadIDCheckAbove] & RoadData[RoadIDCheckBelow] & ((RoadData[UpperErrorLat] & RoadData[BelowErrorLat])|(RoadData[UpperErrorLon] & RoadData[BelowErrorLon])))|
                       (RoadData[RoadIDCheckAbove] & -RoadData[RoadIDCheckBelow] & ((RoadData[UpperErrorLat] &  -RoadData[UpperErrorLat].shift(-1))|(RoadData[UpperErrorLon] &  -RoadData[UpperErrorLon].shift(-1))))|
                       (-RoadData[RoadIDCheckAbove] & RoadData[RoadIDCheckBelow] & ((RoadData[BelowErrorLat] &  -RoadData[BelowErrorLat].shift())|(RoadData[BelowErrorLon] &  -RoadData[BelowErrorLon].shift())))
                      )

    #Erasing Wrong values
    RoadData.loc[RoadData.Error == True, Constants.lat] = np.NaN
    RoadData.loc[RoadData.Error == True, Constants.lon] = np.NaN

    #Interpolating
    SmoothRoadData = RoadData.interpolate()

    SmoothRoadData.drop([UpperErrorLat,UpperErrorLon,BelowErrorLat,BelowErrorLon,RoadIDCheckAbove,RoadIDCheckBelow,Error],inplace=True, axis=1)
    SmoothRoadData.to_csv('../RMMS/CSV/_allRoads_smoothed.csv',index=False)
    return '../RMMS/CSV/_allRoads_smoothed.csv'

def matchRoadToBridge(roadFile, bridgeFile):
    RoadData = pd.read_csv(roadFile)
    BridgeData = pd.read_csv(bridgeFile)

    originalRoadColumns = list(RoadData)
    originalBridgeColumns = list(BridgeData)

    RoadData.columns = [str(col) + '_Road' for col in RoadData.columns]
    BridgeData.columns = [str(col) + '_Bridge' for col in BridgeData.columns]

    BridgeData.columns=BridgeData.columns.str.replace(Constants.estimatedLoc+'_Bridge',Constants.estimatedLoc)
    BridgeData.columns=BridgeData.columns.str.replace(Constants.lrpname+'_Bridge',Constants.lrp)
    BridgeData.columns=BridgeData.columns.str.replace(Constants.road+'_Bridge',Constants.road)
    RoadData.columns=RoadData.columns.str.replace(Constants.lrp+'_Road',Constants.lrp)
    RoadData.columns=RoadData.columns.str.replace(Constants.road+'_Road',Constants.road)

    #Merge Data Frames
    TotalData = pd.merge(BridgeData, RoadData, on=[Constants.road,Constants.lrp], how='outer')
    TotalData = TotalData.fillna(-1)

    #Detecting Errors, tolerance of 10m
    Tolerance=0.00008993614
    TotalData[LatitudeNotMatching]=abs(TotalData.lat_Bridge-TotalData.lat_Road)>Tolerance
    TotalData[LongitudeNotMatching]=abs(TotalData.lon_Bridge-TotalData.lon_Road)>Tolerance
    TotalData[NoDataInRoadFile]=TotalData.lat_Road==-1
    TotalData[NoDataInBridgeFile]=TotalData.lat_Bridge==-1
    TotalData.loc[TotalData[LatitudeNotMatching]&-TotalData[LongitudeNotMatching]&-TotalData[NoDataInRoadFile]&-TotalData[NoDataInBridgeFile],Constants.estimatedLoc]=LatitudeNotMatching
    TotalData.loc[-TotalData[LatitudeNotMatching]&TotalData[LongitudeNotMatching]&-TotalData[NoDataInRoadFile]&-TotalData[NoDataInBridgeFile],Constants.estimatedLoc]=LongitudeNotMatching
    TotalData.loc[TotalData[LatitudeNotMatching]&TotalData[LongitudeNotMatching]&-TotalData[NoDataInRoadFile]&-TotalData[NoDataInBridgeFile],Constants.estimatedLoc]='LatAndLonNotMatching'
    TotalData.loc[TotalData[NoDataInRoadFile]&-TotalData[NoDataInBridgeFile],Constants.estimatedLoc]=NoDataInRoadFile
    TotalData.loc[-TotalData[NoDataInRoadFile]&TotalData[NoDataInBridgeFile],Constants.estimatedLoc]=NoDataInBridgeFile
    TotalData.loc[TotalData[NoDataInRoadFile]&TotalData[NoDataInBridgeFile],Constants.estimatedLoc]='NoDataInRoadAndBridgeFile'
    TotalData.loc[-TotalData[LatitudeNotMatching]&-TotalData[LongitudeNotMatching]&-TotalData[NoDataInRoadFile]&-TotalData[NoDataInBridgeFile],Constants.estimatedLoc]='Correct'

    TotalData[Constants.lat+'_Bridge'] = np.where((TotalData[Constants.estimatedLoc] == 'LatAndLonNotMatching'), TotalData[Constants.lat+'_Road'], TotalData[Constants.lat+'_Bridge'])
    TotalData[Constants.lat+'_Bridge'] = np.where((TotalData[Constants.estimatedLoc] == LatitudeNotMatching), TotalData[Constants.lat+'_Road'], TotalData[Constants.lat+'_Bridge'])
    TotalData[Constants.lon+'_Bridge'] = np.where((TotalData[Constants.estimatedLoc] == 'LatAndLonNotMatching'), TotalData[Constants.lon+'_Road'], TotalData[Constants.lon+'_Bridge'])
    TotalData[Constants.lat+'_Bridge'] = np.where((TotalData[Constants.estimatedLoc] == LongitudeNotMatching), TotalData[Constants.lat+'_Road'], TotalData[Constants.lat+'_Bridge'])
    TotalData[Constants.estimatedLoc] = np.where(TotalData[Constants.estimatedLoc] == 'LatAndLonNotMatching', 'RoadDataUsed', TotalData[Constants.estimatedLoc])
    TotalData[Constants.estimatedLoc] = np.where(TotalData[Constants.estimatedLoc] == LatitudeNotMatching, 'RoadDataUsed', TotalData[Constants.estimatedLoc])
    TotalData[Constants.estimatedLoc] = np.where(TotalData[Constants.estimatedLoc] == LongitudeNotMatching, 'RoadDataUsed', TotalData[Constants.estimatedLoc])

    TotalData.to_csv('merged.csv',index=False)

    RoadData_Updated = TotalData[(TotalData[Constants.estimatedLoc]=='Correct')|(TotalData[Constants.estimatedLoc]=='RoadDataUsed')|(TotalData[Constants.estimatedLoc]=='NoDataInBridgeFile')]
    BridgeData_Updated = TotalData[(TotalData[Constants.estimatedLoc]=='Correct')|(TotalData[Constants.estimatedLoc]=='RoadDataUsed')|(TotalData[Constants.estimatedLoc]=='NoDataInRoadFile')]

    #Format Final Files
    roads = RoadData_Updated[list(RoadData)].copy()
    bridges = BridgeData_Updated[list(BridgeData)].copy()

    roads.columns = originalRoadColumns
    bridges.columns = originalBridgeColumns

    #Replacing empty string that resulted from some fillna work
    roads[Constants.name] = np.where(roads[Constants.name] == -1, '', roads[Constants.name])

    roads.to_csv('../RMMS/CSV/_allRoads_matched.csv',index=False)
    bridges.to_csv('../BMMS/CSV/_allBridges_matched.csv',index=False)

    return ('../RMMS/CSV/_allRoads_matched.csv','../BMMS/CSV/_allBridges_matched.csv')
