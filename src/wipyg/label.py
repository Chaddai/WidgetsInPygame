# -*- coding: utf-8 -*-
"""Provide the Label widget type."""

from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface
from pygame.draw import *


class Label(Widget):
    """A simple label Widget to show some text"""  # TODO #1 add newline support

    def __init__(
        self,
        text="Hello",
        font=None,
        size=30,
        color=(0, 0, 0),
        bg_color=(255, 255, 255, 0),
    ) -> None:
        """Create a Label widget

        Parameters
        ----------
        text : str, optional
            Text to display, by default "Hello"
        font : file | filename, optional
            Font to use, see `pygame.font`, by default None
        size : int, optional
            Font size in pixel, by default 30
        color : color, optional
            color of the text, by default black
        bg_color : color, optional
            background color, by default transparent
        """
        super().__init__()
        self._font = Font(font, size)
        self._text = text
        self._text_color = color
        self._bg_color = bg_color
        self.rect = Rect(0, 0, 0, 0)
        self.redraw()

    def redraw(self):
        bg_color = self._bg_color

        pos = self.rect.topleft
        self._text_img = self._font.render(self._text, True, self._text_color)

        self._text_rect = self._text_img.get_rect()
        padding = self._font.get_height()
        self.rect = self._text_rect.inflate(padding, padding)
        rect_center = (self.rect.w // 2, self.rect.h // 2)
        self._text_rect.center = rect_center

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill(bg_color)
        self.image.blit(self._text_img, self._text_rect)

        # reposition the rect as initially
        self.rect.topleft = pos
