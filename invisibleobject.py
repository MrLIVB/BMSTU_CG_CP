from baseobject import BaseObject, Point, Vector

class Camera(Point):
    def __init__(self, x, y, z, direction: Vector):
        super().__init__(x, y, z)
        self.direction = direction

    def accept(self, visitor):
        visitor.visit(self)

class LightSource(Point):
    def __init__(self, x=0, y=0, z=0, intensity=0.):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity

    def copy_from(self, source):
        self.x, self.y, self.z = source.get_position()

        self.intensity = source.intensity

    def accept(self, visitor):
        visitor.visit(self)

