import dataclasses
from typing import Any, Callable, cast, List, Optional, Type

from . import types


g_field_iterators: List[types.FieldIter] = []


def field_iterator(test=types.TestFn):
    def decorator(fn: Callable[[Any], types.FieldIterator]):
        g_field_iterators.append(types.FieldIter(test=test, iter=fn))
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


@field_iterator(test=lambda cls: dataclasses.is_dataclass(cls))
def _dataclass_iter_fields(model_cls: Type) -> types.FieldIterator:
    for field in dataclasses.fields(model_cls):
        yield field.name


@field_iterator(test=lambda cls: hasattr(cls, '__table__'))
def _sa_model_iter_fields(model_cls: Type) -> types.FieldIterator:
    yield from model_cls.__table__.columns.keys()


try:
    # Optional pydantic support.
    # Does not require pydantic as it's not a dependency, but if installed it
    # will support it out of the box.
    import pydantic

    @field_iterator(test=lambda cls: issubclass(cls, pydantic.BaseModel))
    def _pydantic_iter_fields(model_cls: Type) -> types.FieldIterator:
        pydantic_model = cast(pydantic.BaseModel, model_cls)
        yield from pydantic_model.__fields__.keys()

except ImportError:
    pass
