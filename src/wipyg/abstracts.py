from abc import ABC, abstractmethod
from typing import DefaultDict, Tuple
from pygame.sprite import *
from pygame.event import Event, custom_type, post
from pygame.rect import Rect
from pygame.constants import *


class Widget(Sprite, ABC):
    """Abstract class for widgets

    Methods :
    - update()
    - react(e : Event)
    - add_reaction(type : int, callback : (Widget, Event) -> bool) -> (int, int)
    - del_reaction(idReaction : (int, int))

    Properties :
    - rect : Rect
    - image : Surface
    """

    def __init__(self) -> None:
        super().__init__()
        self._reactions = DefaultDict(list)

    def react(self, e: Event):
        for reaction in self._reactions[e.type]:
            reaction(self, e)

    def add_reaction(self, type, callback):
        reactions = self._reactions[type]
        reactions.append(callback)
        return (type, len(reactions) - 1)

    def del_reaction(self, idReaction: Tuple[int, int]):
        type, index = idReaction
        del self._reactions[type][index]


class Container(Widget, ABC):
    """Abstract class for a Widget that can contain other widgets

    Additional methods :
    - set_grid(col : int, line : int, w : Widget)
    - get_grid(col : int, line : int) -> Widget
    - del_widget(col : int, line : int)

    Additional properties :
    - columns : int
    - lines : int
    """

    def __init__(self) -> None:
        super().__init__()
        self._grid = [[None]]
        self._xdims = [0]
        self._ydims = [0]
        self._columns = 1
        self._lines = 1
        self._grid_rect = Rect(0, 0, 0, 0)

    def _refresh_dims(self):
        for i in range(self._lines):
            for j in range(self._columns):
                w = self._grid[i][j]
                if isinstance(w, Sprite):
                    self._xdims[j] = max(self._xdims[j], w.rect.width)
                    self._ydims[j] = max(self._ydims[j], w.rect.height)
        self._grid_rect.width = sum(self._xdims)
        self._grid_rect.height = sum(self._ydims)

    def set_grid(self, col: int, line: int, w: Widget):
        if col > self._columns:
            self.columns = col
        if line > self._lines:
            self.lines = line
        self._grid[line][col] = w

    def get_grid(self, col: int, line: int) -> Widget:
        if col > self._columns or line > self._lines:
            return
        else:
            return self._grid[line][col]

    def del_widget(self, col: int, line: int):
        if col > self._columns or line > self._lines:
            return
        else:
            w = self._grid[line][col]
            if isinstance(w, Sprite):
                w.kill()
            self._grid[line][col] = None

    def _get_lines(self):
        return self._lines

    def _set_lines(self, lines: int):
        if lines < 0:
            return
        elif lines < self._lines:
            for line in range(lines, self._lines):
                for w in self._grid[line]:
                    if isinstance(w, Sprite):
                        w.kill()
            self._grid = self._grid[:lines]
            self._ydims = self._ydims[:lines]
        elif lines > self._lines:
            for line in range(self.lines, lines):
                self._grid.append([None for _ in range(self._columns)])

    lines = property(_get_lines, _set_lines)

    def _get_columns(self):
        return self._columns

    def _set_columns(self, columns: int):
        if columns < 0:
            return
        elif columns < self._columns:
            for i, line in enumerate(self._grid):
                for w in line[columns : self._columns]:
                    if isinstance(w, Sprite):
                        w.kill()
                self._grid[i] = line[:columns]
            self._xdims = self._xdims[:columns]
        elif columns > self._columns:
            for line in self._grid:
                line.extend([None for _ in range(self._columns, columns)])

    columns = property(_get_columns, _set_columns)

    def update(self, *args, **kwargs) -> None:
        for i in range(self._lines):
            for j in range(self._columns):
                w = self._grid[i][j]
                if isinstance(w, Sprite):
                    w.update()
        self._refresh_dims()


class Button(Widget, ABC):
    """Abstract class for a Widget that can be "clicked" and can be in an "active", "inactive" or "disabled" state

    Special event :
    - Button.CLICKED (launched if the mouse has a left MOUSEBUTTONUP on this button)

    Additional property :
    - state : int (Button.ACTIVE, Button.INACTIVE, Button.DISABLED)
    """

    CLICKED = custom_type()
    INACTIVE = 0
    ACTIVE = 1
    DISABLED = 2

    def _mouse_down(self, e):
        if self.state != Button.DISABLED and self.rect.collidepoint(e.pos):
            self.state = Button.ACTIVE

    def _mouse_up(self, e):
        if self.state != Button.DISABLED and self.rect.collidepoint(e.pos):
            self.state = Button.INACTIVE
            post(Event(Button.CLICKED, {"button": self}))

    def __init__(self) -> None:
        super().__init__()
        self.state = Button.INACTIVE
        self._reactions[MOUSEBUTTONDOWN].append(self._mouse_down)
        self._reactions[MOUSEBUTTONUP].append(self._mouse_up)
