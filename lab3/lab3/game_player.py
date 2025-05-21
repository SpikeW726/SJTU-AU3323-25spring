from agent.rollout_agent import RolloutAgent
from agent.random_agent import RandomAgent
from agent.simple_heuristic_agent import SimpleHeuristicAgent
from agent.expectimax_agent import ExpectimaxAgent
from agent.mcts_agent import MCTSAgent
from agent.rl_agent import Q_LearningAgent

from game.game import Game2048
from game.ui import *
import sys


def default(string):
    return string + ' [Default: %default]'


def readCommand( argv ):
    """
    Processes the command used to run 2048 from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python main.py <options>
    """
    parser = OptionParser(usageStr)

    parser.add_option('-a', '--agent', dest='agent', type='str',
                      help=default('The agent for 2048:[expectimax/rollout/random/simpleheuristic/mcts]'),
                      default='random')
    parser.add_option('-u', '--ui', dest='ui', action='store_true',
                      help=default('Use the GUI for 2048: [True/False]'),
                      default=False)
    parser.add_option('-m', '--max', dest='max_num', type='int',
                      help=default('Max num of 2048: [Default: 2048]'),
                      default=512)
    parser.add_option('-r', '--rounds', dest='rounds', type='int',
                      help=default('Number of rounds to play: [Default: 1]'),
                      default=1)
    
                      

    options, otherjunk = parser.parse_args(argv)
    args = dict()
    args['agent'] = options.agent
    args['ui'] = options.ui
    args['max_num'] = options.max_num
    args['rounds'] = options.rounds

    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
   
    return args

if __name__ == "__main__":
    opt = readCommand(sys.argv[1:])
    print(opt)
    game = Game2048(max_value=opt['max_num'])
    game.random_init()
    
    if opt['ui']:
        ui = Game2048UI()
    else:
        ui = None   

    print("Agent:", opt['agent'])
    print('Rounds to play:', opt['rounds'])

    if opt['agent'] == 'expectimax':
        agent = ExpectimaxAgent(game=game, 
                                ui=ui
                                ) # You can also use your own agent parameters 
    elif opt['agent'] == 'rollout':
        agent = RolloutAgent(game=game, 
                             ui=ui
                             ) # You can also use your own agent parameters
    elif opt['agent'] == 'random': 
         agent = RandomAgent(game=game, ui=ui)
    elif opt['agent'] == 'simpleheuristic':
        agent = SimpleHeuristicAgent(game=game, ui=ui)
    elif opt['agent'] == 'mcts':
        agent = MCTSAgent(game=game, 
                          ui=ui
                          ) # You can also use your own agent parameters
    elif opt['agent'] == 'Q-learning':
        agent = Q_LearningAgent(ui=ui, max_num=opt['max_num'], 
                               alpha=0.1, gamma=0.9, epsilon=0.1, game=game)

    rounds_won = 0
    for _ in range(opt['rounds']):
        won = agent.play()
        if won:
            rounds_won += 1
            print("You won! [%d/%d]" % (rounds_won, opt['rounds']))
        else:
            print("You lost!")
        game.random_init()
    print("Total rounds won: [%d/%d]" % (rounds_won, opt['rounds']))

