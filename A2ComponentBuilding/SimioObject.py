class SimioObject(object):
	def __init__(self, objectClass, objectName, location, lrp = ""):
		self.objectClass = objectClass
		self.objectName = objectName
		self.location = location
		self.lrp = lrp

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
	def __init__(self, location, lrp):
		SimioObject.__init__(self, "Sink", "Chittagong", location, lrp)
		
class DhakaObject(SimioObject):
	def __init__(self, location, lrp, interarrivalTime, entityType = "Truck"):
		SimioObject.__init__(self, "Source", "Dhaka", location, lrp)
		self.interarrivalTime = interarrivalTime
		self.entityType = entityType

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(DhakaObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["InterarrivalTime"].format(index), self.interarrivalTime)
		worksheet.write_string(columnMapping["EntityType"].format(index), self.entityType)

class BridgeObject(SimioObject):
	def __init__(self, road, location, lrp, category, length):
		SimioObject.__init__(self, "Bridge", road+"_"+lrp, location, lrp)
		self.category = category
		self.length = length
		self.initialTravelerCapacity = "SmallBridgeCapacity" if length < 50 else "LargeBridgeCapacity"
		self.runInitializedAddOnProcess = "SetBridgeState_"+category
		self.reportStatistics = "True"

	def chooseInitializedAddOnProcess(self, length):
		if length < 10:
			return "DelayShortBridge"
		elif length < 50:
			return "DelayMediumBridge"
		elif length < 200:
			return "DelayLongBridge"
		else:
			return "DelayExtraLongBridge"

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(BridgeObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_string(columnMapping["Category"].format(index), self.category)
		worksheet.write_number(columnMapping["Length"].format(index), self.length)
		worksheet.write_string(columnMapping["InitialTravelerCapacity"].format(index), self.initialTravelerCapacity)
		worksheet.write_string(columnMapping["RunInitializedAddOnProcess"].format(index), self.runInitializedAddOnProcess)
		worksheet.write_string(columnMapping["ReportStatistics"].format(index), self.reportStatistics)

class EndBridgeObject(BridgeObject):
	def __init__(self, road, location, lrp, category, length):
		BridgeObject.__init__(self, road, location, lrp, category, length)
		self.enteringAddOnProcess = self.chooseInitializedAddOnProcess(length)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(EndBridgeObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_string(columnMapping["EnteredAddOnProcess"].format(index), self.enteringAddOnProcess)