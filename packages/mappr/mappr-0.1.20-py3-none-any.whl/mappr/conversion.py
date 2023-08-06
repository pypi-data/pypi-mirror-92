from typing import Any, List, Optional, Type, TypeVar

from . import exc, iterators, mappers, types


T = TypeVar('T')


class TypeConverter:
    def __init__(
        self,
        src_type: Type,
        dst_type: Type,
        *,
        mapping: Optional[types.FieldMapping] = None
    ):
        self.src_type = src_type
        self.dst_type = dst_type
        self.mapping = mapping or {}

    def convert(self, src_obj: Any) -> Any:
        values = {}

        for name in iterators.iter_fields(self.dst_type):
            mapping_fn = self.mapping.get(name, mappers.map_directly)

            if mapping_fn != mappers.use_default:
                values[name] = mapping_fn(src_obj, name)

        return self.dst_type(**values)


g_converters: List[TypeConverter] = []


def convert(dst_type: Type[T], src_obj, strict: bool = True) -> T:
    """ Convert an object to a given type.

    Args:
        dst_type:   Target type. This is the type of the return value.
        src_obj:    An object to convert. A registered converter will be used
                    to map between the attributes of this object and the target
                    type.
        strict:     If set to ``False`` and the converter is not found for the
                    given type pair, it will create an ad-hoc one that maps
                    the attributes by their name. Defaults to ``True``

    Returns:
        A newly created instance of ``dst_type`` with values initialized
        from ``src_obj``.
    """
    converter = _get_converter(src_obj.__class__, dst_type, strict=strict)
    return converter.convert(src_obj)


def register(src, dst, mapping: Optional[types.FieldMapping] = None):
    """ Register new converter.

    Args:
        src:
        dst:
        mapping:

    Returns:

    """
    existing = _find_converter(src, dst)
    if existing:
        raise exc.ConverterAlreadyExists(src, dst)

    g_converters.append(TypeConverter(
        src_type=src,
        dst_type=dst,
        mapping=mapping or {},
    ))


def _get_converter(src_type: Type, dst_type: Type[T], strict: bool) -> TypeConverter:
    """ Do everything to return a converter or raise if it's not possible.

    In **strict** mode, it will not create an ad-hoc default converter and will
    require the converter to have been registered earlier.
    """
    converter = _find_converter(src_type, dst_type)
    if converter:
        return converter
    elif not strict:
        # If not strict, create an ad-hoc converter for the types. This will try
        # to map the properties from `dst_type` to src_type. `dst_types` attributes
        # must be a subset of `src_type` attributes.
        return TypeConverter(src_type=src_type, dst_type=dst_type)
    else:
        raise exc.NoConverter(src_type, dst_type)


def _find_converter(src_type, dst_type) -> Optional[TypeConverter]:
    return next(
        (c for c in g_converters if c.src_type == src_type and c.dst_type == dst_type),
        None
    )
