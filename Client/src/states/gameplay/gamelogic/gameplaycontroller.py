from .pawn import Pawn
from .rectangle import *
from .ball import Ball
from typing import List

class GameplayController:
    def __init__(self, side: int, possessed_pawn: Pawn, rival_pawn: Pawn, ball : Ball):
        self.floor = Rectangle(0,469,1080,200,Orientation.Horizontal)
        self.left_wall = Rectangle(-10,0,12,580,Orientation.Vertical)
        self.right_wall = Rectangle(1078,0,12,580,Orientation.Vertical)
        self.net = Rectangle(534.5,238,12,300,Orientation.Vertical)
        self.ball = ball
        self.possessed_pawn = possessed_pawn
        self.rival_pawn = rival_pawn
        self._init_colliders()

    def _init_colliders(self):
        self.colliders : List[Rectangle] = []
        self.colliders.append(self.floor)
        self.colliders.append(self.left_wall)
        self.colliders.append(self.right_wall)
        self.colliders.append(self.net)

    def update(self, dt: float):
        if self.ball is not None:
            self.ball.update(dt,self.colliders)
            self.ball.check_player_collision((self.possessed_pawn.position.x,self.possessed_pawn.position.y),45.0)
        self.possessed_pawn.update(dt, self.colliders)
