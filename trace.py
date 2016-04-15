# -*- coding: utf-8 -*-
class Point:
    def __init__(self, input):
        # Координаты
        self.x = input[0]
        self.y = input[1]
        self.speed = input[2]
        # Состояние (свой, чужой, бедствие)
        self.s = input[3]

        # Время
        self.t = input[4]

    def __str__(self):
        return ' '.join([str(arg) for arg in [self.x, self.y, self.s, self.t]])

class Trace:
    def __init__(self, points=None):
        if points:
            assert all([isinstance(c, Point) for c in points])
            self.points = points


class MachineTrace:
    def __init__(self, input_trace):
        assert isinstance(input_trace, Trace)
        self.input_trace = input_trace

    # TODO: make normal
    def get_output_coords(self, time):
        """
        Коородината эхосигнала при вращении time
        :param time: время
        """

        in_coords = self.input_trace.points
        for c in range(len(in_coords)):
            if in_coords[c].t > time:
                return in_coords[c - 1].x, in_coords[c - 1].y


class SupportCoord:
    def __init__(self, coord):
        self.coord = coord['x'], coord['y']
        self.vector = coord['x_v'], coord['y_v']


class SupportTrace:
    def __init__(self, coords):
        assert isinstance(coords, SupportCoord)
        self.coords = coords