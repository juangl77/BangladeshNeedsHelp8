from bisect import bisect_right
from DataReader import BridgeData

import pandas

class BridgeIndexer():
	def __init__(self, bridgeData):
		self.bridgeData = bridgeData

	def cleanDuplicates(self):
		df = pandas.DataFrame.from_records([bridge.toDict() for bridge in self.bridgeData])
		df['duplicated']=df.duplicated(['lrp'],keep=False)
		cleaned = df[-df['duplicated']]

		for lrp, group in df[df['duplicated']].groupby('lrp'):
			empty = group[group['constructionYear'] == '']
			if len(empty)<len(group):
				group = group[group['constructionYear'] != '']
			if (len(group) > 1):
				group = group.iloc[0]
			cleaned.append(group)

		cleaned.columns = cleaned.columns.str.replace('lrp','LRPName')
		newData = []
		for row in cleaned.to_dict(orient='records'):
			newData.append(BridgeData(row))

		self.bridgeData = newData

	def find(self, lrp):
		dummyBridge = BridgeData({
			"road" : "",
			"LRPName" : lrp,
			"length": "",
			"condition": "",
			"lat" : "",
			"lon" : "",
			"constructionYear":""
		})

		i = bisect_right(self.bridgeData, dummyBridge)
		if i:
			return self.bridgeData[i-1]
		raise ValueError
