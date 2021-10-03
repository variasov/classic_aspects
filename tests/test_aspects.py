import pytest

from classic.aspects import PointCut


@pytest.fixture
def points():
    return PointCut()


@pytest.fixture
def some_cls(points):

    class SomeCls:

        @points.join_point
        def some_method(self, some_arg, some_kwarg=None):
            return some_arg, some_kwarg

    return SomeCls


@pytest.fixture
def some_function(points):

    @points.join_point
    def function(some_arg, some_kwarg=None):
        return some_arg, some_kwarg

    return function


@pytest.fixture
def advice():

    def decorator(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs), 'ADDITIONAL'
        return wrapper

    return decorator


def test_cls_method_call(some_cls):
    instance = some_cls()

    results = instance.some_method(1, some_kwarg=2)

    assert results == (1, 2)


def test_cls_method_call_with_advice(some_cls, advice):
    some_cls.some_method.join(advice)

    service = some_cls()
    results = service.some_method(1, some_kwarg=2)

    assert results == ((1, 2), 'ADDITIONAL')


def test_func_call(some_function):
    results = some_function(1, some_kwarg=2)

    assert results == (1, 2)


def test_func_call_with_advice(some_function, advice):
    some_function.join(advice)

    results = some_function(1, some_kwarg=2)

    assert results == ((1, 2), 'ADDITIONAL')


def test_points_join(some_function, some_cls, points, advice):
    points.join(advice)

    service = some_cls()
    cls_results = service.some_method(1, some_kwarg=2)
    func_results = some_function(1, some_kwarg=2)

    assert cls_results == ((1, 2), 'ADDITIONAL')
    assert func_results == ((1, 2), 'ADDITIONAL')
