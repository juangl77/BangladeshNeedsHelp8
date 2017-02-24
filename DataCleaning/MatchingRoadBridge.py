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

def smoothRoads():
    RoadData = pd.read_csv('../RMMS/CSV/_allRoads_fixed.csv')

    #Deleting inconsistent coordinates
    #Finding quantities out of tolerance. This is a 100m Tolerance
    Tolerance = 0.00008
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
    RoadData.loc[RoadData.Error == True, Constants.lat] = -42
    RoadData.loc[RoadData.Error == True, Constants.lon] = -42

    #Interpolating
    SmoothRoadData = RoadData.interpolate()

    #Formatting
    del SmoothRoadData[UpperErrorLat]
    del SmoothRoadData[UpperErrorLon]
    del SmoothRoadData[BelowErrorLat]
    del SmoothRoadData[BelowErrorLon]
    del SmoothRoadData[RoadIDCheckAbove]
    del SmoothRoadData[RoadIDCheckBelow]
    del SmoothRoadData[Error]

    SmoothRoadData.to_csv('../RMMS/CSV/_allRoads_smoothed.csv')

def matchRoadToBridge():
    RoadData = pd.read_csv('../RMMS/CSV/_allRoads_smoothed.csv')
    BridgeData = pd.read_csv('../BMMS/CSV/_allBridges.csv')

    BridgeData.columns=BridgeData.columns.str.replace(Constants.lrpname,Constants.lrp)

    #Merge Data Frames
    TotalData = pd.merge(BridgeData, RoadData, on=[Constants.road,Constants.lrp], how='outer')
    TotalData = TotalData.fillna(-1)

    #Detecting Errors
    TotalData['LatitudeNotMatching']=abs(TotalData.Latitude_x-TotalData.Latitude_y)>Tolerance
    TotalData['LongitudeNotMatching']=abs(TotalData.Longitude_x-TotalData.Longitude_y)>Tolerance
    TotalData['NoDataInRoadFile']=TotalData.Latitude_y==-1
    TotalData['NoDataInBridgeFile']=TotalData.Latitude_x==-1
    TotalData.loc[TotalData['LatitudeNotMatching']&TotalData['LongitudeNotMatching']&-TotalData['NoDataInRoadFile']&-TotalData['NoDataInBridgeFile'],'TypeOfError']='LatAndLongNotMatching'
    TotalData.loc[TotalData['LatitudeNotMatching']&-TotalData['LongitudeNotMatching']&-TotalData['NoDataInRoadFile']&-TotalData['NoDataInBridgeFile'],'TypeOfError']='LatNotMatching'
    TotalData.loc[-TotalData['LatitudeNotMatching']&TotalData['LongitudeNotMatching']&-TotalData['NoDataInRoadFile']&-TotalData['NoDataInBridgeFile'],'TypeOfError']='LongNotMatching'
    TotalData.loc[TotalData['NoDataInRoadFile']&TotalData['NoDataInBridgeFile'],'TypeOfError']='NoDataInRoadAndBridgeFile'
    TotalData.loc[TotalData['NoDataInRoadFile']&-TotalData['NoDataInBridgeFile'],'TypeOfError']='NoDataInRoadFile'
    TotalData.loc[-TotalData['NoDataInRoadFile']&TotalData['NoDataInBridgeFile'],'TypeOfError']='NoDataInBridgeFile'
    TotalData.loc[-TotalData['LatitudeNotMatching']&-TotalData['LongitudeNotMatching']&-TotalData['NoDataInRoadFile']&-TotalData['NoDataInBridgeFile'],'TypeOfError']='CorrectData'

    #Format Final File
    FinalData=TotalData
    del FinalData['LatitudeNotMatching']
    del FinalData['LongitudeNotMatching']
    del FinalData['NoDataInRoadFile']
    del FinalData['NoDataInBridgeFile']
    FinalData.columns=FinalData.columns.str.replace('Latitude_x','Latitude_B')
    FinalData.columns=FinalData.columns.str.replace('Latitude_y','Latitude_R')
    FinalData.columns=FinalData.columns.str.replace('Longitude_x','Longitude_B')
    FinalData.columns=FinalData.columns.str.replace('Longitude_y','Longitude_R')

    FinalData.to_csv('TinderFile.csv')
