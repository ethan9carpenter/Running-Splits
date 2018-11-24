from .constants import *
from .wordCheckers import *
from re import split
from raceObjects import Race
from tools.generalParser import getTime
import numpy as np

def readRaceDetails(text):
    return text
    """
    text = str.lower(text)
    
    details = {}
    
    details['race'] = findRace(text)
    text.replace(details['race']+" ", "")
    
    
    
    words = split(" ", text)
    
    
    for word in words:
        if isGender(word):
            details['gender'] = word
        elif isUnit(word):
            details['unit'] = word
    """
            
def _findRace(text):
    for race in allRaces:
        if race in text:
            return Race
    return None

def buildTable(df):
    df = _dropNanCols(df)
    columnStartIndex = _getSplitsColStart(df)
    _parseAllTimes(df, columnStartIndex)
    
    return df

def _parseAllTimes(df, columnStartIndex):
    _parseSplits(df, columnStartIndex)
    toParse = ('Reaction Time', 'Time')
    
    for term in toParse:
        if term in df.columns:
            _parseTime(df, term)

def _parseTime(df, term):
    colIndex = df.columns.get_loc(term)
    
    for i in range(len(df.index)):
        val = df.iloc[i, colIndex]
        val = getTime(val)
        df.iloc[i, colIndex] = val

def _dropNanCols(df):
    for column in df.columns:
        if str(column) == 'nan':
            df = df.drop(column, axis=1)
    df = df[df.columns.dropna()]
    
    return df

def _parseSplits(df, columnStartIndex):
    if '[' in str(df.iloc[0][-1]):
        for i in range(len(df.index)):
            for j in range(columnStartIndex, len(df.columns)):
                val = str(df.iloc[i, j])
                start = val.find('[') + 1
                end = val.find(']')
                
                if val == 'nan':
                    val = None
                else:
                    val = val[start:end]
                    val = getTime(val)
                df.iloc[i, j] = val    
    
def _getSplitsColStart(df):
    columnStartIndex = None

    for i, cell in enumerate(df.iloc[0]):
        if '[' in str(cell):
            columnStartIndex = i
            break
    if not columnStartIndex:
        columnStartIndex
        
    return columnStartIndex