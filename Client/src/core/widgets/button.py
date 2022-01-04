from src.core.widgets.widget import Widget
from src.core.util.vector import Vec2
from src.core.util.utilis import lerp
from src.core.resources.texture import Texture
from typing import Callable
import pygame

class Button(Widget):
    def __init__(self, pos: Vec2, texture: Texture) -> None:
        super().__init__(pos)
        pygame.sprite.Sprite.__init__(self)
        self.image = texture.image
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]
        self._callback : Callable = None
        self._initial_pos = pos
        self.covered = False

    def _cursor_in_bounds(self, mouse_pos):
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom:
            return True
        else:
            return False

    def check_for_onclick(self, mouse_pos):
        if self.covered:
            if self._callback is not None:
                self._callback()

    def set_callback(self, func: Callable):
        self._callback = func

    def set_initial_pos(self, pos : Vec2):
        self._initial_pos = pos

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self._cursor_in_bounds(mouse_pos):
            self.covered = True
            self.set_position(lerp(self.pos.x,self._initial_pos.x + 7,0.155),self.pos.y)
        else:
            self.covered = False
            self.set_position(lerp(self.pos.x, self._initial_pos.x, 0.155), self.pos.y)

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

