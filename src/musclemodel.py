from math import sqrt, pi

from PyQt5.QtCore import Qt

from baseobject import BaseObject, Point, Vector
from visibleobject import Polygon
from visitor import MoveVisitor, RotateVisitor

class Ellipsoid(object):
    def __init__(self):
        x = 1
        z = 1
        y = 1

        self.vertex_list = [
            [-x, -y, -z], [x, -y, -z], [x, -y, z], [-x, -y, z],
            [-x, y, -z], [x, y, -z], [x, y, z], [-x, y, z]
        ]

        self.triangle_list = [
            [0, 2, 1], [0, 3, 2], [1, 5, 0], [5, 4, 0], [0, 4, 7], [7, 3, 0],
            [6, 5, 1], [1, 2, 6], [7, 2, 3], [7, 6, 2], [4, 5, 6], [6, 7, 4]
        ]

        self.result_ind = []
        self.result_vertexes = []

    @staticmethod
    def normalize(v):
        d = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
        if d == 0.0:
            print("zero division")
        v[0] /= d
        v[1] /= d
        v[2] /= d

    def start_division(self, d):
        self.result_ind = []
        self.result_vertexes = []
        for i in range(12):
            self.rec_subdivide(self.vertex_list[self.triangle_list[i][0]],
                               self.vertex_list[self.triangle_list[i][1]],
                               self.vertex_list[self.triangle_list[i][2]], d)

        for vertex in self.result_vertexes:
            self.normalize(vertex)

    def rec_subdivide(self, v1, v2, v3, d):
        v12 = [0, 0, 0]
        v23 = [0, 0, 0]
        v31 = [0, 0, 0]

        if d == 0:
            if v1 not in self.result_vertexes:
                self.result_vertexes.append(v1)
            if v2 not in self.result_vertexes:
                self.result_vertexes.append(v2)
            if v3 not in self.result_vertexes:
                self.result_vertexes.append(v3)
            t = [0, 0, 0]
            t[0] = self.result_vertexes.index(v1)
            t[1] = self.result_vertexes.index(v2)
            t[2] = self.result_vertexes.index(v3)

            self.result_ind.append(t)
            return

        for i in range(3):
            v12[i] = (v1[i] + v2[i]) / 2
            v23[i] = (v2[i] + v3[i]) / 2
            v31[i] = (v3[i] + v1[i]) / 2

        self.rec_subdivide(v1, v12, v31, d - 1)
        self.rec_subdivide(v2, v23, v12, d - 1)
        self.rec_subdivide(v3, v31, v23, d - 1)
        self.rec_subdivide(v12, v23, v31, d - 1)

    def reshape(self, x, y, z):
        for vertex in self.result_vertexes:
            vertex[0] *= x
            vertex[1] *= y
            vertex[2] *= z

    def polygonise(self, center_x=0, center_y=0, center_z=0):
        polygons = []
        for triangle in self.result_ind:
            p1 = Point(self.result_vertexes[triangle[0]][0] + center_x, self.result_vertexes[triangle[0]][1] + center_y, self.result_vertexes[triangle[0]][2] + center_z)
            p2 = Point(self.result_vertexes[triangle[1]][0] + center_x, self.result_vertexes[triangle[1]][1] + center_y, self.result_vertexes[triangle[1]][2] + center_z)
            p3 = Point(self.result_vertexes[triangle[2]][0] + center_x, self.result_vertexes[triangle[2]][1] + center_y, self.result_vertexes[triangle[2]][2] + center_z)
            polygons.append(Polygon(p1, p2, p3))
        return polygons

# r - соотношение между a и b,
# l - может быть задана расстоянием между точками начала и конца
class StraightMuscleModel(BaseObject):
    def __init__(self, a, b, l, center: Point = Point(0, 0, 0), rotation: Point = Point(0, 0, 0)):
        self.a_base = a
        self.b_base = b
        self.l_base = l

        self.a_current = a
        self.b_current = b
        self.l_current = l

        self.center = center

        self.rotation_ox = rotation.x
        self.rotation_oy = rotation.y
        self.rotation_oz = rotation.z

        self.polygons = None

    def init_polygons(self):
        self.polygons = self.triangulate()
        self.colorize(Qt.red)
        return self.polygons

    def get_polygons(self):
        return self.polygons

    def triangulate(self):
        # возвращает множество своих полигонов расчитанных в соответствии с парамтерами
        temp_sphere = Ellipsoid()
        temp_sphere.start_division(4)
        temp_sphere.reshape(self.l_current / 2, self.a_current, self.b_current)

        polygons = temp_sphere.polygonise(self.center.x, self.center.y, self.center.z)

        # TODO для корреткного отображения необходимо сохранять последовательность поворотов

        rotation = RotateVisitor(self.rotation_ox, self.rotation_oy, self.rotation_oz, self.center)
        for polygon in polygons:
            polygon.accept(rotation)

        return polygons

    def contract(self, parameter, contraction):
        r = self.a_base / self.b_base
        volume = 4 * pi * self.a_base * self.b_base * self.l_base / 2 / 3
        tension = 0
        l_new = self.l_base

        if contraction == 0:  # Изотоническое сокращение - мышца меняет длину
            l_new = self.l_base * parameter
        elif contraction == 1:  # Изометрическое сокращение - длина не меняется
            tension = parameter

        k = 1.28  # параметр, регулирующий влияние "напряженности" на новое соотношение r, в статье рекомендуется 2.56
        r_new = (1 - tension + k * tension) * r
        b_new = sqrt(3 * volume / (4 * pi * r_new * (l_new / 2)))

        self.a_current = b_new * r_new
        self.b_current = b_new
        self.l_current = l_new

        self.init_polygons()
        return self.a_current, self.b_current, self.l_current

    def reset(self):
        self.a_current = self.a_base
        self.b_current = self.b_base
        self.l_current = self.l_base

        self.init_polygons()

    def accept(self, visitor):
        if type(visitor) is MoveVisitor:
            self.center.accept(visitor)

        for i in range(len(self.polygons)):
            self.polygons[i].accept(visitor)

    def colorize(self, color):
        for i in range(len(self.polygons)):
            self.polygons[i].color = color

