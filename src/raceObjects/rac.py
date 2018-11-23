
class Race():
    def __init__(self, distance, times, splits=None, unit='meters', names=None, teams=None, type=None):
        self.distance = distance
        self.times = times
        self.splits = splits
        self.unit = unit
        self.names = names
        self.teams = teams