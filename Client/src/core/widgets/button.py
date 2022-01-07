from src.core.widgets.widget import Widget
from src.core.util.vector import Vec2
from src.core.util.utilis import lerp
from src.core.resources.texture import Texture
from ..resources.sprite import Origin

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
        self._initial_size = Vec2(self.rect.width,self.rect.height)
        self._behaviour = behaviour
        #self.origin = Origin.CENTER
        #self.notScaledImage = self.image.copy()
        #self.scaledImage = self.set_scale(1.1)
        self.bCovered = False
        #self.rect.left -=1000.0

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
        self._initial_pos = pos

    def get_initial_pos(self):
        return self._initial_pos

    def update(self,dt):
        mouse_pos = pygame.mouse.get_pos()

        if self._cursor_in_bounds(mouse_pos):
            if self._behaviour == ButtonBehaviour.NoBehaviour:
                pass
            elif self._behaviour == ButtonBehaviour.SlideRight:
                self.set_position(lerp(self.pos.x, self._initial_pos.x + 3, dt*0.015), self.pos.y)
            self.bCovered = True
        else:
            if self._behaviour == ButtonBehaviour.NoBehaviour:
                pass
            elif self._behaviour == ButtonBehaviour.SlideRight:
                self.set_position(lerp(self.pos.x, self._initial_pos.x, dt*0.015), self.pos.y)
            self.bCovered = False

    def render(self):
        pass

    #def _set_scaled_or_not(self, scaled: bool):
    #    if scaled:
    #        self.image = self.scaledImage
    #    else:
    #        self.image = self.notScaledImage

    def set_scale(self, new_scale: float):
        return pygame.transform.scale(self.image,
                                      (self._initial_size.x*new_scale,self._initial_size.y*new_scale))

    def set_position(self,x: int, y: int) -> None:
        self.pos.x = self.rect.left = x
        self.pos.y = self.rect.top = y

    def move(self, vec : Vec2) -> None:
        self.pos.x += vec.x
        self.pos.y += vec.y
        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

    def set_origin(self, origin: Origin) -> None:
        match origin:
            case Origin.CENTER:
                self.rect = self.image.get_rect(center=[self.pos.x, self.pos.y])
            case Origin.TOP_LEFT:
                self.rect = self.image.get_rect(topleft=[self.pos.x, self.pos.y])
            case Origin.TOP_RIGHT:
                self.rect = self.image.get_rect(topright=[self.pos.x, self.pos.y])
            case Origin.BOTTOM_LEFT:
                self.rect = self.image.get_rect(bottomleft=[self.pos.x, self.pos.y])
            case Origin.BOTTOM_RIGHT:
                self.rect = self.image.get_rect(bottomright=[self.pos.x, self.pos.y])
        self.origin = origin

