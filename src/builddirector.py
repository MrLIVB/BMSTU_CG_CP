from builder import ModelBuilder

class BuildDirector(object):
    def __init__(self, builder: ModelBuilder):
        self.builder = builder

    def create(self):
        product = self.builder.get_product()
        return product
