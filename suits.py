DIAMOND = 'Diamond'
CLOVER = 'Clover'
HEART = 'Heart'
SPADE = 'Spade'
SUITS = [DIAMOND, CLOVER, HEART, SPADE]

def get_all_suits():
    return SUITS[:]

def get_black_suits():
    return [SPADE, CLOVER]

def get_red_suits():
    return [HEART, DIAMOND]
