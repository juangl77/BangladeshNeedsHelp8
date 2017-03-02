from bisect import bisect_right
from DataReader import BridgeData

class BridgeIndexer():
	def __init__(self, bridgeData):
		self.bridgeData = bridgeData

	def find(self, lrp):
		dummyBridge = BridgeData({
			"road" : "",
			"LRPName" : lrp,
			"length": "",
			"condition": "",
			"lat" : "",
			"lon" : ""
		})

		i = bisect_right(self.bridgeData, dummyBridge)
		if i:
			return self.bridgeData[i-1]
		raise ValueError