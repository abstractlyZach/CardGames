class Pot(object):
    def __init__(self):
        self._total = 0

    def collect(self, bets):
        for amount in bets:
            self._total += amount

    def clear(self):
        self._total = 0

    @property
    def size(self):
        return self._total