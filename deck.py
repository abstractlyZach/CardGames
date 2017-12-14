import cards
import exceptions
import ranks
import suits


class Deck(object):
    '''A collection of cards that can execute common actions, like drawing, inserting, and shuffling'''
    def __init__(self):
        self._cards = []

    def draw(self):
        if self.num_cards <= 0:
            raise exceptions.NoCardsLeftException
        else:
            return self._cards.pop()

    def insert_to_top(self, card):
        self._cards.append(card)

    def insert_to_bottom(self, card):
        self._cards.insert(0, card)

    @property
    def num_cards(self):
        return len(self._cards)


class StandardPlayingCardDeck(Deck):
    def __init__(self):
        super().__init__()
        for rank in ranks.get_all_ranks():
            for suit in suits.get_all_suits():
                self._cards.append(cards.StandardPlayingCard(rank, suit))
