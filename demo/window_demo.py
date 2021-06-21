import pygame
from pygame.constants import *
from wipyg import buttons, label, containers
from wipyg.abstracts import Button

pygame.init()

screen = pygame.display.set_mode((640, 480))
screen_rect = screen.get_rect()
pygame.display.set_caption("Demo of wipyg Widgets")

but_quit = buttons.CancelButton(text="Quitter")


def quit(s, e):
    global looping
    if e.button == s:
        looping = False


but_quit.add_reaction(Button.CLICKED, quit)

frame = containers.Frame(
    widgets=[[label.Label("Hello World!")], [but_quit]], bg_color=(110, 110, 110)
)

window = containers.Window(frame, bar_color=(255, 0, 0, 100))
window.rect.center = screen_rect.center

widgets = pygame.sprite.RenderPlain(window)

looping = True
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
