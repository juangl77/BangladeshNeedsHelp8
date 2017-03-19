import pandas as pd
import numpy as np
import math as m
import DataHandling

class SegmentDataFormatter(object):
	def formatWidthData(self, dataframe):
		dataframe = dataframe.drop(['width', 'roadId'], 1)
		dataframe = dataframe.sort_values(by=['road','startChainage']).reset_index()
		dataframe = dataframe.drop('index',1)
		return dataframe

	def formatBridgeData(self, dataframe):
		dataframenoduplicates = dataframe.drop_duplicates('LRPName', keep = 'first')
		dataframemodified = dataframenoduplicates.ix[:,:10]
		dataframemodified = dataframemodified.drop(['km','structureNr','type','roadName','length','name'], 1)
		dataframemodified = dataframemodified.sort_values(by=['road','chainage']).reset_index()
		dataframemodified = dataframemodified.drop('index', 1)
		return dataframemodified

	def formatTrafficData(self, dataframe, sideofroad = 'both'):
		dataframe = dataframe.drop(['name','start_lrp','start_offset','end_lrp','end_offset','length'],1)
		dataframe.columns = dataframe.columns.str.replace('start_chainage','startChainage')
		dataframe.columns = dataframe.columns.str.replace('end_chainage','endChainage')
		dataframe = dataframe.sort_values(by = ['road','startChainage','linkNo'] ).reset_index()
		dataframe = dataframe.drop('index', 1)

		if sideofroad == 'both':
		    dataframe = dataframe.groupby(['road','startChainage'],as_index=False).sum()

		return dataframe

class SegmentDataMerger(object):
	def merge(self, trafficData, bridgeData, widthData, roadside = 'both'):
		indexesMergedData = list(widthData['startChainage'].searchsorted(bridgeData['chainage'], side = 'right'))
		addedNrLanes = bridgeData

		list_a = []
		for i in indexesMergedData:
			list_a.append(widthData['nrLanes'][int(i)-1])

		addedNrLanes['nrLanes']=list_a
		bridgeData = addedNrLanes
		addedTrafficData = bridgeData

		for title in trafficData.ix[:,3:].columns:
			indexesMergedData = trafficData['startChainage'].searchsorted(bridgeData['chainage'], side = 'right')
			indexesMergedData =indexesMergedData.tolist()

			list_b=[]
			skip_add=False
			for i in indexesMergedData:
				try:
					list_b.append(trafficData[title][int(i)-1])
				except:
					skip_add=True

			if not skip_add:
				addedTrafficData[title]=list_b

		return addedTrafficData

class SegmentDataProvider(object):
	def __init__(self):
		self.formatter = SegmentDataFormatter()

	def provideRawBridges(self, road_id):
		return DataHandling.readBridges(road_id)

	def provideFormattedBridges(self, road_id):
		return self.formatter.formatBridgeData(self.provideRawBridges(road_id))

	def provide(self, road_id):
		parts = DataHandling.readRoads(road_id)
		widths = self.formatter.formatWidthData(DataHandling.readWidths(road_id))
		traffic = self.formatter.formatTrafficData(DataHandling.readTraffic(road_id))

		merged_data = SegmentDataMerger().merge(traffic, self.provideFormattedBridges(road_id), widths)

		return self.addLaneDensity(merged_data)

	def addLaneDensity(self, data_frame):
		for title in data_frame.ix[:,5:].columns:
			data_frame[title] = data_frame[title] / data_frame['nrLanes']
		return data_frame

