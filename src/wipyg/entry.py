from os import close, stat
from wipyg.abstracts import *
from pygame.font import Font
from pygame import Surface
from pygame.draw import *
from pygame.time import get_ticks
import unicodedata


class Entry(Widget):
    """A text entry widget

    Additional properties:
    - value : str
    - cursor : int
    - state : int (Entry.SELECTED, Entry.DESELECTED, Entry.DISABLED)
    """

    SELECTED = 0
    DESELECTED = 1
    DISABLED = 2

    def __init__(
        self,
        value: str = "",
        font=None,
        size: int = 30,
        length: int = 40,
        state: int = 1,
    ) -> None:
        super().__init__()
        self._length = length
        self._font = Font(font, size)
        self._value = list(value)
        self._cursor = len(value)
        self._state = state
        self._first_blink = get_ticks()
        self.rect = Rect(0, 0, 0, 0)
        self.redraw()

        self.add_reaction(KEYDOWN, self._press_key)
        self.add_reaction(MOUSEBUTTONUP, self._select)

    def redraw(self):
        if self._state == Entry.DISABLED:
            bg_color = (200, 200, 200)
            text_color = (100, 100, 100)
        else:
            bg_color = (255, 255, 255)
            text_color = (0, 0, 0)

        pos = self.rect.topleft

        xsize, ysize = self._font.size("M" * self._length)
        padding = self._font.get_height()
        self.rect = Rect(0, 0, xsize + 2 * padding, ysize + 2 * padding)

        value_img = self._font.render(self.value, True, text_color)
        value_rect = value_img.get_rect(centery=self.rect.centery, left=padding)

        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        border = self.rect.inflate(-2, -2)
        border.center = self.rect.center
        rect(self.image, bg_color, border, border_radius=4)
        rect(self.image, (0, 0, 0), border, width=1, border_radius=4)

        if self._state == Entry.SELECTED:
            now = get_ticks()
            if ((now - self._first_blink) // 500) % 2:
                xcursor = padding + self._font.size(self.value[: self._cursor])[0]
                cursor_rect = Rect(xcursor, padding, 2, padding)
                rect(self.image, (0, 0, 0), cursor_rect)

        self.image.blit(value_img, value_rect)

        # reposition the rect as initially
        self.rect.topleft = pos

    def update(self, *args, **kwargs) -> None:
        self.redraw()

    def _press_key(self, _, e):
        letter = e.unicode
        if self._state == Entry.SELECTED:
            if e.key == K_LEFT and self._cursor > 0:
                self._cursor -= 1
            elif e.key == K_RIGHT and self._cursor < len(self._value):
                self._cursor += 1
            elif e.key == K_BACKSPACE and self._cursor > 0:
                self._cursor -= 1
                del self._value[self._cursor]
            elif e.key == K_DELETE and self._cursor < len(self._value):
                del self._value[self._cursor]
            elif e.key == K_END:
                self._cursor = len(self._value)
            elif e.key == K_HOME:
                self._cursor = 0
            elif (
                letter != ""
                # don't react to Control characters
                and not unicodedata.category(letter).startswith("C")
                and len(self._value) < self._length
            ):
                self._value.insert(self._cursor, letter)
                self._cursor += 1

    def _select(self, _, e):
        # move the cursor as close as possible to the click (if it is in the Entry)
        if self.rect.collidepoint(e.pos):
            padding = self._font.get_height()
            xletters = [
                self.rect.left + padding + self._font.size(self.value[:j])[0]
                for j in range(len(self._value) + 1)
            ]
            closest = min(
                range(len(self._value) + 1), key=lambda i: abs(e.pos[0] - xletters[i])
            )
            self._cursor = closest

        # toggle SELECTED and DESELECTED state depending on where the user clicked
        if self._state == Entry.DESELECTED and self.rect.collidepoint(e.pos):
            self.state = Entry.SELECTED
        elif self._state == Entry.SELECTED and not self.rect.collidepoint(e.pos):
            self.state = Entry.DESELECTED

    def _get_value(self) -> str:
        return "".join(self._value)

    def _set_value(self, value: str):
        at_end = True if self._cursor == len(self._value) else False
        self._value = list(value)
        if at_end:
            self._cursor = len(self._value)
        else:
            self._cursor = min(self._cursor, len(self._value))

    value = property(_get_value, _set_value, doc="Value of the entry, as a string.")

    def _get_state(self) -> int:
        return self._state

    def _set_state(self, state: int):
        if 0 <= state <= 2:
            self._state = state
        else:
            raise ValueError()

    state = property(
        _get_state,
        _set_state,
        doc="State of the Entry, one of SELECTED, DESELECTED or DISABLED",
    )

    def _get_cursor(self):
        return self._cursor

    def _set_cursor(self, cursor: int):
        if 0 <= cursor <= len(self._value):
            self._cursor = cursor
        else:
            raise ValueError()

    cursor = property(
        _get_cursor,
        _set_cursor,
        doc="Place of the cursor (after self.cursor letters) from 0 to the value length",
    )
