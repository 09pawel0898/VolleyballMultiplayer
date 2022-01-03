from pygame import Color

def parse_color(color):
    if type(color) == str:
        return Color(color)
    else:
        colourRGB = Color("white")
        colourRGB.r = color[0]
        colourRGB.g = color[1]
        colourRGB.b = color[2]
        return colourRGB