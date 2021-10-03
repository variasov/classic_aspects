from dataclasses import dataclass
from typing import List, Callable, Any
from functools import wraps


Decorator = Callable[..., Callable[..., Any]]
AnyFunction = Callable[..., Any]


@dataclass
class JoinPoint:
    function: AnyFunction

    def join(self, *decorators: Decorator):
        for decorator in decorators:
            self.function = decorator(self.function)
        
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    @classmethod
    def wrap(cls, function: AnyFunction) -> 'JoinPoint':
        join_point = cls(function)

        @wraps(function)
        def wrapper(*args, **kwargs):
            return join_point(*args, **kwargs)

        setattr(wrapper, 'function', function)
        setattr(wrapper, 'point', join_point)
        setattr(wrapper, 'join', join_point.join)

        return wrapper


class PointCut:

    def __init__(self):
        self._registry: List[JoinPoint] = []

    def join(self, *decorators: Decorator, exclude: List[JoinPoint] = None):
        exclude = exclude or []
        for point in self._registry:
            if point not in exclude:
                point.join(*decorators)

    def join_point(self, function: AnyFunction):
        wrapped = JoinPoint.wrap(function)
        self._registry.append(wrapped)
        return wrapped
