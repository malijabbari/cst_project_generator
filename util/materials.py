import util.constants as constants
import random
from typing import List


class Materials:
    materials_available = constants.Materials

    def __init__(self, n: int):
        """
        Generate <n> different materials, based on materials defined in
        util.constants.Materials
        """
        ids = random.sample(range(0, len(constants.Materials)), n)
        materials = []
        for idx in ids:
            materials.append(constants.Materials[idx])
        self.materials = materials
        self.n = n

    def _make_array(self, property_name: str) -> List:
        array = []
        for material in self.materials:
            array.append(getattr(material, property_name))
        return array

    def _make_string(self, property_name: str) -> str:
        s = ''
        array = self._make_array(property_name)
        for idx, elem in enumerate(array):
            # add comma to string, except for the first element
            if idx is not 0:
                s += ','
            # convert to string if number
            if isinstance(elem, (float, int)):
                elem = '%.2f' % elem
            # add element to string
            s += '"%s"' % elem
        return s

    def names(self):
        return self._make_string('name')

    def object_names(self):
        return self._make_string('object_name')

    def permittivities(self):
        return self._make_string('permittivity')

    def densities(self):
        return self._make_string('density')

    def conductivities(self):
        return self._make_string('conductivity')

    def reds(self):
        return self._make_string('red')

    def greens(self):
        return self._make_string('green')

    def blues(self):
        return self._make_string('blue')
