import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import gridspec

def plot_traffic_density(segments,HeavyTrucks,MediumTrucks,SmallTrucks,Economic,broken_bridges):
	number_segments = len(segments)
	x = np.arange(number_segments)
	y1 = np.ones(number_segments)
	y2 = np.array(HeavyTrucks)
	y3 = np.array(MediumTrucks)
	y4 = np.array(SmallTrucks)
	y5 = np.array(broken_bridges)

	xmin = x.min()
	xmax = x.max()

	stacked1 = []
	for i in range(len(y2)):
		stacked = y2[i]+y3[i]
		stacked1.append(stacked)

	stacked2 = []
	for i in range(len(y4)):
		stacked = y4[i] + stacked1[i]
		stacked2.append(stacked)

	ymin = 0    
	ymax = max(stacked2)

	y5max = y5.max()

	width = 1

	# Two subplots, the axes array is 1-d
	fig = plt.figure(figsize=(15, 8))
	gs = gridspec.GridSpec(3, 1, height_ratios=[5,1,3])     

	ax0 = plt.subplot(gs[0])
	ax0.fill_between(x, 0, y2, label = 'HeavyTrucks', color = '#44FFD1')
	ax0.fill_between(x, y2, stacked1, label = 'MediumTrucks', color = '#8F2D56')
	ax0.fill_between(x, stacked1, stacked2, label = 'SmallTrucks', color = '#00A8E8')

	ax1 = plt.subplot(gs[1])
	p1 = ax1.hexbin(x, y1, Economic, gridsize=number_segments-1, cmap='RdYlGn_r')

	ax2 = plt.subplot(gs[2])
	p2 = ax2.bar(x, y5, width = 1, color='black', label = 'Broken bridges', align = 'edge')

	# Set titles of subplots
	ax0.set_title('Traffic density [number of trucks per lane per day]')
	ax1.set_title('Traffic density') # eventueel vervangen door average travel time per segment
	ax2.set_title('Broken bridges') 

	# Change layout
	fig.subplots_adjust(hspace=0.25, left=0.07, right=0.93)

	ax0.axis([xmin, xmax, 0, ymax+10])
	ax0.get_xaxis().set_visible(False)
	ax0.legend()

	ax1.axis([xmin, xmax, 0.9999, 1.0001])
	ax1.get_yaxis().set_visible(False)
	ax1.set_frame_on(True)
	ax1.get_xaxis().set_visible(False)

	ax2.axis([xmin, xmax, 0,y5max])
	ax2.get_xaxis().set_visible(True)
	ax2.set_frame_on(True)
	ax2.get_yaxis().set_ticks([0,y5max])

	# Set xlabel for graphs
	plt.xlabel('Chainage')
	if number_segments <= 150:
		plt.xticks(x,segments,rotation='vertical')

	# Colorbar for Total vulnerability graph    
	cb = fig.colorbar(p1, ax=ax2, orientation='horizontal', pad=0.6)
	cb.set_label('Traffic density') # replace?