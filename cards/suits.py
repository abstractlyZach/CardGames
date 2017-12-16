DIAMOND = 'Diamond'
CLOVER = 'Clover'
HEART = 'Heart'
SPADE = 'Spade'
SUITS = [DIAMOND, CLOVER, HEART, SPADE]
SUIT_TO_SYMBOL = {
    SPADE: u'\u2664',
    DIAMOND: u'\u2662',
    CLOVER: u'\u2667',
    HEART: u'\u2661'
}

def get_all_suits():
    return SUITS[:]

def get_black_suits():
    return [SPADE, CLOVER]

def get_red_suits():
    return [HEART, DIAMOND]

def get_suit_symbol(suit):
    return SUIT_TO_SYMBOL[suit]

