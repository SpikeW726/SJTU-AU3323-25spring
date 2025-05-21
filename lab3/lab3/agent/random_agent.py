import random

from agent.base_agent import BaseAgent

class RandomAgent(BaseAgent):
    def __init__(self, game, ui):
        super().__init__(game, ui)

    def _get_action(self):
        possible_actions = self._game.get_valid_actions()
        action_todo = random.choice(possible_actions)
        return action_todo

