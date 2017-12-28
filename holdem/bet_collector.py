import math
import random

from . import exceptions
from . import pot

class BetCollector(object):
    def __init__(self, players):
        if len(players) <= 0:
            raise exceptions.NoPlayersException
        self._players = players
        self.set_dealer(random.choice(self._players))
        self._current_bettor_index = self.small_blind
        self._table_bets = 0
        self._reset_pots()

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

    def _reset_pots(self):
        main_pot = pot.Pot()
        for player in self._players:
            main_pot.add_player(player.name)
        self._pots = [main_pot]

    @property
    def big_blind(self):
        return self._players[self._big_blind_index]

    @property
    def small_blind(self):
        return self._players[self._small_blind_index]

    @property
    def pots(self):
        return self._pots

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
        self._bet_to_match = self._buy_in

    def ask_next_player_for_wager(self):
        """Collect bets for each player still in the game."""
        player = self._players[self._current_bettor_index]
        wager = player.check_wager()
        if player._wager.owner_folded:
            return
        if wager < self._bet_to_match and not player.all_in:
            raise exceptions.BetTooLowException
        self._current_bettor_index = self._next_player(self._current_bettor_index)

    def collect_all_bets(self):
        self._collected_wagers = [player.collect_wager()
                                  for player in self._players]
        self._handle_folds()
        self._handle_all_ins()
        self._handle_regular_bets()
        self._collected_wagers = []

    def _handle_folds(self):
        latest_pot = self._get_incomplete_pot()
        wagers_to_remove = []
        for wager in self._collected_wagers:
            if wager.owner_folded:
                latest_pot.add_chips(wager.total_bet)
                latest_pot.remove_player(wager.owner_name)
                wagers_to_remove.append(wager)
        for wager in wagers_to_remove:
            self._collected_wagers.remove(wager)

    def _get_incomplete_pot(self):
        for pot_ in self._pots:
            if not pot_.is_complete:
                return pot_
        new_pot = pot.Pot()
        self._pots.append(new_pot)
        return new_pot

    def _handle_all_ins(self):
        all_in_wagers = []
        for wager in self._collected_wagers:
            if wager.all_in:
                all_in_wagers.append(wager)
        self._collected_wagers.sort(key=lambda x: x.total_bet)
        for all_in_wager in all_in_wagers:
            if all_in_wager.total_bet <= 0:
                continue
            latest_pot = self._get_incomplete_pot()
            non_empty_wagers = self._get_non_empty_wagers()
            for non_empty_wager in non_empty_wagers:
                latest_pot.add_chips(all_in_wager.total_bet)
                latest_pot.add_player(non_empty_wager.owner_name)
            self._deduct_from_remaining_wagers(all_in_wager.total_bet)
            latest_pot.complete()
        self._clear_empty_wagers()

    def _deduct_from_remaining_wagers(self, amount):
        for wager in self._collected_wagers:
            if wager.total_bet >= amount:
                wager.subtract(amount)

    def _handle_regular_bets(self):
        latest_pot = self._get_incomplete_pot()
        for wager in self._collected_wagers:
            latest_pot.add_chips(wager.total_bet)
            latest_pot.add_player(wager.owner_name)
        self._clear_empty_wagers()

    def _get_non_empty_wagers(self):
        return [wager for wager in self._collected_wagers
                if wager.total_bet > 0]

    def _clear_empty_wagers(self):
        wagers_to_remove = []
        for wager in self._collected_wagers:
            if wager.total_bet <= 0:
                wagers_to_remove.append(wager)
        for wager in wagers_to_remove:
            self._collected_wagers.remove(wager)


















