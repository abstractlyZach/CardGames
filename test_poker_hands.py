import pytest

import cards
import exceptions
import poker_hands
import ranks
import suits

@pytest.fixture
def royal_flush_diamonds():
    ace_diamonds = cards.StandardPlayingCard(ranks.ACE, suits.DIAMOND)
    king_diamonds = cards.StandardPlayingCard(ranks.KING, suits.DIAMOND)
    queen_diamonds = cards.StandardPlayingCard(ranks.QUEEN, suits.DIAMOND)
    jack_diamonds = cards.StandardPlayingCard(ranks.JACK, suits.DIAMOND)
    ten_diamonds = cards.StandardPlayingCard(ranks.TEN, suits.DIAMOND)
    hand = poker_hands.FiveCardHand([ace_diamonds, king_diamonds, queen_diamonds, jack_diamonds, ten_diamonds])
    return hand

@pytest.fixture
def four_of_a_kind_9s():
    hand = [cards.StandardPlayingCard(ranks.NINE, suit) for suit in suits.get_all_suits()]
    hand.append(cards.StandardPlayingCard(ranks.FOUR, suits.CLOVER))
    return poker_hands.FiveCardHand(hand)


class TestFiveCardHand():
    def test_init(self, royal_flush_diamonds):
        pass

    def test_raises_exception_on_4_items(self):
        with pytest.raises(exceptions.NotEnoughCardsException):
            poker_hands.FiveCardHand([1,2,3,4])

    def test_raises_exception_on_6_items(self):
        with pytest.raises(exceptions.TooManyCardsException):
            poker_hands.FiveCardHand([1,2,3,4,5,6])

    def test_suit_counts_royal_flush(self, royal_flush_diamonds):
        assert royal_flush_diamonds.suit_counts == {suits.DIAMOND: 5}

    def test_suit_counts_four_of_a_kind(self, four_of_a_kind_9s):
        expected_suit_counts = {suit: 1 for suit in suits.get_all_suits()}
        expected_suit_counts[suits.CLOVER] += 1
        assert four_of_a_kind_9s.suit_counts == expected_suit_counts

    def test_rank_counts_four_of_a_kind(self, four_of_a_kind_9s):
        expected_rank_counts = {ranks.NINE: 4, ranks.FOUR: 1}
        assert four_of_a_kind_9s.rank_counts == expected_rank_counts

    def test_rank_counts_royal_flush(self, royal_flush_diamonds):
        ranks_to_expect = [ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING, ranks.ACE]
        expected_suit_counts = {rank: 1 for rank in ranks_to_expect}
        assert royal_flush_diamonds.rank_counts == expected_suit_counts

    def test_iterator(self, royal_flush_diamonds):
        ranks_to_expect = reversed([ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING, ranks.ACE])
        cards_to_expect = [cards.StandardPlayingCard(rank, suits.DIAMOND) for rank in ranks_to_expect]
        for expected_card, actual_card in zip(cards_to_expect, royal_flush_diamonds):
            assert expected_card == actual_card


# def test_straight_flush_beats_four_of_a_kind():
#     straight_flush = poker_hands.StraightFlush(['' for i in range(5)])
#     four_of_a_kind = poker_hands.FourOfAKind(['' for i in range(5)])
#     assert straight_flush > four_of_a_kind


def test_classify():
    hand = []
    first_card = cards.StandardPlayingCard(ranks.ACE, suits.CLOVER)
    second_card = cards.StandardPlayingCard(ranks.ACE, suits.SPADE)
    hand.append(first_card)
    hand.append(second_card)
    assert poker_hands.classify(hand) == poker_hands.OnePair('Ace')

# def test_straight_flush_trumps_four_of_a_kind():
#     straight_flush = poker_hands.StraightFlush([])