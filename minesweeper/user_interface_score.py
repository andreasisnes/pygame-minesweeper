from minesweeper import core
from minesweeper import sprites
from typing import Callable
import pygame


class UserInterfaceScore:
    max_score = "999"

    def __init__(
        self,
        board: core.Board,
        sprites: sprites.score.Score,
        offset: int,
        flagged: Callable[[], int],
        white_color=(255, 255, 255),
        dark_grey_color=(128, 128, 128),
    ):
        self._board = board
        self._sprites = sprites
        self._flagged = flagged
        self._offset = int(offset) * 2
        self._white_color = white_color
        self._dark_grey_color = dark_grey_color

    def game_reset(self):
        pass

    def draw(self, screen):
        self.draw_timer(screen)
        self.draw_mines(screen)

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def draw_shadow(self, screen, offset_x, offset_y):
        w, h = self._sprites.one.get_width(), self._sprites.one.get_height()
        screen.fill(
            self._dark_grey_color, rect=(offset_x - 1, offset_y - 1, w * 3 + 2, 1)
        )
        screen.fill(self._dark_grey_color, rect=(offset_x - 1, offset_y - 1, 1, h + 2))
        screen.fill(self._white_color, rect=(offset_x, offset_y + h, w * 3 + 1, 1))
        screen.fill(self._white_color, rect=(offset_x + w * 3, offset_y, 1, h + 1))

    def draw_timer(self, screen):
        elapsed = str(int(self._board.timer)).zfill(3)
        if len(elapsed) > 3:
            elapsed = UserInterfaceScore.max_score
        width, _ = pygame.display.get_surface().get_size()
        self.draw_shadow(screen, self._offset, self._offset)
        [
            screen.blit(
                tile,
                (width - self._offset - ((idx + 1) * tile.get_width()), self._offset),
            )
            for idx, tile in enumerate(reversed(self._sprites[elapsed]))
        ]

    def draw_mines(self, screen):
        flagged = self._board.mines - self._flagged()
        if flagged < 0:
            flagged = 0
        flagged = str(int(flagged)).zfill(3)
        if len(flagged) > 3:
            flagged = UserInterfaceScore.max_score
        w, _ = pygame.display.get_surface().get_size()
        self.draw_shadow(
            screen, w - self._offset - self._sprites.one.get_width() * 3, self._offset
        )
        [
            screen.blit(tile, (self._offset + idx * tile.get_width(), self._offset))
            for idx, tile in enumerate(self._sprites[flagged])
        ]
