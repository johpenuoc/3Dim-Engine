import pygame
import sys
from math import cos, sin, tan, sqrt, radians

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
        self.fov += 3.5 * self.main.dt
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
            points[id][-1] = (x, y)

        # connecting each dot to actually draw the object
        '''for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                self.connect(points[p_id][-1], points[i1][-1])
                self.connect(points[i1][-1], points[i2][-1])
                self.connect(points[i2][-1], points[p_id][-1])'''

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

            # back
            0, 1, 2,
            3, 2, 1,

            # top
            0, 2, 6,
            6, 4, 0,

            # front
            4, 5, 7,
            7, 6, 4,

            # bottom
            1, 3, 7,
            7, 5, 1,

            # left
            0, 1, 5,
            5, 4, 0,

            # right
            2, 3, 7,
            7, 6, 2

        ]

        self.obj = [
            points, theta, centre, points_index
        ]

        self.fov = 0

# a sphere will be generated
class Sphere(Renderer):
    def __init__(self, Main, centre, rad, theta):
        Renderer.__init__(self, Main)

        # generating the sphere's points
        points = []
        theta1 = 0
        theta2 = 0

        # generate first half first
        inc = 90 / RES
        _inc = 360 / RES
        for i in range(int(inc)):
            for j in range(int(_inc)):
                theta1 += _inc

                l = rad * cos(radians(theta2))
                x = l * sin(radians(theta1))
                y = l * cos(radians(theta1))
                z = l * tan(radians(theta2))

                '''x = rad * cos(radians(theta1))
                z = rad * sin(radians(theta1))

                l = sqrt(x**2 + z**2)
                y = l * tan(radians(theta2))'''

                points.append([x, y, z, [x, y, z]])

            theta2 += inc
            theta1 = 0

        # generate second half next
        inc = 90 / RES
        _inc = 360 / RES
        theta1 = 0
        theta2 = 0
        for i in range(int(inc)):
            for j in range(int(_inc)):
                theta1 += _inc

                l = rad * cos(radians(theta2))
                x = l * sin(radians(theta1))
                y = l * cos(radians(theta1))
                z = l * tan(radians(theta2))

                '''x = rad * cos(radians(theta1))
                z = rad * sin(radians(theta1))

                l = sqrt(x**2 + z**2)
                y = l * tan(radians(theta2))'''

                points.append([x, y, z, [x, y, z]])

            theta2 -= inc
            theta1 = 0

        self.obj = [
            points, theta, centre, []
        ]

        self.fov = 0