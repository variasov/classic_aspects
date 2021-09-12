from dataclasses import dataclass, field
from typing import List, Callable, Any


Hook = Callable[..., None]
Wrappable = Callable[..., Any]


@dataclass
class JoinPoint:
    function: Wrappable
    functions_before: List[Hook] = field(default_factory=list)
    functions_after: List[Hook] = field(default_factory=list)
    functions_on_exception: List[Hook] = field(default_factory=list)

    def before(self, function: Hook):
        self.functions_before.append(function)

    def after(self, function: Hook):
        self.functions_after.append(function)

    def instead(self, function: Hook):
        self.function = self._wrap_function_instead(function)

    def on_exception(self, function: Hook):
        self.functions_on_exception.append(function)

    def _wrap_function_instead(self, function):
        def wrapper(*args, **kwargs):
            return function(self.function, *args, **kwargs)

        return wrapper

    def _call_before(self, *args, **kwargs):
        for function in self.functions_before:
            function(*args, **kwargs)

    def _call_after(self, *args, **kwargs):
        for function in self.functions_after:
            function(*args, **kwargs)

    def _call_on_exception(self, exception, *args, **kwargs):
        for function in self.functions_on_exception:
            function(exception, *args, **kwargs)
        
    def __call__(self, *args, **kwargs):
        try:
            self._call_before(*args, **kwargs)

            result = self.function(*args, **kwargs)

        except Exception as exception:
            self._call_on_exception(exception, *args, **kwargs)
            raise exception
        else:
            self._call_after(*args, **kwargs)

        return result

    @classmethod
    def wrap(cls, function: Wrappable) -> 'JoinPoint':
        join_point = cls(function)

        def wrapper(*args, **kwargs):
            return join_point(*args, **kwargs)

        setattr(wrapper, 'function', function)
        setattr(wrapper, 'point', join_point)
        setattr(wrapper, 'before', join_point.before)
        setattr(wrapper, 'after', join_point.after)
        setattr(wrapper, 'instead', join_point.instead)
        setattr(wrapper, 'on_exception', join_point.on_exception)

        return wrapper


@dataclass
class PointCut:
    registry: List[JoinPoint] = field(default_factory=list)

    def before(self, function: Hook):
        for aspect in self.registry:
            aspect.before(function)

    def after(self, function: Hook):
        for aspect in self.registry:
            aspect.after(function)

    def instead(self, function: Hook):
        for aspect in self.registry:
            aspect.instead(function)

    def on_exception(self, function: Hook):
        for aspect in self.registry:
            aspect.on_exception(function)

    def join_point(self, function):
        wrapped = JoinPoint.wrap(function)
        self.registry.append(wrapped)
        return wrapped

    def __call__(self, function):
        return self.join_point(function)
