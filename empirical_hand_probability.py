from collections import defaultdict

from cards.classify_hand import classify
from cards.deck import StandardPlayingCardDeck

poker_hand_counter = defaultdict(int)
deck = StandardPlayingCardDeck()

hands_to_draw = 5000000

for i in range(hands_to_draw):
    hand = [deck.draw() for card in range(5)]
    poker_hand = classify(hand)
    poker_hand_counter[poker_hand.__class__.__name__] += 1
    for card in poker_hand:
        deck.insert_to_bottom(card)
    deck.shuffle()


print('Out of {:,} five-card hands:'.format(hands_to_draw))
print('{:15} || {:>8} || {:6}'.format('Hand', 'Percent', 'Number of Occurrences'))
print('=' * 60)
for poker_hand, occurrences in sorted(poker_hand_counter.items(), key=lambda x:x[1], reverse=True):
    hand_occurrence_percentage = (occurrences / hands_to_draw) * 100
    print('{:15} || {:0>7.4f}% || {:8,}'.format(poker_hand, hand_occurrence_percentage, occurrences))

