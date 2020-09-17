import dotenv
from gamecord import Game
import os


class MyGame(Game):
    def __init__(self):
        super().__init__('game', screen_size=(10, 10), controls=['⬅', '⬆', '⬇', '➡', '🇽'], title='Test Game 1',
                         tick=0.0)
        self.ball = [1, 1]

    async def update(self):
        if self.input:
            if self.input[0] == '⬅':
                self.ball[0] -= 1
            elif self.input[0] == '➡':
                self.ball[0] += 1
            elif self.input[0] == '⬆':
                self.ball[1] -= 1
            elif self.input[0] == '⬇':
                self.ball[1] += 1
            elif self.input[0] == '🇽':
                self.quit()

        self.ball[0] = min(max(self.ball[0], 0), self.screen_size[0] - 1)
        self.ball[1] = min(max(self.ball[1], 0), self.screen_size[1] - 1)

    async def draw(self, screen: list):
        self.fill_screen(screen)
        screen[self.ball[0]][self.ball[1]] = '😎'


dotenv.load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

game = MyGame()
if discord_token:
    game.run(discord_token)
else:
    raise ValueError
