from collections import defaultdict

import exceptions
import ranks


class FiveCardHand(object):
    def __init__(self, cards):
        self._cards = list(cards)
        self._check_hand_size()
        self._count_suits_and_ranks()

    def _check_hand_size(self):
        if len(self._cards) < 5:
            raise exceptions.NotEnoughCardsException
        elif len(self._cards) > 5:
            raise exceptions.TooManyCardsException

    def _count_suits_and_ranks(self):
        self._suit_counts = defaultdict(int)
        self._rank_counts = defaultdict(int)
        for card in self._cards:
            self._suit_counts[card.suit] += 1
            self._rank_counts[card.rank] += 1

    @property
    def suit_counts(self):
        return self._suit_counts

    @property
    def rank_counts(self):
        return self._rank_counts

    @property
    def strength(self):
        return self._strength

    def __repr__(self):
        return 'Hand:\n' \
               '    {}\n' \
               '    {}\n' \
               '    {}\n' \
               '    {}\n' \
               '    {}\n'.format(*self._cards)

    def __iter__(self):
        for card in self._cards:
            yield card

    def __gt__(self, other):
        return self.strength > other.strength

    def __lt__(self, other):
        return self.strength < other.strength


class HighCard(FiveCardHand):
    _strength = 0

class OnePair(FiveCardHand):
    _strength = 1

class TwoPair(FiveCardHand):
    _strength = 2

class ThreeOfAKind(FiveCardHand):
    _strength = 3

class Straight(FiveCardHand):
    _strength = 4

class Flush(FiveCardHand):
    _strength = 5

class FullHouse(FiveCardHand):
    _strength = 6

class FourOfAKind(FiveCardHand):
    _strength = 7

class StraightFlush(Straight, Flush):
    _strength = 8


def next_larger_rank(rank, ordered_rankings):
    rank_index = ordered_rankings.index(rank)
    return ordered_rankings[rank_index + 1]


def is_straight_ace_low_high(five_card_hand):
    return is_straight_ace_high(five_card_hand) or is_straight_ace_low(five_card_hand)

ORDERED_RANKS_ACE_LOW = ranks.ORDERED_RANKS[:]
ORDERED_RANKS_ACE_LOW.remove(ranks.ACE)
ORDERED_RANKS_ACE_LOW.insert(0, ranks.ACE)
def is_straight_ace_low(five_card_hand):
    return _is_straight_under_ordering(five_card_hand, ORDERED_RANKS_ACE_LOW)

ORDERED_RANKS_ACE_HIGH = ranks.ORDERED_RANKS[:]
def is_straight_ace_high(five_card_hand):
    return _is_straight_under_ordering(five_card_hand, ORDERED_RANKS_ACE_HIGH)

def _is_straight_under_ordering(five_card_hand, ordering):
    hand_card_ranks = [card.rank for card in five_card_hand]
    lowest_rank = min(hand_card_ranks, key=lambda x: ordering.index(x))
    current_rank = lowest_rank
    for i in range(4):
        next_rank = next_larger_rank(current_rank, ordering)
        if next_rank not in hand_card_ranks:
            return False
        current_rank = next_rank
    return True


def classify(hand, is_straight_function=is_straight_ace_low_high):
    five_card_hand = FiveCardHand(hand)
    hand_is_straight = is_straight_function(five_card_hand)
    hand_is_flush = is_flush(five_card_hand)
    if hand_is_flush and hand_is_straight:
        return StraightFlush(five_card_hand)
    elif not hand_is_flush and hand_is_straight:
        return Straight(five_card_hand)
    elif hand_is_flush and not hand_is_straight:
        return Flush(five_card_hand)
    first_pass = _classify_first_pass(five_card_hand)
    if first_pass is not None:
        return first_pass
    else:
        return _classify_second_pass(hand)



def _classify_first_pass(five_card_hand):
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 4:
            return FourOfAKind(five_card_hand)
        if rank_count == 3:
            return _classify_card_with_3_of_same_rank(five_card_hand)
    return None

def is_flush(five_card_hand):
    for suit, suit_count in five_card_hand.suit_counts.items():
        if suit_count == 5:
            return True
    return False

def _classify_card_with_3_of_same_rank(five_card_hand):
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 2:
            return FullHouse(five_card_hand)
    return ThreeOfAKind(five_card_hand)

def _classify_second_pass(five_card_hand):
    '''Second pass of classifications. hand is guaranteed to not have full house'''
    num_pairs = 0
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 2:
            num_pairs += 1
    if num_pairs == 2:
        return TwoPair(five_card_hand)
    elif num_pairs == 1:
        return OnePair(five_card_hand)
    else:
        return HighCard(five_card_hand)


