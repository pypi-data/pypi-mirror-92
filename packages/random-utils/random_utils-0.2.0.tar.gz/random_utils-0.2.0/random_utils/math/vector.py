from math import atan, sin, cos, radians, degrees
import numpy as np


class Vector:
    """
    A vector class which has many useful vector methods.
    """
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def get_rad(self):
        """
        Only 2D
        """
        return atan(self.y / self.x)

    def get_deg(self):
        """
        Only 2D
        """
        return degrees(self.get_rad())

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def get_mag(self):
        return self.get_magsq() ** 0.5

    def get_magsq(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        self.set_mag(1)

    def rem(self, vec):
        if isinstance(vec, Vector):
            self.x %= vec.x
            self.y %= vec.y

    def dist(self, vec):
        if isinstance(vec, Vector):
            return ((vec.x - self.x) ** 2 + (vec.y - self.y) ** 2 + (vec.z - self.z) ** 2) ** 0.5

    def limit(self, min_val=None, max_val=None, axes=("x", "y", "z")):
        if min_val is not None:
            for axis in axes:
                setattr(self, axis, max(min_val, getattr(self, axis)))
        if max_val is not None:
            for axis in axes:
                setattr(self, axis, min(max_val, getattr(self, axis)))

    def get_list(self):
        return [self.x, self.y, self.z]

    def get_array(self):
        return self.get_list()

    def set_mag(self, mag):
        ratio = mag / self.get_mag()
        self.mult(ratio)

    def set_rad(self, radians):
        mag = self.get_mag()
        self.x = cos(radians) * mag
        self.y = sin(radians) * mag

    def set_deg(self, degrees):
        self.rotate_rad(radians(degrees))

    def rotate_rad(self, radians):
        self.set_rad(self.get_rad() + radians)

    def rotate_deg(self, degrees):
        self.rotate_rad(radians(degrees))

    def rad_between(self, vec):
        """
        Only 2D
        """
        if isinstance(vec, Vector):
            return vec.get_rad() - self.get_rad()

    def deg_between(self, vec):
        """
        Only 2D
        """
        if isinstance(vec, Vector):
            return vec.get_deg() - self.get_deg()

    def linterp(self, vec, amt):
        self.x += (vec.x - self.x) * amt
        self.y += (vec.y - self.y) * amt
        self.z += (vec.z - self.z) * amt

    def add(self, vec):
        if isinstance(vec, Vector):
            self.x += vec.x
            self.y += vec.y
            self.z += vec.z

    def sub(self, vec):
        if isinstance(vec, Vector):
            self.x -= vec.x
            self.y -= vec.y
            self.z -= vec.z

    def div(self, scalar, floor=False):
        if isinstance(scalar, int) or isinstance(scalar, float):
            if floor:
                self.x //= scalar
                self.y //= scalar
                self.z //= scalar
            else:
                self.x /= scalar
                self.y /= scalar
                self.z /= scalar

    def mult(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            self.x *= scalar
            self.y *= scalar
            self.z *= scalar

    def dot(self, vec):
        if isinstance(vec, Vector):
            return self * vec

    def cross(self, vec):
        if isinstance(vec, Vector):
            return np.cross(self.get_list(), vec.get_list())

    def equals(self, vec):
        return self.__eq__(vec)

    @classmethod
    def from_radians(cls, radians):
        return cls(cos(radians), sin(radians))

    @classmethod
    def from_degrees(cls, degrees):
        return cls(cos(radians(degrees)), sin(radians(degrees)))

    def __iter__(self):
        return iter(self.get_list())

    def __getitem__(self, slice):
        return self.get_list()[slice]

    def __add__(self, vec):
        if isinstance(vec, Vector):
            return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def __sub__(self, vec):
        if isinstance(vec, Vector):
            return Vector(self.x - vec.x, self.y - vec.y, self.z - vec.z)

    def __truediv__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def __floordiv__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector(self.x // scalar, self.y // scalar, self.z // scalar)

    def __mul__(self, val):
        if isinstance(val, Vector):
            return self.x * val.x + self.y * val.y + self.z * val.z
        elif isinstance(val, int) or isinstance(val, float):
            return Vector(self.x * val, self.y * val, self.z * val)

    def __eq__(self, vec):
        if isinstance(vec, Vector):
            return vec.x == self.x and vec.y == self.y and vec.z == self.z

    def __ne__(self, vec):
        if isinstance(vec, Vector):
            return vec.x != self.x and vec.y != self.y and vec.z != self.z

    def __repr__(self):
        return f"Vector at ({self.x}, {self.y}, {self.z})"
