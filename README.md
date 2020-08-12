[![Build Status](https://dev.azure.com/andreasisnes/Elitekollektivet/_apis/build/status/Elitekollektivet.Minesweeper/Elitekollektivet.Minesweeper?branchName=master)](https://dev.azure.com/andreasisnes/Elitekollektivet/_build/latest?definitionId=11&branchName=master)
[![PyPI - License](https://img.shields.io/pypi/l/pygame-minesweeper)](https://github.com/andreasisnes/Elitekollektivet.Minesweeper/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pygame-minesweeper)](https://pypi.org/project/pygame-minesweeper/)
[![Downloads](https://pepy.tech/badge/pygame-minesweeper)](https://pepy.tech/project/pygame-minesweeper)

# Minesweeper
Minesweeper is a single-player puzzle computer game. The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field. The game originates from the 1960s, and has been written for many computing platforms in use today. It has many variations and offshoots.

![](https://raw.githubusercontent.com/andreasisnes/Elitekollektivet.Minesweeper/master/screenshots/game_over.png)

This simple implementation of minesweeper is done in Python using the game library pygame.

The core functionality of the game can be found [here](https://github.com/andreasisnes/Elitekollektivet.Minesweeper.Core) and the python package for the sprite sheet can be found [here](https://github.com/andreasisnes/Elitekollektivet.Minesweeper.Sprites)

# Motivation
The motivation of these minesweeper projects is to learn the tooling around python projects, how to create CI/CD pipelines for python projects, and distributing python eggs.

# Getting Started

## Installation
```bash
python -m pip install pygame-minesweeper
# or
pip install pygame-minesweeper
```

## Start a game
```bash
# if $HOME/.local/bin/ is defined in $PATH
minesweeper <basic | intermediate | expert | custom>
# or
python -m minesweeper <basic | intermediate | expert | custom>`
```

## Boards

| scheme       | rows   | cols   | mines   |
| ------------ | ------ | ------ | ------- |
| Basic        | 10     | 10     | 10      |
| Intermediate | 16     | 16     | 40      |
| expert       | 6      | 30     | 99      |
| custom       | --rows | --cols | --mines |

## Show high Score
```bash
minesweeper --show-high-score
# or
python -m minesweeper --show-high-score
```

```bash
# Stdout

BASIC
-----
#01 0:00:22.641516
#02 0:00:29.936435
#03 0:01:02.104885
#04 -
#05 -
#06 -
#07 -
#08 -
#09 -
#10 -

CUSTOM 10X10:5
-----
#01 0:00:15.618247
#02 -
#03 -
#04 -
#05 -
#06 -
#07 -
#08 -
#09 -
#10 -
```

## Start a game with a different sprite sheet
The `--tile-sprite`, `--face-sprite`, and `--score-sprite` parameters define a set of sprite sheets that are available from this [python package](https://github.com/andreasisnes/Elitekollektivet.Minesweeper.Sprites).

```bash
# if $HOME/.local/bin/ is defined in $PATH
minesweeper -h
# or
python -m minesweeper -h
```
```bash
#stdout
positional arguments:
  {basic,intermediate,expert,custom}

optional arguments:
  -h, --help            show this help message and exit
  --rows ROWS
  --cols COLS
  --mines MINES
  --tile-sprite {2.0,2.9,95,2000,fiorito-2000,fiorito-monochrome,fiorito-xp,monochrome}
  --score-sprite {2000,monochrome}
  --face-sprite {2000,monochrome}
  --sprite {2000,monochrome}
  --show-high-score
```

If the --sprite flag is set it will override the other flags like `--tile-sprite`, `--score-sprite` and `--face-sprite`.
```bash
# Starting an *Expert* game with a full monochrome spritesheet
minesweeper expert --sprite=monochrome
# or
python -m minesweeper expert --sprite=monochrome
```
![monochrome](https://raw.githubusercontent.com/andreasisnes/Elitekollektivet.Minesweeper/master/screenshots/game_over_monochrome.png)

## Credits
### Sprites

The sprites used in this project were created by [Black Squirrel](https://www.spriters-resource.com/submitter/Black+Squirrel/) and can be found [here.](https://www.spriters-resource.com/pc_computer/minesweeper/sheet/19849/)

## TODO
* Refactor Project

## References
* https://en.wikipedia.org/wiki/Minesweeper_(video_game)
