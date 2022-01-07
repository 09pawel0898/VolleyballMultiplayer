from src.core.widgets.widget import Widget
from src.core.util.vector import Vec2
from src.core.util.utilis import lerp
from src.core.resources.texture import Texture
from typing import Callable
from enum import Enum
import pygame

class ButtonBehaviour(Enum):
    NoBehaviour =1
    SlideRight = 2
    Rotate = 3


class Button(Widget):
    def __init__(self, pos: Vec2, texture: Texture, behaviour: ButtonBehaviour = ButtonBehaviour.NoBehaviour) -> None:
        super().__init__(pos)
        pygame.sprite.Sprite.__init__(self)
        self.image = texture.image
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]
        self._callback : Callable = None
        self._initial_pos = Vec2(pos.x,pos.y)
        self.bCovered = False
        self._behaviour = behaviour

    def _cursor_in_bounds(self, mouse_pos):
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom:
            return True
        else:
            return False

    def check_for_onclick(self):
        if self.bCovered:
            if self._callback is not None:
                self._callback()

    def set_callback(self, func: Callable):
        self._callback = func

    def set_initial_pos(self, pos : Vec2):
        if self._initial_pos.x == 300:
            raise ValueError
        self._initial_pos = pos

    def get_initial_pos(self):
        return self._initial_pos

    def update(self,dt):
        mouse_pos = pygame.mouse.get_pos()
        if self._behaviour == ButtonBehaviour.NoBehaviour:
            pass
        elif self._behaviour == ButtonBehaviour.SlideRight:
            if self._cursor_in_bounds(mouse_pos):
                self.bCovered = True
                self.set_position(lerp(self.pos.x,self._initial_pos.x + 7,0.155),self.pos.y)
            else:
                self.bCovered = False
                self.set_position(lerp(self.pos.x, self._initial_pos.x, 0.155), self.pos.y)
        elif self._behaviour == ButtonBehaviour.Rotate:
            pass

    def render(self):
        pass

    def set_position(self,x: int, y: int) -> None:
        self.pos.x = self.rect.left = x
        self.pos.y = self.rect.top = y

    def move(self, vec : Vec2) -> None:
        self.pos.x += vec.x
        self.pos.y += vec.y
        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

