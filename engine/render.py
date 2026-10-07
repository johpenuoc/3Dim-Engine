import pygame
import sys
from math import cos, sin, sqrt, radians

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

    def connect(self, p1, p2):
        pygame.draw.line(self.main.dis, (255, 255, 255), (p1[0], p1[1]), (p2[0], p2[1]))

    def draw(self):
        #self.fov += .2 * self.main.dt
        self.obj[1] += (50 * self.main.dt) % 360
        points = self.obj[0]
        centre = self.obj[2]
        points_index = self.obj[3]

        for id, p in enumerate(points):
            x, z = self.rotate(p[0], p[2], self.obj[1])
            y = p[1]
            
            x += centre[0]
            y += centre[1]
            z += centre[2]

            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)

            self.point(x, y, 2)
            points[id][3] = (x, y)

            # connecting each dot to actually draw the object
            point = (x, y)
            p_id = (id + 1) * 3

            i = points_index[p_id - 3]
            self.connect(points[i][-1], points[i + 1][-1])
            self.connect(points[i + 1][-1], point)
            self.connect(point, points[i][-1])

class Cube(Renderer):
    def __init__(self, Main, centre, dim, theta):
        Renderer.__init__(self, Main)
        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2

        points = [
            # top left                      bottom left                 top right                    bottom right
            [-width2, -height2, -depth2], [-width2, height2, -depth2], [width2, -height2, -depth2], [width2, height2, -depth2],
            [-width2, -height2, depth2], [-width2, height2, depth2], [width2, -height2, depth2], [width2, height2, depth2]
        ]
        points = [[*i, i] for i in points]

        points_index = [
            0, 1, 2,  
            1, 2, 3,

            0, 4, 5,
            0, 1, 5,

            2, 6, 7,
            3, 7, 6,

            4, 5, 6,
            5, 6, 7
        ]

        self.obj = [
            points, theta, centre, points_index
        ]

        self.fov = 0