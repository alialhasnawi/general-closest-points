from typing import List, Tuple, Union

from general_closest_points import _utils

PointRn = Tuple[Union[float, int], ...]


def closest_points(points: List[PointRn]) -> Tuple[PointRn, PointRn]:
    '''
    Return the closest pair of points in the list as a tuple (p1, p2).

    Precondition:
        - There are at least 2 points in the list.
        - All points in the list are tuples in the same dimension.
    '''
    return _utils._closest_recur(points)[0]