class BaseSimioLink(object):
	def __init__(self):
		self.linkClass = "RoadPath"
		self.network = "RoadNetwork"
		self.directionType = "Unidirectional"
		self.drawnToScale = "True"
		self.allowPassing = "False"

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Link Class"].format(index), self.linkClass)
		worksheet.write_string(columnMapping["Link Name"].format(index), self.linkName)
		worksheet.write_string(columnMapping["From Node"].format(index), self.fromNode)
		worksheet.write_string(columnMapping["To Node"].format(index), self.toNode)
		worksheet.write_string(columnMapping["Network"].format(index), self.network)
		worksheet.write_string(columnMapping["Type"].format(index), self.directionType)
		worksheet.write_string(columnMapping["DrawnToScale"].format(index), self.drawnToScale)
		worksheet.write_string(columnMapping["AllowPassing"].format(index), self.allowPassing)

class SimioLink(BaseSimioLink):
	def __init__(self, road, startLRP, endLRP):
		BaseSimioLink.__init__(self)
		self.linkName = road+"_"+startLRP+"_"+endLRP
		self.fromNode = road+"_"+startLRP
		self.toNode = road+"_"+endLRP

class SimioBridgeLink(BaseSimioLink):
	def __init__(self, road, startLRP, endLRP):
		BaseSimioLink.__init__(self)
		# self.linkClass = "BridgePath"
		self.linkName = "bridge_"+road+"_"+startLRP+"_"+endLRP
		self.fromNode = road+"_"+startLRP
		self.toNode = road+"_"+endLRP

class MidPathSourcesLink(BaseSimioLink):
	def __init__(self, road, startLRP, endLRP):
		BaseSimioLink.__init__(self)
		self.linkName = road+"_"+startLRP+"_"+endLRP
		self.fromNode = startLRP
		self.toNode = road+"_"+endLRP
		self.drawnToScale = "False"

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(MidPathSourcesLink, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["LogicalLength"].format(index), 0)

class MidPathSinksLink(BaseSimioLink):
	def __init__(self, road, startLRP, endLRP):
		BaseSimioLink.__init__(self)
		self.linkName = road+"_"+startLRP+"_"+endLRP
		self.fromNode = road+"_"+startLRP
		self.toNode = endLRP
		self.drawnToScale = "False"

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(MidPathSinksLink, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["LogicalLength"].format(index), 0)

class StartSimioLink(BaseSimioLink):
	def __init__(self, road, fromNode, lrp):
		BaseSimioLink.__init__(self)
		self.linkName = road+"_"+fromNode+"_"+lrp
		self.fromNode = fromNode
		self.toNode = road+"_"+lrp

class EndSimioLink(BaseSimioLink):
	def __init__(self, road, lrp, toNode):
		BaseSimioLink.__init__(self)
		self.linkName = road+"_"+lrp+"_"+toNode
		self.fromNode = road+"_"+lrp
		self.toNode = toNode
