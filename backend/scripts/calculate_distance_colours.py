import math


def dist(h1, h2):
    def rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    r1,g1,b1 = rgb(h1)
    r2,g2,b2 = rgb(h2)
    return math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

print(dist('#D4B5A8', '#F4C2C2'))