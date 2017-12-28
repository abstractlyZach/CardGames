import pytest

from holdem import wager
from holdem import exceptions

def test_init():
    wager.Wager()

def test_create_basic_wager():
    my_wager = wager.Wager()
    my_wager.bet(5)
    assert my_wager.total_bet == 5

def test_add_to_wager():
    my_wager = wager.Wager()
    my_wager.bet(5)
    my_wager.bet(10)
    assert my_wager.total_bet == 10

def test_lower_wager():
    my_wager = wager.Wager()
    my_wager.bet(100)
    with pytest.raises(exceptions.WagerDecreaseException):
        my_wager.bet(5)
