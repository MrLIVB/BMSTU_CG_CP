from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from baseobject import BaseObject, Point, Vector

class Polygon(BaseObject):
    def __init__(self, p1: Point, p2: Point, p3: Point, color: QColor = Qt.black):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = color

    def get_points(self):
        return [self.p1, self.p2, self.p3]

    def get_normal(self):
        v1 = Vector().from_points(self.p1, self.p2)
        v2 = Vector().from_points(self.p1, self.p3)
        return (v1 * v2).normalize()

    def get_color(self, lights):
        x, y, z = 0, 0, 0
        for p in self.get_points():
            xt, yt, zt = p.get_position()
            x += xt
            y += yt
            z += zt

        centroid = Point(x / 3, y / 3, z / 3)
        normal = self.get_normal().normalize()

        intensity = 0.4
        for light in lights:
            v = Vector().from_points(light, centroid).normalize()
            cos = max(v.scalar_multiplication(normal), 0)
            intensity += light.intensity * cos

        rgb = list(QColor(self.color).getRgbF())

        rgb[0] *= intensity
        rgb[1] *= intensity
        rgb[2] *= intensity

        return QColor().fromRgbF(rgb[0], rgb[1], rgb[2])

    def accept(self, visitor):
        self.p1.accept(visitor)
        self.p2.accept(visitor)
        self.p3.accept(visitor)
