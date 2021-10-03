# Classic Aspects

This package provides convenient utils for late decorating, based on idea of
aspects-oriented programming. Part of project "Classic".

Usage:

```python

from classic.aspects import PointCut

points = PointCut()


@points.join_point
def add_numbers(left, right):
    return left + right


assert add_numbers(1, 2) == 3  # Returns 3


def some_decorator(fn):
    
    def wrapper(*args, **kwargs):
        print('Function called!')
        return fn(*args, **kwargs)
    
    return wrapper


add_numbers.join(some_decorator)

assert add_numbers(1, 2) == 3  # Returns 3 and print "Function called!"
```

