class SimioObject(object):
	def __init__(self, objectClass, objectName, location):
		self.objectClass = objectClass
		self.objectName = objectName
		self.location = location

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Object Class"].format(index), self.objectClass)
		worksheet.write_string(columnMapping["Object Name"].format(index), self.objectName)
		
		self.location.writeToWorksheet(worksheet, columnMapping, index)

class TruckObject(SimioObject):
	conversionConstant = 1000.0 / 3600.0

	def __init__(self, location, desiredSpeedKPH):
		SimioObject.__init__(self, "TruckEntity", "Truck", location)
		self.initialDesiredSpeed = desiredSpeedKPH * self.conversionConstant

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(TruckObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["InitialDesiredSpeed"].format(index), self.initialDesiredSpeed)

class ChittagongObject(SimioObject):
	def __init__(self, location, interarrivalTime, entityType = "Truck"):
		SimioObject.__init__(self, "Source", "Chittagong", location)
		self.interarrivalTime = interarrivalTime
		self.entityType = entityType

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(ChittagongObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["InterarrivalTime"].format(index), self.interarrivalTime)
		worksheet.write_string(columnMapping["EntityType"].format(index), self.entityType)

class DhakaObject(SimioObject):
	def __init__(self, location):
		SimioObject.__init__(self, "Sink", "Dhaka", location)

class BridgeObject(SimioObject):
	def __init__(self, name, location, category, length):
		SimioObject.__init__(self, "Bridge", name, location)
		self.category = category
		self.length = length
		self.initialTravelerCapacity = "SmallBridgeCapacity" if length < 50 else "LargeBridgeCapacity"
		self.reportStatistics = "True"

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(BridgeObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_string(columnMapping["Category"].format(index), self.category)
		worksheet.write_number(columnMapping["Length"].format(index), self.length)
		worksheet.write_string(columnMapping["InitialTravelerCapacity"].format(index), self.initialTravelerCapacity)
		worksheet.write_string(columnMapping["ReportStatistics"].format(index), self.reportStatistics)
