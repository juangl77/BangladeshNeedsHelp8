import os
import csv

class BridgeData():
	def __init__(self, row):
		self.road = row['road']
		self.lrp = row['LRPName'].strip().upper()
		self.length = row['length']
		self.condition = row['condition']
		self.lat = row['lat']
		self.lon = row['lon']
		self.constructionYear = row['constructionYear']
		self.matched = False

	def __lt__(self, other):
		return self.lrp < other.lrp

	def bridgeComplete(self):
		return self.constructionYear != ''

	def toDict(self):
		return {
			'road':self.road,
			'lrp':self.lrp,
			'length':self.length,
			'condition':self.condition,
			'lat':self.lat,
			'lon':self.lon,
			'constructionYear':self.constructionYear
		}

	def fromDict(row):
		return BridgeData(row)

class RoadData():
	def __init__(self, row):
		self.road = row['road']
		self.lrp = row['lrp'].strip().upper()
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
