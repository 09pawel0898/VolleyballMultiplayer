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
        #set text label pos

    def _init_labels(self) -> None:
        self.host_label = Label(Vec2(self.pos.x + 20, self.pos.y + 20), self.host, 33)
        if self.full:
            self.people_label = Label(Vec2(self.pos.x + 30, self.pos.y + 30), "1/1", 33)
            #init aproppriate texture
        else:
            self.people_label = Label(Vec2(self.pos.x + 30, self.pos.y + 30), "0/1", 33)
            # init apropriate texture

    def draw(self, window : pygame.Surface) -> None:
        super().draw(window)
