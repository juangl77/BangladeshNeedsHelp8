import pandas
import numpy

df = pandas.read_csv('data/bridges_n1.csv')
df.columns = df.columns.str.replace('LRPName','lrp')
df['duplicated']=df.duplicated(['lrp'],keep=False)
df['keep'] = -df.duplicated(['lrp'],keep=False)

for lrp, group in df[df['duplicated']].groupby('lrp'):
    empty = group[group['constructionYear'] == numpy.nan]
    if len(empty)<len(group):
        group = group[group['constructionYear'] != numpy.nan]

    df.ix[group.index.get_level_values(0).values[0],'keep'] = True

cleaned = df[df['keep']]

cleaned.to_csv('data/bridges_n1_nodup.csv')
