class Pot(object):
    def __init__(self):
        self._total = 0
        self._involved_players = set()

    def collect(self, bets):
        for amount in bets:
            self._total += amount

    def add_player(self, player):
        self._involved_players.add(player)

    def remove_player(self, player):
        self._involved_players.remove(player)

    def clear(self):
        self._total = 0

    @property
    def size(self):
        return self._total