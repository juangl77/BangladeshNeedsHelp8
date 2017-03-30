from SimioObject import TruckObject, BusObject, PassengerVehicleObject, ChittagongObject, DhakaObject, BridgeObject, EndBridgeObject, \
						MidPathSourcesObject, MidPathSinksObject
from SimioLink import SimioLink, StartSimioLink, EndSimioLink, SimioBridgeLink, MidPathSourcesLink, MidPathSinksLink
from SimioVertex import SimioVertex
from Location import Location

from math import ceil
import numpy

from BridgeIndexer import BridgeIndexer
from DataReader import RoadData, BridgeData, TrafficData, Traffic

class DataBuilder():
<<<<<<< HEAD
<<<<<<< HEAD
	scalingFactor = 100 # TODO experiment with this number
=======
	scalingFactor = 1 # TODO experiment with this number
>>>>>>> 8607025440f53989a931ff7daab06d7ddee1e71b
=======
	scalingFactor = 1 # TODO experiment with this number
>>>>>>> a55fd8e90ff598b946e83e692c8aff999543845a
	trafficChangeThreshold = 0.1

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

		traffics = []
		starts = []
		ends = []
		objects = []

		objects.append(self.buildDhaka(self.startData, self.trafficData[0]))

		currentTrafficIndex = 0
		for dataPoint in self.roadData:
			if dataPoint.hasGap():
				#Go to the first width entry where the end chainage is greater than the current datapoint's chainage
				originalTrafficIndex = currentTrafficIndex
				while(dataPoint.chainage > self.trafficData[currentTrafficIndex].endChainage):
					currentTrafficIndex += 1

				#if traffic chainage index has changed, source or sink needs to be incorporated here
				(busChange, passengerChange, truckChange) = (False, False, False)
				trafficChange = Traffic()
				if originalTrafficIndex != currentTrafficIndex :
					originalTraffic = self.trafficData[originalTrafficIndex]
					newTraffic = self.trafficData[currentTrafficIndex]
<<<<<<< HEAD
<<<<<<< HEAD
=======
					#print(dataPoint.lrp)
>>>>>>> a55fd8e90ff598b946e83e692c8aff999543845a
					if abs(originalTraffic.leftTraffic.bus-newTraffic.leftTraffic.bus) > self.trafficChangeThreshold*originalTraffic.leftTraffic.bus:
						#print('Bus change in traffic {} -> {}'.format(originalTraffic.leftTraffic.bus,newTraffic.leftTraffic.bus))
						busChange = True
						trafficChange.bus = newTraffic.leftTraffic.bus-originalTraffic.leftTraffic.bus
					if abs(originalTraffic.leftTraffic.truck-newTraffic.leftTraffic.truck) > self.trafficChangeThreshold*originalTraffic.leftTraffic.truck:
						#print('Truck change in traffic {} -> {}'.format(originalTraffic.leftTraffic.truck,newTraffic.leftTraffic.truck))
						truckChange = True
						trafficChange.truck = newTraffic.leftTraffic.truck-originalTraffic.leftTraffic.truck
					if abs(originalTraffic.leftTraffic.passenger-newTraffic.leftTraffic.passenger) > self.trafficChangeThreshold*originalTraffic.leftTraffic.passenger:
						#print('Passenger change in traffic {} -> {}'.format(originalTraffic.leftTraffic.passenger,newTraffic.leftTraffic.passenger))
						passengerChange = True
						trafficChange.passenger = newTraffic.leftTraffic.passenger-originalTraffic.leftTraffic.passenger
<<<<<<< HEAD
=======
					print(dataPoint.lrp)
					if abs(originalTraffic.leftTraffic.bus-newTraffic.leftTraffic.bus) > self.trafficChangeThreshold*originalTraffic.leftTraffic.bus:
						print('Bus change in traffic {} -> {}'.format(originalTraffic.leftTraffic.bus,newTraffic.leftTraffic.bus))
						busChange = True
						trafficChange.bus = newTraffic.leftTraffic.bus-originalTraffic.leftTraffic.bus
					if abs(originalTraffic.leftTraffic.truck-newTraffic.leftTraffic.truck) > self.trafficChangeThreshold*originalTraffic.leftTraffic.truck:
						print('Truck change in traffic {} -> {}'.format(originalTraffic.leftTraffic.truck,newTraffic.leftTraffic.truck))
						truckChange = True
						trafficChange.truck = newTraffic.leftTraffic.truck-originalTraffic.leftTraffic.truck
					if abs(originalTraffic.leftTraffic.passenger-newTraffic.leftTraffic.passenger) > self.trafficChangeThreshold*originalTraffic.leftTraffic.passenger:
						print('Passenger change in traffic {} -> {}'.format(originalTraffic.leftTraffic.passenger,newTraffic.leftTraffic.passenger))
						passengerChange = True
						trafficChange.passenger = newTraffic.leftTraffic.passenger-originalTraffic.leftTraffic.passenger
					print()
>>>>>>> 8607025440f53989a931ff7daab06d7ddee1e71b
=======
					#print()
