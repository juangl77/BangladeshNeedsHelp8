from ExcelWriter import ExcelWriter
from DataBuilder import DataBuilder
from BridgeIndexer import BridgeIndexer
from DataReader import DataReader
import ColumnMapping

reader = DataReader('epa1351user','xgt65RR##','epa1351group08')
indexer = BridgeIndexer(reader.readBridges())

builder = DataBuilder(reader.readRoads(), indexer, reader.readTraffic())
(objects, links, vertices) = builder.build()

ColumnMapping.init()
writer = ExcelWriter("simio.xlsx")
writer.write(objects, links, vertices)
