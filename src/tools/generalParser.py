import re
from string import ascii_letters
import numpy as np


def getTime(time):
    for c in ascii_letters:
        time = time.replace(c, '')
    
    if '-' in time:
        time = np.nan
    elif ':' not in time:
        time = float(time)
    else:
        minutes, seconds = re.split(':', time)
        time = int(minutes) * 60 + float(seconds)
    return time