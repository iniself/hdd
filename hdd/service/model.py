from __future__ import absolute_import, division, print_function, unicode_literals
from ..interface.abs import ModelManagerAbs


class ModelFactory(ModelManagerAbs):
    def __init__(self, which):
        super().__init__()

    def load(self, which):
        print("mode")
        return self

    def input(self):
        pass

    def run(self):
        pass

    def output(self):
        pass
