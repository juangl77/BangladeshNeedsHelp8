import math

class Centre():
	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon

class Location():
	centre = Centre(23, 90)

	def __init__(self, lat, lon):
		self.x = (lon - self.centre.lon) * 102 * 1000
		self.y = 0
		self.z = -(lat - self.centre.lat) * 111 * 1000

	def distanceTo(self, location):
		dx = (location.x - self.x)
		dy = (location.y - self.y)
		dz = (location.z - self.z)
		return math.sqrt(math.pow(dx,2) + math.pow(dy,2) + math.pow(dz,2))

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_number(columnMapping["X"].format(index), self.x)
		worksheet.write_number(columnMapping["Y"].format(index), self.y)
		worksheet.write_number(columnMapping["Z"].format(index), self.z)

	@staticmethod
	def centerOfSegment(start, end):

		lat1,lon1,lat2,lon2 = map(math.radians, [start.lat,start.lon,end.lat,end.lon])
		dLon = lon2-lon1
    	dLat = lat2-lat1

		bx = math.cos(lat2) * math.cos(dLon)
		by = math.cos(lat2) * math.sin(dLon)

		lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) + bx) + by * by))
		lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

		return Location(math.degrees(lat3),math.degrees(lon3))
