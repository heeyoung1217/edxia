from edxia.utils import coordinates
import numpy as np

import unittest


class TestPath(unittest.TestCase):
    def setUp(self):
        self.mat = np.array([[1, 2], [3, 4]])

    def test_xy_from_rc(self):
        x, y = coordinates.rc_to_xy(self.mat, 1, 1)
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)

        x, y = coordinates.rc_to_xy(self.mat, 0, 0)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)


    def test_rc_from_xy(self):
        r, c = coordinates.xy_to_rc(self.mat, 1, 1)
        self.assertEqual(r, 0)
        self.assertEqual(c, 1)

        r, c = coordinates.xy_to_rc(self.mat, 0, 0)
        self.assertEqual(r, 1)
        self.assertEqual(c, 0)

    def test_access_from_xy(self):
        r,c = coordinates.xy_to_rc(self.mat, 1, 0)
        self.assertEqual(self.mat[r, c], 4)
        r,c = coordinates.xy_to_rc(self.mat, 0, 1)
        self.assertEqual(self.mat[r, c], 1)


if __name__ == '__main__':
    unittest.main()