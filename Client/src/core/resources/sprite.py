from src.core.resources.texture import *
from pygame import Surface
from enum import Enum
from src.core.util.vector import Vec2

class Origin(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    CENTER = 5


class Sprite:
    def __init__(self, texture : Texture,
                 origin : Origin = Origin.CENTER,
                 position: Vec2 = Vec2(0, 0)) -> None:
        self.texture : Texture = texture
        self.origin : Origin = origin
        self.position : Vec2 = position
        self.rotation : float = 0.0
        self.rect = None
        self.set_origin(origin)

    def draw(self, window: Surface) -> None:
        window.blit(self.texture.image,self.rect)

    def set_size(self, x: int, y: int) -> None:
        pass
        self.texture.image = pygame.transform.scale(self.texture.image,(x,y))
        self.set_origin(self.origin)

    def set_origin(self, origin: Origin) -> None:
        match origin:
            case Origin.CENTER:
                self.rect = self.texture.image.get_rect(center=[self.position.x, self.position.y])
            case Origin.TOP_LEFT:
                self.rect = self.texture.image.get_rect(topleft=[self.position.x, self.position.y])
            case Origin.TOP_RIGHT:
                self.rect = self.texture.image.get_rect(topright=[self.position.x, self.position.y])
            case Origin.BOTTOM_LEFT:
                self.rect = self.texture.image.get_rect(bottomleft=[self.position.x, self.position.y])
            case Origin.BOTTOM_RIGHT:
                self.rect = self.texture.image.get_rect(bottomright=[self.position.x, self.position.y])
        self.origin = origin

    def set_position(self,x: int, y: int) -> None:
        temp_origin = self.origin
        self.set_origin(Origin.TOP_LEFT)
        self.position.x = self.rect.left = x
        self.position.y = self.rect.top = y
        self.set_origin(temp_origin)

    def set_transparency(self, val: int):
        self.texture.image.set_alpha(val)

    def set_rotation(self, degree: float):
        self.rotation = degree
        self.texture.image = pygame.transform.rotate(self.texture.image,self.rotation)

    def rotate(self, degree: float):
        self.rotation += degree
        self.texture.image = pygame.transform.rotate(self.texture.image, self.rotation)

    def move(self, vec : Vec2) -> None:
        self.position.x += vec.x
        self.position.y += vec.y
        self.rect.left = self.position.x
        self.rect.top = self.position.y
