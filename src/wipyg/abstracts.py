from abc import ABC, abstractmethod
from typing import DefaultDict, Tuple
from pygame.draw import line
from pygame.sprite import *
from pygame.event import Event, custom_type, post
from pygame.rect import Rect
from pygame.constants import *


class Widget(Sprite, ABC):
    """Abstract class for widgets, extends Sprite

    Methods
    -------
    react(e : Event)
        To call in the event loop so that the widget react to the event
    add_reaction(type : int, callback : (Widget, Event) -> bool) -> (int, int)
        Add a callback to react to a certain type (pygame.event.EventType) of event
        Use the returned value as an id for the callback so you can delete it
    del_reaction(idReaction : (int, int))
        Delete a callback with the id that was returned when you added it

    Abstract methods
    ----------------
    redraw()
        Must change the image attribute to reflect the current state of the Widget

    Attributes
    ----------
    container : Container
        The Frame or Window or other subclass of Container that contains this Widget, or None if independent
    """

    def __init__(self) -> None:
        super().__init__()
        self._reactions = DefaultDict(list)
        self.container = None

    def react(self, event: Event):
        """Loop through the callbacks installed through add_reaction and call the appropriates one for the event type

        Parameters
        ----------
        event : Event
            The event which must be handled

        Returns
        -------
        bool
            Must the propagation of the event to containers be stopped ?
        """
        stop_propagation = False
        for reaction in self._reactions[event.type]:
            stop = reaction(self, event)
            stop_propagation = stop_propagation or stop
        return stop_propagation

    def add_reaction(self, type: int, callback) -> Tuple[int, int]:
        """Add a callback to react to event of a certain type via react

        Parameters
        ----------
        type : int
            Type (pygame.event.EventType) of event the callback will be called for
        callback : (Widget, Event) -> bool
            Function called with the Widget that called react() and the event

        Returns
        -------
        Tuple[int, int]
            Identifiant that can be used to delete the callback later on
        """
        reactions = self._reactions[type]
        reactions.append(callback)
        return (type, len(reactions) - 1)

    def del_reaction(self, idReaction: Tuple[int, int]):
        """Delete a callback

        Parameters
        ----------
        idReaction : Tuple[int, int]
            The identifiant that was returned when the callback was added
        """
        type, index = idReaction
        del self._reactions[type][index]

    @abstractmethod
    def redraw(self):
        """Redraw the image attribute to reflect the state of the Widget, normally implemented by a subclass and shouldn't have to be manually called

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError(
            "A Widget subclass must implements the redraw() method"
        )


class Container(Widget, ABC):
    """Abstract class for a Widget that can contain other widgets

    Methods
    -------
    set_grid(col : int, line : int, w : Widget)
        Put a Widget on the given position, extending the grid if necessary
    get_grid(col : int, line : int) -> Widget
        Get the Widget in a certain position of the grid
    del_widget(col : int, line : int)
        Destroy (call kill()) the Widget in the given position

    Attributes
    ----------
    columns : int
        Number of columns in the grid
    lines : int
        Number of lines in the grid
    """

    def __init__(self) -> None:
        super().__init__()
        self._grid = [[None]]
        self._xdims = [0]
        self._ydims = [0]
        self._cells = [[Rect(0, 0, 0, 0)]]
        self._columns = 1
        self._lines = 1
        self._grid_rect = Rect(0, 0, 0, 0)

    def _compute_cells(self):
        """compute a matrix of rectangles corresponding to the grid and its dimensions"""
        cells = [[None for x in range(self.columns)] for y in range(self.lines)]
        y_offset = 0
        for y in range(self.lines):
            x_offset = 0
            for x in range(self.columns):
                cells[y][x] = Rect(x_offset, y_offset, self._xdims[x], self._ydims[y])
                x_offset += self._xdims[x]
            y_offset += self._ydims[y]
        return cells

    def _refresh_dims(self):
        """Refresh the _xdims, _ydims and _grid_rect attributes"""
        for i in range(self._lines):
            for j in range(self._columns):
                w = self._grid[i][j]
                if isinstance(w, Sprite):
                    self._xdims[j] = max(self._xdims[j], w.rect.width)
                    self._ydims[j] = max(self._ydims[j], w.rect.height)
        self._grid_rect.width = sum(self._xdims)
        self._grid_rect.height = sum(self._ydims)
        self._cells = self._compute_cells()

    def set_grid(self, col: int, line: int, w: Widget):
        """Put a Widget on the given position, extending the grid if necessary

        Parameters
        ----------
        col : int
            column where the Widget is placed
        line : int
            line where the widget is placed
        w : Widget
            Widget to place
        """
        if col > self._columns:
            self.columns = col
        if line > self._lines:
            self.lines = line
        self._grid[line][col] = w
        w.container = self

        self._refresh_dims()

    def get_grid(self, col: int, line: int) -> Widget:
        """Get the Widget in a certain position of the grid

        Parameters
        ----------
        col : int
            column
        line : int
            line

        Returns
        -------
        Widget
            The Widget at the position col and line
        """
        if col > self._columns or line > self._lines:
            return
        else:
            return self._grid[line][col]

    def del_widget(self, col: int, line: int):
        """Destroy (call kill()) the Widget in the given position

        Parameters
        ----------
        col : int
        line : int
        """
        if col > self._columns or line > self._lines:
            return
        else:
            w = self._grid[line][col]
            if isinstance(w, Sprite):
                w.kill()
            self._grid[line][col] = None

        self._refresh_dims()

    def kill(self) -> None:
        super().kill()
        for y in range(self._lines):
            for x in range(self._columns):
                w = self._grid[y][x]
                if isinstance(w, Sprite):
                    w.kill()

    def react(self, event: Event):
        stop_propagation = False
        for y in range(self._lines):
            for x in range(self._columns):
                w = self._grid[y][x]
                if isinstance(w, Widget):
                    stop = w.react(event)
                    stop_propagation = stop_propagation or stop
        if not stop_propagation:
            super().react(event)

    def _get_lines(self):
        return self._lines

    def _set_lines(self, lines: int):
        if lines < 0:
            raise ValueError("lines must be positive")
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
                self._ydims.append(0)

        self._lines = lines
        self._refresh_dims()

    lines = property(
        _get_lines,
        _set_lines,
        doc="Number of lines, setting it may destroy some lines of Widgets",
    )

    def _get_columns(self):
        return self._columns

    def _set_columns(self, columns: int):
        if columns < 0:
            raise ValueError("columns must be positive")
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
            self._xdims.extend([0] * (columns - self._columns))

        self._columns = columns
        self._refresh_dims()

    columns = property(
        _get_columns,
        _set_columns,
        doc="Number of columns, setting it may destroy some columns of Widgets",
    )

    def update(self, *args, **kwargs) -> None:
        for i in range(self._lines):
            for j in range(self._columns):
                w = self._grid[i][j]
                if isinstance(w, Sprite):
                    w.update()
        self.redraw()


class Button(Widget, ABC):
    """Abstract class for a Widget that can be "clicked" and can be in an "active", "inactive" or "disabled" state

    Special event
    -------------
    Button.CLICKED
        launched if the mouse has a left MOUSEBUTTONUP on this button

    Attributes
    ----------
    state : int
        State of the button, one of (Button.ACTIVE, Button.INACTIVE, Button.DISABLED)
    """

    CLICKED = custom_type()
    INACTIVE = 0
    ACTIVE = 1
    DISABLED = 2

    def _mouse_down(self, source, e):
        if self.rect.collidepoint(e.pos):
            self.state = Button.ACTIVE

    def _mouse_up(self, source, e):
        if self.rect.collidepoint(e.pos):
            self.state = Button.INACTIVE
            post(Event(Button.CLICKED, {"button": self}))

    def __init__(self) -> None:
        super().__init__()
        self._state = Button.INACTIVE
        self._reactions[MOUSEBUTTONDOWN].append(self._mouse_down)
        self._reactions[MOUSEBUTTONUP].append(self._mouse_up)

    def react(self, e: Event):
        if self.state != Button.DISABLED:
            return super().react(e)

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        self._state = state
        self.redraw()

    state = property(
        _get_state,
        _set_state,
        doc="State of the Button : INACTIVE (normal), ACTIVE (pressed), DISABLED (unresponsive)",
    )
