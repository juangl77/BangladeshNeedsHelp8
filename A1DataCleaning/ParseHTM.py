import csv
import os
import re
from bs4 import BeautifulSoup

import ReadWriteCSV
import Constants

def newRoadEntry():
    return {
        Constants.road:'',
        Constants.lrp: '',
        Constants.chainage: -1,
        Constants.lrpType: '',
        Constants.name:'',
        Constants.lat: -1,
        Constants.lon: -1
    }

def roadEntryIsEmpty(entry):
    return entry[Constants.lat] == -1 and entry[Constants.lon] == -1 and entry[Constants.chainage] == -1 and entry[Constants.lrp] == ''

def newBridge():
    return {
        Constants.road: '',
        Constants.structureNr: '',
        Constants.name: '',
        Constants.lrpType: '',
        Constants.condition: '',
        Constants.width: -1,
        Constants.length: -1,
        Constants.constructionYear: -1,
        Constants.spans: -1,
        Constants.zone: '',
        Constants.circle: '',
        Constants.division: '',
        Constants.subDivision: '',
        Constants.lrpname: '',
        Constants.roadName: '',
        Constants.chainage: -1,
        Constants.km: -1,
        Constants.lat: -1,
        Constants.lon: -1,
        Constants.estimatedLoc: ''
    }

def bridgeIsEmpty(entry):
    return entry[Constants.lat] == -1 and entry[Constants.lon] == -1 and entry[Constants.chainage] == -1 and \
        entry[Constants.spans] == -1 and entry[Constants.constructionYear] == -1 and entry[Constants.width] == -1 and \
        entry[Constants.length] == -1 and entry[Constants.road] == ''

def parseRoadInfo():
    print('Entering road data parsing.')

    roadRoot = '.lrps.htm'
    roadDirectory = '../RMMS/'

    if not os.path.exists(roadDirectory+'CSV/'):
        os.makedirs(roadDirectory+'CSV/')

    allRoads = []
    for filename in os.listdir(roadDirectory):
        if filename.endswith(roadRoot):
            #Do things, this is a good file!!
            parsed = BeautifulSoup(open(roadDirectory+filename), 'lxml')
            headerRow = parsed.body.find(text=re.compile(r'LRP No')).parent.parent.parent
            newRoad = []
            roadId = filename[:-9]

            print ('Active: {}'.format(roadId), end="\r")

            for row in headerRow.next_siblings:
                if (row.name == 'tr'):
                    cells = row.contents

                    newEntry = newRoadEntry()
                    newEntry[Constants.road] = roadId
                    newEntry[Constants.lrp] = cells[3].text.strip()
                    try:
                        newEntry[Constants.chainage] = float(cells[5].text.strip())
                        newEntry[Constants.km] = float(cells[5].text.strip())
                    except ValueError:
                        print('Couldn\'t convert chainage to float for road {} (value is \'{}\').'.format(roadId, cells[5].text.strip()))

                    newEntry[Constants.lrpType] = cells[7].text.strip()
                    newEntry[Constants.name] = cells[9].text.strip()
                    try:
                        newEntry[Constants.lat] = float(cells[11].text.strip())
                    except ValueError:
                        print('Couldn\'t convert latitude to float for road {} (value is \'{}\').'.format(roadId,cells[11].text.strip()))
                    try:
                        newEntry[Constants.lon] = float(cells[13].text.strip())
                    except ValueError:
                        print('Couldn\'t convert longitude to float for road {} (value is \'{}\').'.format(roadId,cells[13].text.strip()))

                    newRoad.append(newEntry)
                else:
                    continue

            #Road is constructed, save to file
            for entry in newRoad:
                if roadEntryIsEmpty(entry):
                    newRoad.remove(entry)
            if len(newRoad) == 0:
                print('Skipping empty road {}'.format(roadId))
                continue

            allRoads.extend(newRoad)
            csvFile = filename.replace(' ', '')[:-4].upper() + '.csv'
            ReadWriteCSV.writeRoads([ReadWriteCSV.Row(row) for row in newRoad],roadDirectory+'CSV/'+csvFile+'.csv')

    ReadWriteCSV.writeRoads([ReadWriteCSV.Row(row) for row in allRoads],roadDirectory + 'CSV/_allRoads.csv')

    print('Completed parsing road data.\n')

