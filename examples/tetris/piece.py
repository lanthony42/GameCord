PIECE = {
    'I': {'orientations': [[(0, 0), (-1, 0), (1, 0), (2, 0)],
                           [(1, 0), (1, -1), (1, 1), (1, 2)],
                           [(0, 1), (-1, 1), (1, 1), (2, 1)],
                           [(0, 0), (0, -1), (0, 1), (0, 2)],
                           ], 'emoji': '☄', 'block': '🆗', 'square': '⬜'},
    'J': {'orientations': [[(0, 0), (1, 0), (-1, 0), (-1, -1)],
                           [(0, 0), (0, 1), (0, -1), (1, -1)],
                           [(0, 0), (1, 0), (-1, 0), (1, 1)],
                           [(0, 0), (0, 1), (0, -1), (-1, 1)],
                           ], 'emoji': '🖌️', 'block': '🛂', 'square': '🟦'},
    'L': {'orientations': [[(0, 0), (1, 0), (-1, 0), (1, -1)],
                           [(0, 0), (0, 1), (0, -1), (1, 1)],
                           [(0, 0), (1, 0), (-1, 0), (-1, 1)],
                           [(0, 0), (0, 1), (0, -1), (-1, -1)],
                           ], 'emoji': '🥕', 'block': '🚼', 'square': '🟧'},
    'O': {'orientations': [[(0, 0), (0, -1), (-1, 0), (-1, -1)],
                           ], 'emoji': '🍌', 'block': '📳', 'square': '🟨'},
    'S': {'orientations': [[(0, 0), (0, -1), (-1, 0), (1, -1)],
                           [(0, 0), (0, -1), (1, 0), (1, 1)],
                           [(0, 0), (0, 1), (1, 0), (-1, 1)],
                           [(0, 0), (0, 1), (-1, 0), (-1, -1)],
                           ], 'emoji': '🥒', 'block': '✅', 'square': '🟩'},
    'T': {'orientations': [[(0, 0), (1, 0), (-1, 0), (0, -1)],
                           [(0, 0), (1, 0), (0, 1), (0, -1)],
                           [(0, 0), (1, 0), (0, 1), (-1, 0)],
                           [(0, 0), (0, -1), (0, 1), (-1, 0)],
                           ], 'emoji': '🍆', 'block': '☮', 'square': '🟪'},
    'Z': {'orientations': [[(0, 0), (0, -1), (1, 0), (-1, -1)],
                           [(0, 0), (0, 1), (1, 0), (1, -1)],
                           [(0, 0), (0, 1), (-1, 0), (1, 1)],
                           [(0, 0), (0, -1), (-1, 0), (-1, 1)],
                           ], 'emoji': '🌶️', 'block': '💟', 'square': '🟥'},
}
WALL_KICK = [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
             [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
             [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
             [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
             ]
WALL_KICK_I = [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
               [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
               [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
               [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
               ]
BACK = '◼'


class Piece:
    def __init__(self, shape: str, visual: str, x: int, y: int):
        self.shape = shape
        self.visual = visual
        self.rotation = 0
        self.x = x
        self.y = y

    @property
    def blocks(self):
        return [(self.x + block[0], self.y + block[1]) for block in PIECE[self.shape]['orientations'][self.rotation]]

    @property
    def emoji(self):
        return PIECE[self.shape][self.visual]

    def draw(self, screen: list):
        for x, y in self.blocks:
            if 0 <= x < len(screen) and 0 <= y < len(screen[0]):
                screen[x][y] = self.emoji

    def check_collisions(self, grid: list, pos_x: int = None, pos_y: int = None, rotation: int = None):
        if pos_x is None:
            pos_x = self.x
        if pos_y is None:
            pos_y = self.y
        if rotation is None:
            rotation = self.rotation
        output = False

        for x, y in PIECE[self.shape]['orientations'][rotation]:
            if 0 <= pos_x + x < len(grid) and pos_y + y < len(grid[0]):
                if pos_y + y >= 0:
                    output = output or grid[pos_x + x][pos_y + y] != BACK
            else:
                output = True
        return output

    def move(self, grid: list, vel_x: int = 0, vel_y: int = 0):
        if not self.check_collisions(grid, self.x + vel_x, self.y):
            self.x += vel_x

        for i in range(vel_y):
            if not self.check_collisions(grid, self.x, self.y + 1):
                self.y += 1
            elif i == 0:
                for x, y in self.blocks:
                    if x < 0 or y < 0:
                        raise IndexError
                    grid[x][y] = self.emoji
                return False
        return True

    def rotate(self, grid: list):
        for x, y in (WALL_KICK_I[self.rotation] if self.shape == 'I' else WALL_KICK[self.rotation]):
            rotate = self.rotation + 1 if self.rotation + 1 < len(PIECE[self.shape]['orientations']) else 0
            if not self.check_collisions(grid, self.x + x, self.y + y, rotate):
                self.rotation += 1
                if self.rotation >= len(PIECE[self.shape]['orientations']):
                    self.rotation = 0

                self.x += x
                self.y += y
                break

    def __str__(self):
        return f'{self.shape}({self.x}, {self.y})'
