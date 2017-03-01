class BridgeIndexer():
	def __init__(self, bridgeData):
		self.index = {}

		for dataPoint in bridgeData:
			self.index[dataPoint.lrp] = dataPoint