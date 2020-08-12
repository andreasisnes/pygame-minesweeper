import appdirs
import json
import sys
from os.path import join, exists
from pathlib import Path
from argparse import Action
from appdirs import AppDirs
from datetime import timedelta

HIGHSCORE_DIR = AppDirs("pygame-minesweeper").user_data_dir
HIGHSCORE_FILE = join(HIGHSCORE_DIR, "high-score.json")


class HighScoreShow(Action):
    def __call__(self, parser, namespace, values, option_string):
        with open(HIGHSCORE_FILE, "r+") as f:
            score = json.load(f)
            if len(score.keys()) == 0:
                print("No games are played")
            for key, value in score.items():
                self.print_score(key, value)
        parser.exit()

    def print_score(self, key, value):
        sys.stdout.write("\n" + key.upper() + "\n-----\n")
        for entry in range(0, 10):
            if entry >= len(value):
                print(f"#{1 + entry:02} -")
            else:
                print(f"#{1 + entry:02} {str(timedelta(seconds=value[entry]))}")


def HighScoreInit():
    Path(HIGHSCORE_DIR).mkdir(parents=True, exist_ok=True)
    if not exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w+") as f:
            json.dump({}, f)


def HighScoreUpdate(entry: str, value: float):
    scores, value = {}, float(value)
    with open(HIGHSCORE_FILE, "r+") as f:
        try:
            scores = json.load(f)
            if entry not in scores:
                scores[entry] = [value]
            else:
                scores[entry].append(value)
            scores[entry].sort()
        except json.decoder.JSONDecodeError:
            scores[entry] = [value]
    with open(HIGHSCORE_FILE, "w+") as f:
        json.dump(scores, f)
