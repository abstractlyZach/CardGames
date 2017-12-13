import ranks
SUITS = ['Diamond', 'Clover', 'Heart', 'Spade']

class Card(object):
    @property
    def text(self):
        return self._text

    @property
    def flavor_text(self):
        return self._flavor_text

class StandardPlayingCard(Card):
    def __init__(self, rank, suit):
        self._rank = str(rank)
        self._suit = suit
        self._text = '{} of {}s'.format(self._rank, self._suit)
        self._flavor_text = ''

    # def __gt__(self, right):
    #     if self._rank > right._rank:
    #         return True

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit


