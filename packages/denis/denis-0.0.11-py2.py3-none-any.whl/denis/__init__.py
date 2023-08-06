import math
import numbers
import os

import numpy as np

from . import _native


class DoesntBelongException(Exception):
    pass


def _raise_if_point_doesnt_belong(point, line):
    custom_vector = Vector(points=(point, line._point1))
    if not line._normed_vector.is_colinear_to(custom_vector):
        raise DoesntBelongException()


def is_zero(value, resolution=None):
    if resolution is None:
        resolution = float(os.environ.get('DENIS_RESOLUTION', '0.01'))
    return abs(value) < resolution


def to_degrees(rad):
    return rad * 180 / math.pi


def square(x):
    return math.pow(x, 2)


def determinant(vector1, vector2):
    return vector1._x * vector2._y - vector2._x * vector1._y


_AVG_EARTH_RADIUS = 6371000  # In meters


def haversine(lat_lng1, lat_lng2, native=True):
    if native:
        return _native.haversine(lat_lng1, lat_lng2)

    """Cf https://github.com/mapado/haversine"""
    lat1, lng1 = lat_lng1
    lat2, lng2 = lat_lng2
    lat1, lng1, lat2, lng2 = map(math.radians, (lat1, lng1, lat2, lng2))
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = math.sin(lat * 0.5) ** 2 \
        + math.cos(lat1) * math.cos(lat2) * math.sin(lng * 0.5) ** 2
    return 2 * _AVG_EARTH_RADIUS * math.asin(math.sqrt(d))


def improved_reverse_haversine(lat_lng):
    rat_lat = lat_lng[0] * math.pi / 180
    rad_ky = 1 / _AVG_EARTH_RADIUS
    rad_kx = math.acos(1 - 2 * square(math.sin(1 / _AVG_EARTH_RADIUS)) / square(math.cos(rat_lat))) / 2
    return to_degrees(rad_kx), to_degrees(rad_ky)


def get_middle(point1, point2):
    return point1 + Vector(points=(point1, point2)) / 2


class Point(object):

    def __init__(self, *, lat_lng=None, x_y=None, base=None):
        if base is None:
            raise Exception('A point needs a base')
        self._base = base

        if lat_lng:
            self.latitude = lat_lng[0]
            self.longitude = lat_lng[1]
            self._x, self._y = self._base._get_x_y(self)

        elif x_y:
            self._x = x_y[0]
            self._y = x_y[1]
            self.latitude, self.longitude = self._base._get_lat_lng(self)

        else:
            raise Exception('A point needs some coordinates')

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError()
        return Point(
            x_y=(self._x + other._x, self._y + other._y),
            base=self._base,
        )

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError()
        return self + -other

    def __str__(self):
        return '<Point latitude={} longitude={}>'.format(self.latitude, self.longitude)


class Base(object):

    def __init__(self, lat_lng):
        self.origin = lat_lng
        self._kx, self._ky = improved_reverse_haversine(self.origin)

    def make_point(self, *, lat_lng=None, x_y=None):
        return Point(lat_lng=lat_lng, x_y=x_y, base=self)

    def _get_x_y(self, point):
        return (
            (point.longitude - self.origin[1]) / self._kx,
            (point.latitude - self.origin[0]) / self._ky,
        )

    def _get_lat_lng(self, point):
        return (
            self.origin[0] + point._y * self._ky,
            self.origin[1] + point._x * self._kx,
        )


class Vector(object):

    def __init__(self, *, points=None, x_y=None):
        if points:
            self._x = points[1]._x - points[0]._x
            self._y = points[1]._y - points[0]._y

        elif x_y:
            self._x = x_y[0]
            self._y = x_y[1]

        else:
            raise Exception('A vector needs some coordinates')

    def get_norm(self):
        return math.sqrt(square(self._x) + square(self._y))

    def get_normalized(self):
        current_norm = self.get_norm()
        return Vector(x_y=(self._x / current_norm, self._y / current_norm))

    def get_direct_orthogonal(self):
        vec = Vector(x_y=(-self._y, self._x))
        # Determinant sign is the same than the sinus of the angle
        # between the two vectors
        if determinant(self, vec) < 0:
            return -vec
        return vec

    def is_colinear_to(self, other_vector):
        return is_zero(determinant(self, other_vector), resolution=1e-6)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(x_y=(self._x * other, self._y * other))

        if isinstance(other, Vector):
            return self._x * other._x + self._y * other._y

        raise NotImplementedError()

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, numbers.Number):
            raise NotImplementedError()
        return Vector(x_y=(self._x / other, self._y / other))

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        return Vector(x_y=(-self._x, -self._y))


class Line(object):

    def __init__(self, point1, point2):
        self._point1 = point1
        self._point2 = point2

        self._normed_vector = Vector(points=(point1, point2)).get_normalized()

    def get_perpendicular_at(self, point):
        _raise_if_point_doesnt_belong(point, self)
        direct_orthogonal_vector = self._normed_vector.get_direct_orthogonal()
        return Line(point, point + direct_orthogonal_vector)

    def get_point_at_distance(self, distance, from_point):
        _raise_if_point_doesnt_belong(from_point, self)
        return from_point + distance * self._normed_vector

    def is_parallel_to(self, other_line):
        return self._normed_vector.is_colinear_to(other_line._normed_vector)

    def is_perpendicular_to(self, other_line):
        return is_zero(
            self._normed_vector * other_line._normed_vector,
            resolution=1e-6,
        )

    def get_intersection_with(self, other_line):
        xv1, yv1 = self._normed_vector._x, self._normed_vector._y
        xv2, yv2 = other_line._normed_vector._x, other_line._normed_vector._y
        xp1, yp1 = self._point1._x, self._point1._y
        xp2, yp2 = other_line._point1._x, other_line._point1._y

        eqs = np.array([[yv1, -xv1], [yv2, -xv2]])
        vals = np.array([yv1*xp1 - xv1*yp1, yv2*xp2 - xv2*yp2])
        x_y = np.linalg.solve(eqs, vals).tolist()
        return self._point1._base.make_point(x_y=x_y)


class Segment(object):

    def __init__(self, point1, point2):
        self.start = point1
        self.end = point2

        self._vector = Vector(points=(point1, point2))
        self.length = self._vector.get_norm()

    def divide_per(self, count):
        vector = self._vector / count
        return (
            Segment(self.start + i * vector, self.start + (i+1) * vector)
            for i in range(count)
        )
