import csv
from shutil import copyfile
import xlsxwriter

import Constants

def readBridges(filename='../BMMS/CSV/_allBridges.csv'):
    rows = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    return rows

def writeBridges(rows,filename):
    with open(filename, 'w') as fixed_csvfile:
        fieldnames = [Constants.road,Constants.km,Constants.lrpType,Constants.lrpname,Constants.name,
            Constants.length,Constants.condition,Constants.structureNr,Constants.roadName,
            Constants.chainage,Constants.width,Constants.constructionYear,Constants.spans,
            Constants.zone,Constants.circle,Constants.division,Constants.subDivision,Constants.lat,Constants.lon]
        writer = csv.DictWriter(fixed_csvfile, fieldnames = fieldnames, dialect='excel')
        writer.writeheader()
        for row in rows:
            writer.writerow(row.data)

def writeBridgesFinal(source, destination):
    rows = []
    with open(source) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    fieldnames = [Constants.road,Constants.km,Constants.lrpType,Constants.lrpname,Constants.name,
        Constants.length,Constants.condition,Constants.structureNr,
        Constants.roadName,Constants.chainage,Constants.width,Constants.constructionYear,
        Constants.spans,Constants.zone,Constants.circle,Constants.division,
        Constants.subDivision,Constants.lat,Constants.lon,Constants.estimatedLoc]

    workbook = xlsxwriter.Workbook(destination)
    worksheet = workbook.add_worksheet()

    worksheet.write_row('A1',fieldnames)
    for index, row in enumerate(rows):
        if index == 0:
            continue
        worksheet.write_string('A{}'.format(index+1),row[Constants.road])
        worksheet.write_number('B{}'.format(index+1),float(row[Constants.chainage]) if row[Constants.chainage] != '' else -1)
        worksheet.write_string('C{}'.format(index+1),row[Constants.lrpType])
        worksheet.write_string('D{}'.format(index+1),row[Constants.lrpname])
        worksheet.write_string('E{}'.format(index+1),row[Constants.name])
        worksheet.write_number('F{}'.format(index+1),float(row[Constants.length]) if row[Constants.length] != '' else -1)
        worksheet.write_string('G{}'.format(index+1),row[Constants.condition])
        worksheet.write_number('H{}'.format(index+1),float(row[Constants.structureNr]) if row[Constants.structureNr] != '' else -1)
        worksheet.write_string('I{}'.format(index+1),row[Constants.roadName])
        worksheet.write_number('J{}'.format(index+1),float(row[Constants.chainage]) if row[Constants.chainage] != '' else -1)
        worksheet.write_number('K{}'.format(index+1),float(row[Constants.width]) if row[Constants.width] != '' else -1)
        worksheet.write_number('L{}'.format(index+1),int(row[Constants.constructionYear]) if row[Constants.constructionYear] != '' else -1)
        worksheet.write_number('M{}'.format(index+1),float(row[Constants.spans]) if row[Constants.spans] != '' else -1)
        worksheet.write_string('N{}'.format(index+1),row[Constants.zone])
        worksheet.write_string('O{}'.format(index+1),row[Constants.circle])
        worksheet.write_string('P{}'.format(index+1),row[Constants.division])
        worksheet.write_string('Q{}'.format(index+1),row[Constants.subDivision])
        worksheet.write_number('R{}'.format(index+1),float(row[Constants.lat]) if row[Constants.lat] != '' else -1)
        worksheet.write_number('S{}'.format(index+1),float(row[Constants.lon]) if row[Constants.lon] != '' else -1)
        worksheet.write_string('T{}'.format(index+1),'')

    workbook.close()

def readRoads(filename='../RMMS/CSV/_allRoads.csv'):
    rows = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    return rows

def writeRoads(rows,filename):
    with open(filename, 'w') as fixed_csvfile:
        fieldnames = [Constants.road,Constants.chainage,Constants.lrp,Constants.lat,Constants.lon,Constants.lrpType,Constants.name]
        writer = csv.DictWriter(fixed_csvfile, fieldnames = fieldnames, dialect='excel')
        writer.writeheader()
        for row in rows:
            writer.writerow(row.data)

def writeRoadsFinal(source, destination):
    copyfile(source,destination)
