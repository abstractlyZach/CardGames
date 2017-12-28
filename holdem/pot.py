from . import exceptions


class Pot(object):
    def __init__(self):
        self._total = 0
        self._involved_players = set()
        self._pot_complete = False

    def add_player(self, player_name):
        if self._pot_complete:
            raise exceptions.PotCompleteException
        self._involved_players.add(player_name)

    def remove_player(self, player_name):
        if self._pot_complete:
            raise exceptions.PotCompleteException
        self._involved_players.remove(player_name)

    def clear(self):
        self._total = 0

    @property
    def is_complete(self):
        return self._pot_complete

    @property
    def size(self):
        return self._total

    def add_chips(self, num_chips):
        if self._pot_complete:
            raise exceptions.PotCompleteException
        self._total += num_chips

    def complete(self):
        """Set the pot to complete. Can only be cashed in."""
        self._pot_complete = True

    def __repr__(self):
        complete_string = 'Complete' if self._pot_complete else 'Incomplete'
        format_string = '<{} Pot; {} chips; players: {}'
        return format_string.format(complete_string, self._total,
                                    self._involved_players)
