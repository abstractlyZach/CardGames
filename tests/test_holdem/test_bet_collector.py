import pytest

from holdem import bet_collector
from holdem import player
from holdem import exceptions


@pytest.fixture
def collector_four_players():
    players = [player.Player('Player {}'.format(i)) for i in range(4)]
    collector = bet_collector.BetCollector(players)
    collector.set_dealer(players[0])
    collector.buy_in = 10
    return collector, players

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

def test_blinds_have_7_chips(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(7)
    collector.collect_blinds()
    assert collector.table_bets == 12

def test_first_player_forgets_to_set_bet(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(15)
    collector.collect_blinds()
    with pytest.raises(exceptions.BetNotSetException):
        collector.collect_next_player()

def test_first_player_buys_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(15)
    collector.collect_blinds()
    players[3].bet(10)
    collector.collect_next_player()
    assert collector.table_bets == 25

def test_everyone_buys_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(15)
    collector.collect_blinds()
    for i in (3, 0):
        players[i].bet(10)
    players[1].bet(5)
    players[2].bet(0)
    for i in range(4):
        collector.collect_next_player()
    assert collector.table_bets == 40

def test_blinds_poor_everyone_else_buys_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for i in (0, 1, 3):
        players[i].award_chips(15)
    players[2].award_chips(4)
    collector.collect_blinds()
    players[3].bet(10)
    players[0].bet(10)
    for i in range(2):
        collector.collect_next_player()
    assert collector.table_bets == 29

def test_everyone_buys_in_but_one_person_doesnt_bet_enough(
        collector_four_players):
    collector, players = collector_four_players
    for player in players:
        player.award_chips(15)
    collector.collect_blinds()
    players[3].bet(4)
    with pytest.raises(exceptions.BetTooLowException):
        collector.collect_next_player()




