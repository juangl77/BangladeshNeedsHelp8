from math import sqrt, pow

class Location():
	def __init__(self, lat, lon):
		self.x = lon
		self.y = 0
		self.z = -lat

	def distanceTo(self, location):
		dx = (location.x - self.x) * 102
		dy = (location.y - self.y)
		dz = (location.z - self.z) * 111
		return int(sqrt(pow(dx,2) + pow(dy,2) + pow(dz,2)) * 1000)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_number(columnMapping["X"].format(index), self.x)
		worksheet.write_number(columnMapping["Y"].format(index), self.y)
		worksheet.write_number(columnMapping["Z"].format(index), self.z)