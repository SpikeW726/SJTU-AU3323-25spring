import sys

import pygame

from sudoku.sudoku_engine import SudokuGraphicsEngine

def default(string):
    return string + ' [Default: %default]'


def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = OptionParser(usageStr)

    parser.add_option('-v', '--var', dest='var', type='str',
                      help=default('The strategy of variable ordering:[next/mrv]'),
                      default='next') # 默认值为'next'
    parser.add_option('-d', '--value', dest='value', type='str',
                      help=default('The strategy of value ordering:[random/lcv]'),
                      default='random') # 默认值为'random'
    parser.add_option('-f', '--filtering', dest='filtering', type='str',
                      help=default('the filtering strategy: [forward_checking/ac1/ac3/ac4]'),
                      default='forward_checking') # 默认值为'forward_checking'
    parser.add_option('-s', '--partial_sol', dest='partial', type='str',
                      help=default('the agent TYPE in the pacmanAgents module to use'),
                      default='part_sol_1') # 默认值为'part_sol_1'

    options, otherjunk = parser.parse_args(argv) # options包含所有解析到的选项及其值，otherjunk包含未被解析的其他参数（如果存在说明命令行输入有误）
    args = dict() # 构建返回值词典
    args['var'] = options.var
    args['value'] = options.value
    args['filtering'] = options.filtering

    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    try: # 尝试从文件 partial_sol/options.partial.data 中读取第一行内容，并将其存储到 args['partial']，作为数独的初始给定的数据
        with open('partial_sol/%s.data' % options.partial) as f:
            args['partial'] = f.readline()
    except ImportError:
        print('Partial Solution [%s] does not exists!' % args['partial'])
        sys.exit(1)
    return args


if __name__ == '__main__':
    opt = readCommand(sys.argv[1:]) # opt是一个字典，键为"var" "value" "filtering" "partial"，值均为运行程序时命令行中输入的字符串
    graphics = SudokuGraphicsEngine(opt)
    graphics.run()
    pygame.quit()


