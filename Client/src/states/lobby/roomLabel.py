import pygame

from src.core.widgets.button import Button,ButtonBehaviour
from src.core.util.vector import Vec2
from src.core.resources.texture import Texture
from src.core.widgets.label import Label

class RoomLabel(Button):
    def __init__(self, texture: Texture, host: str, people: int, full: bool) -> None:
        super().__init__(Vec2(-1000,-1000), texture, ButtonBehaviour.NoBehaviour)
        self.host = host
        self.people = people
        self.full = full
        self._init_labels()

    def set_position(self,x: float, y: float) -> None:
        super().set_position(x,y)
        self.host_label.set_position(x + self.host_label_offset.x,y + self.host_label_offset.y)
        self.people_label.set_position(x + self.people_label_offset.x,y + self.people_label_offset.y)
        self.pos = Vec2(x,y)
        #set text label pos

    def _init_labels(self) -> None:
        self.host_label_offset = Vec2(140,6)
        self.people_label_offset = Vec2(330,6)

        self.host_label = Label(Vec2(0,0), self.host, 27)
        if self.full:
            self.people_label = Label(Vec2(0,0), "1/1", 27)
        else:
            self.people_label = Label(Vec2(0,0), "0/1", 27)

    def set_active(self, active: bool):
        if active:
            self.image.set_alpha(255)
            self.host_label.image.set_alpha(255)
            self.people_label.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
            self.host_label.image.set_alpha(140)
            self.people_label.image.set_alpha(140)

    def draw(self, window : pygame.Surface) -> None:
        super().draw(window)
        window.blit(self.host_label.image,self.host_label.rect)
        window.blit(self.people_label.image,self.people_label.rect)
