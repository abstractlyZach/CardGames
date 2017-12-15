import exceptions
import ranks
import suits


class Card(object):
    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._text

    @property
    def flavor_text(self):
        return self._flavor_text

    def __repr__(self):
        return self._name


class StandardPlayingCard(Card):
    def __init__(self, rank, suit):
        self._rank = str(rank).capitalize()
        self._suit = suit.rstrip('s').capitalize() # allows (Ace, Spade) and (Ace, Spades)
        self._check_legal_card()
        self._name = '{} of {}s'.format(self._rank[0], self._suit)
        self._text = ''
        self._flavor_text = ''

    def _check_legal_card(self):
        self._check_legal_suit()
        self._check_legal_rank()

    def _check_legal_suit(self):
        if self._suit not in suits.get_all_suits():
            raise exceptions.IllegalSuitException

    def _check_legal_rank(self):
        if self._rank not in ranks.get_all_ranks():
            raise exceptions.IllegalRankException

    # comparison operations are limited to equality. external code for game logic should be used if you're
    # comparing values. the only comparison ability cards themselves should have is knowing if they're the same card
    def __eq__(self, right):
        if isinstance(right, str): # Cards can be equated to their suit or their rank
            return self._rank == right or self._suit == right
        else:
            return self._rank == right._rank and self._suit == right._suit

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit
