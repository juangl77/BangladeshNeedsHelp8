from bisect import bisect_right
from DataReader import BridgeData
from operator import itemgetter

import pandas

class BridgeIndexer():
	def __init__(self, bridgeData):
		bridgeData.sort( key=lambda x:x.constructionYear, reverse=True )
		bridgeData.sort( key=lambda x:x.lrp )
		self.bridgeData = bridgeData
		self.matchedBridges = []

	def find(self, lrp):
		for bridge in self.bridgeData:
			if bridge.lrp[:-1] == lrp[:-1]:
				if not bridge.matched:
					bridge.matched = True
					return bridge

		return None

	def addBridgeToData(self, bridgeNodeData, length, category):
		newBridge = BridgeData({
			'road':bridgeNodeData.road,
			'lrp':bridgeNodeData.lrp,
			'length':length,
			'category':category,
			'lat':bridgeNodeData.lat,
			'lon':bridgeNodeData.lon,
			'constructionYear':'-1',
		})
		self.bridgeData.append(newBridge)
		self.matchedBridges.append(newBridge)

	def saveUpdatedBridgeData(self):
		bridge_dicts = [bridge.toDict() for bridge in self.matchedBridges]
		df = pandas.DataFrame(bridge_dicts)
		df.to_csv('data/matched_bridges.csv')
