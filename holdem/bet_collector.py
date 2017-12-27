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
        return self._table_bets

    def collect_blinds(self):
        """Collect the blind amounts and then set current bettor to the left
        of big blind."""
        self._table_bets += self.big_blind.collect_blind(self._buy_in)
        self._table_bets += self.small_blind.collect_blind(math.floor(
            self._buy_in / 2))
        self._current_bettor_index = self._next_player(self._big_blind_index)
        self._current_bet = self._buy_in

    def collect_next_player(self):
        """Collect bets for each player still in the game."""
        bet = self._players[self._current_bettor_index].collect_bet()
        self._table_bets += bet
        self._current_bettor_index = self._next_player(self._current_bettor_index)





