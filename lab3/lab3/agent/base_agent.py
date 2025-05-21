import inspect

from abc import abstractmethod
import sys


class BaseAgent:
    def __init__(self, game, ui):
        self._game = game
        self._ui = ui

    def play(self):
        steps = 0
        while not self._game.is_game_over()[0]:
            action_todo = self._get_action()
            steps += 1
            self._game.set_action(action_todo)
            if self._ui:
                self._game.forward_player_only()
                self._ui.draw(self._game.get_state(),self._game.get_score())
                self._game.add_random_tile()
                self._ui.draw(self._game.get_state(),self._game.get_score())
            else:
                print("Step:", steps, "Action:", action_todo)
                self._game.forward_player_only()
                self._game.add_random_tile()
                self._game.print_state()
        return self._game.is_won()
    
    @abstractmethod
    def _get_action(self):
        pass

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)