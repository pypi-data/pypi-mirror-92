from xdr_parser.data_types.identifier import Identifier
from xdr_parser.data_types.specifiers.specifier import Specifier


class Opaque(Specifier):
    __slots__ = ("identifier", "fixed", "length")

    def __init__(self, identifier: Identifier, length: int, fixed: bool, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.length = length
        self.fixed = fixed

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.length == other.length
            and self.fixed == other.fixed
        )

    def __repr__(self) -> str:
        return "<Opaque identifier={identifier}, length={length}, fixed={fixed}>".format(
            identifier=self.identifier, length=self.length, fixed=self.fixed
        )
