from xdr_parser.data_types.declarations.declaration import Declaration


class Void(Declaration):
    __slots__ = ()

    def __init__(self, source: str):
        super().__init__(source)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return True

    def __repr__(self) -> str:
        return "<Void>"
