from . import exceptions
from . import wager

class Player(object):
    def __init__(self, name):
        self._name = name
        self._cards = []
        self._chip_count = 0
        self._bet_set = False
        self._reset_wager()

    def deal_hole_card(self, card):
        """Deal a hole card to the player."""
        if len(self._cards) >= 2:
            raise exceptions.TooManyCardsException
        self._cards.append(card)

    def collect_hole_cards(self):
        """Return the hole cards and clear this player's cards."""
        hole_cards = self._cards
        self._cards = []
        return hole_cards

    def award_chips(self, chips):
        """Award chips to this player."""
        self._chip_count += chips

    def _reset_wager(self):
        self._wager = wager.Wager(self.name)

    def set_blind_wager(self, blind_amount):
        """Get a blind bet. If it forces a player to all-in, they'll give
        less than the blind amount."""
        if self._chip_count <= blind_amount:
            self._wager.bet(self._chip_count)
            self._wager.set_all_in()
            self._chip_count = 0
        else:
            self._wager.bet(blind_amount)
            self._chip_count -= blind_amount

    def bet(self, amount):
        """Add the amount to the current wager."""
        if self._chip_count < amount:
            exception_message = "{} doesn't have enough chips to " \
                                "bet {}".format(self.name, amount)
            raise exceptions.NotEnoughChipsException(exception_message)
        else:
            self._chip_count -= amount
            self._wager.bet(amount)
            if self._chip_count <= 0:
                self._wager.set_all_in()

    def check_wager(self):
        """Return the amount of the player's current wager."""
        return self._wager.total_bet

    def collect_wager(self):
        """Collect this player's wager. Should be done at the end of every
        round of betting."""
        wager = self._wager
        self._reset_wager()
        return wager

    @property
    def name(self):
        return self._name

    @property
    def chip_count(self):
        return self._chip_count

    @property
    def all_in(self):
        return self._chip_count <= 0

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        else:
            return self.name == other

    def __repr__(self):
        return '<Player: {}>'.format(self.name)
