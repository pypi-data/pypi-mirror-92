import math
import json

from FixedWidthTextParser.Seismic.SpsParser import Point
from SeismicFold.Bin import Bin
from SeismicFold.helpers import create_point_by_line_point_idx


class Grid:
    def __init__(self, x0: float = 0.0, y0: float = 0.0, rot: float = 0.0, dxb: float = 0.0, dyb: float = 0.0,
                 nxb: int = 0, nyb: int = 0):
        self.__x0 = x0
        self.__y0 = y0
        self.__rot = rot
        self.__dxb = dxb
        self.__dyb = dyb
        self.__nxb = nxb
        self.__nyb = nyb

    def get_x0(self):
        return self.__x0

    def get_y0(self):
        return self.__y0

    def get_rot(self):
        return self.__rot

    def get_dxb(self):
        return self.__dxb

    def get_dyb(self):
        return self.__dyb

    def get_nxb(self):
        return self.__nxb

    def get_nyb(self):
        return self.__nyb

    def rotate_point_x_y(self, point: Point, counterclockwise=False):
        rotated_point = create_point_by_line_point_idx(point.line, point.point, point.point_idx)
        x = point.easting
        y = point.northing
        x0 = float(self.__x0)
        y0 = float(self.__y0)
        rot = float(self.__rot)
        if counterclockwise is True:
            rot = rot * -1

        radians = math.radians(rot)

        adjusted_x = (x - x0)
        adjusted_y = (y - y0)
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)
        rotx = x0 + cos_rad * adjusted_x + sin_rad * adjusted_y
        roty = y0 + -sin_rad * adjusted_x + cos_rad * adjusted_y

        rotated_point.easting = rotx
        rotated_point.northing = roty

        return rotated_point

    def bin_xy2cr(self, rotated: Point):
        b = Bin()

        c1 = (rotated.easting - self.__x0) / self.__dxb
        c2 = math.floor(c1)

        if c1 > c2:
            c = int(c2 + 1)
        else:
            c = int(c2)

        r1 = (rotated.northing - self.__y0) / self.__dyb
        r2 = math.floor(r1)

        if r1 > r2:
            r = int(r2 + 1)
        else:
            r = int(r2)

        b.column = c
        b.row = r

        return b

    def bin_number(self, b: Bin):
        number = -1
        if b.column > 0 and b.row > 0:
            number = (b.row - 1) * self.__nxb + b.column

        return number

    def bin_cr(self, bin_number: int):
        b = Bin()
        r = int(math.floor((bin_number / self.__nxb)) + 1)
        c = bin_number - (r - 1) * self.__nxb
        b.column = c
        b.row = r

        return b

    def write(self, filename):
        grid_dict = {'x0': self.__x0, 'y0': self.__y0, 'rot': self.__rot, 'dxb': self.__dxb, 'dyb': self.__dyb,
                     'nxb': self.__nxb, 'nyb': self.__nyb}
        file = open(filename, "w")
        json.dump(grid_dict, file)
        file.close()

    def read(self, filename):
        file = open(filename, "r")
        grid_dict = json.load(file)
        self.__x0 = grid_dict['x0']
        self.__y0 = grid_dict['y0']
        self.__rot = grid_dict['rot']
        self.__dxb = grid_dict['dxb']
        self.__dyb = grid_dict['dyb']
        self.__nxb = grid_dict['nxb']
        self.__nyb = grid_dict['nyb']
        file.close()
