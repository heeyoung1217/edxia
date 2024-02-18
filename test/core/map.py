from edxia.core.map import Map, MapsStack
from edxia.utils import coordinates as coord
import numpy as np

import unittest

class TestMap(unittest.TestCase):
    def setUp(self):
        self.mat = np.array([[1, 2, 3], [4, 5, 6]])
        self.map = Map("F", self.mat, None)

    def test_properties(self):
        self.assertEqual(self.map.component, "F")
        self.assertEqual(self.map.nb_rows, 2)
        self.assertEqual(self.map.nb_cols, 3)


    def test_access(self):
        self.assertEqual(self.mat[1,1], self.map[1,1])
        self.assertEqual(self.mat[0,2], self.map.rc(0,2))
        r,c = coord.xy_to_rc(self.mat, 2, 0)
        self.assertEqual(self.mat[r,c], self.map.xy(2,0))
        self.assertTrue((self.mat[:,2] == self.map[:,2]).all())

    def test_flat_map(self):
        self.assertTrue((self.map.flat_map == np.array([1,2,3,4,5,6])).all())

class TestMapStack(unittest.TestCase):
    def setUp(self):
        self.components = ["A", "B", "C"]
        self.mat_A = np.array([[1,1],[2,2]])
        self.mat_B = np.array([[2,2],[4,4]])
        self.mat_C = np.array([[3,3],[6,6]])

        self.map_A = Map("A", self.mat_A, None)
        self.map_B = Map("B", self.mat_B, None)
        self.map_C = Map("C", self.mat_C, None)

    def test_set(self):
        map_stack = MapsStack(self.components, (2,2), None)

        map_stack.set_map(self.map_B)
        map_stack.set_map(self.map_C)
        map_stack.set_map(self.map_A)

        self.assertDictEqual(map_stack.composition(0, 0), {"A":1, "B":2, "C":3})
        self.assertDictEqual(map_stack.composition(1, 0), {"A":2, "B":4, "C":6})

        self.assertEqual(map_stack.map("A")[1,1], 2)
        self.assertEqual(map_stack[1,1,1], 4)



if __name__ == '__main__':
    unittest.main()