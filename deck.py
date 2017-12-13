import cards

class Deck(object):
    '''A collection of cards that can execute common actions, like drawing, inserting, shuffling, and scrying.'''
    def __init__(self):
        self._cards = []

    def draw(self):
        if self.num_cards <= 0:
            raise NoCardsLeftException
        else:
            pass

    def insert_to_top(self, card):
        self._cards.append(card)

    @property
    def num_cards(self):
        return len(self._cards)


class NoCardsLeftException(Exception):
    pass
