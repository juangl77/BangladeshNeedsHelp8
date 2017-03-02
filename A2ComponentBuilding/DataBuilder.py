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
		objects = [TruckObject(Location(0,0), 48)]
		links = []
		vertices = []

		objects.append(self.buildChittagong())

		for dataPoint in self.roadData:
			if dataPoint.hasGap():
				if dataPoint.gap == "BS":
					startNodeData = dataPoint
				else :
					(bridgeStart, bridgeEnd, linkRoad, linkBridge) = self.buildBridge(objects[-1], startNodeData, dataPoint)
					objects.append(bridgeStart)
					objects.append(bridgeEnd)
					links.append(linkRoad)
					links.append(linkBridge)
			else:
				vertices.append(SimioVertex(dataPoint.road, dataPoint.lrp, Location(dataPoint.lat, dataPoint.lon)))

		objects.append(self.buildDhaka())

		return (objects, links, vertices)

	def buildChittagong(self):
		location = Location(self.startData.lat,self.startData.lon)
		lrp = self.startData.lrp
		interarrivalTime = 5
		return ChittagongObject(location, lrp, interarrivalTime)

	def buildDhaka(self):
		location = Location(self.endData.lat, self.endData.lon)
		lrp = self.endData.lrp
		return DhakaObject(location, lrp)

	def buildBridge(self, lastNode, startNodeData, endNodeData):
		bridgeStartLocation = Location(startNodeData.lat, startNodeData.lon)
		bridgeEndLocation = Location(endNodeData.lat, endNodeData.lon)
		length = bridgeStartLocation.distanceTo(bridgeEndLocation)
		condition = "NA"

		if startNodeData.lrp in self.index:
			condition = self.index[startNodeData.lrp].condition
		elif endNodeData.lrp in self.index:
			condition = self.index[endNodeData.lrp].condition

		bridgeStart = BridgeObject(startNodeData.road, bridgeStartLocation, startNodeData.lrp, condition, length)
		bridgeEnd = BridgeObject(endNodeData.road, bridgeEndLocation, endNodeData.lrp, condition, length)
		linkRoad = SimioLink(startNodeData.road, lastNode.lrp, startNodeData.lrp)
		linkBridge = SimioLink(startNodeData.road, startNodeData.lrp, endNodeData.lrp)

		return (bridgeStart, bridgeEnd, linkRoad, linkBridge)
