from typing import Optional


class Error(Exception):
    msg: str

    def __init__(
        self,
        *args,
        detail: Optional[str] = None,
        **kw
    ):
        super(Error, self).__init__(
            self.msg.format(*args, **kw) + (f": {detail}" if detail else '')
        )

        self.detail = detail
        self.args = args
        self.kwargs = kw


class ConverterAlreadyExists(Error):
    status = 500
    msg = "Converter already exists for {0.__name__} -> {1.__name__}"


class NoConverter(Error):
    status = 500
    msg = "Converter missing for {0.__name__} -> {1.__name__}"
