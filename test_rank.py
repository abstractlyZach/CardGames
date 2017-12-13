
import ranks

ORDERED_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']


def test_get_all_ranks():
    all_ranks = ranks.get_all_ranks()
    assert len(all_ranks) == 13
    for rank in all_ranks:
        assert rank in ORDERED_RANKS

def test_get_smaller_ranks_single_rank():
    rank = 'Ace'
    smaller_ranks = ranks.get_smaller_ranks(rank)
    assert len(smaller_ranks) == 12

def test_get_smaller_ranks_lowest_rank_returns_empty_collection():
    rank = '2'
    smaller_ranks = ranks.get_smaller_ranks(rank)
    assert len(smaller_ranks) == 0

def test_get_smaller_ranks_all_ranks():
    for index, rank in enumerate(ORDERED_RANKS):
        smaller_ranks = ranks.get_smaller_ranks(rank)
        for lower_index in range(index):
            assert ORDERED_RANKS[lower_index] in smaller_ranks


