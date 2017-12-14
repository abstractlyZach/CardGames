import pytest

import cards
from deck import Deck, NoCardsLeftException
import ranks

@pytest.fixture
def empty_deck():
    return Deck()

@pytest.fixture
def stacked_deck():
    deck = Deck()
    for rank in ranks.get_royals():
        card = cards.StandardPlayingCard(rank, 'spade')
        deck.insert_to_top(card)
    return deck

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

def test_bottom_insert_and_draw_yields_same_card(empty_deck):
    deck = empty_deck
    inserted_card = cards.StandardPlayingCard('Jack', 'diamonds')
    deck.insert_to_bottom(inserted_card)
    drawn_card = deck.draw()
    assert inserted_card == drawn_card

def test_bottom_insert_two_and_draw_yields_first_inserted_card(empty_deck):
    deck = empty_deck
    three = cards.StandardPlayingCard('3', 'spades')
    five = cards.StandardPlayingCard('5', 'clovers')
    deck.insert_to_bottom(three)
    deck.insert_to_bottom(five)
    drawn_card = deck.draw()
    assert drawn_card == three

def test_shuffle(stacked_deck, mocker):
    shuffle = mocker.patch('deck.random.shuffle')
    stacked_deck.shuffle()
    shuffle.assert_called_once()

