import pygame

from src.core.resources.sprite import *
from typing import List
from src.networking.serverRoom.packages import *
from src.threads.websocketthread import WebsocketThread
from src.core.util.utilis import *
from .rectangle import *

from enum import Enum

#side: 0 - left, 1 - right

class PawnState(Enum):
    Walk = 0
    Falling = 1
    Raising = 2

class CollisionType(Enum):
    Wall = 1
    Floor = 2
    WallAndFloor = 3
    NoCollision = 4

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
        self.modY = 0
        self.vert_input = 0.0
        self.prev_position = (0,0)
        self._init_at_position()

    def _init_at_position(self):
        if self.bLeftSide:
            self.set_position(100,428)
        else:
            self.set_position(980, 428)
        self.set_origin(Origin.TOP_LEFT)
        self.width = self.drawn_rect[2]
        self.height = self.drawn_rect[3]
        self.set_origin(Origin.CENTER)

    def update(self, dt: float, colliders: List[Rectangle]):
        self.speed = Vec2(lerp(self.speed.x, self.vert_input, dt*0.03),
                          lerp(self.speed.y, self.modY, dt*0.03))
        #print(self.modY)
        if self.state == PawnState.Falling:
            if self.modY < 0.55:
                self.modY = 0
                self.state = PawnState.Walk
            else:
                self.state = PawnState.Falling
                self.modY *= 1.06

        elif self.state == PawnState.Raising:
            if self.modY > -0.515:
                self.modY = 0.6
                self.state = PawnState.Falling
            else:
                self.state = PawnState.Raising
                self.modY /= 1.06


        next_position = (self.position.x + self.speed.x,
                         self.position.y + self.speed.y)

        prev_collision = found_collision = CollisionType.NoCollision

        for collider in colliders:
            collision = self._check_collision(collider, next_position)
            if collision != CollisionType.NoCollision:
                found_collision = collision
                if prev_collision != CollisionType.NoCollision:
                    found_collision = CollisionType.WallAndFloor
                    break
                elif prev_collision == CollisionType.NoCollision:
                    prev_collision = collision


        if found_collision == CollisionType.NoCollision:
            self.set_position(self.position.x + self.speed.x,
                              self.position.y + self.speed.y)
        elif found_collision == CollisionType.Floor:
            self.set_position(self.position.x + self.speed.x,
                              self.position.y)
        elif found_collision == CollisionType.Wall:
            self.set_position(self.position.x,
                              self.position.y + self.speed.y)

        if self.prev_position[0] != self.position.x or self.position.y != self.prev_position[1]:
            WebsocketThread.send(PackageSend(header=CodeSend.PlayerMoved,
                                             body=f"{self.position.x},{self.position.y}"))
        self.prev_position = (self.position.x, self.position.y)


    def _check_collision(self, rect: Rectangle, pos_to_check) -> CollisionType:
        rect_points = []
        rect_points.append((pos_to_check[0]-self.width/2,pos_to_check[1]-self.height/2))
        rect_points.append((pos_to_check[0]-self.width/2,pos_to_check[1]+self.height/2))
        rect_points.append((pos_to_check[0]+self.width/2,pos_to_check[1]+self.height/2))
        rect_points.append((pos_to_check[0]+self.width/2,pos_to_check[1]-self.height/2))

        collision_type = CollisionType.NoCollision
        for point in rect_points:
            if rect.in_bounds(point[0], point[1]):
                if rect.orientation == Orientation.Horizontal:
                    self.modY = 0
                    collision_type = CollisionType.Floor
                elif rect.orientation == Orientation.Vertical:
                    collision_type = CollisionType.Wall
        return collision_type

    def _jump(self):
        if self.state == PawnState.Walk:
            #print("Jump")
            self.modY = -10.0
            self.state = PawnState.Raising

    def handle_events(self, events: List[pygame.event.Event]):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self._jump()
        elif key[pygame.K_a]:
            self.vert_input = -2
        elif key[pygame.K_d]:
            self.vert_input = 2
        else:
            self.vert_input = 0
        if key[pygame.K_SPACE]:
            self._jump()

    def draw(self, window: Surface):
        if self.bLeftSide:
            window.blit(self.drawn_image, self.drawn_rect)
        else:
            window.blit(pygame.transform.flip(self.drawn_image, True, False), self.drawn_rect)