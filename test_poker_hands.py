import poker_hands
import cards
import ranks
import suits

def test_classify():
    hand = []
    first_card = cards.StandardPlayingCard(ranks.ACE, suits.CLOVER)
    second_card = cards.StandardPlayingCard(ranks.ACE, suits.SPADE)
    hand.append(first_card)
    hand.append(second_card)
    assert poker_hands.classify(hand) == poker_hands.OnePair('Ace')