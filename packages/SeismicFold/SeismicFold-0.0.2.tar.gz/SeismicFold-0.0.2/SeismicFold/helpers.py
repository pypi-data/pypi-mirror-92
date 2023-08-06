from FixedWidthTextParser.Seismic.SpsParser import Point


def create_point_by_line_point_idx(line_number, point_number, point_idx):
    data = [
        None,
        line_number,
        point_number,
        point_idx,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

    return Point(data)


def create_point_by_easting_northing(easting: float, northing: float):
    data = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        easting,
        northing,
        None,
        None,
        None,
    ]

    return Point(data)
