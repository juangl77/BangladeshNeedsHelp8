import os
import xlsxwriter

import ColumnMapping

class ExcelWriter():
	def __init__(self, destination):
		self.destination = destination

	def clearOldFiles(self):
		try:
			os.remove(self.destination)
		except OSError:
			pass

	def write(self, objects, links, vertices):
		self.clearOldFiles()

		workbook = xlsxwriter.Workbook(self.destination)

		self.writeObjects(workbook, objects)
		self.writeLinks(workbook, links)
		self.writeVertices(workbook, vertices)

		workbook.close()

	def writeObjects(self, workbook, objects):
		header_format = workbook.add_format({
		    'bg_color': '#FFFF00',
		    'bold': True
		})

		worksheet = workbook.add_worksheet('Objects1')
		worksheet.write_row('A1', ColumnMapping.objectColumnNames,header_format)

		index = 2
		for obj in objects:
			obj.writeToWorksheet(worksheet, ColumnMapping.objectColumnMapping, index)
			index += 1

	def writeLinks(self, workbook, links):
		header_format = workbook.add_format({
		    'bg_color': '#92CDDC',
		    'bold': True
		})

		worksheet = workbook.add_worksheet('Links1')
		worksheet.write_row('A1', ColumnMapping.linkColumnNames,header_format)

		index = 2
		for link in links:
			link.writeToWorksheet(worksheet, ColumnMapping.linkColumnMapping, index)
			index += 1

	def writeVertices(self, workbook, vertices):
		header_format = workbook.add_format({
		    'bg_color': '#D8E4BC',
		    'bold': True
		})

		worksheet = workbook.add_worksheet('Vertices1')
		worksheet.write_row('A1', ColumnMapping.vertexColumnNames, header_format)

		index = 2
		for vertex in vertices:
			vertex.writeToWorksheet(worksheet, ColumnMapping.vertexColumnMapping, index)
			index += 1
