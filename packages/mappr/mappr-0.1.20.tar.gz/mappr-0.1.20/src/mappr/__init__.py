""" A conversion system to ease converting between different types.

This will be especially useful types <-> models conversions.
"""
from .conversion import convert, register, TypeConverter        # noqa: F401
from .exc import ConverterAlreadyExists, Error, NoConverter     # noqa: F401
from .iterators import field_iterator, iter_fields              # noqa: F401
from .mappers import map_directly, set_const, use_default       # noqa: F401
from .types import FieldIterator, MappingFn, ConverterFn        # noqa: F401

__version__ = '0.1.20'
