import pygame

class UserInterfaceFrame:
    white = (255, 255, 255)
    grey = (192, 192, 192)
    dark_grey = (128, 128, 128)
    def __init__(self, shadow=2, grey=5):
        self._shadow, self._grey = int(shadow), int(grey)
        self._frame_drawed = False

    @property
    def offset(self):
        return self._shadow * 2 + self._grey

    def draw_frame(self, screen, w, h):
        screen.fill(UserInterfaceFrame.grey, rect=(0, 0, w, h))
        self.draw_white(screen, w, h)
        self.draw_grey(screen, w, h)
        self.draw_dark_grey(screen, w, h)

    def draw_white(self, screen, w, h):
        screen.fill(UserInterfaceFrame.white, rect=(0, 0, self._shadow, h))
        screen.fill(UserInterfaceFrame.white, rect=(0, 0, w, self._shadow))

        offset = self._grey + self._shadow * 2
        screen.fill(UserInterfaceFrame.white, rect=(w - offset, offset, self._shadow, h - offset * 2 + self._shadow))
        screen.fill(UserInterfaceFrame.white, rect=(0, h - offset, w - offset, self._shadow))

    def draw_grey(self, screen, w, h):
        screen.fill(UserInterfaceFrame.grey, rect=(self._shadow, self._shadow, self._grey, h))
        screen.fill(UserInterfaceFrame.grey, rect=(self._shadow, self._shadow, w, self._shadow))

    def draw_dark_grey(self, screen, w, h):
        offset = self._shadow + self._grey
        screen.fill(UserInterfaceFrame.dark_grey, rect=(offset, offset, self._shadow, h - offset * 2))
        screen.fill(UserInterfaceFrame.dark_grey, rect=(offset, offset, w - offset * 2, self._shadow))

        screen.fill(UserInterfaceFrame.dark_grey, rect=(0, h - self._shadow, w, self._shadow))
        screen.fill(UserInterfaceFrame.dark_grey, rect=(w - self._shadow, 0, self._shadow, h))

    def draw(self, screen):
        self.draw_frame(screen, *pygame.display.get_surface().get_size())

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass
