import pygame
import sys
from math import cos, sin, tan, radians, floor
from random import randint

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

    def vertex_proc(self):
        #self.fov += .2 * self.main.dt
        self.obj[1] += (50 * self.main.dt) % 360
        #self.fov += 3.5 * self.main.dt
        points = self.obj[0]
        centre = self.obj[2]
        #points_index = self.obj[3]

        for id, p in enumerate(points):
            x, z = self.rotate(p[0], p[2], self.obj[1])
            y = p[1]

            x += centre[0]
            y += centre[1]
            z += centre[2]

            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)

            #self.point(x, y, 2)
            points[id][-1] = (x, y)

    def svertex_proc(self):
        self.obj[1] += (20 * self.main.dt) % 360
        #self.fov += 1 * self.main.dt
        points = self.obj[0]
        centre = self.obj[2]

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
                points[l_id][id][-1] = (x, y, z)

    def render(self):
        points = self.obj[0]
        points_index = self.obj[3]

        # connecting each dot to actually draw the object
        for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                self.connect(points[p_id][-1], points[i1][-1])
                self.connect(points[i1][-1], points[i2][-1])
                self.connect(points[i2][-1], points[p_id][-1])

    def triangle_area(self, p1, p2, p3):
        return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2)
    def shader(self, p1, p2, p3):
        x_list = [p1[0], p2[0], p3[0]]
        y_list = [p1[1], p2[1], p3[1]]
        minx = min(x_list)
        miny = min(y_list)
        maxx = max(x_list)
        maxy = max(y_list)
        square_prem = (
            abs(maxx - minx),
            abs(maxy - miny)
        )

        # this determines what points within this square
        # (that surrounds the triangle) are inside the
        # triangle or not
        #c = randint(0, 255)
        colour = (
            200, 0, 0
        )
        dis = self.main.dis
        disx2 = DISPLAYSIZE[0] / 2
        disy2 = DISPLAYSIZE[1] / 2
        for x in range(int(square_prem[0])):
            for y in range(int(square_prem[1])):
                p = (minx + x, miny + y)

                a1 = self.triangle_area(p1, p2, p3)
                a2 = self.triangle_area(p, p1, p2)
                a3 = self.triangle_area(p, p2, p3)
                a4 = self.triangle_area(p, p1, p3)

                if int(a2 + a3 + a4) == int(a1):
                    _x, _y = self.translate_coord(p[0], p[1])
                    #pygame.draw.rect(
                    #    dis, colour, (_x - disx2, _y - disy2, 1, 1)
                    #)
                    __x = int(_x - disx2)
                    __y = (_y - disy2)
                    dis.set_at((__x, __y), colour)
                    continue
                else:
                    continue


    def srender(self):
        points = self.obj[0]
        centre = self.obj[2]
        points_index = self.obj[3]

        #pixel_array = pygame.surfarray.pixels3d(self.main.dis)

        # connecting each dot to actually draw the object
        id = 3
        for _ in range(int(len(points_index) / 3)):
            #print('id', id)
            p_id = points_index[id - 1]
            i1 = points_index[id - 2]
            i2 = points_index[id - 3]

            _id = p_id[0]
            l_id = p_id[1]

            p1 = points[l_id][_id][-1]
            p2 = points[i1[1]][i1[0]][-1]
            p3 = points[i2[1]][i2[0]][-1]

            z_avg = abs((p1[2] + p2[2] + p3[2]) / 3)

            # only render the most front portion of the sphere
            if z_avg < centre[2] / 4:
                #self.shader(p1, p2, p3)
                self.connect(p1, p2)
                self.connect(p2, p3)
                self.connect(p3, p1)
                id += 3
                continue
            else:
                id += 3
                continue

class Cube(Renderer):
    def __init__(self, Main, centre, dim, theta):
        Renderer.__init__(self, Main)
        self.fov = 0

        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2
        points = [
            # top left                      bottom left                 top right                    bottom right
            [-width2, -height2, -depth2], [-width2, height2, -depth2], [width2, -height2, -depth2], [width2, height2, -depth2],
            [-width2, -height2, depth2], [-width2, height2, depth2], [width2, -height2, depth2], [width2, height2, depth2]
        ]
        points = [[*i, i] for i in points]

        index = [

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
            points, theta, centre, index
        ]

