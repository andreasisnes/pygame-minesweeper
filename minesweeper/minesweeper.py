# -*- coding: utf-8 -*-
""" Minesweeper """
import random
import time

def valid_arguments(fn):
    def init(self, width, height, mines):
        try:
            w, h, m = int(width), int(height), int(mines)
            if not ((w >= 10 and h >= 10) and (w <= 100 and h <= 100)):
                raise ValueError('Arguments "width" and "height" must range [10, 100].')
            if m < 0 and m > ((h * w) - 9):
                raise ValueError('Arguments "mines" must range (0, (h * w) - 9]')
        except TypeError:
            raise TypeError("Arguments must be a number")
        return fn(self, w, h, m)
    return init

def valid_attempt(fn):
    def is_valid_attempt(self, y, x):
        if self._is_game_over:
            return []
        if not self.tile_valid(y, x):
            return []
        if not self.encoder.is_tile(self._board[y][x]):
            return []
        if self._is_game_done:
            return []
        if self._opened == 0:
            self._sheet_init(y, x)
        return fn(self, y, x)
    return is_valid_attempt


class API:
    """ API """

    @valid_arguments
    def __init__(self, width, height, mines):
        """ Generates a minesweeper game.

        Parameters
        ----------
        width : int
            width of player's board
        height : int
            height of player's board
        mines : int
            number of mines placed randomly on the player's board

        Raises
        ------
        ValueError
            If arguments exceeds fixed thresholds.
        TypeError
            If arguments are not numbers
        """
        self.encoder = Encoder()

        self._width = width
        self._height = height
        self._mines = mines

        self._board = self._generate_board()
        self._sheet = self._generate_sheet()

        self._is_game_over = False
        self._is_game_done = False
        self._opened = 0
        self._timer = time.time()
        self._timer1= time.time()

    def game_new(self, width, height, mines):
        """ Generates a new game with different settings.

        Parameters
        ----------
        width : int
            width of player's board
        height : int
            height of player's board
        mines : int
            number of mines placed randomly on the player's board

        Raises
        ------
        ValueError
            If arguments exceeds fixed thresholds.
        TypeError
            If arguments are not numbers
        """
        self.__init__(width, height, mines)

    def game_reset(self):
        """ Resets game with the same settings except bomb locations. """
        self.__init__(self.width, self.height, self.mines)

    def _generate_board(self):
        """ Generate board matrix. """
        return [[Encoder.num_tile for _ in range(self.width)] for _ in range(self.height)]

    def _generate_sheet(self):
        """ Generates the bomb locations randomly. """
        mines = [0 for _ in range(self.width * self.height)]
        while mines.count(Encoder.num_mine) != self.mines:
            tile = random.randint(0, len(mines) - 1)
            while mines[tile] == Encoder.num_mine:
                tile = random.randint(0, len(mines) - 1)
            mines[tile] = Encoder.num_mine
        return [[mines[(y * self.width) + x] for x in range(self.width)] for y in range(self.height)]

    def _sheet_init(self, pos_y, pos_x):
        # Make sure the user never hits a mine on the first opened tile
        for y in [pos_y + 1, pos_y - 1, pos_y]:
            for x in [pos_x + 1, pos_x - 1, pos_x]:
                if self.tile_valid(y, x) and self.encoder.is_mine(self._sheet[y][x]):
                    i = random.randint(0, self.height - 1)
                    j = random.randint(0, self.width - 1)
                    while self.encoder.is_mine(self._sheet[i][j]) or (abs(pos_y - i) <= 1 and abs(pos_x - j) <= 1):
                        i = random.randint(0, self.height - 1)
                        j = random.randint(0, self.width - 1)
                    self._sheet[i][j] = Encoder.num_mine
                    self._sheet[y][x] = 0

        # make sure to reset sheet except newly created mines
        for y in range(0, self.height):
            for x in range(0, self.width):
                if not self.encoder.is_mine(self._sheet[y][x]):
                    self._sheet[y][x] = 0

        # calculate the numeric score of each tile
        for y in range(0, self.height):
            for x in range(0, self.width):
                if not self.encoder.is_mine(self._sheet[y][x]):
                    for i in [y, y+1, y-1]:
                        for j in [x, x+1, x-1]:
                            if self.tile_valid(i, j) and self.encoder.is_mine(self._sheet[i][j]):
                                self._sheet[y][x] += 1
        self._timer = time.time()

    @valid_attempt
    def tile_open(self, y, x):
        """ Opens a tile based on given coordinate. """
        # Checks if game is not over and given tile is valid
        tile = {'value': self._sheet[y][x], 'x': x, 'y': y}
        self._board[y][x] = tile['value']
        self._opened += 1
        if (self._opened + self.mines) == (self.width * self.height):
            self._is_game_done = True
            self._timer1 = time.time()
        if self.encoder.is_mine(tile['value']):
            self._is_game_over = True
            self._timer1 = time.time()
        elif tile['value'] >= 0:
            if tile['value'] == 0:
                return self._tile_open_adjacent(y, x, [tile])
        return [tile]

    def _tile_open_adjacent(self, y, x, opened):
        if self.tile_valid(y, x):
            if self.encoder.is_mine(self._sheet[y][x]):
                return [{'value': Encoder.num_mine, 'x': x, 'y': y}]
            for i in [y, y+1, y-1]:
                for j in [x, x+1, x-1]:
                    if self.tile_valid(i, j) and self.encoder.is_tile(self._board[i][j]):
                        self._opened += 1
                        if (self._opened + self.mines) == (self.width * self.height):
                            self._is_game_done = True
                            self._timer1 = time.time()
                        self._board[i][j] = self._sheet[i][j]
                        opened.append({'value': self._sheet[i][j], 'x': j, 'y': i})
                        if self._sheet[i][j] == 0:
                            self._tile_open_adjacent(i, j, opened)
        return opened

    @property
    def timer(self):
        if self.is_game_over or self.is_game_done:
            return self._timer1 - self._timer if self._opened > 0 else 0.0
        return time.time() - self._timer if self._opened > 0 else 0.0

    def tile_valid(self, y, x):
        """ Check if given coordinate is within bound. """
        return True if (x >= 0 and x < self.width) and (y >= 0 and y < self.height) else False

    @property
    def is_game_over(self):
        """ Returns True if game is over False otherwise. """
        return self._is_game_over

    @property
    def is_game_done(self):
        """ Returns True if game is over False otherwise. """
        return self._is_game_done

    @property
    def board(self):
        return self._board

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def mines(self):
        return self._mines

    @property
    def sheet(self):
        return self._sheet

    @property
    def solution(self):
        return "\n".join(["".join([f"{(self.encoder[tile]):2}" for tile in row]).rstrip() for row in self._sheet])

    def __str__(self):
        return "\n".join(["".join([f"{(self.encoder[tile]):2}" for tile in row]).rstrip() for row in self._board])

