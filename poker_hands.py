from collections import defaultdict

import exceptions


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


class StraightFlush(FiveCardHand):
    _strength = 8



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

