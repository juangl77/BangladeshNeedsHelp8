import csv
import shapefile #pip install pyshp

import ReadWriteCSV
import Constants

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
  self.coor = Coordinate(row[Constants.lat],row[Constants.lon])
  self.data = row

 def fix(self):
  fixed_coor = self.coor.fix()
  fixed_data = self.data
  fixed_data[Constants.lat] = fixed_coor.lat
  fixed_data[Constants.lon] = fixed_coor.lon
  return Row(fixed_data)

class Boundary():
 def __init__(self,filename):
  self.box = shapefile.Reader(filename).shapes()[0].bbox

 def inside(self,coordinate):
  return ((coordinate.lat >= self.box[1] and coordinate.lat <= self.box[3]) and (coordinate.lon >= self.box[0] and coordinate.lon <= self.box[2]))

def buildRows(rows):
	return [Row(row) for row in rows]

def fixBridges():
 rows = buildRows(ReadWriteCSV.readBridges())

 new_rows = map(lambda r: r.fix(), rows)
 ReadWriteCSV.writeBridges(new_rows,'../BMMS/CSV/_allBridges_fixed.csv')

def fixRoads():
 rows = buildRows(ReadWriteCSV.readRoads())
 new_rows = map(lambda r: r.fix(), rows)
 ReadWriteCSV.writeRoads(new_rows,'../RMMS/CSV/_allRoads_fixed.csv')

def boundCheckBridges():
 bound = Boundary('../WBSIM/gis/gadm/BGD_adm0.shp')
 rows = buildRows(ReadWriteCSV.readBridges())
 new_rows = filter(lambda r: bound.inside(r.coor), rows)
 ReadWriteCSV.writeBridges(new_rows,'../BMMS/CSV/_allBridges_final.csv')

def boundCheckRoads():
 bound = Boundary('../WBSIM/gis/gadm/BGD_adm0.shp')
 rows = buildRows(ReadWriteCSV.readRoads())
 new_rows = filter(lambda r: bound.inside(r.coor), rows)
 ReadWriteCSV.writeRoads(new_rows,'../RMMS/CSV/_allRoads_final.csv')
