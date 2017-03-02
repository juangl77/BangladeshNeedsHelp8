def init():
	initObjects()
	initLinks()
	initVertices()

def initObjects():
	global objectColumnNames
	objectColumnNames = [
		"Object Class", "Object Name", "X", "Y", "Z", "Length", "Width", "Height", 
		"InitialDesiredSpeed", "EntityType", "InterarrivalTime", "InitialTravelerCapacity", 
		"Category", "EnteredAddOnProcess", "RunInitializedAddOnProcess", "ReportStatistics"
	]
	
	global objectColumnMapping
	objectColumnMapping = {}

	for i in range(0, len(objectColumnNames)):
		objectColumnMapping[objectColumnNames[i]] = "" + chr(ord('A')+i) + "{}"

def initLinks():
	global linkColumnNames
	linkColumnNames = [
		"Link Class", "Link Name", "From Node", "To Node", "Network", "Width", "Height", "Type", "DrawnToScale"
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