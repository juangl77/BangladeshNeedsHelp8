from SegmentBuilder import SegmentBuilder, SuperSegment

class VisualisationElement(object):
	def __init__(self, segment, membership):
		self.name = segment.name
		self.road = segment.road
		self.lrp = segment.lrp
		self.lat = segment.lat
		self.lon = segment.lon
		self.vulnerability = segment.vulnerability
		self.membership = membership

	def __str__(self):
		return "Segment [" + self.name + " | " + str(self.vulnerability) + " | " + str(len(self.membership)) + "]"

class Scenario(object):
	def __init__(self, name, a, b, c, d):
		self.name = name
		self.a = a
		self.b = b
		self.c = c
		self.d = d

class VisualisationElementsProvider(object):
	def __init__(self, scenarios, n, grouping_size, mode = 'short'):
		self.scenarios = scenarios
		self.n = n
		self.grouping_size = grouping_size
		self.mode = mode

	def provide(self):
		builder = SegmentBuilder(self.grouping_size, self.mode)

		elements = {}

		for scenario in self.scenarios:
			print('\nCurrent scenario: {}'.format(scenario.name))
			elements[scenario.name] = builder.buildSelection(scenario)

		return elements

	def top(self, n, segments):
		return list(sorted(segments)[-n:])

# scenarios = [
# 	Scenario('linear', 0.1, 0.2, 0.3, 0.4),
# 	Scenario('log', 0.1, 0.2, 0.25, 0.3),
# 	Scenario('exp', 0.1, 0.2, 0.4, 0.8)
# ]
#
# res = VisualisationElementsProvider(scenarios, 5, 40, mode='N').provide()
