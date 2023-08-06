# -*- coding: utf-8 -*-

from functools import wraps
from typing import Any, Callable, List, TypeVar, cast

from _thread import LockType as _MutexType
from _thread import allocate_lock as _create_mutex
from _thread import start_new_thread as _start_thread

__all__: List[str] = ["synchronized", "threaded"]

_F = TypeVar("_F", bound=Callable[..., Any])


def synchronized(user_function: _F) -> _F:
    """
    A decorator to synchronize a ``user_function``.
    """
    mutex: _MutexType = _create_mutex()

    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with mutex:
            return user_function(*args, **kwargs)

    return cast(_F, wrapper)


def threaded(user_function: _F) -> Callable[..., int]:
    """
    A decorator to run a ``user_function`` in a separate thread.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        return _start_thread(user_function, args, kwargs)

    return wrapper
