from collections import defaultdict


def classify(hand):
    rank_matches = defaultdict(int)
    for card in hand:
        rank_matches[card.rank] += 1
    for rank, number_of_matches in rank_matches.items():
        if number_of_matches:
            return Pair(rank)


class Pair(object):
    def __init__(self, rank_of_pair):
        self._rank = rank_of_pair

    @property
    def rank(self):
        return self._rank

    def __eq__(self, other):
        return isinstance(other, Pair) and (self._rank == other._rank)

