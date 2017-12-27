import pytest

from holdem import bet_collector
from holdem import player
from holdem import exceptions


@pytest.fixture
def collector_four_players():
    players = [player.Player('Player {}'.format(i)) for i in range(4)]
    return bet_collector.BetCollector(players), players

def test_init():
    collector = bet_collector.BetCollector(['a'])

def test_raises_exception_with_no_players_on_init():
    with pytest.raises(exceptions.NoPlayersException):
        collector = bet_collector.BetCollector([])

def test_blinds(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    assert collector.small_blind == players[1]
    assert collector.big_blind == players[2]

def test_blinds_wrap_around(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[3])
    assert collector.small_blind == players[0]
    assert collector.big_blind == players[1]

def test_blinds_broke_players(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    collector.collect_blinds()
    assert collector.table_bets == 0

def test_blinds_buy_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(100)
    collector.collect_blinds()
    assert collector.table_bets == 15




def test_everyone_buys_in(collector_four_players):
    pass
