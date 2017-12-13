
import ranks

ORDERED_RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']


def test_get_all_ranks():
    all_ranks = ranks.get_all_ranks()
    assert len(all_ranks) == 13
    for rank in all_ranks:
        assert rank in ORDERED_RANKS

def test_get_smaller_ranks():
    pass
