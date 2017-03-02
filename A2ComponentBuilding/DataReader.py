import os
import csv

class BridgeData():
	def __init__(self, row):
		self.road = row['road']
		self.lrp = row['LRPName']
		self.length = row['length']
		self.condition = row['condition']
		self.lat = row['lat']
		self.lon = row['lon']

	def __lt__(self, other):
		return self.lrp < other.lrp

class RoadData():
	def __init__(self, row):
		self.road = row['road']
		self.lrp = row['lrp']
		self.gap = row['gap']
		self.lat = float(row['lat'])
		self.lon = float(row['lon'])

	def hasGap(self):
		return self.gap != ''

	def bridgeName(self):
		return self.road + "_" + self.lrp

class DataReader():
	def __init__(self, bridgeDataPath, roadDataPath):
		self.bridgeDataPath = bridgeDataPath
		self.roadDataPath = roadDataPath

	def readBridges(self):
		bridges = []

		with open(self.bridgeDataPath) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				bridges.append(BridgeData(row))
		return bridges

	def readRoads(self):
		roads = []

		with open(self.roadDataPath) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				roads.append(RoadData(row))
		return roads