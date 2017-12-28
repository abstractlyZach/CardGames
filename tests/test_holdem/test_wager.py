import pytest

from holdem import wager
from holdem import exceptions

def test_init():
    wager.Wager('me')

def test_create_basic_wager():
    my_wager = wager.Wager('me')
    my_wager.bet(5)
    assert my_wager.total_bet == 5

def test_add_to_wager():
    my_wager = wager.Wager('me')
    my_wager.bet(5)
    my_wager.bet(5)
    assert my_wager.total_bet == 10
