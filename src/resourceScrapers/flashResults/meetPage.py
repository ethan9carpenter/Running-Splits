from bs4 import BeautifulSoup
import urllib3
from .parsers import getMeetName
from raceObjects import Meet

http = urllib3.PoolManager()

#===============================================================================
# Goes through the meet index page and parses the link for each individual race's
# results page.
#
# @param meetURL The url of main meet index page
# @param htmlParser The HTML parser that will be used by BeautifulSoup
#
# @return A list of extensions for each race in the specified meet
#===============================================================================
def _getRaces(soup):
    raceExt = []
    
    for link in soup.find_all('a'):
        link = link.get('href')

        if link and 'compiled' in link:
            raceExt.append(link)
            
    return raceExt

#===============================================================================
# Goes to the race page and finds the extension for each individual section. 
#
# @param raceExt The extension of the race who's sections will be returned
# @param meetURL The url of main meet index page
# @param htmlParser The HTML parser that will be used by BeautifulSoup 
#
# @return a list of the extensions for each section for the race specified
#===============================================================================
def _getSections(raceExt, meetURL, htmlParser='lxml'):
    url = meetURL + raceExt
    resp = http.request('GET', url)
    soup = BeautifulSoup(resp.data, htmlParser)
    
    sectionExt = []
    
    text = str(soup)

    while text.find('href') != -1:
        index = text.find('href')
        text = text[index+1:]
        link = text[4:text.find(" ")]

        if link.endswith('.htm'):
            sectionExt.append(link)
            
    return sectionExt

def _getSoup(meetURL, htmlParser='lxml'):
    resp = http.request('GET', meetURL)
    soup = BeautifulSoup(resp.data, htmlParser)
    
    return soup

#===============================================================================
# Starts with the meet index page and first parses the race pages using _getRaces
# then pulls each section with _getSections.
#
# @param meetURL The url of main meet index page
# @param htmlParser The HTML parser that will be used by BeautifulSoup 
#
# @return A list of lists.  Each nested list will be for a certain race and each
# element in the list is a section extension.
#===============================================================================
def getAllLinks(soup, meetURL, htmlParser='lxml', flat=False):
    races = _getRaces(soup)
    urlList = []
    for raceExt in races:
        sections = _getSections(raceExt, meetURL, htmlParser)
        
        if len(sections) > 0:
            if flat:
                urlList = urlList + sections
            else:
                urlList.append(sections)
    
    return urlList

def buildMeet(meetURL, flat=False, htmlParser='lxml'):
    soup = _getSoup(meetURL, htmlParser)
    links = getAllLinks(soup, meetURL, flat=flat)
    meetName = getMeetName(soup)

    pass
    
    