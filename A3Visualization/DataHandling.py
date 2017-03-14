import os
import re
from bs4 import BeautifulSoup
import pandas

def readBridges(roadId='', filename='../WBSIM/infrastructure/BMMS_overview.xlsx'):
    return readExcel(roadId=roadId,filename=filename)

def readRoads(roadId='', filename='../WBSIM/infrastructure/_roads3.csv'):
    return readCSV(roadId=roadId,filename=filename)

def readTraffic(roadId='', filename='traffic.csv'):
    return readCSV(roadId=roadId,filename=filename)

def readWidths(roadId='', filename='widths.csv'):
    return readCSV(roadId=roadId,filename=filename)

def readCSV(roadId,filename):
    df = pandas.read_csv(filename)
    if roadId != '':
        return df[df['road']==roadId]
    else:
        return df

def readExcel(roadId,filename):
    df = pandas.read_excel(filename)
    if roadId != '':
        return df[df['road']==roadId]
    else:
        return df

def newTrafficEntry(road):
    return {
        'road':road,
        'linkNo':'',
        'name':'',
        'start_lrp':'',
        'start_offset':-42,
        'start_chainage':-42,
        'end_lrp':'',
        'end_offset':-42,
        'end_chainage':-42,
        'length':-42,
        'heavyTruck':-42,
        'mediumTruck':-42,
        'smallTruck':-42,
        'largeBus':-42,
        'mediumBus':-42,
        'microBus':-42,
        'utility':-42,
        'car':-42,
        'autoRickshaw':-42,
        'motorcycle':-42,
        'bicycle':-42,
        'cycleRickshaw':-42,
        'cart':-42,
        'totalMotorized':-42,
        'totalNonMotorized':-42,
        'total':-42
    }

def parseTrafficInfo():
    print('Entering traffic data parsing.')

    roadDirectory = '../RMMS/'
    trafficRoot = '.traffic.htm'

    allTraffic = []
    for filename in os.listdir(roadDirectory):
        if filename.endswith(trafficRoot):
            roadId = filename[:-12]
            print ('Active: {}'.format(roadId), end="\r")

            parsed = BeautifulSoup(open(roadDirectory+filename), 'lxml')
            headerRow = parsed.body.find(text=re.compile(r'List of links of')).parent.parent

            headerRow = headerRow.next_sibling.next_sibling.next_sibling.next_sibling #go to proper row in file
            roadTraffic = []

            for row in headerRow.next_siblings:
                if (row.name == 'tr'):
                    cells = row.contents
                    try:
                        traf = newTrafficEntry(roadId)
                        traf['linkNo'] = cells[1].a.text.strip()
                        traf['name'] = cells[3].text.strip()
                        traf['start_lrp'] = cells[5].text.strip()
                        traf['start_offset'] = float(cells[7].text.strip())
                        traf['start_chainage'] = float(cells[9].text.strip())
                        traf['end_lrp'] = cells[11].text.strip()
                        traf['end_offset'] = float(cells[13].text.strip())
                        traf['end_chainage'] = float(cells[15].text.strip())
                        traf['length'] = float(cells[17].text.strip())
                        traf['heavyTruck'] = float(cells[19].text.strip()) if cells[19].text.strip() != 'NS' else -1
                        traf['mediumTruck'] = float(cells[21].text.strip()) if cells[21].text.strip() != 'NS' else -1
                        traf['smallTruck'] = float(cells[23].text.strip()) if cells[23].text.strip() != 'NS' else -1
                        traf['largeBus'] = float(cells[25].text.strip()) if cells[25].text.strip() != 'NS' else -1
                        traf['mediumBus'] = float(cells[27].text.strip()) if cells[27].text.strip() != 'NS' else -1
                        traf['microBus'] = float(cells[29].text.strip()) if cells[29].text.strip() != 'NS' else -1
                        traf['utility'] = float(cells[31].text.strip()) if cells[31].text.strip() != 'NS' else -1
                        traf['car'] = float(cells[33].text.strip()) if cells[33].text.strip() != 'NS' else -1
                        traf['autoRickshaw'] = float(cells[35].text.strip()) if cells[35].text.strip() != 'NS' else -1
                        traf['motorcycle'] = float(cells[37].text.strip()) if cells[37].text.strip() != 'NS' else -1
                        traf['bicycle'] = float(cells[39].text.strip()) if cells[39].text.strip() != 'NS' else -1
                        traf['cycleRickshaw'] = float(cells[41].text.strip()) if cells[41].text.strip() != 'NS' else -1
                        traf['cart'] = float(cells[43].text.strip()) if cells[43].text.strip() != 'NS' else -1
                        traf['totalMotorized'] = float(cells[45].text.strip()) if cells[45].text.strip() != 'NS' else -1
                        traf['totalNonMotorized'] = float(cells[47].text.strip()) if cells[47].text.strip() != 'NS' else -1
                        traf['total'] = float(cells[49].text.strip()) if cells[49].text.strip() != 'NS' else -1

                        roadTraffic.append(traf)
                    except ValueError:
                        print('Couldn\'t convert float for road {}. Skipping row.'.format(roadId))
                else:
                    continue

            if len(roadTraffic) == 0:
                print('Skipping empty road {}'.format(roadId))
                continue

            allTraffic.extend(roadTraffic)

    if len(allTraffic) > 0:
        writeAllTraffic(allTraffic)

    print('Completed parsing traffic data.\n')

def writeAllTraffic(rows,filename='traffic.csv'):
    with open(filename, 'w') as fixed_csvfile:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(fixed_csvfile, fieldnames = fieldnames, dialect='excel')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def parseWidthInfo():
        print('Entering width data parsing.')

        roadDirectory = '../RMMS/'
        widthRoot = '.widths.processed.txt'

        allWidths = []
        for filename in os.listdir(roadDirectory):
            if filename.endswith(widthRoot):
                roadId = filename[:-len(widthRoot)]
                print ('Active: {}'.format(roadId), end="\r")

                widths = pandas.read_csv(roadDirectory+filename,sep='\t')
                widths.rename(columns={'roadNo':'road'},inplace=True)

                if len(widths) == 0:
                    print('Skipping empty road {}'.format(roadId))
                    continue

                allWidths.append(widths)

        if len(allWidths) > 0:
            writeAllWidths(pandas.concat(allWidths))

        print('Completed parsing width data.\n')

def writeAllWidths(rows, filename='widths.csv'):
    rows.to_csv(filename,index=False)
