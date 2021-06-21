import pygame
from pygame.constants import *
from wipyg import buttons, label
from wipyg import entry
from wipyg.abstracts import Button

pygame.init()

screen = pygame.display.set_mode((320, 240))
screen_rect = screen.get_rect()
pygame.display.set_caption("Demo of wipyg Widgets")

but_quit = buttons.PlainButton(text="Quitter")


def quit(s, e):
    global looping
    if e.button == s:
        looping = False


but_quit.add_reaction(Button.CLICKED, quit)
but_quit.rect.bottomright = screen_rect.bottomright


but_print = buttons.PlainButton(text="Hello")


def hello(s, e):
    if e.button == s:
        print("hello world !")


but_print.add_reaction(Button.CLICKED, hello)

but_disabled = buttons.PlainButton()
but_disabled.state = Button.DISABLED
but_disabled.rect.bottomleft = screen_rect.bottomleft

lab = label.Label(text="Bonjour tout le monde")
lab.rect.center = screen_rect.center

ent = entry.Entry(value="Et ", length=10, state=entry.Entry.SELECTED)
ent.rect.topright = screen_rect.topright

widgets = pygame.sprite.RenderPlain(but_quit, but_print, but_disabled, lab, ent)

looping = True
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
