class SimioVertex(object):
	def __init__(self, vertexName, location):
		self.vertexClass = "RoadLRP"
		self.vertexName = vertexName
		self.location = location

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Object Class"].format(index), self.vertexClass)
		worksheet.write_string(columnMapping["Object Name"].format(index), self.vertexName)

		self.location.writeToWorksheet(worksheet, columnMapping, index)