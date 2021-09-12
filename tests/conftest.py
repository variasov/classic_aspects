from unittest.mock import Mock

import pytest

from classic.aspects import PointCut


@pytest.fixture
def some_cls():
    join_point = PointCut()

    class SomeCls:

        @join_point
        def some_method(self, some_arg, some_kwarg=None):
            return some_arg, some_kwarg

    return SomeCls


@pytest.fixture
def some_cls_with_error():
    join_point = PointCut()

    class SomeClsWithError:
        error = ValueError()

        @join_point
        def some_method(self, some_arg, some_kwarg=None):
            raise self.error

    return SomeClsWithError


@pytest.fixture
def some_function():
    join_point = PointCut()

    @join_point
    def function(some_arg, some_kwarg=None):
        return some_arg, some_kwarg

    return function


@pytest.fixture
def some_function_with_error():
    join_point = PointCut()
    error = ValueError()

    @join_point
    def function():
        raise error

    return error, function


@pytest.fixture
def advice_before():
    return Mock()


@pytest.fixture
def advice_after():
    return Mock()


@pytest.fixture
def advice_on_exception():
    return Mock()
