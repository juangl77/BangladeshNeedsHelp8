import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import gridspec

def stacks(y2, y3, y4):
	stacked1 = []
	for i in range(len(y2)):
		stacked1.append(y2[i]+y3[i])

	stacked2 = []
	for i in range(len(y4)):
		stacked2.append(y4[i] + stacked1[i])

	return (stacked1, stacked2)

def plot_traffic_density_per_category(gridspec, x, y2, y3, y4, ticks):
	(stacked1, stacked2) = stacks(y2, y3, y4)

	ax0 = plt.subplot(gridspec[0])
	
	ax0.fill_between(x, 0, y2, label = 'Trucks', color = '#44FFD1')
	ax0.fill_between(x, y2, stacked1, label = 'Busses', color = '#8F2D56')
	ax0.fill_between(x, stacked1, stacked2, label = 'Passenger Vehicles', color = '#00A8E8')

	xmin = x.min()
	xmax = x.max()
	ymax = int(max(stacked2)*1.2)

	ax0.axis([xmin, xmax, 0, ymax])
	ax0.get_xaxis().set_visible(False)
	ax0.legend()

	for tick in ticks:
		plot_line(ax0, tick, 0, ymax)

	ax0.set_title('Traffic Density')

	return ax0

def plot_average_time_on_segment(gridspec, x, y1, TimeInSystem, ticks):
	ax1 = plt.subplot(gridspec[1])
	p1 = ax1.hexbin(x, y1, TimeInSystem, gridsize=len(TimeInSystem), cmap='RdYlGn_r')

	xmin = x.min()
	xmax = x.max()
	ymin = 0.9999
	ymax = 1.0001

	ax1.axis([xmin, xmax, ymin, ymax])
	ax1.get_yaxis().set_visible(False)
	ax1.set_frame_on(True)
	ax1.get_xaxis().set_visible(False)

	for tick in ticks:
		plot_line(ax1, tick, ymin, ymax)

	ax1.set_title('Average Time on Segment')

	return (ax1, p1)

def plot_broken_bridges(gridspec, x, y5, ticks):
	ax2 = plt.subplot(gridspec[2])
	p2 = ax2.bar(x, y5, width = 1, color='black', label = 'Broken bridges', align = 'edge')

	xmin = x.min()
	xmax = x.max()
	y5max = y5.max()

	ax2.axis([xmin, xmax, 0,y5max])
	ax2.get_xaxis().set_visible(True)
	ax2.set_frame_on(True)
	ax2.get_yaxis().set_ticks([0,y5max])

	for tick in ticks:
		plot_line(ax2, tick, 0, y5max)

	ax2.set_title('Broken Bridges')

	return (ax2, p2)

def plot_line(sub_plot, tick, ymin, ymax):
	sub_plot.plot([tick,tick],[ymin,ymax],color='black',linestyle=':',linewidth=0.5)

def plot_traffic_density(fig, data):
	TimeInSystem = data['average_waiting_time'] 

	x = data['id']
	y1 = np.ones(len(data['id']))
	y2 = data['truck_count']
	y3 = data['bus_count']
	y4 = data['passenger_vehicle_count']
	y5 = data['bridge_status']

	# Two subplots, the axes array is 1-d
	gs = gridspec.GridSpec(3, 1, height_ratios=[5,0.6,2])   

	len_x = len(x)
	places = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.625, 0.75, 0.875, 1]
	ticks = [x[min(int(len_x*place), len_x-1)] for place in places]

	ax0 = plot_traffic_density_per_category(gs, x, y2, y3, y4, ticks[1:])
	(ax1, p1) = plot_average_time_on_segment(gs, x, y1, TimeInSystem, ticks[1:])
	(ax2, p2) = plot_broken_bridges(gs, x, y5, ticks[1:])

	fig.subplots_adjust(hspace=0.25, left=0.07, right=0.93)

	plt.xlabel('Location')

	names = ['Dhaka','Homna','Comilla','Bangadda','Narayanhat','Chittagong','Chandanaish','Chakaria','Umkhali','Sabrang']
	plt.xticks(ticks,names)

	# Colorbar for Total vulnerability graph    
	cb = fig.colorbar(p1, ax=ax2, orientation='horizontal', pad=0.6)
	cb.set_label('Average Time on Segment')