>>>>>>> a55fd8e90ff598b946e83e692c8aff999543845a

				if dataPoint.gap == "BS":
					startNodeData = dataPoint
					if len(links) == 0:
						road = StartSimioLink(startNodeData.road, "SourceOutput@Dhaka", startNodeData.lrp)
					else:
						road = SimioLink(startNodeData.road, ends[-1].lrp, startNodeData.lrp)
					links.append(road)

					for vertexData in tempVertexData:
						vertices.append(SimioVertex(road.linkName, Location(vertexData.lat, vertexData.lon)))
					tempVertexData = []

					trafficNode = self.buildTempBridgeStart(startNodeData)
					starts.append(trafficNode)

				else:
					(bridgeStart, bridgeEnd, bridgeLink) = self.buildBridge(startNodeData, dataPoint)

					bridgeStart.hasSink = starts[-1].hasSink
					bridgeStart.percentTruckTrafficToDestroy = starts[-1].percentTruckTrafficToDestroy
					bridgeStart.percentBusTrafficToDestroy = starts[-1].percentBusTrafficToDestroy
					bridgeStart.percentPassengerTrafficToDestroy = starts[-1].percentPassengerTrafficToDestroy
					starts[-1] = bridgeStart

					ends.append(bridgeEnd)
					links.append(bridgeLink)
					self.bridgeCount += 1

					trafficNode = bridgeEnd

				if busChange or passengerChange or truckChange:
					(obj, link, hasSink) = self.buildTrafficChangePoint(trafficNode,trafficChange)

					if hasSink:
						if type(trafficNode) is BridgeObject:
							starts[-1].hasSink = hasSink
							if trafficChange.truck < 0:
								starts[-1].percentTruckTrafficToDestroy = abs(trafficChange.truck)/originalTraffic.leftTraffic.truck
							if trafficChange.bus < 0:
								starts[-1].percentBusTrafficToDestroy = abs(trafficChange.bus)/originalTraffic.leftTraffic.bus
							if trafficChange.passenger < 0:
								starts[-1].percentPassengerTrafficToDestroy = abs(trafficChange.passenger)/originalTraffic.leftTraffic.passenger
						elif type(trafficNode) is EndBridgeObject:
							ends[-1].hasSink = hasSink
							if trafficChange.truck < 0:
								ends[-1].percentTruckTrafficToDestroy = abs(trafficChange.truck)/originalTraffic.leftTraffic.truck
							if trafficChange.bus < 0:
								ends[-1].percentBusTrafficToDestroy = abs(trafficChange.bus)/originalTraffic.leftTraffic.bus
							if trafficChange.passenger < 0:
								ends[-1].percentPassengerTrafficToDestroy = abs(trafficChange.passenger)/originalTraffic.leftTraffic.passenger

					traffics.append(obj)
					links.append(link)

			else:
				tempVertexData.append(dataPoint)

		sink = self.buildChittagong(self.endData)

		lastLink = EndSimioLink(self.endData.road, ends[-1].lrp, "Input@N1_End")
		links.append(lastLink)
		objects.append(sink)

		objects.extend(traffics)
		objects.extend(starts)
		objects.extend(ends)

		print('Added {} bridges with {} bridges not matched.'.format(self.bridgeCount,self.categoryECount))

		#self.index.saveUpdatedBridgeData() MATCH

		return (objects, links, vertices)

	def buildChittagong(self, dataPoint):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		return ChittagongObject(location, "N1_End")

	def buildDhaka(self, dataPoint, trafficData):
		location = Location(dataPoint.lat, dataPoint.lon)
		lrp = dataPoint.lrp
		interarrivalTime = 5
		return DhakaObject(location, "Dhaka", trafficData.leftTraffic, self.scalingFactor)

	def buildTempBridgeStart(self, startNodeData):
		bridgeStartLocation = Location(startNodeData.lat, startNodeData.lon)
		category='TEMP'
		bridgeStart = BridgeObject(startNodeData.road, bridgeStartLocation, startNodeData.lrp, category, -1, -1)
		return bridgeStart

	def buildBridge(self, startNodeData, endNodeData):
		bridgeStartLocation = Location(startNodeData.lat, startNodeData.lon)
		bridgeEndLocation = Location(endNodeData.lat, endNodeData.lon)
		length = bridgeStartLocation.distanceTo(bridgeEndLocation)

		bridge = self.index.find(startNodeData.lrp)
		if bridge is not None:
			category = bridge.category
			#self.index.matchedBridges.append(bridge) #MATCH
		else:
			self.categoryECount += 1
			category = 'E'
			#self.index.addBridgeToData(startNodeData, length, 'E') #MATCH

		bridgeStart = BridgeObject(startNodeData.road, bridgeStartLocation, startNodeData.lrp, category, length, bridge.rowId)
		bridgeEnd = EndBridgeObject(endNodeData.road, bridgeEndLocation, endNodeData.lrp, category, length, bridge.rowId)
		bridgeLink = SimioBridgeLink(startNodeData.road, startNodeData.lrp, endNodeData.lrp)

		return (bridgeStart, bridgeEnd, bridgeLink)

	def buildTrafficChangePoint(self, node, traffic):
		if traffic.truck > 0 or traffic.bus > 0 or traffic.passenger > 0:
			source = MidPathSourcesObject(node, traffic, self.scalingFactor)
			link = MidPathSourcesLink(source.road, 'SourceOutput@'+source.objectName, node.lrp)
			return (source, link, False)
		if traffic.truck < 0 or traffic.bus < 0 or traffic.passenger < 0:
			sink = MidPathSinksObject(node, traffic)
			link = MidPathSinksLink(sink.road, node.lrp, 'Input@'+sink.objectName)
			return (sink, link, True)
