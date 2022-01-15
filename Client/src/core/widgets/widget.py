from abc import abstractmethod, ABC
from src.core.util.vector import Vec2
from pygame import Surface
import pygame.sprite

class Widget(ABC,pygame.sprite.Sprite):
    def __init__(self, pos: Vec2):
        super().__init__()
        self.pos : Vec2 = pos

    @abstractmethod
    def draw(self, window: Surface):
        pass

    @abstractmethod
    def update(self,dt):
        pass