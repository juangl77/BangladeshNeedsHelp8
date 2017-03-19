import DataHandling
from SegmentUtils import SegmentDataFormatter, SegmentDataMerger, SegmentVulnerabilityCalculator, SegmentDataGrouper, SegmentDataProvider

class SuperSegment(object):
	def __init__(self, road, lrp, lat, lon, vulnerability, traffic):
		self.name = "segment_" + road + "_" + lrp
		self.road = road
		self.lrp = lrp
		self.lat = lat
		self.lon = lon
		self.vulnerability = vulnerability
		self.originalTraffic = traffic

	def __gt__(self, that):
		return self.vulnerability > that.vulnerability

	def __eq__(self, that):
		return self.vulnerability == that.vulnerability

class SegmentBuilder(object):
	def __init__(self, grouping_size, mode):
		self.grouping_size = grouping_size
		self.road_ids = []
		if mode == 'short':
			self.road_ids = ['N1','N2','N3','N4','N5']
		elif mode == 'all':
			self.road_ids = DataHandling.readRoadIds()
		else:
			for ch in list(mode):
				self.road_ids.extend(DataHandling.readRoadIds(typeChar=ch))

	def buildSelection(self, scenario):
		all_data = []
		for road_id in self.road_ids:
			all_data.extend(self.build(road_id, scenario))
		return all_data
		#return [s for road_id in road_ids for s in self.build(road_id, scenario)] EEB

	def build(self, road_id, scenario):
		print('{} - '.format(road_id), end='')

		provider = SegmentDataProvider()
		grouper = SegmentDataGrouper(self.grouping_size)

		truck_capacity = [15,10,5]
		social_car_capacity = [45,30,15,6,4,2,2,1,2,1]

		road_data = provider.provide(road_id)
		bridge_data = provider.provideRawBridges(road_id)

		if road_data.empty:
			return list()

		calculator = SegmentVulnerabilityCalculator(truck_capacity, social_car_capacity, scenario)
		vulnerability_data = calculator.calculate(road_data)

		segment_data = grouper.group(bridge_data, vulnerability_data)

		return segment_data
		#return list(map(lambda row: self.buildSegment(row), segment_data))

	def buildSegment(self, row):
		road = row['road']
		lrp = row['LRPName']
		lat = row['Latitude']
		lon = row['Longitude']
		vulnerability = float(row['BridgeFailureLikelihood']) * float(row['TotalEconomicVulnerability'])
		traffic = float(row['TotalEconomicVulnerability'])

		return SuperSegment(road, lrp, lat, lon, vulnerability, traffic)
