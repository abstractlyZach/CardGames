from cards import deck
from . import bet_collector
from . import board
from . import dealer
from . import exceptions
from . import player

class GameRunner(object):
    def __init__(self):
        self._starting_chips = 1000
        self._bet_collector = None
        self._deck = deck.StandardPlayingCardDeck()
        self._deck.shuffle()
        self._board = board.Board()
        self._dealer = dealer.Dealer(self._board, self._deck)
        self._players = None

    def set_players(self, players):
        self._players = players
        self._bet_collector = bet_collector.BetCollector(self._players)
        self._bet_collector.buy_in = 10

    def start(self):
        if self._players is None:
            raise exceptions.NoPlayersException
        for player in self._players:
            player.award_chips(self._starting_chips)
        self._dealer.deal_hole_cards(self._players)
        self.print_game()
        self._bet_collector.get_blind_wagers()
        self._collect_round_bets()
        self._dealer.deal_board()
        self.print_game()
        self._collect_round_bets()
        self._dealer.deal_board()
        self._collect_round_bets()

    def _collect_round_bets(self):
        while not self._bet_collector.round_over:
            self._bet_collector.ask_next_player_for_wager()
        self._bet_collector.collect_all_bets()


    def print_game(self):
        for player in self._players:
            print('=' * 10)
            print(player.info())
        print('=' * 20)
        print(self._board)



