def init():
	global objectColumnNames
	objectColumnNames = ["Object Class", "Object Name", "InitialDesiredSpeed", "EntityType", 
    	"InterarrivalTime", "InitialTravelerCapacity",
		"Category", "Length", "EnteringAddOnProcess", "ReportStatistics", "X", "Y", "Z"]
	
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
		objectColumnNames[12] : "M{}" }