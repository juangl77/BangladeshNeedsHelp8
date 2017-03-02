from SimioObject import TruckObject, ChittagongObject, DhakaObject, BridgeObject, EndBridgeObject
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
		tempVertexData = []

		objects.append(self.buildDhaka(self.startData))

		for dataPoint in self.roadData:
			if dataPoint.hasGap():
				if dataPoint.gap == "BS":
					startNodeData = dataPoint
					road = SimioLink(startNodeData.road, objects[-1].lrp, startNodeData.lrp)
					links.append(road)

					for vertexData in tempVertexData:
						vertices.append(SimioVertex(road.linkName, Location(vertexData.lat, vertexData.lon)))

					tempVertexData = []
				else :
					(bridgeStart, bridgeEnd, bridgeLink) = self.buildBridge(startNodeData, dataPoint)
					objects.append(bridgeStart)
					objects.append(bridgeEnd)
					links.append(bridgeLink)
			else:
				tempVertexData.append(dataPoint)

		objects.append(self.buildChittagong(self.endData))

		return (objects, links, vertices)

	def buildChittagong(self, dataPoint):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		return ChittagongObject(location, lrp)

	def buildDhaka(self, dataPoint):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		interarrivalTime = 5
		return DhakaObject(location, lrp, interarrivalTime)

	def buildBridge(self, startNodeData, endNodeData):
		bridgeStartLocation = Location(startNodeData.lat, startNodeData.lon)
		bridgeEndLocation = Location(endNodeData.lat, endNodeData.lon)
		length = bridgeStartLocation.distanceTo(bridgeEndLocation)
		condition = "NA"

		if startNodeData.lrp in self.index:
			condition = self.index[startNodeData.lrp].condition
		elif endNodeData.lrp in self.index:
			condition = self.index[endNodeData.lrp].condition

		bridgeStart = BridgeObject(startNodeData.road, bridgeStartLocation, startNodeData.lrp, condition, length)
		bridgeEnd = EndBridgeObject(endNodeData.road, bridgeEndLocation, endNodeData.lrp, condition, length)
		bridgeLink = SimioLink(startNodeData.road, startNodeData.lrp, endNodeData.lrp)

		return (bridgeStart, bridgeEnd, bridgeLink)
