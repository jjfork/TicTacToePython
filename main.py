import pygame
import sys
from random import randint

WINDOW_SIZE = 1000
BOARD_SIZE = 10
WIN_CONDITION = 5
vec2 = pygame.math.Vector2
CELL_SIZE = WINDOW_SIZE / BOARD_SIZE
CELL_CENTER = vec2(CELL_SIZE / 2)
INF = float('inf')


class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.board_image = self.get_scaled_image(path='resources/board.jpg', res=[WINDOW_SIZE] * 2)
        self.O_image = self.get_scaled_image(path='resources/o_placeholder.jpg', res=[CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image(path='resources/x_placeholder.jpg', res=[CELL_SIZE] * 2)
        self.winner = None

        self.board = [[INF] * BOARD_SIZE for i in range(BOARD_SIZE)]
        self.player = randint(0, 1)

        self.line_indices_array = []
        self.generate_possible_wins()

        self.game_steps = 0
        self.font = pygame.font.SysFont('arial', int(CELL_SIZE / 4), True)

    def generate_possible_wins(self):
        # horizontal
        for i in range(BOARD_SIZE):
            for j in range(WIN_CONDITION + 1):
                self.line_indices_array.append([(i, j + k) for k in range(WIN_CONDITION)])
        # vertical
        for i in range(WIN_CONDITION + 1):
            for j in range(BOARD_SIZE):
                self.line_indices_array.append([(i + k, j) for k in range(WIN_CONDITION)])
        # left to right
        for i in range(WIN_CONDITION + 1):
            for j in range(WIN_CONDITION + 1):
                self.line_indices_array.append([(i + k, j + k) for k in range(WIN_CONDITION)])
        # right to left
        for i in range(WIN_CONDITION + 1):
            for j in range(BOARD_SIZE - 1, BOARD_SIZE - WIN_CONDITION, -1):  # reverse order
                self.line_indices_array.append([(i + k, j - k) for k in range(WIN_CONDITION)])

    def check_winner(self):
        for line_indicates in self.line_indices_array:
            sum_line = sum([self.board[i][j] for i, j in line_indicates])
            if sum_line in {0, WIN_CONDITION}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [vec2(line_indicates[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    vec2(line_indicates[4][::-1]) * CELL_SIZE + CELL_CENTER]

    def run_game_process(self):
        current_cell = vec2(pygame.mouse.get_pos()) / CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.board[row][col] == INF and not self.winner:
            self.board[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        for y, row in enumerate(self.board):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(x, y) * CELL_SIZE)

    def draw_winner(self):
        if self.winner:
            pygame.draw.line(self.game.screen,
                             'red',
                             *self.winner_line,
                             int(CELL_SIZE // 8))

    def draw(self):
        self.game.screen.blit(self.board_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img, res)

    def print_caption(self):
        pygame.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pygame.display.set_caption(f'Player "{self.winner}" wins! Press SPACE to restart')
        elif self.game_steps == BOARD_SIZE * BOARD_SIZE:
            pygame.display.set_caption(f'TIE! Press SPACE to restart')

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pygame.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pygame.display.update()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.new_game()

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)


if __name__ == '__main__':
    game = Game()
    game.run()
