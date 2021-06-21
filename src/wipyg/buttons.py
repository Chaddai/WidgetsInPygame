# -*- coding: utf-8 -*-
"""Provide several buttons widget type."""

from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface
from pygame.draw import *


class PlainButton(Button):
    """A normal button, light grey background when INACTIVE, almost white if ACTIVE, text greyed out if DISABLED

    Derive this class and override _colors to provide variations with different colors (in the three states)
    """

    def __init__(
        self, text="Ok", font=None, size=30, state: int = Button.INACTIVE
    ) -> None:
        """Create a plain button with grey background and black text

        Parameters
        ----------
        text : str, optional
            The text displayed on the button, by default "Ok"
        font : file | filename, optional
            The source file for the font, by default None, that is the default Pygame sys font
        size : int, optional
            Font size (in pixels), by default 30
        state : int, optional
            Initial state of the button, one of (Button.ACTIVE, Button.INACTIVE, Button.DISABLED), by default Button.INACTIVE
        """
        super().__init__(state)
        self._font = Font(font, size)
        self._text = text
        self.rect = Rect(0, 0, 0, 0)
        self.redraw()

    def redraw(self):
        bg_color, text_color = self._colors()

        pos = self.rect.topleft
        self._text_img = self._font.render(self._text, True, text_color)

        self._text_rect = self._text_img.get_rect()
        xsize, ysize = self._text_rect.size
        padding = self._font.get_height()
        self.rect = Rect(0, 0, xsize + 2 * padding, ysize + 2 * padding)
        self._text_rect.center = self.rect.center

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill(bg_color)
        rect(self.image, (0, 0, 0), self.rect, width=3)
        self.image.blit(self._text_img, self._text_rect)

        # reposition the rect as initially
        self.rect.topleft = pos

    def _colors(self):
        if self.state == Button.INACTIVE:
            bg_color = (210, 210, 210)
            text_color = (0, 0, 0)
        elif self.state == Button.ACTIVE:
            bg_color = (250, 250, 250)
            text_color = (0, 0, 0)
        elif self.state == Button.DISABLED:
            bg_color = (150, 150, 150)
            text_color = (100, 100, 100)
        return bg_color, text_color


class CancelButton(PlainButton):
    """Button to cancel or refuse actions/things : red in INACTIVE, pink in ACTIVE, greyish red in DISABLED"""

    def _colors(self):
        if self.state == Button.INACTIVE:
            bg_color = (255, 0, 0)
            text_color = (255, 255, 255)
        elif self.state == Button.ACTIVE:
            bg_color = (219, 127, 127)
            text_color = (0, 0, 0)
        elif self.state == Button.DISABLED:
            bg_color = (110, 0, 0)
            text_color = (100, 100, 100)
        return bg_color, text_color


class SubmitButton(PlainButton):
    """Button to submit or accept actions/things : green in INACTIVE, light green in ACTIVE, greyish green in DISABLED"""

    def _colors(self):
        if self.state == Button.INACTIVE:
            bg_color = (0, 255, 0)
            text_color = (255, 255, 255)
        elif self.state == Button.ACTIVE:
            bg_color = (117, 255, 117)
            text_color = (0, 0, 0)
        elif self.state == Button.DISABLED:
            bg_color = (0, 110, 0)
            text_color = (100, 100, 100)
        return bg_color, text_color


class IconButton(Button):
    """A button that is just a Surface (or several if you chose to provide ACTIVE and DISABLED versions)"""

    def __init__(
        self,
        icon: Surface,
        active_icon: Surface = None,
        disabled_icon=None,
        state: int = Button.INACTIVE,
    ) -> None:
        """Create an icon button

        Parameters
        ----------
        icon : Surface
            the normal appearance of the button, clicking anywhere on the Surface will post a Button.CLICKED
        active_icon : Surface, optional
            Appearance of the button when clicked on (before MOUSEBUTTONUP fires), by default the same as icon
        disabled_icon : [type], optional
            Appearance of the button if it is in Button.DISABLED state, by default the same as icon
        state : int, optional
            Initial state of the button, by default Button.INACTIVE

        Raises
        ------
        ValueError
            [description]
        """
        super().__init__(state)
        if active_icon is None:
            active_icon = icon
        if disabled_icon is None:
            disabled_icon = icon
        self._icons = [icon, active_icon, disabled_icon]
        if active_icon.get_rect() != icon.get_rect():
            raise ValueError(
                "Both the icon and active_icon must have the same dimensions"
            )
        self.rect = icon.get_rect()
        self.image = self._icons[state]

    def _set_state(self, state):
        self.image = self._icons[state]
        super()._set_state(state)

    def redraw(self):
        self.image = self._icons[self.state]
