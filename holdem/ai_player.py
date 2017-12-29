from . import player

class AlwaysChecksPlayer(player.Player):
    """Always checks unless he has to call to play. Never folds."""
    def __init__(self, name, bet_collector):
        super().__init__(name)
        self._bet_collector = bet_collector

    def get_bet(self):
        amount_to_bet = self._bet_collector.bet_to_match - self.check_wager()
        self.bet(amount_to_bet)