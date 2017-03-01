from ExcelWriter import ExcelWriter

from SimioObject import TruckObject, ChittagongObject, DhakaObject, BridgeObject
from SimioLink import SimioLink
from SimioVertex import SimioVertex

from Location import Location
import ColumnMapping

ColumnMapping.init()

writer = ExcelWriter("bridges.xlsx")

objects = [
	TruckObject(Location(0,0,0), 48),
	ChittagongObject(Location(10,0,10), 5),
	DhakaObject(Location(20,0,20)),
	BridgeObject("Bridge", Location(15,0,15), "B", 75)
]

links = [

]

vertices = [
]

writer.write(objects, links, [])