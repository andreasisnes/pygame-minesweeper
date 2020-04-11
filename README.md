# Minesweeper
Minesweeper is a single-player puzzle computer game. The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field. The game originates from the 1960s, and has been written for many computing platforms in use today. It has many variations and offshoots.

![](https://raw.githubusercontent.com/andreasisnes/minesweeper/master/screenshots/ingame.png)

This implementation of minesweeper is done in Python using the game library pygame.

## Install
To install pygame-minesweeper use `pip`.<br/>
`python -m pip install --user pygame-minesweeper`

## Run
To run the game, type following.<br/>
`minesweeper <basic | intermediate | expert>`

### Boards
#### Basic
Width : 10, Height : 10, Mines: 10

#### Intermediate
width : 16, Height : 16, Mines: 40

#### Expert
Width : 30, Height : 16, Mines: 99


## Credits
### Sprites

The sprites used in this project were created by [Black Squirrel](https://www.spriters-resource.com/submitter/Black+Squirrel/) and can be found [here.](https://www.spriters-resource.com/pc_computer/minesweeper/sheet/19849/)

## TODO
* Track score
* Custom boards

## References
* https://en.wikipedia.org/wiki/Minesweeper_(video_game)
