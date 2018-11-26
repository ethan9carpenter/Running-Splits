from .constants import *

def isGender(word):
    return word in genders

def isRaceDistance(word):
    for ch in word:
        if str.isdigit(ch):
            return True
    return False

def isUnit(word):
    return word in units

def isSpecialRaceType(word):
    return word in specialRaces
    
def isRound(word):
    return word in roundType