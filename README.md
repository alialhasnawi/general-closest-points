# fast-closest-points
Faster closest pair of points algorithm for Rn.

- Faster than the optimized iterative algorithm by 98% for a list of 500 points.
- Works for all dimensions (including R1).
- Uses a Minkowski distance function (`n -> -infinity`).


### Usage
```
from general_closest_points.alg import closest_points

# Points is a list of n-tuples.
# All tuples in points must be of the same dimension.
closest_points(points)

# Returns the pair of points as a tuple.
```


### Further future optimizations:
- Optimize storage use by partitioning the array in memory instead of slicing.
- Use a C binding for large inputs.
