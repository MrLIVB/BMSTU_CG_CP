from math import floor

from basescenemanager import *
from builddirector import BuildDirector
from musclemodel import Morph
from visibleobject import *
from visualizer import *


class LoadManager(BaseSceneManager):
    def __init__(self, scene: BaseScene, build_director: BuildDirector):
        super().__init__(scene)
        self.director = build_director

    def execute(self):
        if self.scene is None:
            print("No scene")

        self.scene.add_object(self.director.create())

class DrawManager(BaseSceneManager):
    def __init__(self, scene: BaseScene, draw_factory: BaseDrawerFactory):
        super().__init__(scene)
        self.drawerFactory = draw_factory

    def execute(self):
        visualizer = Visualizer()
        visualizer.setDrawer(self.drawerFactory)
        visualizer.setCamera(self.scene.get_camera())
        visualizer.clear()

        zbuf = ZBuffer(visualizer)

        lights = self.scene.get_lights()
        cam = self.scene.get_camera()

        for model in self.scene.get_model(0):
            process_polygons = [[polygon, True if polygon.get_normal().scalar_multiplication(cam.direction) > 0 else False] for polygon in model.polygons]

            for polygon in process_polygons:
                if polygon[1]:
                    zbuf.process_polygon(polygon[0], lights)

        for light in lights:
            zbuf.safe_process_point(light.x, light.y, light.z, 900, 900, Qt.blue)


class DrawAnimationManager(DrawManager):
    def __init__(self, scene: BaseScene, draw_factory: BaseDrawerFactory, frame):
        super().__init__(scene, draw_factory)
        self.frame = frame

    def execute(self):
        visualizer = Visualizer()
        visualizer.setDrawer(self.drawerFactory)
        visualizer.setCamera(self.scene.get_camera())
        visualizer.clear()

        zbuf = ZBuffer(visualizer)

        lights = self.scene.get_lights()
        cam = self.scene.get_camera()

        morph = self.scene.get_model(1)
        morph: Morph
        process_polygons = [[polygon, True if polygon.get_normal().scalar_multiplication(cam.direction) > 0 else False] for polygon in morph.get_frame(self.frame)]

        for polygon in process_polygons:
            if polygon[1]:
                zbuf.process_polygon(polygon[0], lights)

class ZBuffer(object):
    def __init__(self, visualizer: Visualizer, width=900, height=900):
        self.width = width
        self.height = height
        self.visualizer = visualizer
        self._buf = [[-6000 for _ in range(width)] for __ in range(height)]

    def process_polygon(self, polygon: Polygon, light):
        color = polygon.get_color(light)

        points = polygon.get_points()
        x = [floor(points[i].x) for i in range(3)]
        y = [floor(points[i].y) for i in range(3)]

        ymax = max(y)
        ymin = min(y)

        ymax = ymax if ymax < self.height else self.height
        ymin = 0 if ymin < 0 else ymin

        x1 = x2 = 0
        z1 = z2 = 0
        for y_current in range(ymin, ymax+1):
            first_cycle = 1
            for n in range(3):
                n1 = 0 if n == 2 else n + 1
                if y_current >= max(y[n], y[n1]) or y_current < min(y[n], y[n1]):
                    # Точка вне
                    continue

                m = float(y[n] - y_current) / (y[n]-y[n1])
                if first_cycle == 0:
                    x2 = x[n] + floor(m * (x[n1] - x[n]))
                    z2 = points[n].z + m * (points[n1].z - points[n].z)
                else:
                    x1 = x[n] + floor(m * (x[n1] - x[n]))
                    z1 = points[n].z + m * (points[n1].z - points[n].z)

                first_cycle = 0

            if x2 < x1:
                x2, x1 = x1, x2
                z2, z1 = z1, z2

            x_start = 0 if x1 < 0 else x1
            x_end = x2 if x2 < self.width else self.width
            for x_current in range(x_start, x_end):
                m = float(x1 - x_current) / (x1 - x2)
                z_current = z1 + m * (z2 - z1)
                self.process_point(x_current, y_current, int(z_current), color)

    def process_point(self, x: int, y: int, z: int, color):
        if z > self._buf[x][y]:
            self._buf[x][y] = z
            self.visualizer.drawPoint(x, y, color)

    def safe_process_point(self, x: int, y: int, z: int, width: int, height: int, color):
        if x < 0 or x >= width or y < 0 or y >= height:
            return
        elif z > self._buf[x][y]:
            self._buf[x][y] = z
            self.visualizer.drawWidePoint(x, y, color)
