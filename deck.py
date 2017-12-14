import cards

class Deck(object):
    '''A collection of cards that can execute common actions, like drawing, inserting, shuffling, and scrying.'''
    def __init__(self):
        self._cards = []

    def draw(self, num_cards_to_draw=1):
        if self.num_cards <= 0:
            raise NoCardsLeftException
        elif num_cards_to_draw == 1:
            return self._cards.pop()
        else:
            drawn_cards = []
            for i in range(num_cards_to_draw):
                drawn_cards.append(self._cards.pop())
            return drawn_cards


    def insert_to_top(self, card):
        self._cards.append(card)

    def insert_to_bottom(self, card):
        self._cards.insert(0, card)

    @property
    def num_cards(self):
        return len(self._cards)


class NoCardsLeftException(Exception):
    pass
