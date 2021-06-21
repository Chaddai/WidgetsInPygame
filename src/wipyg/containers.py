from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface, color
from pygame.draw import *


class Frame(Container):
    """A gridded Container without frills

    Attributes
    ----------
    bg_color : color (pygame.color compatible)
        The background color of the Frame
    """

    def __init__(
        self, widgets: list[list[Widget]] = [[None]], bg_color=(255, 255, 255, 0)
    ) -> None:
        """Create a gridded container that simply display all its children in the minimum space, each centered in its cell

        Parameters
        ----------
        widgets : list[list[Widget]], optional
            An initial grid of widgets, by default [[None]], don't give it an empty list
        bg_color : color (pygame.color compatible)
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
                if isinstance(w, Widget):
                    w.container = self

        self._refresh_dims()
        self.rect = self._grid_rect.copy()
        self.redraw()

    def redraw(self):
        bg_color = self._bg_color

        self.rect.size = self._grid_rect.size

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill(bg_color)

        for y in range(self.lines):
            for x in range(self.columns):
                w = self._grid[y][x]
                if isinstance(w, Sprite):
                    r = w.rect
                    i = w.image
                    r.center = self._cells[y][x].center
                    self.image.blit(i, r)

    def _get_bg_color(self):
        return self._bg_color

    def _set_bg_color(self, bg_color):
        self._bg_color = bg_color
        self.redraw()

    bg_color = property(
        _get_bg_color, _set_bg_color, doc="The background color of the Frame"
    )
