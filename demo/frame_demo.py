# -*- coding: utf-8 -*-
"""Show an example of a Frame (grid container) in action"""

import pygame
from pygame.locals import *
from wipyg import buttons, label, entry, containers
from wipyg.abstracts import Button

# CALLBACKS


def quit(s, e):
    global looping
    if e.button == s:
        looping = False


def close(s, e):
    if e.button == s:
        s.container.kill()
    return True  # stop event from propagating upward


# INITIALIZATION

pygame.init()

screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()
pygame.display.set_caption("Demo of wipyg Frame")

but_quit = buttons.CancelButton(text="Quitter")
but_quit.add_reaction(Button.CLICKED, quit)


but_close = buttons.CancelButton(text="Close")
but_close.add_reaction(Button.CLICKED, close)

lab = label.Label(text="Bonjour tout le monde")

ent = entry.Entry(value="Et ", length=10, state=entry.Entry.SELECTED)

frame = containers.Frame(
    widgets=[[lab, but_close], [ent, but_quit]], bg_color=(110, 110, 110)
)
frame.rect.center = screen_rect.center

widgets = pygame.sprite.RenderPlain(frame)

looping = True

# MAIN LOOP

while looping:
    for e in pygame.event.get():
        for w in widgets:
            w.react(e)
        if e.type == QUIT:
            looping = False

    widgets.update()
    screen.fill((150, 0, 0))
    widgets.draw(screen)

    pygame.display.flip()

pygame.quit()
