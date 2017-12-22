.. cards documentation master file, created by
   sphinx-quickstart on Wed Dec 20 15:27:52 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cards's documentation!
=================================
A project containing playgrounds for several different games.

You could see the empirical probability of each type of five-card hand::

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

Which will output something like this::

    Out of 1,000 five-card hands:
    Hand            ||  Percent || Number of Occurrences
    ============================================================
    HighCard        || 49.1000% ||      491
    OnePair         || 42.9000% ||      429
    TwoPair         || 05.0000% ||       50
    ThreeOfAKind    || 02.1000% ||       21
    Straight        || 00.5000% ||        5
    Flush           || 00.3000% ||        3
    FourOfAKind     || 00.1000% ||        1

Cards
----------
.. autoclass::cards.Cards

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
