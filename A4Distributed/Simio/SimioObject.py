import Location

class SimioObject(object):
	def __init__(self, objectClass, objectName, location, lrp = '', road = ''):
		self.objectClass = objectClass
		self.objectName = objectName
		self.location = location
		self.lrp = lrp
		self.road = road

	def writeToWorksheet(self, worksheet, columnMapping, index):
		worksheet.write_string(columnMapping["Object Class"].format(index), self.objectClass)
		worksheet.write_string(columnMapping["Object Name"].format(index), self.objectName)

		self.location.writeToWorksheet(worksheet, columnMapping, index)

class VehicleObject(SimioObject):
	conversionConstant = 1000.0 / 3600.0

	def __init__(self, vehicleType, vehicleName, location, desiredSpeedKPH):
		SimioObject.__init__(self, vehicleType, vehicleName, location)
		self.initialDesiredSpeed = desiredSpeedKPH * self.conversionConstant

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(VehicleObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["InitialDesiredSpeed"].format(index), self.initialDesiredSpeed)

class TruckObject(VehicleObject):
	def __init__(self, location, desiredSpeedKPH):
		VehicleObject.__init__(self, "TruckEntity", "Truck", location, desiredSpeedKPH)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(TruckObject, self).writeToWorksheet(worksheet, columnMapping, index)

class BusObject(VehicleObject):
	def __init__(self, location, desiredSpeedKPH):
		VehicleObject.__init__(self, "BusEntity", "Bus", location, desiredSpeedKPH)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(BusObject, self).writeToWorksheet(worksheet, columnMapping, index)

class PassengerVehicleObject(VehicleObject):
	def __init__(self, location, desiredSpeedKPH):
		VehicleObject.__init__(self, "PassengerVehicleEntity", "PassengerVehicle", location, desiredSpeedKPH)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(PassengerVehicleObject, self).writeToWorksheet(worksheet, columnMapping, index)

class ChittagongObject(SimioObject):
	def __init__(self, location, lrp):
		SimioObject.__init__(self, "Sink", "N1_End", location, lrp, 'N1')

class MidPathSinksObject(SimioObject):
	def __init__(self, node, traffic):
		location = node.location
		location.x += 500

		SimioObject.__init__(self, "Sink", "sinks_"+node.road+"_"+node.lrp, location, node.lrp,  node.road)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(MidPathSinksObject, self).writeToWorksheet(worksheet, columnMapping, index)

class SourcesObject(SimioObject):
	def __init__(self, objectClass, objectName, location, lrp, traffic, road, scalingFactor):
		SimioObject.__init__(self, objectClass, objectName, location, lrp, road)
<<<<<<< HEAD
		self.rushInterarrivalTimeTruck = (1.0/(traffic.truck/scalingFactor*traffic.percentageDuringRush))*traffic.numberRushHours
		self.rushInterarrivalTimeBus = (1.0/(traffic.bus/scalingFactor*traffic.percentageDuringRush))*traffic.numberRushHours
		self.rushInterarrivalTimePassenger = (1.0/(traffic.passenger/scalingFactor*traffic.percentageDuringRush))*traffic.numberRushHours

		self.normalInterarrivalTimeTruck = (1.0/(traffic.truck/scalingFactor*(1-traffic.percentageDuringRush)))*(24-traffic.numberRushHours)
		self.normalInterarrivalTimeBus = (1.0/(traffic.bus/scalingFactor*(1-traffic.percentageDuringRush)))*(24-traffic.numberRushHours)
		self.normalInterarrivalTimePassenger = (1.0/(traffic.passenger/scalingFactor*(1-traffic.percentageDuringRush)))*(24-traffic.numberRushHours)
=======
		# self.rushInterarrivalTimeTruck = (1.0/(traffic.truck/scalingFactor*traffic.percentageDuringRush))*traffic.numberRushHours
		# self.rushInterarrivalTimeBus = (1.0/(traffic.bus/scalingFactor*traffic.percentageDuringRush))*traffic.numberRushHours
		# self.rushInterarrivalTimePassenger = (1.0/(traffic.passenger/scalingFactor*traffic.percentageDuringRush))*traffic.numberRushHours
		#
		# self.normalInterarrivalTimeTruck = (1.0/(traffic.truck/scalingFactor*(1-traffic.percentageDuringRush)))*(24-traffic.numberRushHours)
		# self.normalInterarrivalTimeBus = (1.0/(traffic.bus/scalingFactor*(1-traffic.percentageDuringRush)))*(24-traffic.numberRushHours)
		# self.normalInterarrivalTimePassenger = (1.0/(traffic.passenger/scalingFactor*(1-traffic.percentageDuringRush)))*(24-traffic.numberRushHours)

		self.rushInterarrivalTimeTruck = (1.0/(traffic.truck*traffic.percentageDuringRush))/(24/traffic.numberRushHours)
		self.rushInterarrivalTimeBus = (1.0/(traffic.bus*traffic.percentageDuringRush))/(24/traffic.numberRushHours)
		self.rushInterarrivalTimePassenger = (1.0/(traffic.passenger*traffic.percentageDuringRush))/(24/traffic.numberRushHours)

		self.normalInterarrivalTimeTruck = (1.0/(traffic.truck*(1-traffic.percentageDuringRush)))/(24/(24-traffic.numberRushHours))
		self.normalInterarrivalTimeBus = (1.0/(traffic.bus*(1-traffic.percentageDuringRush)))/(24/(24-traffic.numberRushHours))
		self.normalInterarrivalTimePassenger = (1.0/(traffic.passenger*(1-traffic.percentageDuringRush)))/(24/(24-traffic.numberRushHours))
