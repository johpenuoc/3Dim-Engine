import pygame
import sys
from math import cos, sin, radians

# ensure parent folder is in the search path
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config.mst import *

def square(centrex, centrey, centred,  width, height, depth):
    height2 = height / 2
    width2 = width / 2
    depth2 = depth / 2
    # front 4 poitns, topleft, topright, bottomright, bottom left
    # then back 4 points in the same order
    points = [
        [centrex - width2, centrey - height2, centred + depth2],
        [centrex + width2, centrey - height2, centred + depth2],
        [centrex + width2, centrey + height2, centred + depth2],
        [centrex - width2, centrey + height2, centred + depth2],

        [centrex - width2, centrey - height2, centred - depth2],
        [centrex + width2, centrey - height2, centred - depth2],
        [centrex + width2, centrey + height2, centred - depth2],
        [centrex - width2, centrey + height2, centred - depth2],
    ]

    return [points, 0]

class Renderer:
    def __init__(self, Main):
        self.main = Main

        self.square = square(
            0, 0, 10,
            50, 50, 3
        )

        self.fov = 0

    def translate_coord(self, x, y):
        return x + (DISPLAYSIZE[0] / 2), y + (DISPLAYSIZE[1] / 2)

    def point(self, x, y, s):
        pygame.draw.rect(self.main.dis, (255, 255, 255), (x, y, s, s))

    def translate_Z(self, x, y, z):
        fov = 1#(z + self.fov + .0001)
        #print(fov)
        return x / (z + self.fov), y / (z + self.fov)
        

    def rotate(self, x, z, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _x = (x * c) - (z * s)
        _z = (x * s) + (z * c)
        #print(f'{_z:.2f}', theta)

        return _x, _z

    def draw_square(self):
        #self.fov += 1 * self.main.dt
        self.square[1] += 50 * self.main.dt
        self.square[1] %= 360
        for p in self.square[0]:
            y = p[1]

            x, z = self.rotate(p[0], p[2], self.square[1])
            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)

            self.point(x, y, 2)