from cards.five_card_hand import FiveCardHand
from . import exceptions
from . import ranks


# I'm not writing the logic for comparisons between the same classes since that's very game dependent
# ex. Big 2 or a games that have Ace-high, Ace-low, or both.
# The classes are open for extension in those cases
class HighCard(FiveCardHand):
    """High card hand."""
    _strength = 0

    def __repr__(self):
        high_card = self.get_cards_high_to_low()[0]
        high_card_rank = high_card.rank
        return '{} {}:\n'.format(self.__class__.__name__, high_card_rank) + self.get_cards_as_string()


class OnePair(FiveCardHand):
    """One pair hand."""
    _strength = 1

    def get_pair_rank(self):
        for rank, rank_counts in self._rank_counts.items():
            if rank_counts == 2:
                return rank

    def get_kickers_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return kickers high to low."""
        kicker_ranks = [rank for rank, rank_count in self._rank_counts.items() if rank_count == 1]
        kickers = [card for card in self._cards if card.rank in kicker_ranks]
        return sorted(kickers, key=lambda x: ordering.index(x), reverse=True)

    def __repr__(self):
        return '{} {}\n'.format(self.__class__.__name__, self.get_pair_rank() + 's') + self.get_cards_as_string()

class TwoPair(FiveCardHand):
    """Two pair hand."""
    _strength = 2

    def __init__(self, cards):
        super().__init__(cards)
        self._pair_ranks = None

    def get_high_pair_rank(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return the rank of the higher pair."""
        if self._pair_ranks is None:
            self._find_pairs()
        return max(self._pair_ranks, key=lambda x: ordering.index(x))

    def get_low_pair_rank(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return the rank of the lower pair."""
        if self._pair_ranks is None:
            self._find_pairs()
        return min(self._pair_ranks, key=lambda x: ordering.index(x))

    def _find_pairs(self):
        self._pair_ranks = []
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 2:
                self._pair_ranks.append(rank)

    def __repr__(self):
        high_pair_string = self.get_high_pair_rank() + 's'
        low_pair_string = self.get_low_pair_rank() + 's'
        class_name = self.__class__.__name__
        return '{} {} and {}:\n{}'.format(class_name, high_pair_string, low_pair_string, self.get_cards_as_string())

class ThreeOfAKind(FiveCardHand):
    """Three of kind hand."""
    _strength = 3

    def __init__(self, cards):
        super().__init__(cards)
        self._kickers = None

    def get_dominant_rank(self):
        """Return the rank of the three-of-a-kind."""
        for rank, rank_count in self.rank_counts.items():
            if rank_count == 3:
                return rank

    def get_high_kicker(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return the high kicker."""
        if self._kickers is None:
            self._find_kickers()
        return max(self._kickers, key=lambda x: ordering.index(x.rank))

    def get_low_kicker(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return the low kicker."""
        if self._kickers is None:
            self._find_kickers()
        return min(self._kickers, key=lambda x: ordering.index(x.rank))

    def _find_kickers(self):
        self._kickers = []
        for rank, rank_count in self.rank_counts.items():
            if rank_count == 1:
                rank_index = self._cards.index(rank)
                self._kickers.append(self._cards[rank_index])

    def __repr__(self):
        class_name = self.__class__.__name__
        triple_string = self.get_dominant_rank() + 's'
        card_string = self.get_cards_as_string()
        return '{} {}:\n{}'.format(class_name, triple_string, card_string)

class Straight(FiveCardHand):
    """Straight hand."""
    _strength = 4

    def get_high_card(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return the high card."""
        # check if only would be high in ace-low rules
        if is_straight_ace_low(self) and not is_straight_ace_high(self):
            return ranks.FIVE
        else:
            return max(self._cards, key=lambda x: ordering.index(x))

    def __repr__(self):
        type_of_straight = '{}-High'.format(self.get_high_card().rank)
        card_string = self.get_cards_as_string()
        return '{} Straight:\n{}'.format(type_of_straight, card_string)

class Flush(FiveCardHand):
    """Flush hand."""
    _strength = 5

    def get_cards_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return the cards from high to low."""
        return sorted(self._cards, key=lambda x: ordering.index(x.rank), reverse=True)

    def __repr__(self):
        suit = self._cards[0].rank + 's'
        card_string = self.get_cards_as_string()
        return 'Flush of {}:\n{}'.format(suit, card_string)

class FullHouse(FiveCardHand):
    """Full house hand."""
    _strength = 6

    def get_triple_rank(self):
        """Return the rank of the triple."""
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 3:
                return rank

    def get_double_rank(self):
        """Return the rank of the double."""
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 2:
                return rank

    def __repr__(self):
        triple_string = self.get_triple_rank() + 's'
        card_string = self.get_cards_as_string()
        return 'Full House of {}:\n{}'.format(triple_string, card_string)

class FourOfAKind(FiveCardHand):
    """Four of a kind hand."""
    _strength = 7

    def get_dominant_rank(self):
        """Return the rank of the four-of-a-kind."""
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 4:
                return rank

    def get_kicker(self):
        """Get the kicker."""
        for rank, rank_count in self._rank_counts.items():
            if rank_count == 1:
                kicker_rank = rank
        kicker_index = self._cards.index(kicker_rank)
        return self._cards[kicker_index]

    def __repr__(self):
        rank_string = self.get_dominant_rank() + 's'
        card_string = self.get_cards_as_string()
        return 'Four of a Kind {}:\n{}'.format(rank_string, card_string)

class StraightFlush(Straight, Flush):
    """Straight flush hand."""
    _strength = 8

    def get_cards_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return cards from highest to lowest."""
        # special case where Ace is low
        if is_straight_ace_low(self) and not is_straight_ace_high(self):
            return sorted(self._cards, key=lambda x: ordering.index(x.rank), reverse=True)[1:] + \
                   [card for card in self._cards if card == ranks.ACE]
        else:
            return sorted(self._cards, key=lambda x: ordering.index(x.rank), reverse=True)

    def __repr__(self):
        return 'Straight Flush:\n{}'.format(self.get_cards_as_string())



def is_straight_ace_low_high(five_card_hand):
    """Returns true if the straight is valid under Ace Low-High rules."""
    return is_straight_ace_high(five_card_hand) or is_straight_ace_low(five_card_hand)

def is_straight_ace_low(five_card_hand):
    """Returns true if the straight is valid under Ace Low rules."""
    return _is_straight_under_ordering(five_card_hand, ranks.ORDERED_RANKS_ACE_LOW)

def is_straight_ace_high(five_card_hand):
    """Returns true if the straight is valid under Ace High rules."""
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
    """Takes a list of cards or a FiveCardHand and classifies it as one of the poker hands,
    returning an object of that type containing the given cards."""
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
    """Return true if the hand is a flush."""
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
