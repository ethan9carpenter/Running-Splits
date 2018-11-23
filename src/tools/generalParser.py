import re
from string import ascii_letters


def getTime(time):
    for c in ascii_letters:
        time = time.replace(c, '')
    
    if ':' not in time:
        time = str(time)
    else:
        minutes, seconds = re.split(':', time)
        time = int(minutes) * 60 + float(seconds)
    return time