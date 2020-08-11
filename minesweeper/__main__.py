import sys
sys.stdout = None
import pygame
sys.stdout = sys.__stdout__
import argparse
import appdirs
import json
from os.path import join
from pathlib import Path
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from minesweeper.sprites import *

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


class ShowHighScore(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        directory = appdirs.AppDirs("pygame-minesweeper").user_data_dir
        Path(directory).mkdir(parents=True, exist_ok=True)
        score = join(directory, "high-score.json")
        with open(score, "r+") as f:
            try:
                t = json.load(f)
                for key, value in t.items():
                    self.print_score(key, value)
            except json.decoder.JSONDecodeError:
                print("No Games are played")
        parser.exit()

    def print_score(self, key, value):
        print("\n")
        print(key.upper())
        print("-----")
        for entry in range(0, 10):
            if entry >= len(value):
                print(f"#{1 + entry:02} -")
            else:
                print(f"#{1 + entry:02} {value[entry]}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("difficulty", type=str, choices=["basic", "intermediate", "expert", "custom"], default="basic")
    parser.add_argument("--rows",  type=int, default=10)
    parser.add_argument("--cols",  type=int, default=10)
    parser.add_argument("--mines", type=int, default=10)
    parser.add_argument("--tile-sprite", type=str, choices=TileSheets.__sheets__, default=TileSheets.two_thousand)
    parser.add_argument("--score-sprite", type=str, choices=ScoreSheets.__sheets__, default=ScoreSheets.two_thousand)
    parser.add_argument("--face-sprite", type=str, choices=FaceSheets.__sheets__, default=FaceSheets.two_thousand)
    parser.add_argument("--sprite", type=str, choices=FaceSheets.__sheets__)
    parser.add_argument("--show-high-score", nargs=0, action=ShowHighScore)
    return parser.parse_args()

@init
def main():
    args = parse_args()
    tile_sprite = TileBuilder(TileSheets(args.tile_sprite))
    score_sprite = ScoreBuilder(ScoreSheets(args.score_sprite))
    face_sprite = FaceBuilder(FaceSheets(args.face_sprite))
    if args.sprite != None:
        tile_sprite = TileBuilder(TileSheets(args.sprite))
        score_sprite = ScoreBuilder(ScoreSheets(args.sprite))
        face_sprite = FaceBuilder(FaceSheets(args.sprite))

    if args.difficulty == "basic":
        game(UserInterface(10, 10, 10, tile_sprite=tile_sprite, score_sprite=score_sprite, face_sprite=face_sprite))
    elif args.difficulty == "intermediate":
        game(UserInterface(16, 16, 40, tile_sprite=tile_sprite, score_sprite=score_sprite, face_sprite=face_sprite))
    elif args.difficulty == "expert":
        game(UserInterface(30, 16, 99, tile_sprite=tile_sprite, score_sprite=score_sprite, face_sprite=face_sprite))
    else:
        game(UserInterface(args.rows, args.cols, args.mines, tile_sprite=tile_sprite, score_sprite=score_sprite, face_sprite=face_sprite))

def game(ui):
    clock = pygame.time.Clock()
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
