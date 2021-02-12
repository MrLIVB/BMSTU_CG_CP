from scene import BaseScene

class BaseSceneManager(object):
    def __init__(self, scene:BaseScene):
        self.scene = scene

    def execute(self):
        pass