from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtCore import Qt

class BaseDrawer(object):
    def drawLine(self, x1: float, y1: float, x2: float, y2: float, color):
        pass

    def drawPoint(self, x: float, y: float, color):
        pass

    def clear(self):
        pass

class QDrawer(BaseDrawer):
    def __init__(self, canvas: QImage):
        self.painter = QPainter(canvas)
        self.canvas = canvas

    def drawLine(self, x1: float, y1: float, x2: float, y2: float, color: QColor):
        self.painter.drawLine(x1, y1, x2, y2)

    def drawPoint(self, x: float, y: float, color: QColor):
        self.canvas.setPixelColor(x, y, color)

    def clear(self):
        self.canvas.fill(Qt.white)
