import math
import random

from . import exceptions

class BetCollector(object):
    def __init__(self, players):
        if len(players) <= 0:
            raise exceptions.NoPlayersException
        self._players = players
        self.set_dealer(random.choice(self._players))
        self._current_bettor_index = self.small_blind
        self._table_bets = 0

    def set_dealer(self, target_player):
        """Sets the button and the blinds."""
        self._try_to_make_player_dealer(target_player)
        self._small_blind_index = self._next_player(self._button)
        self._big_blind_index = self._next_player(self._small_blind_index)
        self._current_bettor_index = self._small_blind_index

    def _try_to_make_player_dealer(self, target_player):
        self._button = None
        for index, player in enumerate(self._players):
            if target_player == player:
                self._button = index
        if self._button is None:
            raise exceptions.PlayerNotFoundException

    def _next_player(self, player_index):
        return (player_index + 1) % len(self._players)

    @property
    def big_blind(self):
        return self._players[self._big_blind_index]

    @property
    def small_blind(self):
        return self._players[self._small_blind_index]

    @property
    def buy_in(self):
        return self._buy_in

    @buy_in.setter
    def buy_in(self, buy_in_target):
        self._buy_in = buy_in_target

    @property
    def table_bets(self):
        return sum([player.check_wager() for player in self._players])

    def get_blind_wagers(self):
        """Collect the blind amounts and then set current bettor to the left
        of big blind."""
        self.big_blind.set_blind_wager(self._buy_in)
        self.small_blind.set_blind_wager(math.floor(self._buy_in / 2))
        self._current_bettor_index = self._next_player(self._big_blind_index)
        self._current_bet = self._buy_in

    def ask_next_player_for_wager(self):
        """Collect bets for each player still in the game."""
        player = self._players[self._current_bettor_index]
        wager = player.check_wager()
        if wager < self._current_bet and not player.all_in:
            raise exceptions.BetTooLowException
        self._current_bettor_index = self._next_player(self._current_bettor_index)





