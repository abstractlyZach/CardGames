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

    # def __gt__(self, right):
    #     if self._rank > right._rank:
    #         return True

    def _check_legal_card(self):
        self._check_legal_suit()
        self._check_legal_rank()

    def _check_legal_suit(self):
        if self._suit not in suits.get_all_suits():
            raise IllegalSuitException

    def _check_legal_rank(self):
        if self._rank not in ranks.get_all_ranks():
            raise IllegalRankException

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
