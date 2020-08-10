from minesweeper import core
from minesweeper import sprites
from typing import Callable
import pygame

class UserInterfaceScore:
    max_score = "999"
    def __init__(self, board: core.Board, sprites: sprites.ScoreBuilder, offset: int, flagged : Callable[[], int]):
        self._board = board
        self._sprites = sprites.build()
        self._flagged = flagged
        self._offset = int(offset)

    def game_reset(self):
        pass

    def draw(self, screen):
        self.draw_timer(screen)
        self.draw_mines(screen)

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def draw_timer(self, screen):
        elapsed = str(int(self._board.timer)).zfill(3)
        if len(elapsed) > 3:
            elapsed = UserInterfaceScore.max_score
        width, _ = pygame.display.get_surface().get_size()
        [screen.blit(tile, (width - self._offset - ((idx + 1) * tile.get_width()), self._offset)) for idx, tile in enumerate(reversed(self._sprites[elapsed]))]

    def draw_mines(self, screen):
        flagged = self._board.mines - self._flagged()
        if flagged < 0:
            flagged = 0
        flagged = str(int(flagged)).zfill(3)
        if len(flagged) > 3:
            flagged = UserInterfaceScore.max_score
        [screen.blit(tile, (self._offset + idx * tile.get_width(), self._offset)) for idx, tile in enumerate(self._sprites[flagged])]
