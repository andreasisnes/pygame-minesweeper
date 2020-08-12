import pygame
from functools import reduce

try:
    import sprites
    import minesweeper
except ImportError:
    from . import sprites
    from . import minesweeper


class Board:
    def __init__(self, api, screen, color=True):
        self.board_game = BoardGame(api, y_offset=40)
        self.board_score = BoardScore(api, self.board_game.marked, 8, 8)
        self.board_face = BoardFace(api, self.game_reset)
        self.modules = [self.board_game, self.board_face, self.board_score]
        screen.fill((192, 192, 192))
        self.draw(screen)

    def create_frame(self, screen):
        pass

    def draw(self, screen):
        for m in self.modules:
            m.draw(screen)

    def mouse_down(self, event):
        for m in self.modules:
            m.mouse_down(event)

    def mouse_up(self, event):
        for m in self.modules:
            m.mouse_up(event)

    def game_reset(self):
        for m in self.modules:
            m.game_reset()


class BoardScore:
    def __init__(self, api, marked, x_offset=8, y_offset=8):
        self.api = api
        self.scores = sprites.Score()
        self.x_score = x_offset
        self.y_score = y_offset
        self.x_timer = ((self.api.width * 16) - x_offset) - self.scores.width * 3
        self.y_timer = y_offset
        self.marked = marked

    def game_reset(self):
        self.__init__(self.api, self.marked, self.x_score, self.y_score)

    def draw(self, screen):
        self.draw_score(screen)
        self.draw_timer(screen)

    def draw_timer(self, screen):
        tiles = str(int(self.api.timer)).zfill(3)
        if len(tiles) > 3:
            tiles = "999"
        for x in range(0, 3):
            screen.blit(
                self.scores[tiles[x]],
                (self.x_timer + x * self.scores.width, self.y_timer),
            )

    def draw_score(self, screen):
        marked = self.marked()
        if marked < 0:
            marked = 0
        tiles = str(int(marked)).zfill(3)
        if len(tiles) > 3:
            tiles = "999"
        for x in range(0, 3):
            screen.blit(
                self.scores[tiles[x]],
                (self.x_score + x * self.scores.width, self.y_score),
            )

    def mouse_up(self, event):
        pass

    def mouse_down(self, event):
        pass


class BoardFace:
    def __init__(self, api, game_reset, x_offset=0, y_offset=8):
        self.api = api
        self.faces = sprites.Face()
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x = ((api.width * 16) / 2) - self.faces.width / 2 + x_offset
        self.y = y_offset
        self.img = self.faces[":)"]
        self.click = None
        self._game_reset = game_reset

    def game_reset(self):
        self.__init__(self.api, self._game_reset, self.x_offset, self.y_offset)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def mouse_up(self, event):
        x, y = event.pos
        if self.mouse_on_face(x, y) and self.mouse_on_face(*self.click):
            self._game_reset()
        elif self.api.is_game_over:
            self.img = self.faces["x("]
        elif self.api.is_game_done:
            self.img = self.faces["B)"]
        else:
            self.img = self.faces[":)"]
        self.click = None

    def mouse_down_left(self, event):
        x, y = event.pos
        self.click = event.pos
        if self.mouse_on_face(x, y):
            self.click = event.pos
            self.img = self.faces["*:)"]
        elif self.api.is_game_over:
            self.img = self.faces["x("]
        elif self.api.is_game_done:
            self.img = self.faces["B)"]
        elif self.img == self.faces[":)"]:
            self.img = self.faces[":o"]

    def mouse_on_face(self, x, y):
        return (
            True
            if (y >= self.y and y <= self.y + self.faces.height)
            and (x >= self.x and x <= self.x + self.faces.width)
            else False
        )

    def mouse_down(self, event):
        if event.button == 1:
            self.mouse_down_left(event)


