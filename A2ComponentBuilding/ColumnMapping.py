def init():
	global objectColumnNames
	objectColumnNames = ["Object Class", "Object Name", "X", "Y", "Z", "Length", "Width", "Height", "InitialDesiredSpeed", "EntityType", 
    	"InterarrivalTime", "InitialTravelerCapacity",
		"Category", "EnteringAddOnProcess", "ReportStatistics"]
	
	global objectColumnMapping
	objectColumnMapping = {
		objectColumnNames[0] : 	"A{}",
		objectColumnNames[1] : 	"B{}",
		objectColumnNames[2] : 	"C{}",
		objectColumnNames[3] : 	"D{}",
		objectColumnNames[4] : 	"E{}",
		objectColumnNames[5] : 	"F{}",
		objectColumnNames[6] : 	"G{}",
		objectColumnNames[7] : 	"H{}",
		objectColumnNames[8] : 	"I{}",
		objectColumnNames[9] : 	"J{}",
		objectColumnNames[10] : "K{}",
		objectColumnNames[11] : "L{}",
		objectColumnNames[12] : "M{}",
		objectColumnNames[13] : "N{}",
		objectColumnNames[14] : "O{}" }

	global linkColumnNames
	linkColumnNames = ["Link Class", "Link Name", "From Node", "To Node", "Network", "Width", "Height", "Type", 
		"DrawnToScale"]

	global linkColumnMapping
	linkColumnMapping = {
		linkColumnNames[0] : 	"A{}",
		linkColumnNames[1] : 	"B{}",
		linkColumnNames[2] : 	"C{}",
		linkColumnNames[3] : 	"D{}",
		linkColumnNames[4] : 	"E{}",
		linkColumnNames[5] : 	"F{}",
		linkColumnNames[6] : 	"G{}",
		linkColumnNames[7] : 	"H{}",
		linkColumnNames[8] : 	"I{}"
	}

	global vertexColumnNames
	vertexColumnNames = ["Object Class", "Object Name", "X", "Y", "Z"]

	global vertexColumnMapping
	vertexColumnMapping = {
		vertexColumnNames[0] : 	"A{}",
		vertexColumnNames[1] : 	"B{}",
		vertexColumnNames[2] : 	"C{}",
		vertexColumnNames[3] : 	"D{}",
		vertexColumnNames[4] : 	"E{}"
	}