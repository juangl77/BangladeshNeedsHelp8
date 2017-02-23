import sys

import ParseHTM
import Smoothing

shouldConvertData = '--parse-data'
if len(sys.argv)>1 and sys.argv[1] == shouldConvertData:
    ParseHTM.parseRoadInfo()
    ParseHTM.parseBridgeInfo()



print('Done with data cleaning.')
