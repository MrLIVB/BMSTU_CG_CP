import sys

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *

from controlcommand import *
from invisibleobject import LightSource, Camera
from sceneinterface import SceneInterface


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('mainwindow.ui', self)  # Load the .ui file
        self.show()  # Show the GUI
        self.pixmap = QtGui.QPixmap(900, 900)
        self.pixmap.fill(QtCore.Qt.white)
        self.graphics_scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.graphics_scene)

        self.sceneInterface = SceneInterface()

        add = AddLightCommand(LightSource(0, 0, 0, 0.5))
        self.sceneInterface.execute(add)
        add = AddCameraCommand(Camera(450, 450, 5000, Vector(0, 0, -1)))
        self.sceneInterface.execute(add)

        self.lightNumberSpinBox.setMaximum(len(self.sceneInterface.scene.get_lights()))

        self.connect_buttons()

    def connect_buttons(self):
        # кнопки движения модели
        self.movelButton.clicked.connect(lambda: self.move_model(-100, 0, 0))
        self.moverButton.clicked.connect(lambda: self.move_model( 100, 0, 0))
        self.moveuButton.clicked.connect(lambda: self.move_model(0, -100, 0))
        self.movedButton.clicked.connect(lambda: self.move_model(0,  100, 0))

        # кнопки поворота
        self.rotatelButton.clicked.connect(lambda: self.rotate(0, -10, 0))
        self.rotaterButton.clicked.connect(lambda: self.rotate(0,  10, 0))
        self.rotateuButton.clicked.connect(lambda: self.rotate(-10, 0, 0))
        self.rotatedButton.clicked.connect(lambda: self.rotate( 10, 0, 0))
        # self.rotateuButton.clicked.connect(lambda: self.rotate(0, 0, -10))
        # self.rotatedButton.clicked.connect(lambda: self.rotate(0, 0, 10))

        # конпки движения света
        self.movelButton_2.clicked.connect(lambda: self.move_light(-100, 0, 0))
        self.moverButton_2.clicked.connect(lambda: self.move_light(100, 0, 0))
        self.moveuButton_2.clicked.connect(lambda: self.move_light(0, -100, 0))
        self.movedButton_2.clicked.connect(lambda: self.move_light(0, 100, 0))
        self.movecButton_2.clicked.connect(lambda: self.move_light(0, 0, 100))
        self.movefButton_2.clicked.connect(lambda: self.move_light(0, 0, -100))

        self.addLightButton.clicked.connect(self.add_light)

        self.loadButton.clicked.connect(self.load)

        self.animationButton.clicked.connect(self.animate)

    def load(self):
        filename_dlg = QFileDialog(self, 'Загрузить модель', sys.argv[0], "Text file (*.txt)")
        filename_dlg.exec_()

        if not len(filename_dlg.selectedFiles()):
            return

        command = LoadCommand(filename_dlg.selectedFiles()[0])
        self.sceneInterface.execute(command)

        self.send_draw_command()

    def send_draw_command(self):
        canvas = QImage(900, 900, QImage.Format_ARGB32)
        canvas.fill(QtCore.Qt.white)
        draw = QDrawCommand(canvas)
        self.sceneInterface.execute(draw)

        self.graphics_scene.addPixmap(self.pixmap.fromImage(canvas))

    def send_draw_animation_command(self, frames):
        canvas = QImage(900, 900, QImage.Format_ARGB32)
        canvas.fill(QtCore.Qt.white)
        draw = QDrawAnimationCommand(canvas)

        for i in range(frames):
            self.update()

            QApplication.processEvents()

            canvas.fill(QtCore.Qt.white)
            draw.set_frame(i)
            self.sceneInterface.execute(draw)
            self.graphics_scene.addPixmap(self.pixmap.fromImage(canvas))

    def animate(self):
        frames = self.framesSpinBox.value()

        new_length = self.newLengthSpinBox.value()
        animate_command = AnimateCommand(new_length, frames)
        self.sceneInterface.execute(animate_command)

        self.send_draw_animation_command(frames)

    def move_model(self, x, y, z):
        command = MoveModelCommand(x, y, z, 0)
        self.sceneInterface.execute(command)
        self.send_draw_command()

    def move_light(self, x, y, z):
        number = self.lightNumberSpinBox.value() - 1
        command = MoveLightCommand(x, y, z, number)
        self.sceneInterface.execute(command)
        self.send_draw_command()

    def add_light(self):
        x = self.xSpinBox.value()
        y = self.ySpinBox.value()
        z = self.zSpinBox.value()
        intensity = self.intensitySpinBox.value()

        command = AddLightCommand(LightSource(x, y, z, intensity))

        self.sceneInterface.execute(command)

        self.lightNumberSpinBox.setMaximum(self.lightNumberSpinBox.maximum() + 1)
        self.send_draw_command()

    def rotate(self, x, y, z):
        command = RotateModelCommand(x, y, z)
        self.sceneInterface.execute(command)
        self.send_draw_command()