from holdem import ai_player
from holdem import game_runner

runner = game_runner.GameRunner()
zach = ai_player.AlwaysChecksPlayer('Zach')
josh = ai_player.AlwaysChecksPlayer('Josh')
michelle = ai_player.AlwaysChecksPlayer('Michelle')
runner.set_players([zach, michelle, josh])
runner.start()