from xdr_parser.data_types.identifier import Identifier

from xdr_parser.data_types.declarations.declaration import Declaration


class String(Declaration):
    __slots__ = ("identifier", "length")

    def __init__(self, identifier: Identifier, length: int, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.length = length

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.length == other.length

    def __repr__(self) -> str:
        return "<String identifier={identifier}, length={length}>".format(
            identifier=self.identifier, length=self.length
        )
