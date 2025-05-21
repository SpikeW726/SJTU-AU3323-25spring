import copy
import numpy as np

from agent.base_agent import BaseAgent
from agent.heuristic import exp_heuristic


class SimpleHeuristicAgent(BaseAgent):
    """
        This is a simple heuristic agent for the 2048 game.
    """
    def __init__(self, game, ui, heuristic=exp_heuristic):
        super().__init__(game, ui)
        self._heuristic = heuristic
    
    def _get_action(self):
        possible_actions = self._game.get_valid_actions()
        utility_actions = {}
        for action in possible_actions:
            game_sim = copy.deepcopy(self._game)
            game_sim.set_state(self._game.get_state())
            game_sim.set_action(action)
            game_sim.forward_player_only()
            utility_actions[action] = self._heuristic(game_sim.get_state())
        action_todo, _ = max(utility_actions.items(), key=lambda k: k[1])
        return action_todo
    