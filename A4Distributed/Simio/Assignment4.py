from ExcelWriter import ExcelWriter
from DataBuilder import DataBuilder
from BridgeIndexer import BridgeIndexer
from DataReader import DataReader
import ColumnMapping

reader = DataReader("data/bridges_n1.csv", "data/roads_n1.csv","data/widths_n1.csv", "data/traffic_n1.csv")
indexer = BridgeIndexer(reader.readBridges())

builder = DataBuilder(reader.readRoads(), indexer, reader.readTraffic())
(objects, links, vertices) = builder.build()

ColumnMapping.init()
writer = ExcelWriter("simio.xlsx")
writer.write(objects, links, vertices)
