from collections import defaultdict

from . import exceptions
from . import ranks


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

    def has_matches(self):
        for rank, rank_count in self._rank_counts.items():
            if rank_count > 1:
                return True
        return False

    def get_cards_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        return sorted(self._cards, key=lambda x: ordering.index(x), reverse=True)


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
        return '{}:\n' \
               '    {}\n' \
               '    {}\n' \
               '    {}\n' \
               '    {}\n' \
               '    {}\n'.format(self.__class__.__name__, *self._cards)

    def __iter__(self):
        for card in self._cards:
            yield card

    def __gt__(self, other):
        return self.strength > other.strength

    def __lt__(self, other):
        return self.strength < other.strength


# I'm not writing the logic for comparisons between the same classes since that's very game dependent
# ex. Big 2 or a games that have Ace-high, Ace-low, or both.
# The classes are open for extension in those cases
class HighCard(FiveCardHand):
    _strength = 0

class OnePair(FiveCardHand):
    _strength = 1

    def get_pair_rank(self):
        for rank, rank_counts in self._rank_counts.items():
            if rank_counts == 2:
                return rank

    def get_kickers_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        kicker_ranks = [rank for rank, rank_count in self._rank_counts.items() if rank_count == 1]
        kickers = [card for card in self._cards if card.rank in kicker_ranks]
        return sorted(kickers, key=lambda x: ordering.index(x), reverse=True)



class TwoPair(FiveCardHand):
    _strength = 2

    def __init__(self, cards):
        super().__init__(cards)
        self._pair_ranks = None

    def get_high_pair_rank(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        if self._pair_ranks is None:
            self._find_pairs()
        return max(self._pair_ranks, key=lambda x: ordering.index(x))

    def get_low_pair_rank(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        if self._pair_ranks is None:
            self._find_pairs()
        return min(self._pair_ranks, key=lambda x: ordering.index(x))

    def _find_pairs(self):
        self._pair_ranks = []
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 2:
                self._pair_ranks.append(rank)


class ThreeOfAKind(FiveCardHand):
    _strength = 3

    def __init__(self, cards):
        super().__init__(cards)
        self._kickers = None

    def get_dominant_rank(self):
        for rank, rank_count in self.rank_counts.items():
            if rank_count == 3:
                return rank

    def get_high_kicker(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        if self._kickers is None:
            self._find_kickers()
        return max(self._kickers, key=lambda x: ordering.index(x.rank))
    def get_low_kicker(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        if self._kickers is None:
            self._find_kickers()
        return min(self._kickers, key=lambda x: ordering.index(x.rank))

    def _find_kickers(self):
        self._kickers = []
        for rank, rank_count in self.rank_counts.items():
            if rank_count == 1:
                rank_index = self._cards.index(rank)
                self._kickers.append(self._cards[rank_index])

class Straight(FiveCardHand):
    _strength = 4

    def get_high_card(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        # check if only would be high in ace-low rules
        if is_straight_ace_low(self) and not is_straight_ace_high(self):
            return ranks.FIVE
        else:
            return max(self._cards, key=lambda x: ordering.index(x))

class Flush(FiveCardHand):
    _strength = 5

    def get_cards_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        return sorted(self._cards, key=lambda x: ordering.index(x.rank), reverse=True)

class FullHouse(FiveCardHand):
    _strength = 6

    def get_triple_rank(self):
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 3:
                return rank

    def get_double_rank(self):
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 2:
                return rank

class FourOfAKind(FiveCardHand):
    _strength = 7

    def get_dominant_rank(self):
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 4:
                return rank

    def get_kicker(self):
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 1:
                kicker_rank = rank
        kicker_index = self._cards.index(kicker_rank)
        return self._cards[kicker_index]

class StraightFlush(Straight, Flush):
    _strength = 8

    def get_cards_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        # special case where Ace is low
        if is_straight_ace_low(self) and not is_straight_ace_high(self):
            return sorted(self._cards, key=lambda x: ordering.index(x.rank), reverse=True)[1:] + \
                   [card for card in self._cards if card == ranks.ACE]
        else:
            return sorted(self._cards, key=lambda x: ordering.index(x.rank), reverse=True)


def is_straight_ace_low_high(five_card_hand):
    return is_straight_ace_high(five_card_hand) or is_straight_ace_low(five_card_hand)

def is_straight_ace_low(five_card_hand):
    return _is_straight_under_ordering(five_card_hand, ranks.ORDERED_RANKS_ACE_LOW)

def is_straight_ace_high(five_card_hand):
    return _is_straight_under_ordering(five_card_hand, ranks.ORDERED_RANKS_ACE_HIGH)

def _is_straight_under_ordering(five_card_hand, ordering):
    hand_card_ranks = [card.rank for card in five_card_hand]
    lowest_rank = min(hand_card_ranks, key=lambda x: ordering.index(x))
    current_rank = lowest_rank
    try:
        for i in range(4):
            next_rank = ranks.next_larger_rank(current_rank, ordering)
            if next_rank not in hand_card_ranks:
                return False
            current_rank = next_rank
    except exceptions.NoHigherRankException:
        return False
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
    elif five_card_hand.has_matches():
        return _classify_hand_with_matches(five_card_hand)
    else:
        return HighCard(five_card_hand)

def is_flush(five_card_hand):
    for suit, suit_count in five_card_hand.suit_counts.items():
        if suit_count == 5:
            return True
    return False

def _classify_hand_with_matches(five_card_hand):
    first_pass = _classify_hand_with_matches_first_pass(five_card_hand)
    if first_pass is not None:
        return first_pass
    else:
        return _classify_hand_with_matches_second_pass(five_card_hand)

def _classify_hand_with_matches_first_pass(five_card_hand):
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 4:
            return FourOfAKind(five_card_hand)
        if rank_count == 3:
            return _classify_card_with_3_of_same_rank(five_card_hand)
    return None

def _classify_card_with_3_of_same_rank(five_card_hand):
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 2:
            return FullHouse(five_card_hand)
    return ThreeOfAKind(five_card_hand)

def _classify_hand_with_matches_second_pass(five_card_hand):
    '''Second pass of classifications. hand is guaranteed to not have more than two of a kind'''
    num_pairs = 0
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 2:
            num_pairs += 1
    if num_pairs == 2:
        return TwoPair(five_card_hand)
    else:
        return OnePair(five_card_hand)
