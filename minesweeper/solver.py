#!/usr/bin/env python
""" Minesweeper """

try:
    import minesweeper
except ImportError:
    from . import minesweeper

class Solver:
    def __init__(self, API : minesweeper.API):
        self.api = API

if __name__ == "__main__":
    s = Solver(minesweeper.API(12, 12, 10))
