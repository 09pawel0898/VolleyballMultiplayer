from abc import abstractmethod, ABC
from src.core.util.vector import Vec2
import pygame.sprite

class Widget(ABC,pygame.sprite.Sprite):
    def __init__(self, pos: Vec2):
        self.pos : Vec2 = pos

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def update(self,dt):
        pass