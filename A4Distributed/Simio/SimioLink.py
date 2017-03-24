class BaseSimioLink(object):
	def __init__(self, numberLanes):
		self.linkClass = "RoadPath"
		self.network = "RoadNetwork"
		self.directionType = "Unidirectional"
		self.drawnToScale = "True"
		self.allowPassing = "False"
		self.numberLanes = numberLanes

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Link Class"].format(index), self.linkClass)
		worksheet.write_string(columnMapping["Link Name"].format(index), self.linkName)
		worksheet.write_string(columnMapping["From Node"].format(index), self.fromNode)
		worksheet.write_string(columnMapping["To Node"].format(index), self.toNode)
		worksheet.write_string(columnMapping["Network"].format(index), self.network)
		worksheet.write_string(columnMapping["Type"].format(index), self.directionType)
		worksheet.write_string(columnMapping["DrawnToScale"].format(index), self.drawnToScale)
		worksheet.write_string(columnMapping["AllowPassing"].format(index), self.allowPassing)
		worksheet.write_number(columnMapping["NumberLanes"].format(index), self.numberLanes)

class SimioLink(BaseSimioLink):
	def __init__(self, road, startLRP, endLRP, numberLanes):
		BaseSimioLink.__init__(self, numberLanes)
		self.linkName = road+"_"+startLRP+"_"+endLRP
		self.fromNode = road+"_"+startLRP
		self.toNode = road+"_"+endLRP

class SimioBridgeLink(BaseSimioLink):
	def __init__(self, road, startLRP, endLRP, numberLanes):
		BaseSimioLink.__init__(self, numberLanes)
		self.linkClass = "BridgePath"
		self.linkName = "bridge_"+road+"_"+startLRP+"_"+endLRP
		self.fromNode = road+"_"+startLRP
		self.toNode = road+"_"+endLRP

class StartSimioLink(BaseSimioLink):
	def __init__(self, road, fromNode, lrp, numberLanes):
		BaseSimioLink.__init__(self, numberLanes)
		self.linkName = road+"_"+fromNode+"_"+lrp
		self.fromNode = fromNode
		self.toNode = road+"_"+lrp

class EndSimioLink(BaseSimioLink):
	def __init__(self, road, lrp, toNode, numberLanes):
		BaseSimioLink.__init__(self, numberLanes)
		self.linkName = road+"_"+lrp+"_"+toNode
		self.fromNode = road+"_"+lrp
		self.toNode = toNode
