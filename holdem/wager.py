from . import exceptions


class Wager(object):
    def __init__(self, player_name):
        self._total_bet = 0
        self._all_in = False
        self._owner_name = player_name
        self._owner_folded = False

    def bet(self, amount):
        """Add chips to the current wager."""
        self._total_bet += amount

    def fold(self):
        self._owner_folded = True

    def set_all_in(self):
        self._all_in = True

    def subtract(self, amount):
        """Remove chips from this wager. For use by the bet collector for
        handling side pots."""
        self._total_bet -= amount

    @property
    def all_in(self):
        return self._all_in

    @property
    def total_bet(self):
        return self._total_bet

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def owner_folded(self):
        return self._owner_folded
