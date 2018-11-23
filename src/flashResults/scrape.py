#http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
from re import split
from flashResults import parsers
from flashResults.meetPage import getAllLinks

http = urllib3.PoolManager()

def getRace(url, htmlParser='lxml'):
    table = _getTable(url)
    info = _getInfo(url, htmlParser)
    
    return {'table': table,
            'columns': list(table.columns),
            'raceInfo': info}
    
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
    url1 = 'http://flashresults.com/2017_Meets/Indoor/01-13_AggieTeam/021-1-02.htm'
    url2 = 'http://flashresults.com/2016_Meets/Indoor/02-26_SEC/026-1-01.htm'
    meetURL = 'http://flashresults.com/2016_Meets/Indoor/02-26_SEC/'
    df = getRace(url2)['table']
    df.to_pickle('practiceRaceTable.pickle')
    """
    for urls in getAllLinks(meetURL):
        for url in urls:
            print(getRace(meetURL + url)['raceInfo'])
    """