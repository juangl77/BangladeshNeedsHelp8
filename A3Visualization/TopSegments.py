class SegmentProvider(object):
	def provide(self, bridge_likelihoods):
		return [
			SuperSegment("seg_1", 0, 0, bridge_likelihoods['A']),
			SuperSegment("seg_2", 0, 0, bridge_likelihoods['B']),
			SuperSegment("seg_3", 0, 0, bridge_likelihoods['C']),
			SuperSegment("seg_4", 0, 0, bridge_likelihoods['D']),
		]

class SuperSegment(object):
	def __init__(self, name, centre_x, centre_y, score):
		self.name = name
		self.centre_x = centre_x
		self.centre_y = centre_y
		self.score = score

	def __gt__(self, that):
		return self.score > that.score

	def __eq__(self, that):
		return self.score == that.score

class TopSegment(object):
	def __init__(self, name, segment, count):
		self.name = name
		self.segment = segment
		self.count = count

	def __str__(self):
		return self.name + ' ' + str(self.segment.score)

class TopSegmentProvider(object):
	lin_likelihoods = {'A': 0.1, 'B': 0.2, 'C': 0.3, 'D': 0.4}
	log_likelihoods = {'A': 0.1, 'B': 0.2, 'C': 0.25, 'D': 0.3}
	exp_likelihoods = {'A': 0.1, 'B': 0.2, 'C': 0.4, 'D': 0.8}

	def calculate(self, n):
		provider = SegmentProvider()

		top_lin = self.top(n, provider.provide(self.lin_likelihoods))
		top_log = self.top(n, provider.provide(self.log_likelihoods))
		top_exp = self.top(n, provider.provide(self.exp_likelihoods))

		counts = self.combine(self.combine(self.combine({}, top_lin), top_log), top_exp)
		
		return (self.transform(counts, top_lin), self.transform(counts, top_log), self.transform(counts, top_exp))

	def combine(self, counts, segments):
		for segment in segments:
			counts[segment.name] = 1 if segment.name not in counts else counts[segment.name]+1
		return counts

	def transform(self, counts, segments):
		top_segments = []
		for segment in segments:
			top_segments.append(TopSegment(segment.name, segment, counts[segment.name]))

		return top_segments

	def top(self, n, segments):
		return list(sorted(segments)[-n:])


(lin, log, exp) = TopSegmentProvider().calculate(3)
print(map(lambda s : str(s), lin))
print(map(lambda s : str(s), log))
print(map(lambda s : str(s), exp))