class Encoder:
    ascii_tile = 't'
    ascii_mine = 'x'
    num_tile = -1
    num_mine = -2
    def __init__(self):
        self._num2ascii = {
            self.num_tile : self.ascii_tile,
            self.num_mine : self.ascii_mine,
            0 : '0',
            1 : '1',
            2 : '2',
            3 : '3',
            4 : '4',
            5 : '5',
            6 : '6',
            7 : '7',
            8 : '8',
        }
        self._ascii2num = {
            self.ascii_tile : self.num_tile,
            self.ascii_mine : self.num_mine,
            '0' : 0,
            '1' : 1,
            '2' : 2,
            '3' : 3,
            '4' : 4,
            '5' : 5,
            '6' : 6,
            '7' : 7,
            '8' : 8,
        }

    def ascii2num(self, string):
        try:
            return self._ascii2num[str(string)]
        except KeyError:
            raise KeyError('Argument "string" can not be encoded {}'.format(string))

    def num2ascii(self, integer):
        try:
            return self._num2ascii[int(integer)]
        except ValueError:
            raise ValueError('Argument "integer" must be a string')
        except KeyError:
            raise KeyError('Argument "integer" can not be encoded {}'.format(integer))

    def __getitem__(self, arg):
        if type(arg) == str:
            return self.ascii2num(arg)
        return self.num2ascii(arg)

    def is_tile(self, arg):
        if type(arg) == str:
            return True if arg == self.ascii_tile else False
        return True if arg == self.num_tile else False

    def is_mine(self, arg):
        if type(arg) == str:
            return True if arg == self.ascii_mine else False
        return True if arg == self.num_mine else False
