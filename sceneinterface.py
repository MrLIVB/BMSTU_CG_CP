from scene import Scene
from basecommand import BaseCommand

class SceneInterface(object):
    def __init__(self):
        self.scene = Scene()

    def execute(self, command: BaseCommand):
        command.execute(self.scene)