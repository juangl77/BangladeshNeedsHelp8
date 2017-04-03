import pandas
from sqlalchemy import create_engine
from numpy import random
from math import floor

class BreakBridges():
    def __init__(self, username, password, database):
        self.username=username
        self.password=password
        self.database=database
        self.engine = create_engine('mysql+mysqlconnector://'+ username + ':' + password + '@localhost/'+database)

    def __writeToDatabase(self, df):
        for index, row in df.iterrows():
            sql = "UPDATE bridges SET broken = " + str(row['broken']) + " WHERE lrp = " + "'"+row['lrp']+"'"
            with self.engine.begin() as conn:     # TRANSACTION
                conn.execute(sql)

    def __isBroken(self, percentage):
        rand = random.random_sample(size=1)
        return int(rand < percentage)

    def __nextChangeTime(self):
        df = pandas.read_sql('SELECT * FROM '+self.database+'.simulationstatus', con=self.engine)
        currHour = int(df.iloc[0]['EventCount'])

        if (currHour < 0):
            print('The simulation is not currently running. Bridge status will be updated at the beginning of the next run.')
        else:
            days = floor(currHour/24)
            hours = currHour - days*24

            print('Bridge status will be updated on day {} hour {}.'.format(days, hours))

    def getBridgeList(self):
        df = pandas.read_sql('SELECT * FROM '+self.database+'.bridges', con=self.engine)
        return df

    def breakBridgesOnCategory(self, percentBroken):
        df = self.getBridgeList()
        for index in range(df.shape[0]):
            df.ix[index,'broken'] = self.__isBroken(percentBroken[df.iloc[index]['category']])

        self.__writeToDatabase(df)
        self.__nextChangeTime()

    def breakBridgesOnLRP(self,lrp,isBroken):
        df = self.getBridgeList()
        if not any(df.lrp == lrp):
            print('LRP not found. Please try again.')
            return

        df.loc[df.lrp == lrp, 'broken'] = int(isBroken)

        self.__writeToDatabase(df)
        self.__nextChangeTime()
