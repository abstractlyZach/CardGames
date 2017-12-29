class BoardFullException(Exception):
    pass

class TooManyCardsException(Exception):
    pass

class NoPlayersException(Exception):
    pass

class PlayerNotFoundException(Exception):
    pass

class IllegalBetException(Exception):
    pass

class NotEnoughChipsException(Exception):
    pass

class BetNotSetException(Exception):
    pass

class BetTooLowException(Exception):
    pass

class WagerDecreaseException(Exception):
    pass

class PotCompleteException(Exception):
    pass

class NoValidPlayerInPotException(Exception):
    pass