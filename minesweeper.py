"""
Minesweeper Game using Pygame

Author: Chris Shiman
Emoji icons by Illosalz
"""

import pygame
import sys
import random
import ctypes
import time

pygame.init()
pygame.mixer.init()

# Hide console window (Windows)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
DARK_GRAY = (80, 80, 80)
DARKER_GRAY = (50, 50, 50)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
MAROON = (128, 0, 0)
TURQUOISE = (64, 224, 208)
ORANGE = (255, 165, 0)
NAVY = (0, 0, 128)
BUTTON_BG = (70, 70, 70)  # level buttons background
BUTTON_BG_HIGHLIGHT = (100, 100, 100)

COLOR_MAP = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: NAVY,
    5: MAROON,
    6: TURQUOISE,
    7: BLACK,
    8: GRAY,
}

FONT = pygame.font.SysFont('arial', 20, bold=True)
FONT_TIMER = pygame.font.SysFont('arial', 28, bold=True)

# Loading and scaling of emoticons (you need the files smile.png, dead.png, surprised.png next to the script)
SMILE_SIZE = 60
SMILEY_IMG = pygame.image.load("smile.png")
DEAD_IMG = pygame.image.load("dead.png")
SURPRISED_IMG = pygame.image.load("surprised.png")

SMILEY_IMG = pygame.transform.smoothscale(SMILEY_IMG, (SMILE_SIZE, SMILE_SIZE))
DEAD_IMG = pygame.transform.smoothscale(DEAD_IMG, (SMILE_SIZE, SMILE_SIZE))
SURPRISED_IMG = pygame.transform.smoothscale(SURPRISED_IMG, (SMILE_SIZE, SMILE_SIZE))

WIDTH, HEIGHT = 600, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper")

import winsound
def play_explosion():
    winsound.MessageBeep(winsound.MB_ICONHAND)

class Cell:
    def __init__(self):
        self.is_mine = False
        self.adjacent_mines = 0
        self.revealed = False
        self.flagged = False

