import pytest

import cards
from deck import Deck, NoCardsLeftException

@pytest.fixture
def empty_deck():
    return Deck()

def test_init():
    deck = Deck()

def test_empty(empty_deck):
    deck = empty_deck
    assert deck.num_cards == 0

def test_raise_exception_when_drawing_from_empty_deck(empty_deck):
    deck = empty_deck
    with pytest.raises(NoCardsLeftException):
        deck.draw()

def test_top_insert_once_into_empty_deck_increases_num_cards(empty_deck):
    deck = empty_deck
    card = cards.Card()
    deck.insert_to_top(card)
    assert deck.num_cards == 1

# def test_top_insert_and_draw_yields_same_card(empty_deck):
#     deck = empty_deck
#     card = cards.Card()

