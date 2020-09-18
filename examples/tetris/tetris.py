import dotenv
from gamecord import Game
from piece import Piece, PIECE, BACK
import random
import os


class Tetris(Game):
    def __init__(self):
        super().__init__('tetris', title='⬛⬛⬛⬛Tetris!⬛⬛⬛⬛', screen_size=(10, 18), need_input=False, auto_clear=True,
                         controls=['⬅', '⬇', '➡', '🔃', '🇽'], back=BACK, tick=1.2)
        self.visual = 'square'
        self.grid = None
        self.piece = None
        self.score = 0

    async def pregame(self):
        self.grid = [[self.background] * self.height for _ in range(self.width)]
        self.piece = Piece(random.choice(list(PIECE.keys())), self.visual, 4, -1)
        self.footer = 'Total Score: 0'
        self.score = 0

    async def update(self):
        movement = [0, 1]
        if self.input:
            if self.input[0] == '🔃':
                self.piece.rotate(self.grid)
            elif self.input[0] == '⬅':
                movement[0] -= 1
            elif self.input[0] == '➡':
                movement[0] += 1
            elif self.input[0] == '⬇':
                movement[1] += 1
                self.score += 1
            elif self.input[0] == '🇽':
                self.quit()

        try:
            if not self.piece.move(self.grid, *movement):
                self.piece = Piece(random.choice(list(PIECE.keys())), self.visual, 4, -1)
                self.score += 5
        except IndexError:
            self.footer = f'You LOST! Final Score: {self.score}'
            self.quit()
            return

        self.clear_rows()
        self.footer = f'Total Score: {self.score}'

    async def draw(self, screen: list):
        for i in range(self.width):
            screen[i] = list(self.grid[i])
        self.piece.draw(screen)

    def clear_rows(self):
        cleared = 0
        j = self.height - 1
        while j > 0:
            skip = False
            for i in range(self.width):
                skip = skip or self.grid[i][j] == BACK

            if not skip:
                cleared += 1
                for i in range(self.width):
                    for k in range(j, 1, -1):
                        self.grid[i][k] = self.grid[i][k - 1]
                    self.grid[i][0] = BACK
            else:
                j -= 1

        self.score += (cleared % 4) ** 2 * 100
        self.score += (cleared // 4) * 2000



dotenv.load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

game = Tetris()
if discord_token:
    game.run(discord_token)
else:
    raise ValueError
