from math import sqrt, pow

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
		return sqrt(pow(dx,2) + pow(dy,2) + pow(dz,2))

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_number(columnMapping["X"].format(index), self.x)
		worksheet.write_number(columnMapping["Y"].format(index), self.y)
		worksheet.write_number(columnMapping["Z"].format(index), self.z)