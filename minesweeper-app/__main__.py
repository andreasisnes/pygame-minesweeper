import sys
sys.stdout = None
import pygame
sys.stdout = sys.__stdout__
import argparse
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEBUTTONDOWN


try:
    from .user_interface import UserInterface
except ImportError:
    from user_interface import UserInterface

def init(mainf):
    def initf():
        setup()
        mainf()
        teardown()
    return initf

def setup():
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Pygame - Minesweeper")

def teardown():
    pygame.quit()

@init
def main():
    clock = pygame.time.Clock()
    game(clock, UserInterface(10, 10, 10))

def game(clock, ui):
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                return
            ui.event_handler(event)
        if ui.draw():
            pygame.display.flip()

if __name__ == "__main__":
    main()