# a sphere will be generated
class Sphere(Renderer):
    def __init__(self, Main, centre, rad, theta):
        Renderer.__init__(self, Main)

        self.fov = 0
        self.vertex_buf = []

        ###############################################################
        inc = 90 / SPHERE_RES
        _inc = 360 / inc
        points = []

        # generate first half first
        theta1 = 0
        theta2 = 0
        for _ in range(int(inc)):

            points.append([])
            for _ in range(int(inc)):
                theta1 += _inc

                l = rad * cos(radians(theta2))
                x = l * sin(radians(theta1))
                y = l * cos(radians(theta1))
                z = l * tan(radians(theta2))

                points[-1].append([x, y, z, [x, y, z]])

            theta2 += SPHERE_RES
            theta1 = 0

        # generate second half next
        theta1 = 0
        theta2 = 0
        for _ in range(int(inc)):

            points.append([])
            for _ in range(int(inc)):
                theta1 += _inc

                l = rad * cos(radians(theta2))
                x = l * sin(radians(theta1))
                y = l * cos(radians(theta1))
                z = l * tan(radians(theta2))

                points[-1].append([x, y, z, [x, y, z]])

            theta2 -= SPHERE_RES
            theta1 = 0
        ##################################################################

        self.obj = [
            points, theta, centre
        ]
        self.obj.append(self.index_proc())
        #print('Removing redundant sides...')
        #self.elim_redunants()
        #print('Completed removing redundant sides.')
        #print(self.obj[3])

    def index_proc(self):
        indexes = []
        middle = len(self.obj[0]) / 2
        for l_id, layer in enumerate(self.obj[0][:int(middle)]):
            indexes.append([])
            indexes_len = len(indexes) - 1

            for id, _ in enumerate(layer):
                if l_id > 0:
                    indexes[indexes_len - 1].append([[id - 1, l_id], [id, l_id], [id, l_id - 1]])
                    indexes[indexes_len - 1].append([[id, l_id - 1], [id - 1, l_id - 1], [id - 1, l_id]])


        for l_id, layer in enumerate(self.obj[0][int(middle):]):
            indexes.append([])
            indexes_len = len(indexes) - 1

            l_id += int(middle)

            for id, _ in enumerate(layer):
                if l_id > 0 and l_id - 1 >= middle:
                    indexes[indexes_len - 1].append([[id - 1, l_id], [id, l_id], [id, l_id - 1]])
                    indexes[indexes_len - 1].append([[id, l_id - 1], [id - 1, l_id - 1], [id - 1, l_id]])

        indexes = [k for i in indexes for j in i for k in j]
        return indexes

    # this should remove any lines that overlap and are, hence, 'redundant'
    def elim_redunants(self):
        obj3_len = len(self.obj) - 1
        for id, p1 in enumerate(self.obj[3]):
            for id2, p2 in enumerate(self.obj[3]):
                if id != id2 and id < obj3_len and id2 < obj3_len:
                    if p2[0] == p1[0] and self.obj[3][id2 + 1] == self.obj[3][id + 1]:
                        self.obj[3][id][0] = -self.obj[3][id][0]
                        self.obj[3][id + 1][0] = -self.obj[3][id + 1][0]

                    '''buf.append(id)

                    if (id + 1) % 6 == 0:
                        b1 = (buf[0] == buf[3])
                        b2 = (buf[1] == buf[4])
                        b3 = (buf[2] == buf[5])

                        if b1 and b2:
                            self.obj[0][id - 2] = -self.obj[0][id - 2]
                            self.obj[0][id - 1] = -self.obj[0][id - 1]
                        elif b2 and b3:
                            self.obj[0][id - 1] = -self.obj[0][id - 1]
                            self.obj[0][id] = -self.obj[0][id]
                        elif b3 and b1:
                            self.obj[0][id] = -self.obj[0][id]
                            self.obj[0][id - 2] = -self.obj[0][id - 2]

                        buf = []'''
