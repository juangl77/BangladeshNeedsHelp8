import sys

import ParseHTM
import Smoothing

shouldConvertData = '--parse-data'
if len(sys.argv)>1 and sys.argv[1] == shouldConvertData:
    ConvertHTM.convertRoadInfo()
    ConvertHTM.convertBridgeInfo()



print('Done with data cleaning.')
