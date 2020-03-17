# -*- coding: utf-8 -*-

try:
    from .context import app
except ImportError:
    from context import app

import unittest
import random

class TestUnit(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.height = random.randint(10, 100)
        self.width  = random.randint(10, 100)
        self.mines  = random.randint(10, 90)
        self.iter   = 100
        self.api = app.API(self.width, self.height, self.mines)
        self.assertEqual(self.width, self.api.width)
        self.assertEqual(self.mines, self.api.mines)
        self.assertEqual(self.height, self.api.height)


    def test_game_reset(self):
        self.api.game_reset()
        self.assertEqual(self.width, self.api.width)
        self.assertEqual(self.mines, self.api.mines)
        self.assertEqual(self.height, self.api.height)

    def test_game_new(self):
        self.height = random.randint(10, 100)
        self.width  = random.randint(10, 100)
        self.mines  = random.randint(10, 90)
        self.api.game_new(self.width, self.height, self.mines)
        self.assertEqual(self.width, self.api.width)
        self.assertEqual(self.mines, self.api.mines)
        self.assertEqual(self.height, self.api.height)

    def test_board_dim(self):
        self.assertEqual(len(self.api.board), self.api.height)
        self.assertEqual(len(self.api.board[0]), self.api.width)

    def test_sheet_dim(self):
        self.assertEqual(len(self.api._sheet), self.api.height)
        self.assertEqual(len(self.api._sheet[0]), self.api.width)

    def test_tile_open(self):
        for _ in range(self.iter):
            self.height = random.randint(10, 100)
            self.width  = random.randint(10, 100)
            self.mines  = random.randint((self.width * self.height) // 2, (self.width * self.height) - 10)
            self.api.game_new(self.width, self.height, self.mines)
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            tiles = self.api.tile_open(y, x)
            surrounding = 9
            if x in [0, self.api.width - 1]:
                surrounding = -3
            if y in [0, self.api.height - 1]:
                surrounding = -3
            if x in [0, self.api.width - 1] and y in [0, self.api.height - 1]:
                surrounding += 1
            self.assertGreaterEqual(len(tiles), surrounding)
            for i in [y+1, y-1, y]:
                for j in [x+1, x-1]:
                    if self.api.tile_valid(i, j):
                        self.assertNotEqual(self.api.board[i][j], self.api.encoder.num_mine)

    def test_playing(self):
        for _ in range(self.iter):
            self.height = random.randint(10, 100)
            self.width  = random.randint(10, 100)
            self.mines  = random.randint((self.width * self.height) // 2, (self.width * self.height) - 10)
            self.api.game_new(self.width, self.height, self.mines)
            self.assertEqual(self.api.timer, 0.0)
            game_over = False
            for y in range(0, self.height):
                for x in range(0, self.width):
                    tiles = self.api.tile_open(x, y)
                    for tile in tiles:
                        if self.api.encoder.is_mine(tile['value']):
                            self.assertTrue(self.api.encoder.is_mine(self.api.sheet[tile['y']][tile['x']]))
                            self.assertTrue(self.api.is_game_over)
                    if game_over:
                        self.assertEqual(len(tiles), 0)
                    if game_over == False and self.api.is_game_over:
                        game_over = True
            self.assertGreater(self.api.timer, 0)

    def test_finish(self):
        for _ in range(self.iter):
            self.height = random.randint(10, 100)
            self.width  = random.randint(10, 100)
            self.mines  = random.randint((self.width * self.height) // 2, (self.width * self.height) - 10)
            self.api.game_new(self.width, self.height, self.mines)
            self.api.tile_open(0, 0)
            for y in range(0, self.height):
                for x in range(0, self.width):
                    if not self.api.encoder.is_mine(self.api.sheet[y][x]):
                        self.api.tile_open(y, x)
            self.assertTrue(self.api.is_game_done)


class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = app.minesweeper.Encoder()

    def test_ascii2num(self):
        for key, val in self.encoder._ascii2num.items():
            self.assertEqual(key, self.encoder._num2ascii[val])
            self.assertEqual(key, self.encoder.num2ascii(val))
            self.assertEqual(val, self.encoder.ascii2num(key))
            with self.assertRaises(KeyError):
                self.encoder.ascii2num(key + "test")

    def test_num2ascii(self):
        for key, val in self.encoder._num2ascii.items():
            self.assertEqual(key, self.encoder._ascii2num[val])
            self.assertEqual(key, self.encoder.ascii2num(val))
            self.assertEqual(val, self.encoder.num2ascii(key))
            with self.assertRaises(ValueError):
                self.encoder.num2ascii(str(key) + "test")
            with self.assertRaises(KeyError):
                self.encoder.num2ascii(key + random.randint(100, 10000))

    def test_getitem_ascii(self):
        for key, val in self.encoder._ascii2num.items():
            self.assertEqual(val, self.encoder[key])

    def test_getitem_num(self):
        for key, val in self.encoder._num2ascii.items():
            self.assertEqual(val, self.encoder[key])

    def test_is_tile_ascii(self):
        for key in self.encoder._ascii2num.keys():
            if key == self.encoder.ascii_tile:
                self.assertEqual(True, self.encoder.is_tile(key))
            else:
                self.assertEqual(False, self.encoder.is_tile(key))

    def test_is_tile_num(self):
        for key in self.encoder._num2ascii.keys():
            if key == self.encoder.num_tile:
                self.assertEqual(True, self.encoder.is_tile(key))
            else:
                self.assertEqual(False, self.encoder.is_tile(key))

    def test_is_mine_ascii(self):
        for key in self.encoder._ascii2num.keys():
            if key == self.encoder.ascii_mine:
                self.assertEqual(True, self.encoder.is_mine(key))
            else:
                self.assertEqual(False, self.encoder.is_mine(key))

    def test_is_min_num(self):
        for key in self.encoder._num2ascii.keys():
            if key == self.encoder.num_mine:
                self.assertEqual(True, self.encoder.is_mine(key))
            else:
                self.assertEqual(False, self.encoder.is_mine(key))

if __name__ == '__main__':
    unittest.main()
