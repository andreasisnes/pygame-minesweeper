# -*- coding: utf-8 -*-
""" Minesweeper """
import pygame
from os.path import dirname, join

try:
    from .util import Spritesheet
except ImportError:
    from util import Spritesheet


class Tiles:
    def __init__(self, size=(16, 16)):
        filename = join(dirname(__file__), "minesweeper_tiles.jpg")
        self.spritesheet = Spritesheet(filename)
        images = self.spritesheet.load_grid((4, 3), None)
        for i in range(len(images)):
            images[i] = pygame.transform.scale(images[i], size)
        
        self.images = {
            '?' : images[0],
            'f' : images[1],
            'x' : images[2],
            '0' : images[3],
            '1' : images[4],
            '2' : images[5],
            '3' : images[6],
            '4' : images[7],
            '5' : images[8],
            '6' : images[9],
            '7' : images[10],
            '8' : images[11],
        }
    def __getitem__(self, tile):
        return self.images[tile]

    def __iter__(self):
        return self.images.values().__iter__()

class Board(pygame.sprite.Sprite):
    def __init__(self, board_size=(32, 32), tile_size=(16, 16)):
        super().__init__()
        self.tile_total = board_size[0] * board_size[1]
        self.tile_opened = 0
        self.tile_size = tile_size
        self.board_size = board_size
        self.tiles = Tiles(self.tile_size)
        self.board = [[self.tiles['?'] for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]
        self.mouse_click_l = (-1, -1)
    
    def draw(self, screen):
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                screen.blit(tile, (tile.get_width() * i, tile.get_height() * j))

    def mouse_down(self, event):
        pos = self.mouse_pos(event.pos)
        
        # left click
        if event.button == 1 and self.board[pos[0]][pos[1]] == self.tiles['?']:
            self.board[pos[0]][pos[1]] = self.tiles['0']
            self.mouse_click_l = pos
        
        # right click
        elif event.button == 3 and self.board[pos[0]][pos[1]] == self.tiles['?']:
            self.board[pos[0]][pos[1]] = self.tiles['f']

    def mouse_up(self, event):
        pos = self.mouse_pos(event.pos)

        # left click
        if event.button == 1:
            if pos == self.mouse_click_l:
                self.tile_open(pos)
            else:
                print(pos, self.mouse_click_l)
                self.board[self.mouse_click_l[0]][self.mouse_click_l[1]] = self.tiles['?']

    def tile_open(self, pos):
        if self.tile_opened == 0:
            pass

    def mouse_pos(self, pos):
        return (pos[0] // self.tile_size[0], pos[1] // self.tile_size[1])

    @property
    def display_size(self):
        return (self.board_size[0] * self.tile_size[0], self.board_size[1] * self.tile_size[1])

if __name__ == "__main__":
    b = Board()
