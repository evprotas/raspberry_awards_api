class Interval:

    def __init__(self, producer, previousWin, followingWin, interval=None):
        self.producer = producer
        self.previousWin = previousWin
        self.followingWin = followingWin
        if interval is None:
            self.interval = followingWin - previousWin
        else:
            self.interval = interval

    def __str__(self):
        return str([self.producer, self.previousWin, self.followingWin, self.interval])