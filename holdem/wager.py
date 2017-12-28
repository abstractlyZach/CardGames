from . import exceptions


class Wager(object):
    def __init__(self):
        self._total_bet = 0
        self._all_in = False

    def bet(self, amount):
        """Add chips to the current wager."""
        self._total_bet += amount

    def set_all_in(self):
        self._all_in = True

    @property
    def all_in(self):
        return self._all_in

    @property
    def total_bet(self):
        return self._total_bet
