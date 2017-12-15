import exceptions

TWO = '2'
THREE = '3'
FOUR = '4'
FIVE = '5'
SIX = '6'
SEVEN = '7'
EIGHT = '8'
NINE = '9'
TEN = '10'
JACK = 'Jack'
QUEEN = 'Queen'
KING = 'King'
ACE = 'Ace'
ORDERED_RANKS_ACE_HIGH = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]
ORDERED_RANKS_ACE_LOW = [ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING]

def get_all_ranks():
    return ORDERED_RANKS_ACE_HIGH[:]

def get_smaller_ranks(rank):
    '''Gets the ranks that are smaller than the given rank'''
    rank_index = ORDERED_RANKS_ACE_HIGH.index(rank)
    return ORDERED_RANKS_ACE_HIGH[:rank_index]

def get_larger_ranks(rank):
    '''Gets the ranks that are larger than the given rank'''
    rank_index = ORDERED_RANKS_ACE_HIGH.index(rank)
    return ORDERED_RANKS_ACE_HIGH[rank_index + 1:]

def get_royals():
    return [TEN, JACK, QUEEN, KING, ACE]

def get_faces():
    return [JACK, QUEEN, KING]

def next_larger_rank(rank, ordered_rankings):
    rank_index = ordered_rankings.index(rank)
    if rank_index == len(ordered_rankings) - 1:
        raise exceptions.NoHigherRankException
    return ordered_rankings[rank_index + 1]