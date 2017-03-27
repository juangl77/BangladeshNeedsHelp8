from math import floor

def init():
	initObjects()
	initLinks()
	initVertices()

def initObjects():
	global objectColumnNames
	objectColumnNames = [
		"Object Class", "Object Name", "X", "Y", "Z", "Length", "Width", "Height",
		"InitialDesiredSpeed", "EntityType", "RushInterarrivalTimeTruck", "RushInterarrivalTimeBus", "RushInterarrivalTimePassenger",
		"NormalInterarrivalTimeTruck", "NormalInterarrivalTimeBus", "NormalInterarrivalTimePassenger", "InitialTravelerCapacity",
		"MaximumArrivalsTruck", "MaximumArrivalsBus", "MaximumArrivalsPassenger",
		"Category", "EnteredAddOnProcess", "RunInitializedAddOnProcess", "ReportStatistics", "BridgeLength", "HasSink",
		"PercentTruckTrafficToDestroy", "PercentBusTrafficToDestroy", "PercentPassengerTrafficToDestroy"
	]

	global objectColumnMapping
	objectColumnMapping = {}

	for i in range(0, len(objectColumnNames)):
		temp = i % 26
		wrapped = floor(i/26)
		objectColumnMapping[objectColumnNames[i]] = ""
		if wrapped == 0:
			objectColumnMapping[objectColumnNames[i]] += chr(ord('A')+temp)
		else:
			objectColumnMapping[objectColumnNames[i]] += chr(ord('A')+wrapped-1)
			objectColumnMapping[objectColumnNames[i]] += chr(ord('A')+temp)
		objectColumnMapping[objectColumnNames[i]] += "{}"
		
def initLinks():
	global linkColumnNames
	linkColumnNames = [
		"Link Class", "Link Name", "From Node", "To Node", "Network", "Width", "Height", "Type", "DrawnToScale", "AllowPassing"
	]

	global linkColumnMapping
	linkColumnMapping = {}

	for i in range(0, len(linkColumnNames)):
		linkColumnMapping[linkColumnNames[i]] = "" + chr(ord('A')+i) + "{}"

def initVertices():
	global vertexColumnNames
	vertexColumnNames = ["Link Name", "X", "Y", "Z"]

	global vertexColumnMapping
	vertexColumnMapping = {}

	for i in range(0, len(vertexColumnNames)):
		vertexColumnMapping[vertexColumnNames[i]] = "" + chr(ord('A')+i) + "{}"
