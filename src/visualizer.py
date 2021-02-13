from drawerFactory import *
from invisibleobject import Camera

class Visualizer(object):
    def __init__(self):
        self.drawer = None
        self.camera = None

    def setDrawer(self, factory: BaseDrawerFactory):
        self.drawer = factory.create()

    def setCamera(self, camera: Camera):
        self.camera = camera

    def drawLine(self, x1: float, y1: float, x2: float, y2: float, color):
        self.drawer.drawLine(x1, y1, x2, y2, color)

    def drawPoint(self, x: float, y: float, color):
        self.drawer.drawPoint(x, y, color)

    def drawWidePoint(self, x: float, y: float, color):
        self.drawer.drawPoint(x - 1, y - 1, color)
        self.drawer.drawPoint(x + 1, y - 1, color)
        self.drawer.drawPoint(x - 1, y + 1, color)
        self.drawer.drawPoint(x + 1, y + 1, color)
        self.drawer.drawPoint(x, y + 1, color)
        self.drawer.drawPoint(x, y - 1, color)
        self.drawer.drawPoint(x + 1, y, color)
        self.drawer.drawPoint(x - 1, y, color)

    def clear(self):
        self.drawer.clear()