class ComplexMuscleModel(BaseObject, list):
    def __init__(self, parts=None):
        super().__init__()
        if parts is None:
            parts = []
        self.parts = parts
        self.center = Point(0, 0, 0)
        self.calculate_center()

    def __iter__(self):
        return iter(self.parts)

    def __len__(self):
        return len(self.parts)

    def calculate_center(self):
        for part in self.parts:
            part: StraightMuscleModel
            self.center = self.center + part.center

        self.center.divide_number(len(self.parts))

    def contract(self, l_new, contraction):
        for part in self.parts:
            part: StraightMuscleModel
            part.contract(l_new, contraction)

    def get_polygons(self):
        res = []
        for part in self.parts:
            part: StraightMuscleModel
            res += part.get_polygons()

        return res

    def accept(self, visitor):
        if type(visitor) is MoveVisitor:
            self.center.accept(visitor)
        elif type(visitor) is RotateVisitor:
            visitor: RotateVisitor
            visitor.center_x = self.center.x
            visitor.center_y = self.center.y
            visitor.center_z = self.center.z

        for i in range(len(self.parts)):
            self.parts[i].accept(visitor)

class Morph(BaseObject):
    def __init__(self, begin, end, frames=30):
        self.begin = begin
        self.end = end
        self.paths = []  # массив троек веткоров, отражающих путь, который необходимо пройти
        self.pairs = []  # массив формата [0, [0,0], 0]: первое - индекс начала, третье - индекс конца, в середине - расстояние и перестановка

        self.frames = frames

        self.straight_map()
        self.calculate_paths()

    def straight_map(self):
        number = len(self.begin)
        self.pairs = [[i, i, 0] for i in range(number)]
        return self.pairs

    # алгоритм, сопостоставляющий каждому полигону из начала ближайший полигон из конца,
    # проблема в том, что он не всегда выбирает подходящий полигон, в связи с чем нарушается
    # целостность объекта - в промежуточных состояних полигон
    def map_polygons(self):
        # [0, [0,0], 0] - первое - индекс начала, третье - индекс конца, в середине - расстояние и перестановка
        number = len(self.begin)

        def calculate_distance(polygon1: Polygon, polygon2: Polygon):
            points_begin = polygon1.get_points()
            points_end = polygon2.get_points()

            def square_distance(point_from, point_to):
                distance = pow((point_to.x - point_from.x), 2) + pow((point_to.y - point_from.y), 2) + pow((point_to.z - point_from.z), 2)
                return distance

            permutations = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
            min_d = square_distance(points_begin[0], points_end[0]) + square_distance(points_begin[1], points_end[1]) + square_distance(points_begin[2], points_end[2])
            permutation = 0
            for i in range(1, 3):
                d = square_distance(points_begin[0], points_end[permutations[i][0]]) + \
                    square_distance(points_begin[1], points_end[permutations[i][1]]) + \
                    square_distance(points_begin[2], points_end[permutations[i][2]])

                if d < min_d:
                    min_d = d
                    permutation = i

            return [min_d, permutation]

        all_pairs = [[i // number, [0, 0], i % number] for i in range(number * number)]  # инициалзируем множество всех возможных дистанций
        for i in range(len(all_pairs)):
            all_pairs[i][1] = calculate_distance(self.begin[all_pairs[i][0]], self.end[all_pairs[i][2]])

        all_pairs.sort(key=lambda x: x[1][0])

        is_free_begin = [[i, True] for i in range(number)]
        is_free_end = [[i, True] for i in range(number)]
        for pair in all_pairs:
            if is_free_begin[pair[0]] and is_free_end[pair[2]]:
                self.pairs.append([pair[0], pair[2], pair[1][1]])
                is_free_begin[pair[0]] = False
                is_free_end[pair[2]] = False
            if len(self.pairs) == number:
                break

        self.pairs.sort(key=lambda x: x[0])

        return self.pairs

    def calculate_paths(self):
        for pair in self.pairs:
            p1 = self.begin[pair[0]].get_points()
            p2 = self.end[pair[1]].get_points()
            v3 = []
            for i in range(3):
                v = Vector()
                v.from_points(p1[i], p2[i])
                v3.append(v)

            self.paths.append(v3)

        return self.paths

    # Возвращает массив полигонов
    def get_frame(self, frame_number):
        number = len(self.begin)
        result = []  # Массив полигонов

        for i in range(number):
            points = self.begin[self.pairs[i][0]].get_points()
            for p in range(3):  # цикл по точкам
                points[p] = points[p] + self.paths[self.pairs[i][0]][p].number_multiplication(frame_number) / self.frames
            result.append(Polygon(points[0], points[1], points[2], self.begin[self.pairs[i][0]].color))

        return result
