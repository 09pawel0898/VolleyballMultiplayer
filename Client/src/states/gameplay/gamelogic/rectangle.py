from enum import Enum

import pygame


class Orientation(Enum):
    Vertical = 1
    Horizontal = 2

class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float, orientation : Orientation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation

    def in_bounds(self, x: float, y: float) -> bool:
        if self.x < x < self.x+self.width and self.y < y <self.y+self.height:
            return True
        else:
            return False

    def draw(self, window : pygame.Surface):
        pygame.draw.rect(window,(255,0,0), pygame.Rect(self.x,self.y,self.width,self.height))
