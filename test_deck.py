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

def test_top_insert_and_draw_yields_same_card(empty_deck):
    deck = empty_deck
    inserted_card = cards.Card()
    deck.insert_to_top(inserted_card)
    drawn_card = deck.draw()
    assert inserted_card is drawn_card

def test_top_insert_two_and_draw_yields_second_inserted_card(empty_deck):
    deck = empty_deck
    ace = cards.StandardPlayingCard('ace', 'spades')
    seven = cards.StandardPlayingCard(7, 'clovers')
    deck.insert_to_top(ace)
    deck.insert_to_top(seven)
    drawn_card = deck.draw()
    assert seven is drawn_card

