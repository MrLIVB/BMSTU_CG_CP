from drawer import *

class BaseDrawerFactory(object):
    def create(self):
        pass

class QDrawerFactory(BaseDrawerFactory):
    def __init__(self, canvas: QImage):
        self.canvas = canvas

    def create(self):
        return QDrawer(self.canvas)
