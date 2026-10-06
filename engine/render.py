import pygame
import sys

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
        [centrex - width2, centrey - height2, centred - depth2],
        [centrex + width2, centrey - height2, centred - depth2],
        [centrex + width2, centrey + height2, centred - depth2],
        [centrex - width2, centrey + height2, centred - depth2],

        [centrex - width2, centrey - height2, centred + depth2],
        [centrex + width2, centrey - height2, centred + depth2],
        [centrex + width2, centrey + height2, centred + depth2],
        [centrex - width2, centrey + height2, centred + depth2],
    ]

    return points

class Renderer:
    def __init__(self, Main):
        self.main = Main

        self.sqaure1 = square(
            0, 0, 0,
            100, 100, 25
        )

        self.fov = 0

    def translate_coord(self, x, y):
        return x + (DISPLAYSIZE[0] / 2), y + (DISPLAYSIZE[1] / 2)

    def point(self, x, y, s):
        pygame.draw.rect(self.main.dis, (255, 255, 255), (x, y, s, s))

    def translate_Z(self, x, y, z):
        fov = 1#abs(z + self.fov + .0001)
        return (
            x / fov,
            y / fov
        )

    def draw_square(self):
        #self.fov += 1 * self.main.dt
        for p in self.sqaure1:
            tz = self.translate_Z(p[0], p[1], p[2])
            #print('after', tz, self.fov)
            p1, p2 = self.translate_coord(tz[0], tz[1])
            self.point(p1, p2, 2)

    def render(self):
        pass