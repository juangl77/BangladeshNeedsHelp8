from bisect import bisect_right

class BridgeIndexer():
	def __init__(self, bridgeData):
		self.bridgeData = bridgeData

	def find(self, lrp):
		i = bisect_right(self.bridgeData, lrp)
		if i:
			return self.bridgeData[i-1]
		raise ValueError