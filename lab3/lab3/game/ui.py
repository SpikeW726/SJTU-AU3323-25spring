import pygame

"""
    This is the definition of 2048 UI.
    Written by: Yun Gu (yungu@ieee.org), supported by Github Copilot and DeepSeekR1.
"""
# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 500
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
FONT_SIZE = CELL_SIZE // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (187, 173, 160)
UPDATE_FPS = 30

# Colors for tiles
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

class Game2048UI:
    def __init__(self):
       self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
       pygame.display.set_caption("2048")
       self.font = pygame.font.Font(None, FONT_SIZE)
       self.score_font = pygame.font.Font(None, 30)
       self.clock = pygame.time.Clock()


    def draw(self, state, score=0):
        self.screen.fill(BG_COLOR)
        
        # Draw score
        score_text = self.score_font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = state[i][j]
                color = TILE_COLORS[value]
                rect = pygame.Rect(j*CELL_SIZE + 5, i*CELL_SIZE + 50 + 5, 
                                 CELL_SIZE - 10, CELL_SIZE - 10)
                pygame.draw.rect(self.screen, color, rect)
                
                
                if value != 0:
                    text = self.font.render(str(value), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        pygame.display.update()
        self.clock.tick(UPDATE_FPS)
