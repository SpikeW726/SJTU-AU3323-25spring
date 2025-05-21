import numpy as np
import math
import copy

class Q_LearningAgent:
    def __init__(self, ui, max_num, alpha, gamma, epsilon, game=None, num_episodes=500, n_actions = 4):
        self.game = game
        self.num_episodes = num_episodes
        self.Q_table = np.zeros(((int)(math.log2(max_num)**(16)), n_actions))
        self.nactions = n_actions
        self.alpha = alpha # 学习率
        self.gamma = gamma # 计算G值(disconted return)时使用的折扣率
        self.epsilon = epsilon # ε-Greedy算法的参数
    
    def update_Q(self, s0, a0, r1, s1):
        TD_error = self.Q_table[s0,a0] - (r1 + self.gamma*self.Q_table[s1].max())
        self.Q_table[s0,a0] -= self.alpha*TD_error
    
    def take_action(self, state):
        action_list = self.game._valid_actions_full
        if np.random.random() < self.nactions*self.epsilon/(self.nactions-1):
            action = np.random.randint(self.nactions)
        else:
            action = np.argmax(self.Q_table[state])
        return action_list[action]
    
    def train(self):
        for i_episode in range(self.num_episodes): 
            game_sim = copy.deepcopy(self.game) # 每个episode创建一个模拟游戏
            game_sim.set_state(self.game.get_state())
            episode_return = 0
            state = game_sim.get_state()
            action = self.take_action(state)
            done = False

            while not done:
                game_sim.set_action(action)
                next_state, reward, done = game_sim.step()
                episode_return += reward
                self.update_Q(state, action, reward, next_state)
                action = self.take_action(next_state)
                state = next_state
            
            print("Episode{} finished, return is {}".format(i_episode, episode_return))
    
    def play(self):
        np.random.seed(0)
        self.train() # 训练得到对每一个 state-action pair 的 

'''由于最近对强化学习比较感兴趣, 在课外花了点时间学,刚好课内也才学完 Q-Learning, 就想试着实现一下
写到这里发现2048的状态空间太大了, 很难用传统的 Q-table 跟踪记录每个 state-action pair 的Q值,
经过网络搜索发现这种情况应该使用DQN, 正好我正在学习的《强化学习的数学基础》下一章就是这个内容,
故暂且就此作罢, 等到学完DQN再回来尝试一下'''
