from bisect import bisect_right
from DataReader import BridgeData
from operator import itemgetter

import pandas

class BridgeIndexer():
	def __init__(self, bridgeData):
		bridgeData.sort( key=lambda x:x.constructionYear, reverse=True )
		bridgeData.sort( key=lambda x:x.lrp )
		self.bridgeData = bridgeData

	def find(self, lrp):
		for bridge in self.bridgeData:
			if bridge.lrp[:-1] == lrp[:-1]:
				if not bridge.matched:
					bridge.matched = True
					return bridge

		return None

	def addBridgeToData(self, bridgeNodeData, length, condition):
		newBridge = BridgeData({
			'road':bridgeNodeData.road,
			'lrp':bridgeNodeData.lrp,
			'length':length,
			'condition':condition,
			'lat':bridgeNodeData.lat,
			'lon':bridgeNodeData.lon,
			'constructionYear':'',
		})
		self.bridgeData.append(newBridge)

	def saveUpdatedBridgeData(self):
		bridge_dicts = [bridge.toDict() for bridge in self.bridgeData]
		df = pandas.DataFrame(bridge_dicts)
		df.to_csv('data/updated_bridge.csv')
