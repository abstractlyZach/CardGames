ORDERED_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

def get_all_ranks():
    return ORDERED_RANKS[:]

def get_smaller_ranks(rank):
    '''Gets the ranks that are smaller than the given rank'''
    rank_index = ORDERED_RANKS.index(rank)
    return set(ORDERED_RANKS[:rank_index])



