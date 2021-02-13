class BaseScene(object):
    def __init__(self):
        self.objects = []
        self.ligths = []
        self.cams = []
        self.curCam = 0

    def set_camera(self, camera_index):
        pass

    def add_object(self, smt):
        pass

    def add_camera(self, smt):
        pass

    def add_light(self, index):
        pass

    def get_light(self, index):
        pass

    def get_lights(self):
        pass

    def get_camera(self):
        pass

    def get_models(self):
        pass

    def get_model(self, index):
        pass

    def remove_model(self, index):
        pass

    def remove_light(self, index):
        pass

    def remove_camera(self, index):
        pass

class Scene(BaseScene):
    def __init__(self):
        super().__init__()

    def add_object(self, smt):
        self.objects.append(smt)

    def add_camera(self, smt):
        self.cams.append(smt)

    def add_light(self, smt):
        self.ligths.append(smt)

    def set_camera(self, camera_index):
        self.curCam = camera_index

    def get_camera(self):
        return self.cams[self.curCam]

    def get_light(self, index):
        return self.ligths[index]

    def get_lights(self):
        return self.ligths

    def get_models(self):
        return self.objects

    def get_model(self, index):
        return self.objects[index]

    def remove_model(self, index):
        self.objects.pop(index)

    def remove_camera(self, index):
        self.cams.pop(index)

    def remove_light(self, index):
        self.ligths.pop(index)

