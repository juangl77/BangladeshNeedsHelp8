class SimioVertex(object):
	def __init__(self, link, location):
		self.linkName = link
		self.location = location

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Link Name"].format(index), self.linkName)

		self.location.writeToWorksheet(worksheet, columnMapping, index)