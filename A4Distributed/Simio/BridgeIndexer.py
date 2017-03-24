from bisect import bisect_right
from DataReader import BridgeData

import pandas

class BridgeIndexer():
	def __init__(self, bridgeData):
		self.bridgeData = bridgeData

	def find(self, lrp):
		for bridge in self.bridgeData:
			if bridge.lrp[:-1] == lrp[:-1] and bridge.bridgeComplete():
				if not bridge.matched:
					bridge.matched = True
					return bridge

		return None