class Game:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.first_click = True
        self.game_over = False
        self.win = False
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def reset(self, rows, cols, mines):
        self.__init__(rows, cols, mines)

    def place_mines(self, avoid_x, avoid_y):
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if not (abs(r - avoid_y) <= 1 and abs(c - avoid_x) <= 1)]
        for r, c in random.sample(spots, self.mines_count):
            self.board[r][c].is_mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.board[r][c].is_mine:
                    self.board[r][c].adjacent_mines = sum(
                        self.board[nr][nc].is_mine
                        for nr in range(max(0, r - 1), min(self.rows, r + 2))
                        for nc in range(max(0, c - 1), min(self.cols, c + 2))
                        if not (nr == r and nc == c))

    def reveal(self, x, y):
        if self.game_over or self.win:
            return
        cell = self.board[y][x]
        if cell.flagged or cell.revealed:
            return
        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False
        cell.revealed = True
        if cell.is_mine:
            self.game_over = True
            play_explosion()
            self.reveal_all_mines()
        elif cell.adjacent_mines == 0:
            self.reveal_neighbors(x, y)
        self.check_win()

    def reveal_neighbors(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    neighbor = self.board[ny][nx]
                    if not neighbor.revealed and not neighbor.flagged:
                        neighbor.revealed = True
                        if neighbor.adjacent_mines == 0 and not neighbor.is_mine:
                            self.reveal_neighbors(nx, ny)

    def toggle_flag(self, x, y):
        if self.game_over or self.win:
            return
        cell = self.board[y][x]
        if not cell.revealed:
            cell.flagged = not cell.flagged
        self.check_win()

    def reveal_all_mines(self):
        for row in self.board:
            for cell in row:
                if cell.is_mine:
                    cell.revealed = True

    def flagged_count(self):
        return sum(cell.flagged for row in self.board for cell in row)

    def check_win(self):
        # Checking that all mines are flagged and that there are no extra flags.
        if self.flagged_count() != self.mines_count:
            return
        for row in self.board:
            for cell in row:
                if cell.is_mine and not cell.flagged:
                    return
                if cell.flagged and not cell.is_mine:
                    return
        self.win = True
        self.game_over = False

    def draw(self, surface, offset_y):
        w, h = surface.get_size()
        cell_size = min((w - 40) // self.cols, (h - offset_y - 20) // self.rows)
        top_left_x = (w - (cell_size * self.cols)) // 2

        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(top_left_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size)
                cell = self.board[y][x]

                if cell.revealed:
                    pygame.draw.rect(surface, WHITE, rect)
                    pygame.draw.rect(surface, DARK_GRAY, rect, 1)
                    if cell.is_mine:
                        pygame.draw.circle(surface, BLACK, rect.center, cell_size // 4)
                    elif cell.adjacent_mines > 0:
                        color = COLOR_MAP.get(cell.adjacent_mines, BLACK)
                        text = FONT.render(str(cell.adjacent_mines), True, color)
                        surface.blit(text, text.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(surface, GRAY, rect)
                    pygame.draw.rect(surface, BLACK, rect, 1)
                    if cell.flagged:
                        # Drawing flag
                        pygame.draw.polygon(surface, RED, [
                            (rect.left + cell_size*0.3, rect.top + cell_size*0.7),
                            (rect.left + cell_size*0.7, rect.top + cell_size*0.5),
                            (rect.left + cell_size*0.3, rect.top + cell_size*0.3)
                        ])
                        pygame.draw.line(surface, BLACK,
                                         (rect.left + cell_size*0.3, rect.top + cell_size*0.3),
                                         (rect.left + cell_size*0.3, rect.top + cell_size*0.9), 2)
        return top_left_x, cell_size

def draw_ui(game, smile_state, elapsed_time):
    screen.fill(WHITE)

    # Difficulty level buttons
    levels = [("Easy", 9, 9, 10), ("Medium", 16, 16, 40), ("Hard", 16, 30, 99)]
    total_width = 3 * 110 + 2 * 10
    start_x = (screen.get_width() - total_width) // 2
    btn_rects = []
    for i, (name, r, c, m) in enumerate(levels):
        rect = pygame.Rect(start_x + i * (110 + 10), 10, 110, 45)
        pygame.draw.rect(screen, BUTTON_BG, rect, border_radius=6)
        text = FONT.render(name, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))
        btn_rects.append((rect, r, c, m))

    # Emoji with Bottom Margin (Space Between Emoji and Field)
    smile_x = screen.get_width() // 2 - SMILE_SIZE // 2
    smile_y = 70
    smile_rect = pygame.Rect(smile_x, smile_y, SMILE_SIZE, SMILE_SIZE)
    border_color = DARK_GRAY if not game.game_over and not game.win else RED if game.game_over else (0, 180, 0)
    pygame.draw.rect(screen, border_color, smile_rect.inflate(8,8), border_radius=8, width=3)

    img = SMILEY_IMG
    if game.game_over:
        img = DEAD_IMG
    elif smile_state == "surprised" and not game.game_over:
        img = SURPRISED_IMG
    elif game.win:
        img = SMILEY_IMG

    screen.blit(img, smile_rect)

    # Counters on the left and right of the emoji
    bomb_text = FONT_TIMER.render(f"Bombs: {game.mines_count}", True, BLACK)
    flags_text = FONT_TIMER.render(f"Flags: {game.flagged_count()}", True, BLACK)
    # Left
    screen.blit(bomb_text, bomb_text.get_rect(midright=(smile_rect.left - 20, smile_rect.centery)))
    # Right
    screen.blit(flags_text, flags_text.get_rect(midleft=(smile_rect.right + 20, smile_rect.centery)))

    # Timer under the emoji (centered)
    timer_text = FONT_TIMER.render(f"Time: {int(elapsed_time)}s", True, BLACK)
    screen.blit(timer_text, timer_text.get_rect(midtop=(screen.get_width() // 2, smile_rect.bottom + 10)))

    # If you win - display the message
    if game.win:
        win_text = FONT_TIMER.render("You Win!", True, (0, 150, 0))
        screen.blit(win_text, win_text.get_rect(center=(screen.get_width() // 2, smile_rect.top - 25)))

    return smile_rect, btn_rects

def main():
    global screen
    clock = pygame.time.Clock()
    game = Game(9, 9, 10)
    smile_state = "smile"
    top_offset = 180  # Spacing between an emoji and a field

    start_time = None

    while True:
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        screen.fill(WHITE)

        # # Calculating time since the start of the game
        if start_time and not (game.game_over or game.win):
            elapsed_time = time.time() - start_time
        else:
            elapsed_time = 0

        smile_rect, levels = draw_ui(game, smile_state, elapsed_time)
        top_left_x, cell_size = game.draw(screen, top_offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if event.button == 1:  # Левая кнопка
                    if smile_rect.collidepoint(event.pos):
                        game.reset(game.rows, game.cols, game.mines_count)
                        smile_state = "smile"
                        start_time = None
                    for btn_rect, r, c, m in levels:
                        if btn_rect.collidepoint(event.pos):
                            game.reset(r, c, m)
                            smile_state = "smile"
                            start_time = None
                    grid_x = (mx - top_left_x) // cell_size
                    grid_y = (my - top_offset) // cell_size
                    if 0 <= grid_x < game.cols and 0 <= grid_y < game.rows:
                        game.reveal(grid_x, grid_y)
                        if game.first_click == False and start_time is None:
                            start_time = time.time()
                        if game.game_over:
                            smile_state = "dead"
                        else:
                            smile_state = "surprised"
                elif event.button == 3:  # Right button
                    grid_x = (mx - top_left_x) // cell_size
                    grid_y = (my - top_offset) // cell_size
                    if 0 <= grid_x < game.cols and 0 <= grid_y < game.rows:
                        game.toggle_flag(grid_x, grid_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and smile_state == "surprised" and not (game.game_over or game.win):
                    smile_state = "smile"

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
