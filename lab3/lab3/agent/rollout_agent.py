import copy
import random
from joblib import Parallel, delayed

from agent.base_agent import BaseAgent, raiseNotDefined

class RolloutAgent(BaseAgent):
    def __init__(self, game, ui, num_rollouts=1000):
        super().__init__(game, ui)
        self._num_rollouts = num_rollouts
       
    def _get_action(self):
        raiseNotDefined()
