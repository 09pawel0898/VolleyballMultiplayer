import math

from src.core.resources.sprite import *
from .rectangle import *
from typing import List, Tuple
from src.core.util.utilis import start_delayed
from src.threads.websocketthread import WebsocketThread
from src.networking.serverRoom.packages import *

class Ball(Sprite):
    def __init__(self,
                 texture: Texture,
                 origin: Origin = Origin.CENTER,
                 position: Vec2 = Vec2(0.0, 0.0)) -> None:
        super().__init__(texture, origin, position)
        self.speed = 0.05
        self.mod = 0.05
        self.rotation = 0.0
        self.D =0.0
        self.radius = 0
        self.bStopped = False
        self.bPlayerInteractionEnabled = True

        #self.bIsRisingUp = False

    def update(self, dt: float, colliders: List[Rectangle]) -> None:
        self.radius = self.texture.image.get_rect().height / 2
        if self.D == 0:
            self.rotation /= 1.01
        if self.speed < 0:
            if -0.5 < self.D < 0.5:
                self.speed /= 1.02
                self.move(Vec2(0,self.speed))
                self.speed+=self.mod
            else:
                self.speed /= 1.02
                self.move(Vec2(self.D, self.speed))
                self.speed += self.mod
        else:
            self.speed *=1.002
            if -0.5 < self.D < 0.5:
                self.move(Vec2(0,self.speed))
                self.speed+=self.mod
            else:
                self.move(Vec2(self.D, self.speed))
                self.speed += self.mod

        for collider in colliders:
            self._check_wall_collision(collider)
        self.rotation /= 1.0005
        self.rotate(-self.D)


    def _check_wall_collision(self, rect: Rectangle):
        if rect.orientation == Orientation.Horizontal:
            if rect.in_bounds(self.position.x+self.radius,self.position.y+self.radius):
                self.speed *= -1
                if not self.bStopped:
                    if self.position.y > 400:
                        side = ""
                        if self.position.x < 540:
                            side = 0
                        elif self.position.x > 540:
                            side = 1
                        WebsocketThread.send(
                            PackageSend(
                                header=CodeSend.BallTouchedFloor,
                                body=f"{side}"))
                        self.bStopped = True
        if rect.orientation == Orientation.Vertical:
            if rect.in_bounds(self.position.x-self.radius,self.position.y):
                self.D *= -1
            elif rect.in_bounds(self.position.x+self.radius,self.position.y):
                self.D *= -1
            #if self.position.y + self.radius >= rect.y:
            #    self.speed *= -1
        elif rect.orientation == Orientation.Vertical:
            pass

    def check_player_collision(self, player_pos : Tuple[float,float], player_radius: float):
        if self.bPlayerInteractionEnabled:
            player_x = player_pos[0]
            player_y = player_pos[1]
            ball_x = self.position.x
            ball_y = self.position.y
            x = abs(ball_x-player_x)
            y = ball_y-player_y
            d = math.sqrt(x*x+y*y)

            if d < self.radius + player_radius:
                if y > 0:
                    self.speed = 5
                    print(-10)
                elif y < 0:
                    self.speed = -10
                    print(-10)
                self.D =  (ball_x - player_x)/14.0
                self.bPlayerInteractionEnabled = False
                # send ball bounced information
                WebsocketThread.send(
                    PackageSend(
                        header=CodeSend.BallBounced,
                        body=f"{self.position.x},{self.position.y},{self.speed},{self.D}"))
                start_delayed(0.5,self._enable_player_interaction)

    def _enable_player_interaction(self):
        self.bPlayerInteractionEnabled = True

