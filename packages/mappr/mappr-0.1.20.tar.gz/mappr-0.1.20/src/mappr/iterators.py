from typing import Any, Callable, List, Optional, Type

from . import types


g_field_iterators: List[types.FieldIter] = []


def field_iterator(test=types.TestFn):
    def decorator(fn: Callable[[Any], types.FieldIterator]):
        g_field_iterators.append(types.FieldIter(test=test, iter_factory=fn))
        return fn
    return decorator


def iter_fields(any_cls: Type):
    field_iter = _find_field_iter(any_cls)
    if field_iter:
        yield from field_iter.make_iterator(any_cls)


def _find_field_iter(any_cls: Type) -> Optional[types.FieldIter]:
    return next(
        (x for x in g_field_iterators if x.can_handle(any_cls)),
        None
    )


# All imports below are are optional and add support for various popular
# libraries out of the box.
try:
    from .integrations import dataclasses   # noqa: F401
except ImportError:
    pass

try:
    from .integrations import pydantic   # noqa: F401
except ImportError:
    pass

try:
    from .integrations import sqlalchemy   # noqa: F401
except ImportError:
    pass
