#!/usr/bin/env python
""" Minesweeper """
import sys
sys.stdout = None
import pygame
sys.stdout = sys.__stdout__
import argparse
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEBUTTONDOWN

try:
    from .gui import Board
    from .minesweeper import API
except ImportError:
    from gui import Board
    from minesweeper import API

def init(mainf):
    """ initialize and shutsdown minesweeper"""
    def initf():
        setup()
        mainf()
        teardown()
    return initf

def setup():
    global board, resolution, screen, mines, clock, width, height
    parser = argparse.ArgumentParser(description="""
    Minesweeper

    basic        : (10x10) - 10
    intermediate : (16x16) - 40
    expert       : (30x16) - 99
    """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("difficulty", choices=["basic", "intermediate", "expert"], help="")
    parser.add_argument("--no-color", action="store_false", help="")
    args = parser.parse_args()
    if args.difficulty == "basic":
        width, height, mines = 10, 10, 10
    elif args.difficulty == "intermediate":
        width, height, mines = 16, 16, 40
    else:
        width, height, mines = 30, 16, 99

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Minesweeper")
    resolution = (width * 16, height * 16 + 40)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    board = Board(API(width, height, mines), screen)

def teardown():
    pygame.quit()

@init
def main():
    """
    some doc
    """
    done = False
    rate = 0
    while not done:
        rate %= 30
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
            if event.type == MOUSEBUTTONDOWN:
                board.mouse_down(event)
                rate = 0
            if event.type == MOUSEBUTTONUP:
                board.mouse_up(event)
                rate = 0
        if rate == 0:
            board.draw(screen)
            pygame.display.flip()
        rate += 1

if __name__ == "__main__":
    main()
