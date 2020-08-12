import pygame


class UserInterfaceFrame:
    def __init__(
        self,
        shadow=2,
        grey=5,
        white_color=(255, 255, 255),
        grey_color=(192, 192, 192),
        dark_grey_color=(128, 128, 128),
    ):
        self._shadow, self._grey = int(shadow), int(grey)
        self._frame_drawed = False
        self._white_color = white_color
        self._grey_color = grey_color
        self._dark_grey_color = dark_grey_color

    @property
    def offset(self):
        return self._shadow * 2 + self._grey

    def draw_white(self, screen, w, h):
        screen.fill(self._white_color, rect=(0, 0, self._shadow, h))
        screen.fill(self._white_color, rect=(0, 0, w, self._shadow))

        offset = self._grey + self._shadow * 2
        screen.fill(
            self._white_color,
            rect=(w - offset, offset, self._shadow, h - offset * 2 + self._shadow),
        )
        screen.fill(self._white_color, rect=(0, h - offset, w - offset, self._shadow))

    def draw_grey(self, screen, w, h):
        screen.fill(self._grey_color, rect=(self._shadow, self._shadow, self._grey, h))
        screen.fill(
            self._grey_color, rect=(self._shadow, self._shadow, w, self._shadow)
        )

    def draw_dark_grey(self, screen, w, h):
        offset = self._shadow + self._grey
        screen.fill(
            self._dark_grey_color, rect=(offset, offset, self._shadow, h - offset * 2)
        )
        screen.fill(
            self._dark_grey_color, rect=(offset, offset, w - offset * 2, self._shadow)
        )

        screen.fill(self._dark_grey_color, rect=(0, h - self._shadow, w, self._shadow))
        screen.fill(self._dark_grey_color, rect=(w - self._shadow, 0, self._shadow, h))

    def draw(self, screen, board_size):
        w, h = pygame.display.get_surface().get_size()
        board_size = h - board_size - (self._shadow * 4) - (self._grey * 2)
        screen.fill(self._grey_color, rect=(0, 0, w, h))
        self.draw_white(screen, w, h)
        self.draw_grey(screen, w, h)
        self.draw_dark_grey(screen, w, h)

        screen.fill(
            self._white_color,
            rect=(self.offset, board_size, w - self.offset * 2, self._shadow),
        )
        screen.fill(
            self._grey_color,
            rect=(
                self._shadow,
                board_size + self._shadow,
                w - (self._shadow * 2),
                self._grey,
            ),
        )
        screen.fill(
            self._dark_grey_color,
            rect=(
                self.offset,
                board_size + self._shadow + self._grey,
                w - self.offset * 2,
                self._shadow,
            ),
        )
