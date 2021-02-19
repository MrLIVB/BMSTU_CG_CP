from math import sqrt, acos, asin, degrees
from scipy import interpolate

from musclemodel import StraightMuscleModel, ComplexMuscleModel, Point, Vector

class BaseModelBuilder(object):
    def __init__(self):
        self.model = []

    def read_file(self):
        pass

    def init_model(self, params):
        pass

    def get_product(self):
        pass

        
class ModelBuilder(BaseModelBuilder):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    @staticmethod
    def read_muscle(file):
        point_start = None
        point_end = None
        a = None
        b = None
        angle_ox = 0

        while 1:
            line = file.readline().split()
            if not line:
                break

            if line[0] == 'ps':
                point_start = Point(float(line[1]), float(line[2]), float(line[3]))
            elif line[0] == 'pe':
                point_end = Point(float(line[1]), float(line[2]), float(line[3]))
            elif line[0] == 'a':
                a = float(line[1])
            elif line[0] == 'b':
                b = float(line[1])
            elif line[0] == 'ox':
                angle_ox = float(line[1])
            else:
                # TODO error
                break

        if (a is None) or (b is None) or (point_start is None) or (point_end is None):
            # TODO error
            quit()

        l = sqrt(pow(point_start.x - point_end.x, 2) + pow(point_start.y - point_end.y, 2) + pow(point_start.z - point_end.z, 2))
        center = Point((point_end.x + point_start.x) / 2, (point_end.y + point_start.y) / 2, (point_end.z + point_start.z) / 2)

        rotation = Vector().from_points(point_start, center)
        rotation: Vector
        rotation.normalize()

        ox_vector = Vector(1, 0, 0)
        angle_oz = degrees(acos(rotation.scalar_multiplication(ox_vector)))

        oz_vector = Vector(0, 0, 1)
        angle_oy = degrees(asin(rotation.scalar_multiplication(oz_vector)))

        rotation_vector = Vector(angle_ox, angle_oy, angle_oz)

        result = [a, b, l, center, rotation_vector]

        return result

    @staticmethod
    def read_spline(file):
        points_start_x = []
        points_start_y = []
        points_end_x = []
        points_end_y = []
        n = None

        while 1:
            line = file.readline().split()
            if not line:
                break

            if line[0] == 'ps':
                points_start_x.append(float(line[1]))
                points_start_y.append(float(line[2]))
            elif line[0] == 'pe':
                points_end_x.append(float(line[1]))
                points_end_y.append(float(line[2]))
            elif line[0] == 'n':
                n = int(line[1])
            else:
                # TODO error
                break

        if n is None:
            # TODO error
            quit()

        points_start = []
        dx1 = (points_start_x[len(points_start_x) - 1] - points_start_x[0]) / (n + 1)
        x = points_start_x[0]

        tck = interpolate.splrep(points_start_x, points_start_y, s=0)
        xnew = [x + i * dx1 for i in range(n)]
        ynew = interpolate.splev(xnew, tck, der=0)

        for i in range(n):
            points_start.append(Point(xnew[i], ynew[i], 0))

        points_end = []
        dx2 = (points_end_x[len(points_end_x) - 1] - points_end_x[0]) / (n + 1)
        tck = interpolate.splrep(points_end_x, points_end_y, s=0)
        x = points_end_x[0]
        xnew = [x + i * dx2 for i in range(n)]
        ynew = interpolate.splev(xnew, tck, der=0)

        for i in range(n):
            points_end.append(Point(xnew[i], ynew[i], 0))

        def calculate_muscle(point_start, point_end):
            l = sqrt(pow(point_start.x - point_end.x, 2) + pow(point_start.y - point_end.y, 2) + pow(point_start.z - point_end.z, 2))
            center = Point((point_end.x + point_start.x) / 2, (point_end.y + point_start.y) / 2, (point_end.z + point_start.z) / 2)

            rotation = Vector().from_points(point_start, center)
            rotation: Vector
            rotation.normalize()

            ox_vector = Vector(1, 0, 0)
            angle_oz = degrees(acos(rotation.scalar_multiplication(ox_vector)))

            oz_vector = Vector(0, 0, 1)
            angle_oy = degrees(asin(rotation.scalar_multiplication(oz_vector)))

            rotation_vector = Vector(90, angle_oy, angle_oz)

            result = [0, 0, l, center, rotation_vector]

            return result

        result = []
        for i in range(n):
            res = calculate_muscle(points_start[i], points_end[i])
            res[0] = (dx1 + dx2) / 2
            res[1] = (dx1 + dx2) / 2

            result.append(res)

        return result

    def read_file(self):
        f = open(self.filename, 'r')

        params = []
        while 1:
            t = f.readline().strip('\n')
            if not t:
                break
            elif t == 'm':
                params.append(self.read_muscle(f))
            elif t == 's':
                params += self.read_spline(f)
            else:
                # TODO error
                print('Break', t)
                quit()

        f.close()

        return params

    def init_muscle(self, params):
        part = StraightMuscleModel(params[0], params[1], params[2], params[3], params[4])
        part.init_polygons()
        self.model.append(part)

    def init_model(self, parameteres_array):
        for parameteres in parameteres_array:
            self.init_muscle(parameteres)

        result = ComplexMuscleModel(self.model)
        return result

    def get_product(self):
        parameteres_array = self.read_file()

        return self.init_model(parameteres_array)
