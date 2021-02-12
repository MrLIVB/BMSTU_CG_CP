from math import sin, cos, pi, radians

from baseobject import Point

class TransformVisitor(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def visit(self, smt):
        pass

class MoveVisitor(TransformVisitor):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    def visit(self, smt):
        x, y, z = smt.get_position()
        x += self.x
        y += self.y
        z += self.z

        smt.set_position(x, y, z)

class RotateVisitor(TransformVisitor):
    def __init__(self, x, y, z, center: Point = Point(0, 0, 0)):
        super().__init__(x, y, z)
        self.center_x = center.x
        self.center_y = center.y
        self.center_z = center.z

    def rotate_ox(self, xyz, cos_teta_x,  sin_teta_x):
        y = xyz[1]
        z = xyz[2]

        xyz[1] = +y * cos_teta_x + z * sin_teta_x
        xyz[2] = -y * sin_teta_x + z * cos_teta_x

    def rotate_oy(self, xyz, cos_teta_y, sin_teta_y):
        x = xyz[0]
        z = xyz[2]

        xyz[0] = +x * cos_teta_y + z * sin_teta_y
        xyz[2] = -x * sin_teta_y + z * cos_teta_y

    def rotate_oz(self, xyz, cos_teta_z, sin_teta_z):
        x = xyz[0]
        y = xyz[1]

        xyz[0] = x * cos_teta_z - y * sin_teta_z
        xyz[1] = x * sin_teta_z + y * cos_teta_z

    def visit(self, smt):
        sin_teta_x = sin(radians(self.x))
        cos_teta_x = cos(radians(self.x))

        sin_teta_y = sin(radians(self.y))
        cos_teta_y = cos(radians(self.y))

        sin_teta_z = sin(radians(self.z))
        cos_teta_z = cos(radians(self.z))

        xyz = [smt.x - self.center_x, smt.y - self.center_y, smt.z - self.center_z]

        self.rotate_ox(xyz, cos_teta_x, sin_teta_x)
        self.rotate_oy(xyz, cos_teta_y, sin_teta_y)
        self.rotate_oz(xyz, cos_teta_z, sin_teta_z)

        smt.x = xyz[0] + self.center_x
        smt.y = xyz[1] + self.center_y
        smt.z = xyz[2] + self.center_z
