class SimioLink(object):
	def __init__(self, linkName, fromNode, toNode):
		self.linkClass = "Path"
		self.linkName = linkName
		self.fromNode = fromNode
		self.toNode = toNode
		self.network = "RoadNetwork"
		self.directionType = "Unidirectional"
		self.drawnToScale = "True"

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Link Class"].format(index), self.linkClass)
		worksheet.write_string(columnMapping["Link Name"].format(index), self.linkName)
		worksheet.write_string(columnMapping["From Node"].format(index), self.fromNode)
		worksheet.write_string(columnMapping["To Node"].format(index), self.toNode)
		worksheet.write_string(columnMapping["Network"].format(index), self.network)
		worksheet.write_string(columnMapping["Type"].format(index), self.directionType)
		worksheet.write_string(columnMapping["DrawnToScale"].format(index), self.drawnToScale)