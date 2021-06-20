from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface
from pygame.draw import *


class StandardButton(Button):
    """A normal button, light grey background when INACTIVE, almost white if ACTIVE, text greyed out if DISABLED"""

    def __init__(self, text="Ok", font=None, size=30) -> None:
        super().__init__()
        self._font = Font(font, size)
        self._text = text
        self.rect = Rect(0, 0, 0, 0)
        self._draw_button()

    def _draw_button(self):
        if self.state == Button.INACTIVE:
            bg_color = (210, 210, 210)
            text_color = (0, 0, 0)
        elif self.state == Button.ACTIVE:
            bg_color = (250, 250, 250)
            text_color = (0, 0, 0)
        elif self.state == Button.DISABLED:
            bg_color = (150, 150, 150)
            text_color = (100, 100, 100)

        pos = self.rect.topleft
        self._text_img = self._font.render(self._text, True, text_color)

        self._text_rect = self._text_img.get_rect()
        padding = self._font.get_height()
        self.rect = self._text_rect.inflate(2 * padding, 2 * padding)
        rect_center = (self.rect.w // 2, self.rect.h // 2)
        self._text_rect.center = rect_center

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill(bg_color)
        border = self.rect.inflate(-2, -2)
        border.center = rect_center
        rect(self.image, (0, 0, 0), border, width=2)
        self.image.blit(self._text_img, self._text_rect)

        # reposition the rect as initially
        self.rect.topleft = pos

    def update(self, *args, **kwargs) -> None:
        self._draw_button()
