from holdem import game_runner
from holdem import player

runner = game_runner.GameRunner()
zach = player.Player('Zach')
josh = player.Player('Josh')
michelle = player.Player('Michelle')
runner.set_players([zach, michelle, josh])
runner.start()