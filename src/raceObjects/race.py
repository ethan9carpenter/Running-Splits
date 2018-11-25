import pandas as pd
import numpy as np


class Race():
    def __init__(self, splitsTable, raceName):
        self.splitsTable = splitsTable
        self.raceName = raceName
        
        if 'Athlete' in self.splitsTable.columns:
            self.names = self.splitsTable['Athlete']
        elif 'Team' in self.splitsTable.columns:
            self.names = self.splitsTable['Team']
        
    def _cumulative(self):
        cumulative = pd.DataFrame()
        for _, row in self.splitsTable.iterrows():
            row = row.cumsum()
            cumulative = cumulative.append(row)
        return cumulative
    
    def _splits(self):
        return self.splitsTable
    
    def _splitDifference(self):
        df = self.splitsTable
        for column in df:
            df[column] = np.min(df[column]) - df[column] 
        return df
    
    def _cumulativeDifference(self):
        cumulative = self._splitDifference()
        for _, row in self.splitsTable.iterrows():
            row = row.cumsum()
            cumulative = cumulative.append(row)
        return cumulative
    
    def getTimes(self, how):
        if how == 'splits':
            return self._splits()
        elif how == 'splits-difference':
            return self._splitDifference()
        elif how == 'cumulative':
            return self._cumulative()
        elif how == 'cumulative-difference':
            return self._cumulativeDifference()
        
        