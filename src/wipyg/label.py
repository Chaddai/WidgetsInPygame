from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface
from pygame.draw import *


class Label(Widget):
    """A simple label Widget to show some text"""  # TODO add newline support

    def __init__(self, text="Hello", font=None, size=30, color=(0, 0, 0)) -> None:
        super().__init__()
        self._font = Font(font, size)
        self._text = text
        self._text_color = color
        self.rect = Rect(0, 0, 0, 0)
        self._draw_label()

    def _draw_label(self):
        bg_color = (210, 210, 210)

        pos = self.rect.topleft
        self._text_img = self._font.render(self._text, True, self._text_color)

        self._text_rect = self._text_img.get_rect()
        size = self._font.get_height()
        self.rect = self._text_rect.inflate(size, size)
        rect_center = (self.rect.w // 2, self.rect.h // 2)
        self._text_rect.center = rect_center

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill(bg_color)
        self.image.blit(self._text_img, self._text_rect)

        # reposition the rect as initially
        self.rect.topleft = pos
