import pandas
from sqlalchemy import create_engine

class BridgeData():
	def __init__(self, row):
		self.road = row['road']
		self.lrp = row['lrp'].strip().upper()
		self.length = row['length']
		self.category = row['category']
		self.lat = row['lat']
		self.lon = row['lon']
		self.constructionYear = row['constructionYear']
		self.matched = False

	def __lt__(self, other):
		return self.lrp < other.lrp

	def bridgeComplete(self):
		return self.constructionYear != ''

	def toDict(self):
		return {
			'road':self.road,
			'lrp':self.lrp,
			'length':self.length,
			'category':self.category,
			'lat':self.lat,
			'lon':self.lon,
			'constructionYear':self.constructionYear
		}

	def fromDict(row):
		return BridgeData(row)

class RoadData():
	def __init__(self, row):
		self.road = row['road']
		self.lrp = row['lrp'].strip().upper()
		self.gap = row['gap']
		self.lat = float(row['lat'])
		self.lon = float(row['lon'])
		self.chainage = float(row['chainage'])

	def hasGap(self):
		return self.gap != ''

	def bridgeName(self):
		return self.road + "_" + self.lrp

class Traffic():
	percentageDuringRush = 0.5
	numberRushHours = 6

	def __init__(self, truck=0, bus=0, passenger=0):
		self.truck = truck
		self.bus = bus
		self.passenger = passenger

	def trafficPerLanePerSegment(self, numberLanes, fractionOfLength):
		self.truck = (self.truck / numberLanes)*fractionOfLength
		self.bus = (self.bus / numberLanes)*fractionOfLength
		self.passenger = (self.passenger / numberLanes)*fractionOfLength
		return self

	def addTraffic(self, traffic):
		self.bus += traffic.bus
		self.truck += traffic.truck
		self.passenger += traffic.passenger
		return self

	def totalTraffic(self):
		return self.truck + self.bus + self.passenger

class TrafficData():
	def __init__(self, row):
		self.road = row['road']
		self.startChainage = round( float(row['width_start']), 3)
		self.endChainage = round( float(row['width_end']), 3)
		self.numberLanes = int(row['numberLanes'])

		self.fullStart = round( float(row['start_chainage']), 3)
		self.fullEnd = round( float(row['end_chainage']), 3)

		self.leftTraffic = Traffic()
		self.rightTraffic = Traffic()

class DataReader():
	def __init__(self,username,password,database):
		self.database = database
		self.engine = create_engine('mysql+mysqlconnector://'+ username + ':' + password + '@localhost/'+database)

	def readBridges(self):
		bridges = []

		df = pandas.read_sql('SELECT * FROM '+self.database+'.bridges', con=self.engine)
		for index, row in df.iterrows():
			bridges.append(BridgeData(row.to_dict()))

		return bridges

	def readRoads(self):
		roads = []

		df = pandas.read_sql('SELECT * FROM '+self.database+'.roads', con=self.engine)
		for index, row in df.iterrows():
			roads.append(RoadData(row.to_dict()))
		return roads

	def readTraffic(self):
		trafficEntries = []

		df = pandas.read_sql('SELECT * FROM '+self.database+'.traffic', con=self.engine)
		for linkId, group in df.groupby('linkId'):
			for end, group in group.groupby('width_end'):
				trafficEntry = TrafficData(dict(group.iloc[0]))

				for index, row in group.iterrows():

					truckTraffic = (int(row['heavyTruck']) + int(row['mediumTruck']) + int(row['smallTruck']))
					busTraffic = (int(row['largeBus']) + int(row['mediumBus']) + int(row['microBus']))
					passengerTraffic = (int(row['utility']) + int(row['car']) + int(row['autoRickshaw']) + int(row['motorcycle']))

					# Normalize traffic per lane
					traffic = Traffic(int(round(truckTraffic/trafficEntry.numberLanes)),
									  int(round(busTraffic/trafficEntry.numberLanes)),
									  int(round(passengerTraffic/trafficEntry.numberLanes)) )

					if(row['side_of_road'] == 'Left'):
						trafficEntry.leftTraffic = traffic
					elif(row['side_of_road'] == 'Right'):
						trafficEntry.rightTraffic = traffic
					else:
						traffic.truck = int(traffic.truck/2)
						traffic.bus = int(traffic.bus/2)
						traffic.passenger = int(traffic.passenger/2)
						trafficEntry.leftTraffic = traffic
						trafficEntry.rightTraffic = traffic

				trafficEntries.append(trafficEntry)

		trafficEntries.sort(key=lambda x: x.startChainage)

		return trafficEntries
