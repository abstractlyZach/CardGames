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
ORDERED_RANKS = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]

def get_all_ranks():
    return ORDERED_RANKS[:]

def get_smaller_ranks(rank):
    '''Gets the ranks that are smaller than the given rank'''
    rank_index = ORDERED_RANKS.index(rank)
    return ORDERED_RANKS[:rank_index]

def get_larger_ranks(rank):
    '''Gets the ranks that are larger than the given rank'''
    rank_index = ORDERED_RANKS.index(rank)
    return ORDERED_RANKS[rank_index + 1:]

def get_royals():
    return [TEN, JACK, QUEEN, KING, ACE]

def get_faces():
    return [JACK, QUEEN, KING]