>>>>>>> 8607025440f53989a931ff7daab06d7ddee1e71b

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(SourcesObject, self).writeToWorksheet(worksheet, columnMapping, index)
		worksheet.write_number(columnMapping["RushInterarrivalTimeTruck"].format(index), self.rushInterarrivalTimeTruck)
		worksheet.write_number(columnMapping["RushInterarrivalTimeBus"].format(index), self.rushInterarrivalTimeBus)
		worksheet.write_number(columnMapping["RushInterarrivalTimePassenger"].format(index), self.rushInterarrivalTimePassenger)

		worksheet.write_number(columnMapping["NormalInterarrivalTimeTruck"].format(index), self.normalInterarrivalTimeTruck)
		worksheet.write_number(columnMapping["NormalInterarrivalTimeBus"].format(index), self.normalInterarrivalTimeBus)
		worksheet.write_number(columnMapping["NormalInterarrivalTimePassenger"].format(index), self.normalInterarrivalTimePassenger)

class DhakaObject(SourcesObject):
	def __init__(self, location, lrp, traffic, scalingFactor):
		SourcesObject.__init__(self, 'Sources', 'Dhaka', location, lrp, traffic, 'N1', scalingFactor)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(DhakaObject, self).writeToWorksheet(worksheet, columnMapping, index)

class MidPathSourcesObject(SourcesObject):
	def __init__(self, node, traffic, scalingFactor):
		location = node.location
		location.x -= 500
		self.maximumArrivalsTruck = 'Infinity'
		self.maximumArrivalsBus = 'Infinity'
		self.maximumArrivalsPassenger = 'Infinity'
		if traffic.truck <= 0:
			self.maximumArrivalsTruck = '0'
			traffic.truck = 1
		if traffic.bus <= 0:
			self.maximumArrivalsBus = '0'
			traffic.bus = 1
		if traffic.passenger <= 0:
			self.maximumArrivalsPassenger = '0'
			traffic.passenger = 1

		SourcesObject.__init__(self, "Sources", "sources_"+node.road+"_"+node.lrp, location, node.lrp, traffic, node.road, scalingFactor)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(MidPathSourcesObject, self).writeToWorksheet(worksheet, columnMapping, index)

		worksheet.write_string(columnMapping["MaximumArrivalsTruck"].format(index), self.maximumArrivalsTruck)
		worksheet.write_string(columnMapping["MaximumArrivalsBus"].format(index), self.maximumArrivalsBus)
		worksheet.write_string(columnMapping["MaximumArrivalsPassenger"].format(index), self.maximumArrivalsPassenger)

<<<<<<< HEAD
# class DhakaObject(SimioObject):
# 	def __init__(self, location, lrp, entityType = "SourceEntity"):
# 		SimioObject.__init__(self, "Source", "Dhaka", location, lrp)
# 		# self.interarrivalTime = interarrivalTime
# 		self.entityType = entityType
#
# 	def writeToWorksheet(self, worksheet, columnMapping, index):
# 		super(DhakaObject, self).writeToWorksheet(worksheet, columnMapping, index)
# 		# worksheet.write_number(columnMapping["InterarrivalTime"].format(index), self.interarrivalTime)
# 		worksheet.write_string(columnMapping["EntityType"].format(index), self.entityType)

=======
>>>>>>> 8607025440f53989a931ff7daab06d7ddee1e71b
class BridgeObject(SimioObject):
	def __init__(self, road, location, lrp, category, length):
		SimioObject.__init__(self, "Bridge", road+"_"+lrp, location, lrp, road)
		self.category = category
		self.length = length
		self.initialTravelerCapacity = "SmallBridgeCapacity" if length < 50 else "LargeBridgeCapacity"
		self.runInitializedAddOnProcess = "SetBridgeState_"+category
		self.reportStatistics = "True"
		self.enteringAddOnProcess = "VehicleEnteredBridge"
		self.hasSink = False
		self.percentTruckTrafficToDestroy = 0
		self.percentBusTrafficToDestroy = 0
		self.percentPassengerTrafficToDestroy = 0

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
		worksheet.write_number(columnMapping["BridgeLength"].format(index), self.length)
		worksheet.write_string(columnMapping["InitialTravelerCapacity"].format(index), self.initialTravelerCapacity)
		worksheet.write_string(columnMapping["RunInitializedAddOnProcess"].format(index), self.runInitializedAddOnProcess)
		worksheet.write_string(columnMapping["ReportStatistics"].format(index), self.reportStatistics)
		worksheet.write_string(columnMapping["EnteredAddOnProcess"].format(index), self.enteringAddOnProcess)
		worksheet.write_boolean(columnMapping["HasSink"].format(index), self.hasSink)
		worksheet.write_number(columnMapping["PercentTruckTrafficToDestroy"].format(index), self.percentTruckTrafficToDestroy)
		worksheet.write_number(columnMapping["PercentBusTrafficToDestroy"].format(index), self.percentBusTrafficToDestroy)
		worksheet.write_number(columnMapping["PercentPassengerTrafficToDestroy"].format(index), self.percentPassengerTrafficToDestroy)


class EndBridgeObject(BridgeObject):
	def __init__(self, road, location, lrp, category, length):
		BridgeObject.__init__(self, road, location, lrp, category, length)
		self.enteringAddOnProcess = self.chooseInitializedAddOnProcess(length)

	def writeToWorksheet(self, worksheet, columnMapping, index):
		super(EndBridgeObject, self).writeToWorksheet(worksheet, columnMapping, index)
