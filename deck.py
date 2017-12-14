import cards

class Deck(object):
    '''A collection of cards that can execute common actions, like drawing, inserting, shuffling, and scrying.'''
    def __init__(self):
        self._cards = []

    def draw(self):
        if self.num_cards <= 0:
            raise NoCardsLeftException
        else:
            return self._cards.pop()

    def insert_to_top(self, card):
        self._cards.append(card)

    def insert_to_bottom(self, card):
        self._cards.insert(0, card)

    @property
    def num_cards(self):
        return len(self._cards)


class NoCardsLeftException(Exception):
    pass
