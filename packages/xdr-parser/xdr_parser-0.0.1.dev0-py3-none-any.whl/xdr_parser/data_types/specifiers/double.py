from xdr_parser.data_types.specifiers.specifier import Specifier


class Double(Specifier):
    __slots__ = ()

    def __init__(self, source: str):
        super().__init__(source)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return True

    def __repr__(self) -> str:
        return "<Double>"
