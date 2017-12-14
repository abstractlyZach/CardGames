import pytest

import cards
import exceptions
import poker_hands
import ranks
import suits

# @pytest.fixture
# def straight_flush():
#     hand = []

class TestFiveCardHand():
    def test_init(self):
        poker_hands.FiveCardHand([1,2,3,4,5])

    def test_raises_exception_on_4_items(self):
        with pytest.raises(exceptions.NotEnoughCardsException):
            poker_hands.FiveCardHand([1,2,3,4])

    def test_raises_exception_on_6_items(self):
        with pytest.raises(exceptions.TooManyCardsException):
            poker_hands.FiveCardHand([1,2,3,4,5,6])





def test_classify():
    hand = []
    first_card = cards.StandardPlayingCard(ranks.ACE, suits.CLOVER)
    second_card = cards.StandardPlayingCard(ranks.ACE, suits.SPADE)
    hand.append(first_card)
    hand.append(second_card)
    assert poker_hands.classify(hand) == poker_hands.OnePair('Ace')

# def test_straight_flush_trumps_four_of_a_kind():
#     straight_flush = poker_hands.StraightFlush([])