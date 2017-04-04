import mysql.connector as sql
import pandas as pd

class Database(object):
	def __init__(self, host, database, user, password):
		self.host = host
		self.database = database
		self.user = user
		self.password = password

		self.paths = 'bangladeshroadpaths'
		self.bridges = 'bangladeshroadbridges'
		self.status = 'simulationstatus'

	def connect(self):
		self.connection = sql.connect(host=self.host,
			database=self.database,
			user=self.user,
			password=self.password)
		self.connection.autocommit = True
		self.cursor = self.connection.cursor()

	def disconnect(self):
		self.connection.close()

	def latestTime(self):
		command = 'SELECT * FROM {0}.{1};'
		frame = pd.read_sql(command.format(self.database, self.status), con=self.connection)

		return int(frame.to_dict(orient='records')[0]['EventCount'])

	def traffic(self, time):
		command = 'SELECT * FROM {0}.{1} WHERE {0}.{1}.SimulationTime = {2};'
		frame = pd.read_sql(command.format(self.database, self.paths, time), con=self.connection)
		return frame

	def brokenBridges(self, time):
		command = 'SELECT {0}.{1}.BridgeName FROM {0}.{1} WHERE {0}.{1}.SimulationTime = {2} and {0}.{1}.IsBridgeBroken;'

		frame =  pd.read_sql(command.format(self.database, self.bridges, time), con=self.connection)
		return list(map(lambda x: str(x[3:]).lower().strip(), list(frame['BridgeName'])))

	def bridgeStatus(self, path_names, broken_bridges):
		bridge_status = []
		for path_name in path_names:
			if path_name.startswith('bridge'):
				(_,_,lrp_s,lrp_e) = path_name.split("_")

				if lrp_s.lower() in broken_bridges:
					bridge_status.append(1)
				elif lrp_e.lower() in broken_bridges:
					bridge_status.append(1)
				else:
					bridge_status.append(0)
			else:
				bridge_status.append(0)

		frame = pd.DataFrame({'path_name':path_names, 'bridge_status': bridge_status})
		return frame

	def averageWaitingTime(self, traffic_data, categories):
		waiting_times = []

		for row in traffic_data.to_dict(orient='records'):
			number_of_vehicles = row['NumberVehicles']

			if number_of_vehicles < 1:
				waiting_times.append(0)
			else:
				total_time = 0
				for category in categories:
					category_name = category.replace(' ', '')
					total_time += (row['Average{0}WaitingTime'.format(category_name)] * row['{0}AverageNumberWaiting'.format(category_name)])
				waiting_times.append(total_time / number_of_vehicles)

		return waiting_times

	def dataPerSegment(self, time):
		traffic = self.traffic(time)
		broken_bridges = self.brokenBridges(time)
		path_names = list(traffic['PathName'])

		data = pd.DataFrame()
		data['id'] = list(range(0, len(path_names)))
		data['path_name'] = path_names

		bridge_status = self.bridgeStatus(path_names, broken_bridges)
		data = pd.merge(data, bridge_status, on='path_name')

		categories = ['Truck', 'Bus', 'Passenger Vehicle']
		for category in categories:
			sql_name = category.replace(' ', '')
			data_name = category.lower().replace(' ', '_')

			data['{0}_count'.format(data_name)] = traffic['{0}AverageNumberWaiting'.format(sql_name)]

		data['average_waiting_time'] = self.averageWaitingTime(traffic, categories)

		return data
