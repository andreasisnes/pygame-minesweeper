import pygame

try:
    import sprites
    import minesweeper
except ImportError:
    from . import sprites
    from . import minesweeper


class Board:
    def __init__(self, api : minesweeper.API):
        super().__init__()
        self.api = api
        self.tiles = sprites.Tile()
        self.board = []
        self.last_click = (-1, -1)
        for row in self.api.board:
            r = []
            for tile in row:
                if tile == minesweeper.MINE:
                    r.append(self.tiles['x'])
                elif tile == minesweeper.TILE:
                    r.append(self.tiles['t'])
                else:
                    r.append(self.tiles[str(tile)])
            self.board.append(r)
    
    def game_reset(self):
        self.api.game_reset()
        self.__init__(self.api)
    
    def game_new(self, width, height, mines):
        self.api.game_new(width, height, mines)
        self.__init__(self.api)

    def game_over(self):
        for pos_x, row in enumerate(self.board):
            for pos_y, tile in enumerate(row):
                if self.api.sheet[pos_x][pos_y] == minesweeper.MINE:
                    if tile == self.tiles['t']:
                        self.board[pos_x][pos_y] = self.tiles['x']
                else:
                    if tile == self.tiles['f']:
                        self.board[pos_x][pos_y] = self.tiles['fx']

    def draw(self, screen):
        for pos_x, row in enumerate(self.board):
            for pos_y, tile in enumerate(row):
                screen.blit(tile, (tile.get_width() * pos_x, tile.get_height() * pos_y))

    def mouse_down_left(self, event):
        if self.api.is_game_over:
            return
        
        pos_x, pos_y = self.mouse_pos(event.pos)
        if self.api.tile_valid(pos_x, pos_y):
            if self.api.board[pos_x][pos_y] == minesweeper.TILE:
                if self.board[pos_x][pos_y] == self.tiles['t']:
                    self.board[pos_x][pos_y] = self.tiles['0']
                elif self.board[pos_x][pos_y] == self.tiles['?']:
                    self.board[pos_x][pos_y] = self.tiles['*?']
                else:
                    return
                self.last_click = (pos_x, pos_y)

    def mouse_down_right(self, event):
        if self.api.is_game_over:
            return
        
        pos_x, pos_y = self.mouse_pos(event.pos)
        if self.api.tile_valid(pos_x, pos_y):
            if self.board[pos_x][pos_y] == self.tiles['t']:
                self.board[pos_x][pos_y] = self.tiles['f']
            elif self.board[pos_x][pos_y] == self.tiles['f']:
                self.board[pos_x][pos_y] = self.tiles['?']
            elif self.board[pos_x][pos_y] == self.tiles['?']:
                self.board[pos_x][pos_y] = self.tiles['t']
                

    def mouse_up_left(self, event):
        if self.api.is_game_over:
            return

        pos_x, pos_y = self.mouse_pos(event.pos)
        if self.last_click != (pos_x, pos_y):
            if self.api.board[self.last_click[0]][self.last_click[1]] == minesweeper.TILE:
                if self.board[self.last_click[0]][self.last_click[1]] == self.tiles['0']:
                    self.board[self.last_click[0]][self.last_click[1]] = self.tiles['t']
                elif self.board[self.last_click[0]][self.last_click[1]] == self.tiles['*?']:
                    self.board[self.last_click[0]][self.last_click[1]] = self.tiles['?']
            self.last_click = (-1, -1)
            return
        
        if self.api.tile_valid(pos_x, pos_y):
            if (pos_x, pos_y) == self.last_click and self.api.board[pos_x][pos_y] == minesweeper.TILE:
                for tile in self.api.tile_open(pos_x, pos_y):
                    if tile['value'] == minesweeper.MINE:
                        self.board[pos_x][pos_y] = self.tiles['*x']
                        self.game_over()
                    else:
                        self.board[tile['x']][tile['y']] = self.tiles[str(tile['value'])]
        print(self.api)

    def mouse_up_right(self, event):
        pos_x, pos_y = self.mouse_pos(event.pos)
        if self.api.tile_valid(pos_x, pos_y) and not self.api.is_game_over:
            pass

    def mouse_down(self, event):
        if event.button == 1:
            return self.mouse_down_left(event)
        elif event.button == 3:
            return self.mouse_down_right(event)
    
    def mouse_up(self, event):
        if event.button == 1:
            return self.mouse_up_left(event)
        elif event.button == 3:
            return self.mouse_up_right(event)

    def mouse_pos(self, pos):
        return (pos[0] // self.api.width, pos[1] // self.api.height)