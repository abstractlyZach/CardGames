from . import exceptions

class Player(object):
    def __init__(self, name):
        self._name = name
        self._cards = []
        self._chip_count = 0

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

    def collect_blind(self, blind_amount):
        """Get a blind bet. If it forces a player to all-in, they'll give
        less than the blind amount."""
        if self._chip_count <= blind_amount:
            blind_bet = self._chip_count
            self._chip_count = 0
            return blind_bet
        else:
            self._chip_count -= blind_amount
            return blind_amount

    @property
    def name(self):
        return self._name

    @property
    def chip_count(self):
        return self._chip_count

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        else:
            return self.name == other

    def __repr__(self):
        return '<Player: {}>'.format(self.name)