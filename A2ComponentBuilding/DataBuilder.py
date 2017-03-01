from SimioObject import TruckObject, ChittagongObject, DhakaObject, BridgeObject
from SimioLink import SimioLink
from SimioVertex import SimioVertex
from Location import Location

from BridgeIndexer import BridgeIndexer
from DataReader import RoadData, BridgeData

class DataBuilder():
	def __init__(self, roadData, indexer):
		self.startData = roadData[0]
		self.roadData = roadData[1:-1]
		self.endData = roadData[-1]
		self.index = indexer.index

	def build(self):
		objects = [TruckObject(Location(0,0,0), 48)]
		links = []
		vertices = []

		objects.append(ChittagongObject(Location(10,0,10), self.startData.lrp, 5))

		for dataPoint in self.roadData:
			if dataPoint.hasGap():
				# bridgeData = self.index[dataPoint.lrp]
				bridge = BridgeObject(dataPoint.road, Location(0,0,0), dataPoint.lrp, "A", 50)
				lastLRP = objects[-1].lrp
				links.append(SimioLink(dataPoint.road, lastLRP, dataPoint.lrp))
				objects.append(bridge)
			else:
				vertices.append(SimioVertex(dataPoint.road, dataPoint.lrp, Location(0,0,0)))

		objects.append(DhakaObject(Location(10,0,10), self.endData.lrp))

		return (objects, links, vertices)
