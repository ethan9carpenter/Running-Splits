import pandas as pd
import numpy as np


class Race:
    def __init__(self, splitsTable, raceName, extraInfo, names):
        self.splitsTable = pd.DataFrame(splitsTable)
        self.raceName = str(raceName)
        self.extraInfo = extraInfo
        self.names = list(names)
            
        
    def _cumulative(self):    
        cumDf = []
        for _, row in self.splitsTable.iterrows():
            cum = [row[0]]
            for time in row[1:]:
                if time is not None:
                    cumTime = cum[-1] + time
                    cum.append(cumTime)
            cumDf.append(cum)
        cumDf = pd.DataFrame(cumDf, columns=self.splitsTable.columns)

        return cumDf
    
    def _splits(self):
        return self.splitsTable
    
    def _splitDifference(self):
        df = self.splitsTable
        for column in df:
            df[column] = df[column] - np.min(df[column])
        return df
    
    def _cumulativeDifference(self):
        df = self._cumulative()
        for column in df:
            df[column] = df[column] - np.min(df[column])
        return df
    
    def getTimes(self, how):
        if how == 'splits':
            return self._splits()
        elif how == 'splits-difference':
            return self._splitDifference()
        elif how == 'cumulative':
            return self._cumulative()
        elif how == 'cumulative-difference':
            return self._cumulativeDifference()
        
    def __str__(self):
        return self.raceName