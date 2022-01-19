from src.core.resources.sprite import *
from typing import List
from src.networking.serverRoom.packages import *
from src.threads.websocketthread import WebsocketThread
from src.core.util.utilis import *
from enum import Enum

#side: 0 - left, 1 - right

class PawnState(Enum):
    Walk = 0
    Falling = 1
    Raising = 2

class Pawn(Sprite):
    def __init__(self, side: int,
                 texture : Texture,
                 x: float,
                 y: float,
                 origin : Origin = Origin.CENTER):
        super().__init__(texture,origin,Vec2(x,y))
        self.bLeftSide = True if side == 0 else False
        self.state = PawnState.Walk
        self.speed = Vec2(0,0)
        self.vert_input = 0.0
        self._init_at_position()

    def _init_at_position(self):
        if self.bLeftSide:
            print("Left")
            self.set_position(100,300)
        else:
            print("Right")
            self.set_position(700, 300)

    def update(self, dt: float):
        self.speed = Vec2(lerp(self.speed.x, self.vert_input, dt*0.01),self.speed.y)
        self.set_position(self.position.x+self.speed.x,
                          self.position.y+self.speed.y)



    def _jump(self):
        pass

    def handle_events(self, events: List[pygame.event.Event]):
        key = pygame.key.get_pressed()
        moved = False
        if key[pygame.K_w]:
            self._jump()
            moved = True
        elif key[pygame.K_a]:
            self.vert_input = -2
        elif key[pygame.K_d]:
            self.vert_input = 2
        else:
            self.vert_input = 0
        #if moved:
            #WebsocketThread.send(PackageSend(header=CodeSend.BallMoved,
            #                                 body=f"{self.ball.position.x},"
            #                                      f"{self.ball.position.y}"))

    def draw(self, window: Surface):
        if self.bLeftSide:
            window.blit(self.texture.image, self.rect)
        else:
            window.blit(pygame.transform.flip(self.texture.image, True, False), self.rect)