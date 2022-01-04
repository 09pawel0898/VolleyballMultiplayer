from pygame import Color
from typing import Callable
import threading

def parse_color(color):
    if type(color) == str:
        return Color(color)
    else:
        colourRGB = Color("white")
        colourRGB.r = color[0]
        colourRGB.g = color[1]
        colourRGB.b = color[2]
        return colourRGB


def lerp(a,b,alpha):
    return a + (b-a) * alpha

def start_delayed(delay: float, func: Callable):
    threading.Timer(delay,func).start()