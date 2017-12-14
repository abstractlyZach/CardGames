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

@pytest.fixture
def full_house_queens():
    hand = [cards.StandardPlayingCard(ranks.QUEEN, suit) for suit in [suits.DIAMOND, suits.CLOVER, suits.SPADE]]
    hand += [cards.StandardPlayingCard(ranks.SEVEN, suit) for suit in [suits.HEART, suits.SPADE]]
    return poker_hands.FullHouse(hand)

@pytest.fixture
def flush_spades():
    hand = [cards.StandardPlayingCard(rank, suits.SPADE)
            for rank in [ranks.SEVEN, ranks.QUEEN, ranks.ACE, ranks.TWO, ranks.TEN]]
    return poker_hands.Flush(hand)

@pytest.fixture
def straight():
    hand = [cards.StandardPlayingCard(rank, suits.HEART) for rank in ranks.get_all_ranks()[3:7]]
    hand.append(cards.StandardPlayingCard(ranks.NINE, suits.CLOVER))
    return poker_hands.Straight(hand)

@pytest.fixture
def three_of_a_kind():
   hand = [cards.StandardPlayingCard(ranks.SIX, suit) for suit in [suits.SPADE, suits.HEART, suits.DIAMOND]]
   hand += [cards.StandardPlayingCard(ranks.NINE, suits.CLOVER), cards.StandardPlayingCard(ranks.TWO, suits.SPADE)]
   return poker_hands.ThreeOfAKind(hand)

@pytest.fixture
def two_pair():
    hand = [cards.StandardPlayingCard(ranks.THREE, suit) for suit in suits.get_black_suits()]
    hand += [cards.StandardPlayingCard(ranks.FIVE, suit) for suit in suits.get_red_suits()]
    hand += [cards.StandardPlayingCard(ranks.QUEEN, suits.DIAMOND)]
    return poker_hands.TwoPair(hand)

@pytest.fixture
def one_pair():
    hand = [cards.StandardPlayingCard(ranks.TWO, suit) for suit in suits.get_black_suits()]
    hand += [cards.StandardPlayingCard(rank, suits.CLOVER) for rank in [ranks.QUEEN, ranks.FIVE, ranks.TEN]]
    return poker_hands.OnePair(hand)

@pytest.fixture
def high_card():
    hand = [cards.StandardPlayingCard(rank, suits.DIAMOND) for rank in ranks.get_all_ranks()[:4]]
    hand += [cards.StandardPlayingCard(ranks.TEN, suits.CLOVER)]
    return poker_hands.HighCard(hand)


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

class TestHandTrumpMechanics(object):
    def test_straight_flush_beats_four_of_a_kind(self, royal_flush_diamonds, four_of_a_kind_9s):
        straight_flush = poker_hands.StraightFlush([card for card in royal_flush_diamonds])
        four_of_a_kind = poker_hands.FourOfAKind([card for card in four_of_a_kind_9s])
        assert straight_flush > four_of_a_kind
        assert four_of_a_kind < straight_flush

    def test_four_of_a_kind_beats_full_house(self, four_of_a_kind_9s, full_house_queens):
        four_of_a_kind = poker_hands.FourOfAKind([card for card in four_of_a_kind_9s])
        full_house = poker_hands.FullHouse([card for card in full_house_queens])
        assert four_of_a_kind > full_house
        assert full_house < four_of_a_kind

    def test_full_house_beats_flush(self, full_house_queens, flush_spades):
        assert full_house_queens > flush_spades
        assert flush_spades < full_house_queens

    def test_flush_beats_straight(self, flush_spades, straight):
        assert flush_spades > straight
        assert straight < flush_spades

    def test_straight_beats_three_of_a_kind(self, straight, three_of_a_kind):
        assert straight > three_of_a_kind
        assert three_of_a_kind < straight

    def test_three_of_a_kind_beats_two_pair(self, three_of_a_kind, two_pair):
        assert three_of_a_kind > two_pair
        assert two_pair < three_of_a_kind

    def test_two_pair_beats_one_pair(self, two_pair, one_pair):
        assert two_pair > one_pair
        assert one_pair < two_pair

    def test_one_pair_beats_high_card(self, one_pair, high_card):
        assert one_pair > high_card
        assert high_card < one_pair




# def test_classify():
#     hand = []
#     first_card = cards.StandardPlayingCard(ranks.ACE, suits.CLOVER)
#     second_card = cards.StandardPlayingCard(ranks.ACE, suits.SPADE)
#     hand.append(first_card)
#     hand.append(second_card)
#     assert poker_hands.classify(hand) == poker_hands.OnePair('Ace')

# def test_straight_flush_trumps_four_of_a_kind():
#     straight_flush = poker_hands.StraightFlush([])