
# coding: utf-8
-Import libraries (Done)
-Import Data (Done)
-Smooth Roads
    -Coordinates close to each other (Done)
-Detect non-existing IDs and create a file with it (Done, no errors found)
-Matching the coordinates from both files
-Detect Bridge and Road Errors and label 
-Create the outputs

# In[2]:

#Importing libraries
import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt


# In[118]:


#Import data from roads
InitialRoadData = pd.read_csv('..\RMMS\CSV\_allRoads.csv')
RoadData = InitialRoadData


# In[119]:

#Deleting inconsistent coordinates 
#Finding quantities out of tolerance. This is a 100m Tolerance
Tolerance = 0.00008
RoadData['UpperErrorLat']=abs(RoadData['Latitude'].shift(-1)-RoadData['Latitude'])>Tolerance
RoadData['BelowErrorLat']=abs(RoadData['Latitude'].shift()-RoadData['Latitude'])>Tolerance
RoadData['UpperErrorLon']=abs(RoadData['Longitude'].shift(-1)-RoadData['Longitude'])>Tolerance
RoadData['BelowErrorLon']=abs(RoadData['Longitude'].shift()-RoadData['Longitude'])>Tolerance
#Checking Road ID
RoadData['RoadIDCheckAbove']=RoadData['Road Id']==RoadData['Road Id'].shift(-1)
RoadData['RoadIDCheckBelow']=RoadData['Road Id']==RoadData['Road Id'].shift()
#Labeling Errors
RoadData['Error']=((RoadData['RoadIDCheckAbove'] & RoadData['RoadIDCheckBelow'] & ((RoadData['UpperErrorLat'] & RoadData['BelowErrorLat'])|(RoadData['UpperErrorLon'] & RoadData['BelowErrorLon'])))|
                   (RoadData['RoadIDCheckAbove'] & -RoadData['RoadIDCheckBelow'] & ((RoadData['UpperErrorLat'] &  -RoadData['UpperErrorLat'].shift(-1))|(RoadData['UpperErrorLon'] &  -RoadData['UpperErrorLon'].shift(-1))))|
                   (-RoadData['RoadIDCheckAbove'] & RoadData['RoadIDCheckBelow'] & ((RoadData['BelowErrorLat'] &  -RoadData['BelowErrorLat'].shift())|(RoadData['BelowErrorLon'] &  -RoadData['BelowErrorLon'].shift())))
                  )


# In[120]:

#Erasing Wrong values
RoadData.loc[RoadData.Error == True, 'Latitude'] = np.NaN
RoadData.loc[RoadData.Error == True, 'Longitude'] = np.NaN      


# In[121]:

#Interpolating 
SmoothRoadData = RoadData.interpolate()
#Formatting
del SmoothRoadData['UpperErrorLat']
del SmoothRoadData['UpperErrorLon']
del SmoothRoadData['BelowErrorLat']
del SmoothRoadData['BelowErrorLon']
del SmoothRoadData['RoadIDCheckAbove']
del SmoothRoadData['RoadIDCheckBelow']
del SmoothRoadData['Error']
SmoothRoadData.columns=SmoothRoadData.columns.str.replace('LRP Number','IDnumber')
SmoothRoadData.columns=SmoothRoadData.columns.str.replace('Road Id','RoadNo')



# In[122]:

#Load Bridge Data
InitialBridgeData = pd.read_csv('..\BMMS\CSV\_allBridges.csv')
#This texts deletes NaN values
BridgeData = InitialBridgeData
BridgeData.columns=BridgeData.columns.str.replace('BridgeNo','IDnumber')


# In[123]:

#Merge Data Frames
TotalData = pd.merge(BridgeData, SmoothRoadData, on=['RoadNo','IDnumber'], how='outer')
TotalData = TotalData.fillna(-1)


# In[124]:

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




# In[ ]:




# In[125]:

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


# In[126]:

FinalData.to_csv('TinderFile.csv')

