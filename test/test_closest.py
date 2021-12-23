import unittest
import sys

sys.path.append('../')

from general_closest_points.alg import closest_points

class TestClosest(unittest.TestCase):

    def test_zero_2d(self):
        points = [(0, 0), (0, 0)]
        expected = ((0, 0), (0, 0))
        self.assertEqual(closest_points(points), expected)

    def test_zero_3d(self):
        points = [(0, 0, 0), (0, 0, 0)]
        expected = ((0, 0, 0), (0, 0, 0))
        self.assertEqual(closest_points(points), expected)

    def test_three_points_3d(self):
        points = [(0, 0, 0), (1, 1, 1), (0.1, 1, 0.1)]
        expected = set(((0, 0, 0), (0.1, 1, 0.1)))
        self.assertEqual(set(closest_points(points)), expected)

    def test_axis_dist_2d(self):
        points = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
        actual = closest_points(points)
        actual_dist = ((actual[0][0] - actual[1][0]) **
                       2 + (actual[0][1] - actual[1][1])) ** 0.5
        self.assertEqual(actual_dist, 1)


if __name__ == '__main__':
    unittest.main()
