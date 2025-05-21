import numpy as np
import math
import copy

class Q_LearningAgent:
    def __init__(self, ui, max_num, alpha, gamma, epsilon, game=None, num_episodes=500, n_actions = 4):
        self.game = game
        self.num_episodes = num_episodes
        self.Q_table = np.zeros(((int)(math.log2(max_num)**(16)), n_actions))
        self.nactions = n_actions
        self.alpha = alpha # ѧϰ��
        self.gamma = gamma # ����Gֵ(disconted return)ʱʹ�õ��ۿ���
        self.epsilon = epsilon # ��-Greedy�㷨�Ĳ���
    
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
            game_sim = copy.deepcopy(self.game) # ÿ��episode����һ��ģ����Ϸ
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
        self.train() # ѵ���õ���ÿһ�� state-action pair �� 

'''���������ǿ��ѧϰ�Ƚϸ���Ȥ, �ڿ��⻨�˵�ʱ��ѧ,�պÿ���Ҳ��ѧ�� Q-Learning, ��������ʵ��һ��
д�����﷢��2048��״̬�ռ�̫����, �����ô�ͳ�� Q-table ���ټ�¼ÿ�� state-action pair ��Qֵ,
�����������������������Ӧ��ʹ��DQN, ����������ѧϰ�ġ�ǿ��ѧϰ����ѧ��������һ�¾����������,
�����Ҿʹ�����, �ȵ�ѧ��DQN�ٻ�������һ��'''
