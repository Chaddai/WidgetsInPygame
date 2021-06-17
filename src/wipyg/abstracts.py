from abc import ABC, abstractmethod
from pygame.sprite import *


class Widget(ABC, Sprite):
    """Abstract class for widgets :
    Methods :
    - update()
    - display(rect : Rect)
    - react(e : event.EventType)
    Properties :
    - rect : Rect
    - image : Surface
    """
