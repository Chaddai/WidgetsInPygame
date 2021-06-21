# -*- coding: utf-8 -*-
"""Show an example of a Window (decorated container) in action (move, close, minimize)

Since the content of the Window is a Frame it also demonstrate the recursivity of Container"""

import pygame
from pygame.constants import *
from wipyg import buttons, label, containers
from wipyg.abstracts import Button

# CALLBACK
def quit(s, e):
    global looping
    if e.button == s:
        looping = False


# INITIALIZATION

pygame.init()

screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()
pygame.display.set_caption("Demo of wipyg Widgets")

but_quit = buttons.CancelButton(text="Quitter")
but_quit.add_reaction(Button.CLICKED, quit)

# We build a frame
frame = containers.Frame(
    widgets=[[label.Label("Hello World!")], [but_quit]], bg_color=(110, 110, 110)
)

# And we put it inside a Window
window = containers.Window(frame, bar_color=(255, 0, 0, 100))
window.rect.center = screen_rect.center

widgets = pygame.sprite.RenderPlain(window)

looping = True

# MAIN LOOP

while looping:
    for e in pygame.event.get():
        for w in widgets:
            w.react(e)
        if e.type == QUIT:
            looping = False

    widgets.update()
    screen.fill((50, 50, 200))
    widgets.draw(screen)

    pygame.display.flip()

pygame.quit()
