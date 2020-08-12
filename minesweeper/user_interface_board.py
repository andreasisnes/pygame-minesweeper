from minesweeper import core
from minesweeper import sprites
from typing import Callable
from pygame.locals import BUTTON_LEFT, BUTTON_RIGHT
import pygame


class UserInterfaceBoard:
    def __init__(
        self, board: core.Board, sprites: sprites.tile.Tile, offset: int, callback
    ):
        self._core = board
        self._sprites = sprites
        self._offset = int(offset)
        self._flagged = 0
        self._click = None
        self._callback = callback
        self._mapper = UserInterfaceBoardMapper(self._sprites)
        self._tiles = [[self._mapper[j] for j in i] for i in self._core._tiles]

    def game_reset(self):
        self.__init__(self._core, self._sprites, self._offset, self._callback)

    def game_over(self):
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                if self._core._board[i][j].type == core.BoardTile.mine:
                    if tile == self._sprites.unopened:
                        self._tiles[i][j] = self._sprites.mine
                else:
                    if tile == self._sprites.flag:
                        self._tiles[i][j] = self._sprites.mine_red_cross

    def game_finished(self):
        self._callback(self._core.timer)

    def draw(self, screen):
        _, height = pygame.display.get_surface().get_size()
        for i_idx, row in enumerate(self._tiles):
            for j_idx, tile in enumerate(row):
                x = self._offset + (j_idx * tile.get_width())
                y = (
                    height
                    - ((len(self._tiles) - i_idx) * tile.get_height())
                    - self._offset
                )
                screen.blit(tile, (x, y))

    def mouse_down(self, event):
        y, x = self.mouse_tile(*event.pos)
        if self._core.tile_valid(y, x) and not (
            self._core.is_game_over or self._core.is_game_finished
        ):
            if event.button == BUTTON_LEFT:
                self.mouse_down_left(y, x)
            if event.button == BUTTON_RIGHT:
                self.mouse_down_right(y, x)

    def mouse_down_left(self, y, x):
        tile = self._tiles[y][x]
        self._click = (y, x)
        if tile == self._sprites.unopened:
            self._tiles[y][x] = self._sprites.empty
        if tile == self._sprites.question_mark:
            self._tiles[y][x] = self._sprites.question_mark_click

    def mouse_down_right(self, y, x):
        if self._tiles[y][x] == self._sprites.unopened:
            self._tiles[y][x] = self._sprites.flag
            self._flagged += 1
        elif self._tiles[y][x] == self._sprites.flag:
            self._flagged -= 1
            self._tiles[y][x] = self._sprites.question_mark
        elif self._tiles[y][x] == self._sprites.question_mark:
            self._tiles[y][x] = self._sprites.unopened

    def mouse_up_left(self, y, x):
        if self._click[0] != y or self._click[1] != x:
            y, x = self._click
            if self._core._tiles[y][x] == core.BoardTile.unopened:
                if self._tiles[y][x] == self._sprites.question_mark_click:
                    self._tiles[y][x] = self._sprites.question_mark
                elif self._tiles[y][x] == self._sprites.empty:
                    self._tiles[y][x] = self._sprites.unopened
        else:
            if (
                self._core._tiles[y][x] == core.BoardTile.unopened
                and self._tiles[y][x] == self._sprites.empty
            ):
                f = self._core.tile_open(y, x)
                for tile in f:
                    self._tiles[tile.i][tile.j] = self._mapper[tile]
                    if tile == core.BoardTile.mine:
                        self._tiles[y][x] = self._sprites.mine_red
                        self.game_over()
            elif self._tiles[y][x] == self._sprites.question_mark_click:
                self._tiles[y][x] = self._sprites.unopened
        if self._core.is_game_finished:
            self.game_finished()
        self._click = None

    def mouse_up_right(self, y, x):
        if self._core.is_game_finished:
            self.game_finished()

    def mouse_up(self, event):
        y, x = self.mouse_tile(*event.pos)
        if self._click is not None and not self._core.is_game_over:
            if event.button == BUTTON_LEFT:
                self.mouse_up_left(y, x)
            if event.button == BUTTON_RIGHT:
                self.mouse_up_right(y, x)

    def mouse_tile(self, x, y):
        _, height = pygame.display.get_surface().get_size()
        x = (x - self._offset) // self._sprites.eight.get_width()
        y = (
            y
            - (
                height
                - (len(self._tiles) * self._sprites.eight.get_width())
                - self._offset
            )
        ) // self._sprites.eight.get_width()
        return y, x

    def flagged(self):
        return self._flagged

    def reset(self):
        self._core.game_reset()


class UserInterfaceBoardMapper:
    def __init__(self, sprites: sprites.tile.Tile):
        self._sprites = sprites
        self._tile2sprites = {
            core.BoardTile.mine: lambda: self._sprites.mine,
            core.BoardTile.unopened: lambda: self._sprites.unopened,
            core.BoardTile.zero: lambda: self._sprites.empty,
            core.BoardTile.one: lambda: self._sprites.one,
            core.BoardTile.two: lambda: self._sprites.two,
            core.BoardTile.three: lambda: self._sprites.three,
            core.BoardTile.four: lambda: self._sprites.four,
            core.BoardTile.five: lambda: self._sprites.five,
            core.BoardTile.six: lambda: self._sprites.six,
            core.BoardTile.seven: lambda: self._sprites.seven,
            core.BoardTile.eight: lambda: self._sprites.eight,
        }

    def __getitem__(self, tile: core.BoardTile):
        return self._tile2sprites[str(tile)]()
