from math import sqrt

class BaseObject(object):
    def accept(self, visitor):
        pass

class Point(BaseObject):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def divide_number(self, number):
        self.x = self.x / number
        self.y = self.y / number
        self.z = self.z / number
        return self

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_position(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def accept(self, visitor):
        visitor.visit(self)

class Vector(Point):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)

    def from_points(self, p1, p2):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y
        self.z = p2.z - p1.z
        return self

    def multiplication(self, a, b):
        res = Vector(0, 0, 0)
        res.x = a.y * b.z - a.z * b.y
        res.y = a.z * b.x - a.x * b.z
        res.z = a.x * b.y - a.y * b.x
        return res

    def scalar_multiplication(self, b):
        return self.x * b.x + self.y * b.y + self.z * b.z

    def number_multiplication(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def normalize(self):
        length = self.length()
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length
        return self

    def __mul__(self, b):
        res = Vector(0, 0, 0)
        res.x = self.y * b.z - self.z * b.y
        res.y = self.z * b.x - self.x * b.z
        res.z = self.x * b.y - self.y * b.x
        return res

    def __truediv__(self, other):
        res = Vector(0, 0, 0)
        res.x = self.x / other
        res.y = self.y / other
        res.z = self.z / other
        return res

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
