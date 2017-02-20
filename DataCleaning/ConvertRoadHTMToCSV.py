import csv
import os
from bs4 import BeautifulSoup
import re
from itertools import chain

class RoadEntry():
    roadId = ''
    lrpNumber = ''
    roadChainage = -1
    lrpType = ''
    desc = ''
    latitude = -1
    longitude = -1

roadRoot = '.lrps.htm'
directory = '../RMMS/'

if not os.path.exists(directory+'CSV/'):
    os.makedirs(directory+'CSV/')

allRoads = []
for filename in os.listdir(directory):
    if filename.endswith(roadRoot):
        #Do things, this is a good file!!
        parsed = BeautifulSoup(open(directory+filename), 'lxml')
        headerRow = parsed.body.find(text=re.compile(r'LRP No')).parent.parent.parent
        newRoad = []
        roadId = filename[:-9]
        for row in headerRow.next_siblings:
            if (row.name == 'tr'):
                cells = row.contents

                newEntry = RoadEntry()
                newEntry.roadId = roadId
                newEntry.lrpNumber = cells[3].text.strip()
                try:
                    newEntry.roadChainage = float(cells[5].text.strip())
                except ValueError:
                    print('Couldn\'t convert chainage to float for road {}. Ignoring row.'.format(roadId))
                    break

                newEntry.lrpType = cells[7].text.strip()
                newEntry.desc = cells[9].text.strip()
                try:
                    newEntry.latitude = float(cells[11].text.strip())
                except ValueError:
                    print('Couldn\'t convert latitude to float for road {}. Ignoring row.'.format(roadId))
                    break
                try:
                    newEntry.longitude = float(cells[13].text.strip())
                except ValueError:
                    print('Couldn\'t convert longitude to float for road {}. Ignoring row.'.format(roadId))
                    break

                newRoad.append(newEntry)
            else:
                continue

        #Road is constructed, save to file
        allRoads.append(newRoad)
        csvFile = filename.replace(' ', '')[:-4].upper()
        with open('../RMMS/CSV/'+csvFile+'.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('Road Id','LRP Number', 'Road Chainage','Type','Desc','Latitude','Longitude'))
            writer.writerows((entry.roadId,entry.lrpNumber,entry.roadChainage,entry.lrpType,entry.desc,entry.latitude,entry.longitude) for entry in newRoad)

print('Writing to summary file!')

with open('../RMMS/CSV/_allRoads.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('Road Id','LRP Number','Road Chainage','Type','Desc','Latitude','Longitude'))
    for road in allRoads:
        writer.writerows((entry.roadId,entry.lrpNumber,entry.roadChainage,entry.lrpType,entry.desc,entry.latitude,entry.longitude) for entry in road)

print('All done. Thanks for playing.')
