from src.core.resources.sprite import *

class Pawn(Sprite):
    def __init__(self, left_side: int,
                 texture : Texture,
                 origin : Origin = Origin.CENTER,
                 position: Vec2 = Vec2(0.0, 0.0)):
        super().__init__(texture,origin,position)
        self.bLeftSide = True if left_side == 0 else False
        self._init_at_position()

    def _init_at_position(self):
        if self.bLeftSide:
            self.set_position(100,300)
        else:
            self.set_position(400, 300)

    def draw(self, window: Surface):
        if self.bLeftSide:
            window.blit(self.texture.image, self.rect)
        else:
            window.blit(pygame.transform.flip(self.texture.image, True, False), self.rect)