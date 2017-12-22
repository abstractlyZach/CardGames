from cards import deck

class Board(object):
    """The "board". Holds the community cards (flop, turn, river) and the
    discard pile."""
    def __init__(self):
        self._flop = []
        self._turn = []
        self._river = []
        self._discard_pile = deck.Deck()

    @property
    def flop(self):
        return self._flop

    @flop.setter
    def flop(self, flop):
        self._flop =  flop

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        if not isinstance(turn, list):
            self._turn = [turn]
        else:
            self._turn = turn

    @property
    def river(self):
        return self._river

    @river.setter
    def river(self, river):
        if not isinstance(river, list):
            self._river = [river]
        else:
            self._river = river

    @property
    def discard_pile(self):
        return self._discard_pile

    @property
    def community_cards(self):
        all_cards = self._flop + self._turn + self._river
        return [card for card in all_cards
                if card is not None]

    @property
    def empty(self):
        return self.community_cards == []
