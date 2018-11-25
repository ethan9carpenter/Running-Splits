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
    info = _getInfo(url, htmlParser)
    extraInfo = pd.DataFrame()
    names = pd.Series()
    
    if dropOutliers:
        for column in table.columns:
            try:
                table[column] = [np.abs(table[column]-table[column].mean()) <= (3*table[column].std())]
            except:
                pass
            
    if 'Athlete' in table.columns:
        names = table['Athlete']
    elif 'Team' in table.columns:
        names = table['Team']
            
    for col in colsToDrop:
        if col in table.columns:
            extraInfo[col] = table[col]
            table.drop(col, axis=1, inplace=True)
    
    
    return Race(table, info, extraInfo, names)
    
def _getInfo(url, htmlParser='lxml'):
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