class SegmentVulnerabilityCalculator(object):
	def __init__(self, truck_capacity, social_car_capacity, scenario):
		self.truck_capacity = truck_capacity
		self.social_car_capacity = social_car_capacity
		self.scenario = scenario

	def calculate(self, dataframe):
		vulbasematrix = dataframe.ix[:,:4]

		if not vulbasematrix.empty:
		    vulbasematrix.loc[vulbasematrix.condition == 'A', 'BridgeFailureLikelihood'] = self.scenario.a
		    vulbasematrix.loc[vulbasematrix.condition == 'A', 'NumberOfABridges'] = 1
		    vulbasematrix.loc[vulbasematrix.condition != 'A', 'NumberOfABridges'] = 0
		    vulbasematrix.loc[vulbasematrix.condition == 'B', 'NumberOfBBridges'] = 1
		    vulbasematrix.loc[vulbasematrix.condition != 'B', 'NumberOfBBridges'] = 0
		    vulbasematrix.loc[vulbasematrix.condition == 'C', 'NumberOfCBridges'] = 1
		    vulbasematrix.loc[vulbasematrix.condition != 'C', 'NumberOfCBridges'] = 0
		    vulbasematrix.loc[vulbasematrix.condition == 'D', 'NumberOfDBridges'] = 1
		    vulbasematrix.loc[vulbasematrix.condition != 'D', 'NumberOfDBridges'] = 0
		    vulbasematrix.loc[vulbasematrix.condition == 'B', 'BridgeFailureLikelihood'] = self.scenario.b
		    vulbasematrix.loc[vulbasematrix.condition == 'C', 'BridgeFailureLikelihood'] = self.scenario.c
		    vulbasematrix.loc[vulbasematrix.condition == 'D', 'BridgeFailureLikelihood'] = self.scenario.d

		cargo_titles = ['heavyTruck', 'mediumTruck', 'smallTruck']
		social_titles = ['largeBus','mediumBus','microBus','utility','car','autoRickshaw','motorcycle','bicycle','cycleRickshaw','cart']

		vulbasematrix['TrafficEconomicVulnerability'] = 0
		for i in range(len(cargo_titles)):
			additionalVulnerability = -42
			try:
				additionalVulnerability = dataframe[cargo_titles[i]]*self.truck_capacity[i]
			except:
				additionalVulnerability = 0
			vulbasematrix['TrafficEconomicVulnerability'] = vulbasematrix['TrafficEconomicVulnerability'] + additionalVulnerability

		vulbasematrix['TrafficSocialVulnerability'] = 0
		for i in range(len(social_titles)):
			additionalVulnerability = -42
			try:
				additionalVulnerability = dataframe[social_titles[i]]*self.social_car_capacity[i]
			except:
				additionalVulnerability = 0
			vulbasematrix['TrafficSocialVulnerability'] =  vulbasematrix['TrafficSocialVulnerability']+additionalVulnerability

		vulbasematrix['TotalTraffic'] = vulbasematrix['TrafficEconomicVulnerability']+vulbasematrix['TrafficSocialVulnerability']

		if vulbasematrix.empty:
			vulbasematrix['TotalEconomicVulnerability'] = 0
			vulbasematrix['TotalSocialVulnerability'] = 0
		else:
			vulbasematrix['TotalEconomicVulnerability'] = vulbasematrix['TrafficEconomicVulnerability']*vulbasematrix['BridgeFailureLikelihood']
			vulbasematrix['TotalSocialVulnerability'] = vulbasematrix['TrafficSocialVulnerability']*vulbasematrix['BridgeFailureLikelihood']

		return vulbasematrix

class SegmentDataGrouper(object):
	def __init__(self, group_size):
		self.group_size = group_size

	def group(self, bridges, dataframe):
		londictionary = dict(zip(bridges['LRPName'], bridges['lon']))
		latdictionary = dict(zip(bridges['LRPName'], bridges['lat']))

		temp = dataframe.groupby(['road',np.floor(dataframe.index/1.0*self.group_size)], as_index = False).sum()
		result = dataframe.groupby(['road',np.floor(dataframe.index/(1.0*self.group_size))], as_index = False)

		bridgereliability = result.apply(lambda x: np.product(1-x['BridgeFailureLikelihood'])).reset_index(drop=True)

		lista = []
		for i in bridgereliability:
			lista.append(i.max())

		if not lista:
			return {}

		result = result.max()

		result['NumberOfABridges'] = temp['NumberOfABridges']
		result['NumberOfBBridges'] = temp['NumberOfBBridges']
		result['NumberOfCBridges'] = temp['NumberOfCBridges']
		result['NumberOfDBridges'] = temp['NumberOfDBridges']

		result['BridgeFailureLikelihood'] = 1-pd.DataFrame(lista)
		result['TotalSocialVulnerability'] = result['TrafficSocialVulnerability']*result['BridgeFailureLikelihood']
		result['TotalEconomicVulnerability'] = result['TrafficEconomicVulnerability']*result['BridgeFailureLikelihood']
		result = result.drop('condition',1)
		result['Latitude']=result['LRPName']
		result['Longitude']=result['LRPName']
		result = result.replace({"Latitude": latdictionary})
		result = result.replace({"Longitude": londictionary})

		return result.to_dict('records')
