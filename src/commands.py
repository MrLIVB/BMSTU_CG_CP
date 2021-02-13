from builder import ModelBuilder
from managers import *
from musclemodel import Morph, ComplexMuscleModel
from visitor import RotateVisitor, MoveVisitor

class BaseCommand(object):
    def execute(self, scene):
        pass

class LoadCommand(BaseCommand):
    def __init__(self, filename):
        self.filename = filename
    
    def execute(self, scene: BaseScene):
        builder = ModelBuilder(self.filename)
        director = BuildDirector(builder)
        manager = LoadManager(scene, director)

        manager.execute()


class DrawCommand(BaseCommand):
    def __init__(self):
        self.factory = None

    def execute(self, scene: BaseScene):
        DrawManager(scene, self.factory).execute()

class QDrawCommand(DrawCommand):
    def __init__(self, canvas: QImage):
        super().__init__()
        self.factory = QDrawerFactory(canvas)

class QDrawAnimationCommand(DrawCommand):
    def __init__(self, canvas: QImage):
        super().__init__()
        self.factory = QDrawerFactory(canvas)
        self.frame = 0

    def set_frame(self, frame):
        self.frame = frame

    def execute(self, scene: BaseScene):
        DrawAnimationManager(scene, self.factory, self.frame).execute()

class AddCommand(BaseCommand):
    def __init__(self, adding):
        self.adding = adding

class AddCameraCommand(AddCommand):
    def __init__(self, adding):
        super().__init__(adding)

    def execute(self, scene):
        scene.add_camera(self.adding)

class AddLightCommand(AddCommand):
    def __init__(self, adding):
        super().__init__(adding)

    def execute(self, scene):
        scene.add_light(self.adding)

class TransformCommand(BaseCommand):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class MoveCommand(TransformCommand):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

class MoveLightCommand(MoveCommand):
    def __init__(self, x, y, z, light_index):
        super().__init__(x, y, z)
        self.light_index = light_index

    def execute(self, scene):
        light = scene.get_light(self.light_index)
        visitor = MoveVisitor(self.x, self.y, self.z)
        light.accept(visitor)

class MoveModelCommand(MoveCommand):
    def __init__(self, x, y, z, index):
        super().__init__(x, y, z)
        self.index = index

    def execute(self, scene):
        model = scene.get_model(self.index)
        visitor = MoveVisitor(self.x, self.y, self.z)
        model.accept(visitor)

class RotateCommand(TransformCommand):
    def __init__(self, x, y, z, center_x=0, center_y=0, center_z=0):
        super().__init__(x, y, z)
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z

    def execute(self, scene):
        pass

class RotateModelCommand(RotateCommand):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    def execute(self, scene):
        model = scene.get_model(0)
        visitor = RotateVisitor(self.x, self.y, self.z)
        model.accept(visitor)

class AnimateCommand(BaseCommand):
    def __init__(self, parameter, contraction, frames=30):
        self.frames = frames
        self.parameter = parameter
        self.contraction = contraction

    def execute(self, scene):
        model = scene.get_model(0)
        model: ComplexMuscleModel
        a = model.get_polygons()
        model.contract(self.parameter, self.contraction)

        if len(scene.get_models()) == 2:
            scene.remove_model(1)

        morph = Morph(a, model.get_polygons(), self.frames)

        scene.add_object(morph)
