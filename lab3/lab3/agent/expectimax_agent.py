import copy
from agent.base_agent import BaseAgent, raiseNotDefined
from agent.heuristic import exp_heuristic


# class ExpectimaxAgent(BaseAgent):
#     def __init__(self, game, ui, max_depth=5, heuristic=exp_heuristic):
#         super().__init__(game, ui)
#         self._max_depth = max_depth
#         self._heuristic = heuristic
        
#     def _get_action(self):
#         possible_actions = self._game.get_valid_actions()
#         utility_actions = {}
#         for action in possible_actions:
#             game_sim = copy.deepcopy(self._game)
#             game_sim.set_state(self._game.get_state())
#             game_sim.set_action(action)
#             game_sim.forward_player_only()
#             successor_states = game_sim.get_valid_successors()
#             utility_actions[action] = sum(self._heuristic(suc_state[0])*suc_state[1] for suc_state in successor_states)
#         action_todo, _ = max(utility_actions.items(), key=lambda k: k[1])
#         return action_todo

    # def _get_action(self):
    #     possible_actions = self._game.get_valid_actions()
    #     utility_actions = {action: 0 for action in possible_actions}
    #     for action in possible_actions:
    #         game_sim = copy.deepcopy(self._game)
    #         game_sim.set_state(self._game.get_state())
    #         game_sim.set_action(action)
    #         game_sim.forward_player_only()
    #         successor_states = game_sim.get_valid_successors()
    #         for suc_state in successor_states:
    #             game_sim.set_state(suc_state[0])
    #             possible_actions2 = game_sim.get_valid_actions()
    #             utility_actions2 = {} # 瀛樺偍绗�浜屽眰Max-agnet瀵逛簬鍥涚�峚ction鐨剈tility浼拌��
    #             if possible_actions2: # 濡傛灉杩樻湁鍙�鎵ц�岀殑琛屽姩
    #                 for action2 in possible_actions2:
    #                     game_sim_sim = copy.deepcopy(game_sim)
    #                     game_sim_sim.set_state(game_sim.get_state())
    #                     game_sim_sim.set_action(action2)
    #                     game_sim_sim.forward_player_only()
    #                     successor_states2 = game_sim_sim.get_valid_successors()
    #                     utility_actions2[action2] = sum(self._heuristic(suc_state2[0])*suc_state2[1] for suc_state2 in successor_states2)
    #                 utility_actions[action] += max(utility_actions2.values())*suc_state[1]
    #             else:
    #                 utility_actions[action] += self._heuristic(suc_state[0])*suc_state[1]
    #     action_todo, _ = max(utility_actions.items(), key=lambda k: k[1])
    #     return action_todo
class ExpectimaxAgent(BaseAgent):
    def __init__(self, game, ui, max_depth=3, heuristic=exp_heuristic):
        super().__init__(game, ui)
        self._max_depth = max_depth
        self._heuristic = heuristic


    def _get_action(self):
        current_state = self._game.get_state()
        possible_actions = self._game.get_valid_actions()
        best_action = None
        best_value = -float('inf')

        for action in possible_actions:
            # 克隆游戏状态并执行玩家移动
            game_clone = copy.deepcopy(self._game)
            game_clone.set_state(current_state)
            game_clone.set_action(action)
            game_clone.forward_player_only()
            
            # 计算期望值（进入Expect层）
            action_value = self.expectimax(game_clone, self._max_depth-1, False)
            
            if action_value > best_value:
                best_value = action_value
                best_action = action
        
        return best_action

    def expectimax(self, game, depth, is_max_player):
        # 终止条件：达到深度或游戏结束
        if depth == 0 or game.is_game_over()[0]:
            return self._heuristic(game.get_state())

        if is_max_player:
            # Max玩家层（选择最优动作）
            max_value = -float('inf')
            for action in game.get_valid_actions():
                new_game = copy.deepcopy(game)
                new_game.set_action(action)
                new_game.forward_player_only()
                
                # 进入Expect层（depth保持不变）
                value = self.expectimax(new_game, depth, False)
                max_value = max(max_value, value)
            return max_value
        else:
            # 期望层（计算所有可能新块的期望值）
            successors = game.get_valid_successors()
            expected_value = 0.0
            
            for state, prob in successors:
                new_game = copy.deepcopy(game)
                new_game.set_state(state)
                
                # 进入Max层（depth减1）
                value = self.expectimax(new_game, depth-1, True)
                expected_value += prob * value
            
            return expected_value