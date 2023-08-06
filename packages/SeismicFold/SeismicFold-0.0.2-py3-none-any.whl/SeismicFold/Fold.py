import csv

from FixedWidthTextParser.Seismic.SpsParser import SpsParser, Relation, Point
from SeismicFold.Grid import Grid
from SeismicFold.helpers import create_point_by_easting_northing


class Fold:
    def __init__(
            self,
            grid: Grid,
            parser: SpsParser,
            sps_file: str,
            rps_file: str,
            xps_file: str,
            verbose=False,
            every=10000
    ):
        self.__parser = parser
        self.__grid = grid
        self.__sps_file = sps_file
        self.__rps_file = rps_file
        self.__xps_file = xps_file

        self.__sps: dict = {}  # key is combined line point index, value is Point object
        self.__rps: dict = {}  # key is line, value is List of Point objects

        self.__fold: dict = {}  # key is bin number
        self.__row: dict = {}  # key is bin number
        self.__col: dict = {}  # key is bin number

        self.__verbose = verbose
        self.__every = every

    def get_sps(self):
        return self.__sps

    def get_rps(self):
        return self.__rps

    def __load_points(self, filename):
        points = []
        with open(filename) as sps:
            line = sps.readline()
            while line:
                parsed = self.__parser.parse_point(line)
                if parsed is not None:
                    points.append(Point(parsed))
                line = sps.readline()
        return points

    def load_sps(self):
        point: Point
        for point in self.__load_points(self.__sps_file):
            self.__sps[Fold.combine_point_number(point)] = point

    def load_rps(self):
        point: Point
        for point in self.__load_points(self.__rps_file):
            number = point.line
            if number in self.__rps.keys():
                self.__rps[number].append(point)
            else:
                self.__rps[number] = [point]

    def load_data(self):
        self.load_sps()
        self.load_rps()

    @staticmethod
    def combine_point_number(point: Point):
        return str(point.line) + str(point.point) + str(point.point_idx)

    @staticmethod
    def combine_point_number_from_partials(line: float, point: float, idx: int):
        return str(line) + str(point) + str(idx)

    def get_r4line_range_points(self, line: float, fp: float, tp: float):
        points = self.__rps[line]
        points_range = []

        point: Point
        for point in points:
            pn = point.point
            if fp <= pn <= tp:
                points_range.append(point)

        return points_range

    def calculate_fold(self):

        previous_sln: float = 0
        previous_spn: float = 0
        previous_sidx: int = 0

        counter = 0
        with open(self.__xps_file, mode='r', buffering=(2 << 16) + 8) as xps:
            line = xps.readline()
            while line:
                relation = self.parse_xps_record(line)
                if relation is not None:
                    if self.__verbose is True:
                        counter += 1
                        if counter % self.__every == 0:
                            print("{:15,d}".format(counter))
                    sln = relation.line
                    spn = relation.point
                    sidx = relation.point_idx

                    if sln != previous_sln or spn != previous_spn or sidx != previous_sidx:
                        combined_sp = self.combine_point_number_from_partials(sln, spn, sidx)
                        sp: Point
                        sp = self.__sps[combined_sp]

                    previous_sln = sln
                    previous_spn = spn
                    previous_sidx = sidx

                    self.calculate_fold4xps_record(sp, relation)

                line = xps.readline()
            if self.__verbose is True:
                print("{:15,d}".format(counter))

    def parse_xps_record(self, record: str):
        parsed = self.__parser.parse_relation(record)
        if parsed is not None:
            relation = Relation(parsed)
            return relation

        return None

    def add_fold_to_bin(self, binn: int, column: int, row: int):
        if binn in self.__fold:
            self.__fold[binn] = self.__fold[binn] + 1
        else:
            self.__fold[binn] = 1
            self.__col[binn] = column
            self.__row[binn] = row

    def calculate_fold4xps_record(self, src_point: Point, relation: Relation):
        sx = src_point.easting
        sy = src_point.northing
        r_points = self.get_r4line_range_points(relation.rcv_line, relation.from_rcv, relation.to_rcv)
        point: Point
        for point in r_points:
            rx = point.easting
            ry = point.northing
            bx = (sx + rx) / 2
            by = (sy + ry) / 2

            bin_point = create_point_by_easting_northing(bx, by)

            if 0.0 != self.__grid.get_rot():
                bin_rot_point = self.__grid.rotate_point_x_y(bin_point)
            else:
                bin_rot_point = bin_point

            bin = self.__grid.bin_xy2cr(bin_rot_point)
            binn = self.__grid.bin_number(bin)

            self.add_fold_to_bin(binn, bin.column, bin.row)

    def write_fold2csv(self, filename: str):
        csv_file = open(filename, "w")

        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Easting', 'Northing', 'Fold', 'Bin Number', 'Row', 'Column'])

        for binn in self.__fold.keys():
            c = self.__col[binn]
            r = self.__row[binn]
            fold_val = self.__fold[binn]

            bxr = self.__grid.get_x0() + self.__grid.get_dxb() / 2 + (c - 1) * self.__grid.get_dxb()
            byr = self.__grid.get_y0() + self.__grid.get_dyb() / 2 + (r - 1) * self.__grid.get_dyb()
            pbr = create_point_by_easting_northing(bxr, byr)

            if 0.0 != self.__grid.get_rot():
                pb = self.__grid.rotate_point_x_y(pbr, True)
            else:
                pb = pbr

            csv_writer.writerow([
                pb.easting,
                pb.northing,
                fold_val,
                binn,
                r,
                c
            ])

        csv_file.close()
