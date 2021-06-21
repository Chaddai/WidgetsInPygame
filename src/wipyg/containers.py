# -*- coding: utf-8 -*-
"""Provides a Frame container, with a grid, and a Window container with decorations."""

from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface, color
from pygame.draw import *

from wipyg.buttons import IconButton


class Frame(GridContainer):
    """A gridded Container without frills

    Attributes
    ----------
    bg_color : color
        The background color of the Frame
    """

    def __init__(
        self, widgets: list[list[Widget]], bg_color=(255, 255, 255, 0)
    ) -> None:
        """Create a gridded container that simply display all its children in the minimum space, each centered in its cell

        Parameters
        ----------
        widgets : list[list[Widget]], optional
            An initial grid of widgets, don't give it an empty list
        bg_color : color
            The background color of the Frame, by default transparent
        Raises
        ------
        ValueError
            widgets can't be empty, there must be at least one cell in the grid
        """
        if widgets == [] or widgets[0] == []:
            raise ValueError(
                "widgets can't be empty, there must be at least one cell in the grid"
            )
        super().__init__()
        self._bg_color = bg_color

        self._grid = widgets
        self.lines = len(widgets)
        self.columns = len(widgets[0])
        for y in range(self.lines):
            for x in range(self.columns):
                w = self._grid[y][x]
                if isinstance(w, Sprite):
                    self.add_widget(w)

        self.rect = self._grid_rect.copy()
        self.redraw()

    def redraw(self):
        bg_color = self._bg_color
        self._refresh_dims()
        self.rect.size = self._grid_rect.size

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill(bg_color)

        for y in range(self.lines):
            for x in range(self.columns):
                w = self._grid[y][x]
                if isinstance(w, Sprite):
                    # center the subwidgets in the cells
                    r = w.rect
                    i = w.image
                    r.center = self._cells[y][x].center
                    self.image.blit(i, r)
                    # place the rectangle of the subwidgets relative to the screen for
                    # correct event reactions
                    r.move_ip(self.rect.topleft)

    def _get_bg_color(self):
        return self._bg_color

    def _set_bg_color(self, bg_color):
        self._bg_color = bg_color
        self.redraw()

    bg_color = property(
        _get_bg_color, _set_bg_color, doc="The background color of the Frame"
    )


CROSS = Surface((20, 20), SRCALPHA)
line(CROSS, (0, 0, 0), (4, 4), (16, 16))
line(CROSS, (0, 0, 0), (16, 4), (4, 16))
BAR = Surface((20, 20), SRCALPHA)
line(BAR, (0, 0, 0), (4, 10), (16, 10))


class Window(Container):
    """A container with a window decoration

    The bar allows to close or minimize (roll up) or move the window as usual"""

    def __init__(self, window_content: Widget, bar_color=(110, 110, 110)) -> None:
        """Create a window with a bar with the usual controls to close or minimize the window

        Parameters
        ----------
        window_content : Widget
            The content of the window, usually a Frame but may be a single Widget
        bar_color : color, optional
            The color of the window bar, by default (110, 110, 110)
        """
        super().__init__()
        self._bar_color = bar_color
        self._close = IconButton(CROSS)
        self._minimize = IconButton(BAR)
        self._content = window_content
        self.add_widget(self._close)
        self.add_widget(self._minimize)
        self.add_widget(window_content)

        self.rect = Rect(0, 0, 0, 0)

        self._minimized = False
        self._close.add_reaction(Button.CLICKED, self._close_window)
        self._minimize.add_reaction(Button.CLICKED, self._min_window)
        self.add_reaction(MOUSEBUTTONDOWN, self._grabbing)
        self.add_reaction(MOUSEBUTTONUP, self._ungrabbing)
        self._grabbed = False

        self.redraw()

    def redraw(self):
        if self._minimized:
            self.rect.height = 20
        else:
            self._content.rect.topleft = self.rect.move(0, 20).topleft
            self._content.redraw()
            content_img = self._content.image
            content_rect = content_img.get_rect(y=20)

            self.rect.size = content_rect.size
            self.rect.height += 20

        self.image = Surface(self.rect.size, SRCALPHA)

        if not self._minimized:
            self.image.blit(content_img, content_rect)

        rect(self.image, self._bar_color, Rect(0, 0, self.rect.width, 20))

        self._close.rect.topright = self.rect.topright
        self._minimize.rect.topright = self.rect.move(-20, 0).topright
        self._close.redraw()
        self._minimize.redraw()
        self.image.blit(self._close.image, Rect(self.rect.width - 20, 0, 20, 20))
        self.image.blit(self._minimize.image, Rect(self.rect.width - 40, 0, 20, 20))

    def _close_window(self, source, e):
        if e.button == self._close:
            self.kill()

    def _min_window(self, source, e):
        if e.button == self._minimize:
            self._minimized = not self._minimized
            if self._minimized:
                self._content.disable()
            else:
                self._content.enable()
            self.redraw()

    def _grabbing(self, source, e):
        bar = self.rect.copy()
        bar.height = 20
        bar.width -= 40
        if bar.collidepoint(e.pos):
            self._grabbed = self.add_reaction(MOUSEMOTION, self._move_window)

    def _ungrabbing(self, source, e):
        if self._grabbed:
            self.del_reaction(self._grabbed)
            self._grabbed = False

    def _move_window(self, source, e):
        self.rect.move_ip(e.rel)
        self.redraw()
