import dotenv
from gamecord import Game
from piece import Piece, PIECE, BACK
import random
import os

TYPES = list(PIECE.keys())
INITIAL_DIFF = len(PIECE.keys()) - 5
GOOD_LIST = ['L', 'J', 'O', 'T', 'I', 'T', 'I', 'O', 'J', 'L']


class Tetris(Game):
    def __init__(self):
        super().__init__('tetris', title='⬛⬛⬛⬛Tetris!⬛⬛⬛⬛', screen_size=(10, 18), need_input=False, auto_clear=False,
                         controls=['⬅', '⬇', '➡', '🔃', '🇽'], cogs=('cog', ), back=BACK, tick=1.2)
        try:
            with open('tetris/leader.board', 'r', encoding='utf-8') as file:
                self.leaderboard = [line[:-1].split(',', maxsplit=1) for line in file]
        except FileNotFoundError:
            open('tetris/leader.board', 'x', encoding='utf-8')
            self.leaderboard = []

        self.difficulty = INITIAL_DIFF
        self.piece_count = 0
        self.active = []

        self.visual = 'square'
        self.grid = None
        self.piece = None
        self.score = 0

    async def pregame(self):
        self.grid = [[self.background] * self.height for _ in range(self.width)]
        self.footer = 'Total Score: 0'
        self.spawn_piece()
        self.score = 0

        self.difficulty = INITIAL_DIFF
        self.piece_count = 0
        self.active = []

    async def update(self):
        if '🔃' in self.input:
            while self.input.count('🔃'):
                self.piece.rotate(self.grid)
                self.input.remove('🔃')

        movement = [0, 1]
        if self.input:
            if self.input[0] == '⬅':
                movement[0] -= 1
            elif self.input[0] == '➡':
                movement[0] += 1
            elif self.input[0] == '⬇':
                movement[1] += self.height - self.piece.y - 1
                self.score += self.height - self.piece.y - 1

            if self.input[0] == '🇽':
                self.quit()

        try:
            if not self.piece.move(self.grid, *movement):
                self.spawn_piece()
                print(self.piece_count)
                self.score += 5
        except IndexError:
            self.footer = f'You LOST! Final Score: {self.score}'
            self.quit()
            return

        self.clear_rows()
        self.footer = f'Total Score: {self.score}'
        self.difficulty = INITIAL_DIFF - self.piece_count // 5

    async def draw(self, screen: list):
        for i in range(self.width):
            screen[i] = list(self.grid[i])
        self.piece.draw(screen)

    async def postgame(self):
        name = self.bot.context.author.name.replace(',', '')
        self.leaderboard.append([name, str(self.score)])
        print(f'{self.bot.context.author.name}: {self.score} points')

        self.leaderboard.sort(key=lambda x: int(x[1]), reverse=True)
        with open('tetris/leader.board', 'w', encoding='utf-8') as file:
            leaderboard = [f'{record[0].strip()}, {record[1].strip()}\n' for record in self.leaderboard][:10]
            file.writelines(leaderboard)

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

    def spawn_piece(self):
        if not self.active:
            choices = list(TYPES) * (3 if self.difficulty < 0 else 2)
            bad = list(GOOD_LIST)

            if self.difficulty <= 0:
                for i, piece in enumerate(bad):
                    if random.randint(min(i * 4, 99), 100) <= min(abs(self.difficulty) * 8, 90 + i):
                        choices.remove(piece)
                        print(piece)

            for _ in range(max(self.difficulty, 1)):
                if not choices:
                    break

                piece = random.choice(choices)
                self.active.append(piece)
                choices.remove(piece)
            self.piece = Piece(self.active[0], self.visual, 4, -1)
            self.active.pop(0)
        else:
            self.piece = Piece(self.active[0], self.visual, 4, -1)
            self.active.pop(0)
        self.piece_count += 1
        print(self.difficulty)
        print(self.active)


dotenv.load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

game = Tetris()
if discord_token:
    game.run(discord_token)
else:
    raise ValueError
