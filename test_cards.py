import cards

class TestCards(object):
    def test_init(self):
        cards.StandardPlayingCard('Ace', 'Spade')

    def test_rank(self):
        ace = cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.rank == 'Ace'

    def test_suit(self):
        ace = cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.suit == 'Spade'

    def test_text(self):
        ace = cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.text == 'Ace of Spades'

    # def test_bigger_rank_wins(self):
    #     for suit in cards.SUITS:
    #         for big_rank in cards.RANKS:
    #             big_rank_index = cards.RANKS.index(big_rank)
    #             little_rank_index = cards.RANKS[]
    #             big_card = cards.StandardPlayingCard('Ace', suit)
    #             little_card = cards.StandardPlayingCard(2, suit)
    #             assert big_card > little_card






