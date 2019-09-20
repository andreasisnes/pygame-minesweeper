""" Minesweeper util """

import pygame

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

    def load_grid(self, grid=(4, 3), colorkey=None):
        "load grids of images and returns them as a list"
        rects  = []
        size_x = self.sheet.get_width()  // grid[0]
        size_y = self.sheet.get_height() // grid[1]
        for y in range(0, self.sheet.get_height(), size_y):
            for x in range(0, self.sheet.get_width(), size_x):
                rects.append((x, y, size_x, size_y))
        return self.images_at(rects, colorkey)
