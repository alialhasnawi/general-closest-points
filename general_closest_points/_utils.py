from typing import Dict, List, Tuple, Union


_MINIMUM_POINTS_DEPTH = 8
# Reduces FPA errors.
_DISTANCE_SEARCH_SCALAR = 0.51
_MAX_SAMPLE_SIZE = 5

PointRn = Tuple[Union[float, int], ...]


def _euclid_distance(p1: PointRn, p2: PointRn) -> float:
    '''
    Return the Euclidean distance between two points.
    '''
    total = 0
    for i in range(len(p1)):
        total += (p1[i] - p2[i]) ** 2

    return total ** 0.5


def _minkowski_distance(p1: PointRn, p2: PointRn) -> float:
    '''
    Return the cross-shaped distance between two points.
    '''

    # Minkowski distance with p -> -infinity
    ret = float('inf')
    for i in range(len(p1)):
        ret = min(ret, abs(p1[i]-p2[i]))

    return ret


def _get_closest_iter(points: List[PointRn]) -> Tuple[Tuple[PointRn, PointRn], float]:
    '''
    Return a tuple of the form ((p1, p2), distance),
    containing the distance between the closest pair of points,
    naively.
    '''

    closest = (None, None)
    dist = float('inf')

    for i in range(len(points)):
        # Only check after i to cut checks in half.
        for j in range(i+1, len(points)):
            if i != j:
                pair_dist = _euclid_distance(points[i], points[j])
                if pair_dist < dist:
                    closest = (points[i], points[j])
                    dist = pair_dist

    return closest, dist


def _partition_space(points: List[PointRn]) -> Tuple[Dict[str, List[PointRn]], PointRn]:
    '''
    Partition the points into 2^n spaces around an arbitrary point.
    The space between the partitions are all orthogonal and intersect
    at the point.

    Return that point and a dictionary of the partitions.
    '''

    centre = points[len(points) // 2]

    # Take average of first few points.
    sample_size = min(len(points), _MAX_SAMPLE_SIZE)
    centre = tuple(
        (sum(points[j][i] for j in range(sample_size)))/sample_size
        for i in range(len(points[0]))
    )

    partitions: Dict[str, List[PointRn]] = {}

    for point in points:
        # Each entry in the tuple is greater than or not to its corresponding
        # central entry. This can be used to create unique keys for the partition.
        key = ''
        for i in range(len(point)):
            key += '1' if point[i] > centre[i] else '0'

        partitions.setdefault(key, [])
        partitions[key].append(point)

    return partitions, centre


def _get_cross(points: List[PointRn], centre: PointRn, d: float) -> List[PointRn]:
    '''
    Return a list of all points which have a "distance" <= d
    from the centre.
    '''
    cross = []

    for point in points:
        if _minkowski_distance(point, centre) <= d:
            cross.append(point)

    return cross


def _closest_recur(points: List[PointRn]) -> Tuple[Tuple[PointRn, PointRn], float]:
    '''
    Return a tuple of the form ((p1, p2), distance),
    containing the distance between the closest pair of points.

    Return ((None, None), float('inf')) if no such pair is possible.
    '''
    # Base case.
    if len(points) <= 1:
        return ((None, None), float('inf'))
    elif len(points) < _MINIMUM_POINTS_DEPTH:
        return _get_closest_iter(points)

    # Partition the space.
    partitions, centre = _partition_space(points)

    # Find the best result.
    partition_results = []
    for partition in partitions.values():
        # Bad partition due to non distinct points case.
        # Exit to prevent hitting the recursion limit.
        if len(partition) == len(points):
            return _get_closest_iter(points)

        partition_results.append(_closest_recur(partition))

    # Get the minimum distance of all the partitions.
    best_partition_result = ((None, None), float('inf'))

    for result in partition_results:
        if result[1] < best_partition_result[1]:
            best_partition_result = result

    # Compute the distances of all the points in the in between space.
    cross_result = _get_closest_iter(_get_cross(points,
                                                centre,
                                                best_partition_result[1] * _DISTANCE_SEARCH_SCALAR))

    # Best case: bT(n/b) + n    O(nlogn) with 0 points in the cross.
    # Worst case:               O(n^2) with all items in partition.
    #                           but worse than naive due to extra checks.
    # Average:                  O(nlogn) assuming uniform point distribution.

    # Runtime for R^k: T(n) ~ [2^k]*T(n / [2^k]) + n

    if cross_result[1] > best_partition_result[1]:
        return best_partition_result
    else:
        return cross_result
