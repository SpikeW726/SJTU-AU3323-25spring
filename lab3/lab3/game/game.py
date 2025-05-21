import copy
import random
import numpy as np

"""
    This is the definition of 2048 Game.
    Written by: Yun Gu (yungu@ieee.org), supported by Github Copilot.
"""
class Game:
    def __init__(self):
        pass
    
    def set_action(self, action:str):
        """
            Set the action to the game.
        """
        pass

    def set_state(self, state:list):
        """
            Set the state of the game.
        """
        pass

    def get_state(self):
        """
            Get the state of the game.
        """
        pass

class Game2048(Game):
    def __init__(self, max_value=2048, prob_two=0.9):
        self._state: list = [[0 for _ in range(4)] for _ in range(4)] # 4x4 matrix
        self._valid_actions_full = ['U', 'D', 'L', 'R']
        self._max_value = max_value
        self._cur_val = -1
        self._total_score = 0
        self._PROB_TWO = prob_two


    def get_score(self):
        return self._total_score
    
    def start(self):
        """
            Start the game.
        """
        self.random_init()
        self.print_state()
        while True:
            action = input("Enter action %s: " %self.get_valid_actions().__str__())
            self.set_action(action)
            self.forward()
            self.print_state()

            if self.is_game_over():
                print("Game Over!")
                break
    
    def is_game_over(self):
        """
            Check whether the game is over.
        """
        self._cur_val = np.max(self._state)
        if self._cur_val == self._max_value:
            return True, self._max_value, self._total_score
        for action in self._valid_actions_full:
            if self.is_valid_action(action):
                return False, self._cur_val, self._total_score
        return True, self._cur_val, self._total_score
    
    def is_won(self):
        """
            Check whether the game is won.
        """
        if self._cur_val == self._max_value:
            return True
        return False
  
    def is_valid_action(self, action:str):
        """
            Check whether the action is valid.
        """
        if action not in self._valid_actions_full:
            return False
        if action == 'U':
            return self.can_move_up()
        elif action == 'D':
            return self.can_move_down()
        elif action == 'L':
            return self.can_move_left()
        elif action == 'R':
            return self.can_move_right()
        else:
            raise ValueError("Invalid action.")
               
    def can_move_up(self):
        """
            Check whether the game can move up.
            A. when the game can merge, return True.
            B. when the game can move up (there is an empty cell), return True.
            else, return False.
        """
        state = [list(row) for row in zip(*self._state)]
        for i in range(4):
            if self.can_merge(state[i]):
                return True
        for i in range(4):
            if 0 in state[i] and not all(state[i][j] == 0 for j in range(state[i].index(0)+1, 4)):
                return True
        return False
    def can_move_down(self):
        state = [list(row) for row in zip(*self._state)]
        for i in range(4):
            if self.can_merge(state[i][::-1]):
                return True
        for i in range(4):
            for j in range(4):
                if state[i][j] == 0 and not all(state[i][k] for k in range(4-j+1, 4)):
                    return True
        return False
    def can_move_left(self):
        for i in range(4):
            if self.can_merge(self._state[i]):
                return True
        for i in range(4):
            if 0 in self._state[i] and not all(self._state[i][j] == 0 for j in range(self._state[i].index(0)+1, 4)):
                return True
        return False
    def can_move_right(self):
        for i in range(4):
            if self.can_merge(self._state[i][::-1]):
                return True
        for i in range(4):
            for j in range(4):
                if self._state[i][j] == 0 and not all(self._state[i][k] for k in range(4-j+1, 4)):
                    return True
        return False    
    def can_merge(self, row):
        """
            Check whether the row can be merged.
        """
        row = [i for i in row if i != 0]
        for i in range(len(row)-1):
            if row[i] == row[i+1]:
                return True
        return

    def get_valid_actions(self, role:str = 'Player'):
        """
            Return the list of valid actions.
            For 2024, we need to confirm whether the move ?
        """
        if role == 'Player':
            valid_actions = []
            for action in self._valid_actions_full:
                if self.is_valid_action(action):
                    valid_actions.append(action)
            return valid_actions
        elif role == 'RandTile':
            valid_actions = []
            for action in self._valid_actions_full:
                if self.is_valid_action(action):
                    valid_actions.append(action)
            return valid_actions
        
    def get_valid_successors(self):
        """
            Get all valid successors of the current state.
            The successors are the states after the player moves.
        """
        all_possible_successors = []
        for i in range(4):
            for j in range(4):
                if self._state[i][j] == 0:
                    zero_state = copy.deepcopy(self._state)
                    zero_state[i][j] = 2
                    all_possible_successors.append([zero_state, self._PROB_TWO])
                    zero_state = copy.deepcopy(self._state)
                    zero_state[i][j] = 4
                    all_possible_successors.append([zero_state, 1.0 - self._PROB_TWO])
        num_successors = len(all_possible_successors)
        for i in range(num_successors):
            all_possible_successors[i][1] /= (0.5 * num_successors)
        return all_possible_successors

    def set_action(self, action:str):
        """
            Set the action to the game.
        """
        if not self.is_valid_action(action):
            raise ValueError("Invalid action.")
        self._action = action
    
    def forward(self):
        """
            Move the game state forward.
        """
        self.forward_player_only() # move the player
        self.add_random_tile() # add a random number [2/4]
    
    def forward_player_only(self):
        if self._action == 'U':
            self.move_up()
        elif self._action == 'D':
            self.move_down()
        elif self._action == 'L':
            self.move_left()
        elif self._action == 'R':
            self.move_right()
        else:
            raise ValueError("Invalid action.")
        
    def move_up(self):
        self._state = [list(row) for row in zip(*self._state)] # 转置，然后上下移动合并列元素就也能调用merge函数了
        for i in range(4):
            self._state[i] = self.merge(self._state[i]) # merge the row
        self._state = [list(row) for row in zip(*self._state)] # 最后再转置一次还原

    def move_down(self):
        self._state = [list(row) for row in zip(*self._state)]
        for i in range(4):
            self._state[i] = self.merge(self._state[i][::-1])[::-1]
        self._state = [list(row) for row in zip(*self._state)]

    def move_left(self):
        for i in range(4):
            self._state[i] = self.merge(self._state[i])
    
    def move_right(self):
        for i in range(4):
            self._state[i] = self.merge(self._state[i][::-1])[::-1]

    def random_init(self):
        """
            Randomly initialize the game state.
        """
        self._state: list = [[0 for _ in range(4)] for _ in range(4)] # 4x4 matrix
        self._total_score = 0
        self.add_random_tile()
        self.add_random_tile()
    
    def get_state(self):
        return self._state
    
    def set_state(self, state:list):
        for i in range(0,4):
            for j in range(0,4):
                self._state[i][j] = state[i][j]

    def print_state(self):
        for row in self._state:
            print(row)
        
    def merge(self, row):
        """
            Merge the row.
        """
        row = [i for i in row if i != 0]
        for i in range(len(row)-1):
            if row[i] == row[i+1]:
                row[i] *= 2
                self._total_score += row[i]
                row[i+1] = 0
        row = [i for i in row if i != 0]
        row += [0] * (4 - len(row))
        return row
    
    def add_random_tile(self):
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self._state[i][j] == 0:
                    empty_cells.append((i, j))
        if empty_cells:
            row, col = random.choice(empty_cells)
            self._state[row][col] = 2 if random.random() < self._PROB_TWO else 4
        else:
            raise ValueError("No empty cell.")
    
    def step(self):
        last_score = self._total_score # 记录执行此步前的总分数
        self.forward_player_only() 
        self.add_random_tile() 
        reward = self._total_score - last_score - 2 # reward为执行此步获得的分数-每走一步的消耗
        is_done = self.is_game_over()
        # 如果这一步导致游戏结束了，reward就要加上游戏成功的奖励或减去游戏失败的惩罚
        if is_done:
            if self.is_won(): reward += 256 
            else: reward -= 256     
        return self._state, reward, is_done

# 这个文件的主函数是干啥用的？
if __name__ == "__main__":
    # Game2048().start()
    game = Game2048()
    game.random_init()
    game_sim = Game2048()
    sim_rounds = 50
    steps = 0
    while not game.is_game_over()[0]:
        possible_actions = game.get_valid_actions()
        utility_actions = {}
        for action in possible_actions:
            utility_actions[action] = 0

            for round in range(0,sim_rounds):
                game_sim.set_state(game.get_state())
                game_sim.set_action(action)
                game_sim.forward()
                while True:
                    over, state_val = game_sim.is_game_over()
                    if over:
                        utility_actions[action] += state_val
                        break
                    else:
                        possible_actions_sim = game_sim.get_valid_actions()
                        if possible_actions_sim:
                            action_sim = random.choice(possible_actions_sim)
                            game_sim.set_action(action_sim)
                            game_sim.forward()
            utility_actions[action] = utility_actions[action] * 1.0 / sim_rounds
        action_todo, val = max(utility_actions.items(), key=lambda k: k[1])
        print(steps, action_todo)
        steps += 1
        game.set_action(action_todo)
        game.forward()
        game.print_state()
    