def parseBridgeInfo():
    print('Entering bridge data parsing.')

    bridgeeRoot = '.htm'
    bridgeDirectory = '../BMMS/'

    if not os.path.exists(bridgeDirectory+'CSV/'):
        os.makedirs(bridgeDirectory+'CSV/')

    allBridges = []
    for dirName in os.listdir(bridgeDirectory):
        superDir = bridgeDirectory+dirName+'/'
        if os.path.isdir(superDir):
            bridgesForRoad = {}
            for filename in os.listdir(superDir):
                if filename.endswith(bridgeeRoot):
                    parsed = BeautifulSoup(open(superDir+filename), 'lxml')

                    roadId = filename.split('.')[0]
                    bridgeId = filename.split('.')[1]
                    structureNr = filename.split('.')[2]

                    print ('Active: {}.{}'.format(roadId,bridgeId), end="\r")

                    if 'bcs1' in filename:
                        tables = parsed.find_all('table')

                        if parsed.find(text=re.compile('error')):
                            continue

                        if bridgeId not in bridgesForRoad:
                            bridgesForRoad[bridgeId] = newBridge()

                        bridgesForRoad[bridgeId][Constants.structureNr] = structureNr

                        data = tables[2].find_all('td')
                        bridgesForRoad[bridgeId][Constants.zone] = data[1].text.strip()
                        bridgesForRoad[bridgeId][Constants.circle] = data[3].text.strip()
                        bridgesForRoad[bridgeId][Constants.division] = data[5].text.strip()
                        bridgesForRoad[bridgeId][Constants.subDivision] = data[7].text.strip()
                        bridgesForRoad[bridgeId][Constants.road] = data[9].text.strip()
                        bridgesForRoad[bridgeId][Constants.roadName] = data[11].text.strip()
                        bridgesForRoad[bridgeId][Constants.lrpname] = data[13].text.strip()

                        data = tables[3].find_all('td')

                        try:
                            latDeg = float(data[5].text.strip()) if data[5].text.strip() != '' else 0
                            latMin = float(data[6].text.strip()) if data[6].text.strip() != '' else 0
                            latSec = float(data[7].text.strip()) if data[7].text.strip() != '' else 0
                            lonDeg = float(data[9].text.strip()) if data[9].text.strip() != '' else 0
                            lonMin = float(data[10].text.strip()) if data[10].text.strip() != '' else 0
                            lonSec = float(data[11].text.strip()) if data[11].text.strip() != '' else 0
                            bridgesForRoad[bridgeId][Constants.lat] = latDeg + latMin/60. + latSec/3600.
                            bridgesForRoad[bridgeId][Constants.lon] = lonDeg + lonMin/60. + lonSec/3600.
                        except ValueError:
                            print('Problem with latitude/longitude for bridge {} on road {}'.format(bridgeId,roadId))
                            bridgesForRoad[bridgeId][Constants.lat] = -1
                            bridgesForRoad[bridgeId][Constants.lon] = -1

                        data = tables[4].find_all('td')

                        bridgesForRoad[bridgeId][Constants.name] = data[1].text.strip()
                        try:
                            bridgesForRoad[bridgeId][Constants.chainage] = float(data[7].text.strip().replace(',','')) if data[7].text.strip() != '' else -1
                        except ValueError:
                            print('Problem with location offset for bridge {} on road {}'.format(bridgeId,roadId))

                        data = tables[5].find_all('td')

                        bridgesForRoad[bridgeId][Constants.lrpType] = data[0].text.strip()

                        data = tables[7].find_all('td')

                        bridgesForRoad[bridgeId][Constants.constructionYear] = data[3].text.strip()
                        try:
                            bridgesForRoad[bridgeId][Constants.spans] = float(data[9].text.strip().replace(',','')) if data[9].text.strip() != '' else -1
                            bridgesForRoad[bridgeId][Constants.length] = float(data[13].text.strip().replace(',','')) if data[13].text.strip() != '' else -1
                            bridgesForRoad[bridgeId][Constants.width] = float(data[15].text.strip().replace(',','')) if data[15].text.strip() != '' else -1
                        except ValueError:
                            print('Problem with construction data for bridge {} on road {}'.format(bridgeId,roadId))

                    elif 'bcs2' in filename:
                        #This file contains bridge category information only
                        if parsed.find(text=re.compile('error')):
                            continue
                        if bridgeId not in bridgesForRoad:
                            bridgesForRoad[bridgeId] = newBridge()

                        tables = parsed.find_all('table')
                        data = tables[2].find_all('td')

                        zone = data[4].text.strip()
                        circle = data[5].text.strip()
                        division = data[6].text.strip()
                        subDivision = data[7].text.strip()

                        bridgesForRoad[bridgeId][Constants.road] = roadId if bridgesForRoad[bridgeId][Constants.road] == '' else bridgesForRoad[bridgeId][Constants.road]
                        bridgesForRoad[bridgeId][Constants.zone] = zone if bridgesForRoad[bridgeId][Constants.zone] == '' else bridgesForRoad[bridgeId][Constants.zone]
                        bridgesForRoad[bridgeId][Constants.circle] = circle if bridgesForRoad[bridgeId][Constants.circle] == '' else bridgesForRoad[bridgeId][Constants.circle]
                        bridgesForRoad[bridgeId][Constants.division] = division if bridgesForRoad[bridgeId][Constants.division] == '' else bridgesForRoad[bridgeId][Constants.division]
                        bridgesForRoad[bridgeId][Constants.subDivision] = subDivision if bridgesForRoad[bridgeId][Constants.subDivision] == '' else bridgesForRoad[bridgeId][Constants.subDivision]

                        category = parsed.find('td', text=re.compile('Category')).parent.find_all('table')[0]
                        bridgesForRoad[bridgeId][Constants.condition] = category.find_all('td')[0].text.strip()

                    elif 'bcs3' in filename:
                        #potentially interesting data, if they exist
                        if parsed.find(text=re.compile('error')):
                            continue

                        if bridgeId not in bridgesForRoad:
                            bridgesForRoad[bridgeId] = newBridge()

                        mainTable = parsed.find_all('table')[1].find_all('tr')
                        rowA = mainTable[1].find_all('td')
                        rowB = mainTable[2].find_all('td')
                        rowC = mainTable[3].find_all('td')

                        zone = rowA[1].text.strip()
                        circle = rowA[3].text.strip()
                        division = rowA[5].text.strip()
                        subDivision = rowA[7].text.strip()
                        roadId = rowB[1].text.strip()
                        roadName = rowB[3].text.strip()
                        structureId = rowC[1].text.strip()
                        structureName = rowC[5].text.strip()

                        #only replace information if it is not already specified in bcs1
                        bridgesForRoad[bridgeId][Constants.zone] = zone if bridgesForRoad[bridgeId][Constants.zone] == '' else bridgesForRoad[bridgeId][Constants.zone]
                        bridgesForRoad[bridgeId][Constants.circle] = circle if bridgesForRoad[bridgeId][Constants.circle] == '' else bridgesForRoad[bridgeId][Constants.circle]
                        bridgesForRoad[bridgeId][Constants.division] = division if bridgesForRoad[bridgeId][Constants.division] == '' else bridgesForRoad[bridgeId][Constants.division]
                        bridgesForRoad[bridgeId][Constants.subDivision] = subDivision if bridgesForRoad[bridgeId][Constants.subDivision] == '' else bridgesForRoad[bridgeId][Constants.subDivision]
                        bridgesForRoad[bridgeId][Constants.road] = roadId if bridgesForRoad[bridgeId][Constants.road] == '' else bridgesForRoad[bridgeId][Constants.road]
                        bridgesForRoad[bridgeId][Constants.roadName] = roadName if bridgesForRoad[bridgeId][Constants.roadName] == '' else bridgesForRoad[bridgeId][Constants.roadName]
                        bridgesForRoad[bridgeId][Constants.structureNr] = structureId if bridgesForRoad[bridgeId][Constants.structureNr] == '' else bridgesForRoad[bridgeId][Constants.structureNr]
                        bridgesForRoad[bridgeId][Constants.name] = structureName if bridgesForRoad[bridgeId][Constants.name] == '' else bridgesForRoad[bridgeId][Constants.name]

                        try:
                            chainage = float(rowB[5].text.strip().replace(',','')) if rowB[5].text.strip() != '' else -1
                            bridgesForRoad[bridgeId][Constants.chainage] = chainage if bridgesForRoad[bridgeId][Constants.chainage] == -1 else bridgesForRoad[bridgeId][Constants.chainage]
                        except ValueError:
                            print('Problem with location chainage for bridge {} on road {}'.format(bridgeId,roadId))

                    else:
                        #not an interesting file, skip
                        continue

            #Bridges are constructed, save to file
            if not bridgesForRoad:
                #no bridges created, don't create CSV
                continue

            csvFile = dirName + '.csv'
            bridges = []
            for entry in list(bridgesForRoad.values()):
                if bridgeIsEmpty(entry):
                    continue
                bridges.append(ReadWriteCSV.Row(entry))

            allBridges.extend(bridges)
            ReadWriteCSV.writeBridges(bridges,bridgeDirectory+'CSV/'+csvFile+'.csv')

    ReadWriteCSV.writeBridges(allBridges,bridgeDirectory + 'CSV/_allBridges.csv')

    print('Completed parsing bridge data.')
