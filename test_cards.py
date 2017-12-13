import pytest

import cards

class TestCards(object):
    def test_init(self):
        cards.StandardPlayingCard('Ace', 'Spade')

    def test_bad_suit_raises_exception(self):
        with pytest.raises(cards.IllegalSuitException):
            cards.StandardPlayingCard('ace', 'bunnies')

    def test_bad_rank_raises_exception(self):
        with pytest.raises(cards.IllegalRankException):
            cards.StandardPlayingCard('potato', 'spades')

    def test_rank(self):
        ace = cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.rank == 'Ace'

    def test_suit(self):
        ace = cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.suit == 'Spade'

    def test_text(self):
        ace = cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.text == 'Ace of Spades'

    # def test_ace_beats_2(self):
    #     ace = cards.StandardPlayingCard('Ace', 'Spade')
    #     two = cards.StandardPlayingCard('two', 'spade')






