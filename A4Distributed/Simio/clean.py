import pandas

df = pandas.from_csv('data/bridges_n1.csv')
df['duplicated']=df.duplicated(['lrp'],keep=False)
df['keep'] = -df.duplicated(['lrp'],keep=False)

for lrp, group in df[df['duplicated']].groupby('lrp'):
	empty = group[group['constructionYear'] == '']
	if len(empty)<len(group):
		group = group[group['constructionYear'] != '']

	df.ix[group.index.get_level_values(0).values[0],'keep'] = True

cleaned = df[df['keep']]
cleaned.columns = cleaned.columns.str.replace('lrp','LRPName')
newData = []
for row in cleaned.to_dict(orient='records'):
	newData.append(BridgeData(row))

df.to('data/bridges_n1_nodup.csv')
