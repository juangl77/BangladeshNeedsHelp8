import csv


class Coordinate():
 lat = 0
 lon = 0
	
 def __init__(self,lat,lon):
  self.lat = lat
  self.lon = lon

 def __str__(self):
  return "("+str(self.lat)+", "+str(self.lon)+")"
	
 def fix(self):
  if self.lon > self.lat:
   return Coordinate(self.lat,self.lon)
  else:
   return Coordinate(self.lon,self.lat)

class Row():
 def __init__(self,row):
  self.coor = Coordinate(row['Latitude'],row['Longitude'])
  self.data = row
 def fix(self):
  fixed_coor = self.coor.fix()
  fixed_data = self.data
  fixed_data['Latitude'] = fixed_coor.lat
  fixed_data['Longitude'] = fixed_coor.lon
  return Row(fixed_data)
  
			

rows = []

with open('../BMMS/CSV/_allBridges.csv') as csvfile:
 reader = csv.DictReader(csvfile)
 for row in reader:
  rows.append(Row(row))

print(len(rows))
		
new_rows = map(lambda r: r.fix(), rows)

with open('../BMMS/CSV/_allBridges_fixed.csv', 'w') as fixed_csvfile:
 fieldnames = ['Number','Structure Name','Condition of Bridge', 'TotalWidth','TotalLength','ConstructionYear',
  'NumberOfSpan','Zone','Circle','Division','Sub-Division','RoadNo','BridgeNo','StructureLRPName','ReferenceLRPNo','LocationLRPOffset',
  'LocationChainage','Latitude','Longitude']
 writer = csv.DictWriter(fixed_csvfile, fieldnames = fieldnames, dialect='excel')
 writer.writeheader()
 for row in new_rows:
  writer.writerow(row.data)



