import csv
import os
from bs4 import BeautifulSoup
import re

class Bridge():
    bridgeId = ''
    roadId = ''
    structureName = ''
    structureType = ''
    bridgeCategory = ''
    width = -1
    length = -1
    constructionYear = -1
    spanNumber = -1
    zone = ''
    circle = ''
    division = ''
    subDivision = ''
    structureLrpName = ''
    referenceLrp = ''
    locationLrpOffset = -1
    locationChainage = -1
    latitude = -1
    longitude = -1
    bcsTotalScore = -1

    def isBridgeEmpty(self):
        return (self.latitude == -1 and self.longitude == -1 and self.locationChainage == -1 and self.locationLrpOffset == -1 and self.spanNumber == -1
                and self.constructionYear == -1 and self.width == -1 and self.length == -1 and self.bridgeId == '' and self.roadId == '')

fileRoot = '.htm'
directory = '../BMMS/'

if not os.path.exists(directory+'CSV/'):
    os.makedirs(directory+'CSV/')

allBridges = []

for dirName in os.listdir(directory):
    superDir = directory+dirName+'/'
    if os.path.isdir(superDir):
        bridgesForRoad = {}
        for filename in os.listdir(superDir):
            if filename.endswith(fileRoot):
                parsed = BeautifulSoup(open(superDir+filename), 'lxml')

                roadId = filename.split('.')[0]
                bridgeId = filename.split('.')[1]

                if 'bcs1' in filename:
                    #this is a new bridge
                    tables = parsed.find_all('table')

                    if parsed.find(text=re.compile('error')):
                        continue

                    if bridgeId not in bridgesForRoad:
                        bridgesForRoad[bridgeId] = Bridge()

                    bridgesForRoad[bridgeId].bridgeId = bridgeId

                    data = tables[2].find_all('td')
                    bridgesForRoad[bridgeId].zone = data[1].text.strip()
                    bridgesForRoad[bridgeId].circle = data[3].text.strip()
                    bridgesForRoad[bridgeId].division = data[5].text.strip()
                    bridgesForRoad[bridgeId].subDivision = data[7].text.strip()
                    bridgesForRoad[bridgeId].roadId = data[9].text.strip()
                    bridgesForRoad[bridgeId].structureLrpName = data[13].text.strip()

                    data = tables[3].find_all('td')

                    try:
                        latDeg = float(data[5].text.strip()) if data[5].text.strip() != '' else 0
                        latMin = float(data[6].text.strip()) if data[6].text.strip() != '' else 0
                        latSec = float(data[7].text.strip()) if data[7].text.strip() != '' else 0
                        lonDeg = float(data[9].text.strip()) if data[9].text.strip() != '' else 0
                        lonMin = float(data[10].text.strip()) if data[10].text.strip() != '' else 0
                        lonSec = float(data[11].text.strip()) if data[11].text.strip() != '' else 0
                        bridgesForRoad[bridgeId].latitude = latDeg + latMin/60. + latSec/3600.
                        bridgesForRoad[bridgeId].longitude = lonDeg + lonMin/60. + lonSec/3600.
                    except ValueError:
                        print('Problem with latitude/longitude for bridge {} on road {}'.format(bridgeId,roadId))
                        bridgesForRoad[bridgeId].latitude = -1
                        bridgesForRoad[bridgeId].longitude = -1

                    data = tables[4].find_all('td')

                    bridgesForRoad[bridgeId].structureName = data[1].text.strip()
                    bridgesForRoad[bridgeId].referenceLrp = data[3].text.strip()
                    try:
                        bridgesForRoad[bridgeId].locationLrpOffset = float(data[5].text.strip().replace(',','')) if data[5].text.strip() != '' else -1
                    except ValueError:
                        print('Problem with location offset for bridge {} on road {}'.format(bridgeId,roadId))
                    try:
                        bridgesForRoad[bridgeId].locationChainage = float(data[7].text.strip().replace(',','')) if data[7].text.strip() != '' else -1
                    except ValueError:
                        print('Problem with location offset for bridge {} on road {}'.format(bridgeId,roadId))

                    data = tables[5].find_all('td')

                    bridgesForRoad[bridgeId].structureType = data[0].text.strip()

                    data = tables[7].find_all('td')

                    bridgesForRoad[bridgeId].constructionYear = data[3].text.strip()
                    try:
                        bridgesForRoad[bridgeId].spanNumber = float(data[9].text.strip().replace(',','')) if data[9].text.strip() != '' else -1
                        bridgesForRoad[bridgeId].length = float(data[13].text.strip().replace(',','')) if data[13].text.strip() != '' else -1
                        bridgesForRoad[bridgeId].width = float(data[15].text.strip().replace(',','')) if data[15].text.strip() != '' else -1
                        bridgesForRoad[bridgeId].carriageway = float(data[17].text.strip().replace(',','')) if data[17].text.strip() != '' else -1
                    except ValueError:
                        print('Problem with construction data for bridge {} on road {}'.format(bridgeId,roadId))

                elif 'bcs2' in filename:
                    #This file contains bridge category information only
                    if parsed.find(text=re.compile('error')):
                        continue
                    if bridgeId not in bridgesForRoad:
                        bridgesForRoad[bridgeId] = Bridge()

                    tables = parsed.find_all('table')
                    data = tables[2].find_all('td')

                    zone = data[4].text.strip()
                    circle = data[5].text.strip()
                    division = data[6].text.strip()
                    subDivision = data[7].text.strip()

                    bridgesForRoad[bridgeId].roadId = roadId if bridgesForRoad[bridgeId].roadId == '' else bridgesForRoad[bridgeId].roadId
                    bridgesForRoad[bridgeId].bridgeId = bridgeId if bridgesForRoad[bridgeId].bridgeId == '' else bridgesForRoad[bridgeId].bridgeId

                    bridgesForRoad[bridgeId].zone = zone if bridgesForRoad[bridgeId].zone == '' else bridgesForRoad[bridgeId].zone
                    bridgesForRoad[bridgeId].circle = circle if bridgesForRoad[bridgeId].circle == '' else bridgesForRoad[bridgeId].circle
                    bridgesForRoad[bridgeId].division = division if bridgesForRoad[bridgeId].division == '' else bridgesForRoad[bridgeId].division
                    bridgesForRoad[bridgeId].subDivision = subDivision if bridgesForRoad[bridgeId].subDivision == '' else bridgesForRoad[bridgeId].subDivision

                    category = parsed.find('td', text=re.compile('Category')).parent.find_all('table')[0]
                    bridgesForRoad[bridgeId].bridgeCategory = category.find_all('td')[0].text.strip()

                elif 'bcs3' in filename:
                    #potentially interesting data, if they exist
                    if parsed.find(text=re.compile('error')):
                        continue

                    if bridgeId not in bridgesForRoad:
                        bridgesForRoad[bridgeId] = Bridge()

                    mainTable = parsed.find_all('table')[1].find_all('tr')
                    rowA = mainTable[1].find_all('td')
                    rowB = mainTable[2].find_all('td')
                    rowC = mainTable[3].find_all('td')

                    zone = rowA[1].text.strip()
                    circle = rowA[3].text.strip()
                    division = rowA[5].text.strip()
                    subDivision = rowA[7].text.strip()
                    roadId = rowB[1].text.strip()
                    structureName = rowC[5].text.strip()

                    #only replace information if it is not already specified in bcs1
                    bridgesForRoad[bridgeId].zone = zone if bridgesForRoad[bridgeId].zone == '' else bridgesForRoad[bridgeId].zone
                    bridgesForRoad[bridgeId].circle = circle if bridgesForRoad[bridgeId].circle == '' else bridgesForRoad[bridgeId].circle
                    bridgesForRoad[bridgeId].division = division if bridgesForRoad[bridgeId].division == '' else bridgesForRoad[bridgeId].division
                    bridgesForRoad[bridgeId].subDivision = subDivision if bridgesForRoad[bridgeId].subDivision == '' else bridgesForRoad[bridgeId].subDivision
                    bridgesForRoad[bridgeId].roadId = roadId if bridgesForRoad[bridgeId].roadId == '' else bridgesForRoad[bridgeId].roadId
                    bridgesForRoad[bridgeId].bridgeId = bridgeId if bridgesForRoad[bridgeId].bridgeId == '' else bridgesForRoad[bridgeId].bridgeId
                    bridgesForRoad[bridgeId].structureName = structureName if bridgesForRoad[bridgeId].structureName == '' else bridgesForRoad[bridgeId].structureName

                    try:
                        chainage = float(rowB[5].text.strip().replace(',','')) if rowB[5].text.strip() != '' else -1
                        bridgesForRoad[bridgeId].locationChainage = chainage if bridgesForRoad[bridgeId].locationChainage == -1 else bridgesForRoad[bridgeId].locationChainage
                    except ValueError:
                        print('Problem with location chainage for bridge {} on road {}'.format(bridgeId,roadId))



                else:
                    #not an interesting file, skip
                    continue

        #Bridges are constructed, save to file
        if not bridgesForRoad:
            #no bridges created, don't create CSV
            continue

        csvFile = dirName
        with open(directory+'CSV/'+csvFile+'.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('Number','Structure Name','Condition of Bridge', 'TotalWidth','TotalLength','ConstructionYear',
                'NumberOfSpan','Zone','Circle','Division','Sub-Division','RoadNo','BridgeNo','StructureLRPName','ReferenceLRPNo','LocationLRPOffset',
                'LocationChainage','Latitude','Longitude'))
            index = 1
            for key in bridgesForRoad:
                entry = bridgesForRoad[key]
                if entry.isBridgeEmpty():
                    continue
                allBridges.append(entry)
                writer.writerow((index,entry.structureName,entry.bridgeCategory,entry.width,entry.length,entry.constructionYear,
                    entry.spanNumber,entry.zone,entry.circle,entry.division,entry.subDivision,entry.roadId,entry.bridgeId,entry.structureLrpName,entry.referenceLrp,entry.locationLrpOffset,
                    entry.locationChainage,entry.latitude,entry.longitude))
                index += 1
        print('Done with writing {}'.format(csvFile))

print('Writing to summary file!')

with open('../BMMS/CSV/_allBridges.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('Number','Structure Name','Condition of Bridge', 'TotalWidth','TotalLength','ConstructionYear',
        'NumberOfSpan','Zone','Circle','Division','Sub-Division','RoadNo','BridgeNo','StructureLRPName','ReferenceLRPNo','LocationLRPOffset',
        'LocationChainage','Latitude','Longitude'))
    index = 1
    for entry in allBridges:
        writer.writerow((index,entry.structureName,entry.bridgeCategory,entry.width,entry.length,entry.constructionYear,
            entry.spanNumber,entry.zone,entry.circle,entry.division,entry.subDivision,entry.roadId,entry.bridgeId,entry.structureLrpName,entry.referenceLrp,entry.locationLrpOffset,
            entry.locationChainage,entry.latitude,entry.longitude))
        index += 1

print('All done. Thanks for playing.')
