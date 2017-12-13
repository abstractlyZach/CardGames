import ranks
import suits


class Card(object):
    @property
    def text(self):
        return self._text

    @property
    def flavor_text(self):
        return self._flavor_text


class StandardPlayingCard(Card):
    def __init__(self, rank, suit):
        self._rank = str(rank).capitalize()
        self._suit = suit.rstrip('s').capitalize() # allows (Ace, Spade) and (Ace, Spades)
        self._check_legal_card()
        self._text = '{} of {}s'.format(self._rank, self._suit)
        self._flavor_text = ''

    def _check_legal_card(self):
        self._check_legal_suit()
        self._check_legal_rank()

    def _check_legal_suit(self):
        if self._suit not in suits.get_all_suits():
            raise IllegalSuitException

    def _check_legal_rank(self):
        if self._rank not in ranks.get_all_ranks():
            raise IllegalRankException

    def __eq__(self, right):
        return self._rank == right._rank

    def __gt__(self, right):
        lesser_ranks = ranks.get_smaller_ranks(self._rank)
        if right._rank in lesser_ranks:
            return True

    def __ge__(self, right):
        return self > right or self == right

    def __lt__(self, right):
        return not (self >= right)

    def __le__(self, right):
        return not (self > right)

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit


class IllegalSuitException(Exception):
    pass


class IllegalRankException(Exception):
    pass
