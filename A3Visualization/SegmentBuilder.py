import DataHandling
from SegmentUtils import SegmentDataFormatter, SegmentDataMerger, SegmentVulnerabilityCalculator, SegmentDataGrouper, SegmentDataProvider

class SuperSegment(object):
	def __init__(self, road, lrp, lat, lon, vulnerability):
		self.name = "segment_" + road + "_" + lrp
		self.road = road
		self.lrp = lrp
		self.lat = lat
		self.lon = lon
		self.vulnerability = vulnerability

	def __gt__(self, that):
		return self.vulnerability > that.vulnerability

	def __eq__(self, that):
		return self.vulnerability == that.vulnerability

class SegmentBuilder(object):
	def __init__(self, grouping_size):
		self.grouping_size = grouping_size

	def buildShort(self, scenario):
		return self.buildSelection(scenario, ['N1', 'N2', 'N3', 'N4', 'N5'])

	def buildAll(self, scenario):
		return self.buildSelection(scenario, DataHandling.readRoadIds())

	def buildSelection(self, scenario, road_ids):
		return [s for road_id in road_ids for s in self.build(road_id, scenario)]

	def build(self, road_id, scenario):
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

		return list(map(lambda row: self.buildSegment(row), segment_data))

	def buildSegment(self, row):
		road = row['road']
		lrp = row['LRPName']
		lat = row['Latitude']
		lon = row['Longitude']
		vulnerability = float(row['BridgeFailureLikelihood']) * float(row['TotalEconomicVulnerability'])

		return SuperSegment(road, lrp, lat, lon, vulnerability)