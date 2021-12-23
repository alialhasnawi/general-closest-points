import sys
import unittest
from hypothesis import given, settings, strategies as st

sys.path.append('../')

from general_closest_points.alg import closest_points
from general_closest_points._utils import _get_closest_iter
from generate_points import get_points

class TestClosest(unittest.TestCase):
    
    @given(
        st.integers(min_value=1, max_value=10),
        st.integers(min_value=1, max_value=300),
        st.floats(min_value=-100000, max_value=100000),
        st.floats(min_value=-100000, max_value=100000),
    )
    @settings(deadline=None)
    def test_arbitrary_accuracy(self, n: int, size: int, param1: float, param2: float):
        lower = min(param1, param2)
        upper = max(param1, param2)

        points = get_points(n, size, lower, upper)

        print(f'\n {size} points of dimension {n}: {points[:2]}...')

        self.assertEqual(
            set(_get_closest_iter(points)[0]),
            set(closest_points(points)),
        )

if __name__ == '__main__':
    unittest.main()