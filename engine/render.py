import pygame
import sys
from math import cos, sin, radians

# ensure parent folder is in the search path
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config.mst import *

class Renderer:
    def __init__(self, Main):
        self.main = Main

    def translate_coord(self, x, y):
        return x + (DISPLAYSIZE[0] / 2), y + (DISPLAYSIZE[1] / 2)

    def point(self, x, y, s):
        pygame.draw.rect(self.main.dis, (255, 255, 255), (x, y, s, s))

    def translate_Z(self, x, y, z):
        return (x / (z + self.fov)) * RENDER_SCALE, (y / (z + self.fov)) * RENDER_SCALE
        
    def rotate(self, x, z, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _x = (x * c) - (z * s)
        _z = (x * s) + (z * c)

        return _x, _z

    def wire(self, p1, p2):
        pass

    def draw(self):
        #self.fov += .2 * self.main.dt
        self.cube[1] += (50 * self.main.dt) % 360
        points = self.cube[0]
        centre = self.cube[2]
        for p in points:
            x, z = self.rotate(p[0], p[2], self.cube[1])
            y = p[1]
            
            x += centre[0]
            y += centre[1]
            z += centre[2]

            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)

            self.point(x, y, 2)

class Cube(Renderer):
    def __init__(self, Main, centre, dim, theta):
        Renderer.__init__(self, Main)
        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2
        points = [
            [-width2, -height2, -depth2], [-width2, height2, -depth2], [width2, -height2, -depth2], [width2, height2, -depth2],
            [-width2, -height2, depth2], [-width2, height2, depth2], [width2, -height2, depth2], [width2, height2, depth2]
        ]

        self.cube = [
            points, theta, centre
        ]

        self.fov = 0