from collections import defaultdict

import exceptions


class FiveCardHand(object):
    def __init__(self, cards):
        self._cards = cards
        self._check_hand_size()
        self._count_suits()
        self._count_ranks()

    def _check_hand_size(self):
        if len(self._cards) < 5:
            raise exceptions.NotEnoughCardsException
        elif len(self._cards) > 5:
            raise exceptions.TooManyCardsException

    def _count_suits(self):
        self._suit_counts = defaultdict(int)
        for card in self._cards:
            self._suit_counts[card.suit] += 1

    def _count_ranks(self):
        self._rank_counts = defaultdict(int)
        for card in self._cards:
            self._rank_counts[card.rank] += 1

    @property
    def suit_counts(self):
        return self._suit_counts

    @property
    def rank_counts(self):
        return self._rank_counts




def classify(hand):
    rank_matches = defaultdict(int)
    for card in hand:
        rank_matches[card.rank] += 1
    for rank, number_of_matches in rank_matches.items():
        if number_of_matches == 2:
            return OnePair(rank)


class OnePair(object):
    def __init__(self, rank_of_pair):
        self._rank = rank_of_pair

    @property
    def rank(self):
        return self._rank

    def __eq__(self, other):
        return isinstance(other, OnePair) and (self._rank == other._rank)

