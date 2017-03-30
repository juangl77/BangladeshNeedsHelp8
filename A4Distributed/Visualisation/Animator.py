import matplotlib.pyplot as plt
import matplotlib.animation as animation
import warnings

from multiprocessing import Process, Queue
from Visualisation import plot_traffic_density
from MySQL import Database

class Animator(object):
	def animate(self, interval, start_time, end_time):

		db = Database('127.0.0.1', 'Discrete', 'epa1351user', 'qwertyu1234')
		db.connect()

		fig = plt.figure(figsize=(12, 6))

		def update(frame):
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				plot_traffic_density(fig, db.dataPerSegment(frame))

		anim = animation.FuncAnimation(fig=fig, func=update, frames=range(start_time,end_time), blit=False, interval=interval, repeat=False)

		video = anim.to_html5_video()

		db.disconnect()

		return video