import csv
import shapefile

class Coordinate():
	
 def __init__(self,lat,lon):
  self.lat = float(lat)
  self.lon = float(lon)

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
  
class Boundary():
 def __init__(self,filename):
  self.box = shapefile.Reader(filename).shapes()[0].bbox
  
 def inside(self,coordinate):
  return ((coordinate.lat >= self.box[1] and coordinate.lat <= self.box[3]) and (coordinate.lon >= self.box[0] and coordinate.lon <= self.box[2]))

def readBridges():
 rows = []

 with open('../BMMS/CSV/_allBridges.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
   rows.append(Row(row))

 return rows
 
def writeBridges(rows,filename):
 with open(filename, 'w') as fixed_csvfile:
  fieldnames = ['Number','Structure Name','Condition of Bridge', 'TotalWidth','TotalLength','ConstructionYear',
   'NumberOfSpan','Zone','Circle','Division','Sub-Division','RoadNo','BridgeNo','StructureLRPName','ReferenceLRPNo','LocationLRPOffset',
   'LocationChainage','Latitude','Longitude']
  writer = csv.DictWriter(fixed_csvfile, fieldnames = fieldnames, dialect='excel')
  writer.writeheader()
  for row in rows:
   writer.writerow(row.data)
   
def readRoads():
 rows = []

 with open('../RMMS/CSV/_allRoads.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
   rows.append(Row(row))

 return rows  
 
def writeRoads(rows,filename):
 with open(filename, 'w') as fixed_csvfile:
  fieldnames = ['Road Id','LRP Number','Road Chainage','Type','Desc','Latitude','Longitude']
  writer = csv.DictWriter(fixed_csvfile, fieldnames = fieldnames, dialect='excel')
  writer.writeheader()
  for row in rows:
   writer.writerow(row.data)
 
def fixBridges():
 rows = readBridges()		
 new_rows = map(lambda r: r.fix(), rows)
 writeBridges(new_rows,'../BMMS/CSV/_allBridges_fixed.csv')

def fixRoads():
 rows = readRoads()		
 new_rows = map(lambda r: r.fix(), rows)
 writeRoads(new_rows,'../RMMS/CSV/_allRoads_fixed.csv')

def boundCheckBridges():
 bound = Boundary('../WBSIM/gis/gadm/BGD_adm0.shp')
 rows = readBridges()
 new_rows = filter(lambda r: bound.inside(r.coor), rows)
 writeBridges(new_rows,'../BMMS/CSV/_allBridges_final.csv')
 
def boundCheckRoads():
 bound = Boundary('../WBSIM/gis/gadm/BGD_adm0.shp')
 rows = readRoads()
 new_rows = filter(lambda r: bound.inside(r.coor), rows)
 writeRoads(new_rows,'../RMMS/CSV/_allRoads_final.csv')