import pytest

from cards import cards
from cards.deck import Deck
from cards import exceptions
from cards import ranks
from cards import suits

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
    with pytest.raises(exceptions.NoCardsLeftException):
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
    shuffle = mocker.patch('cards.deck.random.shuffle')
    stacked_deck.shuffle()
    assert shuffle.call_count == 1

def test_remove(stacked_deck):
    stacked_deck.remove(cards.StandardPlayingCard(ranks.ACE, suits.SPADE))
    expected_cards = [cards.StandardPlayingCard(rank, suits.SPADE)
                          for rank in [ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING]]
    for expected_card in expected_cards:
        assert expected_card in stacked_deck
    assert stacked_deck.num_cards == 4

def test_remove_all_single_card(stacked_deck):
    stacked_deck.remove_all(cards.StandardPlayingCard(ranks.ACE, suits.SPADE))
    expected_cards = [cards.StandardPlayingCard(rank, suits.SPADE)
                      for rank in [ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING]]
    for expected_card in expected_cards:
        assert expected_card in stacked_deck
    assert stacked_deck.num_cards == 4

def test_remove_all_criteria(stacked_deck):
    stacked_deck.remove_all(suits.SPADE)
    assert stacked_deck.num_cards == 0

def test_remove_all_except_one(empty_deck):
    deck = empty_deck
    for i in range(5):
        deck.insert_to_top(cards.StandardPlayingCard(ranks.KING, suits.HEART))
    deck.insert_to_top(cards.StandardPlayingCard(ranks.FOUR, suits.SPADE))
    deck.shuffle()
    deck.remove_all(ranks.KING)
    assert deck.num_cards == 1
    assert deck.draw() == cards.StandardPlayingCard(ranks.FOUR, suits.SPADE)

