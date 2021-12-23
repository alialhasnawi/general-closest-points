import sys
import time

sys.path.append('../')

import general_closest_points._utils
from generate_points import get_points
from general_closest_points.alg import PointRn, closest_points
import reference_alg

reset = {'euclid_counter': 0, 'goofy_counter': 0}
result = reset.copy()


def _counted_euclid_distance(p1: PointRn, p2: PointRn) -> float:
    '''
    Return the Euclidean distance between two points.
    '''
    result['euclid_counter'] += 1

    total = 0
    for i in range(len(p1)):
        total += (p1[i] - p2[i]) ** 2

    return total ** 0.5


def _counted_minkowski_distance(p1: PointRn, p2: PointRn) -> float:
    '''
    Return the cross-shaped distance between two points.

    Try it on desmos ! https://www.desmos.com/calculator/2qddnq2raq
    '''
    result['goofy_counter'] += 1
    ret = float('inf')
    for i in range(len(p1)):
        ret = min(ret, abs(p1[i]-p2[i]))

    return ret

reference_alg._euclid_distance = _counted_euclid_distance
general_closest_points._utils._euclid_distance = _counted_euclid_distance
general_closest_points._utils._minkowski_distance = _counted_minkowski_distance

N = 2
SIZE = 1000
LOWER = -100
UPPER = 100

points = get_points(N, SIZE, LOWER, UPPER)

with open('latest_run.txt', mode='w') as f:
    print("\nOwn Implementation:", file=f)
    result = reset.copy()

    start = time.perf_counter_ns()
    actual = closest_points(points)
    actual_time = round((time.perf_counter_ns() - start) / 1e6, 3)

    print(
        f"{result['euclid_counter']} euclidean distance calls + {result['goofy_counter']} other distance calls = {result['euclid_counter']+result['goofy_counter']} total calls.",
        file=f
        )
    print('(other distance calls only use abs and subtraction, Minkowski p-> -infinity)', file=f)
    print(f"Took {actual_time}ms.", file=f)

    print("\nNormal Implementation (with extra pair checks removed)", file=f)
    result = reset.copy()
    
    start = time.perf_counter_ns()
    expected = general_closest_points._utils._get_closest_iter(points)[0]
    expected_time = round((time.perf_counter_ns() - start) / 1e6, 3)
    
    print(
        f"{result['euclid_counter']} euclidean distance calls.",
        file=f
    )
    print(f"Took {expected_time}ms.", file=f)


    # Only for n=2.
    if N == 2:
        print("\nGeneric Implementation (uses built-in sorting, but only works for R2)", file=f)
        result = reset.copy()

        start = time.perf_counter_ns()
        standard = reference_alg.closest(points)
        standard_time = round((time.perf_counter_ns() - start) / 1e6, 3)

        print(
            f"{result['euclid_counter']} euclidean distance calls.",
            file=f
        )
        print(f"Took {standard_time}ms.", file=f)