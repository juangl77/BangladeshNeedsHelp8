from ExcelWriter import ExcelWriter
from DataBuilder import DataBuilder
from BridgeIndexer import BridgeIndexer
from DataReader import DataReader
import ColumnMapping

reader = DataReader("n1_bridges.csv", "n1_road.csv")
indexer = BridgeIndexer(reader.readBridges())

builder = DataBuilder(reader.readRoads(), indexer)
(objects, links, vertices) = builder.build()

ColumnMapping.init()
writer = ExcelWriter("simio.xlsx")
writer.write(objects, links, vertices)