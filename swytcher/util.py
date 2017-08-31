"""Util functions"""
import logging
from contextlib import wraps  # type: ignore
from typing import Type


def suppress_err(
        exception: Type[Exception], logger: logging.Logger=None,
        level=logging.WARNING, traceback=False):
    """Decorator that will catch `exception`, suppress it, and optionally log
    it with a traceback through the logger.

    Usage example:

        >>> @exception_handler(TypeError, log, "my msg")
            def func():
                return 'a' + 1

        >>> func()
        'WARNING [Can't convert 'int' object to str implicitly'] my msg

        E.g., it will be equivalent to implementing 'func' as:

        >>> def func():
                try:
                    return 'a' + 1
                except TypeError as err:
                    logging.error("You can't do that: %s", err)

        Multiple exceptions can be handled by just adding more decorators:

        >>> @exception_handler(TypeError, log, "You can't do that")
            @exception_handler(AttributeError, log, "You can't do that")
            def func():
                return 'a' + 1
    """
    def wrapper(func):
        """Wrapper for func"""
        @wraps(func)
        def inner(*args, **kwargs):
            """Inner function that actually calls func"""
            try:
                return func(*args, **kwargs)
            except exception as err:
                if logger:
                    logger.log(
                        level, "%r", err, exc_info=1 if traceback else 0)
        return inner
    return wrapper
