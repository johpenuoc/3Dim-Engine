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
        #self.fov += 3.5 * self.main.dt
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
        for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                self.connect(points[p_id][-1], points[i1][-1])
                self.connect(points[i1][-1], points[i2][-1])
                self.connect(points[i2][-1], points[p_id][-1])

    def draw_sphere(self):
        #self.fov += .2 * self.main.dt
        self.obj[1] += (20 * self.main.dt) % 360
        #self.fov += 1 * self.main.dt
        points = self.obj[0]
        centre = self.obj[2]
        points_index = self.obj[3]

        for l_id, layer in enumerate(points):
            for id, p in enumerate(layer):
                x, z = self.rotate(p[0], p[2], self.obj[1])
                y = p[1]
                
                x += centre[0]
                y += centre[1]
                z += centre[2]

                x, y = self.translate_Z(x, y, z)
                x, y = self.translate_coord(x, y)

                self.point(x, y, 2)
                points[l_id][id][-1] = (x, y)

        # connecting each dot to actually draw the object
        for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                _id = p_id[0]
                l_id = p_id[1]

                p1 = points[l_id][_id][-1]
                p2 = points[i1[1]][i1[0]][-1]
                p3 = points[i2[1]][i2[0]][-1]
                self.connect(p1, p2)
                self.connect(p2, p3)
                self.connect(p3, p1)

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

        self.index = []

        # generate first half first
        inc = 90 / SPHERE_RES
        _inc = 360 / inc
        for i in range(int(inc)):
            points.append([])
            self.index.append([])
            for j in range(int(inc)):
                theta1 += _inc

                l = rad * cos(radians(theta2))
                x = l * sin(radians(theta1))
                y = l * cos(radians(theta1))
                z = l * tan(radians(theta2))

                '''x = rad * cos(radians(theta1))
                z = rad * sin(radians(theta1))

                l = sqrt(x**2 + z**2)
                y = l * tan(radians(theta2))'''

                points[-1].append([x, y, z, [x, y, z]])
                self.index[-1].append([j, i])

            theta2 += SPHERE_RES
            theta1 = 0

        # generate second half next
        theta1 = 0
        theta2 = 0
        orig_len_points = len(points)
        for i in range(int(inc)):
            #points.insert(0, [])
            points.append([])
            self.index.append([])
            for j in range(int(inc)):
                theta1 += _inc

                l = rad * cos(radians(theta2))
                x = l * sin(radians(theta1))
                y = l * cos(radians(theta1))
                z = l * tan(radians(theta2))

                '''x = rad * cos(radians(theta1))
                z = rad * sin(radians(theta1))

                l = sqrt(x**2 + z**2)
                y = l * tan(radians(theta2))'''

                points[-1].append([x, y, z, [x, y, z]])
                self.index[-1].append([j, orig_len_points + i])

            theta2 -= SPHERE_RES
            theta1 = 0

        self.obj = [
            points, theta, centre, []
        ]

        self.fov = 0

        self.triangulate()

    def triangulate(self):
        [
            [
                [0, 0, 0]
            ],

            [
                [0, 0, 0]
            ]
        ]
        indexes = []
        '''for l_id, layer in enumerate(self.obj[0]):
            for id, _ in enumerate(layer):
                indexes.append([id, l_id])
                if id % 3 == 0 and l_id > 0:
                    indexes.append([id - 1, l_id])
                    indexes.append([id - 2, l_id])
                    indexes.append([id - 2, l_id])'''
                    #indexes.append([id - 3, (l_id + 1) % len(self.obj[0]) - 1])
                        
            
        for l_id, layer in enumerate(self.obj[0]):
            indexes.append([])
            indexes_len = len(indexes) - 1
            for id, _ in enumerate(layer):

                if l_id > 0:
                    indexes[indexes_len - 1].append([[id - 1, l_id], [id, l_id], [id, l_id - 1]])
                #elif l_id < 1 and id > 0:
                #    indexes[0].append([[id - 1, l_id], [id, l_id], [id, l_id]])
                

                #id_id = len(indexes) - 1
                #if l_id > 0 and len(indexes[id_id - 1]) > id:
                #    indexes[id_id - 1][id].append([id, l_id])

                #if id > 0:
                #    indexes[-1].append([[id - 1, l_id], [id, l_id]])

            #if l_id >= len(self.obj[0]):
            #    indexes[0][id].append([id, l_id])

        #print(indexes)

        indexes = [k for i in indexes for j in i for k in j]
        #print(self.index)
        sphere_mid = len(self.index) / 2
        _index = []
        for ll_id, layer in enumerate(self.index):
            for p_id, p in enumerate(layer):
                id = p[0]
                l_id = p[1]

                if p_id < len(layer) - 1 and (p_id + 1) % 2 != 0:
                    next_p = layer[p_id + 1]
                    if not (l_id >= len(self.index) - 1):
                        point = [p, next_p, self.index[l_id + 1][next_p[0]]]
                        _index.append(point)
                    else:
                        pass

                '''if not (l_id >= len(self.index) - 1):
                    if p_id < len(layer) - 1 and (p_id + 1) % 2 != 0:
                        next_p = layer[p_id + 1]
                        point = [p, next_p, self.index[l_id + 1][next_p[0]]]
                        _index.append(point)'''
        _index = [j for i in _index for j in i]
        #print(_index)

        self.obj[3] = indexes
                