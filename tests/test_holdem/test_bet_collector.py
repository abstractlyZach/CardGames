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

@pytest.fixture
def everyone_buys_in_for_flop():
    players = [player.Player('Player {}'.format(i)) for i in range(4)]
    collector = bet_collector.BetCollector(players)
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player_ in players:
        player_.award_chips(15)
    collector.get_blind_wagers()
    for player_ in players:
        amount_to_bet = collector.buy_in - player_.check_wager()
        player_.bet(amount_to_bet)
    for i in range(4):
        collector.ask_next_player_for_wager()
    return collector, players


def test_init():
    temp_player = player.Player('hi')
    collector = bet_collector.BetCollector([temp_player])

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
    collector.get_blind_wagers()
    assert collector.table_bets == 0

def test_blinds_buy_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(100)
    collector.get_blind_wagers()
    assert collector.table_bets == 15

def test_blinds_have_7_chips(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(7)
    collector.get_blind_wagers()
    assert collector.table_bets == 12

def test_first_player_forgets_to_set_bet(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(15)
    collector.get_blind_wagers()
    with pytest.raises(exceptions.BetTooLowException):
        collector.ask_next_player_for_wager()

def test_first_player_buys_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(15)
    collector.get_blind_wagers()
    players[3].bet(10)
    collector.ask_next_player_for_wager()
    assert collector.table_bets == 25

def test_everyone_buys_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for player in players:
        player.award_chips(15)
    collector.get_blind_wagers()
    for i in (3, 0):
        players[i].bet(10)
    players[1].bet(5)
    players[2].bet(0)
    for i in range(4):
        collector.ask_next_player_for_wager()
    assert collector.table_bets == 40

def test_blinds_poor_everyone_else_buys_in(collector_four_players):
    collector, players = collector_four_players
    collector.set_dealer(players[0])
    collector.buy_in = 10
    for i in (0, 1, 3):
        players[i].award_chips(15)
    players[2].award_chips(4)
    collector.get_blind_wagers()
    players[3].bet(10)
    players[0].bet(10)
    for i in range(2):
        collector.ask_next_player_for_wager()
    assert collector.table_bets == 29

def test_everyone_buys_in_but_one_person_doesnt_bet_enough(
        collector_four_players):
    collector, players = collector_four_players
    for player in players:
        player.award_chips(15)
    collector.get_blind_wagers()
    players[3].bet(4)
    with pytest.raises(exceptions.BetTooLowException):
        collector.ask_next_player_for_wager()

def test_only_main_pot_at_beginning_of_game(collector_four_players):
    collector, players = collector_four_players
    assert len(collector.pots) == 1

def test_pot_where_everyone_buys_in_first_round(everyone_buys_in_for_flop):
    collector, players = everyone_buys_in_for_flop
    collector.collect_all_bets()
    assert len(collector.pots) == 1
    assert collector.pots[0].size == 40

def test_one_person_folds_before_betting(collector_four_players):
    collector, players = collector_four_players
    for player in players:
        player.award_chips(15)
    collector.get_blind_wagers()
    players[3].fold()
    for i in range(3):
        player = players[i]
        amount_to_buy_in = collector.buy_in - player.check_wager()
        players[i].bet(amount_to_buy_in)
    for i in range(4):
        collector.ask_next_player_for_wager()
    collector.collect_all_bets()
    assert len(collector.pots) == 1
    assert collector.pots[0].size == 30

def test_one_player_bets_high_and_everyone_folds(collector_four_players):
    collector, players = collector_four_players
    for player in players:
        player.award_chips(15)
    collector.get_blind_wagers()
    players[3].bet(15)
    for player in players[:3]:
        player.fold()
    for i in range(4):
        collector.ask_next_player_for_wager()
    collector.collect_all_bets()
    assert len(collector.pots) == 2
    assert collector.pots[0].size == 30
    assert collector.pots[1].size == 0








