from src.core.resources.sprite import *
from .rectangle import *
from typing import List

class Ball(Sprite):
    def __init__(self,
                 texture: Texture,
                 origin: Origin = Origin.CENTER,
                 position: Vec2 = Vec2(0.0, 0.0)) -> None:
        super().__init__(texture, origin, position)
        self.speed = 0.05
        self.mod = 0.05
        self.rotation = 0.0
        self.D =0.0
        self.radius = 0
        #self.bIsRisingUp = False

    def update(self, dt: float, colliders: List[Rectangle]) -> None:
        self.radius = self.texture.image.get_rect().height/2

        if self.D == 0:
            self.rotation /= 1.01
        if self.speed < 0:
            if -0.5 < self.D < 0.5:
                self.speed /= 1.02
                self.move(Vec2(0,self.speed))
                self.speed+=self.mod
            else:
                self.speed /= 1.02
                self.move(Vec2(self.D, self.speed))
                self.speed += self.mod
        else:
            self.speed *=1.002
            if -0.5 < self.D < 0.5:
                self.move(Vec2(0,self.speed))
                self.speed+=self.mod
            else:
                self.move(Vec2(self.D, self.speed))
                self.speed += self.mod

        for collider in colliders:
            self._check_collision(collider)
        self.rotation /= 1.0005
        self.rotate(self.D)

    def _check_collision(self, rect: Rectangle):
        if rect.orientation == Orientation.Horizontal:
            if rect.in_bounds(self.position.x,self.position.y+self.radius):
                self.speed *= -1
            #if self.position.y + self.radius >= rect.y:
            #    self.speed *= -1
        elif rect.orientation == Orientation.Vertical:
            pass