class BoardGame:
    def __init__(self, api, x_offset=0, y_offset=0):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.api = api
        self.tiles = sprites.Tile(api)
        self.click = None
        self.board = [
            [self.tiles[self.api.encoder[x]] for x in y] for y in self.api.board
        ]

    def game_reset(self):
        self.api.game_reset()
        self.__init__(self.api, self.x_offset, self.y_offset)

    def game_new(self, width, height, mines):
        self.api.game_new(width, height, mines)
        self.__init__(self.api)

    def game_over(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if self.api.encoder.is_mine(self.api.sheet[y][x]):
                    if tile == self.tiles[self.api.encoder.ascii_tile]:
                        self.board[y][x] = self.tiles[self.api.encoder.ascii_mine]
                else:
                    if tile == self.tiles["f"]:
                        self.board[y][x] = self.tiles["fx"]

    def game_done(self):
        for y in range(self.api.height):
            for x in range(self.api.width):
                if self.api.encoder.is_tile(self.api.sheet[y][x]):
                    self.board[y][x] = self.tiles["*?"]
                else:
                    self.board[y][x] = self.tiles[
                        self.api.encoder.num2ascii(self.api.sheet[y][x])
                    ]

    def draw(self, screen):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                screen.blit(
                    tile,
                    (
                        tile.get_width() * x + self.x_offset,
                        tile.get_height() * y + self.y_offset,
                    ),
                )

    def mouse_down_left(self, y, x):
        if self.api.is_game_over or not self.api.tile_valid(y, x):
            return

        self.click = (y, x)
        if self.board[y][x] == self.tiles[self.api.encoder.ascii_tile]:
            self.board[y][x] = self.tiles["0"]
        if self.board[y][x] == self.tiles["?"]:
            self.board[y][x] = self.tiles["*?"]

    def mouse_down_right(self, y, x):
        if self.api.is_game_over or not self.api.tile_valid(y, x):
            return

        if self.board[y][x] == self.tiles[self.api.encoder.ascii_tile]:
            self.board[y][x] = self.tiles["f"]
        elif self.board[y][x] == self.tiles["f"]:
            self.board[y][x] = self.tiles["?"]
        elif self.board[y][x] == self.tiles["?"]:
            self.board[y][x] = self.tiles[self.api.encoder.ascii_tile]

    def mouse_up_left(self, y, x):
        if self.api.is_game_over or self.click is None:
            pass

        elif self.click[0] != y or self.click[1] != x:
            if self.api.encoder.is_tile(self.api.board[self.click[0]][self.click[1]]):
                if self.board[self.click[0]][self.click[1]] == self.tiles["0"]:
                    self.board[self.click[0]][self.click[1]] = self.tiles[
                        self.api.encoder.ascii_tile
                    ]
                elif self.board[self.click[0]][self.click[1]] == self.tiles["*?"]:
                    self.board[self.click[0]][self.click[1]] = self.tiles["?"]
        else:
            if (
                self.api.encoder.is_tile(self.api.board[y][x])
                and self.board[y][x] == self.tiles["0"]
            ):
                for tile in self.api.tile_open(y, x):
                    v = self.api.encoder.num2ascii(tile["value"])
                    self.board[tile["y"]][tile["x"]] = self.tiles[v]
                    if self.api.encoder.is_mine(v) and self.api.is_game_over:
                        self.board[y][x] = self.tiles["*x"]
                        self.game_over()
            elif self.board[y][x] == self.tiles["*?"]:
                self.board[y][x] = self.tiles[self.api.encoder.ascii_tile]
        if self.api.is_game_done:
            self.game_done()

        self.click = None

    def marked(self):
        c = 0
        for row in self.board:
            c += row.count(self.tiles["f"])
        return self.api.mines - c

    def mouse_up_right(self, y, x):
        if self.api.is_game_done:
            self.game_done()

    def mouse_down(self, event):
        y, x = self.mouse_tile(event.pos)
        if event.button == 1:
            self.mouse_down_left(y, x)
        elif event.button == 3:
            self.mouse_down_right(y, x)

    def mouse_up(self, event):
        y, x = self.mouse_tile(event.pos)
        if event.button == 1:
            self.mouse_up_left(y, x)
        elif event.button == 3:
            self.mouse_up_right(y, x)

    def mouse_tile(self, pos):
        return ((pos[1] - self.y_offset) // 16, (pos[0] - self.x_offset) // 16)
