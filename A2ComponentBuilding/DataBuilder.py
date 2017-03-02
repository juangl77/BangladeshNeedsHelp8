from SimioObject import TruckObject, ChittagongObject, DhakaObject, BridgeObject, EndBridgeObject
from SimioLink import SimioLink, StartSimioLink, EndSimioLink, SimioBridgeLink
from SimioVertex import SimioVertex
from Location import Location

from BridgeIndexer import BridgeIndexer
from DataReader import RoadData, BridgeData

class DataBuilder():
	def __init__(self, roadData, index):
		self.startData = roadData[0]
		self.roadData = roadData[1:-1]
		self.endData = roadData[-1]
		self.index = index

	def mergeData(self):
		#Add condition and length values to the road data
		self.setBridgeData(self.startData)
		self.setBridgeData(self.endData)

		for road in self.roadData:
			self.setBridgeData(road)

		for road in self.roadData:
			if (road.hasGap()):
				print("{} (with gap {}): {} - {}".format(road.lrp,road.gap,road.condition,road.length))

	def setBridgeData(self, road):
		if road.hasGap() and (road.gap == "BS" or road.gap == "BE"):
			try:
				bridge = self.index.find(road.lrp)
				print('BRIDGE DATA: {} - {} - {}'.format(bridge.lrp,bridge.condition,bridge.length))
				road.condition = bridge.condition
				road.length = bridge.length
			except:
				print('No bridge found for start')
		return road

	def build(self):
		objects = [TruckObject(Location(23.7, 90.4), 48)]
		links = []
		vertices = []
		tempVertexData = []

		objects.append(self.buildDhaka(self.startData))

		for dataPoint in self.roadData:
			if dataPoint.hasGap():
				if dataPoint.gap == "BS":
					startNodeData = dataPoint
					if len(links) == 0:
						road = StartSimioLink(startNodeData.road, "Output@Dhaka", startNodeData.lrp)
					else:
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

		sink = self.buildChittagong(self.endData)
		lastLink = EndSimioLink(self.endData.road, objects[-1].lrp, "Input@Chittagong")
		objects.append(sink)
		links.append(lastLink)

		return (objects, links, vertices)

	def buildChittagong(self, dataPoint):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		return ChittagongObject(location, "Chittagong")

	def buildDhaka(self, dataPoint):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		interarrivalTime = 5
		return DhakaObject(location, "Dhaka", interarrivalTime)

	def buildBridge(self, startNodeData, endNodeData):
		bridgeStartLocation = Location(startNodeData.lat, startNodeData.lon)
		bridgeEndLocation = Location(endNodeData.lat, endNodeData.lon)
		length = bridgeStartLocation.distanceTo(bridgeEndLocation)
		condition = self.index.find(startNodeData.lrp).condition

		bridgeStart = BridgeObject(startNodeData.road, bridgeStartLocation, startNodeData.lrp, condition, length)
		bridgeEnd = EndBridgeObject(endNodeData.road, bridgeEndLocation, endNodeData.lrp, condition, length)
		bridgeLink = SimioBridgeLink(startNodeData.road, startNodeData.lrp, endNodeData.lrp)

		return (bridgeStart, bridgeEnd, bridgeLink)
