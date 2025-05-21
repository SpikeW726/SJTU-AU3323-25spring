"""
    This is a simple graphics implementation of sudoku game.
"""
import sys
import time

import pygame

from sudoku.sudoku_problem import Sudoku
from heuristics import *
from arc_consistency import *
from backtrack import *


def convert_grid(grid):
    cur_str = ''
    for row in grid:
        for m in row:
            cur_str += str(m)
    return cur_str


def convert_str(str_grid):
    grid = []
    for i in range(0, 9):
        cur_row = []
        for j in range(0, 9):
            cur_row.append(int(str_grid[i*9+j]) if str_grid[i*9+j] != '.' else 0)
        grid.append(cur_row)
    return grid


class SudokuGraphicsEngine:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    CELL_SIZE = 500 / 10
    COL_CHAR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    ROW_CHAR = [str(i) for i in range(1,10)]
    MOUSE_ALLOWED_MAX = (SCREEN_WIDTH - CELL_SIZE, SCREEN_WIDTH - CELL_SIZE)

    def __init__(self, opt):
        pygame.font.init()
        pygame.display.set_caption("Sudoku Simulator")
        self._screen = pygame.display.set_mode((self.SCREEN_HEIGHT, self.SCREEN_WIDTH))
        self._font = pygame.font.SysFont("Consola", 40)
        self._cell_selected = False
        self._last_cur_position = None
        self._temp_val = -1
        self.opt = opt
        list1 = []
        list1[:0] = opt['partial']
        self._grid = convert_str(list1)
        self._fixed_grid = []

        for i in range(0, len(self._grid)):
            cur_row = [x == 0 for x in self._grid[i]]
            self._fixed_grid.append(cur_row)

        self._running_flag = True

    def draw_grid(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self._grid[i][j] != 0:
                    pygame.draw.rect(self._screen, (0, 153, 153), (i * self.CELL_SIZE, j * self.CELL_SIZE,
                                                                   self.CELL_SIZE + 1, self.CELL_SIZE + 1))
                    text1 = self._font.render(str(self._grid[i][j]), True, (0, 0, 0))
                    self._screen.blit(text1, (i * self.CELL_SIZE + 15, j * self.CELL_SIZE + 15))

        for i, s in enumerate(self.COL_CHAR):
            self._screen.blit(self._font.render(s, True, (0, 0, 0)), (i * self.CELL_SIZE + self.CELL_SIZE / 2,
                                                                      self.SCREEN_WIDTH - self.CELL_SIZE * 0.8))
        for i, s in enumerate(self.ROW_CHAR):
            self._screen.blit(self._font.render(s, True, (0, 0, 0)), (self.SCREEN_WIDTH - self.CELL_SIZE * 0.8,
                                                                      i * self.CELL_SIZE + self.CELL_SIZE / 2
                                                                      ))
        for i in range(0, 10):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self._screen, (0, 0, 0), (0, i * self.CELL_SIZE),
                             (500 - self.CELL_SIZE, i * self.CELL_SIZE), thick)
            pygame.draw.line(self._screen, (0, 0, 0), (i * self.CELL_SIZE, 0),
                             (i * self.CELL_SIZE, 500 - self.CELL_SIZE), thick)

    def check_cur_val(self):
        return True

    def highlight_cell(self):
        pos = self._last_cur_position
        x = pos[0] // self.CELL_SIZE
        y = pos[1] // self.CELL_SIZE
        for i in range(2):
            pygame.draw.line(self._screen, (255, 0, 0), (x * self.CELL_SIZE - 3, (y + i) * self.CELL_SIZE),
                             (x * self.CELL_SIZE + self.CELL_SIZE + 3, (y + i) * self.CELL_SIZE), 7)
            pygame.draw.line(self._screen, (255, 0, 0), ((x + i) * self.CELL_SIZE, y * self.CELL_SIZE),
                             ((x + i) * self.CELL_SIZE, y * self.CELL_SIZE + self.CELL_SIZE), 7)

    def run(self):
        while self._running_flag:
            self._screen.fill((255, 255, 255))
            self.draw_grid()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._running_flag = False
                elif e.type == pygame.KEYDOWN:
                    if e.key in range(pygame.K_1, pygame.K_9+1):
                        self._temp_val = e.key - pygame.K_1 + 1
                    elif e.key == pygame.K_s:
                        # if self.solver is not None:
                        #     print(self.solver)
                        # else:
                        #     print('You should assign a solver!')
                        h = Sudoku(convert_grid(self._grid))
                        t = time.time()
                        print('Searching...')
                        if not backtracking_wrapper(h, self.opt): # h是个Sudoku问题（继承CSP类）的实例化；如果backtracking_wrapper函数返回的是None，即没有得到一个满足约束的解，就打印信息并退出程序
                            print('No Solution!')
                            sys.exit(1)
                        # backtracking_search(h, select_unassigned_variable=mrv, inference=mac)
                        # h.display(h.infer_assignment())
                        print('Solution Obtained via %.3f sec!' % (time.time()-t))
                        self._grid = convert_str(list(h.infer_assignment().values()))

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self._last_cur_position = pygame.mouse.get_pos()
                    self._cell_selected = True

            if self._cell_selected:
                self.highlight_cell()
                if self._temp_val != -1:
                    if self.check_cur_val():
                        pos = self._last_cur_position
                        x = pos[0] // self.CELL_SIZE
                        y = pos[1] // self.CELL_SIZE
                        if self._fixed_grid[int(x)][int(y)]:
                            self._grid[int(x)][int(y)] = self._temp_val
                    self._temp_val = -1

            pygame.display.update()


if __name__ == "__main__":
    graphics = SudokuGraphicsEngine()
    graphics.run()
    pygame.quit()
