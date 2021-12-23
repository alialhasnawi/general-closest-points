from typing import List, Tuple, Union
from random import random

Point = Tuple[Union[float, int], ...]


def get_points(n: int, size: int, lower: float = -100, upper: float = 100) -> List[Point]:
    '''Create a list of points in Rn, of <size>, with entries ranging from
    <upper> to <lower>.'''
    points = []

    for _ in range(size):
        points.append(
            tuple([
                (upper - lower) * random() + lower
                for __ in range(n)
            ])
        )

    return points
