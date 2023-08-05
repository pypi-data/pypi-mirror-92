import dataclasses
from typing import Any, Callable, Dict, Iterator, Type

ConverterFn = Callable[[Any], Any]
MappingFn = Callable[[Any, str], Any]
FieldMapping = Dict[str, MappingFn]
FieldIterator = Iterator[str]
TestFn = Callable[[Type], bool]


@dataclasses.dataclass
class FieldIter:
    test: TestFn
    iter: Callable[[Type], FieldIterator]

    def can_handle(self, any_cls: Type) -> bool:
        # We need to use getattr as using self.test will call test as a method
        # (passing self as first argument). At least mypy reports that.
        # TODO: Look into whether this is just a mypy issue.
        return getattr(self, 'test')(any_cls)

    def make_iterator(self, any_cls: Type) -> FieldIterator:
        return getattr(self, 'iter')(any_cls)
