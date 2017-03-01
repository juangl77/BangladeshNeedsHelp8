class Location():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_number(columnMapping["X"].format(index), self.x)
		worksheet.write_number(columnMapping["Y"].format(index), self.y)
		worksheet.write_number(columnMapping["Z"].format(index), self.z)