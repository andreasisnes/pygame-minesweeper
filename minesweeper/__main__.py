import sys

sys.stdout = None
import pygame

sys.stdout = sys.__stdout__
import argparse
from os.path import exists
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from minesweeper.sprites import (
    TileBuilder,
    TileSheets,
    ScoreBuilder,
    ScoreSheets,
    FaceBuilder,
    FaceSheets,
)

try:
    from .user_interface import UserInterface
    from .util import HighScoreInit, HighScoreShow, HighScoreUpdate
except ImportError:
    from user_interface import UserInterface
    from util import HighScoreInit, HighScoreShow, HighScoreUpdate


def init(mainf):
    def initf():
        setup()
        mainf()
        teardown()

    return initf


def setup():
    HighScoreInit()
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Pygame - Minesweeper")


def teardown():
    pygame.quit()


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
    Minesweeper

    basic        : 10 x 10   - 10 mines
    intermediate : 16 x 16   - 40 mines
    expert       : 16 x 30   - 99 mines
    custom       : ROWSxCOLS - MINES mines
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "difficulty",
        type=str,
        choices=["basic", "intermediate", "expert", "custom"],
        default="basic",
    )
    parser.add_argument("--rows", type=int, default=10)
    parser.add_argument("--cols", type=int, default=10)
    parser.add_argument("--mines", type=int, default=10)
    parser.add_argument(
        "--tile-sprite",
        type=str,
        choices=TileSheets.__sheets__,
        default=TileSheets.two_thousand,
    )
    parser.add_argument(
        "--score-sprite",
        type=str,
        choices=ScoreSheets.__sheets__,
        default=ScoreSheets.two_thousand,
    )
    parser.add_argument(
        "--face-sprite",
        type=str,
        choices=FaceSheets.__sheets__,
        default=FaceSheets.two_thousand,
    )
    parser.add_argument("--sprite", type=str, choices=FaceSheets.__sheets__)
    parser.add_argument("--show-high-score", nargs=0, action=HighScoreShow)
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
        game(
            UserInterface(
                10,
                10,
                10,
                lambda x: HighScoreUpdate("basic", x),
                tile_sprite=tile_sprite,
                score_sprite=score_sprite,
                face_sprite=face_sprite,
            )
        )
    elif args.difficulty == "intermediate":
        game(
            UserInterface(
                16,
                16,
                40,
                lambda x: HighScoreUpdate("intermediate", x),
                tile_sprite=tile_sprite,
                score_sprite=score_sprite,
                face_sprite=face_sprite,
            )
        )
    elif args.difficulty == "expert":
        game(
            UserInterface(
                16,
                30,
                99,
                lambda x: HighScoreUpdate("expert", x),
                tile_sprite=tile_sprite,
                score_sprite=score_sprite,
                face_sprite=face_sprite,
            )
        )
    else:
        game(
            UserInterface(
                args.rows,
                args.cols,
                args.mines,
                lambda x: HighScoreUpdate(
                    f"custom {args.rows}x{args.cols}:{args.mines}", x
                ),
                tile_sprite=tile_sprite,
                score_sprite=score_sprite,
                face_sprite=face_sprite,
            )
        )


def game(ui: UserInterface):
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            ui.event_handler(event)
        if ui.draw():
            pygame.display.flip()


if __name__ == "__main__":
    main()
