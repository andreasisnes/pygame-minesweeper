from minesweeper import core
from minesweeper import sprites
from typing import Callable
from pygame.locals import BUTTON_LEFT
import pygame


class UserInterfaceFace:
    def __init__(
        self,
        board: core.Board,
        sprites: sprites.face.Face,
        offset: int,
        game_reset: Callable[[], None],
    ):
        self._core = board
        self._sprites = sprites
        self._offset = int(offset)
        self._img = self._sprites.smile
        self._update = True
        self._game_reset = game_reset
        self._click = None

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value: pygame.Surface):
        if self._img != value:
            self._img = value
            self._update = True
        else:
            self._update = False

    def game_reset(self):
        self.__init__(self._core, self._sprites, self._offset, self._game_reset)

    def draw(self, screen):
        if self._update:
            screen.blit(self.img, (self.x, self.y))
        return self._update

    def mouse_down(self, event):
        if event.button != BUTTON_LEFT:
            return
        self._click = event.pos
        if self.on_face(*self._click):
            self.img = self._sprites.smile_click
        elif self._core.is_game_over:
            self.img = self._sprites.dead
        elif self._core.is_game_finished:
            self.img = self._sprites.winner
        elif self.img == self._sprites.smile:
            self.img = self._sprites.excited

    def mouse_up(self, event):
        if event.button != BUTTON_LEFT:
            return
        if (
            self.on_face(*event.pos)
            and self._click != None
            and self.on_face(*self._click)
        ):
            self._game_reset()
        elif self._core.is_game_over:
            self.img = self._sprites.dead
        elif self._core.is_game_finished:
            self.img = self._sprites.winner
        else:
            self.img = self._sprites.smile

    @property
    def x(self) -> int:
        width, _ = pygame.display.get_surface().get_size()
        return width / 2 - (self._sprites.dead.get_width() / 2)

    @property
    def y(self) -> int:
        return self._offset * 2

    def on_face(self, x, y):
        return (
            True
            if (y >= self.y and y <= self.y + self.img.get_height())
            and (x >= self.x and x <= self.x + self.img.get_width())
            else False
        )
