from bisect import bisect_right
from DataReader import BridgeData

import pandas

class BridgeIndexer():
	def __init__(self, bridgeData):
		self.bridgeData = bridgeData

	# def cleanDuplicates(self):
	# 	df = pandas.DataFrame.from_records([bridge.toDict() for bridge in self.bridgeData])
	# 	df['duplicated']=df.duplicated(['lrp'],keep=False)
	# 	df['keep'] = -df.duplicated(['lrp'],keep=False)
	#
	# 	for lrp, group in df[df['duplicated']].groupby('lrp'):
	# 		empty = group[group['constructionYear'] == '']
	# 		if len(empty)<len(group):
	# 			group = group[group['constructionYear'] != '']
	#
	# 		df.ix[group.index.get_level_values(0).values[0],'keep'] = True
	#
	# 	cleaned = df[df['keep']]
	# 	cleaned.columns = cleaned.columns.str.replace('lrp','LRPName')
	# 	newData = []
	# 	for row in cleaned.to_dict(orient='records'):
	# 		newData.append(BridgeData(row))
	#
	# 	self.bridgeData = newData

	def find(self, lrp):
		for bridge in self.bridgeData:
			if bridge.lrp[:-1] == lrp[:-1] and bridge.bridgeComplete():
				if not bridge.matched:
					bridge.matched = True
					return bridge

		return None
