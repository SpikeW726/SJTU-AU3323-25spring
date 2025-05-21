"""
    This is the main file of this project. DONT CHANGE THE CODE!
    We would like to thank the great efforts from CS188-UCB.
"""

import sys
from pacman.pacman import readCommand
from pacman.pacman import runGames


if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    runGames(**args)
