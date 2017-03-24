from SimioObject import TruckObject, BusObject, PassengerVehicleObject, ChittagongObject, DhakaObject, BridgeObject, EndBridgeObject
from SimioLink import SimioLink, StartSimioLink, EndSimioLink, SimioBridgeLink
from SimioVertex import SimioVertex
from Location import Location

from math import ceil

from BridgeIndexer import BridgeIndexer
from DataReader import RoadData, BridgeData, TrafficData, Traffic

class DataBuilder():

	def __init__(self, roadData, index, trafficData):
		self.startData = roadData[0]
		self.roadData = roadData[1:-1]
		self.endData = roadData[-1]
		self.index = index
		self.trafficData = trafficData

		self.categoryECount = 0
		self.bridgeCount = 0

	def build(self):
		links = []
		vertices = []
		tempVertexData = []
		# objects = [TruckObject(Location(23.7, 90.4), 48),BusObject(Location(23.7,89.996), 48),PassengerVehicleObject(Location(23.7,89.992), 48)]
		objects = []

		objects.append(self.buildDhaka(self.startData, self.trafficData[0]))

		currentTrafficIndex = 0
		for dataPoint in self.roadData:
			if dataPoint.hasGap():
				#Go to the first width entry where the end chainage is greater than the current datapoint's chainage
				originalTrafficIndex = currentTrafficIndex
				while(dataPoint.chainage > self.trafficData[currentTrafficIndex].endChainage):
					currentTrafficIndex += 1
				lanes = self.trafficData[currentTrafficIndex].numberLanes

				#if traffic chainage index has changed, source or sink needs to be incorporated here
				if originalTrafficIndex != currentTrafficIndex :
					originalTraffic = self.trafficData[originalTrafficIndex]
					newTraffic = self.trafficData[currentTrafficIndex]
					if abs(originalTraffic.leftTraffic.totalTraffic()-newTraffic.leftTraffic.totalTraffic()) > 1:
						print('need to change traffic flow now. {} -> {}'.format(originalTraffic.leftTraffic.totalTraffic(),newTraffic.leftTraffic.totalTraffic()))

				if dataPoint.gap == "BS":
					startNodeData = dataPoint
					if len(links) == 0:
						road = StartSimioLink(startNodeData.road, "SourceOutput@Dhaka", startNodeData.lrp, lanes)
					else:
						road = SimioLink(startNodeData.road, objects[-1].lrp, startNodeData.lrp, lanes)
					links.append(road)

					for vertexData in tempVertexData:
						vertices.append(SimioVertex(road.linkName, Location(vertexData.lat, vertexData.lon)))
					tempVertexData = []
				else :
					(bridgeStart, bridgeEnd, bridgeLink) = self.buildBridge(startNodeData, dataPoint, lanes)
					objects.append(bridgeStart)
					objects.append(bridgeEnd)
					links.append(bridgeLink)
					self.bridgeCount += 1
			else:
				tempVertexData.append(dataPoint)

		sink = self.buildChittagong(self.endData)

		lastLink = EndSimioLink(self.endData.road, objects[-1].lrp, "Input@N1_End", self.trafficData[len(self.trafficData)-1].numberLanes)
		links.append(lastLink)
		objects.append(sink)

		print('Added {} bridges with {} category UK.'.format(self.bridgeCount,self.categoryECount))

		return (objects, links, vertices)

	def buildChittagong(self, dataPoint):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		return ChittagongObject(location, "N1_End")

	def buildDhaka(self, dataPoint, trafficData):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		interarrivalTime = 5
		return DhakaObject(location, "Dhaka", trafficData.leftTraffic)

	def buildBridge(self, startNodeData, endNodeData, numberLanes):
		bridgeStartLocation = Location(startNodeData.lat, startNodeData.lon)
		bridgeEndLocation = Location(endNodeData.lat, endNodeData.lon)
		length = bridgeStartLocation.distanceTo(bridgeEndLocation)
		bridge = self.index.find(startNodeData.lrp)

		if bridge is not None:
			condition = bridge.condition
		else:
			self.categoryECount += 1
			condition = "UK"

		bridgeStart = BridgeObject(startNodeData.road, bridgeStartLocation, startNodeData.lrp, condition, length)
		bridgeEnd = EndBridgeObject(endNodeData.road, bridgeEndLocation, endNodeData.lrp, condition, length)
		bridgeLink = SimioBridgeLink(startNodeData.road, startNodeData.lrp, endNodeData.lrp, numberLanes)

		return (bridgeStart, bridgeEnd, bridgeLink)
