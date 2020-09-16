import dotenv
from gamecord import Game
import os

game = Game('game', screen_size=(10, 10), controls=['⬅', '⬆', '⬇', '➡', '🇽'], title='Test Game 1', tick=0.0)
ball = [1, 1]


@game.set_update()
def update():
    global ball

    if game.input:
        if game.input[0] == '⬅':
            ball[0] -= 1
        elif game.input[0] == '➡':
            ball[0] += 1
        elif game.input[0] == '⬆':
            ball[1] -= 1
        elif game.input[0] == '⬇':
            ball[1] += 1
        elif game.input[0] == '🇽':
            game.quit()

    ball[0] = min(max(ball[0], 0), game.screen_size[0] - 1)
    ball[1] = min(max(ball[1], 0), game.screen_size[1] - 1)


@game.set_draw()
def draw(screen: list):
    game.fill_screen(screen)
    screen[ball[0]][ball[1]] = '<:dwastarnew:751892195501539399>'


dotenv.load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
game.run(discord_token)
