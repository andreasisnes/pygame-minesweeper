#!/usr/bin/env python
""" Minesweeper """

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEBUTTONDOWN

try:
    from .minesweeper import Board
except ImportError:
    from minesweeper import Board

def init(mainf):
    """ initialize and shutsdown minesweeper"""
    def initf():
        setup()
        mainf()
        teardown()
    return initf

def setup():
    """ setup hook runs before main """
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Minesweeper")

def teardown():
    """ teardown hook runs after main """
    pygame.quit()

@init
def main():
    """
    some doc
    """
    resolution = (512, 512)
    background = pygame.Surface(resolution)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    board = Board()
    done = False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
            if event.type == MOUSEBUTTONDOWN:
                board.mouse_down(event)
            if event.type == MOUSEBUTTONUP:
                board.mouse_up(event)
        board.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
