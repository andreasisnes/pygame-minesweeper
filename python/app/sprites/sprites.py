""" Minesweeper util """

from os.path import join, dirname
import pygame
import copy

class Spritesheet:
    """ Spritesheet """
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print("Unable to load spritesheet image: %s" % filename)
            raise SystemExit(message)

    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid(self, grid, colorkey=None):
        "load grids of images and returns them as a list"
        rects = []
        size_x = self.sheet.get_width()  // grid[0]
        size_y = self.sheet.get_height() // grid[1]
        for pos_y in range(0, self.sheet.get_height(), size_y):
            for pos_x in range(0, self.sheet.get_width(), size_x):
                rects.append((pos_x, pos_y, size_x, size_y))
        return self.images_at(rects, colorkey)


class Tile(Spritesheet):
    """ Tile """
    def  __init__(self, api, color=True):
        if color:
            super().__init__(join(dirname(__file__), "color_tiles.png"))
        else:
            super().__init__(join(dirname(__file__), "bw_tiles.png"))
        images = self.load_grid((8, 2))
        self.images = {
            api.encoder.ascii_tile      : images[0],
            api.encoder.ascii_mine      : images[5],
            'f'  : images[2],
            '?'  : images[3],
            '*?' : images[4],
            '*x' : images[6],
            'fx' : images[7],

            # nums
            '0' : images[1],
            '1' : images[8],
            '2' : images[9],
            '3' : images[10],
            '4' : images[11],
            '5' : images[12],
            '6' : images[13],
            '7' : images[14],
            '8' : images[15],
        }
        self.width = images[0].get_width()
        self.height = images[0].get_height()

    def __getitem__(self, tile):
        return self.images[tile]


class Face(Spritesheet):
    """ Face """
    def __init__(self, color=True):
        if color:
            super().__init__(join(dirname(__file__), "color_face.png"))
        else:
            super().__init__(join(dirname(__file__), "bw_tiles.png"))
        images = self.load_grid((5, 1))
        self.images = {
            ':)'  : images[0],
            '*:)' : images[1],
            ':o'  : images[2],
            'B)'  : images[3],
            'x('  : images[4],
        }
        self.width = images[0].get_width()
        self.height = images[0].get_height()
    def __getitem__(self, face):
        return self.images[face]



class Score(Spritesheet):
    """ Score """
    def __init__(self, color=True):
        if color:
            super().__init__(join(dirname(__file__), "color_face.png"))
        else:
            super().__init__(join(dirname(__file__), "bw_face.png"))

        images = self.load_grid((10, 1))
        self.images = {
            '0' : images[0],
            '1' : images[1],
            '2' : images[2],
            '3' : images[3],
            '4' : images[4],
            '5' : images[5],
            '6' : images[6],
            '7' : images[7],
            '8' : images[8],
            '9' : images[9],
        }
        self.width = images[0].get_width()
        self.height = images[0].get_height()
    def __getitem__(self, number):
        return self.images[str(number)]
