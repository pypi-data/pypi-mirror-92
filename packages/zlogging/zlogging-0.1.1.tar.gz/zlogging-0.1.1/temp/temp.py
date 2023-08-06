from typing import *

T = TypeVar('T')
S = TypeVar('S')


def a_fun(x: T) -> None:
    # this is OK
    y = []  # type: List[T]
    # but below is an error!
    y = []  # type: List[S]


class Bar(Generic[T]):
    # this is also an error
    an_attr = []  # type: List[S]

    def do_something(x: S) -> S:  # this is OK though
        ...
