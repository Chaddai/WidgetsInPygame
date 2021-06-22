# -*- coding: utf-8 -*-
"""Simple game integrating widgets

Start with a `Window` with some settings

In the game, `Frames` with simple computations (`Label`) and text `Entry`
fall from the top of the screen, and you must select and answer them 
before they reach the ground. You have three lives and once they're
used up you get to the highscore hall where you can enter your name

You can press Esc to pause the game and change settings"""


import random
from pathlib import Path

import pygame
from pygame.event import Event
from pygame.locals import *
from pygame.sprite import RenderPlain
from pygame.time import Clock, get_ticks
from pygame.colordict import THECOLORS

from wipyg import *
from wipyg.abstracts import Button

# check if highscore file exists, create it otherwise
highscore_path = Path("highscore.txt")
if not highscore_path.exists():
    highscore_path.write_text("")


def gen_random_computation():
    operator = random.choice(["+", "*", "-"])
    a, b = random.randint(1, 12), random.randint(1, 12)
    if operator == "+":
        return f"{a} {operator} {b}", a + b
    if operator == "*":
        return f"{a} {operator} {b}", a * b
    if operator == "-":
        return f"{a} {operator} {b}", a - b


class Offensive(Frame):
    """Computation attack : Frame of a computation label and a response entry"""

    def __init__(self, stage) -> None:
        self.stage = stage
        question, self.answer = gen_random_computation()
        computation_label = Label(question)
        self.computation_entry = Entry(length=5)
        self.computation_entry.add_reaction(Entry.SUBMIT, self.check_answer)
        super().__init__(widgets=[[computation_label], [self.computation_entry]])
        self.rect.top = 0
        self.rect.left = random.randint(0, screen_rect.width - self.rect.width)
        self.redraw()

    def update(self) -> None:
        super().update()
        self.rect.move_ip(0, self.stage.game_speed * self.stage.delta // 100)
        if self.rect.bottom > screen_rect.bottom:
            self.stage.lives -= 1
            self.stage.offensive -= 1
            self.kill()
        self.redraw()

    def check_answer(self, reacting, e):
        if e.entry == self.computation_entry:
            try:
                answer = int(e.value)
                if answer == self.answer:
                    self.kill()
                    self.stage.offensive -= 1
                    self.stage.score += self.stage.game_speed
            except:
                self.computation_entry.value = ""


class Stage:
    def __init__(self) -> None:
        self.bg_color = (255, 255, 255)
        self.groups = []
        self.looping = True
        self.next_stage = None
        self.clock = Clock()
        self.widgets = RenderPlain()

    def loop(self):
        if self.next_stage is not None:
            self.next_stage.looping = True
        self.clock.tick()
        while self.looping:
            self.delta = self.clock.tick(30)  # 30 fps
            for e in pygame.event.get():
                for w in self.widgets:
                    w.react(e)
                self.react(e)
                if e.type == QUIT:
                    self.looping = False
                    self.next_stage = None

            self.global_update()
            self.widgets.update()
            for g in self.groups:
                g.update()

            screen.fill(self.bg_color)

            for g in self.groups:
                g.draw(screen)
            self.widgets.draw(screen)

            pygame.display.flip()

    def global_update(self):
        return

    def react(self, e):
        pass


# MAIN MENU
class MainMenu(Stage):
    def __init__(self, next_stage, first=False, game_speed=10, color="red") -> None:
        super().__init__()

        self.game_speed_entry = Entry(str(game_speed), length=2)
        self.color_entry = Entry(color, length=6)
        self.starting_lives_entry = Entry("3", length=2)
        but_quit = CancelButton("Quit")
        but_quit.add_reaction(Button.CLICKED, self.quit)
        but_play = SubmitButton("Play")
        but_play.add_reaction(Button.CLICKED, self.play)
        third_line = (
            [Label("Starting Lives"), self.starting_lives_entry]
            if first
            else [None, None]
        )
        frame = Frame(
            [
                [Label("Game speed (between 1 and 99)"), self.game_speed_entry],
                [Label("Background color"), self.color_entry],
                third_line,
                [but_quit, but_play],
            ],
            bg_color=(110, 110, 110),
        )
        window = Window(frame, bar_color=(255, 0, 0, 100))
        window.rect.center = screen_rect.center

        self.widgets.add(window)

        self._first = first
        self.next_stage = next_stage

    def quit(self, s, e):
        if e.button == s:
            self.looping = False
            self.next_stage = None

    def play(self, s, e):
        if e.button == s:
            self.looping = False
            try:
                self.next_stage.game_speed = int(self.game_speed_entry.value)
            except:
                pass
            if self.color_entry.value in THECOLORS:
                self.next_stage.bg_color = self.color_entry.value
            if self._first:
                try:
                    self.next_stage.lives = int(self.starting_lives_entry.value)
                except:
                    pass


# GAME
class Game(Stage):
    def __init__(self) -> None:
        super().__init__()
        self.offensive = 0
        self.last_offensive = get_ticks()
        self.score = 0

    def global_update(self):
        if self.lives <= 0:
            self.looping = False
            self.next_stage = HighScore(self.score)
        now = get_ticks()
        if self.offensive < 3 and now - self.last_offensive > 2000:
            self.last_offensive = now
            self.offensive += 1
            self.widgets.add(Offensive(self))

    def react(self, e: Event):
        # pause the game
        if e.type == KEYUP and e.key == K_ESCAPE:
            self.looping = False
            self.next_stage = MainMenu(
                self, game_speed=self.game_speed, color=self.bg_color
            )


# HIGHSCORE
class HighScore(Stage):
    def __init__(self, score: int) -> None:
        super().__init__()
        self.score = score

        self.highscores = []
        try:
            for line in highscore_path.read_text(encoding="utf-8").splitlines():
                score_str, name = line.split(";")
                self.highscores.append((int(score_str), name))
        except:
            pass
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:10]

        grid = []
        for score, name in self.highscores:
            grid.append([Label(str(score)), Label(name)])

        but_quit = CancelButton("Quit")
        but_quit.add_reaction(Button.CLICKED, self.quit)
        grid.append([None, but_quit])

        i = 0
        while i < len(self.highscores) and self.highscores[i][0] > self.score:
            i += 1
        if i < 10:
            self.i = i
            self.name_entry = Entry("AAAAAAAA", state=Entry.SELECTED, length=8)
            self.name_entry.add_reaction(Entry.SUBMIT, self.register)

            grid.insert(i, [Label(str(self.score), color="red"), self.name_entry])

        self.frame = Frame(grid)
        self.frame.rect.center = screen_rect.center
        self.widgets.add(self.frame)

    def quit(self, s, e):
        if e.button == s:
            self.looping = False
            self.next_stage = None

    def register(self, s, e):
        self.name = e.value.replace(";", "")
        self.highscores.insert(self.i, [self.score, self.name])
        self.highscores = self.highscores[:10]
        try:
            with highscore_path.open("w", encoding="utf-8") as file:
                for score, name in self.highscores:
                    file.write(f"{score};{name}\n")
        except:
            pass
        self.frame.del_cell(2, self.i + 1)
        self.frame.set_grid(2, self.i + 1, Label(self.name, color="red"))
        self.frame.rect.center = screen_rect.center


# INITIALIZATION
pygame.init()
screen = pygame.display.set_mode((1024, 800))
screen_rect = screen.get_rect()
pygame.display.set_caption("Compute them all")

stage = MainMenu(Game(), first=True)
while stage is not None:
    stage.loop()
    stage = stage.next_stage

pygame.quit()
