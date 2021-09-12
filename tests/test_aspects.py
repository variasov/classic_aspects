from unittest.mock import Mock

import pytest


def test_cls_call(some_cls):
    instance = some_cls()

    results = instance.some_method(1, some_kwarg=2)

    assert results == (1, 2)


def test_call_with_instead(some_cls):
    advice = Mock(return_value=None)
    some_cls.some_method.instead(advice)
    instance = some_cls()

    result = instance.some_method(1, some_kwarg=2)

    assert result is None


def test_cls_success_call_with_advice(some_cls,
                                      advice_before: Mock,
                                      advice_after: Mock,
                                      advice_on_exception: Mock):
    service = some_cls()
    service.some_method.before(advice_before)
    service.some_method.after(advice_after)
    service.some_method.on_exception(advice_on_exception)

    results = service.some_method(1, some_kwarg=2)

    assert results == (1, 2)

    advice_before.assert_called_once_with(service, 1, some_kwarg=2)
    advice_after.assert_called_once_with(service, 1, some_kwarg=2)
    advice_on_exception.assert_not_called()


def test_cls_error_call_with_advice(some_cls_with_error,
                                    advice_before: Mock,
                                    advice_after: Mock,
                                    advice_on_exception: Mock):
    service = some_cls_with_error()
    service.some_method.before(advice_before)
    service.some_method.after(advice_after)
    service.some_method.on_exception(advice_on_exception)

    with pytest.raises(ValueError):
        service.some_method(1, some_kwarg=2)

    advice_before.assert_called_once_with(service, 1, some_kwarg=2)
    advice_after.assert_not_called()
    advice_on_exception.assert_called_once_with(
        service.error, service, 1, some_kwarg=2,
    )


def test_func_call(some_function):
    results = some_function(1, some_kwarg=2)

    assert results == (1, 2)


def test_func_success_call_with_advice(some_function,
                                       advice_before: Mock,
                                       advice_after: Mock,
                                       advice_on_exception: Mock):
    some_function.before(advice_before)
    some_function.after(advice_after)
    some_function.on_exception(advice_on_exception)

    results = some_function(1, some_kwarg=2)

    assert results == (1, 2)

    advice_before.assert_called_once_with(1, some_kwarg=2)
    advice_after.assert_called_once_with(1, some_kwarg=2)
    advice_on_exception.assert_not_called()


def test_func_error_call_with_advice(some_function_with_error,
                                     advice_before: Mock,
                                     advice_after: Mock,
                                     advice_on_exception: Mock):
    error, function = some_function_with_error
    function.before(advice_before)
    function.after(advice_after)
    function.on_exception(advice_on_exception)

    with pytest.raises(ValueError):
        function()

    advice_before.assert_called_once()
    advice_after.assert_not_called()
    advice_on_exception.assert_called_once_with(error)
