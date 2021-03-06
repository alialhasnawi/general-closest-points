# general-closest-points
Closest pair of points algorithm for all Rn.

- Faster than the optimized iterative algorithm by 98% for a list of 500 points.
- Works for all dimensions (including R1).
- Uses a Minkowski distance function (`n -> -infinity`).


### Usage
```python
from general_closest_points.alg import closest_points

points = [
  (1, 2),
  (-1, 3),
  (2, 2)
]

closest_points(points)
# > ((1, 2), (2, 2))
```


### Further future optimizations:
- Optimize storage use by partitioning the array in memory instead of slicing.
- Use a C binding for large inputs.
