DIAMOND = 'Diamond'
CLOVER = 'Clover'
HEART = 'Heart'
SPADE = 'Spade'
SUITS = [DIAMOND, CLOVER, HEART, SPADE]

def get_all_suits():
    return set(SUITS[:])

def get_black_suits():
    return set(SPADE, CLOVER)

def get_red_suits():
    return set(HEART, DIAMOND)
