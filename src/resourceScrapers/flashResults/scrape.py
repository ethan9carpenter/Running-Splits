#http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
from flashResults import parsers
import numpy as np
from raceObjects import Race
from .constants import columns as colsToDrop

http = urllib3.PoolManager()

def getRace(url, htmlParser='lxml', dropOutliers=True):
    table = _getTable(url)
    title = _getTitle(url, htmlParser)
    names = _getNames(table)
    splits, extraInfo = _keepSplits(table)
    
    if dropOutliers:
        table = _dropOutliers(table)
    
    return Race(splits, title, extraInfo, names)

def _keepSplits(df):
    extraInfo = pd.DataFrame()
    for col in colsToDrop:
        if col in df.columns:
            extraInfo[col] = df[col]
            df.drop(col, axis=1, inplace=True)
            
    return df, extraInfo

def _getNames(df):
    if 'Athlete' in df.columns:
        names = df['Athlete']
    elif 'Team' in df.columns:
        names = df['Team']
    else:
        names = pd.Series()
    
    return names

def _dropOutliers(table):
    for column in table.columns:
        try:
            table[column] = [np.abs(table[column]-table[column].mean()) <= 3*table[column].std()]
        except ValueError:
            pass
    return table
    
def _getTitle(url, htmlParser='lxml'):
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, htmlParser)
    soup = soup.find('table')
    text = str(soup)
    start = text.find('<td>') + 4
    end = text.find('</td>')
    text = text[start:end]
    
    content = parsers.readRaceDetails(text)
            
    return content

def _getTable(url):
    df = pd.read_html(url)[2]
    
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(0, inplace=True)
    
    df = parsers.buildTable(df)
    
    return df

if __name__ == '__main__':
    print(_getTable('http://www.flashresults.com/2017_Meets/Outdoor/06-29_TTSSFO/107-1-01.htm'))